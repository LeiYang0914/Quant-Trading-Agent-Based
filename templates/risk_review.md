# Risk Review — `{strategy_name}`

**Risk Agent**
**Date:** `{date}`
**Source Backtest Report:** `reports/backtests/{report_file}.md`
**Source Handoff:** `handoffs/completed/{handoff_file}.md`

---

## Decision

**`{APPROVED | REJECTED | MODIFICATIONS_REQUIRED}`**

## Risk Metrics

| Metric | Value | Threshold | Pass? |
|--------|-------|-----------|-------|
| Annualized return | `{X%}` | `{min}` | `{ }` |
| Annualized volatility | `{X%}` | `{max}` | `{ }` |
| Sharpe ratio | `{X.XX}` | `{min}` | `{ }` |
| Calmar ratio | `{X.XX}` | `{min}` | `{ }` |
| Max drawdown | `{-X%}` | `{max}` | `{ }` |
| Max drawdown duration | `{N} days` | `{max}` | `{ }` |
| VaR 95% (daily) | `{-X%}` | `{max}` | `{ }` |
| VaR 99% (daily) | `{-X%}` | `{max}` | `{ }` |
| CVaR 95% (daily) | `{-X%}` | `{max}` | `{ }` |
| Worst 1-day return | `{-X%}` | — | |
| Worst 5-day return | `{-X%}` | — | |
| Avg daily turnover | `{X%}` | `{max}` | `{ }` |
| Capacity estimate | `{ $X M}` | `{min}` | `{ }` |

---

## Correlation with Existing Strategies

| Existing Strategy | Correlation | Concern? |
|-------------------|-------------|----------|
| `{name}` | `{X.XX}` | `{yes/no}` |

---

## Position Sizing Rules

```
{Formulaic position sizing rules in plain English or structural pseudocode}
```

---

## Risk Limits

| Limit | Value |
|-------|-------|
| Max position size (% of portfolio) | `{X%}` |
| Max leverage | `{X.Xx}` |
| Max gross exposure | `{X%}` |
| Max net exposure | `{X%}` |
| Max sector concentration | `{X%}` |
| Max single-asset concentration | `{X%}` |

---

## Kill Switches

| Trigger | Condition | Action |
|---------|-----------|--------|
| Drawdown limit | `{e.g., -15% from peak}` | `{halt trading, liquidate}` |
| Volatility spike | `{e.g., 3x realized vol vs. forecast}` | `{reduce position by 50%}` |
| Correlation breakdown | `{e.g., rolling corr < 0.3 with benchmark}` | `{pause strategy}` |
| Liquidity drop | `{e.g., bid/ask > 5x normal}` | `{halt trading}` |

---

## Rejection / Modification Reasons

`{If rejected: specific reasons with supporting evidence}`

`{If modifications required: numbered, specific requests to Programmer Agent}`

---

## Risk Agent Notes

`{Free-form risk assessment, concerns, observations}`
