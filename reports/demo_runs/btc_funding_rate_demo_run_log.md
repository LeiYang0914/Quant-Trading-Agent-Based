# Demo Run Log: BTC Funding Rate Crowding & Reversal Signal

**Date:** 2026-05-19
**Session type:** Demo — interview evidence workflow
**Session domain:** crypto
**Alpha ID:** CRYPTO-DEMO-001

---

## Input Alpha Idea

> "Bitcoin perpetual funding rate as a crowding and reversal signal."

A directional contrarian signal: when BTC perpetual funding rates reach extreme positive levels (indicating crowded leveraged-long positioning), fade the crowd with a short position expecting a mean-reverting reversal driven by liquidation cascades and deleveraging dynamics.

---

## Files Inspected (Read Order)

| # | File | Purpose |
|---|------|---------|
| 1 | `CLAUDE.md` | Project identity, five-agent architecture, memory protocol, alpha lifecycle, writing guidelines |
| 2 | `memory/PROJECT_STATE.md` | Current project phase (architecture + research), active memos (CRYPTO-001 through 003), LLM Router status |
| 3 | `memory/ALPHA_BACKLOG.md` | 13 queued ideas across crypto/commodities/cross-market; CRYPTO-001 already covers funding rate carry + crowding |
| 4 | `memory/SOURCE_TRACKER.md` | 28 registered sources (all crypto), 11 Tier 1 papers, 10 data vendors; CRYPTO-PAPER-001 through 007 directly relevant |
| 5 | `memory/SYSTEM_MAP.md` | Full directory map including `src/llm/` router infrastructure, 112 passing tests |
| 6 | `memory/DECISIONS.md` | Architecture decisions: LLM Router (Claude for complex, DeepSeek for throughput), cross-sectional vs absolute carry distinction, source verification requirements |
| 7 | `memory/RESEARCH_LOG.md` | 6 prior sessions (2026-05-12 through 2026-05-17), full 9-skill sequence on CRYPTO-002, LLM Router production upgrade |
| 8 | `system/workflows/alpha_lifecycle.md` | 9-stage lifecycle: idea → research → review → approved → handoff → implementation → backtest → paper_trade → risk_review |
| 9 | `system/protocols/research_protocol.md` | 9-skill research workflow with quality gates, source tier requirements, domain separation |
| 10 | `system/protocols/handoff_protocol.md` | 5 handoff types, 20-field Research→Programmer handoff requirement, integrity rules |
| 11 | `system/protocols/llm_routing_protocol.md` | Routing decision tree, Claude/DeepSeek task split, fallback rules, caching exclusions |
| 12 | `templates/research_memo.md` | 19-section memo template with structured reference format |
| 13 | `templates/programmer_handoff.md` | 11-section handoff template |
| 14 | `knowledge/Quant-Research-KB/Dashboard.md` | Vault map: 2 concepts, 2 alpha ideas, 5 paper notes, 1 data source note |
| 15 | `knowledge/Quant-Research-KB/01_Concepts/Funding Rate.md` | Core concept: absolute vs cross-sectional FR signals, mechanism, key papers |
| 16 | `research/memos/crypto/01_crypto_funding_rate_carry.md` | CRYPTO-001: full memo with 3 sub-hypotheses including Factor B (crowding reversal); 7 Tier 1 sources, 9 failure modes, 11 robustness tests |

---

## Workflow Steps

### Step 1: Domain Queue Management (Skill 1)
- **Domain selected:** crypto
- **Rationale:** PROJECT_STATE.md confirms crypto-first priority; commodities backlog not yet active
- **Idea selected:** "BTC perpetual funding rate as crowding and reversal signal" — refines CRYPTO-001 Factor B as a standalone signal
- **Relationship to existing work:** CRYPTO-001 covers this as Sub-hypothesis B within a broader three-factor memo. This demo isolates and sharpens the crowding-reversal signal as a self-contained alpha, adding specific calibration and edge case detail not present in the original memo.

### Step 2: Source Discovery (Skill 2 — abbreviated for demo)
- **Existing sources consulted:** CRYPTO-PAPER-001 through 007 all provide supporting evidence
- **Key sources for this signal:**
  - Schmeling, Schrimpf, Todorov (2023), BIS WP 1087 — documents that high absolute funding predicts crashes (reversal relationship)
  - He, Manela, Ross, von Wachter (2022), arXiv:2212.06888 — perpetual futures pricing fundamentals
  - Inan (2025), SSRN:5576424 — funding rate predictability supports signal timing
