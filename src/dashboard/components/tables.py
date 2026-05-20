"""Table components for the LLM Router dashboard."""

import streamlit as st
import pandas as pd
from typing import Any


def render_routing_table(entries: list[dict[str, Any]]) -> None:
    """Render a sortable table of routing decisions / usage entries."""
    if not entries:
        st.caption("No entries to display.")
        return

    rows = []
    for e in entries:
        rows.append({
            "Timestamp": _fmt_ts(e.get("timestamp")),
            "Task ID": e.get("task_id", "")[:16],
            "Agent": e.get("agent_name", ""),
            "Task Type": e.get("task_type", ""),
            "Provider": e.get("provider", ""),
            "Model": e.get("model", ""),
            "Type": "Dry-Run" if e.get("dry_run") else "Real",
            "Success": "✓" if e.get("success") else "✗",
            "Cache": "✓" if e.get("cache_hit") else "",
            "Fallback": "✓" if e.get("fallback_used") else "",
            "Latency (ms)": e.get("latency_ms", ""),
            "Cost": f"${e.get('estimated_cost', 0):.4f}" if e.get("estimated_cost") else "",
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_failures_table(failures: list[dict[str, Any]]) -> None:
    """Render a table of failed calls."""
    if not failures:
        st.success("No failures recorded.")
        return

    rows = []
    for f in failures:
        rows.append({
            "Timestamp": _fmt_ts(f.get("timestamp")),
            "Task ID": f.get("task_id", "")[:16],
            "Agent": f.get("agent_name", ""),
            "Task Type": f.get("task_type", ""),
            "Provider": f.get("provider", ""),
            "Model": f.get("model", ""),
            "Error": (f.get("error_summary") or f.get("error", ""))[:150],
            "Fallback": "✓" if f.get("fallback_used") else "",
            "Latency (ms)": f.get("latency_ms", ""),
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_agent_summary_table(agent_metrics: dict[str, dict]) -> None:
    """Render a table summarizing all agents."""
    if not agent_metrics:
        st.caption("No agent data.")
        return

    rows = []
    for agent, m in sorted(agent_metrics.items()):
        rows.append({
            "Agent": agent.replace("-agent", "").title(),
            "Calls": m.get("total_calls", 0),
            "Cost": f"${m.get('total_cost', 0):.4f}",
            "Claude": m.get("claude_count", 0),
            "DeepSeek": m.get("deepseek_count", 0),
            "Avg Latency": f"{m.get('avg_latency_ms', 0):.0f}ms",
            "Failures": m.get("failure_count", 0),
            "Fallbacks": m.get("fallback_count", 0),
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_cost_table(entries: list[dict[str, Any]], n: int = 20) -> None:
    """Render a table of the most expensive calls."""
    from ..backend.aggregation import top_expensive

    top = top_expensive(entries, n=n)
    if not top:
        st.caption("No cost data.")
        return

    rows = []
    for e in top:
        rows.append({
            "Timestamp": _fmt_ts(e.get("timestamp")),
            "Agent": e.get("agent_name", ""),
            "Task Type": e.get("task_type", ""),
            "Provider": e.get("provider", ""),
            "Model": e.get("model", ""),
            "Type": "Dry-Run" if e.get("dry_run") else "Real",
            "Cost": f"${e.get('estimated_cost', 0):.6f}",
            "Latency (ms)": e.get("latency_ms", ""),
            "Cache": "✓" if e.get("cache_hit") else "",
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------


def _fmt_ts(ts_str: str | None) -> str:
    if not ts_str:
        return ""
    # Truncate to readable format
    if "T" in ts_str:
        return ts_str[:19].replace("T", " ")
    return ts_str[:19]
