"""KPI metric cards for the dashboard overview."""

import streamlit as st


def render_overview_cards(overview: dict) -> None:
    """Render the main overview KPI cards in a row."""
    col1, col2, col3, col4, col5 = st.columns(5)

    real = overview.get("real_count", 0)
    dry = overview.get("dry_run_count", 0)
    with col1:
        st.metric("Total Calls", overview.get("total_calls", 0),
                  delta=f"{real} real, {dry} dry-run",
                  delta_color="off")
    with col2:
        cost = overview.get("total_cost", 0)
        st.metric("Real API Cost", f"${cost:.4f}")
    with col3:
        rate = overview.get("success_rate", 1.0)
        st.metric("Success Rate", f"{rate:.1%}")
    with col4:
        hits = overview.get("cache_hit_ratio", 0)
        st.metric("Cache Hit Rate", f"{hits:.1%}")
    with col5:
        latency = overview.get("avg_latency_ms", 0)
        st.metric("Avg Latency", f"{latency:.0f}ms")


def render_secondary_cards(overview: dict) -> None:
    """Render secondary KPI cards."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        fb = overview.get("fallback_ratio", 0)
        st.metric("Fallback Rate", f"{fb:.1%}")
    with col2:
        fails = overview.get("failure_count", 0)
        st.metric("Failures", fails, delta=None, delta_color="inverse")
    with col3:
        st.metric("Claude Calls", overview.get("claude_count", 0))
    with col4:
        st.metric("DeepSeek Calls", overview.get("deepseek_count", 0))


def render_provider_card(metrics: dict) -> None:
    """Render a single provider health/cost card."""
    provider = metrics.get("provider", "unknown")
    st.metric(
        label=f"{provider.title()} Calls",
        value=metrics.get("total_calls", 0),
    )
    cols = st.columns(3)
    with cols[0]:
        st.metric("Success Rate", f"{metrics.get('success_rate', 0):.1%}")
    with cols[1]:
        st.metric("Avg Latency", f"{metrics.get('avg_latency_ms', 0):.0f}ms")
    with cols[2]:
        st.metric("Est. Cost", f"${metrics.get('total_cost', 0):.4f}")


def render_agent_card(metrics: dict) -> None:
    """Render a single agent summary card."""
    agent = metrics.get("agent", "unknown")
    display = agent.replace("-agent", "").title()
    st.metric(label=display, value=metrics.get("total_calls", 0))

    cols = st.columns(4)
    with cols[0]:
        st.metric("Cost", f"${metrics.get('total_cost', 0):.4f}")
    with cols[1]:
        st.metric("Claude", metrics.get("claude_count", 0))
    with cols[2]:
        st.metric("DeepSeek", metrics.get("deepseek_count", 0))
    with cols[3]:
        st.metric("Failures", metrics.get("failure_count", 0))
