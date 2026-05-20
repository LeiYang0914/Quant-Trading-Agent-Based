"""Tests for dashboard backend metrics_service module."""

from datetime import datetime, timedelta, timezone

import pytest

from src.dashboard.backend.metrics_service import (
    compute_agent_metrics,
    compute_cache_savings,
    compute_failures,
    compute_overview,
    compute_provider_metrics,
)


@pytest.fixture
def empty_entries():
    return []


@pytest.fixture
def sample_entries():
    """All real calls (dry_run=False)."""
    now = datetime.now(timezone.utc)
    return [
        {
            "timestamp": (now - timedelta(hours=3)).isoformat(),
            "task_id": "t-001",
            "agent_name": "research-agent",
            "task_type": "RESEARCH_REASONING",
            "provider": "claude",
            "model": "claude-sonnet-4-6",
            "estimated_cost": 0.003,
            "cache_hit": False,
            "fallback_used": False,
            "success": True,
            "latency_ms": 1200,
            "dry_run": False,
        },
        {
            "timestamp": (now - timedelta(hours=2)).isoformat(),
            "task_id": "t-002",
            "agent_name": "data-agent",
            "task_type": "DATA_GRABBING",
            "provider": "deepseek",
            "model": "deepseek-v4-flash",
            "estimated_cost": 0.0001,
            "cache_hit": True,
            "fallback_used": False,
            "success": True,
            "latency_ms": 400,
            "dry_run": False,
        },
        {
            "timestamp": (now - timedelta(hours=1)).isoformat(),
            "task_id": "t-003",
            "agent_name": "programmer-agent",
            "task_type": "CODE_GENERATION",
            "provider": "claude",
            "model": "claude-opus-4-7",
            "estimated_cost": 0.012,
            "cache_hit": False,
            "fallback_used": True,
            "success": False,
            "latency_ms": 3000,
            "error_summary": "API error: 503 Service Unavailable",
            "dry_run": False,
        },
        {
            "timestamp": (now - timedelta(minutes=30)).isoformat(),
            "task_id": "t-004",
            "agent_name": "review-agent",
            "task_type": "CLASSIFICATION",
            "provider": "deepseek",
            "model": "deepseek-v4-pro",
            "estimated_cost": 0.0002,
            "cache_hit": False,
            "fallback_used": False,
            "success": True,
            "latency_ms": 500,
            "dry_run": False,
        },
    ]


@pytest.fixture
def mixed_entries(sample_entries):
    """Mix of real and dry-run calls."""
    now = datetime.now(timezone.utc)
    entries = list(sample_entries)
    entries.append({
        "timestamp": (now - timedelta(minutes=10)).isoformat(),
        "task_id": "t-dry-1",
        "agent_name": "research-agent",
        "task_type": "SUMMARIZATION",
        "provider": "deepseek",
        "model": "deepseek-v4-flash",
        "estimated_cost": 0.0005,
        "cache_hit": False,
        "fallback_used": False,
        "success": True,
        "latency_ms": 0,
        "dry_run": True,
    })
    entries.append({
        "timestamp": (now - timedelta(minutes=5)).isoformat(),
        "task_id": "t-dry-2",
        "agent_name": "risk-agent",
        "task_type": "RISK_REVIEW",
        "provider": "claude",
        "model": "claude-sonnet-4-6",
        "estimated_cost": 0.01,
        "cache_hit": False,
        "fallback_used": False,
        "success": True,
        "latency_ms": 0,
        "dry_run": True,
    })
    return entries


class TestComputeOverview:
    def test_empty_input(self, empty_entries):
        result = compute_overview(empty_entries)
        assert result["total_calls"] == 0
        assert result["real_count"] == 0
        assert result["dry_run_count"] == 0
        assert result["total_cost"] == 0.0

    def test_with_entries(self, sample_entries):
        result = compute_overview(sample_entries)
        assert result["total_calls"] == 4
        assert result["real_count"] == 4
        assert result["dry_run_count"] == 0
        assert result["success_count"] == 3
        assert result["failure_count"] == 1
        assert result["cache_hit_count"] == 1
        assert result["cache_hit_ratio"] == 0.25
        assert result["fallback_count"] == 1
        assert result["fallback_ratio"] == 0.25
        assert result["claude_count"] == 2
        assert result["deepseek_count"] == 2
        assert result["total_cost"] == round(0.003 + 0.0001 + 0.012 + 0.0002, 6)
        assert result["real_cost"] == result["total_cost"]
        assert result["success_rate"] == 0.75
        assert result["avg_latency_ms"] == round((1200 + 400 + 3000 + 500) / 4, 1)

    def test_dry_run_not_counted_as_cost(self, mixed_entries):
        """Dry-run calls should not contribute to total_cost."""
        result = compute_overview(mixed_entries)
        assert result["total_calls"] == 6
        assert result["real_count"] == 4
        assert result["dry_run_count"] == 2
        # Cost should only be from real calls (same as sample_entries)
        assert result["total_cost"] == round(0.003 + 0.0001 + 0.012 + 0.0002, 6)
        assert result["real_cost"] == result["total_cost"]


