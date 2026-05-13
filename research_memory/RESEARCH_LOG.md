# Research Log

Dated entries for each research session.

---

## 2026-05-14 — Cross-Sectional Altcoin Funding Rate Carry (Memo #03)

**Session type:** Alpha research — second alpha research session of the day

### Alpha Research: Cross-Sectional Altcoin Funding Rate Carry

Researched the #2 priority alpha idea from the backlog. The research agent produced:

**Mechanism synthesized from 7 verified sources:**
- Cross-sectional funding rate dispersion across altcoins is driven by concentrated retail leverage demand in specific "hot" altcoins and structurally constrained arbitrage capital (higher barriers to altcoin arbitrage vs. BTC/ETH: fragmented spot custody, higher volatility, lower liquidity, fewer institutional participants).
- Unlike absolute BTC/ETH funding carry (which has compressed to near-zero Sharpe by 2025), cross-sectional relative-value carry across 20-30 altcoins remains harvestable because: (a) arbitraging each additional altcoin adds linear operational complexity, (b) altcoin perp capacity is severely limited, capping total arbitrage capital, and (c) the alpha source is diversified across multiple independent retail-attention cycles.
- Critical distinction established: absolute funding rate extremes (time-series) predict reversals (crowding/crash signal per BIS paper), while relative funding rate rankings (cross-section) support carry capture (go with high relative funding). The cross-sectional construction is beta-neutral, hedging the directional crash risk that plagues absolute carry.

