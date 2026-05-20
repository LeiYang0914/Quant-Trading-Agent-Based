"""Aggregation helpers for LLM usage data.

Group and summarize entries by provider, agent, task type, time bucket, etc.
"""

from collections import defaultdict
from datetime import datetime
from typing import Any


def group_by_provider(entries: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group entries by provider field."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for e in entries:
        provider = e.get("provider", "unknown")
        groups[provider].append(e)
    return dict(groups)


def group_by_agent(entries: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group entries by agent_name field."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for e in entries:
        agent = e.get("agent_name", "unknown")
        groups[agent].append(e)
    return dict(groups)


def group_by_task_type(entries: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group entries by task_type field."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for e in entries:
        tt = e.get("task_type", "unknown")
        groups[tt].append(e)
    return dict(groups)


def group_by_model(entries: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group entries by model field."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for e in entries:
        model = e.get("model", "unknown")
        groups[model].append(e)
    return dict(groups)


def group_by_success(entries: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group entries into success and failure buckets."""
    success = [e for e in entries if e.get("success")]
    failure = [e for e in entries if not e.get("success")]
    return {"success": success, "failure": failure}


def group_by_cache_hit(entries: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group entries into cache_hit and cache_miss buckets."""
    hits = [e for e in entries if e.get("cache_hit")]
    misses = [e for e in entries if not e.get("cache_hit")]
    return {"hit": hits, "miss": misses}


def group_by_fallback(entries: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group entries into fallback_used and no_fallback buckets."""
    fb = [e for e in entries if e.get("fallback_used")]
    no_fb = [e for e in entries if not e.get("fallback_used")]
    return {"fallback": fb, "no_fallback": no_fb}


def group_by_dry_run(entries: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group entries into real and dry_run buckets."""
    real = [e for e in entries if not e.get("dry_run", False)]
    dry_runs = [e for e in entries if e.get("dry_run", False)]
    return {"real": real, "dry_run": dry_runs}


def time_buckets(
    entries: list[dict[str, Any]],
    bucket_minutes: int = 60,
) -> dict[str, dict[str, Any]]:
    """Bucket entries into time windows and compute per-bucket metrics.

    Returns dict mapping bucket key to {count, cost, avg_latency, ...}.
    """
    buckets: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"count": 0, "total_cost": 0.0, "total_latency": 0.0}
    )
    for e in entries:
        ts_str = e.get("timestamp")
        if not ts_str:
            continue
        try:
            ts = datetime.fromisoformat(ts_str)
        except (ValueError, TypeError):
            continue
        # Round to bucket (handle buckets >= 60 min with hour rollup)
        total_minutes = ts.hour * 60 + ts.minute
        bucket_minute_of_day = (total_minutes // bucket_minutes) * bucket_minutes
        bucket_hour = bucket_minute_of_day // 60
        bucket_min = bucket_minute_of_day % 60
        bucket_ts = ts.replace(hour=bucket_hour, minute=bucket_min, second=0, microsecond=0)
        key = bucket_ts.isoformat()

        bucket = buckets[key]
        bucket["count"] += 1
        bucket["total_cost"] += e.get("estimated_cost") or 0
        bucket["total_latency"] += e.get("latency_ms") or 0

    for key, b in buckets.items():
        b["avg_latency"] = round(b["total_latency"] / b["count"], 1) if b["count"] else 0

    return dict(buckets)


def daily_buckets(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Aggregate entries by day."""
    return time_buckets(entries, bucket_minutes=1440)


def top_expensive(entries: list[dict[str, Any]], n: int = 10) -> list[dict[str, Any]]:
    """Return the N calls with the highest estimated cost."""
    sorted_entries = sorted(
        entries,
        key=lambda e: e.get("estimated_cost") or 0,
        reverse=True,
    )
    return sorted_entries[:n]


def top_slowest(entries: list[dict[str, Any]], n: int = 10) -> list[dict[str, Any]]:
    """Return the N calls with the highest latency."""
    sorted_entries = sorted(
        entries,
        key=lambda e: e.get("latency_ms") or 0,
        reverse=True,
    )
    return sorted_entries[:n]
