"""Filter controls for the LLM Router dashboard."""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import streamlit as st


def render_global_filters(
    entries: list[dict[str, Any]],
) -> dict[str, Any]:
    """Render global filter controls in the sidebar.

    Returns a dict of filter criteria to apply to entries.
    """
    st.sidebar.header("Filters")

    # Time range
    time_options = {
        "All time": None,
        "Last 24 hours": timedelta(hours=24),
        "Last 7 days": timedelta(days=7),
        "Last 30 days": timedelta(days=30),
        "Last 1 hour": timedelta(hours=1),
    }
    time_choice = st.sidebar.selectbox("Time Range", list(time_options.keys()))
    time_delta = time_options[time_choice]

    since: Optional[datetime] = None
    if time_delta is not None:
        since = datetime.now(timezone.utc) - time_delta

    # Provider filter
    providers = sorted({e.get("provider", "") for e in entries if e.get("provider")})
    selected_provider = st.sidebar.selectbox(
        "Provider", ["All"] + providers,
    )

    # Agent filter
    agents = sorted({e.get("agent_name", "") for e in entries if e.get("agent_name")})
    selected_agent = st.sidebar.selectbox(
        "Agent", ["All"] + agents,
    )

    # Task type filter
    task_types = sorted({e.get("task_type", "") for e in entries if e.get("task_type")})
    selected_task = st.sidebar.selectbox(
        "Task Type", ["All"] + task_types,
    )

    # Success filter
    success_options = {"All": None, "Success": True, "Failure": False}
    success_choice = st.sidebar.selectbox("Status", list(success_options.keys()))
    success_filter = success_options[success_choice]

    # Cache hit filter
    cache_options = {"All": None, "Cache Hit": True, "Cache Miss": False}
    cache_choice = st.sidebar.selectbox("Cache", list(cache_options.keys()))
    cache_filter = cache_options[cache_choice]

    # Fallback filter
    fb_options = {"All": None, "Fallback Used": True, "No Fallback": False}
    fb_choice = st.sidebar.selectbox("Fallback", list(fb_options.keys()))
    fb_filter = fb_options[fb_choice]

    # Call type filter (real vs dry-run)
    call_type_options = {"All Calls": None, "Real Calls Only": False, "Dry-Run Calls Only": True}
    call_type_choice = st.sidebar.selectbox("Call Type", list(call_type_options.keys()))
    call_type_filter = call_type_options[call_type_choice]

    # Limit
    limit = st.sidebar.slider("Max entries", 10, 500, 200, step=10)

    return {
        "since": since,
        "provider": selected_provider if selected_provider != "All" else None,
        "agent": selected_agent if selected_agent != "All" else None,
        "task_type": selected_task if selected_task != "All" else None,
        "success": success_filter,
        "cache_hit": cache_filter,
        "fallback": fb_filter,
        "call_type": call_type_filter,
        "limit": limit,
    }


def apply_filters(
    entries: list[dict[str, Any]],
    filters: dict[str, Any],
) -> list[dict[str, Any]]:
    """Apply filter criteria to a list of entries."""
    result = entries

    # Time filter
    since = filters.get("since")
    if since is not None:
        result = [
            e for e in result
            if _ts_after(e.get("timestamp"), since)
        ]

    # Provider
    provider = filters.get("provider")
    if provider:
        result = [e for e in result if e.get("provider") == provider]

    # Agent
    agent = filters.get("agent")
    if agent:
        result = [e for e in result if e.get("agent_name") == agent]

    # Task type
    task_type = filters.get("task_type")
    if task_type:
        result = [e for e in result if e.get("task_type") == task_type]

    # Success
    success = filters.get("success")
    if success is not None:
        result = [e for e in result if e.get("success") == success]

    # Cache hit
    cache_hit = filters.get("cache_hit")
    if cache_hit is not None:
        result = [e for e in result if e.get("cache_hit") == cache_hit]

    # Fallback
    fallback = filters.get("fallback")
    if fallback is not None:
        result = [e for e in result if e.get("fallback_used") == fallback]

    # Call type (real vs dry-run)
    call_type = filters.get("call_type")
    if call_type is not None:
        result = [e for e in result if e.get("dry_run", False) == call_type]

    # Limit
    limit = filters.get("limit", 200)
    if limit > 0:
        result = result[-limit:]

    return result


def _ts_after(ts_str: str | None, cutoff: datetime) -> bool:
    if not ts_str:
        return True
    try:
        ts = datetime.fromisoformat(ts_str)
        return ts >= cutoff
    except (ValueError, TypeError):
        return True
