# CLAUDE.md — Quant Trading AI System

## Project Identity

This is a **Quant Trading AI System** — a five-agent research and strategy development platform for crypto markets and commodity futures. The system discovers alpha ideas, reviews them, implements them as backtestable strategies, manages data infrastructure, and enforces risk controls.

**This is not financial advice.** This is a research and engineering system.

## Five-Agent Architecture

| Agent | Role | Boundaries |
|-------|------|------------|
| **Research Agent** | Discover alpha, write memos, create handoffs | No code, no backtests, no trading decisions |
| **Review Agent** | Gate between research and implementation | No code, no alpha invention, no risk approval |
| **Programmer Agent** | Implement approved ideas, run backtests | No alpha invention, no risk approval |
| **Data Agent** | Data sourcing, quality, execution simulation | No alpha invention, no risk approval |
| **Risk Agent** | Final risk gate, position sizing, kill switches | No alpha invention, no signal code |

**Core rule:** No agent does everything. Each agent has absolute boundaries.

See `system/architecture/system_overview.md` for the full architecture.

## Research Agent Domain Separation

The Research Agent enforces strict separation between crypto and commodities research:

- **crypto** — perpetual futures, spot, funding rates, OI, liquidations, on-chain, exchange flows
- **commodities** — gold, silver, crude oil, natural gas, copper, ags; term structure, CFTC COT, inventory
- **cross_market** — ideas explicitly linking both domains

**Default order:** crypto first → commodities second → cross_market only when requested.

Crypto and commodities must not be mixed in the same memo without cross_market labeling.

See `system/protocols/research_protocol.md` for the full Research Agent workflow.

## Scope

**In-scope markets:**
- Crypto: BTC, ETH, liquid altcoins, spot, perpetual futures, funding rates, open interest, liquidations, stablecoin flows, on-chain activity, exchange flows, order book imbalance, volatility, options skew, ETF flows, social sentiment
- Commodities: gold futures, silver futures, crude oil futures; term structure, carry, roll yield, inventory, CFTC positioning, real rates, USD, inflation expectations, volatility regimes, macro sensitivity, seasonality

**Current phase:** Architecture and research. Strategy code, backtests, and live trading are not yet implemented.

## Memory Protocol (mandatory)

At the **start of every session**, read files in this order:
1. `CLAUDE.md` (this file)
2. `memory/PROJECT_STATE.md`
3. `memory/ALPHA_BACKLOG.md`
4. `memory/DECISIONS.md`
5. `memory/SYSTEM_MAP.md`

At the **end of every session**, update:
- `memory/PROJECT_STATE.md` — what was done, what changed, next steps
- `memory/RESEARCH_LOG.md` — append a dated session entry
- `memory/ALPHA_BACKLOG.md` — if new alpha ideas were added
- `memory/SOURCE_TRACKER.md` — if new sources were used
- `memory/DECISIONS.md` — if important project decisions were made

## Directory Structure

```
CLAUDE.md                              — This file
README.md                              — Human-readable project overview
.claude/agents/                        — Agent personality definitions (5 agents)
memory/                                — Persistent project state
  PROJECT_STATE.md                     — Current state, recent work, next steps
  ALPHA_BACKLOG.md                     — Queue of alpha ideas to research
  RESEARCH_LOG.md                      — Dated log of research sessions
  SOURCE_TRACKER.md                    — Registry of sources consulted
  DECISIONS.md                         — Important project decisions
  SYSTEM_MAP.md                        — Where everything lives
research/                              — Alpha research outputs
  memos/{crypto,commodities,cross_market}/ — Research memos
  ideas/{proposed,approved,rejected,archived}/ — Idea pipeline
  papers/                              — Saved papers
handoffs/                              — Programmer handoff pipeline
  {pending,in_progress,completed,archived}/
knowledge/Quant-Research-KB/           — Obsidian knowledge graph
system/                                — System documentation
  architecture/                        — Architecture docs
  workflows/                           — Workflow definitions
  protocols/                           — Inter-agent protocols
  agent_specs/                         — Detailed agent specifications
src/                                   — Source code (future)
configs/                               — Configuration files (future)
tests/                                 — Tests (future)
reports/                               — Backtest, risk, data quality reports
paper_trading/                         — Paper trading simulation
templates/                             — Document templates
```

## Alpha Lifecycle

```
idea → research → review → approved → handoff → implementation
→ backtest → paper_trade → risk_review → live_candidate → archived
                                                              ↘ rejected
```

See `system/workflows/alpha_lifecycle.md` for details.

## Writing Guidelines

- Research memos follow the template in `templates/research_memo.md`
- Handoff documents follow the template in `templates/programmer_handoff.md`
- Every alpha memo must include: mechanism, source inspiration, factor definition, data requirements, failure modes, evaluation metrics, robustness tests
- Every source citation must include: full author/title, a verified URL or DOI that resolves, and a relevance statement explaining what was taken from the source
- No source may be cited without a working link — never cite by name alone (e.g., "BIS.org" or "SSRN:12345" without the full URL)
- Every source must be verified before inclusion (paper exists, URL resolves, claims cross-checked)
- Prioritize falsifiability: every hypothesis must specify what evidence would disprove it
- Signal logic must be plain English. No executable code in research output.

## Agent Invocation

To invoke a specific agent, reference its role:
- "Research Agent: investigate X" — alpha discovery and documentation
- "Review Agent: evaluate idea Y" — gate review
- "Programmer Agent: implement handoff Z" — code and backtests
- "Data Agent: check data quality for X" — data infrastructure
- "Risk Agent: review strategy Y" — risk assessment and approval
