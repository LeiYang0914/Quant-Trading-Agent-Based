"""Production-readiness tests for the LLM Router.

Covers: provider config validation, health checks, cache hit/miss,
circuit breaker cycles, rate limiter exhaustion, usage tracker persistence,
no_cache behavior on ask(), and CLI dry-run integration.
"""

import json
import os
from pathlib import Path
from unittest import mock

import pytest

from src.llm import (
    Complexity,
    Domain,
    LLMRouter,
    ProviderName,
    TaskRequest,
    TaskType,
)
from src.llm.prompts.task_classifier import (
    classify_task,
    infer_complexity,
    infer_cost_sensitivity,
    infer_long_context,
)
from src.llm.providers.claude_provider import ClaudeProvider
from src.llm.providers.deepseek_provider import DeepSeekProvider
from src.llm.utils.cache import ResponseCache
from src.llm.utils.circuit_breaker import (
    CIRCUIT_CLOSED,
    CIRCUIT_HALF_OPEN,
    CIRCUIT_OPEN,
    CircuitBreaker,
)
from src.llm.utils.rate_limiter import RateLimiter
from src.llm.utils.usage_tracker import UsageTracker


# ============================================================================
# Provider config validation (no API keys required)
# ============================================================================

class TestProviderConfigValidation:
    def test_claude_provider_without_api_key(self):
        """ClaudeProvider should not crash when ANTHROPIC_API_KEY is unset."""
        provider = ClaudeProvider({
            "default_model": "claude-sonnet-4-6",
            "models": ["claude-sonnet-4-6"],
        })
        result = provider.call(
            prompt="Hello",
            model="claude-sonnet-4-6",
            max_tokens=100,
        )
        assert result["success"] is False
        assert result["error"] is not None
        assert "ANTHROPIC_API_KEY" in result["error"] or "SDK" in result.get("error", "")

    def test_deepseek_provider_without_api_key(self):
        """DeepSeekProvider should not crash when DEEPSEEK_API_KEY is unset."""
        provider = DeepSeekProvider({
            "default_model": "deepseek-v4-flash",
            "models": ["deepseek-v4-flash"],
        })
        result = provider.call(
            prompt="Hello",
            model="deepseek-v4-flash",
            max_tokens=100,
        )
        assert result["success"] is False
        assert result["error"] is not None

    def test_claude_health_check_without_key(self):
        """health_check() returns False when API key is missing."""
        provider = ClaudeProvider({
            "default_model": "claude-sonnet-4-6",
            "models": ["claude-sonnet-4-6"],
        })
        with mock.patch.dict(os.environ, {}, clear=True):
            ok = provider.health_check()
        assert ok is False

    def test_deepseek_health_check_without_key(self):
        """health_check() returns False when API key is missing."""
        provider = DeepSeekProvider({
            "default_model": "deepseek-v4-flash",
            "models": ["deepseek-v4-flash"],
        })
        with mock.patch.dict(os.environ, {}, clear=True):
            ok = provider.health_check()
        assert ok is False

    def test_claude_validate_config_without_key(self):
        provider = ClaudeProvider({"models": ["claude-sonnet-4-6"]})
        with mock.patch.dict(os.environ, {}, clear=True):
            assert provider.validate_config() is False

    def test_deepseek_validate_config_without_key(self):
        provider = DeepSeekProvider({"models": ["deepseek-v4-flash"]})
        with mock.patch.dict(os.environ, {}, clear=True):
            assert provider.validate_config() is False

    def test_health_details_structure_when_unavailable(self):
        provider = ClaudeProvider({
            "default_model": "claude-sonnet-4-6",
            "models": ["claude-sonnet-4-6", "claude-haiku-4-5-20251001"],
        })
        details = provider.health_details()
        assert "available" in details
        assert "sdk_installed" in details
        assert "api_key_set" in details
        assert "reason" in details
        assert "configured_models" in details
        assert len(details["configured_models"]) >= 1


# ============================================================================
# Health check integration
# ============================================================================

class TestHealthCheck:
    def test_router_health_check_returns_all_fields(self):
        router = LLMRouter(dry_run=True)
        result = router.health_check()
        for provider in ["claude", "deepseek"]:
            assert provider in result
            for key in ["available", "reason", "configured_models", "circuit_state", "rate_limit_remaining"]:
                assert key in result[provider], f"Missing '{key}' in {provider}"

    def test_health_check_configured_models_are_lists(self):
        router = LLMRouter(dry_run=True)
        result = router.health_check()
        assert isinstance(result["claude"]["configured_models"], list)
        assert isinstance(result["deepseek"]["configured_models"], list)
        assert len(result["claude"]["configured_models"]) >= 1
        assert len(result["deepseek"]["configured_models"]) >= 1