- **Note:** No new web search conducted for this demo; all sources drawn from existing verified registry

### Step 3: Paper Analysis (Skill 3 — abbreviated)
- Existing paper summaries in knowledge base and SOURCE_TRACKER.md provide sufficient foundation
- Extracted key finding: BIS paper confirms that extreme positive funding rates predict negative BTC forward returns over 1–30 day horizons

### Step 4: Crypto Market Structure Analysis (Skill 4)
- Applied crypto-specific microstructure context:
  - 8-hour funding settlement cycle (00:00, 08:00, 16:00 UTC) creates natural signal evaluation cadence
  - Cross-margin liquidation cascades amplify reversals — when crowded longs get liquidated, forced selling pushes price further down, triggering more liquidations
  - CEX funding formula differences (Binance vs Bybit vs OKX) require OI-weighted multi-exchange aggregation
  - Funding rate caps (typically 0.375%–0.75% per 8h) create a natural ceiling that may mask true crowding intensity
  - Institutional arbitrage capital has compressed static carry but the crowding-reversal dynamic persists because it requires timing, not just position size

### Step 5: Alpha Discovery (Skill 5)
- Wrote alpha discovery note to `research/ideas/proposed/crypto/CRYPTO_DEMO_btc_funding_rate_crowding_reversal.md`
- Hypothesis: When BTC 8-hour funding rate exceeds the 90th percentile of its trailing 30-day distribution, forward 8–48 hour BTC spot returns are negatively skewed with negative expected value
- Mechanism: Crowded leveraged longs → elevated liquidation risk → forced selling cascade on adverse price moves

### Step 6: Memo Writing (Skill 6)
- Wrote 19-section research memo to `research/memos/crypto/CRYPTO_DEMO_btc_funding_rate_crowding_reversal.md`
- Plain English only, no executable code
- 6 structured source references, 5 failure modes, 6 robustness tests

### Step 7: Quality Control (Skill 7 — lightweight for demo)
- **Source check:** 6 sources cited, all Tier 1, all verified in SOURCE_TRACKER.md
- **Domain clarity:** crypto only, no commodity mixing
- **Falsifiability:** Yes — if extreme funding is NOT followed by negative forward returns over 8–48h, the hypothesis is falsified
- **No code:** Confirmed — all signal logic in plain English

### Step 8: Handoff Preparation (Skill 9)
- Note: In a real workflow, the Review Agent gate (Skill 8) would precede the programmer handoff
- For demo purposes, prepared handoff draft directly in `handoffs/pending/CRYPTO_DEMO_btc_funding_rate_programmer_handoff.md`
- 20-field implementation spec following handoff protocol

### Step 9: Memory Update (Skill 10 — demo scope)
- This run log serves as the RESEARCH_LOG entry for this demo session
- ALPHA_BACKLOG.md not updated (demo idea is a refinement of existing CRYPTO-001, not a new backlog entry)
- SOURCE_TRACKER.md not updated (no new sources discovered)

---

## LLM Routing Decision

In a production run of this workflow, each step would be routed through the LLM Router (`src/llm/router.py`) to either Claude or DeepSeek based on task type, complexity, and cost sensitivity.

| Workflow Step | Task Type | Route To | Why |
|---------------|-----------|----------|-----|
| Domain Queue Management | CLASSIFICATION | **DeepSeek** | Simple structured lookup; low complexity; cost-sensitive |
| Source Discovery (new web search) | WEB_SOURCE_SCREENING | **DeepSeek** | Screening search results for relevance is low-complexity; DeepSeek suffices for initial triage |
| Paper Analysis (deep reading) | PAPER_ANALYSIS | **Claude** | Requires careful extraction of methodology and findings; high complexity per routing protocol |
| Crypto Market Structure Analysis | RESEARCH_REASONING | **Claude** | Domain expertise + reasoning; high complexity; requires long context for market microstructure knowledge |
| Alpha Discovery Note | ALPHA_IDEA_GENERATION | **Claude** | Core creative research task; high complexity; requires synthesis across multiple sources |
| Memo Writing (19-section) | MEMO_WRITING | **Claude** | Long-form structured output; requires factual precision; Review Agent gate depends on memo quality |
| Quality Control | CLASSIFICATION | **DeepSeek** | Checklist verification is structured and low-complexity; cost-efficient |
| Handoff Preparation | MEMO_WRITING | **Claude** | Implementation spec must be precise and unambiguous; errors propagate to Programmer Agent |
| Memory Update | MEMORY_UPDATE | **DeepSeek** | Structured file updates; low complexity; cost-sensitive per routing protocol |
| Run Log Writing | SUMMARIZATION | **DeepSeek** | Session recording is low-complexity; cost-efficient |

