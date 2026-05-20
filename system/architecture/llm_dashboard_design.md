# LLM Router Dashboard — Architecture Design

## Purpose

The LLM Router Dashboard provides browser-accessible observability into router operations: usage, costs, provider health, failures, cache performance, and routing decisions. It reads from existing log files and health checks — no separate data pipeline needed.

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        STREAMLIT BROWSER UI                          │
│                                                                      │
│  ┌─────────┐ ┌──────────┐ ┌────────┐ ┌───────┐ ┌──────┐ ┌────────┐  │
│  │Overview │ │Providers │ │ Agents │ │ Costs │ │Routing│ │Failures│  │
│  └────┬────┘ └────┬─────┘ └───┬────┘ └───┬───┘ └───┬──┘ └───┬────┘  │
│       └───────────┴───────────┴──────────┴─────────┴───────┘         │
│                                 │                                     │
│  ┌──────────────────────────────▼──────────────────────────────────┐ │
│  │                    DASHBOARD BACKEND                             │ │
│  │                                                                  │ │
│  │  ┌────────────┐ ┌────────────────┐ ┌──────────────────────┐     │ │
│  │  │ log_reader │ │metrics_service │ │    aggregation       │     │ │
│  │  │            │ │                │ │                      │     │ │
│  │  │ read JSONL │ │ compute KPIs   │ │ group_by, buckets,   │     │ │
│  │  │ filter by  │ │ per provider,  │ │ top-N, time series   │     │ │
│  │  │ time range │ │ agent, cache   │ │                      │     │ │
│  │  └────────────┘ └────────────────┘ └──────────────────────┘     │ │
│  │                                                                  │ │
│  │  ┌──────────────────────────────────────────────────────────┐   │ │
│  │  │                   health_service                         │   │ │
│  │  │  calls router.health_check() → sanitizes → returns safe  │   │ │
│  │  │  dict. NEVER exposes API keys. Falls back to offline.    │   │ │
│  │  └──────────────────────────────────────────────────────────┘   │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                 │                                     │
│  ┌──────────────────────────────▼──────────────────────────────────┐ │
│  │                       DATA SOURCES                              │ │
│  │  logs/llm/usage.jsonl          — usage tracking (JSONL)         │ │
│  │  reports/llm_routing/routing_log.jsonl — routing audit (JSONL) │ │
│  │  src/llm/router.health_check() — live provider health           │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

## Layer Separation

| Layer | Location | Responsibility |
|-------|----------|----------------|
| **App** | `src/dashboard/app.py` | Page routing, layout, sidebar, empty states |
| **Components** | `src/dashboard/components/` | Reusable UI: metric cards, charts, tables, filters |
| **Backend** | `src/dashboard/backend/` | Pure functions: log reading, metrics, aggregation, health |

Components never read files or call the router directly. Backend functions are pure — they accept data, return values, with no Streamlit imports.

## Dashboard Pages

| Page | Purpose | Key Metrics |
|------|---------|-------------|
| **Overview** | Top-level KPIs | Total calls, cost, success rate, cache rate, latency, provider split |
| **Providers** | Per-provider breakdown | Calls, success rate, cost, models used, last error |
| **Agents** | Per-agent breakdown | Calls, cost, latency, provider split, task type mix |
| **Costs** | Cost analysis | Total cost, cache savings, avg cost/call, top expensive calls |
| **Routing** | Routing decision log | Full table with filters, latency distribution |
| **Failures** | Error analysis | Failure count, rate, fallback rate, error summaries |
| **Cache** | Cache performance | Hit ratio, hits, misses, estimated savings, cached task types |
| **Health** | Live provider status | Availability, circuit state, models, rate limits |

## Data Flow

1. `app.py` calls `log_reader.read_usage_log()` to load entries
2. `filters.render_global_filters()` renders sidebar controls and returns filter criteria
3. `filters.apply_filters()` filters entries
4. Backend functions compute metrics from filtered entries
5. Component functions render metric cards, charts, and tables
6. Health page calls `health_service.get_health(router)` for live status

## Empty State Handling

When no real log file exists:
- All backend functions return sensible defaults (0 counts, empty lists)
- `app.py` shows an info message directing users to run real or dry-run router CLI commands
- Health page remains functional (offline mode)

## Real vs Dry-Run Distinction

Every entry in `logs/llm/usage.jsonl` carries a `dry_run` boolean field:
- **Real calls** (`dry_run: false`): actual API calls, contribute to cost calculations, may have real token counts
- **Dry-run calls** (`dry_run: true`): no API keys required, zero latency, zero cost, used for testing routing logic

The dashboard:
- Shows real + dry-run total in the call count
- Calculates costs only from real calls
- Provides a "Call Type" filter (All / Real / Dry-Run)
- Displays "Real" or "Dry-Run" in routing and cost tables

## Security

- **API keys never displayed.** `health_service._sanitize()` strips `api_key` and `_api_key` fields
- **Key-like strings redacted.** `_redact_keys()` replaces `sk-...` patterns with `[REDACTED]`
- **Config redaction.** `configs/dashboard/dashboard.yaml` lists `redact_fields` for safety
- **Logs never read .env.** The dashboard only reads JSONL log files and health check output

## Chart Strategy

Charts use Plotly via lazy import — the dashboard works without Plotly installed (shows info message instead of chart).

| Chart | Type | Bucket |
|-------|------|--------|
| Requests over time | Line | 60-min buckets |
| Cost over time | Bar | Daily buckets |
| Provider distribution | Pie | — |
| Task type distribution | Horizontal bar | — |
| Agent distribution | Horizontal bar | — |
| Latency distribution | Histogram | — |
| Cost by category | Horizontal bar | Grouped by provider/agent/task_type |

## Configuration

`configs/dashboard/dashboard.yaml` controls:
- Port, host, log file paths
- Auto-refresh (disabled by default)
- Page visibility toggles
- Chart bucket settings
- Field redaction list
