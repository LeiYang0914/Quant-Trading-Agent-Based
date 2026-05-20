"""LLM Router — core routing engine.

Accepts TaskRequests, applies routing rules, selects provider/model,
checks cache, rate limits, circuit breaker, invokes provider, handles fallback.
"""

import hashlib
import logging
import time
import uuid
from pathlib import Path
from typing import Any, Optional

import yaml

from .prompts.task_classifier import (
    classify_task,
    infer_complexity,
    infer_cost_sensitivity,
    infer_long_context,
)
from .providers.base import BaseProvider
from .types import (
    Complexity,
    Domain,
    LLMResponse,
    ProviderName,
    RoutingDecision,
    TaskRequest,
    TaskType,
)
from .utils.cache import ResponseCache
from .utils.circuit_breaker import CircuitBreaker
from .utils.cost_estimator import estimate_cost
from .utils.logging import RoutingLogger
from .utils.rate_limiter import RateLimiter
from .utils.usage_tracker import UsageTracker

logger = logging.getLogger("llm_router")

# Tasks that MUST use Claude (or equivalent high-capability model).
_CLAUDE_DEFAULT_TASKS: set[TaskType] = {
    TaskType.SYSTEM_ARCHITECTURE,
    TaskType.RESEARCH_REASONING,
    TaskType.PAPER_ANALYSIS,
    TaskType.ALPHA_IDEA_GENERATION,
    TaskType.CODE_PLANNING,
    TaskType.CODE_GENERATION,
    TaskType.CODE_REVIEW,
    TaskType.DEBUGGING,
    TaskType.RISK_REVIEW,
    TaskType.MEMO_WRITING,
}

# Tasks that SHOULD use DeepSeek (or equivalent cost-efficient model).
_DEEPSEEK_DEFAULT_TASKS: set[TaskType] = {
    TaskType.SUMMARIZATION,
    TaskType.TEXT_CLEANUP,
    TaskType.WEB_SOURCE_SCREENING,
    TaskType.DATA_GRABBING,
    TaskType.GIT_ACTIVITY_SUMMARY,
    TaskType.CLASSIFICATION,
    TaskType.MEMORY_UPDATE,
}

# Task types that must never fallback to a lower-capability model.
_NO_CODE_FALLBACK_TASKS: set[TaskType] = {
    TaskType.CODE_GENERATION,
    TaskType.CODE_PLANNING,
    TaskType.CODE_REVIEW,
    TaskType.DEBUGGING,
    TaskType.RISK_REVIEW,
}

# Agents that should always prefer Claude.
_CLAUDE_PREFERRED_AGENTS: set[str] = {
    "review-agent",
    "risk-agent",
    "programmer-agent",
}


