# handoff_preparation_skill.md

## Purpose

Help the Research Agent prepare clean, complete handoffs for the Review Agent (primary path) or the Programmer Agent (after Review approval). This skill defines exactly what must be included, what must be excluded, and what the Research Agent cannot decide.

## When to Use

After a research memo passes all quality control checks and is marked `ready_for_review`. The handoff to the Review Agent is the standard next step. A direct programmer handoff is only prepared AFTER the Review Agent approves the idea.

## Handoff Paths

### Path A: Research Agent → Review Agent (Standard)

This is the primary path. The Research Agent writes:
- The completed research memo in `research/memos/{domain}/`
- The alpha discovery note in `research/ideas/proposed/{domain}/`
- A session log following `templates/research_session_log.md`

The Review Agent picks up from `research/ideas/proposed/{domain}/` and reads the linked memo.

### Path B: Research Agent → Programmer Agent (After Review Approval Only)

Only after the Review Agent moves the idea to `research/ideas/approved/{domain}/` does the Research Agent write a programmer handoff to `handoffs/pending/` following `templates/programmer_handoff.md`.

**The Research Agent must not skip the Review Agent and hand directly to the Programmer Agent.**

## What a Review Handoff Must Include

The review package (what the Review Agent sees) must contain:

1. **Alpha discovery note** in `research/ideas/proposed/{domain}/`
   - Alpha ID
   - Domain
   - One-paragraph mechanism summary
   - Falsifiable hypothesis
   - Required data (with availability status)
   - Key failure modes (top 3)
   - Link to full research memo
   - Reference status: sufficient / partial / none

2. **Research memo** in `research/memos/{domain}/`
   - Complete all 19 sections per `templates/research_memo.md`
   - Quality control checklist passed (per `research_quality_control_skill.md`)

3. **Source confirmation**
   - All references have working URLs
   - All sources recorded in `memory/SOURCE_TRACKER.md`

## What a Programmer Handoff Must Include

Only after Review Agent approval. Write to `handoffs/pending/` following `templates/programmer_handoff.md`.

Required fields (20 minimum):
1. Strategy name and Alpha ID
2. Alpha mechanism (plain English, one paragraph)
3. Signal specification (plain English, step by step)
4. Universe definition (assets, filters, rebalancing)
5. Data requirements (sources, fields, frequency)
6. Lookback windows
7. Entry conditions (unambiguous)
8. Exit conditions (unambiguous)
9. Position sizing (plain English formula)
10. Rebalancing frequency
11. Transaction cost assumptions
12. Slippage assumptions
13. Expected holding period
14. Capacity estimate
15. Edge cases (minimum 5, with expected behavior)
16. Data quality edge cases
17. Validation checks for implementation correctness
18. Parameter ranges to sweep
19. Subperiods to test
20. Link to approved review decision

## What Must NOT Be in Any Handoff

- Executable code (Python, SQL, Pine Script, etc.)
- Trading recommendations ("buy X," "allocate Y%")
- Risk approval (that's the Risk Agent's job)
- Performance claims ("this will generate 20% annual return")
- Live trading instructions
- API keys or credentials

## What the Research Agent Cannot Decide

The Research Agent must not:
- Decide that an idea is ready for implementation without Review Agent approval
- Set position limits (Risk Agent's job)
- Set leverage limits (Risk Agent's job)
- Approve a strategy for paper trading (Risk Agent's job)
- Decide that a strategy's risk is acceptable (Risk Agent's job)
- Modify the alpha logic during handoff — the handoff must match the approved memo

## How to Describe Implementation Requirements Without Code

For the Programmer Agent, describe:

**Data loading:** "Fetch daily funding rates from Binance API for the top 20 altcoins by market cap. Use the funding rate at 00:00 UTC each day. Reconstruct the universe point-in-time using CoinGecko historical market cap rankings."

**Signal computation:** "For each day, compute the cross-sectional z-score of the funding rate across the universe. Rank assets by z-score. Assign top quintile to long portfolio, bottom quintile to short portfolio. Equal-weight within each quintile."

**Backtest design:** "Run from 2021-01-01 to 2024-12-31. Rebalance daily at 00:00 UTC. Account for 0.04% taker fee per trade. Test parameter sweeps: lookback windows of 1d/3d/7d for the z-score; quintile vs. decile splits; top 20 vs. top 30 universe."

**Tests:** "Test that signal values are identical when recomputed from raw data. Test that positions sum to zero (dollar-neutral). Test edge case: fewer than 5 assets in universe → strategy returns cash."

## How to Mark Unresolved Questions

Include in the handoff:

```
## Open Questions for Programmer Agent
1. Can CoinGecko historical market cap data be reconstructed point-in-time?
   If not, use current market cap as a static universe.
2. What is the actual capacity before slippage exceeds 10 bps?
   Test with position sizes of $1M, $5M, $10M, $20M.
```

## Inputs

- Approved alpha discovery note (from `research/ideas/approved/{domain}/`)
- Research memo
- Review Agent approval

## Outputs

- Programmer handoff in `handoffs/pending/{alpha_id}_handoff.md`
- Updated `memory/PROJECT_STATE.md`

## Anti-Patterns

- Writing a programmer handoff before Review Agent approval
- Including executable code in the handoff
- Making risk decisions (leverage, position limits)
- Vague edge case descriptions ("handle missing data gracefully")
- Skipping the validation checks section
- Omitting the link to the approved review decision