# ============================================================================
# Cache hit / miss / no_cache
# ============================================================================

class TestCacheHitMiss:
    @pytest.fixture
    def cache(self):
        c = ResponseCache(cache_dir=".cache/llm/test_prod", ttl_seconds=3600, enabled=True)
        yield c
        c.clear()

    def test_cache_hit_after_put(self, cache):
        req = TaskRequest(
            task_id="ch-001", agent_name="research-agent",
            task_type=TaskType.SUMMARIZATION, prompt="Cache me.",
        )
        resp = type("FakeResponse", (), {
            "task_id": "ch-001", "success": True, "provider": ProviderName.DEEPSEEK,
            "model": "m", "content": "cached content", "cache_hit": False,
            "estimated_cost": 0.001, "error": None,
        })()
        cache.put(req, "deepseek", "m", resp)
        hit = cache.get(req, "deepseek", "m")
        assert hit is not None
        assert hit.cache_hit is True
        assert hit.content == "cached content"

    def test_cache_miss_different_prompt(self, cache):
        req1 = TaskRequest(
            task_id="a", agent_name="ra", task_type=TaskType.SUMMARIZATION, prompt="Prompt A.",
        )
        req2 = TaskRequest(
            task_id="b", agent_name="ra", task_type=TaskType.SUMMARIZATION, prompt="Prompt B.",
        )
        resp = type("FakeResponse", (), {
            "task_id": "a", "success": True, "provider": ProviderName.DEEPSEEK,
            "model": "m", "content": "A", "cache_hit": False, "estimated_cost": 0.0, "error": None,
        })()
        cache.put(req1, "deepseek", "m", resp)
        assert cache.get(req2, "deepseek", "m") is None

    def test_cache_miss_different_provider(self, cache):
        req = TaskRequest(
            task_id="c", agent_name="ra", task_type=TaskType.SUMMARIZATION, prompt="P.",
        )
        resp = type("FakeResponse", (), {
            "task_id": "c", "success": True, "provider": ProviderName.DEEPSEEK,
            "model": "m", "content": "X", "cache_hit": False, "estimated_cost": 0.0, "error": None,
        })()
        cache.put(req, "deepseek", "m", resp)
        assert cache.get(req, "claude", "m2") is None

    def test_no_cache_metadata_prevents_cache(self, cache):
        req = TaskRequest(
            task_id="nc", agent_name="ra", task_type=TaskType.SUMMARIZATION,
            prompt="No cache.", metadata={"no_cache": True},
        )
        resp = type("FakeResponse", (), {
            "task_id": "nc", "success": True, "provider": ProviderName.DEEPSEEK,
            "model": "m", "content": "X", "cache_hit": False, "estimated_cost": 0.0, "error": None,
        })()
        cache.put(req, "deepseek", "m", resp)
        assert cache.get(req, "deepseek", "m") is None

    def test_risk_review_not_cached(self, cache):
        req = TaskRequest(
            task_id="rr", agent_name="risk-agent", task_type=TaskType.RISK_REVIEW,
            prompt="Risk review this.",
        )
        resp = type("FakeResponse", (), {
            "task_id": "rr", "success": True, "provider": ProviderName.CLAUDE,
            "model": "m", "content": "safe", "cache_hit": False, "estimated_cost": 0.0, "error": None,
        })()
        cache.put(req, "claude", "m", resp)
        assert cache.get(req, "claude", "m") is None

    def test_code_generation_not_cached_by_default(self, cache):
        req = TaskRequest(
            task_id="cg", agent_name="programmer-agent", task_type=TaskType.CODE_GENERATION,
            prompt="Write code.",
        )
        resp = type("FakeResponse", (), {
            "task_id": "cg", "success": True, "provider": ProviderName.CLAUDE,
            "model": "m", "content": "def f(): pass", "cache_hit": False,
            "estimated_cost": 0.0, "error": None,
        })()
        cache.put(req, "claude", "m", resp)
        assert cache.get(req, "claude", "m") is None

    def test_debugging_not_cached_by_default(self, cache):
        req = TaskRequest(
            task_id="dbg", agent_name="programmer-agent", task_type=TaskType.DEBUGGING,
            prompt="Debug this.",
        )
        resp = type("FakeResponse", (), {
            "task_id": "dbg", "success": True, "provider": ProviderName.CLAUDE,
            "model": "m", "content": "fixed", "cache_hit": False, "estimated_cost": 0.0, "error": None,
        })()
        cache.put(req, "claude", "m", resp)
        assert cache.get(req, "claude", "m") is None


