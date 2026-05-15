# Handoff Protocol

How agents hand off work to each other in the Quant Trading AI System.

## Handoff Types

### 1. Research → Review: Alpha Idea Proposal

**From:** Research Agent
**To:** Review Agent
**Trigger:** Research memo is complete, idea note is written
**Artifact:** Alpha idea note in `research/ideas/proposed/`

**Required fields:**
- Idea title and ID
- One-paragraph mechanism summary
- Falsifiable hypothesis
- Required data sources (with availability confirmed by Data Agent)
- Key failure modes (top 3)
- Link to full research memo

**Protocol:**
1. Research Agent writes `research/ideas/proposed/{idea_id}_{slug}.md`
2. Research Agent updates `memory/PROJECT_STATE.md` status to `in_review`
3. Review Agent picks up from `research/ideas/proposed/`

---

### 2. Review → Research: Approval or Rejection

**From:** Review Agent
**To:** Research Agent
**Trigger:** Review is complete
**Artifact:** Decision document

**If approved:**
- Write `research/ideas/approved/{idea_id}_{slug}.md` with approval rationale
- Move original from `proposed/` to `approved/`
- Research Agent proceeds to write programmer handoff

**If rejected:**
- Write `research/ideas/rejected/{idea_id}_{slug}.md` with specific rejection reasons
- Include: what was wrong, whether it's fixable, conditions for reconsideration
- Move original from `proposed/` to `rejected/`

**If needs more research:**
- Add specific questions to the idea note
- Leave in `proposed/` with updated status
- Research Agent addresses questions and resubmits

---

### 3. Research → Programmer: Implementation Handoff

**From:** Research Agent
**To:** Programmer Agent
**Prerequisite:** Review Agent approval
**Artifact:** Programmer handoff in `handoffs/pending/`

**Required fields (20 minimum):**
1. Strategy name and ID
2. Alpha mechanism (plain English, 1 paragraph)
3. Signal specification (plain English, detailed)
4. Universe definition (what assets, when, filters)
5. Data requirements (exact sources, fields, frequency)
6. Lookback windows (signal calculation windows)
7. Entry conditions (exact, unambiguous)
8. Exit conditions (exact, unambiguous)
9. Position sizing (formula in plain English)
10. Rebalancing frequency
11. Transaction cost assumptions
12. Slippage assumptions
13. Expected holding period
14. Capacity estimate
15. Edge cases (minimum 5, with expected behavior)
16. Data quality edge cases (what if data is missing/stale?)
17. Validation checks (how to verify implementation correctness)
18. Parameter ranges to sweep
19. Subperiods to test
20. Link to approved review decision

**Protocol:**
1. Research Agent writes `handoffs/pending/{strategy_id}_handoff.md`
2. Follows `templates/programmer_handoff.md`
3. Programmer Agent picks up and moves to `handoffs/in_progress/`

---

### 4. Programmer → Risk: Backtest Report

**From:** Programmer Agent
**To:** Risk Agent
**Trigger:** Backtest is complete
**Artifact:** Backtest report in `reports/backtests/`

**Required contents:**
- Full backtest configuration (matching handoff spec)
- Equity curve (daily)
- Return statistics (annualized return, vol, Sharpe, Calmar)
- Drawdown chart and statistics
- Parameter sweep results
- Subperiod analysis (at minimum: full period, first half, second half)
- Transaction cost sensitivity (0.5x, 1x, 2x baseline costs)
- Turnover statistics
- Capacity utilization
- Link to source handoff

**Protocol:**
1. Programmer Agent writes `reports/backtests/{strategy_id}_backtest_report.md`
2. Follows `templates/backtest_report.md`
3. Programmer Agent moves handoff to `handoffs/completed/`
4. Risk Agent picks up the backtest report for review

---

### 5. Risk → System: Final Decision

**From:** Risk Agent
**To:** All agents (via `memory/PROJECT_STATE.md`)
**Trigger:** Risk review is complete
**Artifact:** Risk review in `reports/risk_reviews/`

**Required contents:**
- All mandatory risk metrics (see `system/agent_specs/risk-agent.md`)
- Correlation with existing approved strategies
- Defined position limits
- Defined kill switches
- Final decision: approved / rejected / modifications required

**If approved:**
- Risk limits written to `configs/risk/{strategy_id}_limits.yaml`
- Status updated to `paper_trade` or `live_candidate`
- Strategy ready for paper trading under Data Agent

**If rejected:**
- Specific rejection reasons
- Strategy moves to `research/ideas/rejected/`

**If modifications required:**
- Numbered, specific requests
- Sent back to Programmer Agent

---

## Handoff Integrity Rules

1. **No skipping gates.** Research → Review → (approved) → Programmer → Risk. This order is absolute.
2. **No silent modifications.** If the Programmer Agent finds an issue with the signal spec, it must flag it — it cannot silently change the logic.
3. **Every handoff is traceable.** Each document references the previous stage's document.
4. **Rejected ideas are preserved.** They move to `rejected/` or `archived/`, never deleted.
5. **Plain English only in research output.** Research and Review agents produce no code.
6. **The Risk Agent has final authority.** No other agent can override a Risk Agent decision.