class TestMixedEntries:
    """Tests for real + dry-run mixed scenarios."""

    def test_dry_run_entries_present_in_total(self, mixed_entries):
        result = compute_overview(mixed_entries)
        assert result["total_calls"] == 6  # 4 real + 2 dry

    def test_cache_savings_only_real(self, mixed_entries):
        result = compute_cache_savings(mixed_entries)
        # Only 1 cache hit in real entries (sample_entries has 1)
        assert result["cache_hit_count"] == 1
        assert result["estimated_savings"] == 0.0001

    def test_provider_metrics_exclude_dry_run_cost(self, mixed_entries):
        result = compute_provider_metrics(mixed_entries, "deepseek")
        # 2 real deepseek calls + 1 dry-run deepseek call
        assert result["total_calls"] == 3
        assert result["real_count"] == 2
        assert result["dry_run_count"] == 1
        # Cost only from real calls: 0.0001 + 0.0002 = 0.0003
        assert result["total_cost"] == 0.0003

    def test_agent_metrics_exclude_dry_run_cost(self, mixed_entries):
        result = compute_agent_metrics(mixed_entries, "research-agent")
        assert result["total_calls"] == 2  # 1 real + 1 dry-run
        assert result["real_count"] == 1
        assert result["dry_run_count"] == 1
        assert result["total_cost"] == 0.003  # only the real call cost


class TestComputeProviderMetrics:
    def test_empty_group(self, empty_entries):
        result = compute_provider_metrics(empty_entries, "claude")
        assert result["provider"] == "claude"
        assert result["total_calls"] == 0
        assert result["success_rate"] == 0.0
        assert result["models_used"] == []

    def test_claude_metrics(self, sample_entries):
        result = compute_provider_metrics(sample_entries, "claude")
        assert result["provider"] == "claude"
        assert result["total_calls"] == 2
        assert result["success_count"] == 1
        assert result["failure_count"] == 1
        assert result["total_cost"] == 0.015
        assert result["avg_latency_ms"] == 2100.0
        assert set(result["models_used"]) == {"claude-sonnet-4-6", "claude-opus-4-7"}
        assert result["last_error"] == "API error: 503 Service Unavailable"

    def test_deepseek_metrics(self, sample_entries):
        result = compute_provider_metrics(sample_entries, "deepseek")
        assert result["provider"] == "deepseek"
        assert result["total_calls"] == 2
        assert result["success_count"] == 2
        assert result["failure_count"] == 0
        assert result["last_error"] is None

    def test_last_error_returns_most_recent(self, sample_entries):
        # Add another failure earlier to verify we get the latest
        sample_entries.append({
            "task_id": "t-005",
            "provider": "claude",
            "success": False,
            "error_summary": "older error",
            "estimated_cost": 0,
            "latency_ms": 100,
        })
        result = compute_provider_metrics(sample_entries, "claude")
        # Most recent non-success with error_summary
        assert result["last_error"] == "older error"


class TestComputeAgentMetrics:
    def test_empty_group(self, empty_entries):
        result = compute_agent_metrics(empty_entries, "research-agent")
        assert result["agent"] == "research-agent"
        assert result["total_calls"] == 0
        assert result["total_cost"] == 0.0

    def test_with_entries(self, sample_entries):
        result = compute_agent_metrics(sample_entries, "data-agent")
        assert result["agent"] == "data-agent"
        assert result["total_calls"] == 1
        assert result["total_cost"] == 0.0001
        assert result["deepseek_count"] == 1
        assert result["claude_count"] == 0
        assert result["task_type_split"] == {"DATA_GRABBING": 1}

    def test_task_type_split(self, sample_entries):
        # Add another entry for same agent
        sample_entries.append({
            "task_id": "t-005",
            "agent_name": "research-agent",
            "task_type": "MEMO_WRITING",
            "provider": "claude",
            "model": "claude-sonnet-4-6",
            "estimated_cost": 0.005,
            "cache_hit": False,
            "fallback_used": False,
            "success": True,
            "latency_ms": 2000,
        })
        result = compute_agent_metrics(sample_entries, "research-agent")
        assert result["total_calls"] == 2
        assert result["task_type_split"] == {"RESEARCH_REASONING": 1, "MEMO_WRITING": 1}


class TestComputeFailures:
    def test_empty(self, empty_entries):
        assert compute_failures(empty_entries) == []

    def test_only_successes(self):
        entries = [
            {"task_id": "ok1", "success": True},
            {"task_id": "ok2", "success": True},
        ]
        assert compute_failures(entries) == []

    def test_extracts_failures(self, sample_entries):
        failures = compute_failures(sample_entries)
        assert len(failures) == 1
        f = failures[0]
        assert f["task_id"] == "t-003"
        assert f["agent_name"] == "programmer-agent"
        assert f["error_summary"] == "API error: 503 Service Unavailable"
        assert f["fallback_used"] is True

    def test_handles_missing_error_field(self):
        entries = [{"task_id": "fail1", "success": False}]
        failures = compute_failures(entries)
        assert len(failures) == 1
        assert failures[0]["error_summary"] == ""


class TestComputeCacheSavings:
    def test_empty(self, empty_entries):
        result = compute_cache_savings(empty_entries)
        assert result["cache_hit_count"] == 0
        assert result["estimated_savings"] == 0.0
        assert result["cache_hit_ratio"] == 0.0

    def test_with_hits(self, sample_entries):
        result = compute_cache_savings(sample_entries)
        assert result["cache_hit_count"] == 1
        assert result["estimated_savings"] == 0.0001
        assert result["cache_hit_ratio"] == 0.25
