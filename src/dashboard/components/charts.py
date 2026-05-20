"""Chart components for the LLM Router dashboard."""

import streamlit as st
import pandas as pd
from typing import Any

from ..backend.aggregation import (
    daily_buckets,
    group_by_agent,
    group_by_provider,
    group_by_task_type,
    time_buckets,
)


def _ensure_generic_chart_imports():
    """Lazy-import plotly safely."""
    try:
        import plotly.express as px
        import plotly.graph_objects as go

        return px, go
    except ImportError:
        return None, None


def requests_over_time(entries: list[dict[str, Any]]) -> None:
    """Line chart of requests over time bucketed by hour."""
    px, go = _ensure_generic_chart_imports()
    if px is None:
        st.info("Plotly not installed — install with: pip install plotly")
        return

    buckets = time_buckets(entries, bucket_minutes=60)
    if not buckets:
        st.caption("No time-series data available.")
        return

    df = pd.DataFrame([
        {"time": k, "requests": v["count"]}
        for k, v in sorted(buckets.items())
    ])
    fig = px.line(df, x="time", y="requests", markers=True,
                  title="Requests Over Time (hourly)")
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)


def cost_over_time(entries: list[dict[str, Any]]) -> None:
    """Line chart of estimated cost over time bucketed by day."""
    px, go = _ensure_generic_chart_imports()
    if px is None:
        return

    buckets = daily_buckets(entries)
    if not buckets:
        st.caption("No cost data available.")
        return

    df = pd.DataFrame([
        {"day": k[:10], "cost": round(v["total_cost"], 6)}
        for k, v in sorted(buckets.items())
    ])
    fig = px.bar(df, x="day", y="cost", title="Estimated Cost per Day")
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)


def provider_distribution(entries: list[dict[str, Any]]) -> None:
    """Pie chart of provider distribution."""
    px, go = _ensure_generic_chart_imports()
    if px is None:
        return

    groups = group_by_provider(entries)
    if not groups:
        st.caption("No provider data.")
        return

    df = pd.DataFrame([
        {"provider": k, "count": len(v)} for k, v in groups.items()
    ])
    fig = px.pie(df, names="provider", values="count", title="Provider Distribution")
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)


def task_type_distribution(entries: list[dict[str, Any]]) -> None:
    """Bar chart of task type distribution."""
    px, go = _ensure_generic_chart_imports()
    if px is None:
        return

    groups = group_by_task_type(entries)
    if not groups:
        st.caption("No task type data.")
        return

    df = pd.DataFrame([
        {"task_type": k, "count": len(v)} for k, v in groups.items()
    ]).sort_values("count", ascending=True)

    fig = px.bar(df, x="count", y="task_type", orientation="h",
                 title="Task Type Distribution")
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)


def agent_distribution(entries: list[dict[str, Any]]) -> None:
    """Bar chart of agent distribution."""
    px, go = _ensure_generic_chart_imports()
    if px is None:
        return

    groups = group_by_agent(entries)
    if not groups:
        st.caption("No agent data.")
        return

    df = pd.DataFrame([
        {"agent": k, "count": len(v)} for k, v in groups.items()
    ]).sort_values("count", ascending=True)

    fig = px.bar(df, x="count", y="agent", orientation="h",
                 title="Agent Distribution")
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)


def latency_distribution(entries: list[dict[str, Any]]) -> None:
    """Histogram of latency values."""
    px, go = _ensure_generic_chart_imports()
    if px is None:
        return

    latencies = [e.get("latency_ms") for e in entries if e.get("latency_ms")]
    if not latencies:
        st.caption("No latency data.")
        return

    df = pd.DataFrame({"latency_ms": latencies})
    fig = px.histogram(df, x="latency_ms", nbins=30,
                       title="Latency Distribution")
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)


def cost_by_category(
    entries: list[dict[str, Any]],
    group_key: str = "provider",
    title: str = "Cost by Provider",
) -> None:
    """Bar chart of cost grouped by a category."""
    px, go = _ensure_generic_chart_imports()
    if px is None:
        return

    cost_map: dict[str, float] = {}
    for e in entries:
        key = e.get(group_key, "unknown")
        cost = e.get("estimated_cost") or 0
        cost_map[key] = cost_map.get(key, 0) + cost

    if not cost_map:
        st.caption("No cost data.")
        return

    df = pd.DataFrame([
        {group_key: k, "cost": round(v, 6)} for k, v in cost_map.items()
    ]).sort_values("cost", ascending=True)

    fig = px.bar(df, x="cost", y=group_key, orientation="h", title=title)
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)
