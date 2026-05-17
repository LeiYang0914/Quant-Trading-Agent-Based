# LLM Task Request Template

Template for agents constructing a task request for the LLM Router.

## Required Fields

| Field | Example | Notes |
|-------|---------|-------|
| **task_id** | `research-crypto-001-paper-analysis` | Unique per request; use agent-domain-id-activity format |
| **agent_name** | `research-agent` | Must match registered agent name |
| **task_type** | `PAPER_ANALYSIS` | From TaskType enum |
| **prompt** | `Analyze the following paper...` | Full prompt text |

## Recommended Fields

| Field | Example | Notes |
|-------|---------|-------|
| **domain** | `crypto` | crypto / commodities / cross_market / system |
| **complexity** | `high` | low / medium / high |
| **requires_code** | `false` | true if code is generated |
| **requires_long_context** | `true` | true for papers, long docs |
| **cost_sensitive** | `false` | true if cost matters |
| **timeout_seconds** | `120` | longer for complex tasks |
| **fallback_allowed** | `true` | false for risk-critical tasks |

## Example Requests

### Research Agent — Paper Analysis

```yaml
task_id: "research-crypto-001-paper"
agent_name: "research-agent"
task_type: "PAPER_ANALYSIS"
prompt: "Analyze the methodology and findings of this paper..."
domain: "crypto"
complexity: "high"
requires_code: false
requires_long_context: true
cost_sensitive: false
timeout_seconds: 120
fallback_allowed: true
```

### Programmer Agent — Code Generation

```yaml
task_id: "programmer-backtest-003-implement"
agent_name: "programmer-agent"
task_type: "CODE_GENERATION"
prompt: "Implement a backtest for the funding rate carry signal..."
domain: "crypto"
complexity: "high"
requires_code: true
requires_long_context: false
cost_sensitive: false
timeout_seconds: 180
fallback_allowed: false
```

### Data Agent — Simple Fetch

```yaml
task_id: "data-crypto-btc-ohlcv"
agent_name: "data-agent"
task_type: "DATA_GRABBING"
prompt: "Fetch BTC/USDT daily OHLCV for the past 90 days..."
domain: "crypto"
complexity: "low"
requires_code: false
requires_long_context: false
cost_sensitive: true
timeout_seconds: 60
fallback_allowed: true
```

### Risk Agent — Review

```yaml
task_id: "risk-review-strategy-005"
agent_name: "risk-agent"
task_type: "RESEARCH_REASONING"
prompt: "Review the risk profile of strategy CRYPTO-005..."
domain: "crypto"
complexity: "high"
requires_code: false
requires_long_context: true
cost_sensitive: false
timeout_seconds: 120
fallback_allowed: false
```
