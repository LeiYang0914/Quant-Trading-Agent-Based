"""Tests for advanced LLM Router features: ask(), health_check(), caching, etc."""

import pytest

from src.llm import (
    Complexity,
    Domain,
    LLMRouter,
    ProviderName,
    TaskRequest,
    TaskType,
)


@pytest.fixture
def router():
    return LLMRouter(dry_run=True)


class TestRouterAsk:
    def test_ask_auto_classifies_summarization(self, router):
        response = router.ask(
            prompt="Summarize this article about crypto markets.",
            agent_name="research-agent",
        )
        assert response.success is True
        # Should auto-classify as SUMMARIZATION → DeepSeek
        assert response.provider == ProviderName.DEEPSEEK

    def test_ask_respects_manual_task_type(self, router):
        response = router.ask(
            prompt="Summarize this article.",
            agent_name="research-agent",
            task_type=TaskType.PAPER_ANALYSIS,  # manual override
        )
        # PAPER_ANALYSIS should route to Claude
        assert response.provider == ProviderName.CLAUDE

    def test_ask_with_explicit_complexity(self, router):
        response = router.ask(
            prompt="A simple task.",
            agent_name="data-agent",
            task_type=TaskType.GENERAL_QA,
            complexity=Complexity.LOW,
            metadata={"cost_sensitive": True},
        )
        response2 = router.route(TaskRequest(
            task_id="test-manual",
            agent_name="data-agent",
            task_type=TaskType.GENERAL_QA,
            prompt="A simple task.",
            complexity=Complexity.LOW,
            cost_sensitive=True,
        ))
        assert response.provider == response2.provider

    def test_ask_fallback_blocked_for_code(self, router):
        response = router.ask(
            prompt="Write a Python function to compute Sharpe ratio.",
            agent_name="programmer-agent",
            task_type=TaskType.CODE_GENERATION,
            requires_code=True,
            fallback_allowed=False,
        )
        assert response.provider == ProviderName.CLAUDE
        assert response.fallback_used is False

    def test_ask_returns_structured_response(self, router):
        response = router.ask(
            prompt="Fetch BTC daily OHLCV data.",
            agent_name="data-agent",
        )
        assert response.task_id is not None
        assert response.provider is not None
        assert response.model is not None
        assert response.routing_decision is not None
        assert response.routing_decision.reason is not None


class TestRouterHealthCheck:
    def test_health_check_returns_structure(self, router):
        result = router.health_check()
        assert "claude" in result
        assert "deepseek" in result
        assert "available" in result["claude"]
        assert "reason" in result["claude"]
        assert "configured_models" in result["claude"]
        assert "circuit_state" in result["claude"]
        assert "rate_limit_remaining" in result["claude"]

    def test_health_check_deepseek(self, router):
        result = router.health_check()
        assert "available" in result["deepseek"]
        assert isinstance(result["deepseek"]["configured_models"], list)


class TestRouterUsageSummary:
    def test_usage_summary_returns_structure(self, router):
        summary = router.get_usage_summary()
        assert "total_calls" in summary
        assert "total_cost" in summary
        assert "cost_by_agent" in summary
        assert "cost_by_provider" in summary
        assert "cost_by_task_type" in summary
        assert "cache_hit_ratio" in summary
        assert "fallback_ratio" in summary
        assert "success_rate" in summary
        assert "recent_calls" in summary

    def test_usage_tracks_dry_run_calls(self, router):
        router.ask(prompt="Hello", agent_name="test-agent")
        summary = router.get_usage_summary()
        assert summary["total_calls"] >= 1


class TestRouterCacheIntegration:
    def test_code_generation_not_cacheable(self, router):
        request = TaskRequest(
            task_id="test-code-001",
            agent_name="programmer-agent",
            task_type=TaskType.CODE_GENERATION,
            prompt="Write a function.",
            requires_code=True,
        )
        decision = router._make_decision(request)
        assert decision.cacheable is False

    def test_risk_review_not_cacheable(self, router):
        request = TaskRequest(
            task_id="test-risk-001",
            agent_name="risk-agent",
            task_type=TaskType.RISK_REVIEW,
            prompt="Review strategy risk.",
        )
        decision = router._make_decision(request)
        assert decision.cacheable is False

    def test_summarization_is_cacheable(self, router):
        request = TaskRequest(
            task_id="test-sum-001",
            agent_name="research-agent",
            task_type=TaskType.SUMMARIZATION,
            prompt="Summarize this.",
        )
        decision = router._make_decision(request)
        assert decision.cacheable is True

    def test_no_cache_metadata_disables_cache(self, router):
        request = TaskRequest(
            task_id="test-nocache-001",
            agent_name="research-agent",
            task_type=TaskType.SUMMARIZATION,
            prompt="Summarize this.",
            metadata={"no_cache": True},
        )
        decision = router._make_decision(request)
        assert decision.cacheable is False

    def test_clear_cache_works(self, router):
        count = router.clear_cache()
        assert count >= 0  # Works even if empty


class TestRouterClearUsage:
    def test_clear_usage_works(self, router):
        router.ask(prompt="Test", agent_name="test-agent")
        count = router.clear_usage()
        assert count >= 0


class TestRouterResetCircuits:
    def test_reset_circuits_works(self, router):
        router.reset_circuits()
        router.reset_rate_limiters()
        result = router.health_check()
        assert result["claude"]["circuit_state"] == "closed"
        assert result["deepseek"]["circuit_state"] == "closed"


class TestRouterRISKREVIEW:
    def test_risk_review_routes_to_claude(self, router):
        request = TaskRequest(
            task_id="test-risk-002",
            agent_name="risk-agent",
            task_type=TaskType.RISK_REVIEW,
            prompt="Review the risk profile.",
        )
        response = router.route(request)
        assert response.provider == ProviderName.CLAUDE

    def test_risk_review_no_fallback_to_deepseek(self, router):
        """RISK_REVIEW should be in the no-fallback set."""
        assert router._fallback_allowed_for_task(TaskType.RISK_REVIEW, requires_code=False) is False


class TestRouterMemoWriting:
    def test_memo_writing_routes_to_claude(self, router):
        request = TaskRequest(
            task_id="test-memo-001",
            agent_name="research-agent",
            task_type=TaskType.MEMO_WRITING,
            prompt="Write a research memo about funding rates.",
        )
        response = router.route(request)
        assert response.provider == ProviderName.CLAUDE


class TestRouterCircuitBreakerIntegration:
    def test_circuit_breaker_allows_when_closed(self, router):
        assert router.circuit_breaker.allow_request("claude") is True

    def test_health_check_shows_circuit_state(self, router):
        result = router.health_check()
        assert result["claude"]["circuit_state"] == "closed"


class TestRouterRateLimitIntegration:
    def test_rate_limiter_allows_initial_requests(self, router):
        assert router.rate_limiter.acquire("claude") is True

    def test_rate_limit_remaining_reported_in_health(self, router):
        result = router.health_check()
        # Rate limiter may be None if not enabled, or a number
        assert result["claude"]["rate_limit_remaining"] is not None