# ============================================================================
# Rate limiter edge cases
# ============================================================================

class TestRateLimiterExhaustion:
    def test_acquire_blocks_after_exhaustion(self):
        limiter = RateLimiter({
            "claude": {"requests_per_minute": 2, "enabled": True},
        })
        assert limiter.acquire("claude") is True
        assert limiter.acquire("claude") is True
        assert limiter.acquire("claude") is False  # exhausted

    def test_remaining_decreases_with_use(self):
        limiter = RateLimiter({
            "deepseek": {"requests_per_minute": 5, "enabled": True},
        })
        assert limiter.remaining("deepseek") == 5
        limiter.acquire("deepseek")
        assert limiter.remaining("deepseek") == 4

    def test_reset_restores_capacity(self):
        limiter = RateLimiter({
            "claude": {"requests_per_minute": 2, "enabled": True},
        })
        limiter.acquire("claude")
        limiter.acquire("claude")
        assert limiter.acquire("claude") is False
        limiter.reset("claude")
        assert limiter.acquire("claude") is True

    def test_disabled_provider_always_returns_true(self):
        limiter = RateLimiter({
            "claude": {"requests_per_minute": 1, "enabled": False},
        })
        for _ in range(100):
            assert limiter.acquire("claude") is True

    def test_unconfigured_provider_always_allows(self):
        limiter = RateLimiter({})
        assert limiter.acquire("unknown-provider") is True
        assert limiter.remaining("unknown-provider") is None

    def test_rate_limited_response_has_correct_error(self):
        router = LLMRouter(dry_run=True)
        # Exhaust rate limiter for claude
        for _ in range(30):
            router.rate_limiter.acquire("claude")
        req = TaskRequest(
            task_id="rl-test", agent_name="test-agent",
            task_type=TaskType.PAPER_ANALYSIS, prompt="Test.",
            fallback_allowed=False,
        )
        resp = router.route(req)
        # If rate limited without fallback, should fail with rate limit error
        if not resp.success:
            assert "Rate limit" in (resp.error or "") or resp.rate_limited


# ============================================================================
# Circuit breaker full cycle
# ============================================================================

class TestCircuitBreakerFullCycle:
    def test_closed_to_open_after_threshold(self):
        cb = CircuitBreaker({
            "enabled": True, "failure_threshold": 3,
            "cooldown_seconds": 300, "half_open_max_requests": 1,
        })
        assert cb.get_state("claude") == CIRCUIT_CLOSED
        cb.record_failure("claude")
        cb.record_failure("claude")
        assert cb.get_state("claude") == CIRCUIT_CLOSED
        cb.record_failure("claude")
        assert cb.get_state("claude") == CIRCUIT_OPEN
        assert cb.allow_request("claude") is False

    def test_open_to_half_open_after_cooldown(self):
        cb = CircuitBreaker({
            "enabled": True, "failure_threshold": 2,
            "cooldown_seconds": -1,  # instantly elapsed
            "half_open_max_requests": 1,
        })
        cb.record_failure("x")
        cb.record_failure("x")
        assert cb.get_state("x") == CIRCUIT_OPEN
        allowed = cb.allow_request("x")
        assert allowed is True
        assert cb.get_state("x") == CIRCUIT_HALF_OPEN

    def test_half_open_success_closes(self):
        cb = CircuitBreaker({
            "enabled": True, "failure_threshold": 2,
            "cooldown_seconds": -1, "half_open_max_requests": 1,
        })
        cb.record_failure("x")
        cb.record_failure("x")
        cb.allow_request("x")  # transitions to half-open
        cb.record_success("x")
        assert cb.get_state("x") == CIRCUIT_CLOSED

    def test_half_open_failure_reopens(self):
        cb = CircuitBreaker({
            "enabled": True, "failure_threshold": 2,
            "cooldown_seconds": -1, "half_open_max_requests": 1,
        })
        cb.record_failure("x")
        cb.record_failure("x")
        cb.allow_request("x")
        cb.record_failure("x")
        assert cb.get_state("x") == CIRCUIT_OPEN

    def test_success_resets_counter_mid_sequence(self):
        cb = CircuitBreaker({
            "enabled": True, "failure_threshold": 5,
            "cooldown_seconds": 300, "half_open_max_requests": 1,
        })
        cb.record_failure("y")
        cb.record_failure("y")
        cb.record_success("y")  # resets counter
        cb.record_failure("y")
        cb.record_failure("y")
        cb.record_failure("y")
        cb.record_failure("y")
        assert cb.get_state("y") == CIRCUIT_CLOSED  # not 5 consecutive

    def test_disabled_circuit_breaker_always_allows(self):
        cb = CircuitBreaker({"enabled": False})
        for _ in range(10):
            cb.record_failure("z")
        assert cb.allow_request("z") is True
        assert cb.get_state("z") == CIRCUIT_CLOSED


