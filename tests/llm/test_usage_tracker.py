"""Tests for UsageTracker."""

import json

import pytest

from src.llm.utils.usage_tracker import UsageTracker


@pytest.fixture
def tracker():
    t = UsageTracker(log_dir="logs/llm/test")
    yield t
    t.clear()


class TestUsageTracker:
    def test_record_and_count(self, tracker):
        tracker.record(
            task_id="test-001",
            agent_name="research-agent",
            task_type="SUMMARIZATION",
            provider="deepseek",
            model="deepseek-v4-flash",
            estimated_cost=0.001,
        )
        assert tracker.get_total_calls() == 1

    def test_total_cost_aggregates(self, tracker):
        tracker.record(task_id="a", agent_name="ra", task_type="T1", provider="claude", model="m1", estimated_cost=0.01)
        tracker.record(task_id="b", agent_name="pa", task_type="T2", provider="deepseek", model="m2", estimated_cost=0.02)
        assert tracker.get_total_cost() == pytest.approx(0.03)

    def test_cost_by_agent(self, tracker):
        tracker.record(task_id="a", agent_name="research-agent", task_type="T1", provider="claude", model="m1", estimated_cost=0.01)
        tracker.record(task_id="b", agent_name="research-agent", task_type="T2", provider="deepseek", model="m2", estimated_cost=0.02)
        tracker.record(task_id="c", agent_name="risk-agent", task_type="T3", provider="claude", model="m3", estimated_cost=0.05)
        by_agent = tracker.get_cost_by_agent()
        assert by_agent.get("research-agent") == pytest.approx(0.03)
        assert by_agent.get("risk-agent") == pytest.approx(0.05)

    def test_cost_by_provider(self, tracker):
        tracker.record(task_id="a", agent_name="ra", task_type="T1", provider="claude", model="m1", estimated_cost=0.01)
        tracker.record(task_id="b", agent_name="ra", task_type="T2", provider="deepseek", model="m2", estimated_cost=0.003)
        tracker.record(task_id="c", agent_name="ra", task_type="T3", provider="claude", model="m1", estimated_cost=0.02)
        by_provider = tracker.get_cost_by_provider()
        assert by_provider.get("claude") == pytest.approx(0.03)
        assert by_provider.get("deepseek") == pytest.approx(0.003)

    def test_cost_by_task_type(self, tracker):
        tracker.record(task_id="a", agent_name="ra", task_type="SUMMARIZATION", provider="deepseek", model="m1", estimated_cost=0.001)
        tracker.record(task_id="b", agent_name="ra", task_type="CODE_GENERATION", provider="claude", model="m2", estimated_cost=0.05)
        by_type = tracker.get_cost_by_task_type()
        assert by_type.get("SUMMARIZATION") == pytest.approx(0.001)
        assert by_type.get("CODE_GENERATION") == pytest.approx(0.05)

    def test_recent_usage_respects_limit(self, tracker):
        for i in range(10):
            tracker.record(task_id=f"t-{i}", agent_name="ra", task_type="T", provider="p", model="m")
        recent = tracker.get_recent_usage(limit=5)
        assert len(recent) == 5

    def test_cache_hit_ratio(self, tracker):
        tracker.record(task_id="a", agent_name="ra", task_type="T", provider="p", model="m", cache_hit=False)
        tracker.record(task_id="b", agent_name="ra", task_type="T", provider="p", model="m", cache_hit=True)
        tracker.record(task_id="c", agent_name="ra", task_type="T", provider="p", model="m", cache_hit=False)
        assert tracker.get_cache_hit_ratio() == pytest.approx(1 / 3)

    def test_fallback_ratio(self, tracker):
        tracker.record(task_id="a", agent_name="ra", task_type="T", provider="p", model="m", fallback_used=False)
        tracker.record(task_id="b", agent_name="ra", task_type="T", provider="p", model="m", fallback_used=True)
        assert tracker.get_fallback_ratio() == pytest.approx(0.5)

    def test_success_rate(self, tracker):
        tracker.record(task_id="a", agent_name="ra", task_type="T", provider="p", model="m", success=True)
        tracker.record(task_id="b", agent_name="ra", task_type="T", provider="p", model="m", success=True)
        tracker.record(task_id="c", agent_name="ra", task_type="T", provider="p", model="m", success=False)
        assert tracker.get_success_rate() == pytest.approx(2 / 3)

    def test_empty_tracker_defaults(self, tracker):
        assert tracker.get_total_calls() == 0
        assert tracker.get_total_cost() == 0.0
        assert tracker.get_cache_hit_ratio() == 0.0
        assert tracker.get_success_rate() == 1.0

    def test_clear_removes_all(self, tracker):
        tracker.record(task_id="a", agent_name="ra", task_type="T", provider="p", model="m")
        assert tracker.get_total_calls() == 1
        tracker.clear()
        assert tracker.get_total_calls() == 0
