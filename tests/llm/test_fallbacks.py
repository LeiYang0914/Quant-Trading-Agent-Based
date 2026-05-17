"""Tests for LLM Router fallback behavior in dry_run mode."""

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


class TestFallbackBehavior:
    def test_code_generation_does_not_fallback_to_deepseek(self, router):
        """Code generation should not fallback Claude→DeepSeek by default."""
        # The router's _fallback_allowed_for_task blocks code tasks
        assert router._fallback_allowed_for_task(TaskType.CODE_GENERATION, requires_code=False) is False
        assert router._fallback_allowed_for_task(TaskType.CODE_GENERATION, requires_code=True) is False
        assert router._fallback_allowed_for_task(TaskType.CODE_PLANNING, requires_code=False) is False
        assert router._fallback_allowed_for_task(TaskType.CODE_REVIEW, requires_code=False) is False
        assert router._fallback_allowed_for_task(TaskType.DEBUGGING, requires_code=False) is False

    def test_non_code_tasks_allow_fallback(self, router):
        """Non-code tasks should allow fallback."""
        assert router._fallback_allowed_for_task(TaskType.SUMMARIZATION, requires_code=False) is True
        assert router._fallback_allowed_for_task(TaskType.TEXT_CLEANUP, requires_code=False) is True
        assert router._fallback_allowed_for_task(TaskType.DATA_GRABBING, requires_code=False) is True
        assert router._fallback_allowed_for_task(TaskType.GENERAL_QA, requires_code=False) is True

    def test_requires_code_true_blocks_fallback(self, router):
        """If requires_code is true, fallback is blocked regardless of task type."""
        assert router._fallback_allowed_for_task(TaskType.GENERAL_QA, requires_code=True) is False

    def test_fallback_decision_deepseek_to_claude(self, router):
        """When DeepSeek is primary, fallback should be Claude."""
        request = TaskRequest(
            task_id="test-001",
            agent_name="data-agent",
            task_type=TaskType.SUMMARIZATION,
            prompt="Summarize this.",
            fallback_allowed=True,
        )
        decision = router._make_decision(request)
        assert decision.selected_provider == ProviderName.DEEPSEEK
        assert decision.fallback_provider == ProviderName.CLAUDE

        fallback = router._make_fallback_decision(request, decision)
        assert fallback.selected_provider == ProviderName.CLAUDE

    def test_fallback_decision_claude_to_deepseek_non_code(self, router):
        """Claude→DeepSeek fallback for non-code tasks."""
        request = TaskRequest(
            task_id="test-002",
            agent_name="research-agent",
            task_type=TaskType.SUMMARIZATION,
            prompt="Summarize this.",
            preferred_provider=ProviderName.CLAUDE,
            fallback_allowed=True,
        )
        decision = router._make_decision(request)
        assert decision.selected_provider == ProviderName.CLAUDE
        assert decision.fallback_provider == ProviderName.DEEPSEEK

        fallback = router._make_fallback_decision(request, decision)
        assert fallback.selected_provider == ProviderName.DEEPSEEK

    def test_dry_run_response_includes_fallback_flag(self, router):
        """Dry run responses should include fallback_used flag."""
        request = TaskRequest(
            task_id="test-003",
            agent_name="data-agent",
            task_type=TaskType.TEXT_CLEANUP,
            prompt="Format this document.",
        )
        response = router.route(request)
        assert response.success is True
        assert response.fallback_used is False
        assert "[DRY RUN" in (response.content or "")
