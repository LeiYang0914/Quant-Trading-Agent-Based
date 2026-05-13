---
title: ""
type: backtest_request
status: pending
created: {{date}}
updated: {{date}}
tags:
  - backtest_request
  - ""
source_alpha: ""
requested_by: Quant Research Agent
assigned_to: Quant Trading Programmer Agent
priority: medium
---

# Backtest Request: {{title}}

## Source Alpha Idea
- [[Alpha Idea Name]]
- [[Strategy Hypothesis Name]]

## What to Test
[Plain English description of what the backtest should evaluate.]

## Signal Specification (Plain English)
### Entry Logic
[Describe entry logic in plain English. No code. May use high-level pseudocode.]

### Exit Logic
[Describe exit logic in plain English. No code.]

### Position Sizing
[Describe position sizing logic in plain English.]

### Filters
[Describe any filters.]

## Universe & Data
| Parameter | Value |
|-----------|-------|
| Assets | |
| Venues | |
| Data frequency | |
| Start date | |
| End date | |
| Data source | [[Data Source Note]] |

## Backtest Design
| Parameter | Value |
|-----------|-------|
| In-sample period | |
| Out-of-sample period | |
| Walk-forward design | |
| Benchmark | |
| Rebalance frequency | |
| Holding period | |
| Transaction cost model | [[Transaction Cost]] |
| Slippage model | [[Slippage]] |

## Expected Metrics to Report
- [ ] Equity curve
- [ ] Sharpe ratio
- [ ] Max drawdown
- [ ] Win rate
- [ ] Profit factor
- [ ] Turnover
- [ ] Parameter sensitivity heatmap
- [ ] Sub-period performance breakdown

## Robustness Checks Required
- [ ] Parameter sweep
- [ ] Sub-period analysis
- [ ] Out-of-sample test
- [ ] Alternative universe test
- [ ] Transaction cost stress test

## What NOT to Test
- [Anything explicitly excluded from scope.]

## Failure Mode Awareness
[Specific failure modes to watch for, from [[Risk Note]]]

## Acceptance Criteria
[What results would make this alpha worth pursuing further.]

## Rejection Criteria
[What results would lead to rejecting this alpha.]

## Related
- [[Alpha Idea Name]]
- [[Risk Note Name]]

---

*Requested by: Quant Research Agent*
*To be implemented by: Quant Trading Programmer Agent*
*This is a research specification only. No trading code.*
