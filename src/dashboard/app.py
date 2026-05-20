"""LLM Router Dashboard — browser-based observability.

Run with:
    streamlit run src/dashboard/app.py
or:
    python scripts/run_dashboard.py
"""

import sys
from pathlib import Path

# Ensure project root is on path so `from src.llm import ...` works.
_project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_project_root))

import streamlit as st

from src.dashboard.backend.aggregation import (
    group_by_agent,
    group_by_task_type,
)
from src.dashboard.backend.health_service import get_health
from src.dashboard.backend.log_reader import (
    DEFAULT_USAGE_LOG,
    log_file_exists,
    read_usage_log,
)
from src.dashboard.backend.metrics_service import (
    compute_agent_metrics,
    compute_cache_savings,
    compute_failures,
    compute_overview,
    compute_provider_metrics,
)
from src.dashboard.components.charts import (
    agent_distribution,
    cost_by_category,
    cost_over_time,
    latency_distribution,
    provider_distribution,
    requests_over_time,
    task_type_distribution,
)
from src.dashboard.components.filters import apply_filters, render_global_filters
from src.dashboard.components.metric_cards import (
    render_agent_card,
    render_overview_cards,
    render_provider_card,
    render_secondary_cards,
)
from src.dashboard.components.tables import (
    render_agent_summary_table,
    render_cost_table,
    render_failures_table,
    render_routing_table,
)

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------

st.set_page_config(
    page_title="LLM Router Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------

st.sidebar.title("LLM Router Dashboard")
st.sidebar.caption("Observability for the LLM Router infrastructure layer")

# Load data
_has_logs = log_file_exists()
_all_entries = read_usage_log()

# Navigation
page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Providers",
        "Agents",
        "Costs",
        "Routing",
        "Failures",
        "Cache",
        "Health",
    ],
)

st.sidebar.divider()
if st.sidebar.button("Refresh Data"):
    st.rerun()

# Show log file info
st.sidebar.caption(f"Log: `{DEFAULT_USAGE_LOG}`")
st.sidebar.caption(f"Entries: {len(_all_entries):,}")

# ------------------------------------------------------------------
# Empty state
# ------------------------------------------------------------------

if not _has_logs:
    st.title("LLM Router Dashboard")
    st.info(
        "No real LLM usage logs found yet. "
        "Run real or dry-run LLM Router calls to populate logs.\n\n"
        "```bash\n"
        "# Dry-run call (no API key needed):\n"
        "python scripts/llm_router_cli.py --dry-run --agent research-agent "
        "--task research_reasoning --prompt \"Analyze market structure\"\n\n"
        "# Real API call (requires API keys configured):\n"
        "python scripts/llm_router_cli.py --real --agent data-agent "
        "--task summarization --prompt \"Summarize this data\"\n"
        "```"
    )
    # Still show health
    st.divider()
    st.subheader("Provider Health")
    _render_health_page()
    st.stop()

# ------------------------------------------------------------------
# Filters (shown on most pages)
# ------------------------------------------------------------------

filters = render_global_filters(_all_entries)
_filtered = apply_filters(_all_entries, filters)
_overview = compute_overview(_filtered)


# ==================================================================
# Page: Overview
# ==================================================================

if page == "Overview":
    st.title("Overview")

    render_overview_cards(_overview)
    st.divider()
    render_secondary_cards(_overview)
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        requests_over_time(_filtered)
        provider_distribution(_filtered)
    with col2:
        cost_over_time(_filtered)
        task_type_distribution(_filtered)

    st.divider()
    agent_distribution(_filtered)


# ==================================================================
# Page: Providers
# ==================================================================

elif page == "Providers":
    st.title("Providers")

    claude_metrics = compute_provider_metrics(_filtered, "claude")
    deepseek_metrics = compute_provider_metrics(_filtered, "deepseek")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Claude (Anthropic)")
        render_provider_card(claude_metrics)
        if claude_metrics.get("models_used"):
            st.caption(f"Models: {', '.join(claude_metrics['models_used'])}")
        if claude_metrics.get("last_error"):
            st.error(f"Last error: {claude_metrics['last_error']}")

    with col2:
        st.subheader("DeepSeek")
        render_provider_card(deepseek_metrics)
        if deepseek_metrics.get("models_used"):
            st.caption(f"Models: {', '.join(deepseek_metrics['models_used'])}")
        if deepseek_metrics.get("last_error"):
            st.error(f"Last error: {deepseek_metrics['last_error']}")

    st.divider()
    cost_by_category(_filtered, group_key="provider", title="Cost by Provider")


# ==================================================================
# Page: Agents
# ==================================================================

elif page == "Agents":
    st.title("Agents")

    agent_groups = group_by_agent(_filtered)
    all_agent_metrics = {}
    for agent in sorted(agent_groups.keys()):
        all_agent_metrics[agent] = compute_agent_metrics(_filtered, agent)

    render_agent_summary_table(all_agent_metrics)
    st.divider()

    # Per-agent detail
    agent_list = sorted(agent_groups.keys())
    if agent_list:
        selected_agent = st.selectbox("Agent detail", agent_list)
        if selected_agent:
            metrics = all_agent_metrics.get(selected_agent, {})
            render_agent_card(metrics)

            col1, col2 = st.columns(2)
            with col1:
                if metrics.get("task_type_split"):
                    task_df = {"Task Type": list(metrics["task_type_split"].keys()),
                               "Count": list(metrics["task_type_split"].values())}
                    st.dataframe(task_df, use_container_width=True, hide_index=True)
            with col2:
                st.metric("Avg Latency", f"{metrics.get('avg_latency_ms', 0):.0f}ms")
                st.metric("Fallbacks", metrics.get("fallback_count", 0))


