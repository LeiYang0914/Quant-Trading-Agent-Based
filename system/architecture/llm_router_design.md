# LLM Router — Architecture Design

## Purpose

The LLM Router is an **infrastructure layer** that sits beneath all five agents. Agents do not call LLM providers directly. Instead, each agent submits a `TaskRequest` to the router, and the router decides which provider and model to use based on task type, complexity, cost sensitivity, context requirements, and safety rules.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     QUANT TRADING AI SYSTEM                      │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  ┌─────┐ │
│  │ RESEARCH │  │  REVIEW  │  │PROGRAMMER│  │  DATA  │  │RISK │ │
│  │  AGENT   │  │  AGENT   │  │  AGENT   │  │  AGENT │  │AGENT│ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬────┘  └──┬──┘ │
│       │              │              │           │          │     │
│       └──────────────┴──────────────┴───────────┴──────────┘     │
│                              │                                   │
│                     ┌────────▼────────┐                         │
│                     │   LLM ROUTER    │                         │
│                     │  (infra layer)  │                         │
│                     └───┬─────────┬───┘                         │
│                         │         │                              │
│              ┌──────────▼──┐  ┌───▼───────────┐                │
│              │   CLAUDE    │  │   DEEPSEEK    │                │
│              │  PROVIDER   │  │   PROVIDER    │                │
│              │ (Anthropic) │  │  (DeepSeek)   │                │
│              └─────────────┘  └───────────────┘                │
│                         │         │                              │
│                    ┌────▼─────────▼────┐                        │
│                    │  ROUTING LOGGER   │                        │
│                    │  (JSONL audit)    │                        │
│                    └──────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

## Provider Abstraction

All providers implement the `BaseProvider` interface:

| Method | Purpose |
|--------|---------|
| `available_models` | List of model names |
| `call(prompt, model, ...)` | Invoke the provider |
| `validate_config()` | Check API key and config |
| `estimate_cost(prompt, model, max_tokens)` | Rough cost estimate |
| `health_check()` | Provider reachability check |

Provider-specific code is isolated in `src/llm/providers/`. Adding a new provider (e.g., Grok, Gemini) means implementing `BaseProvider` and registering in `models.yaml` — no router changes needed.

## Routing Criteria

The router evaluates each request in this priority order:

1. **Explicit preference** — `preferred_provider` field set by agent
2. **Agent-level preference** — Review, Risk, Programmer agents prefer Claude
3. **Task-type defaults** — `_CLAUDE_DEFAULT_TASKS` vs `_DEEPSEEK_DEFAULT_TASKS`
4. **Dynamic overrides** — code requirement, complexity, context length, cost sensitivity
5. **Safety default** — ambiguous tasks route to Claude

## Default Routing Rules

### Claude (high-capability reasoning)
- SYSTEM_ARCHITECTURE
- RESEARCH_REASONING
- PAPER_ANALYSIS
- ALPHA_IDEA_GENERATION
- CODE_PLANNING
- CODE_GENERATION
- CODE_REVIEW
- DEBUGGING
- High complexity tasks
- Long context tasks
- Risk-critical reviews

### DeepSeek (cost-efficient throughput)
- SUMMARIZATION
- TEXT_CLEANUP
- WEB_SOURCE_SCREENING
- DATA_GRABBING
- GIT_ACTIVITY_SUMMARY
- CLASSIFICATION
- MEMORY_UPDATE
- Low complexity tasks with high cost sensitivity

## Per-Agent Usage

| Agent | Claude For | DeepSeek For |
|-------|-----------|--------------|
| **Research** | Final reasoning, memo synthesis, paper analysis, discovery notes | Source pre-screening, formatting, lightweight summaries |
| **Review** | All gate decisions | (none by default) |
| **Programmer** | Coding, debugging, code review, test generation | Backtest report formatting |
| **Data** | Complex architecture, data quality analysis, API adapter generation | Simple data fetching, formatting |
| **Risk** | Risk review, position sizing, kill switches, all approval decisions | (none by default) |

## Fallback Behavior

| Primary | Falls Back To | Conditions |
|---------|--------------|------------|
| Claude | DeepSeek | Only for non-code tasks; CODE_GENERATION, CODE_PLANNING, CODE_REVIEW, DEBUGGING blocked |
| DeepSeek | Claude | Always allowed |

Fallback is triggered only when:
- Provider call returns `success: false`
- `fallback_allowed` is `true` on the request
- The task type is not in `_NO_CODE_FALLBACK_TASKS` (for Claude→DeepSeek)

## Logging

Every routing decision is logged to `reports/llm_routing/routing_log.jsonl`:

