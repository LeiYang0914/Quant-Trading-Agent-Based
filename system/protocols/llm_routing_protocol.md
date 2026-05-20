# LLM Routing Protocol

How agents request LLM calls through the routing infrastructure layer.

## Core Principle

**Agents do not call LLM providers directly.** Every LLM call goes through the `LLMRouter`. The router selects the provider, model, and handles fallback, caching, rate limiting, and circuit breaking.

## How Agents Request LLM Calls

### Option 1: `router.route()` — explicit control

An agent constructs a `TaskRequest` and passes it to the router:

```python
from src.llm import LLMRouter, TaskRequest, TaskType, Domain, Complexity

request = TaskRequest(
    task_id="research-2026-05-17-001",
    agent_name="research-agent",
    task_type=TaskType.PAPER_ANALYSIS,
    prompt="Analyze the methodology of this paper...",
    domain=Domain.CRYPTO,
    complexity=Complexity.HIGH,
    requires_code=False,
    requires_long_context=True,
    cost_sensitive=False,
    timeout_seconds=120,
)

router = LLMRouter(dry_run=True)
response = router.route(request)
```

### Option 2: `router.ask()` — convenience with auto-classification

For simpler cases, use `router.ask()` which auto-classifies the task type:

```python
response = router.ask(
    prompt="Summarize this article about crypto markets.",
    agent_name="research-agent",
    # Optional overrides:
    task_type=TaskType.SUMMARIZATION,
    complexity=Complexity.LOW,
    domain=Domain.CRYPTO,
    requires_code=False,
    cost_sensitive=True,
    preferred_provider=None,
    fallback_allowed=True,
    metadata={"no_cache": False},
)
```

## Required Task Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `task_id` | str | Yes | Unique ID for this task |
| `agent_name` | str | Yes | Name of the requesting agent |
| `task_type` | TaskType | Yes | Task category (enum) |
| `prompt` | str | Yes | The prompt text |
| `domain` | Domain | No (default: system) | Market domain |
| `complexity` | Complexity | No (default: medium) | Task complexity |
| `requires_code` | bool | No (default: false) | Whether code is produced |
| `requires_long_context` | bool | No (default: false) | Long context needed |
| `cost_sensitive` | bool | No (default: false) | Cost is a concern |
| `timeout_seconds` | int | No (default: 120) | Max wait time |
| `preferred_provider` | ProviderName | No | Override routing |
| `fallback_allowed` | bool | No (default: true) | Allow fallback |
| `metadata` | dict | No | Arbitrary metadata |

## Routing Decision Process

```
TaskRequest received
    │
    ▼
preferred_provider set? ──yes──▶ Use that provider
    │ no
    ▼
Agent in claude_preferred_agents? ──yes──▶ Claude
    │ no
    ▼
TaskType in Claude defaults? ──yes──▶ Claude
    │ no
    ▼
TaskType in DeepSeek defaults? ──yes──▶ DeepSeek
    │ no
    ▼
Dynamic overrides:
  requires_code? ──yes──▶ Claude
  complexity=high? ──yes──▶ Claude
  requires_long_context? ──yes──▶ Claude
  cost_sensitive + low? ──yes──▶ DeepSeek
    │
    ▼
Default ──▶ Claude (safety)
```

## When Claude Must Be Used

- Any task with `requires_code = true`
- Any task with `complexity = high`
- Any task with `requires_long_context = true`
- All `CODE_GENERATION`, `CODE_PLANNING`, `CODE_REVIEW`, `DEBUGGING`
- All `SYSTEM_ARCHITECTURE`, `RESEARCH_REASONING`, `PAPER_ANALYSIS`, `ALPHA_IDEA_GENERATION`
- All Review Agent and Risk Agent tasks
- All Programmer Agent code tasks
- Research Agent final memo synthesis and paper analysis

## When DeepSeek Should Be Used

- `SUMMARIZATION`, `TEXT_CLEANUP`, `CLASSIFICATION`
- `WEB_SOURCE_SCREENING`, `DATA_GRABBING`
- `GIT_ACTIVITY_SUMMARY`, `MEMORY_UPDATE`
- Cost-sensitive low-complexity tasks
- Research Agent source pre-screening
- Data Agent simple data retrieval and formatting

## Fallback Rules