class LLMRouter:
    """Routes LLM task requests to the appropriate provider and model.

    Features:
    - Task classification and routing
    - Response caching (with exclusions for code/risk)
    - Rate limiting per provider
    - Circuit breaker for provider failures
    - Usage and cost tracking
    - Dry-run mode for testing
    - Health checks
    - Convenience ask() method
    """

    def __init__(
        self,
        models_config_path: str = "configs/llm/models.yaml",
        routing_rules_path: Optional[str] = "configs/llm/routing_rules.yaml",
        dry_run: bool = True,
        log_dir: Optional[Path] = None,
    ):
        self.dry_run = dry_run
        self.log_dir = Path(log_dir) if log_dir else Path("reports/llm_routing")

        self.models_config = self._load_yaml(models_config_path)
        self.routing_rules = self._load_yaml(routing_rules_path) if routing_rules_path else {}

        self.claude = self._build_provider("claude")
        self.deepseek = self._build_provider("deepseek")

        self.routing_logger = RoutingLogger(self.log_dir)

        # Cache
        cache_cfg = self.models_config.get("cache", {})
        self.cache = ResponseCache(
            cache_dir=cache_cfg.get("cache_dir", ".cache/llm"),
            ttl_seconds=cache_cfg.get("ttl_seconds", 86400),
            max_entries=cache_cfg.get("max_entries", 10000),
            enabled=cache_cfg.get("enabled", True) and not dry_run,
        )

        # Rate limiter
        self.rate_limiter = RateLimiter(self.models_config.get("rate_limits", {}))

        # Circuit breaker
        self.circuit_breaker = CircuitBreaker(self.models_config.get("circuit_breaker", {}))

        # Usage tracker
        self.usage_tracker = UsageTracker()

        logger.info("LLMRouter initialized (dry_run=%s)", dry_run)
        logger.info("Claude models: %s", self.claude.available_models)
        logger.info("DeepSeek models: %s", self.deepseek.available_models)
        logger.info("Cache: %s (entries=%d)", "enabled" if self.cache.enabled else "disabled", self.cache.size)
        logger.info("Rate limiter: claude=%s deepseek=%s",
                    self.rate_limiter.remaining("claude"),
                    self.rate_limiter.remaining("deepseek"))

    # ==================================================================
    # Public API
    # ==================================================================

    def route(self, request: TaskRequest) -> LLMResponse:
        """Route a TaskRequest, select provider/model, invoke, handle fallback.

        This is the primary entry point called by agents.
        """
        decision = self._make_decision(request)
        self.routing_logger.log_decision(request, decision)

        response = self._invoke_with_guards(request, decision)

        # Fallback on failure
        if not response.success and request.fallback_allowed and decision.fallback_provider:
            if not self._fallback_allowed_for_task(request.task_type, request.requires_code, request.agent_name):
                logger.warning(
                    "Fallback blocked for task_type=%s requires_code=%s",
                    request.task_type.value,
                    request.requires_code,
                )
                self._record_usage(request, decision, response)
                return response

            # Check if fallback provider is available
            fb_provider = decision.fallback_provider
            if not self.circuit_breaker.allow_request(fb_provider.value):
                logger.warning("Fallback provider %s circuit open — cannot fallback", fb_provider.value)
                self._record_usage(request, decision, response)
                return response

            if not self.rate_limiter.acquire(fb_provider.value):
                logger.warning("Fallback provider %s rate limited — cannot fallback", fb_provider.value)
                self._record_usage(request, decision, response)
                return response

            fallback_decision = self._make_fallback_decision(request, decision)
            self.routing_logger.log_fallback(request, decision, fallback_decision, response.error or "provider_error")
            fallback_response = self._do_invoke(request, fallback_decision)
            fallback_response.fallback_used = True
            fallback_response.routing_decision = fallback_decision
            self.routing_logger.log_response(request, fallback_decision, fallback_response)
            self._record_usage(request, fallback_decision, fallback_response)
            self._update_circuit(fallback_response, fallback_decision.selected_provider.value)
            return fallback_response

        self.routing_logger.log_response(request, decision, response)
        self._record_usage(request, decision, response)
        self._update_circuit(response, decision.selected_provider.value)
        return response

    def ask(
        self,
        prompt: str,
        agent_name: str = "unknown",
        task_type: Optional[TaskType] = None,
        domain: Optional[Domain] = None,
        complexity: Optional[Complexity] = None,
        metadata: Optional[dict[str, Any]] = None,
        **kwargs,
    ) -> LLMResponse:
        """Convenience method: auto-classify and route a prompt.

        If task_type is not provided, it is inferred from the prompt.
        If complexity is not provided, it is inferred.
        """
        meta = metadata or {}
        if task_type is None:
            task_type = classify_task(prompt, agent_name=agent_name, metadata=meta)
        if complexity is None:
            requires_code = kwargs.get("requires_code", task_type.value.startswith("CODE"))
            long_ctx = kwargs.get("requires_long_context", infer_long_context(prompt, meta))
            complexity = infer_complexity(prompt, task_type, requires_code=requires_code, long_context=long_ctx, metadata=meta)

        request = TaskRequest(
            task_id=meta.get("task_id", f"ask-{uuid.uuid4().hex[:12]}"),
            agent_name=agent_name,
            task_type=task_type,
            prompt=prompt,
            domain=domain or meta.get("domain", Domain.SYSTEM),
            complexity=complexity,
            requires_code=kwargs.get("requires_code", task_type.value.startswith("CODE")),
            requires_long_context=kwargs.get("requires_long_context", infer_long_context(prompt, meta)),
            cost_sensitive=kwargs.get("cost_sensitive", infer_cost_sensitivity(task_type, complexity, meta)),
            timeout_seconds=kwargs.get("timeout_seconds", 120),
            preferred_provider=kwargs.get("preferred_provider"),
            fallback_allowed=kwargs.get("fallback_allowed", True),
            metadata=meta,
        )
        return self.route(request)

    def dry_run_route(self, request: TaskRequest) -> LLMResponse:
        """Route in dry-run mode regardless of the router's dry_run setting."""
        prev = self.dry_run
        self.dry_run = True
        try:
            return self.route(request)
        finally:
            self.dry_run = prev

    def health_check(self) -> dict[str, Any]:
        """Return structured health status for all providers."""
        result: dict[str, Any] = {}
        # Claude
        claude_details = self.claude.health_details() if hasattr(self.claude, "health_details") else {}
        result["claude"] = {
            "available": self.claude.health_check(),
            "reason": claude_details.get("reason", "unknown"),
            "configured_models": claude_details.get("configured_models", self.claude.available_models),
            "circuit_state": self.circuit_breaker.get_state("claude"),
            "rate_limit_remaining": self.rate_limiter.remaining("claude"),
        }
        # DeepSeek
        deepseek_details = self.deepseek.health_details() if hasattr(self.deepseek, "health_details") else {}
        result["deepseek"] = {
            "available": self.deepseek.health_check(),
            "reason": deepseek_details.get("reason", "unknown"),
            "configured_models": deepseek_details.get("configured_models", self.deepseek.available_models),
            "circuit_state": self.circuit_breaker.get_state("deepseek"),
            "rate_limit_remaining": self.rate_limiter.remaining("deepseek"),
        }
        return result

    def get_usage_summary(self) -> dict[str, Any]:
        """Return aggregated usage statistics."""
        return {
            "total_calls": self.usage_tracker.get_total_calls(),
            "total_cost": round(self.usage_tracker.get_total_cost(), 6),
            "cost_by_agent": self.usage_tracker.get_cost_by_agent(),
            "cost_by_provider": self.usage_tracker.get_cost_by_provider(),
            "cost_by_task_type": self.usage_tracker.get_cost_by_task_type(),
            "cache_hit_ratio": round(self.usage_tracker.get_cache_hit_ratio(), 4),
            "fallback_ratio": round(self.usage_tracker.get_fallback_ratio(), 4),
            "success_rate": round(self.usage_tracker.get_success_rate(), 4),
            "recent_calls": self.usage_tracker.get_recent_usage(20),
        }

    def clear_cache(self) -> int:
        """Clear the response cache. Returns count of entries removed."""
        return self.cache.clear()

    def clear_usage(self) -> int:
        """Clear usage records. Returns count removed."""
        return self.usage_tracker.clear()

    def reset_circuits(self) -> None:
        """Reset all circuit breakers."""
        self.circuit_breaker.reset()

    def reset_rate_limiters(self) -> None:
        """Reset all rate limiters."""
        self.rate_limiter.reset()

    # ==================================================================
    # Internal: invoke pipeline
    # ==================================================================

    def _invoke_with_guards(self, request: TaskRequest, decision: RoutingDecision) -> LLMResponse:
        """Check cache → rate limit → circuit breaker → invoke."""
        provider_name = decision.selected_provider.value

        # 1. Cache lookup
        if not request.metadata.get("no_cache"):
            cached = self.cache.get(request, provider_name, decision.selected_model)
            if cached is not None:
                cached.routing_decision = decision
                logger.debug("CACHE HIT | task=%s provider=%s", request.task_id, provider_name)
                return cached

        # 2. Circuit breaker
        if not self.circuit_breaker.allow_request(provider_name):
            return LLMResponse(
                task_id=request.task_id,
                success=False,
                provider=decision.selected_provider,
                model=decision.selected_model,
                error=f"Circuit breaker open for {provider_name}",
                routing_decision=decision,
            )

        # 3. Rate limiter
        if not self.rate_limiter.acquire(provider_name):
            # If rate limited and fallback available, let route() handle it
            if request.fallback_allowed and decision.fallback_provider:
                fb = decision.fallback_provider
                if self.circuit_breaker.allow_request(fb.value) and self.rate_limiter.acquire(fb.value):
                    logger.info("Rate limited on %s, attempting fallback to %s", provider_name, fb.value)
                    # The route() method will handle fallback
            return LLMResponse(
                task_id=request.task_id,
                success=False,
                provider=decision.selected_provider,
                model=decision.selected_model,
                error=f"Rate limit exceeded for {provider_name}",
                routing_decision=decision,
                rate_limited=True,
            )

        return self._do_invoke(request, decision)

    def _do_invoke(self, request: TaskRequest, decision: RoutingDecision) -> LLMResponse:
        """Actually call the provider (or return dry-run placeholder)."""
        provider = self._get_provider(decision.selected_provider)
        if provider is None:
            return LLMResponse(
                task_id=request.task_id,
                success=False,
                provider=decision.selected_provider,
                model=decision.selected_model,
                error=f"Unknown provider: {decision.selected_provider}",
                routing_decision=decision,
            )

        if self.dry_run:
            response = LLMResponse(
                task_id=request.task_id,
                success=True,
                provider=decision.selected_provider,
                model=decision.selected_model,
                content="[DRY RUN — no actual API call]",
                routing_decision=decision,
                latency_ms=0,
                latency_seconds=0.0,
            )
            return response

        t0 = time.monotonic()
        result = provider.call(
            prompt=request.prompt,
            model=decision.selected_model,
            max_tokens=decision.max_tokens,
            temperature=decision.temperature,
            timeout_seconds=decision.timeout_seconds,
        )
        latency_ms = int((time.monotonic() - t0) * 1000)
        latency_s = round(latency_ms / 1000, 3)

        response = LLMResponse(
            task_id=request.task_id,
            success=result["success"],
            provider=decision.selected_provider,
            model=result.get("model", decision.selected_model),
            content=result.get("content"),
            error=result.get("error"),
            routing_decision=decision,
            latency_ms=latency_ms or result.get("latency_ms", 0),
            latency_seconds=latency_s or result.get("latency_seconds"),
            input_tokens=result.get("input_tokens"),
            output_tokens=result.get("output_tokens"),
            estimated_tokens=result.get("estimated_tokens", True),
            estimated_cost=result.get("estimated_cost"),
        )

        # Write to cache on success
        if response.success and not request.metadata.get("no_cache"):
            self.cache.put(request, decision.selected_provider.value, decision.selected_model, response)

        return response

    # ==================================================================
    # Decision logic
    # ==================================================================

    def _make_decision(self, request: TaskRequest) -> RoutingDecision:
        """Apply routing rules to produce a RoutingDecision."""
        # 1. Explicit preferred provider
        if request.preferred_provider:
            return self._decision_for(request.preferred_provider, request, "explicitly preferred")

        # 2. Agent-level override: Review, Risk, Programmer prefer Claude
        if request.agent_name.lower().strip() in _CLAUDE_PREFERRED_AGENTS:
            return self._decision_for(ProviderName.CLAUDE, request, f"agent={request.agent_name} prefers Claude")

        # 3. Task is in Claude-default set
        if request.task_type in _CLAUDE_DEFAULT_TASKS:
            return self._decision_for(ProviderName.CLAUDE, request, f"task_type={request.task_type.value} → Claude default")

        # 4. Task is in DeepSeek-default set
        if request.task_type in _DEEPSEEK_DEFAULT_TASKS:
            return self._decision_for(ProviderName.DEEPSEEK, request, f"task_type={request.task_type.value} → DeepSeek default")

        # 5. Risk review always Claude
        if request.task_type == TaskType.RISK_REVIEW:
            return self._decision_for(ProviderName.CLAUDE, request, "RISK_REVIEW always → Claude")

        # 6. Dynamic overrides
        if request.requires_code:
            return self._decision_for(ProviderName.CLAUDE, request, "requires_code=true → Claude")

        if request.complexity == Complexity.HIGH:
            return self._decision_for(ProviderName.CLAUDE, request, "complexity=high → Claude")

        if request.requires_long_context:
            return self._decision_for(ProviderName.CLAUDE, request, "requires_long_context=true → Claude")

        if request.cost_sensitive and request.complexity == Complexity.LOW:
            return self._decision_for(ProviderName.DEEPSEEK, request, "cost_sensitive + low complexity → DeepSeek")

        if request.cost_sensitive:
            return self._decision_for(ProviderName.DEEPSEEK, request, "cost_sensitive → DeepSeek")

        # 7. Default: Claude for safety on anything ambiguous
        return self._decision_for(ProviderName.CLAUDE, request, "default → Claude (safety)")

    def _make_fallback_decision(
        self,
        request: TaskRequest,
        failed_decision: RoutingDecision,
    ) -> RoutingDecision:
        """When primary provider fails, decide where to fall back."""
        primary = failed_decision.selected_provider

        if primary == ProviderName.CLAUDE:
            if request.task_type in _NO_CODE_FALLBACK_TASKS:
                logger.warning("Code/risk task %s cannot fallback Claude→DeepSeek", request.task_id)
            return self._decision_for(
                ProviderName.DEEPSEEK,
                request,
                "Claude failed, fallback to DeepSeek",
                use_stronger=True,
            )

        return self._decision_for(
            ProviderName.CLAUDE,
            request,
            "DeepSeek failed, fallback to Claude",
        )

    def _decision_for(
        self,
        provider: ProviderName,
        request: TaskRequest,
        reason: str,
        use_stronger: bool = False,
    ) -> RoutingDecision:
        """Build a RoutingDecision for a given provider."""
        if provider == ProviderName.CLAUDE:
            model = self._choose_claude_model(request, use_stronger)
            fallback_provider = ProviderName.DEEPSEEK
            fallback_model = self._choose_deepseek_model(request, stronger=True)
        else:
            model = self._choose_deepseek_model(request, stronger=use_stronger)
            fallback_provider = ProviderName.CLAUDE
            fallback_model = self._choose_claude_model(request, stronger=True)

        max_tokens = self._resolve_max_tokens(request)
        temperature = self._resolve_temperature(request)
        timeout = request.timeout_seconds or self._provider_timeout(provider)
        cacheable = not request.metadata.get("no_cache", False) and request.task_type not in {
            TaskType.CODE_GENERATION, TaskType.CODE_PLANNING, TaskType.CODE_REVIEW,
            TaskType.DEBUGGING, TaskType.RISK_REVIEW,
        }

        return RoutingDecision(
            selected_provider=provider,
            selected_model=model,
            reason=reason,
            fallback_provider=fallback_provider,
            fallback_model=fallback_model,
            estimated_cost_level=estimate_cost(provider, model, len(request.prompt), max_tokens)["level"],
            max_tokens=max_tokens,
            temperature=temperature,
            timeout_seconds=timeout,
            cacheable=cacheable,
        )

    # ==================================================================
    # Model selection
    # ==================================================================

    def _choose_claude_model(self, request: TaskRequest, stronger: bool = False) -> str:
        cfg = self.models_config.get("claude", {})
        # Check task-specific override
        overrides = self.models_config.get("task_model_overrides", {})
        for task_key in [request.task_type.value, request.task_type.value.lower()]:
            if task_key in overrides and "claude" in overrides[task_key]:
                return overrides[task_key]["claude"]
        if request.complexity == Complexity.HIGH or request.requires_long_context or stronger:
            return cfg.get("complex_model", cfg.get("default_model", "claude-sonnet-4-6"))
        return cfg.get("default_model", "claude-sonnet-4-6")

    def _choose_deepseek_model(self, request: TaskRequest, stronger: bool = False) -> str:
        cfg = self.models_config.get("deepseek", {})
        if request.complexity == Complexity.HIGH or stronger:
            return cfg.get("stronger_model", cfg.get("default_model", "deepseek-v4-pro"))
        return cfg.get("default_model", "deepseek-v4-flash")

    # ==================================================================
    # Helpers
    # ==================================================================

    def _resolve_max_tokens(self, request: TaskRequest) -> int:
        if request.requires_long_context:
            return 8192
        if request.complexity == Complexity.HIGH:
            return 8192
        return 4096

    def _resolve_temperature(self, request: TaskRequest) -> float:
        creative_tasks = {TaskType.ALPHA_IDEA_GENERATION, TaskType.RESEARCH_REASONING, TaskType.MEMO_WRITING}
        return 0.7 if request.task_type in creative_tasks else 0.3

    def _provider_timeout(self, provider: ProviderName) -> int:
        cfg = self.models_config.get(provider.value, {})
        return cfg.get("timeout_seconds", 120)

    def _fallback_allowed_for_task(self, task_type: TaskType, requires_code: bool, agent_name: str = "") -> bool:
        # Hardcoded defaults
        if task_type in _NO_CODE_FALLBACK_TASKS:
            return False
        if requires_code:
            return False

        # Read forbidden_fallback from routing_rules.yaml if present
        fb_cfg = self.routing_rules.get("forbidden_fallback", {})
        if fb_cfg.get("no_fallback_if_code_required") and requires_code:
            return False
        no_fb_tasks = fb_cfg.get("no_fallback_tasks", [])
        if task_type.value in no_fb_tasks:
            return False
        if fb_cfg.get("risk_never_low_cost") and task_type == TaskType.RISK_REVIEW:
            return False
        no_fb_agents = fb_cfg.get("no_fallback_agents", [])
        if no_fb_agents and any(a in agent_name.lower() for a in no_fb_agents):
            return False

        return True

    def _record_usage(
        self,
        request: TaskRequest,
        decision: RoutingDecision,
        response: LLMResponse,
    ) -> None:
        """Record usage after a provider call (or dry run)."""
        self.usage_tracker.record(
            task_id=request.task_id,
            agent_name=request.agent_name,
            task_type=request.task_type.value,
            provider=decision.selected_provider.value,
            model=decision.selected_model,
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
            estimated_tokens=response.estimated_tokens,
            estimated_cost=response.estimated_cost,
            cache_hit=response.cache_hit,
            fallback_used=response.fallback_used,
            success=response.success,
            latency_ms=response.latency_ms,
            dry_run=self.dry_run,
        )

    def _update_circuit(self, response: LLMResponse, provider: str) -> None:
        """Update circuit breaker state based on call outcome."""
        if response.success:
            self.circuit_breaker.record_success(provider)
        elif not response.cache_hit:
            self.circuit_breaker.record_failure(provider)

    def _get_provider(self, name: ProviderName) -> Optional[BaseProvider]:
        if name == ProviderName.CLAUDE:
            return self.claude
        if name == ProviderName.DEEPSEEK:
            return self.deepseek
        return None

    # ==================================================================
    # Config loading
    # ==================================================================

    def _build_provider(self, name: str) -> BaseProvider:
        cfg = self.models_config.get(name, {})
        if name == "claude":
            from .providers.claude_provider import ClaudeProvider
            return ClaudeProvider(cfg)
        if name == "deepseek":
            from .providers.deepseek_provider import DeepSeekProvider
            return DeepSeekProvider(cfg)
        raise ValueError(f"Unknown provider: {name}")

    @staticmethod
    def _load_yaml(path: str) -> dict[str, Any]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            logger.warning("Config file not found: %s — using defaults", path)
            return {}
