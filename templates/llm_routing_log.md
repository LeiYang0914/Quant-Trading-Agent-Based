# LLM Routing Log Template

Structured log format for every routing decision. Logs are written to `reports/llm_routing/routing_log.jsonl`.

## Decision Log Entry

Logged when the router selects a provider for a task.

```json
{
  "timestamp": "2026-05-17T14:30:00.000Z",
  "task_id": "research-crypto-001-paper",
  "agent_name": "research-agent",
  "task_type": "PAPER_ANALYSIS",
  "domain": "crypto",
  "complexity": "high",
  "requires_code": false,
  "requires_long_context": true,
  "cost_sensitive": false,
  "selected_provider": "claude",
  "selected_model": "claude-sonnet-4-6",
  "reason": "task_type=PAPER_ANALYSIS -> Claude default",
  "fallback_provider": "deepseek",
  "fallback_model": "deepseek-v4-pro",
  "estimated_cost_level": "low",
  "max_tokens": 8192,
  "temperature": 0.3,
  "timeout_seconds": 120
}
```

## Response Log Entry

Logged after the provider call completes (or dry run returns).

```json
{
  "timestamp": "2026-05-17T14:30:05.000Z",
  "task_id": "research-crypto-001-paper",
  "agent_name": "research-agent",
  "task_type": "PAPER_ANALYSIS",
  "selected_provider": "claude",
  "selected_model": "claude-sonnet-4-6",
  "success": true,
  "fallback_used": false,
  "latency_ms": 4500,
  "error_summary": null
}
```

## Fallback Log Entry

Logged when the primary provider fails and a fallback is attempted.

```json
{
  "timestamp": "2026-05-17T14:30:10.000Z",
  "event": "fallback_triggered",
  "task_id": "research-crypto-001-paper",
  "agent_name": "research-agent",
  "task_type": "PAPER_ANALYSIS",
  "primary_provider": "claude",
  "primary_model": "claude-sonnet-4-6",
  "fallback_provider": "deepseek",
  "fallback_model": "deepseek-v4-pro",
  "reason": "Claude API timeout"
}
```

## Log Fields Reference

| Field | Description |
|-------|-------------|
| `timestamp` | ISO 8601 UTC |
| `task_id` | Agent-assigned unique task ID |
| `agent_name` | Name of requesting agent |
| `task_type` | TaskType enum value |
| `domain` | crypto / commodities / cross_market / system |
| `complexity` | low / medium / high |
| `selected_provider` | claude / deepseek |
| `selected_model` | Model name string |
| `reason` | Human-readable routing reason |
| `fallback_provider` | Fallback provider if primary fails |
| `estimated_cost_level` | negligible / low / medium / high |
| `success` | Whether the call succeeded |
| `fallback_used` | Whether fallback was triggered |
| `latency_ms` | Round-trip latency in milliseconds |
| `error_summary` | First 200 chars of error message |

## What Must NOT Be Logged

- API keys or secrets
- Full prompt text
- Full response content (beyond what is needed for debugging)
- Personal or identifying information
