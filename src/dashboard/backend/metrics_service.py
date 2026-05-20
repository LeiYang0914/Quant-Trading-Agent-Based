"""Compute aggregate metrics from LLM usage log entries.

All functions are pure: accept a list of entries, return a metrics dict or value.
No side effects, no UI dependencies.
"""

from typing import Any


def compute_overview(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute top-level KPIs from usage entries.

    Costs are only counted for real (non-dry-run) calls.
    """
    total = len(entries)
    if total == 0:
        return _empty_overview()

    real = [e for e in entries if not e.get("dry_run", False)]
    dry_runs = [e for e in entries if e.get("dry_run", False)]

    successes = sum(1 for e in entries if e.get("success"))
    failures = total - successes
    cache_hits = sum(1 for e in entries if e.get("cache_hit"))
    fallbacks = sum(1 for e in entries if e.get("fallback_used"))
    claude_count = sum(1 for e in entries if e.get("provider") == "claude")
    deepseek_count = sum(1 for e in entries if e.get("provider") == "deepseek")
    total_cost = sum(e.get("estimated_cost") or 0 for e in real)
    real_cost = sum(e.get("estimated_cost") or 0 for e in real)
    total_latency = sum(e.get("latency_ms") or 0 for e in entries)

    return {
        "total_calls": total,
        "real_count": len(real),
        "dry_run_count": len(dry_runs),
        "total_cost": round(total_cost, 6),
        "real_cost": round(real_cost, 6),
        "success_rate": round(successes / total, 4),
        "success_count": successes,
        "failure_count": failures,
        "cache_hit_ratio": round(cache_hits / total, 4),
        "cache_hit_count": cache_hits,
        "fallback_ratio": round(fallbacks / total, 4),
        "fallback_count": fallbacks,
        "avg_latency_ms": round(total_latency / total, 1),
        "claude_count": claude_count,
        "deepseek_count": deepseek_count,
    }


def compute_provider_metrics(
    entries: list[dict[str, Any]],
    provider: str,
) -> dict[str, Any]:
    """Compute metrics for a single provider.

    Costs are only counted for real (non-dry-run) calls.
    """
    group = [e for e in entries if e.get("provider") == provider]
    total = len(group)
    if total == 0:
        return _empty_provider_metrics(provider)

    real = [e for e in group if not e.get("dry_run", False)]
    successes = sum(1 for e in group if e.get("success"))
    failures = total - successes
    total_latency = sum(e.get("latency_ms") or 0 for e in group)
    total_cost = sum(e.get("estimated_cost") or 0 for e in real)
    models = list({e.get("model") for e in group if e.get("model")})
    last_error = None
    for e in reversed(group):
        if not e.get("success") and e.get("error_summary"):
            last_error = e["error_summary"]
            break

    return {
        "provider": provider,
        "total_calls": total,
        "real_count": len(real),
        "dry_run_count": total - len(real),
        "success_rate": round(successes / total, 4) if total else 0,
        "success_count": successes,
        "failure_count": failures,
        "avg_latency_ms": round(total_latency / total, 1) if total else 0,
        "total_cost": round(total_cost, 6),
        "models_used": models,
        "last_error": last_error,
    }


def compute_agent_metrics(
    entries: list[dict[str, Any]],
    agent: str,
) -> dict[str, Any]:
    """Compute metrics for a single agent.

    Costs are only counted for real (non-dry-run) calls.
    """
    group = [e for e in entries if e.get("agent_name") == agent]
    total = len(group)
    if total == 0:
        return _empty_agent_metrics(agent)

    real = [e for e in group if not e.get("dry_run", False)]
    successes = sum(1 for e in group if e.get("success"))
    failures = total - successes
    total_latency = sum(e.get("latency_ms") or 0 for e in group)
    total_cost = sum(e.get("estimated_cost") or 0 for e in real)
    fallbacks = sum(1 for e in group if e.get("fallback_used"))

    # Provider split
    claude_count = sum(1 for e in group if e.get("provider") == "claude")
    deepseek_count = sum(1 for e in group if e.get("provider") == "deepseek")

    # Task type split
    task_types: dict[str, int] = {}
    for e in group:
        tt = e.get("task_type", "unknown")
        task_types[tt] = task_types.get(tt, 0) + 1

    return {
        "agent": agent,
        "total_calls": total,
        "real_count": len(real),
        "dry_run_count": total - len(real),
        "total_cost": round(total_cost, 6),
        "avg_latency_ms": round(total_latency / total, 1) if total else 0,
        "success_count": successes,
        "failure_count": failures,
        "fallback_count": fallbacks,
        "claude_count": claude_count,
        "deepseek_count": deepseek_count,
        "task_type_split": task_types,
    }


def compute_failures(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract failure entries with relevant fields."""
    failures = []
    for e in entries:
        if e.get("success"):
            continue
        failures.append({
            "timestamp": e.get("timestamp"),
            "task_id": e.get("task_id"),
            "agent_name": e.get("agent_name"),
            "task_type": e.get("task_type"),
            "provider": e.get("provider"),
            "model": e.get("model"),
            "error_summary": e.get("error_summary") or e.get("error", ""),
            "fallback_used": e.get("fallback_used", False),
            "latency_ms": e.get("latency_ms"),
        })
    return failures


def compute_cache_savings(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Estimate cost savings from cache hits (real calls only)."""
    real = [e for e in entries if not e.get("dry_run", False)]
    hits = [e for e in real if e.get("cache_hit")]
    total_saved = sum(e.get("estimated_cost") or 0 for e in hits)
    return {
        "cache_hit_count": len(hits),
        "estimated_savings": round(total_saved, 6),
        "cache_hit_ratio": round(len(hits) / len(real), 4) if real else 0,
    }


# ------------------------------------------------------------------
# Empty state helpers
# ------------------------------------------------------------------


def _empty_overview() -> dict[str, Any]:
    return {
        "total_calls": 0,
        "real_count": 0,
        "dry_run_count": 0,
        "total_cost": 0.0,
        "real_cost": 0.0,
        "success_rate": 1.0,
        "success_count": 0,
        "failure_count": 0,
        "cache_hit_ratio": 0.0,
        "cache_hit_count": 0,
        "fallback_ratio": 0.0,
        "fallback_count": 0,
        "avg_latency_ms": 0.0,
        "claude_count": 0,
        "deepseek_count": 0,
    }


def _empty_provider_metrics(provider: str) -> dict[str, Any]:
    return {
        "provider": provider,
        "total_calls": 0,
        "real_count": 0,
        "dry_run_count": 0,
        "success_rate": 0.0,
        "success_count": 0,
        "failure_count": 0,
        "avg_latency_ms": 0.0,
        "total_cost": 0.0,
        "models_used": [],
        "last_error": None,
    }


def _empty_agent_metrics(agent: str) -> dict[str, Any]:
    return {
        "agent": agent,
        "total_calls": 0,
        "real_count": 0,
        "dry_run_count": 0,
        "total_cost": 0.0,
        "avg_latency_ms": 0.0,
        "success_count": 0,
        "failure_count": 0,
        "fallback_count": 0,
        "claude_count": 0,
        "deepseek_count": 0,
        "task_type_split": {},
    }