**Key routing rules applied:**
- Claude for all RESEARCH_REASONING, PAPER_ANALYSIS, ALPHA_IDEA_GENERATION, and MEMO_WRITING — these are the high-value research core
- DeepSeek for CLASSIFICATION, WEB_SOURCE_SCREENING, MEMORY_UPDATE, SUMMARIZATION — structured, low-complexity, cost-sensitive
- Code tasks blocked from Claude→DeepSeek fallback (not triggered here — no code in research workflow)
- Review/Risk agent tasks always route to Claude (not triggered here — those agents not active in this demo)

---

## Generated Output Files

| # | File | Description |
|---|------|-------------|
| 1 | `reports/demo_runs/btc_funding_rate_demo_run_log.md` | This file — demo workflow documentation |
| 2 | `research/memos/crypto/CRYPTO_DEMO_btc_funding_rate_crowding_reversal.md` | 19-section research memo |
| 3 | `research/ideas/proposed/crypto/CRYPTO_DEMO_btc_funding_rate_crowding_reversal.md` | Alpha discovery note for Review Agent gate |
| 4 | `handoffs/pending/CRYPTO_DEMO_btc_funding_rate_programmer_handoff.md` | Programmer implementation handoff (20-field spec) |

---

## Current Limitations

### System Limitations
1. **Single-agent execution:** This demo was run by a general-purpose AI, not the dedicated Research Agent. The five-agent architecture (Research, Review, Programmer, Data, Risk) is defined but only the Research Agent has been actively used. The Review, Programmer, Data, and Risk agents are defined in `.claude/agents/` but have not been invoked in practice.
2. **No review gate:** In a real run, the alpha discovery note would be evaluated by the Review Agent before any programmer handoff is written. This demo skips that gate.
3. **No backtest data:** No actual BTC funding rate or spot price data was pulled. All signal parameters (lookback windows, percentile thresholds) are informed by the cited literature but not empirically calibrated or validated.
4. **LLM Router not invoked:** The router infrastructure exists (`src/llm/` with 112 passing tests) but was not called during this demo. The routing decision table above is a design-level recommendation consistent with the routing protocol, not actual routing logs.
5. **No rate limiting or circuit breaker exercised:** Router production features (caching, rate limiting, circuit breaker, usage tracking) are implemented but not triggered in this demo.

### Research Limitations
6. **CEX carry compression:** CRYPTO-001 and the ScienceDirect (2025) source document that CEX funding carry Sharpe ratios have collapsed to near-zero by 2024–2025. The crowding-reversal signal may also have decayed as institutional participants now monitor and trade against the same extremes.
7. **Funding rate caps:** Exchange-imposed caps on funding rates (e.g., 0.375% per 8h on Binance) truncate the signal at the top, making extreme-crowding detection harder — the 90th percentile may be compressed.
8. **Single-asset scope:** BTC-only signal ignores cross-asset information. A multi-asset crowding signal (BTC + ETH + top alts) may produce stronger and more robust signals.

### Demo-Specific Limitations
9. **No new source verification:** All sources are drawn from the existing SOURCE_TRACKER.md registry; no new web search or paper verification was performed for this demo.
10. **No Obsidian vault update:** The knowledge graph (`knowledge/Quant-Research-KB/`) was read but not updated with new notes for this alpha.
11. **No backtest specification validation:** The handoff backtest spec (in-sample/out-of-sample dates, walk-forward design) follows the template but has not been reviewed for feasibility against actual data availability.

---

## Disclaimer

**This is a demo research workflow for interview evidence.** It documents the process and artifacts the system would produce for a real alpha research session. It does not claim:
- Live trading or production deployment
- Real backtest results
- Verified predictive power of the signal
- Financial advice of any kind

All sources cited exist and were verified in prior research sessions. Signal parameters are informed by literature but not empirically validated.

---

*Demo run log authored by: Research Agent (demo mode)*
*Date: 2026-05-19*
*Next: Review Agent gate (not executed in demo)*
