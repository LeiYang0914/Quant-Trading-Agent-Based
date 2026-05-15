# Alpha Lifecycle

The complete lifecycle of an alpha idea in the Quant Trading AI System.

## Lifecycle Stages

```
                         ┌─────────────┐
                         │    IDEA     │  ← Research Agent discovers or backlog promotes
                         └──────┬──────┘
                                │
                                ▼
                         ┌─────────────┐
                         │  RESEARCH   │  ← Research Agent writes memo + idea note
                         └──────┬──────┘
                                │
                                ▼
                         ┌─────────────┐
                         │   REVIEW    │  ← Review Agent evaluates
                         └──────┬──────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              ┌──────────┐ ┌────────┐ ┌──────────────┐
              │ APPROVED │ │ NEEDS  │ │   REJECTED   │
              └────┬─────┘ │ MORE   │ └──────────────┘
                   │        │RESEARCH│      ↑
                   │        └────────┘      │ (return to Research Agent
                   │                        │  with specific questions)
                   │                        │
                   ▼                        │
              ┌──────────┐                  │
              │ HANDOFF  │  ← Research Agent writes programmer handoff
              └────┬─────┘
                   │
                   ▼
              ┌──────────────┐
              │IMPLEMENTATION│  ← Programmer Agent implements
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │  BACKTEST    │  ← Programmer Agent runs backtest, writes report
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │ PAPER_TRADE  │  ← Data Agent runs paper trading simulation
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │ RISK_REVIEW  │  ← Risk Agent evaluates (FINAL GATE)
              └──────┬───────┘
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
   ┌───────────┐ ┌────────┐ ┌──────────────┐
   │ APPROVED  │ │ NEEDS  │ │   REJECTED   │
   │ (live     │ │ CHANGES│ └──────────────┘
   │ candidate) │ └────────┘
   └─────┬─────┘
         │
         ▼
   ┌──────────────┐
   │ LIVE         │  ← Future: live trading integration
   │ CANDIDATE    │
   └──────────────┘
```

## Stage Details

### 1. IDEA
- **Source:** Research Agent discovery, backlog promotion, or external inspiration
- **Artifact:** Entry in `memory/ALPHA_BACKLOG.md`
- **Owner:** Research Agent

### 2. RESEARCH
- **Action:** Research Agent investigates mechanism, sources, data requirements, failure modes
- **Artifacts:** Research memo in `research/memos/`, idea note in `research/ideas/proposed/`
- **Owner:** Research Agent
- **Checkpoint:** Is the idea well-defined enough to review? Is there a falsifiable hypothesis?

### 3. REVIEW
- **Action:** Review Agent evaluates economic rationale, data availability, lookahead bias, overfitting, overlap
- **Artifact:** Decision in `research/ideas/approved/` or `research/ideas/rejected/`
- **Owner:** Review Agent
- **Checkpoint:** Does this idea pass all review criteria?

### 4. APPROVED
- **Action:** Research Agent writes programmer handoff
- **Artifact:** Handoff document in `handoffs/pending/`
- **Owner:** Research Agent
- **Checkpoint:** Is the handoff complete and unambiguous?

### 5. HANDOFF → IMPLEMENTATION
- **Action:** Programmer Agent picks up handoff, moves to `handoffs/in_progress/`, implements signal + backtest
- **Artifacts:** Code in `src/signals/`, `src/backtest/`, tests in `tests/`
- **Owner:** Programmer Agent
- **Checkpoint:** Does the implementation match the handoff exactly?

### 6. BACKTEST
- **Action:** Programmer Agent runs backtest, writes report
- **Artifacts:** Backtest report in `reports/backtests/`, handoff moved to `handoffs/completed/`
- **Owner:** Programmer Agent
- **Checkpoint:** Are backtest results within expected ranges?

### 7. PAPER_TRADE
- **Action:** Data Agent runs paper trading simulation with realistic execution
- **Artifacts:** Logs in `paper_trading/logs/`, state in `paper_trading/state/`
- **Owner:** Data Agent
- **Checkpoint:** Does live signal behavior match backtest expectations?

### 8. RISK_REVIEW (FINAL GATE)
- **Action:** Risk Agent evaluates all risk metrics, correlation, capacity, defines limits
- **Artifacts:** Risk review in `reports/risk_reviews/`, risk limits in `configs/risk/`
- **Owner:** Risk Agent
- **Checkpoint:** Is this strategy safe to promote to live candidate?

### 9. LIVE_CANDIDATE / REJECTED / ARCHIVED
- **Live candidate:** Strategy is ready for future live trading integration
- **Rejected:** Returned to `research/ideas/rejected/` with reasons
- **Archived:** Previously approved but retired strategies move to `research/ideas/archived/`

## Rejection Paths

An idea can be rejected at two gates:

| Gate | Rejected By | Reason |
|------|------------|--------|
| Review | Review Agent | Economic rationale unsound, data unavailable, lookahead bias, overfitting, overlap |
| Risk Review | Risk Agent | Excessive drawdown, low Sharpe, insufficient capacity, high correlation, unstable parameters |

Rejected ideas are **preserved**, never deleted. They live in `research/ideas/rejected/` and serve as institutional memory.

## Agent Ownership Per Stage

| Stage | Owner | Other Agents Involved |
|-------|-------|----------------------|
| idea → research | Research Agent | Data Agent (consulted for availability) |
| review | Review Agent | Data Agent (consulted for quality) |
| approved → handoff | Research Agent | — |
| implementation → backtest | Programmer Agent | Data Agent (data loaders) |
| paper_trade | Data Agent | Programmer Agent (signal code) |
| risk_review | Risk Agent | Data Agent (quality reports) |
| live_candidate | Risk Agent (final sign-off) | All agents informed |
