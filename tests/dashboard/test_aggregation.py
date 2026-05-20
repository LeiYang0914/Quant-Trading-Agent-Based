"""Tests for dashboard backend aggregation module."""

from datetime import datetime, timedelta, timezone

import pytest

from src.dashboard.backend.aggregation import (
    daily_buckets,
    group_by_agent,
    group_by_cache_hit,
    group_by_dry_run,
    group_by_fallback,
    group_by_model,
    group_by_provider,
    group_by_success,
    group_by_task_type,
    time_buckets,
    top_expensive,
    top_slowest,
)


@pytest.fixture
def sample_entries():
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
            "dry_run": True,
        },
    ]


class TestGroupByProvider:
    def test_groups_by_provider(self, sample_entries):
        groups = group_by_provider(sample_entries)
        assert len(groups["claude"]) == 2
        assert len(groups["deepseek"]) == 2

    def test_empty_input(self):
        assert group_by_provider([]) == {}


class TestGroupByAgent:
    def test_groups_by_agent(self, sample_entries):
        groups = group_by_agent(sample_entries)
        assert len(groups) == 4
        assert len(groups["research-agent"]) == 1
        assert len(groups["data-agent"]) == 1

    def test_empty_input(self):
        assert group_by_agent([]) == {}


class TestGroupByTaskType:
    def test_groups_by_task_type(self, sample_entries):
        groups = group_by_task_type(sample_entries)
        assert len(groups["RESEARCH_REASONING"]) == 1
        assert len(groups["DATA_GRABBING"]) == 1
        assert len(groups["CODE_GENERATION"]) == 1
        assert len(groups["CLASSIFICATION"]) == 1

    def test_empty_input(self):
        assert group_by_task_type([]) == {}


class TestGroupByModel:
    def test_groups_by_model(self, sample_entries):
        groups = group_by_model(sample_entries)
        assert len(groups) == 4
        assert len(groups["claude-sonnet-4-6"]) == 1
        assert len(groups["claude-opus-4-7"]) == 1

    def test_empty_input(self):
        assert group_by_model([]) == {}


class TestGroupBySuccess:
    def test_groups_by_success(self, sample_entries):
        groups = group_by_success(sample_entries)
        assert len(groups["success"]) == 3
        assert len(groups["failure"]) == 1

    def test_empty_input(self):
        groups = group_by_success([])
        assert groups["success"] == []
        assert groups["failure"] == []


class TestGroupByCacheHit:
    def test_groups_by_cache_hit(self, sample_entries):
        groups = group_by_cache_hit(sample_entries)
        assert len(groups["hit"]) == 1
        assert len(groups["miss"]) == 3

    def test_empty_input(self):
        groups = group_by_cache_hit([])
        assert groups["hit"] == []
        assert groups["miss"] == []


class TestGroupByFallback:
    def test_groups_by_fallback(self, sample_entries):
        groups = group_by_fallback(sample_entries)
        assert len(groups["fallback"]) == 1
        assert len(groups["no_fallback"]) == 3

    def test_empty_input(self):
        groups = group_by_fallback([])
        assert groups["fallback"] == []
        assert groups["no_fallback"] == []


class TestTimeBuckets:
    def test_creates_buckets(self, sample_entries):
        buckets = time_buckets(sample_entries, bucket_minutes=60)
        # All entries are in different hours
        assert len(buckets) == 4

    def test_aggregates_per_bucket_metrics(self, sample_entries):
        buckets = time_buckets(sample_entries, bucket_minutes=1440)
        # All within same day
        assert len(buckets) == 1
        only_bucket = list(buckets.values())[0]
        assert only_bucket["count"] == 4
        assert only_bucket["total_cost"] == 0.003 + 0.0001 + 0.012 + 0.0002
        assert only_bucket["avg_latency"] == round((1200 + 400 + 3000 + 500) / 4, 1)

    def test_handles_entries_without_timestamp(self):
        entries = [
            {"task_id": "no-ts", "estimated_cost": 1.0, "latency_ms": 100},
        ]
        buckets = time_buckets(entries, bucket_minutes=60)
        assert len(buckets) == 0

    def test_empty_input(self):
        assert time_buckets([]) == {}


class TestDailyBuckets:
    def test_groups_by_day(self, sample_entries):
        buckets = daily_buckets(sample_entries)
        assert len(buckets) == 1


class TestGroupByDryRun:
    def test_groups_by_dry_run(self, sample_entries):
        groups = group_by_dry_run(sample_entries)
        assert len(groups["real"]) == 3
        assert len(groups["dry_run"]) == 1

    def test_empty_input(self):
        groups = group_by_dry_run([])
        assert groups["real"] == []
        assert groups["dry_run"] == []


class TestTopExpensive:
    def test_returns_top_n(self, sample_entries):
        top = top_expensive(sample_entries, n=2)
        assert len(top) == 2
        assert top[0]["task_id"] == "t-003"  # $0.012
        assert top[1]["task_id"] == "t-001"  # $0.003

    def test_empty_input(self):
        assert top_expensive([]) == []


class TestTopSlowest:
    def test_returns_top_n(self, sample_entries):
        top = top_slowest(sample_entries, n=2)
        assert len(top) == 2
        assert top[0]["task_id"] == "t-003"  # 3000ms
        assert top[1]["task_id"] == "t-001"  # 1200ms

    def test_empty_input(self):
        assert top_slowest([]) == []
