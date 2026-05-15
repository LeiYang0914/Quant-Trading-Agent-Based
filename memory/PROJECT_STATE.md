# Project State

**Last updated:** 2026-05-16

## Current Default Research Domain

**crypto** — Commodities research is separate and should only begin after current crypto priorities are complete or when explicitly requested.

## Domain Priority Order

1. **crypto** — active, process first
2. **commodities** — separate domain, begin after crypto priorities complete
3. **cross_market** — only when explicitly requested

## Current Status

Project is active. Three crypto research memos exist:
- `research/memos/crypto/01_crypto_funding_rate_carry.md` — CRYPTO-001: Funding Rate Carry and Crowding Signal (complete, handed off)
- `research/memos/crypto/02_oi_momentum_reversal.md` — CRYPTO-002: OI-Price Divergence Reversal Signal (in progress, needs_data_check)
- `research/memos/crypto/03_cross_sectional_altcoin_funding_carry.md` — CRYPTO-003: Cross-Sectional Altcoin Funding Rate Carry (complete, handed off)

**Obsidian vault:** `knowledge/Quant-Research-KB/` — registered in Obsidian, active.

## System Architecture

Five-agent Quant Trading AI System:

| Agent | Purpose | Status |
|-------|---------|--------|
| Research Agent | Alpha discovery, memos, handoffs — crypto-first domain separation | Active (upgraded 2026-05-15) |
| Review Agent | Gate between research and programming | Defined, not yet active |
| Programmer Agent | Implement approved ideas, run backtests | Defined, not yet active |
| Data Agent | Data sourcing, quality, execution simulation | Defined, not yet active |
| Risk Agent | Final risk gate, position sizing, kill switches | Defined, not yet active |

## Active Research

| Alpha ID | Title | Domain | Status | Since |
|----------|-------|--------|--------|-------|
| CRYPTO-002 | OI-Price Divergence Reversal | Crypto | ready_for_review | 2026-05-16 |

## Completed Memos

| Alpha ID | Title | File | Domain | Status |
|----------|-------|------|--------|--------|
| CRYPTO-001 | Funding Rate Carry and Crowding Signal | research/memos/crypto/01_crypto_funding_rate_carry.md | Crypto | Complete, handed off |
| CRYPTO-003 | Cross-Sectional Altcoin Funding Rate Carry | research/memos/crypto/03_cross_sectional_altcoin_funding_carry.md | Crypto | Complete, handed off |

## In-Progress Memos

| Alpha ID | Title | File | Domain | Status |
|----------|-------|------|--------|--------|
| CRYPTO-002 | OI-Price Divergence Reversal | research/memos/crypto/02_oi_momentum_reversal.md | Crypto | ready_for_review |

## Next Priorities

1. **CRYPTO-002:** Ready for Review Agent — evaluate data availability, OI quality, and edge persistence. After approval, prepare programmer handoff.
2. **CRYPTO-004:** DEX venue funding carry (Drift / ApolloX) — next new research
3. **CRYPTO-005:** Stablecoin mint/burn flows — after DEX carry
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

- 2026-05-16 (session 4): **CRYPTO-002 upgraded to ready_for_review.** Ran full 9-skill sequence on CRYPTO-002. Created alpha discovery note (was missing). Updated memo to 19-section template. Wrote 4 paper summaries. Ran 20-item QC (all pass). Moved from needs_data_check to ready_for_review. Created Research Agent skills layer (10 skills + README) as system infrastructure.
- 2026-05-15 (session 3): **Research Agent skills layer.** Created 10 modular skills: domain queue management, source discovery, paper analysis, crypto/commodities market structure, alpha discovery, memo writing, quality control, handoff prep, memory update. Master README index. Updated agent definitions, system specs, research protocol, SYSTEM_MAP.
- 2026-05-15 (session 2): **Research Agent upgrade.** Added strict crypto/commodities domain separation, source quality tiers, alpha ID standard (CRYPTO-NNN, COMMOD-NNN, CROSS-NNN), research protocol with 10-step workflow, quality gates before ready_for_review, structured reference tracking in SOURCE_TRACKER.md, new templates (paper_summary, alpha_discovery_note, research_session_log), domain-grouped ALPHA_BACKLOG.md, and crypto-first research order. Created domain-specific subdirectories under research/ideas/.
- 2026-05-15 (session 1): **Major refactoring.** Restructured repo from research workspace to five-agent Quant Trading AI System. Created agent definitions, specs, system docs, workflows, protocols.
- 2026-05-14: Cleaned placeholder content from Obsidian vault. Researched OI-Price Divergence alpha with 5 verified sources. Completed Cross-Sectional Altcoin Funding Rate Carry (Memo #03) with programmer handoff.
- 2026-05-13: Obsidian vault created, registered, configured.
- 2026-05-12: Project structure created. Memo #01 written and handed off.