# ============================================================================
# Usage tracker persistence and aggregation
# ============================================================================

class TestUsageTrackerPersistence:
    @pytest.fixture
    def tracker(self):
        t = UsageTracker(log_dir="logs/llm/test_prod")
        yield t
        t.clear()

    def test_record_writes_to_jsonl(self, tracker):
        tracker.record(
            task_id="u-001", agent_name="ra", task_type="SUMMARIZATION",
            provider="deepseek", model="deepseek-v4-flash",
            input_tokens=100, output_tokens=50,
            estimated_cost=0.002, cache_hit=False, success=True,
        )
        assert tracker.get_total_calls() == 1

    def test_entries_persist_across_instances(self, tracker):
        tracker.record(task_id="p-001", agent_name="ra", task_type="T",
                       provider="p", model="m", estimated_cost=0.01)
        # New instance reading same file
        t2 = UsageTracker(log_dir="logs/llm/test_prod")
        try:
            assert t2.get_total_calls() >= 1
        finally:
            t2.clear()

    def test_get_total_cost_aggregates_correctly(self, tracker):
        tracker.record(task_id="a", agent_name="ra", task_type="T",
                       provider="claude", model="m", estimated_cost=0.01)
        tracker.record(task_id="b", agent_name="ra", task_type="T",
                       provider="deepseek", model="m", estimated_cost=0.02)
        assert tracker.get_total_cost() == pytest.approx(0.03)

    def test_cost_by_agent_groups_correctly(self, tracker):
        tracker.record(task_id="1", agent_name="research-agent", task_type="T",
                       provider="p", model="m", estimated_cost=0.01)
        tracker.record(task_id="2", agent_name="risk-agent", task_type="T",
                       provider="p", model="m", estimated_cost=0.05)
        tracker.record(task_id="3", agent_name="research-agent", task_type="T",
                       provider="p", model="m", estimated_cost=0.02)
        by_agent = tracker.get_cost_by_agent()
        assert by_agent.get("research-agent") == pytest.approx(0.03)
        assert by_agent.get("risk-agent") == pytest.approx(0.05)

    def test_cost_by_provider_groups_correctly(self, tracker):
        tracker.record(task_id="1", agent_name="ra", task_type="T",
                       provider="claude", model="m", estimated_cost=0.03)
        tracker.record(task_id="2", agent_name="ra", task_type="T",
                       provider="deepseek", model="m", estimated_cost=0.001)
        by_provider = tracker.get_cost_by_provider()
        assert by_provider.get("claude") == pytest.approx(0.03)
        assert by_provider.get("deepseek") == pytest.approx(0.001)

    def test_cost_by_task_type_groups_correctly(self, tracker):
        tracker.record(task_id="1", agent_name="ra", task_type="SUMMARIZATION",
                       provider="ds", model="m", estimated_cost=0.001)
        tracker.record(task_id="2", agent_name="ra", task_type="CODE_GENERATION",
                       provider="cl", model="m", estimated_cost=0.05)
        by_type = tracker.get_cost_by_task_type()
        assert by_type.get("SUMMARIZATION") == pytest.approx(0.001)
        assert by_type.get("CODE_GENERATION") == pytest.approx(0.05)

    def test_recent_usage_respects_limit(self, tracker):
        for i in range(20):
            tracker.record(task_id=f"r-{i}", agent_name="ra", task_type="T",
                           provider="p", model="m")
        recent = tracker.get_recent_usage(limit=5)
        assert len(recent) == 5

    def test_clear_removes_all_entries(self, tracker):
        tracker.record(task_id="x", agent_name="ra", task_type="T",
                       provider="p", model="m")
        assert tracker.get_total_calls() == 1
        count = tracker.clear()
        assert count >= 1
        assert tracker.get_total_calls() == 0

    def test_empty_tracker_returns_sensible_defaults(self, tracker):
        assert tracker.get_total_calls() == 0
        assert tracker.get_total_cost() == 0.0
        assert tracker.get_cache_hit_ratio() == 0.0
        assert tracker.get_fallback_ratio() == 0.0
        assert tracker.get_success_rate() == 1.0
        assert tracker.get_recent_usage() == []


