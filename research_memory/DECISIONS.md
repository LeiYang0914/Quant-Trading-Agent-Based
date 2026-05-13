# Decisions Log

Important project decisions and their rationale.

---

## 2026-05-12 — Project Structure Decisions

### Decision: Separate research and programming concerns
**What:** Research memos and programmer handoffs are separate artifacts. The researcher documents the alpha idea; the programmer implements the backtest.
**Why:** Prevents scope creep, keeps research focused on idea generation rather than implementation details, and allows the two agents to operate in sequence without conflict.

### Decision: Memory files use flat markdown, not a database
**What:** All project memory (state, backlog, log, sources, decisions) is stored as markdown files in research_memory/.
**Why:** Markdown is human-readable, works with git diff, requires no tooling, and Claude can read/write it natively. Sufficient for a research project of this scale.

### Decision: Research scope limited to crypto and commodities
**What:** Markets covered are crypto (spot, perps, on-chain) and commodity futures (gold, silver, crude oil).
**Why:** These markets have rich data availability, well-documented inefficiencies, and distinct alpha drivers. Equities and FX are excluded for now to maintain focus.

### Decision: No backtests, no trading code, no broker connections
**What:** This project produces research documentation only. Implementation is deferred to a separate Quant Programmer Agent.
**Why:** Maintains a clear boundary between alpha discovery (what this project does) and strategy implementation (what it hands off). Prevents the researcher from becoming a trading system.

## 2026-05-13 — Obsidian Integration Decisions

### Decision: Obsidian vault is the Research Agent's long-term memory, separate from project memory files
**What:** The Obsidian vault (`Quant-Research-KB/`) stores research knowledge (alpha ideas, paper notes, concepts, etc.) while `research_memory/` files remain the project coordination layer (state, backlog, log, sources, decisions).
**Why:** Obsidian excels at interlinked knowledge graphs with backlinks and tags. The project memory files are flat coordination artifacts. They serve different purposes and should not be merged.

### Decision: 9-status alpha lifecycle with clear Research/Programmer ownership boundaries
**What:** Ideas flow through: idea → researching → needs_data_check → ready_for_backtest → waiting_for_programmer → in_backtest → validated | rejected | deprecated. Research Agent owns all statuses except `in_backtest` (Programmer Agent) and post-backtest classification (Research Agent).
**Why:** Prevents ownership ambiguity. The Research Agent never implements; the Programmer Agent never decides what to test.

### Decision: Rejected and deprecated ideas are preserved, never deleted
**What:** Rejected and deprecated alpha ideas move to `11_Rejected_Deprecated/` but the original notes persist with updated status. A Rejected Idea Note explains why.
**Why:** Institutional memory prevents repeating dead ends. Knowing what failed and why is as valuable as knowing what worked.

### Decision: Signal logic must be plain English; high-level structural pseudocode allowed but must not be executable
**What:** Plain English is the default. Structural pseudocode is acceptable only if it cannot be copy-pasted and run. Python, Pine Script, SQL, and any executable code are prohibited in all Research Agent output.
**Why:** Enforces the boundary between research (what to test) and implementation (how to code it). Keeps the Research Agent in its lane.

### Decision: Templated YAML frontmatter with standardized tags for all Obsidian notes
**What:** Every Obsidian note uses YAML frontmatter with `type`, `status`, `tags`, `created`, `updated`, `concepts`, and type-specific fields. Tags use a controlled taxonomy.
**Why:** Enables programmatic retrieval by tag, status, and date. Makes the vault queryable by both the Research Agent and the Programmer Agent.

### Decision: Duplicate detection required before creating any new Alpha Idea note
**What:** The Research Agent must search existing Alpha Ideas and Rejected Ideas for similar mechanisms before creating a new note. If the mechanism matches, the existing note is updated rather than duplicated.
**Why:** Prevents alpha idea clutter. A library of 50 ideas with 30 near-duplicates is worse than 20 distinct, well-researched ideas.

### Decision: Source verification required
**What:** Every source cited in a research memo must be verified (paper confirmed to exist, URL resolves, claims cross-checked).
**Why:** Prevents hallucinated citations from entering the research record. Academic credibility is the foundation of this project.

## 2026-05-14 — Cross-Sectional vs. Absolute Carry Distinction

### Decision: Cross-sectional funding carry is a carry CAPTURE strategy, not a reversal strategy
**What:** For cross-sectional altcoin funding rate strategies, the alpha direction is to go long (with) high relative funding rate altcoins and short low relative funding rate altcoins -- capturing the persistent carry spread. This is distinguished from absolute (time-series) funding rate strategies where extreme funding predicts reversals (crowding/crash signal).
**Why:** The BIS paper (Schmeling et al. 2023) documents that high absolute funding rates predict crashes for BTC/ETH -- a reversal relationship. However, cross-sectional strategies rank altcoins RELATIVE to each other at the same point in time, which hedges out the market-directional crash risk that affects absolute carry. The carry spread between top and bottom quintile altcoins is driven by structurally persistent forces (retail attention concentration, constrained arbitrage capital) that support a carry capture direction. Fan et al. (2024) empirically validates this direction with Sharpe 0.74 for long high-FR / short low-FR. This distinction is foundational for all future cross-sectional alpha research.

### Decision: Every citation must include a full working URL or DOI
**What:** No source may be cited without a resolvable link. Shorthand references like "BIS.org", "SSRN:12345", "arXiv:2212.06888" are not acceptable — the full URL (e.g., `https://arxiv.org/abs/2212.06888`) must be included in the memo and in SOURCE_TRACKER.md.
**Why:** Makes every source instantly verifiable by a human reader or another agent. Removes ambiguity about where to find the paper. Prevents dead citations that can't be located later.
