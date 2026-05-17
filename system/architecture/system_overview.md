# System Overview — Quant Trading AI System

## Architecture

This is a **five-agent Quant Trading AI System**. Each agent has a distinct, non-overlapping responsibility. No agent does everything.

A shared **LLM Router** infrastructure layer sits beneath all five agents. Agents do not call LLM providers directly — they submit task requests to the router, which selects Claude or DeepSeek based on task type, complexity, and safety rules.

## The Five Agents + LLM Router

```
┌──────────────────────────────────────────────────────────────────────┐
│                     QUANT TRADING AI SYSTEM                          │
│                                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐              │
│  │ RESEARCH │───→│  REVIEW  │───→│   PROGRAMMER     │              │
│  │  AGENT   │    │  AGENT   │    │     AGENT        │              │
│  │          │←───│  (gate)  │    │                  │              │
│  │ Discover │    │          │    │ Implement        │              │
│  │ Document │    │ Approve/ │    │ Backtest         │              │
│  │ Handoff  │    │ Reject   │    │ Report           │              │
│  └──────────┘    └──────────┘    └────────┬─────────┘              │
│       │                                    │                        │
│       │                                    ↓                        │
│       │              ┌──────────────────────────┐                  │
│       │              │       DATA AGENT         │                  │
│       └──────────────┤   (foundation layer)     │                  │
│                      │                          │                  │
│                      │  Data sourcing           │                  │
│                      │  Quality monitoring      │                  │
│                      │  API adapters            │                  │
│                      │  Execution simulation    │                  │
│                      │  Paper trading infra     │                  │
│                      └──────────────────────────┘                  │
│                                    │                                │
│                                    ↓                                │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                      RISK AGENT                              │  │
│  │                      (final gate)                            │  │
│  │                                                              │  │
│  │  Drawdown · Vol · Leverage · Correlation                     │  │
│  │  Liquidity · Capacity · Kill Switches                        │  │
│  │  Position Sizing · Risk Limits · Approval                    │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    INFRASTRUCTURE LAYER                       │  │
│  │                                                              │  │
│  │  ┌──────────────────────────────────────────────────────┐   │  │
│  │  │                   LLM ROUTER                         │   │  │
│  │  │         (shared by all five agents)                  │   │  │
│  │  │                                                      │   │  │
│  │  │  Task classification → Routing rules → Provider call │   │  │
│  │  │  Claude (complex) / DeepSeek (cost-efficient)        │   │  │
│  │  │  Fallback handling · Decision logging · Cost est.    │   │  │
│  │  └──────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## Agent Boundaries (The Most Important Rule)

| Agent | Does | Never Does |
|-------|------|------------|
| **Research** | Discover alpha, write memos, create handoffs | Write code, run backtests, approve risk |
| **Review** | Evaluate ideas, check overlap, approve/reject | Implement code, invent alpha, approve risk |
| **Programmer** | Implement signals, build backtests, write tests | Invent alpha, approve risk, trade live |
| **Data** | Source data, monitor quality, simulate execution | Invent alpha, approve risk, modify signals |
| **Risk** | Review risk, set limits, final approval gate | Invent alpha, write signal code |

## LLM Router — Shared Infrastructure

The LLM Router is an infrastructure layer shared by all five agents. Key design:

- **Agents do not call LLM providers directly.**
- Each agent submits a `TaskRequest` with task type, complexity, and domain.
- The router applies routing rules and selects Claude or DeepSeek.
- Claude handles high-complexity reasoning, code, and risk-critical decisions.
- DeepSeek handles summarization, text cleanup, source screening, and low-cost tasks.
- All routing decisions are logged to `reports/llm_routing/routing_log.jsonl`.
- Fallback behavior: Claude→DeepSeek blocked for code tasks; DeepSeek→Claude always allowed.
- Dry run mode available for testing without real API calls.

See `system/architecture/llm_router_design.md` for full design and `system/protocols/llm_routing_protocol.md` for the routing protocol.

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
| `src/llm/` | LLM Router, providers, task classifier, utils | Infrastructure |
| `src/data/` | Data loaders and API adapters | Data Agent |
| `src/signals/` | Signal implementations | Programmer Agent |
| `src/backtest/` | Backtest engines | Programmer Agent |
| `src/execution/` | Execution simulation | Data Agent |
| `src/risk/` | Risk calculation utilities | Risk Agent |
| `src/portfolio/` | Portfolio construction | Risk Agent |
| `configs/llm/` | LLM model config, routing rules | Infrastructure |
| `configs/` | Configuration files | Respective agents |
| `tests/llm/` | LLM Router unit tests | Infrastructure |
| `tests/` | Unit and integration tests | Programmer Agent |
| `reports/` | Backtest, risk, data quality reports | Programmer + Risk + Data |
| `reports/llm_routing/` | LLM routing decision audit logs | Infrastructure |
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
9. Agents do not call LLM providers directly — all LLM calls go through the LLM Router.
10. Code generation never falls back from Claude to DeepSeek by default.
11. Risk-critical approvals never route to low-cost models by default.