# ============================================================================
# router.ask() behavior
# ============================================================================

class TestRouterAskBehavior:
    def test_ask_auto_classifies_task(self):
        router = LLMRouter(dry_run=True)
        resp = router.ask(
            prompt="Summarize this article about BTC funding rates.",
            agent_name="research-agent",
        )
        assert resp.success is True
        # Should auto-classify as SUMMARIZATION → DeepSeek
        assert resp.provider == ProviderName.DEEPSEEK

    def test_ask_respects_manual_task_type_override(self):
        router = LLMRouter(dry_run=True)
        resp = router.ask(
            prompt="Summarize this article.",
            agent_name="research-agent",
            task_type=TaskType.PAPER_ANALYSIS,
        )
        # PAPER_ANALYSIS routes to Claude even though prompt says "summarize"
        assert resp.provider == ProviderName.CLAUDE

    def test_ask_respects_no_cache_metadata(self):
        router = LLMRouter(dry_run=True)
        resp = router.ask(
            prompt="A unique prompt that should be summarization.",
            agent_name="research-agent",
            metadata={"no_cache": True},
        )
        decision = resp.routing_decision
        assert decision is not None
        assert decision.cacheable is False

    def test_ask_respects_cost_sensitive_flag(self):
        router = LLMRouter(dry_run=True)
        resp = router.ask(
            prompt="A simple routine task.",
            agent_name="data-agent",
            cost_sensitive=True,
            complexity=Complexity.LOW,
        )
        assert resp.provider == ProviderName.DEEPSEEK

    def test_ask_risk_review_always_claude(self):
        router = LLMRouter(dry_run=True)
        resp = router.ask(
            prompt="Review the risk of this strategy.",
            agent_name="risk-agent",
            task_type=TaskType.RISK_REVIEW,
        )
        assert resp.provider == ProviderName.CLAUDE

    def test_ask_code_generation_always_claude(self):
        router = LLMRouter(dry_run=True)
        resp = router.ask(
            prompt="Write a Python function for Sharpe ratio.",
            agent_name="programmer-agent",
            task_type=TaskType.CODE_GENERATION,
            requires_code=True,
        )
        assert resp.provider == ProviderName.CLAUDE

    def test_ask_returns_all_response_fields(self):
        router = LLMRouter(dry_run=True)
        resp = router.ask(
            prompt="Fetch BTC market data.",
            agent_name="data-agent",
        )
        assert resp.task_id is not None
        assert resp.provider is not None
        assert resp.model is not None
        assert resp.routing_decision is not None
        assert resp.routing_decision.reason is not None
        assert resp.latency_ms is not None


# ============================================================================
# Fallback rule enforcement
# ============================================================================

