"""Tests for dashboard backend log_reader module."""

import json
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from src.dashboard.backend.log_reader import (
    count_entries,
    log_file_exists,
    read_routing_log,
    read_usage_log,
)


def _write_jsonl(path: Path, entries: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")


@pytest.fixture
def sample_entries():
    now = datetime.now(timezone.utc)
    return [
        {
            "timestamp": (now - timedelta(hours=2)).isoformat(),
            "task_id": "task-001",
            "agent_name": "research-agent",
            "task_type": "RESEARCH_REASONING",
            "provider": "claude",
            "model": "claude-sonnet-4-6",
            "input_tokens": 500,
            "output_tokens": 200,
            "estimated_cost": 0.0021,
            "cache_hit": False,
            "fallback_used": False,
            "success": True,
            "latency_ms": 1500,
            "dry_run": False,
        },
        {
            "timestamp": (now - timedelta(hours=1)).isoformat(),
            "task_id": "task-002",
            "agent_name": "data-agent",
            "task_type": "DATA_GRABBING",
            "provider": "deepseek",
            "model": "deepseek-v4-flash",
            "input_tokens": 200,
            "output_tokens": 50,
            "estimated_cost": 0.000075,
            "cache_hit": True,
            "fallback_used": False,
            "success": True,
            "latency_ms": 300,
            "dry_run": False,
        },
        {
            "timestamp": (now - timedelta(minutes=30)).isoformat(),
            "task_id": "task-003",
            "agent_name": "risk-agent",
            "task_type": "RISK_REVIEW",
            "provider": "claude",
            "model": "claude-opus-4-7",
            "input_tokens": 1000,
            "output_tokens": 0,
            "estimated_cost": 0.003,
            "cache_hit": False,
            "fallback_used": True,
            "success": False,
            "latency_ms": 800,
            "error_summary": "Connection timeout after 120s",
            "dry_run": False,
        },
    ]


class TestReadUsageLog:
    def test_returns_empty_list_for_non_existent_file(self):
        result = read_usage_log(path=Path("/nonexistent/usage.jsonl"))
        assert result == []

    def test_parses_entries_correctly(self, sample_entries, tmp_path):
        log_path = tmp_path / "usage.jsonl"
        _write_jsonl(log_path, sample_entries)

        result = read_usage_log(path=log_path)
        assert len(result) == 3
        assert result[0]["task_id"] == "task-001"
        assert result[1]["task_id"] == "task-002"
        assert result[2]["task_id"] == "task-003"

    def test_filters_by_since(self, sample_entries, tmp_path):
        log_path = tmp_path / "usage.jsonl"
        _write_jsonl(log_path, sample_entries)
        now = datetime.now(timezone.utc)

        result = read_usage_log(path=log_path, since=now - timedelta(minutes=45))
        assert len(result) == 1
        assert result[0]["task_id"] == "task-003"

    def test_filters_by_until(self, sample_entries, tmp_path):
        log_path = tmp_path / "usage.jsonl"
        _write_jsonl(log_path, sample_entries)
        now = datetime.now(timezone.utc)

        result = read_usage_log(path=log_path, until=now - timedelta(minutes=45))
        assert len(result) == 2
        assert result[0]["task_id"] == "task-001"
        assert result[1]["task_id"] == "task-002"

    def test_applies_limit(self, sample_entries, tmp_path):
        log_path = tmp_path / "usage.jsonl"
        _write_jsonl(log_path, sample_entries)

        result = read_usage_log(path=log_path, limit=2)
        assert len(result) == 2
        # Limit returns last N entries
        assert result[0]["task_id"] == "task-002"
        assert result[1]["task_id"] == "task-003"

    def test_handles_bad_json_lines(self, sample_entries, tmp_path):
        log_path = tmp_path / "usage.jsonl"
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("not valid json\n")
            f.write(json.dumps(sample_entries[0]) + "\n")
            f.write("also not json}\n")
            f.write(json.dumps(sample_entries[1]) + "\n")

        result = read_usage_log(path=log_path)
        assert len(result) == 2
        assert result[0]["task_id"] == "task-001"
        assert result[1]["task_id"] == "task-002"

    def test_handles_empty_lines(self, tmp_path):
        log_path = tmp_path / "usage.jsonl"
        entry = {"task_id": "only", "timestamp": datetime.now(timezone.utc).isoformat()}
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("\n")
            f.write(json.dumps(entry) + "\n")
            f.write("  \n")
            f.write("\n")

        result = read_usage_log(path=log_path)
        assert len(result) == 1
        assert result[0]["task_id"] == "only"

    def test_entries_without_timestamp_always_included(self, tmp_path):
        log_path = tmp_path / "usage.jsonl"
        entry = {"task_id": "no-ts"}
        _write_jsonl(log_path, [entry])

        now = datetime.now(timezone.utc)
        result = read_usage_log(path=log_path, since=now)
        assert len(result) == 1

    def test_parses_dry_run_field(self, tmp_path):
        log_path = tmp_path / "usage.jsonl"
        entries = [
            {"task_id": "real-call", "timestamp": datetime.now(timezone.utc).isoformat(), "dry_run": False, "estimated_cost": 0.01},
            {"task_id": "dry-run-call", "timestamp": datetime.now(timezone.utc).isoformat(), "dry_run": True, "estimated_cost": 0.005},
        ]
        _write_jsonl(log_path, entries)

        result = read_usage_log(path=log_path)
        assert len(result) == 2
        assert result[0]["dry_run"] is False
        assert result[1]["dry_run"] is True
        assert result[0]["task_id"] == "real-call"
        assert result[1]["task_id"] == "dry-run-call"


class TestReadRoutingLog:
    def test_returns_empty_list_for_non_existent_file(self):
        result = read_routing_log(path=Path("/nonexistent/routing.jsonl"))
        assert result == []

    def test_parses_entries_correctly(self, tmp_path):
        log_path = tmp_path / "routing_log.jsonl"
        entries = [
            {"timestamp": datetime.now(timezone.utc).isoformat(), "decision": "claude"},
            {"timestamp": datetime.now(timezone.utc).isoformat(), "decision": "deepseek"},
        ]
        _write_jsonl(log_path, entries)

        result = read_routing_log(path=log_path)
        assert len(result) == 2

    def test_filters_by_time_range(self, tmp_path):
        log_path = tmp_path / "routing_log.jsonl"
        now = datetime.now(timezone.utc)
        entries = [
            {"timestamp": (now - timedelta(hours=5)).isoformat(), "decision": "old"},
            {"timestamp": (now - timedelta(minutes=5)).isoformat(), "decision": "recent"},
        ]
        _write_jsonl(log_path, entries)

        result = read_routing_log(path=log_path, since=now - timedelta(hours=1))
        assert len(result) == 1
        assert result[0]["decision"] == "recent"


class TestLogFileExists:
    def test_returns_false_for_non_existent_file(self):
        assert log_file_exists(path=Path("/nonexistent/usage.jsonl")) is False

    def test_returns_false_for_empty_file(self, tmp_path):
        log_path = tmp_path / "empty.jsonl"
        log_path.write_text("")
        assert log_file_exists(path=log_path) is False

    def test_returns_true_for_non_empty_file(self, tmp_path):
        log_path = tmp_path / "has_content.jsonl"
        log_path.write_text('{"test": true}\n')
        assert log_file_exists(path=log_path) is True


class TestCountEntries:
    def test_returns_zero_for_missing_file(self):
        assert count_entries(path=Path("/nonexistent/usage.jsonl")) == 0

    def test_returns_correct_count(self, sample_entries, tmp_path):
        log_path = tmp_path / "usage.jsonl"
        _write_jsonl(log_path, sample_entries)
        assert count_entries(path=log_path) == 3