1. Claude → DeepSeek: Allowed **only** for non-code tasks. Blocked for `CODE_GENERATION`, `CODE_PLANNING`, `CODE_REVIEW`, `DEBUGGING`.
2. DeepSeek → Claude: Always allowed.
3. Fallback is skipped if `fallback_allowed = false` on the request.
4. Risk Agent critical decisions: fallback to low-cost models is never allowed by default.

### Forbidden Fallback (Hard Blocks)

Configured in `routing_rules.yaml` under `forbidden_fallback`:

- **no_fallback_tasks**: CODE_GENERATION, CODE_PLANNING, CODE_REVIEW, DEBUGGING, RISK_REVIEW
- **no_fallback_if_code_required**: Any task with `requires_code=true`
- **risk_never_low_cost**: Risk review never falls back to low-cost models
- **no_fallback_agents**: Review Agent and Risk Agent tasks never fall back

These rules are enforced at the router level and cannot be bypassed by metadata overrides.

## Response Caching

The router caches responses to reduce duplicate API calls:

- **Cache key:** SHA-256 hash of provider + model + task_type + prompt
- **Never cached:** CODE_GENERATION, CODE_PLANNING, CODE_REVIEW, DEBUGGING, RISK_REVIEW
- **Opt-out:** Set `metadata.no_cache = true` on the TaskRequest
- **Disabled during dry_run:** Cache is automatically disabled to prevent pollution
- **TTL:** 24 hours by default (configurable in `models.yaml`)
- **Storage:** `.cache/llm/cache_index.json`

## Rate Limiting

Per-provider sliding-window rate limiting protects against API quota exhaustion:

- `router.rate_limiter.acquire("claude")` — attempt to claim a request slot
- Returns `False` when the per-minute limit is exceeded
- The router skips rate-limited providers during routing
- Limits configured per provider in `models.yaml` under `rate_limits`

## Circuit Breaker

Automatic provider disabling after consecutive failures:

- **CLOSED → OPEN:** After `failure_threshold` (default 3) consecutive failures
- **OPEN → HALF_OPEN:** After `cooldown_seconds` (default 300s) with one probe request
- **HALF_OPEN → CLOSED:** Probe succeeds; **HALF_OPEN → OPEN:** Probe fails
- When a provider's circuit is OPEN, the router falls back to the alternative
- State is reported in `router.health_check()`

## Health Check & Monitoring

`router.health_check()` returns per-provider status:

```python
{
    "claude": {
        "available": True,
        "reason": "SDK present, API key configured",
        "configured_models": ["claude-sonnet-4-6", ...],
        "circuit_state": "closed",
        "rate_limit_remaining": 50,
    },
    "deepseek": { ... },
}
```

## Usage Summary

`router.get_usage_summary()` returns aggregated call stats:

```python
{
    "total_calls": 150,
    "total_cost": 0.42,
    "cost_by_agent": {"research-agent": 0.15, ...},
    "cost_by_provider": {"claude": 0.30, "deepseek": 0.12},
    "cost_by_task_type": {"SUMMARIZATION": 0.05, ...},
    "cache_hit_ratio": 0.23,
    "fallback_ratio": 0.03,
    "success_rate": 0.98,
    "recent_calls": [...],
}
```

## CLI Access

The router can be accessed from the command line:

```bash
python scripts/llm_router_cli.py --dry-run --agent research-agent --task SUMMARIZATION --prompt "Summarize this"
python scripts/llm_router_cli.py --health-check
python scripts/llm_router_cli.py --usage-summary
python scripts/llm_router_cli.py --clear-cache
python scripts/llm_router_cli.py --clear-usage
python scripts/llm_router_cli.py --reset-circuits
```

## Logging Rules

- Every routing decision logged to `reports/llm_routing/routing_log.jsonl`
- Every call logged to `logs/llm/usage.jsonl` with cost and performance data
- Log includes: timestamp, task_id, agent, task_type, provider, model, reason
- Every response logged with success/failure, latency, cache_hit, fallback usage
- Every fallback event logged with primary failure reason
- **Never log:** API keys, full prompt text, or secrets

## Forbidden Behavior

The router MUST NOT:

- Make trading decisions or modify trading logic
- Override Risk Agent decisions
- Expose API keys in logs, responses, or config files
- Silently switch models for risk-critical tasks
- Route risk-critical approvals to low-cost models by default
- Call live trading APIs
- Bypass the five-agent architecture
- Auto-approve or reject anything on behalf of an agent