- Decision log: provider, model, reason, task metadata
- Response log: success, latency, fallback usage
- Fallback log: primary failure reason, fallback provider

No API keys or full prompts are logged.

## Cost Control

- Cost estimates are computed per-call and logged with each decision
- DeepSeek is used for cost-insensitive throughput tasks
- High-cost models are reserved for truly complex reasoning
- Cost estimates are rough (token-based) and non-billing

## Dry Run Mode

The router supports `dry_run=True` (default) for testing without real API calls. In dry run mode:
- Full routing logic executes
- Decisions are logged
- Provider skeletons return placeholder responses
- No real API keys are consumed
- Cache is disabled to prevent pollution with placeholder responses

## Response Caching

File-based JSON index cache (`src/llm/utils/cache.py`) to reduce duplicate API calls:

| Feature | Detail |
|---------|--------|
| **Key** | SHA-256 hash of provider + model + task_type + prompt |
| **Storage** | JSON index file at `.cache/llm/cache_index.json` |
| **TTL** | 86400 seconds (24 hours) by default |
| **Eviction** | LRU by creation time when exceeding `max_entries` (10000) |
| **Exclusions** | CODE_GENERATION, CODE_PLANNING, CODE_REVIEW, DEBUGGING, RISK_REVIEW never cached |
| **Override** | `metadata.no_cache = true` disables caching per-request |
| **Status** | Responsive — disablable via `enabled=False` in config |

## Rate Limiting

Sliding-window rate limiter (`src/llm/utils/rate_limiter.py`) per provider:

- Configurable `requests_per_minute` per provider in `models.yaml`
- Per-provider enable/disable toggle
- `acquire()` returns `False` when limit exceeded
- `remaining()` returns current window capacity
- `reset()` clears all counters

## Circuit Breaker

Failure-protection circuit breaker (`src/llm/utils/circuit_breaker.py`) per provider:

```
CLOSED ──(N failures)──▶ OPEN ──(cooldown elapsed)──▶ HALF_OPEN
                                                             │
                                              ┌─(success)────┘
                                              │
                                              ▼
                                           CLOSED
                                              ▲
                                              └─(failure)────HALF_OPEN
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `failure_threshold` | 3 | Consecutive failures to open circuit |
| `cooldown_seconds` | 300 | Time before half-open probe |
| `half_open_max_requests` | 1 | Probe requests in half-open state |

When a provider's circuit is OPEN, the router skips it and falls back to the alternative provider.

## Usage & Cost Tracking

Usage tracker (`src/llm/utils/usage_tracker.py`) with JSONL-based logging:

- Logs every call to `logs/llm/usage.jsonl` with task_id, agent, task_type, provider, model, cost, latency, cache_hit, fallback_used
- Aggregation methods: `get_cost_by_agent()`, `get_cost_by_provider()`, `get_cost_by_task_type()`
- Ratios: `get_cache_hit_ratio()`, `get_fallback_ratio()`, `get_success_rate()`
- Available via `router.get_usage_summary()` as a structured dict

## Router Convenience API

`router.ask()` auto-classifies and routes in one call:

```python
response = router.ask(
    prompt="Summarize this article about crypto markets.",
    agent_name="research-agent",
    # Optional overrides:
    task_type=TaskType.PAPER_ANALYSIS,
    complexity=Complexity.HIGH,
    domain=Domain.CRYPTO,
    requires_code=False,
    cost_sensitive=False,
    preferred_provider=None,
    fallback_allowed=True,
)
```

## Health Check API

`router.health_check()` returns a structured dict per provider:
- `available` — whether the provider is reachable
- `reason` — human-readable status
- `configured_models` — list of available models
- `circuit_state` — CLOSED / OPEN / HALF_OPEN
- `rate_limit_remaining` — remaining requests in current window

## CLI Tool

`scripts/llm_router_cli.py` provides command-line access:

```
python scripts/llm_router_cli.py --dry-run --agent research-agent --task SUMMARIZATION --prompt "Summarize this"
python scripts/llm_router_cli.py --health-check
python scripts/llm_router_cli.py --usage-summary
python scripts/llm_router_cli.py --clear-cache
python scripts/llm_router_cli.py --clear-usage
python scripts/llm_router_cli.py --reset-circuits
```

## Future Improvements

1. **Streaming support** — SSE streaming for long responses
2. **Additional providers** — Gemini, Grok, Mistral, Llama (local)
3. **Prompt versioning** — Track prompt templates and their performance
4. **Model A/B testing** — Route a percentage of traffic to alternative models for evaluation
5. **Cost tracking dashboard** — Visual dashboard for cost analytics
6. **Distributed rate limiting** — Redis-backed rate limiter for multi-process deployments
