---
title: ""
type: programmer_handoff
status: pending
created: {{date}}
updated: {{date}}
tags:
  - programmer_handoff
  - ""
source_alpha: ""
research_owner: Quant Research Agent
implementation_owner: Quant Trading Programmer Agent
handoff_version: 1
---

# Programmer Handoff: {{title}}

## Handoff Summary
- **Alpha idea:** [[Alpha Idea Name]]
- **Research memo:** [Link to research memo in project]
- **Backtest request:** [[Backtest Request Name]]
- **Date handed off:** {{date}}
- **Handoff version:** 1

## Alpha Summary
[One-paragraph summary of the alpha idea, mechanism, and expected behavior. Written by Research Agent.]

## Market & Universe
| Parameter | Value |
|-----------|-------|
| Market | |
| Assets | |
| Venues | |
| Timeframe | |

## Signal Specification (Plain English)
### Entry Logic
[Describe entry logic in plain English. Structural description, NOT code.]

### Exit Logic
[Describe exit logic in plain English. Structural description, NOT code.]

### Position Sizing
[Describe position sizing logic in plain English.]

### Risk Management
[Describe risk management logic in plain English.]

## Data Requirements
| Dataset | Fields | Frequency | Vendor | Access Method |
|---------|--------|-----------|--------|---------------|
| | | | | |

## Preprocessing Description
1. [Step 1 — describe in plain English, no code]
2. [Step 2 — describe in plain English, no code]

## Backtest Scope
| Parameter | Value |
|-----------|-------|
| In-sample | |
| Out-of-sample | |
| Benchmark | |
| Rebalance frequency | |
| Transaction cost assumption | |

## Known Risk Factors
1. [Risk 1]
2. [Risk 2]

## Failure Modes (Researcher's Notes)
| Failure Mode | Severity | What to Watch |
|-------------|----------|---------------|
| | | |

## Assumptions
1. [Assumption 1]
2. [Assumption 2]

## Expected Edge (Qualitative)
[Qualitative description of expected edge. No performance claims before backtesting.]

## What the Programmer Should Implement
- [ ] [Implementation task 1]
- [ ] [Implementation task 2]

## What the Programmer Should NOT Implement
- [ ] [Excluded scope 1]
- [ ] [Excluded scope 2]

## Open Research Questions
1. [Question for future research]
2. [Question for future research]

## Constraints
- **Do not** implement live trading
- **Do not** connect to broker APIs
- **Do not** place orders
- This is a research backtest only
- Return results to Research Agent for interpretation

## Acceptance Criteria
[What backtest results would indicate the alpha is worth further investigation.]

## Rejection Criteria
[What backtest results would indicate the alpha should be rejected or deprecated.]

## Related Documents
- [[Alpha Idea Name]]
- [[Strategy Hypothesis Name]]
- [[Backtest Request Name]]
- [[Risk Note Name]]
- [[Paper Note Name]]

---

*Handoff prepared by: Quant Research Agent*
*For: Quant Trading Programmer Agent*
*Implementation responsibility: Quant Trading Programmer Agent*
*Research responsibility: Quant Research Agent*