# ==================================================================
# Page: Costs
# ==================================================================

elif page == "Costs":
    st.title("Costs")
    st.caption("Costs are calculated from real API calls only. Dry-run calls have zero cost.")

    total_cost = _overview.get("total_cost", 0)
    real_count = _overview.get("real_count", 0)
    cache_savings = compute_cache_savings(_filtered)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Real API Cost", f"${total_cost:.4f}")
    with col2:
        st.metric("Cache Savings", f"${cache_savings.get('estimated_savings', 0):.4f}")
    with col3:
        st.metric("Avg Cost/Real Call",
                  f"${total_cost / max(real_count, 1):.6f}")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        cost_over_time(_filtered)
        cost_by_category(_filtered, group_key="provider", title="Cost by Provider (Real Calls)")
    with col2:
        cost_by_category(_filtered, group_key="agent_name", title="Cost by Agent (Real Calls)")
        cost_by_category(_filtered, group_key="task_type", title="Cost by Task Type (Real Calls)")

    st.divider()
    st.subheader("Most Expensive Calls (Real Only)")
    render_cost_table(_filtered, n=20)


# ==================================================================
# Page: Routing
# ==================================================================

elif page == "Routing":
    st.title("Routing Decisions")

    st.caption(f"Showing {len(_filtered):,} of {len(_all_entries):,} entries")
    render_routing_table(_filtered)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        latency_distribution(_filtered)
    with col2:
        task_type_distribution(_filtered)


# ==================================================================
# Page: Failures
# ==================================================================

elif page == "Failures":
    st.title("Failures")

    failures = compute_failures(_filtered)
    fail_count = len(failures)
    fail_rate = (fail_count / max(len(_filtered), 1))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Failed Calls", fail_count)
    with col2:
        st.metric("Failure Rate", f"{fail_rate:.1%}")
    with col3:
        fallback_count = sum(1 for f in failures if f.get("fallback_used"))
        st.metric("Had Fallback", fallback_count)

    st.divider()
    render_failures_table(failures)


# ==================================================================
# Page: Cache
# ==================================================================

elif page == "Cache":
    st.title("Cache")

    cache_savings = compute_cache_savings(_filtered)
    hit_count = cache_savings.get("cache_hit_count", 0)
    hit_ratio = cache_savings.get("cache_hit_ratio", 0)
    total_calls = _overview.get("total_calls", 0)
    miss_count = total_calls - hit_count

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Cache Hit Ratio", f"{hit_ratio:.1%}")
    with col2:
        st.metric("Cache Hits", hit_count)
    with col3:
        st.metric("Cache Misses", miss_count)
    with col4:
        st.metric("Est. Savings", f"${cache_savings.get('estimated_savings', 0):.4f}")

    st.divider()

    # Cache hit by task type
    hits = [e for e in _filtered if e.get("cache_hit")]
    if hits:
        st.subheader("Cached Task Types")
        tt_groups = group_by_task_type(hits)
        st.dataframe(
            {"Task Type": list(tt_groups.keys()), "Cache Hits": [len(v) for v in tt_groups.values()]},
            use_container_width=True,
            hide_index=True,
        )

    st.caption(f"Cache directory: `.cache/llm/`")
    st.caption("Note: CODE_GENERATION, CODE_PLANNING, CODE_REVIEW, DEBUGGING, RISK_REVIEW are never cached.")


# ==================================================================
# Page: Health
# ==================================================================

elif page == "Health":
    st.title("Health")
    _render_health_page()


# ==================================================================
# Health page helper
# ==================================================================

def _render_health_page() -> None:
    """Render the health check page — safe to call from empty state."""
    # Try to get a router instance for live health check
    health = _try_get_health()

    for provider_name, info in health.items():
        with st.expander(
            f"{'✅' if info.get('available') else '❌'} {provider_name.title()}",
            expanded=True,
        ):
            cols = st.columns(4)
            with cols[0]:
                st.metric("Available", "Yes" if info.get("available") else "No")
            with cols[1]:
                st.metric("Status", info.get("reason", "unknown"))
            with cols[2]:
                st.metric("Models", len(info.get("configured_models", [])))
            with cols[3]:
                circuit = info.get("circuit_state", "unknown")
                st.metric("Circuit", circuit.upper() if circuit else "N/A")

            if info.get("configured_models"):
                st.caption(f"Models: {', '.join(info['configured_models'])}")

            rate_remaining = info.get("rate_limit_remaining")
            if rate_remaining is not None:
                st.caption(f"Rate limit remaining: {rate_remaining}")

            # Show SDK/key status without values
            reason = info.get("reason", "")
            if "SDK" in reason:
                st.warning(reason)
            elif "API_KEY" in reason:
                st.info(reason)
            elif reason == "ready":
                st.success("Provider configured and ready")


def _try_get_health() -> dict:
    """Attempt to get live health from the router. Falls back to offline."""
    try:
        from src.llm import LLMRouter

        router = LLMRouter(dry_run=True)
        return get_health(router)
    except Exception:
        return get_health(None)
