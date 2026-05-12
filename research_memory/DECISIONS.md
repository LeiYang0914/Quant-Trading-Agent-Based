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

### Decision: Source verification required
**What:** Every source cited in a research memo must be verified (paper confirmed to exist, URL resolves, claims cross-checked).
**Why:** Prevents hallucinated citations from entering the research record. Academic credibility is the foundation of this project.

### Decision: Every citation must include a full working URL or DOI
**What:** No source may be cited without a resolvable link. Shorthand references like "BIS.org", "SSRN:12345", "arXiv:2212.06888" are not acceptable — the full URL (e.g., `https://arxiv.org/abs/2212.06888`) must be included in the memo and in SOURCE_TRACKER.md.
**Why:** Makes every source instantly verifiable by a human reader or another agent. Removes ambiguity about where to find the paper. Prevents dead citations that can't be located later.
