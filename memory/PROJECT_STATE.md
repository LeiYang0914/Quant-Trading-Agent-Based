# Project State

**Last updated:** 2026-05-20 (session 9)

## Current Default Research Domain

**crypto** — Commodities research is separate and should only begin after current crypto priorities are complete or when explicitly requested.

## Domain Priority Order

1. **crypto** — active, process first
2. **commodities** — separate domain, begin after crypto priorities complete
3. **cross_market** — only when explicitly requested

## Current Status

Project is active. Three crypto research memos exist:
- `research/memos/crypto/01_crypto_funding_rate_carry.md` — CRYPTO-001: Funding Rate Carry and Crowding Signal (complete, handed off)
- `research/memos/crypto/02_oi_momentum_reversal.md` — CRYPTO-002: OI-Price Divergence Reversal Signal (conditional pass, handed off)
- `research/memos/crypto/03_cross_sectional_altcoin_funding_carry.md` — CRYPTO-003: Cross-Sectional Altcoin Funding Rate Carry (complete, handed off)

**Obsidian vault:** `knowledge/Quant-Research-KB/` — registered in Obsidian, active.

## System Architecture

Five-agent Quant Trading AI System with shared LLM Router infrastructure:

| Agent | Purpose | Status |
|-------|---------|--------|
| Research Agent | Alpha discovery, memos, handoffs — crypto-first domain separation | Active (upgraded 2026-05-15) |
| Review Agent | Gate between research and programming | Active (reviewed CRYPTO-002 2026-05-20) |
| Programmer Agent | Implement approved ideas, run backtests | Defined, not yet active |
| Data Agent | Data sourcing, quality, execution simulation | Defined, not yet active |
| Risk Agent | Final risk gate, position sizing, kill switches | Defined, not yet active |
| **LLM Router** | **Infrastructure: routes agent tasks to Claude or DeepSeek** | **Implemented 2026-05-17** |

## Active Research

| Alpha ID | Title | Domain | Status | Since |
|----------|-------|--------|--------|-------|
| CRYPTO-004 | DEX Venue Funding Carry | Crypto | ready_for_review | 2026-05-20 |

## Completed Memos

| Alpha ID | Title | File | Domain | Status |
|----------|-------|------|--------|--------|
| CRYPTO-001 | Funding Rate Carry and Crowding Signal | research/memos/crypto/01_crypto_funding_rate_carry.md | Crypto | Complete, handed off |
| CRYPTO-003 | Cross-Sectional Altcoin Funding Rate Carry | research/memos/crypto/03_cross_sectional_altcoin_funding_carry.md | Crypto | Complete, handed off |
| CRYPTO-004 | DEX Venue Funding Carry | research/memos/crypto/04_dex_venue_funding_carry.md | Crypto | Memo complete, awaiting Review Agent |

## Handoffs Pending

| Alpha ID | Title | File | Conditions |
|----------|-------|------|------------|
| CRYPTO-002 | OI-Price Divergence Reversal | `handoffs/pending/CRYPTO-002_oi_divergence_reversal.md` | 5 mandatory validation conditions |

## In-Progress Memos

| Alpha ID | Title | File | Status |
|----------|-------|------|--------|
| CRYPTO-004 | DEX Venue Funding Carry | research/memos/crypto/04_dex_venue_funding_carry.md | Research complete; awaiting Review Agent gate |

## Next Priorities

1. **Review Agent:** Evaluate CRYPTO-004 (DEX venue funding carry — memo at `research/memos/crypto/04_dex_venue_funding_carry.md`)
2. **Data Agent:** Confirm DEX funding rate history availability for Drift, Hyperliquid, ApolloX (on-chain indexing via Dune/Flipside/The Graph)
3. **CRYPTO-005:** Stablecoin mint/burn flows — next new research (after CRYPTO-004 review)
4. *(Only after crypto backlog is clear)* → **COMMOD-001:** Gold futures term structure as macro regime signal

## Vault Contents

`knowledge/Quant-Research-KB/`:
- `99_Templates/` — 9 Obsidian templates
- `01_Concepts/` — 2 concept notes
- `02_Alpha_Ideas/` — 2 alpha idea notes
- `05_Paper_Notes/` — 5 paper notes
- `06_Data_Source_Notes/` — 1 data source note
- `07_Risk_Failure_Modes/` — 1 risk note
- `09_Programmer_Handoffs/` — 1 handoff note
- `Dashboard.md` — Map of Content

## Blockers

None currently.

## Recent Changes

