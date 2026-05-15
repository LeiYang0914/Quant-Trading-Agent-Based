# Quant Trading AI System

A five-agent AI-powered quantitative trading research and strategy development platform for crypto and commodity markets.

**This is not financial advice.** This is a research and engineering system.

## Overview

This system uses five specialized AI agents with strict boundaries to discover, evaluate, implement, and risk-manage quantitative trading strategies:

| Agent | Role | Does | Never Does |
|-------|------|------|------------|
| **Research Agent** | Alpha discovery | Research papers, write memos, create handoffs | Write code, run backtests, make trading decisions |
| **Review Agent** | Quality gate | Evaluate ideas, check overlap, approve/reject | Implement code, invent alpha, approve risk |
| **Programmer Agent** | Implementation | Build signals, backtests, tests, reports | Invent alpha, approve risk, trade live |
| **Data Agent** | Data infrastructure | Source data, monitor quality, simulate execution | Invent alpha, approve risk, modify signals |
| **Risk Agent** | Final gate | Review risk, set limits, approve for paper trading | Invent alpha, write signal code |

## Current Status

**Phase:** Architecture and alpha research. Strategy code, backtests, and live trading are not yet implemented.

### Completed Research (3 memos)
- Crypto Funding Rate Carry and Crowding Signal
- Open Interest-Price Divergence Reversal Signal
- Cross-Sectional Altcoin Funding Rate Carry

### In Progress
- Open Interest-Price Divergence Reversal (needs data check)
- DEX venue funding carry (Drift / ApolloX) — next priority

### Backlog
12 alpha ideas queued across crypto, commodities, and cross-market categories.

## Project Structure

```
.
├── .claude/agents/       — Agent definitions (5 agents)
├── memory/               — Persistent project state
├── research/             — Alpha research memos and idea pipeline
├── handoffs/             — Programmer handoff pipeline
├── knowledge/            — Obsidian knowledge graph
├── system/               — Architecture, workflows, protocols, specs
├── src/                  — Source code (future)
├── configs/              — Configuration files (future)
├── tests/                — Unit and integration tests (future)
├── reports/              — Backtest, risk, and data quality reports
├── paper_trading/        — Paper trading simulation
└── templates/            — Document templates
```

## Alpha Lifecycle

```
idea → research → review → approved → handoff → implementation
→ backtest → paper_trade → risk_review → live_candidate
```

Every idea passes through the Review Agent gate (quality) and the Risk Agent gate (safety). No agent can bypass these gates. Rejected ideas are preserved as institutional memory.

## Getting Started

1. Open this project in Claude Code
2. Claude reads the memory files automatically
3. Invoke agents by role: "Research Agent: investigate..."
4. Agents coordinate through the shared directory structure

## Markets

- **Crypto:** BTC, ETH, liquid altcoins, perpetual futures, funding rates, open interest
- **Commodities:** gold, silver, crude oil futures; term structure, carry, positioning

## Key Design Rules

1. **No agent does everything.** Boundaries are absolute.
2. **Every idea passes review.** The Review Agent is the research-programming gate.
3. **Every strategy passes risk review.** The Risk Agent has final authority.
4. **Plain English only in research output.** No executable code from Research or Review agents.
5. **All sources verified with working URLs.** No hallucinated citations.
6. **Rejected ideas are preserved, never deleted.** Institutional memory is valuable.

## Documentation

- `system/architecture/system_overview.md` — Full system architecture
- `system/workflows/alpha_lifecycle.md` — Complete alpha lifecycle
- `system/protocols/handoff_protocol.md` — Inter-agent handoff formats
- `system/agent_specs/` — Detailed agent specifications
- `memory/SYSTEM_MAP.md` — Where everything lives
