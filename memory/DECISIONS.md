# Decisions Log

Important project decisions and their rationale.

---

## 2026-05-15 — Five-Agent System Architecture

### Decision: Restructure from research workspace to five-agent Quant Trading AI System
**What:** The project was refactored from a simple research workspace (single Research Agent + future Programmer Agent) into a five-agent system: Research, Review, Programmer, Data, Risk.
**Why:** A single research agent with a direct-to-programmer pipeline lacks quality gates. The five-agent architecture creates clear separation of concerns: research (discover), review (validate), programming (implement), data (infrastructure), and risk (final gate). Each agent has absolute boundaries — no agent does everything. This prevents scope creep and ensures every alpha idea is independently reviewed before code is written and independently risk-assessed before any capital is put at risk.

### Decision: Two mandatory gates — Review and Risk
**What:** Every alpha idea must pass through two independent gates: the Review Agent (economic rationale, data availability, lookahead bias, overfitting, overlap) and the Risk Agent (drawdown, volatility, correlation, capacity, position sizing, kill switches).
**Why:** Research quality and risk management are distinct concerns. The Review Agent validates that an idea makes sense before anyone writes code. The Risk Agent validates that a strategy is safe before it moves toward paper trading. Neither gate can be bypassed.

### Decision: Clean directory structure with short, simple folder names
**What:** The top-level structure uses simple names: `memory/`, `research/`, `handoffs/`, `knowledge/`, `system/`, `src/`, `configs/`, `tests/`, `reports/`, `paper_trading/`, `templates/`.
**Why:** The old structure (`research_memory/`, `research_memos/`, `handoff_to_programmer/`) was verbose and mixed concerns. The new structure separates research output from project memory, and gives each function a clear, self-explanatory home.

### Decision: All agent specs, workflows, protocols, and architecture docs live under `system/`
**What:** `system/architecture/`, `system/workflows/`, `system/protocols/`, `system/agent_specs/`.
**Why:** Centralizes system-level documentation in one place. Separates agent definitions (`.claude/agents/` — how Claude invokes them) from agent specifications (`system/agent_specs/` — detailed capability and boundary documentation).

---

## 2026-05-14 — Cross-Sectional vs. Absolute Carry Distinction

### Decision: Cross-sectional funding carry is a carry CAPTURE strategy, not a reversal strategy
**What:** For cross-sectional altcoin funding rate strategies, the alpha direction is to go long (with) high relative funding rate altcoins and short low relative funding rate altcoins -- capturing the persistent carry spread. This is distinguished from absolute (time-series) funding rate strategies where extreme funding predicts reversals (crowding/crash signal).
**Why:** The BIS paper (Schmeling et al. 2023) documents that high absolute funding rates predict crashes for BTC/ETH -- a reversal relationship. However, cross-sectional strategies rank altcoins RELATIVE to each other at the same point in time, which hedges out the market-directional crash risk that affects absolute carry. The carry spread between top and bottom quintile altcoins is driven by structurally persistent forces (retail attention concentration, constrained arbitrage capital) that support a carry capture direction. Fan et al. (2024) empirically validates this direction with Sharpe 0.74 for long high-FR / short low-FR. This distinction is foundational for all future cross-sectional alpha research.

### Decision: Every citation must include a full working URL or DOI
**What:** No source may be cited without a resolvable link. Shorthand references like "BIS.org", "SSRN:12345", "arXiv:2212.06888" are not acceptable — the full URL must be included in the memo and in `memory/SOURCE_TRACKER.md`.
**Why:** Makes every source instantly verifiable by a human reader or another agent. Removes ambiguity about where to find the paper. Prevents dead citations that can't be located later.

---

## 2026-05-13 — Obsidian Integration Decisions

### Decision: Obsidian vault is the Research Agent's long-term memory, separate from project memory files
**What:** The Obsidian vault (`knowledge/Quant-Research-KB/`) stores research knowledge (alpha ideas, paper notes, concepts, etc.) while `memory/` files remain the project coordination layer (state, backlog, log, sources, decisions).
**Why:** Obsidian excels at interlinked knowledge graphs with backlinks and tags. The project memory files are flat coordination artifacts. They serve different purposes and should not be merged.

### Decision: 9-status alpha lifecycle with clear Research/Programmer ownership boundaries
**What:** Ideas flow through: idea → researching → needs_data_check → ready_for_backtest → waiting_for_programmer → in_backtest → validated | rejected | deprecated. Research Agent owns all statuses except `in_backtest` (Programmer Agent) and post-backtest classification (Research Agent). **Note:** This has been superseded by the broader lifecycle in `system/workflows/alpha_lifecycle.md` which adds Review and Risk gates.
**Why:** Prevents ownership ambiguity. The Research Agent never implements; the Programmer Agent never decides what to test.

### Decision: Rejected and deprecated ideas are preserved, never deleted
**What:** Rejected and deprecated alpha ideas move to `research/ideas/rejected/` but the original notes persist with updated status.
**Why:** Institutional memory prevents repeating dead ends. Knowing what failed and why is as valuable as knowing what worked.

### Decision: Signal logic must be plain English; high-level structural pseudocode allowed but must not be executable
**What:** Plain English is the default. Structural pseudocode is acceptable only if it cannot be copy-pasted and run. Python, Pine Script, SQL, and any executable code are prohibited in all Research Agent output.
**Why:** Enforces the boundary between research (what to test) and implementation (how to code it).

### Decision: Templated YAML frontmatter with standardized tags for all Obsidian notes
**What:** Every Obsidian note uses YAML frontmatter with `type`, `status`, `tags`, `created`, `updated`, `concepts`, and type-specific fields.
**Why:** Enables programmatic retrieval by tag, status, and date.

### Decision: Duplicate detection required before creating any new Alpha Idea note
**What:** The Research Agent must search existing Alpha Ideas and Rejected Ideas for similar mechanisms before creating a new note.
**Why:** Prevents alpha idea clutter.

### Decision: Source verification required
**What:** Every source cited in a research memo must be verified (paper confirmed to exist, URL resolves, claims cross-checked).
**Why:** Prevents hallucinated citations from entering the research record.

---

## 2026-05-12 — Project Structure Decisions

### Decision: Separate research and programming concerns
**What:** Research memos and programmer handoffs are separate artifacts. The researcher documents the alpha idea; the programmer implements the backtest.
**Why:** Prevents scope creep and keeps research focused on idea generation.

### Decision: Memory files use flat markdown, not a database
**What:** All project memory is stored as markdown files in `memory/`.
**Why:** Markdown is human-readable, works with git diff, requires no tooling.

### Decision: Research scope limited to crypto and commodities
**What:** Markets covered are crypto (spot, perps, on-chain) and commodity futures (gold, silver, crude oil).
**Why:** These markets have rich data availability, well-documented inefficiencies, and distinct alpha drivers.

### Decision: No backtests, no trading code, no broker connections
**What:** This project produces research documentation only. Implementation is deferred to the Programmer Agent.
**Why:** Maintains a clear boundary between alpha discovery and strategy implementation.
