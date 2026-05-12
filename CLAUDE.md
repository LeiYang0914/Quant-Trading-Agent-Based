# CLAUDE.md — Quant Alpha Research Project

## Project Identity

This is a **Quant Alpha Research workspace**. The goal is to discover, evaluate, and document alpha ideas for crypto markets and commodity futures. Output is research memos and programmer handoff documents — not trading code.

## Scope

**In-scope markets:**
- Crypto: BTC, ETH, liquid altcoins, spot, perpetual futures, funding rates, open interest, liquidations, stablecoin flows, on-chain activity, exchange flows, order book imbalance, volatility, options skew, ETF flows, social sentiment
- Commodities: gold futures, silver futures, crude oil futures; term structure, carry, roll yield, inventory, CFTC positioning, real rates, USD, inflation expectations, volatility regimes, macro sensitivity, seasonality

**Out of scope (do not do):**
- Do not write production trading code
- Do not implement backtests
- Do not create a Python trading system
- Do not connect to broker APIs
- Do not place trades
- Do not give financial advice

This project is for academic-style quant research and alpha documentation only.

## Memory Protocol (mandatory)

At the **start of every session**, read files in this order:
1. `CLAUDE.md` (this file)
2. `research_memory/PROJECT_STATE.md`
3. `research_memory/ALPHA_BACKLOG.md`
4. `research_memory/DECISIONS.md`

At the **end of every session**, update:
- `research_memory/PROJECT_STATE.md` — what was done, what changed, next steps
- `research_memory/RESEARCH_LOG.md` — append a dated session entry
- `research_memory/ALPHA_BACKLOG.md` — if new alpha ideas were added
- `research_memory/SOURCE_TRACKER.md` — if new sources were used
- `research_memory/DECISIONS.md` — if important project decisions were made

## Agent Roles

### Quant Alpha Researcher (`claude`)
- Read/research/documentation agent
- Discovers alpha ideas from papers, blogs, data sources
- Synthesizes factor definitions, data requirements, failure modes
- Writes research memos in `research_memos/`
- Writes handoff documents for the Programmer Agent in `handoff_to_programmer/pending/`
- Does **not** write code, backtests, or connect to APIs

### Quant Programmer (future agent, not yet configured)
- Reads handoff documents from `handoff_to_programmer/pending/`
- Implements backtests according to specifications
- Writes results back to `handoff_to_programmer/completed/`

## File Structure

```
CLAUDE.md                                  — This file
README.md                                  — Human-readable project overview
.claude/agents/quant-alpha-researcher.md   — Researcher agent definition
research_memory/                           — Persistent project state
  PROJECT_STATE.md                         — Current state, recent work, next steps
  ALPHA_BACKLOG.md                         — Queue of alpha ideas to research
  RESEARCH_LOG.md                          — Dated log of research sessions
  SOURCE_TRACKER.md                        — Registry of sources consulted
  DECISIONS.md                             — Important project decisions
research_memos/                            — Completed research memos
  crypto/                                  — Crypto alpha memos
  commodities/                             — Commodity alpha memos
  cross_market/                            — Cross-market alpha memos
handoff_to_programmer/                     — Handoff documents
  pending/                                 — Ready for programmer agent
  completed/                               — Implemented by programmer agent
templates/                                 — Document templates
  alpha_research_memo_template.md
  programmer_handoff_template.md
alpha_idea/                                — Legacy; migrate to research_memos/
```

## Writing Guidelines

- Research memos follow the template in `templates/alpha_research_memo_template.md`
- Handoff documents follow the template in `templates/programmer_handoff_template.md`
- Every alpha memo must include: mechanism, source inspiration, factor definition, data requirements, failure modes, evaluation metrics, robustness tests
- Every source citation must include: full author/title, a verified URL or DOI that resolves, and a relevance statement explaining what was taken from the source
- No source may be cited without a working link — never cite by name alone (e.g., "BIS.org" or "SSRN:12345" without the full URL)
- Every source must be verified before inclusion (paper exists, URL resolves, claims cross-checked)
- Prioritize falsifiability: every hypothesis must specify what evidence would disprove it
