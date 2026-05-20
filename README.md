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

### Prerequisites

- Python 3.11 or later
- pip

### Install

```bash
# Core (routing, configs, dry-run mode — no API keys needed)
pip install pyyaml python-dotenv

# With Claude (Anthropic) provider support
pip install anthropic

# With DeepSeek provider support
pip install openai

# Everything
pip install anthropic openai python-dotenv pyyaml
```

Or use the pyproject.toml:

```bash
pip install -e ".[all]"
```

### Configure API Keys

Create a `.env` file in the project root. The file is gitignored — it will never be committed.

```bash
# .env (gitignored — never commit this file)
ANTHROPIC_API_KEY=sk-ant-...
DEEPSEEK_API_KEY=sk-...
```

Keys are loaded via `python-dotenv` on provider import. You can also set them as system environment variables.

**Without API keys**, the router works in dry-run mode for testing and development.

### LLM Router Quick Start

```bash
# Check which providers are configured
python scripts/llm_router_cli.py --health-check

# Dry-run a routing decision (no API call)
python scripts/llm_router_cli.py --dry-run --agent research-agent --task paper_analysis --prompt "Analyze this paper..."

# Real API call (requires API key configured)
python scripts/llm_router_cli.py --real --agent programmer-agent --task code_generation --prompt "Write a Sharpe ratio function"

# View usage and cost summary
python scripts/llm_router_cli.py --usage-summary
```

### LLM Router Dashboard

Launch the browser-based observability dashboard:

```bash
# Install dashboard dependencies
pip install streamlit pandas plotly

# Run real or dry-run LLM Router calls to populate logs
python scripts/llm_router_cli.py --dry-run --agent research-agent --task research_reasoning --prompt "Analyze market structure"
python scripts/llm_router_cli.py --real --agent data-agent --task summarization --prompt "Summarize this data"

# Launch the dashboard
python scripts/run_dashboard.py
```

The dashboard opens at `http://localhost:8501` with 8 pages:
- **Overview** — KPIs: calls (real + dry-run), real API cost, success rate, cache rate, latency, provider split
- **Providers** — Per-provider breakdown (Claude vs DeepSeek)
- **Agents** — Per-agent usage, cost, task type mix
- **Costs** — Real API cost analysis, cache savings, most expensive calls
- **Routing** — Full routing decision table with real/dry-run type indicator and filters
- **Failures** — Error analysis with failure rate and fallback tracking
- **Cache** — Cache hit ratio, savings, cached task types
- **Health** — Live provider health (availability, circuit state, rate limits)

If no logs exist, the dashboard shows an empty state with instructions to run router CLI commands.

### Work in Claude Code

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
