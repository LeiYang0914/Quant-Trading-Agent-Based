"""Tests for LLM Router routing decisions in dry_run mode."""

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


class TestRoutingToClaude:
    def test_system_architecture_routes_to_claude(self, router):
        request = TaskRequest(
            task_id="test-001",
            agent_name="research-agent",
            task_type=TaskType.SYSTEM_ARCHITECTURE,
            prompt="Design a data pipeline architecture.",
        )
        response = router.route(request)
        assert response.provider == ProviderName.CLAUDE

    def test_research_reasoning_routes_to_claude(self, router):
        request = TaskRequest(
            task_id="test-002",
            agent_name="research-agent",
            task_type=TaskType.RESEARCH_REASONING,
            prompt="Investigate the relationship between funding rates and momentum.",
            complexity=Complexity.HIGH,
        )
        response = router.route(request)
        assert response.provider == ProviderName.CLAUDE

    def test_paper_analysis_routes_to_claude(self, router):
        request = TaskRequest(
            task_id="test-003",
            agent_name="research-agent",
            task_type=TaskType.PAPER_ANALYSIS,
            prompt="Analyze this paper on volatility prediction.",
        )
        response = router.route(request)
        assert response.provider == ProviderName.CLAUDE

    def test_code_generation_routes_to_claude(self, router):
        request = TaskRequest(
            task_id="test-004",
            agent_name="programmer-agent",
            task_type=TaskType.CODE_GENERATION,
            prompt="Write a function to compute the Sharpe ratio.",
            requires_code=True,
        )
        response = router.route(request)
        assert response.provider == ProviderName.CLAUDE

    def test_code_review_routes_to_claude(self, router):
        request = TaskRequest(
            task_id="test-005",
            agent_name="programmer-agent",
            task_type=TaskType.CODE_REVIEW,
            prompt="Review this backtest implementation.",
        )
        response = router.route(request)
        assert response.provider == ProviderName.CLAUDE

    def test_debugging_routes_to_claude(self, router):
        request = TaskRequest(
            task_id="test-006",
            agent_name="programmer-agent",
            task_type=TaskType.DEBUGGING,
            prompt="Why does this backtest produce negative Sharpe?",
        )
        response = router.route(request)
        assert response.provider == ProviderName.CLAUDE

    def test_high_complexity_routes_to_claude(self, router):
        request = TaskRequest(
            task_id="test-007",
            agent_name="research-agent",
            task_type=TaskType.GENERAL_QA,
            prompt="Complex multi-step reasoning task.",
            complexity=Complexity.HIGH,
        )
        response = router.route(request)
        assert response.provider == ProviderName.CLAUDE

    def test_requires_code_routes_to_claude(self, router):
        request = TaskRequest(
            task_id="test-008",
            agent_name="data-agent",
            task_type=TaskType.GENERAL_QA,
            prompt="Write a utility function.",
            requires_code=True,
        )
        response = router.route(request)
        assert response.provider == ProviderName.CLAUDE

    def test_requires_long_context_routes_to_claude(self, router):
        request = TaskRequest(
            task_id="test-009",
            agent_name="research-agent",
            task_type=TaskType.GENERAL_QA,
            prompt="Analyze this very long document.",
            requires_long_context=True,
        )
        response = router.route(request)
        assert response.provider == ProviderName.CLAUDE

    def test_risk_agent_review_routes_to_claude(self, router):
        request = TaskRequest(
            task_id="test-010",
            agent_name="risk-agent",
            task_type=TaskType.RESEARCH_REASONING,
            prompt="Review the risk profile of strategy CRYPTO-005.",
            complexity=Complexity.HIGH,
            domain=Domain.CRYPTO,
        )
        response = router.route(request)
        assert response.provider == ProviderName.CLAUDE

    def test_review_agent_routes_to_claude(self, router):
        request = TaskRequest(
            task_id="test-011",
            agent_name="review-agent",
            task_type=TaskType.RESEARCH_REASONING,
            prompt="Evaluate this alpha idea.",
        )
        response = router.route(request)
        assert response.provider == ProviderName.CLAUDE

    def test_programmer_agent_routes_to_claude(self, router):
        request = TaskRequest(
            task_id="test-012",
            agent_name="programmer-agent",
            task_type=TaskType.GENERAL_QA,
            prompt="How should I structure this module?",
        )
        response = router.route(request)
        assert response.provider == ProviderName.CLAUDE