**Key sources:**
1. Fan, Jiao, Lu, Tong (2024) — Central paper: cross-sectional crypto carry yields 43.4% annualized, Sharpe 0.74 (verified via Memo #01)
2. Schmeling, Schrimpf, Todorov (2023) — BIS WP 1087: crypto carry fundamentals, retail demand + limited arb capital, high carry predicts crashes (verified via WebFetch)
3. Inan (2025) — Funding rate predictability supports carry persistence (verified via Memo #01)
4. Liu, Tsyvinski, Wu (2022) — JoF: cross-sectional momentum is a robust crypto factor; must orthogonalize carry from momentum (verified via Memo #01)
5. ScienceDirect (2025) — CEX carry Sharpe near-zero by 2024-25, DEX carry still 6.5-23.6 (verified via Memo #01)
6. He, Manela, Ross, von Wachter (2022) — No-arbitrage perpetual pricing, cross-currency comovement (verified via WebFetch)
7. Ackerer, Hugonnier, Jermann (2025) — Mathematical Finance: perpetual pricing theory (verified via Memo #01)

**Key questions answered:**
- **Carry capture vs. reversal:** Cross-sectional is carry CAPTURE (go with high relative funding), not reversal. Absolute carry (time-series extremes) predicts crashes; relative carry (cross-sectional ranking) captures persistent spread.
- **Funding rate persistence:** Altcoin funding rates at the cross-sectional level are likely persistent (constrained arb capital, wide spreads, concentrated retail demand). This supports the carry capture direction.
- **Absolute vs. cross-sectional carry:** Absolute carry is delta-neutral per-asset (spot + perp), market-direction-exposed; cross-sectional carry is beta-neutral across assets, market-direction-hedged.
- **Transaction costs:** Tiered by altcoin liquidity: 0.07-0.26% one-way depending on volume bucket. Round-trip 0.14-0.52%. Costs are the #1 failure risk.
- **Scalability:** $5-20M total notional due to altcoin perp liquidity constraints. Small-to-medium capacity.

**Gap identified:** WebSearch tool was non-functional throughout the session (persistent API error "400 deepseek-reasoner does not support this tool_choice"), preventing discovery of additional practitioner sources, blog posts, and institutional reports. The research relied primarily on previously verified academic sources from Memo #01 and direct WebFetch of a limited set of accessible URLs. SSRN, Investopedia, Binance Research, Bybit, and many other sites blocked automated access. Practitioner-sourced information on altcoin perp liquidity tiers and exchange fee schedules is based on researcher domain knowledge rather than newly verified URLs. Future sessions should revisit practitioner sourcing when the WebSearch tool is functional.

### Outputs Created

- `research_memos/crypto/03_cross_sectional_altcoin_funding_carry.md` — Full research memo with 7 verified sources, factor definitions, failure modes, robustness tests
- `handoff_to_programmer/pending/03_cross_sectional_altcoin_funding_carry_handoff.md` — Programmer handoff with backtest spec, edge cases, validation checks
- Updated: PROJECT_STATE.md, ALPHA_BACKLOG.md, SOURCE_TRACKER.md, RESEARCH_LOG.md

### Next Session
- Option 1: Complete Memo #02 (OI-Price Divergence Reversal) — verify data availability and create programmer handoff
- Option 2: Start Memo #04 (DEX venue funding carry — Drift Protocol / ApolloX) — next priority in backlog
- Option 3: Commodity futures research (Memo #06, gold term structure as macro regime signal)

## 2026-05-14 — Real Alpha Research: OI-Price Divergence Reversal (Memo #02)

**Session type:** Alpha research — first real research session

### Vault Cleanup
Removed all placeholder/testing content from the Obsidian vault created on 2026-05-13. Preserved only the 9 templates in `99_Templates/` and the `.obsidian/` configuration. All 13 concept notes and Dashboard were purely scaffolding and were deleted.

### Alpha Research: Open Interest-Price Divergence Reversal

Researched the top-priority alpha idea from the backlog. The research agent produced:

**Mechanism synthesized from 5 verified sources:**
- When OI and price diverge over a 7-day window (price up + OI down = bullish conviction waning; price down + OI up = bearish buildup), the trend lacks structural support and is likely to reverse
- Two reinforcing layers: (1) sentiment — divergence signals waning conviction; (2) structural — falling OI = thinning market depth = larger price impact per unit order flow = higher reversal probability (Bessembinder & Seguin 1993; Matsui et al. 2022)
- Crypto-specific amplifier: liquidation cascades amplify reversals beyond fair value

**Key sources verified:**
1. Giagkiozis & Said (2024) — OI misreporting by major crypto exchanges (critical data quality warning)
2. Matsui, Al-Ali, Knottenbelt (2022) — Negative OI-volatility relationship confirmed for crypto
3. Chen, Ma, Nie (2024) — DEX vs. CEX OI dynamics differ (scope to CLOB CEXs only)
4. Bessembinder & Seguin (1993) — Foundational paper, OI as market depth proxy
5. Practitioner consensus — Four-quadrant OI-price framework (Wikipedia, CryptoSlate, Glassnode)

**Gap identified:** No academic paper directly tests OI-price divergence as a directional signal in crypto perpetuals. The concept is well-known among practitioners but has not been rigorously quantitatively tested. This is both a risk (may be crowded/decayed) and an opportunity (quantitative specification may capture alpha the discretionary crowd leaves on the table).

### Outputs Created

**Obsidian vault (6 notes):**
- `01_Concepts/Open Interest.md` — Core concept note with four-quadrant framework
- `02_Alpha_Ideas/crypto_oi_momentum_reversal.md` — Full alpha idea note (status: needs_data_check)
- `05_Paper_Notes/paper_giagkiozis_2024_oi_reconciliation_perps.md`
- `05_Paper_Notes/paper_matsui_2022_dynamics_gold_futures.md`
- `05_Paper_Notes/paper_chen_2024_dex_design_perpetual_futures.md`
- `06_Data_Source_Notes/coinglass_aggregated_derivatives.md`
- `07_Risk_Failure_Modes/oi_data_quality_misreporting.md`

**Project files:**
- `research_memos/crypto/02_oi_momentum_reversal.md` — Formal research memo
- Updated: PROJECT_STATE.md, ALPHA_BACKLOG.md, SOURCE_TRACKER.md, RESEARCH_LOG.md

### Next Session
- Verify data availability for CoinGlass/Binance OI (move from needs_data_check to ready_for_backtest)
- Create Backtest Request and Programmer Handoff notes in vault
- Optionally: start research on Memo #03 (cross-sectional altcoin funding carry)

## 2026-05-13 — Obsidian Integration Design

**Session type:** Architecture & design

Designed the complete Obsidian integration for the Quant Research Agent. The design covers:

1. **Vault Structure** — 13-folder Obsidian vault (`Quant-Research-KB/`) with clear pipeline from Inbox to Alpha Ideas to Programmer Handoffs to Rejected/Deprecated
2. **Markdown Templates** — 9 Obsidian-compatible templates with YAML frontmatter, tags, and `[[wikilinks]]` for alpha ideas, strategy hypotheses, paper notes, market regimes, risk/failure modes, backtest requests, programmer handoffs, research reviews, and rejected ideas
3. **Write Workflow** — Specified when to create vs. update notes, file naming conventions, tag taxonomy, backlink conventions, duplicate detection, and code-prevention rules
4. **Retrieval Workflow** — Defined search priority, tag-based retrieval, backlink traversal, staleness detection, relevance ranking, duplicate detection, and assumption-vs-current-condition evaluation
5. **Alpha Idea Lifecycle** — 9-status lifecycle (idea → researching → needs_data_check → ready_for_backtest → waiting_for_programmer → in_backtest → validated | rejected | deprecated) with clear ownership boundaries between Research Agent and Programmer Agent
6. **Programmer Handoff Format** — Structured handoff with 20 required fields, plain-English-only logic, explicit exclusion list, and pseudocode policy
7. **Agent Policy** — 8-section operating policy covering code prohibition, trading prohibition, performance claims prohibition, documentation requirements, Obsidian discipline, handoff responsibility, source integrity, and research integrity

Key design decisions recorded in DECISIONS.md.

## 2026-05-12 — Project Initialization

**Session type:** Infrastructure setup

Created the Quant Alpha Research project structure:
- Root documentation: CLAUDE.md, README.md
- Agent definition: quant-alpha-researcher
- Memory files: PROJECT_STATE, ALPHA_BACKLOG, RESEARCH_LOG, SOURCE_TRACKER, DECISIONS
- Templates: alpha research memo, programmer handoff
- Directory structure: research_memos (crypto, commodities, cross_market), handoff_to_programmer (pending, completed)

**Prior session work (memo #01):** Crypto Funding Rate Carry and Crowding Signal memo written. Covers delta-neutral carry, crowding reversal signal, and dynamic carry scaling. Eight verified sources. Full factor definitions, data requirements, backtest design, failure modes, evaluation metrics, robustness tests. Handed off to programmer agent.

**Next session:** Start Memo #02 — Open Interest Momentum Reversal.