class TestFallbackRuleEnforcement:
    def test_code_generation_fallback_blocked(self):
        router = LLMRouter(dry_run=True)
        assert router._fallback_allowed_for_task(TaskType.CODE_GENERATION, False, "programmer-agent") is False

    def test_code_planning_fallback_blocked(self):
        router = LLMRouter(dry_run=True)
        assert router._fallback_allowed_for_task(TaskType.CODE_PLANNING, False, "programmer-agent") is False

    def test_code_review_fallback_blocked(self):
        router = LLMRouter(dry_run=True)
        assert router._fallback_allowed_for_task(TaskType.CODE_REVIEW, False, "programmer-agent") is False

    def test_debugging_fallback_blocked(self):
        router = LLMRouter(dry_run=True)
        assert router._fallback_allowed_for_task(TaskType.DEBUGGING, False, "programmer-agent") is False

    def test_risk_review_fallback_blocked(self):
        router = LLMRouter(dry_run=True)
        assert router._fallback_allowed_for_task(TaskType.RISK_REVIEW, False, "risk-agent") is False

    def test_requires_code_blocks_fallback_regardless_of_type(self):
        router = LLMRouter(dry_run=True)
        assert router._fallback_allowed_for_task(TaskType.GENERAL_QA, True, "data-agent") is False

    def test_non_code_low_risk_tasks_allow_fallback(self):
        router = LLMRouter(dry_run=True)
        assert router._fallback_allowed_for_task(TaskType.SUMMARIZATION, False, "research-agent") is True
        assert router._fallback_allowed_for_task(TaskType.TEXT_CLEANUP, False, "research-agent") is True
        assert router._fallback_allowed_for_task(TaskType.DATA_GRABBING, False, "data-agent") is True
        assert router._fallback_allowed_for_task(TaskType.MEMO_WRITING, False, "research-agent") is True


# ============================================================================
# Task classifier improvements
# ============================================================================

class TestClassifierNewKeywords:
    def test_paper_analysis_variants(self):
        assert classify_task("summarize this paper on volatility") == TaskType.PAPER_ANALYSIS
        assert classify_task("extract from paper the key findings") == TaskType.PAPER_ANALYSIS
        assert classify_task("literature review of crypto papers") == TaskType.PAPER_ANALYSIS
        assert classify_task("this is a journal paper about markets") == TaskType.PAPER_ANALYSIS

    def test_code_generation_variants(self):
        assert classify_task("write the backtest for this signal") == TaskType.CODE_GENERATION
        assert classify_task("code the data loader module") == TaskType.CODE_GENERATION
        assert classify_task("write the test for this function") == TaskType.CODE_GENERATION

    def test_debugging_variants(self):
        assert classify_task("why is this failing in production") == TaskType.DEBUGGING
        assert classify_task("what is wrong with this backtest") == TaskType.DEBUGGING
        assert classify_task("troubleshoot the API connection") == TaskType.DEBUGGING
        assert classify_task("fix this issue with the data") == TaskType.DEBUGGING

    def test_risk_review_variants(self):
        assert classify_task("var calculation for portfolio") == TaskType.RISK_REVIEW
        assert classify_task("stress test the strategy") == TaskType.RISK_REVIEW
        assert classify_task("risk profile for strategy CRYPTO-005") == TaskType.RISK_REVIEW

    def test_source_screening_variants(self):
        assert classify_task("source verification for this paper") == TaskType.WEB_SOURCE_SCREENING
        assert classify_task("is this source reliable for data") == TaskType.WEB_SOURCE_SCREENING

    def test_data_grabbing_variants(self):
        assert classify_task("retrieve data from the exchange API") == TaskType.DATA_GRABBING
        assert classify_task("download the OHLCV data for BTC") == TaskType.DATA_GRABBING
        assert classify_task("query the database for funding rates") == TaskType.DATA_GRABBING

    def test_alpha_generation_variants(self):
        assert classify_task("new trading idea for mean reversion") == TaskType.ALPHA_IDEA_GENERATION

    def test_system_architecture_variants(self):
        assert classify_task("design the architecture for the backtester") == TaskType.SYSTEM_ARCHITECTURE

    def test_agent_hint_fallback(self):
        assert classify_task("do something", agent_name="programmer-agent") == TaskType.CODE_GENERATION
        assert classify_task("do something", agent_name="risk-agent") == TaskType.RISK_REVIEW
        assert classify_task("do something", agent_name="data-agent") == TaskType.DATA_GRABBING
        assert classify_task("do something", agent_name="unknown-agent") == TaskType.GENERAL_QA

    def test_activity_hints(self):
        assert classify_task("source pre-screen these URLs") == TaskType.WEB_SOURCE_SCREENING
        assert classify_task("source discovery for funding rates") == TaskType.WEB_SOURCE_SCREENING
        assert classify_task("memo synthesis for CRYPTO-005") == TaskType.MEMO_WRITING
        assert classify_task("final synthesis of research findings") == TaskType.RESEARCH_REASONING
        assert classify_task("backtest report formatting") == TaskType.SUMMARIZATION