- 2026-05-20 (session 9): **CRYPTO-004 DEX Venue Funding Carry research complete.** Full 9-skill sequence executed. Alpha discovery note at `research/ideas/proposed/crypto/CRYPTO-004_dex_funding_carry.md`, memo at `research/memos/crypto/04_dex_venue_funding_carry.md`. Identified 5 structural drivers of DEX carry premium (capital pool fragmentation, vAMM inventory effects, lazy settlement, execution friction, Rebate Pool capping). Documented 10 sources (6 Tier 1, 4 Tier 2), 8 failure modes, 8 open questions. All 20 QC checks PASS. Marked ready_for_review. Defined 6 falsification conditions. WebSearch non-functional (deepseek-reasoner error). ScienceDirect (2025) paper remains paywalled and findings are second-hand from CRYPTO-001. Data availability for DEX funding rate history requires Data Agent verification. Next: Review Agent evaluation.
- 2026-05-20 (session 8): **CRYPTO-002 programmer handoff.** Created programmer handoff document with 5 mandatory conditions from review embedded as validation checks. Handoff at `handoffs/pending/CRYPTO-002_oi_divergence_reversal.md`. Backlog updated to `handed off`. Project state, alpha backlog, decisions log updated. Next: CRYPTO-004 research or Programmer Agent implementation.
- 2026-05-20 (session 7): **CRYPTO-002 Review Agent gate.** Review Agent evaluated CRYPTO-002 (OI-Price Divergence Reversal). Verdict: CONDITIONAL PASS with 5 mandatory implementation conditions (control test vs price-only reversal, data quality filter, parameter sensitivity, regime-conditional performance, out-of-sample validation). Review report at `research/ideas/reviewed/CRYPTO-002_review.md`. No lookahead bias found. Low overlap with CRYPTO-001 and CRYPTO-003. Backlog and project state updated. Ready for programmer handoff with conditions attached.
- 2026-05-17 (session 6): **LLM Router production upgrade.** Upgraded router from skeleton to production-style with: real Anthropic/OpenAI SDK wiring with graceful degradation, response caching with file-based JSON index, sliding-window rate limiting per provider, circuit breaker (CLOSED→OPEN→HALF_OPEN→CLOSED), usage/cost tracking with JSONL logging, improved task classification (MEMO_WRITING, RISK_REVIEW, domain hints), `router.ask()` convenience API with auto-classification, `router.health_check()` returning structured per-provider status, `router.get_usage_summary()` for cost analytics, CLI tool (`scripts/llm_router_cli.py`), and config improvements (task-model overrides, rate limits, circuit breaker params). Added 59 new tests across 5 test files (cache, rate limiter, circuit breaker, usage tracker, router advanced). All 112 tests passing. Updated architecture docs, protocol docs, and SYSTEM_MAP. No core trading logic modified.
- 2026-05-17 (session 5): **LLM Router infrastructure layer.** Added full LLM Router architecture under `src/llm/`. Created provider abstraction (ClaudeProvider, DeepSeekProvider), routing rules with task-type-based routing, fallback logic, structured logging, and cost estimation. Added `configs/llm/models.yaml` and `routing_rules.yaml`. Created `tests/llm/` with 46 tests (all passing). Added architecture doc (`system/architecture/llm_router_design.md`), protocol doc (`system/protocols/llm_routing_protocol.md`), and two templates. Updated all 5 agent specs with LLM Router usage tables. Updated `system/architecture/system_overview.md` with Router layer. No core trading logic modified.
- 2026-05-16 (session 4): **CRYPTO-002 upgraded to ready_for_review.** Ran full 9-skill sequence on CRYPTO-002. Created alpha discovery note (was missing). Updated memo to 19-section template. Wrote 4 paper summaries. Ran 20-item QC (all pass). Moved from needs_data_check to ready_for_review. Created Research Agent skills layer (10 skills + README) as system infrastructure.
- 2026-05-15 (session 3): **Research Agent skills layer.** Created 10 modular skills: domain queue management, source discovery, paper analysis, crypto/commodities market structure, alpha discovery, memo writing, quality control, handoff prep, memory update. Master README index. Updated agent definitions, system specs, research protocol, SYSTEM_MAP.
- 2026-05-15 (session 2): **Research Agent upgrade.** Added strict crypto/commodities domain separation, source quality tiers, alpha ID standard (CRYPTO-NNN, COMMOD-NNN, CROSS-NNN), research protocol with 10-step workflow, quality gates before ready_for_review, structured reference tracking in SOURCE_TRACKER.md, new templates (paper_summary, alpha_discovery_note, research_session_log), domain-grouped ALPHA_BACKLOG.md, and crypto-first research order. Created domain-specific subdirectories under research/ideas/.
- 2026-05-15 (session 1): **Major refactoring.** Restructured repo from research workspace to five-agent Quant Trading AI System. Created agent definitions, specs, system docs, workflows, protocols.
- 2026-05-14: Cleaned placeholder content from Obsidian vault. Researched OI-Price Divergence alpha with 5 verified sources. Completed Cross-Sectional Altcoin Funding Rate Carry (Memo #03) with programmer handoff.
- 2026-05-13: Obsidian vault created, registered, configured.
- 2026-05-12: Project structure created. Memo #01 written and handed off.
