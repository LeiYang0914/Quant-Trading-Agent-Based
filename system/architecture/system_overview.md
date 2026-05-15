# System Overview — Quant Trading AI System

## Architecture

This is a **five-agent Quant Trading AI System**. Each agent has a distinct, non-overlapping responsibility. No agent does everything.

## The Five Agents

```
┌─────────────────────────────────────────────────────────────┐
│                  QUANT TRADING AI SYSTEM                     │
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐     │
│  │ RESEARCH │───→│  REVIEW  │───→│   PROGRAMMER     │     │
│  │  AGENT   │    │  AGENT   │    │     AGENT        │     │
│  │          │←───│  (gate)  │    │                  │     │
│  │ Discover │    │          │    │ Implement        │     │
│  │ Document │    │ Approve/ │    │ Backtest         │     │
│  │ Handoff  │    │ Reject   │    │ Report           │     │
│  └──────────┘    └──────────┘    └────────┬─────────┘     │
│       │                                    │               │
│       │                                    ↓               │
│       │              ┌──────────────────────────┐         │
│       │              │       DATA AGENT         │         │
│       └──────────────┤   (foundation layer)     │         │
│                      │                          │         │
│                      │  Data sourcing           │         │
│                      │  Quality monitoring      │         │
│                      │  API adapters            │         │
│                      │  Execution simulation    │         │
│                      │  Paper trading infra     │         │
│                      └──────────────────────────┘         │
│                                    │                       │
│                                    ↓                       │
│  ┌────────────────────────────────────────────────────┐   │
│  │                 RISK AGENT                         │   │
│  │                 (final gate)                       │   │
│  │                                                    │   │
│  │  Drawdown · Vol · Leverage · Correlation           │   │
│  │  Liquidity · Capacity · Kill Switches              │   │
│  │  Position Sizing · Risk Limits · Approval          │   │
│  └────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Agent Boundaries (The Most Important Rule)

| Agent | Does | Never Does |
|-------|------|------------|
| **Research** | Discover alpha, write memos, create handoffs | Write code, run backtests, approve risk |
| **Review** | Evaluate ideas, check overlap, approve/reject | Implement code, invent alpha, approve risk |
| **Programmer** | Implement signals, build backtests, write tests | Invent alpha, approve risk, trade live |
| **Data** | Source data, monitor quality, simulate execution | Invent alpha, approve risk, modify signals |
| **Risk** | Review risk, set limits, final approval gate | Invent alpha, write signal code |

## Directory Map

| Directory | Purpose | Primary Owner |
|-----------|---------|---------------|
| `memory/` | Persistent project state, backlog, decisions | All agents |
| `research/memos/` | Completed research memos | Research Agent |
| `research/ideas/` | Idea pipeline: proposed → approved → rejected | Research + Review |
| `research/papers/` | Downloaded/saved papers | Research Agent |
| `handoffs/` | Programmer handoffs: pending → in_progress → completed | Research + Programmer |
| `knowledge/Quant-Research-KB/` | Obsidian knowledge graph | Research Agent |
| `system/` | Architecture, workflows, protocols, agent specs | System-level |
| `src/data/` | Data loaders and API adapters | Data Agent |
| `src/signals/` | Signal implementations | Programmer Agent |
| `src/backtest/` | Backtest engines | Programmer Agent |
| `src/execution/` | Execution simulation | Data Agent |
| `src/risk/` | Risk calculation utilities | Risk Agent |
| `src/portfolio/` | Portfolio construction | Risk Agent |
| `configs/` | Configuration files | Respective agents |
| `tests/` | Unit and integration tests | Programmer Agent |
| `reports/` | Backtest, risk, data quality reports | Programmer + Risk + Data |
| `paper_trading/` | Paper trading logs and state | Data Agent |
| `templates/` | Document templates | All agents |

## Alpha Lifecycle

```
idea → research → review → approved → handoff → implementation
→ backtest → paper_trade → risk_review → live_candidate → archived
                                                                  ↘ rejected
```

See `system/workflows/alpha_lifecycle.md` for the detailed lifecycle.

## System Invariants

1. No agent does everything. Boundaries are absolute.
2. Every alpha idea passes through the Review Agent gate.
3. Every strategy passes through the Risk Agent gate before paper trading.
4. Rejected ideas are preserved, never deleted.
5. All sources must be verified with working URLs.
6. All signal logic in research output must be plain English (no executable code).
7. The Data Agent serves all other agents — it is the foundation.
8. The Risk Agent has final authority on all risk decisions.