class TestRoutingToDeepSeek:
    def test_summarization_routes_to_deepseek(self, router):
        request = TaskRequest(
            task_id="test-101",
            agent_name="research-agent",
            task_type=TaskType.SUMMARIZATION,
            prompt="Summarize this article.",
        )
        response = router.route(request)
        assert response.provider == ProviderName.DEEPSEEK

    def test_text_cleanup_routes_to_deepseek(self, router):
        request = TaskRequest(
            task_id="test-102",
            agent_name="research-agent",
            task_type=TaskType.TEXT_CLEANUP,
            prompt="Format this memo.",
        )
        response = router.route(request)
        assert response.provider == ProviderName.DEEPSEEK

    def test_data_grabbing_routes_to_deepseek(self, router):
        request = TaskRequest(
            task_id="test-103",
            agent_name="data-agent",
            task_type=TaskType.DATA_GRABBING,
            prompt="Fetch BTC OHLCV data.",
        )
        response = router.route(request)
        assert response.provider == ProviderName.DEEPSEEK

    def test_web_source_screening_routes_to_deepseek(self, router):
        request = TaskRequest(
            task_id="test-104",
            agent_name="research-agent",
            task_type=TaskType.WEB_SOURCE_SCREENING,
            prompt="Screen these sources for relevance.",
        )
        response = router.route(request)
        assert response.provider == ProviderName.DEEPSEEK

    def test_git_activity_summary_routes_to_deepseek(self, router):
        request = TaskRequest(
            task_id="test-105",
            agent_name="data-agent",
            task_type=TaskType.GIT_ACTIVITY_SUMMARY,
            prompt="Summarize recent git activity.",
        )
        response = router.route(request)
        assert response.provider == ProviderName.DEEPSEEK

    def test_classification_routes_to_deepseek(self, router):
        request = TaskRequest(
            task_id="test-106",
            agent_name="research-agent",
            task_type=TaskType.CLASSIFICATION,
            prompt="Classify these market events.",
        )
        response = router.route(request)
        assert response.provider == ProviderName.DEEPSEEK

    def test_memory_update_routes_to_deepseek(self, router):
        request = TaskRequest(
            task_id="test-107",
            agent_name="research-agent",
            task_type=TaskType.MEMORY_UPDATE,
            prompt="Update the project state memory.",
        )
        response = router.route(request)
        assert response.provider == ProviderName.DEEPSEEK

    def test_cost_sensitive_low_complexity_routes_to_deepseek(self, router):
        request = TaskRequest(
            task_id="test-108",
            agent_name="data-agent",
            task_type=TaskType.GENERAL_QA,
            prompt="Do something cheap.",
            cost_sensitive=True,
            complexity=Complexity.LOW,
        )
        response = router.route(request)
        assert response.provider == ProviderName.DEEPSEEK


class TestExplicitPreference:
    def test_preferred_claude_overrides_default(self, router):
        request = TaskRequest(
            task_id="test-201",
            agent_name="data-agent",
            task_type=TaskType.SUMMARIZATION,
            prompt="Summarize this.",
            preferred_provider=ProviderName.CLAUDE,
        )
        response = router.route(request)
        assert response.provider == ProviderName.CLAUDE

    def test_preferred_deepseek_overrides_default(self, router):
        request = TaskRequest(
            task_id="test-202",
            agent_name="research-agent",
            task_type=TaskType.RESEARCH_REASONING,
            prompt="Analyze this.",
            preferred_provider=ProviderName.DEEPSEEK,
        )
        response = router.route(request)
        assert response.provider == ProviderName.DEEPSEEK


class TestDryRun:
    def test_dry_run_returns_success(self, router):
        request = TaskRequest(
            task_id="test-301",
            agent_name="research-agent",
            task_type=TaskType.PAPER_ANALYSIS,
            prompt="Analyze this paper.",
        )
        response = router.route(request)
        assert response.success is True
        assert "[DRY RUN" in (response.content or "")

    def test_dry_run_does_not_call_real_api(self, router):
        request = TaskRequest(
            task_id="test-302",
            agent_name="research-agent",
            task_type=TaskType.RESEARCH_REASONING,
            prompt="Research this topic.",
        )
        response = router.route(request)
        assert response.latency_ms is not None
        # In dry run, latency should be essentially zero or very small
        assert response.latency_ms < 100