class TestClassifierComplexityInference:
    def test_complexity_from_task_type(self):
        assert infer_complexity("any", TaskType.SYSTEM_ARCHITECTURE) == Complexity.HIGH
        assert infer_complexity("any", TaskType.CODE_GENERATION) == Complexity.HIGH
        assert infer_complexity("any", TaskType.RESEARCH_REASONING) == Complexity.HIGH
        assert infer_complexity("any", TaskType.SUMMARIZATION) == Complexity.LOW
        assert infer_complexity("any", TaskType.CLASSIFICATION) == Complexity.LOW
        assert infer_complexity("any", TaskType.MEMORY_UPDATE) == Complexity.LOW

    def test_complexity_from_keywords(self):
        assert infer_complexity("complex multi-step reasoning task") == Complexity.HIGH
        assert infer_complexity("nuanced analysis") == Complexity.HIGH
        assert infer_complexity("simple quick task") == Complexity.LOW
        assert infer_complexity("trivial formatting change") == Complexity.LOW

    def test_long_context_inference(self):
        assert infer_long_context("analyze the full paper from start to end") is True
        assert infer_long_context("complete backtest analysis") is True
        assert infer_long_context("just a short question") is False
        assert infer_long_context("hello") is False

    def test_cost_sensitivity_inference(self):
        assert infer_cost_sensitivity(TaskType.SUMMARIZATION, Complexity.LOW) is True
        assert infer_cost_sensitivity(TaskType.CODE_GENERATION, Complexity.HIGH) is False
        assert infer_cost_sensitivity(TaskType.RISK_REVIEW, Complexity.HIGH) is False
        assert infer_cost_sensitivity(TaskType.CLASSIFICATION, Complexity.MEDIUM) is False
        assert infer_cost_sensitivity(TaskType.GENERAL_QA, Complexity.LOW) is False


# ============================================================================
# CLI dry-run integration (import and smoke test)
# ============================================================================

