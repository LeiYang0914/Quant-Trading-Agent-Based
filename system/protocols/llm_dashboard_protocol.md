# LLM Router Dashboard — Protocol

## Purpose

This document defines how the LLM Router Dashboard is launched, configured, and used. The dashboard is a read-only observability tool — it never modifies logs, routing rules, or provider state.

## Launch

### Primary (via script)

```bash
python scripts/run_dashboard.py
python scripts/run_dashboard.py --port 8502
python scripts/run_dashboard.py --no-browser
```

The script:
1. Locates `src/dashboard/app.py` relative to project root
2. Invokes `streamlit run` with port and host arguments
3. Opens the default browser unless `--no-browser` is set

### Direct (via streamlit)

```bash
streamlit run src/dashboard/app.py
```

### Populating Logs

The dashboard reads only real usage logs. To populate logs, run the LLM Router CLI:

```bash
# Dry-run call (no API key needed):
python scripts/llm_router_cli.py --dry-run --agent research-agent \
  --task research_reasoning --prompt "Analyze market structure"

# Real API call (requires API keys configured in .env):
python scripts/llm_router_cli.py --real --agent data-agent \
  --task summarization --prompt "Summarize this data"
```

All calls — both real and dry-run — are logged to `logs/llm/usage.jsonl` with a `dry_run` flag. The dashboard distinguishes them for cost calculation and filtering.

## Navigation

The dashboard sidebar provides radio-button navigation across 8 pages. All pages share:
- Global filter controls (time range, provider, agent, task type, status, cache, fallback, call type)
- A "Refresh Data" button that triggers `st.rerun()`
- Log file path and entry count display

## Filter Protocol

Filters are applied in this order:
1. Time range (since/until)
2. Provider
3. Agent
4. Task type
5. Success status
6. Cache hit status
7. Fallback status
8. Call type (All / Real Calls Only / Dry-Run Calls Only)
9. Entry limit (last N entries)

Filters are additive — all criteria must match. "All" options pass through as `None` (no filter).

The Call Type filter uses the `dry_run` boolean field:
- **All Calls**: Shows both real and dry-run (no filter)
- **Real Calls Only**: Shows only entries with `dry_run: false`
- **Dry-Run Calls Only**: Shows only entries with `dry_run: true`

### Real vs Dry-Run Distinction

The usage log records a `dry_run` boolean field on every entry. The dashboard uses this to:
- **Cost calculation**: Only real calls contribute to cost totals
- **Cache savings**: Only computed from real calls
- **Filters**: Users can view all, real-only, or dry-run-only calls
- **Tables**: A "Type" column shows "Real" or "Dry-Run"

## Metrics Computation

### Overview
- `total_calls`, `real_count`, `dry_run_count`, `total_cost` (real only), `real_cost`, `success_rate`, `cache_hit_ratio`, `fallback_ratio`, `avg_latency_ms`, `claude_count`, `deepseek_count`

### Provider Metrics
- `total_calls`, `real_count`, `dry_run_count`, `success_rate`, `avg_latency_ms`, `total_cost` (real only), `models_used`, `last_error`

### Agent Metrics
- `total_calls`, `real_count`, `dry_run_count`, `total_cost` (real only), `avg_latency_ms`, `success_count`, `failure_count`, `fallback_count`, `claude_count`, `deepseek_count`, `task_type_split`

### Failures
- Extracted entries with: `timestamp`, `task_id`, `agent_name`, `task_type`, `provider`, `model`, `error_summary`, `fallback_used`, `latency_ms`

### Cache Savings
- `cache_hit_count` (real only), `estimated_savings` (real only), `cache_hit_ratio` (real only)

## Aggregation Protocol

| Function | Output |
|----------|--------|
| `group_by_provider` | `{provider: [entries]}` |
| `group_by_agent` | `{agent_name: [entries]}` |
| `group_by_task_type` | `{task_type: [entries]}` |
| `group_by_model` | `{model: [entries]}` |
| `group_by_success` | `{success: [...], failure: [...]}` |
| `group_by_cache_hit` | `{hit: [...], miss: [...]}` |
| `group_by_fallback` | `{fallback: [...], no_fallback: [...]}` |
| `group_by_dry_run` | `{real: [...], dry_run: [...]}` |
| `time_buckets(entries, minutes)` | `{iso_ts: {count, total_cost, avg_latency}}` |
| `daily_buckets(entries)` | Same as time_buckets with 1440-min buckets |
| `top_expensive(entries, n)` | Top-N entries by estimated_cost |
| `top_slowest(entries, n)` | Top-N entries by latency_ms |

## Health Check Protocol

1. Dashboard calls `health_service.get_health(router)`
2. If router is `None` or raises an exception → return offline status
3. Otherwise, call `router.health_check()` and sanitize each provider's result
4. Sanitization strips `api_key` and `_api_key` fields
5. Key-like strings (`sk-...`) are regex-replaced with `[REDACTED]`

**Never expose API keys in the dashboard UI.** The health page shows availability, circuit state, configured model names, and rate limit remaining — never raw credentials.

## Security Rules

1. **No key exposure.** Health service always redacts. Log reader only reads JSONL (never .env).
2. **Read-only.** The dashboard never writes logs, modifies configs, or changes router state.
3. **Config-driven redaction.** `configs/dashboard/dashboard.yaml` `redact_fields` list provides an extra safety net.
4. **Offline fallback.** If the router is unavailable, health shows offline status rather than crashing.
5. **No authentication.** The dashboard runs on localhost by default — it assumes a trusted local environment.

## Dependency Protocol

- **Streamlit** — required. Dashboard fails with a clear error message if not installed.
- **Plotly** — optional. Charts show info message if Plotly is missing; all other content renders.
- **Pandas** — required for dataframes. Streamlit includes pandas by default.
- **LLM Router** — optional for live health. Dashboard uses offline health if router import fails.

## Adding a New Page

1. Add the page name to the `Navigation` radio in `app.py`
2. Create the page block in the `if/elif` chain
3. Use existing backend functions for metrics; add new ones to `metrics_service.py` if needed
4. Add any new charts to `components/charts.py`
5. Update `configs/dashboard/dashboard.yaml` page visibility toggle