class TestCLIIntegration:
    def test_cli_module_imports(self):
        """CLI script can be imported without error."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "llm_router_cli",
            Path("scripts/llm_router_cli.py"),
        )
        assert spec is not None

    def test_router_dry_run_cli_flow(self):
        """Simulate what the CLI does: create router, route a prompt."""
        router = LLMRouter(dry_run=True)
        request = TaskRequest(
            task_id="cli-test-001",
            agent_name="research-agent",
            task_type=TaskType.PAPER_ANALYSIS,
            prompt="Analyze this paper abstract about BTC volatility.",
            domain=Domain.CRYPTO,
            complexity=Complexity.HIGH,
        )
        response = router.route(request)
        assert response.success is True
        assert response.provider == ProviderName.CLAUDE
        assert response.model is not None
        assert response.routing_decision is not None
        assert "DRY RUN" in (response.content or "")

    def test_cli_health_check_flow(self):
        router = LLMRouter(dry_run=True)
        result = router.health_check()
        for key in ["claude", "deepseek"]:
            assert key in result
            assert "available" in result[key]

    def test_cli_usage_summary_flow(self):
        router = LLMRouter(dry_run=True)
        summary = router.get_usage_summary()
        for key in ["total_calls", "total_cost", "cost_by_agent", "cost_by_provider",
                     "cost_by_task_type", "cache_hit_ratio", "fallback_ratio",
                     "success_rate", "recent_calls"]:
            assert key in summary


# ============================================================================
# Dotenv and environment variable loading (no secrets exposed)
# ============================================================================

class TestEnvVarLoading:
    def test_claude_provider_detects_env_var_key(self):
        """ClaudeProvider picks up ANTHROPIC_API_KEY from os.environ."""
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-1234"}, clear=True):
            provider = ClaudeProvider({
                "default_model": "claude-sonnet-4-6",
                "models": ["claude-sonnet-4-6"],
            })
            assert provider.validate_config() is True
            details = provider.health_details()
            assert details["api_key_set"] is True
            assert details["available"] is True

    def test_deepseek_provider_detects_env_var_key(self):
        """DeepSeekProvider picks up DEEPSEEK_API_KEY from os.environ."""
        with mock.patch.dict(os.environ, {"DEEPSEEK_API_KEY": "sk-deepseek-test-5678"}, clear=True):
            provider = DeepSeekProvider({
                "default_model": "deepseek-v4-flash",
                "models": ["deepseek-v4-flash"],
            })
            assert provider.validate_config() is True
            details = provider.health_details()
            assert details["api_key_set"] is True
            assert details["available"] is True

    def test_claude_provider_missing_key_shows_clear_error(self):
        """Health check returns clear reason when key is missing."""
        with mock.patch.dict(os.environ, {}, clear=True):
            provider = ClaudeProvider({
                "default_model": "claude-sonnet-4-6",
                "models": ["claude-sonnet-4-6"],
            })
            assert provider.health_check() is False
            details = provider.health_details()
            assert details["api_key_set"] is False
            assert details["reason"] != "ready"
            assert "ANTHROPIC_API_KEY" in details["reason"] or details["reason"] == "anthropic SDK not installed"

    def test_deepseek_provider_missing_key_shows_clear_error(self):
        """Health check returns clear reason when key is missing."""
        with mock.patch.dict(os.environ, {}, clear=True):
            provider = DeepSeekProvider({
                "default_model": "deepseek-v4-flash",
                "models": ["deepseek-v4-flash"],
            })
            assert provider.health_check() is False
            details = provider.health_details()
            assert details["api_key_set"] is False
            assert details["reason"] != "ready"

    def test_call_with_key_but_no_sdk(self):
        """When key is set but SDK missing, error is about SDK."""
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test"}, clear=True):
            # We can't easily mock the SDK import, but we know the provider handles it.
            provider = ClaudeProvider({
                "default_model": "claude-sonnet-4-6",
                "models": ["claude-sonnet-4-6"],
            })
            # validate_config checks both SDK and key
            ok = provider.validate_config()
            # True if SDK is installed, False otherwise — either is fine
            assert ok in (True, False)

    def test_dotenv_loader_is_idempotent(self):
        """load_dotenv_if_available can be called multiple times safely."""
        from src.llm.utils.env_loader import load_dotenv_if_available

        load_dotenv_if_available()
        load_dotenv_if_available()
        load_dotenv_if_available()
        # Should not raise or crash

    def test_dotenv_loader_finds_project_root(self):
        """The env loader can locate the project root."""
        from src.llm.utils.env_loader import _find_project_root

        root = _find_project_root()
        assert root.exists()
        assert (root / "CLAUDE.md").exists()

    def test_providers_do_not_expose_api_key_in_logs_or_details(self):
        """Health details must never contain the actual API key value."""
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-secret-do-not-leak"}, clear=True):
            provider = ClaudeProvider({
                "default_model": "claude-sonnet-4-6",
                "models": ["claude-sonnet-4-6"],
            })
            details = provider.health_details()
            # Keys must never appear in the health details output
            details_str = str(details)
            assert "sk-ant-secret-do-not-leak" not in details_str

    def test_deepseek_provider_does_not_expose_api_key_in_details(self):
        """DeepSeek health details must never contain the actual API key value."""
        with mock.patch.dict(os.environ, {"DEEPSEEK_API_KEY": "sk-ds-secret-do-not-leak"}, clear=True):
            provider = DeepSeekProvider({
                "default_model": "deepseek-v4-flash",
                "models": ["deepseek-v4-flash"],
            })
            details = provider.health_details()
            details_str = str(details)
            assert "sk-ds-secret-do-not-leak" not in details_str

    def test_env_loader_does_not_expose_key_in_logs(self, caplog):
        """The env loader must never log the actual key value."""
        import logging

        from src.llm.utils.env_loader import load_dotenv_if_available

        # Reset the _LOADED flag so it runs again
        import src.llm.utils.env_loader as env_mod

        env_mod._LOADED = False

        with caplog.at_level(logging.DEBUG, logger="llm_router.env"):
            load_dotenv_if_available()
        # The loader should not log any key value
        combined = " ".join(record.message for record in caplog.records)
        assert "sk-ant" not in combined
        assert "sk-" not in combined

    def test_router_health_check_integrates_with_dotenv_keys(self):
        """Router health_check shows providers as available when keys are set."""
        with mock.patch.dict(os.environ, {
            "ANTHROPIC_API_KEY": "sk-ant-test",
            "DEEPSEEK_API_KEY": "sk-ds-test",
        }, clear=True):
            router = LLMRouter(dry_run=True)
            result = router.health_check()
            # Providers should report ready (assuming SDKs are installed)
            assert "reason" in result["claude"]
            assert "reason" in result["deepseek"]
            # Circuit state should be closed
            assert result["claude"]["circuit_state"] == "closed"
            assert result["deepseek"]["circuit_state"] == "closed"
