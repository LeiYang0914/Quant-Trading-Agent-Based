# Alpha Research Memo: OI-Price Divergence Reversal

**Alpha ID:** CRYPTO-002
**Domain:** crypto
**Date:** 2026-05-16
**Status:** ready_for_review
**Priority:** high

---

## 1. Title

OI-Price Divergence Reversal — using directional divergence between perpetual futures open interest and spot price as a short-term reversal signal in BTC and ETH.

## 2. Market & Instrument

- **Market:** crypto
- **Asset universe:** BTC, ETH (initial test only; extension to top-10 altcoins after validation)
- **Instrument type:** perpetual futures (inverse or linear)
- **Venues:** CLOB CEXs only — Binance, Bybit, OKX. DEX perpetuals excluded due to different OI mechanics (Chen, Ma, Nie 2024).

## 3. One-Sentence Hypothesis

> When the 7-day change in perpetual futures OI and the 7-day change in spot price have opposite signs, and the divergence magnitude exceeds a threshold normalized by 30-day historical volatility, price will revert toward the OI-implied direction over the subsequent 1-7 days. Signal strength increases when OI is at extreme absolute levels and when funding rates are not already at extremes in the signal direction.

## 4. Economic Rationale

Open interest (OI) measures the total number of outstanding futures contracts. Changes in OI reflect capital flows into or out of directional positions:

- **Rising OI** = new positions opened = fresh capital committing = trend has structural support
- **Falling OI** = positions closed = capital exiting = trend losing foundation

When price moves in one direction but OI moves in the opposite direction (divergence), the price move is not supported by new capital. Existing participants are exiting rather than reinforcing the trend. This creates a structurally fragile price level with two reinforcing layers:

**Layer 1 — Sentiment:** Divergence signals that conviction behind the trend is waning. Participants who drove the move are taking profits or cutting losses, reducing the probability of continuation.

**Layer 2 — Structural (market depth):** Falling OI means thinning market depth. Bessembinder & Seguin (1993) established OI as a proxy for market depth — higher OI = deeper market = less price impact per unit of order flow. Matsui et al. (2022) confirmed this relationship holds for crypto futures. When depth thins (falling OI), each unit of order flow produces larger price impact, making overshooting and reversal more likely.

**Crypto-specific amplifier:** In perpetual futures, high-OI environments with one-sided positioning create liquidation cascade risk. Cross-margin mechanics mean losses in one position can trigger liquidations across correlated positions, amplifying any initial reversal beyond what pure mean reversion would predict.

## 5. Behavioral or Structural Source of Edge

The edge is primarily **structural**, reinforced by a behavioral component:

**Structural persistence:**
1. **OI data requires active monitoring.** Most traders focus on price action. OI requires cross-referencing a second data stream. This attention asymmetry creates a systematic underweighting of OI information.
2. **Quantification gap.** The four-quadrant OI-price framework is textbook practitioner knowledge, but few market participants specify it quantitatively with precise entry/exit thresholds, lookback windows, and position sizing.
3. **Crypto-specific arbitrage constraints.** Unlike BTC/ETH funding rate arbitrage (which has compressed as institutional capital entered), trading OI divergence requires taking directional risk and tolerating drawdowns during trend regimes — reducing arbitrageur participation.

**Behavioral reinforcement:**
- Retail traders tend to increase positions in trending markets, inflating OI near local tops and bottoms. This behavioral pattern means extreme OI levels themselves are contrarian signals.
- Less informed traders overreact to positive news by adding long positions (Chen, Ma, Nie 2024), creating the OI extreme that the reversal signal exploits.

## 6. Source Inspiration

### Primary Sources (Tier 1)

**Reference ID:** CRYPTO-PAPER-008
**Title:** Reconciling Open Interest with Traded Volume in Perpetual Swaps
**Authors:** Giagkiozis, Ioannis and Said, Emilio
**Year:** 2024
**Venue / Publisher:** Ledger, Volume 9
**DOI / arXiv / SSRN:** arXiv:2310.14973
**URL:** https://arxiv.org/abs/2310.14973
**Relevance to alpha:** Documents systematic OI misreporting by major crypto exchanges. Provides data quality framework (cross-check OI changes against volume). Informs the recommendation to use Binance or CoinGlass aggregated OI with quality filtering.

---

**Reference ID:** CRYPTO-PAPER-009
**Title:** On the Dynamics of Solid, Liquid and Digital Gold Futures
**Authors:** Matsui, Toshiko; Al-Ali, Ali; Knottenbelt, William J.
**Year:** 2022
**Venue / Publisher:** IEEE ICBC 2022
**DOI / arXiv / SSRN:** arXiv:2202.09845
**URL:** https://arxiv.org/abs/2202.09845
**Relevance to alpha:** Confirms the negative OI-volatility relationship extends to crypto futures (CME Bitcoin). Provides the structural mechanism for why falling OI makes prices more vulnerable to reversal: thinning depth amplifies order flow impact.

---

**Reference ID:** CRYPTO-PAPER-010
**Title:** Exploring the Impact: How Decentralized Exchange Designs Shape Traders' Behavior on Perpetual Future Contracts
**Authors:** Chen, Erdong; Ma, Mengzhong; Nie, Zixin
**Year:** 2024
**Venue / Publisher:** arXiv preprint
**DOI / arXiv / SSRN:** arXiv:2402.03953
**URL:** https://arxiv.org/abs/2402.03953
**Relevance to alpha:** Shows OI dynamics differ between CEX (CLOB) and DEX (VAMM/Oracle) perpetuals. Scopes CRYPTO-002 to CLOB CEXs where OI signals are symmetric and interpretable.

---

**Reference ID:** CRYPTO-PAPER-011
**Title:** Price Volatility, Trading Volume, and Market Depth: Evidence from Futures Markets
**Authors:** Bessembinder, Hendrik and Seguin, Paul J.
**Year:** 1993
**Venue / Publisher:** Journal of Financial and Quantitative Analysis, Vol. 28, No. 1
**DOI / arXiv / SSRN:** — (JSTOR)
**URL:** https://www.jstor.org/stable/2331234
**Relevance to alpha:** Foundational paper establishing OI as a proxy for market depth. Establishes the negative OI-volatility relationship that underpins the entire OI-price divergence mechanism.

---

### Supplementary Sources (Tier 3)

**Reference ID:** CRYPTO-PRACT-001
**Title:** Wikipedia — Open Interest (four-quadrant framework)
**URL:** https://en.wikipedia.org/wiki/Open_interest
**Relevance to alpha:** Documents the practitioner four-quadrant framework (Price Up/Down × OI Up/Down) that this alpha quantifies.

---

**Reference ID:** CRYPTO-PRACT-005
**Title:** Glassnode Insights — Market Pulse
**URL:** https://insights.glassnode.com/
**Relevance to alpha:** Additional practitioner confirmation that OI-price divergence is monitored by institutional crypto analysts.

## 7. Required Data

| Dataset | Fields | Frequency | Vendor Options | Min Coverage | Known Issues |
|---------|--------|-----------|----------------|--------------|--------------|
| BTC/ETH perpetual OI | Open interest (USD, contracts) | Daily EOD | Binance API, CoinGlass, Coinalyze | 3 years | Exchange misreporting (Giagkiozis & Said 2024) |
| BTC/ETH spot price | OHLCV | Daily | Binance API | 3 years | Standard |
| 8h funding rate | Rate per 8h interval | 8h → daily mean | Binance API, CoinGlass | 3 years | Gaps during exchange downtime |
| Futures expiry calendar | Quarterly/monthly expiry dates | Static | Exchange docs | Current year | Standard |

**Data source candidates:**
- **Primary:** Binance API (free, best data quality per Giagkiozis & Said 2024) — REST endpoint for OI, WebSocket for real-time
- **Secondary:** CoinGlass aggregated OI (multi-exchange, free tier available, paid API for history)
- **Data quality filter:** Cross-check OI changes against cumulative traded volume. Discard periods where ΔOI and net traded volume diverge by >20%.

## 8. Signal Construction (Plain English Only)

**Raw input:** Daily OI (BTC/USD terms), daily spot close price, 8h funding rate (daily average).

**Lookback window:** 7 days for OI change and price change. 30 days for volatility normalization.

**Transformation:**
1. Compute 7-day percentage change in OI: `ΔOI_7d = (OI_today - OI_7d_ago) / OI_7d_ago`
2. Compute 7-day percentage change in spot price: `ΔPrice_7d = (Price_today - Price_7d_ago) / Price_7d_ago`
3. Compute divergence score: `DivScore = sign(ΔPrice_7d) × sign(ΔOI_7d)`. Negative score = divergence.
4. Compute divergence magnitude: `DivMag = |ΔPrice_7d - ΔOI_7d|` (how far apart the two changes are).
5. Normalize: `NormDiv = DivMag / σ_30d(returns)` where σ_30d is the 30-day rolling standard deviation of daily price returns.

**Entry condition:** Enter when ALL of:
- DivScore < 0 (divergence present)
- NormDiv > 1.5 (divergence is significant relative to recent volatility)
- Funding rate is NOT in top/bottom decile of 30-day range (avoid catching extremes that would reverse anyway)
- Position is not within 3 days of quarterly expiry (avoid expiry-driven OI changes)

**Exit condition:** Exit when ANY of:
- Holding period reaches N days (sweep N = 1, 2, 3, 5, 7 in backtest)
- OI and price re-align (same direction) for 2 consecutive days
- Stop-loss hit at 2 × ATR(14) from entry

**Position size:** 1% risk per trade. Position size = (1% of capital) / (ATR × contract multiplier). Max 3 concurrent positions across BTC and ETH.

**Signal frequency:** Daily, evaluated at 00:00 UTC.

**Expected holding period:** 1-7 days, with most signals expected to resolve in 2-5 days.

## 9. Portfolio Construction Idea

- **Rebalance frequency:** Daily (signal check at 00:00 UTC)
- **Position sizing:** Risk-parity across BTC and ETH signals (equal risk allocation per trade)
- **Leverage:** None (fully cash-funded positions)
- **Max position:** 3 concurrent positions across both assets
- **Universe filtering:** Exclude during 3-day expiry windows. Exclude if OI data quality flag is triggered (ΔOI vs volume divergence >20%).

## 10. Transaction Cost Sensitivity

| Cost Item | Estimate | Impact on Signal |
|-----------|----------|------------------|
| Taker fee | 0.04% per trade (Binance) | Round-trip 0.08%. At expected 2-5 day hold, ~0.08% per signal. Target gross return per signal must exceed 0.24% (3× cost buffer). |
| Slippage | 0.01-0.03% (BTC), 0.03-0.08% (ETH) | Slippage on reversal entry could be significant. At 2× baseline: 0.02-0.06% BTC, 0.06-0.16% ETH. |
| Funding cost | Variable, 0.001-0.01% per 8h | Over 2-5 day hold: 0.006-0.15%. Direction of position relative to funding direction matters. |

**Total round-trip cost estimate (mean scenario):** 0.15-0.35% per signal. The alpha must generate >1% gross return per signal to be viable after costs.

## 11. Liquidity Constraints

- **Capacity estimate:** ~$50M for BTC, ~$20M for ETH before exceeding 5% market impact per order
- **Liquidity bottleneck:** ETH leg in volatile conditions; altcoin extension would be severely constrained
- **Scalability assessment:** Medium for BTC/ETH only. Small if extended to altcoins (top-10 alts add ~$10-20M total capacity)
- **Slippage during cascades:** In liquidation events, slippage can exceed 10x normal. Position sizing must account for tail risk

## 12. Known Risks

1. **OI data quality (severity: high).** Giagkiozis & Said (2024) document systematic OI misreporting. False signals from bad data are the primary risk. Mitigation: data quality filter (cross-check OI vs volume), Binance-only as primary source.
2. **Regime dependence (severity: high).** Signal likely performs differently in trending vs. range-bound markets. In strong trends, OI-price divergence can persist (price up + OI up = trend has support) and the signal generates many false reversal entries. Mitigation: conditional on trend strength indicator.
3. **Crowding (severity: medium).** The four-quadrant framework is widely known. Quantitative specification may preserve edge, but crowding risk increases with strategy AUM. Mitigation: inversely scale position sizes with total OI extremes.
4. **Expiry contamination (severity: medium).** OI changes during roll periods are mechanical (positions moving from front to next month) and generate false divergence. Mitigation: calendar filter.
5. **Structural change (severity: medium).** Crypto market structure evolves rapidly (post-FTX, ETF approvals, institutional entry). Historical OI relationships may not persist. Mitigation: rolling window estimation and regime detection.

## 13. Failure Modes

| Failure Mode | Severity | Trigger | Mitigation |
|-------------|----------|---------|------------|
| OI data misreporting generates false signals | High | ΔOI diverges from cumulative volume by >20% | Use Binance-only or CoinGlass reconciled OI; apply data quality filter; discard periods with bad data |
| Signal is redundant with price momentum reversal | Medium | OI-enhanced signal has no higher Sharpe than pure price reversal | Must include control test in backtest; if no improvement, reject the alpha |
| Expiry-driven OI changes cause false readings | Medium | Signal clusters on quarterly expiry dates | Calendar filter: no entry within 3 days of quarterly/monthly expiry |
| Signal fails in trending regimes | High | Hit rate falls below 40% during strong trends | Conditional signal: only trade when 30-day trend strength is below threshold |
| Slippage consumes edge at scale | Medium | Average slippage > 2× baseline estimate | Conservative slippage assumptions in backtest; scale limit based on liquidity |
| Regime shift collapses OI-price relationship | High | Post-2021 structural changes invalidate the relationship | Rolling window estimation; out-of-sample validation by year |

## 14. Data Quality Concerns

1. **Exchange OI misreporting:** Giagkiozis & Said (2024) found that some exchanges report "wholly implausible" OI levels. Mitigation: Binance had better reporting quality in the study; use Binance as primary source.
2. **OI vs. volume reconciliation:** The same paper shows that OI changes should be cross-checked against cumulative traded volume. Periods where these diverge indicate data quality issues. Implement as a real-time data quality filter.
3. **CoinGlass aggregation methodology:** CoinGlass aggregates OI across exchanges but the aggregation methodology is not fully documented. Use Binance standalone as primary, CoinGlass aggregated as cross-check.
4. **Historical OI data depth:** Binance perpetual futures launched in 2019 but historical OI data availability depends on API rate limits and data retention. Minimum 3 years required for meaningful backtest.

## 15. Similar Existing Ideas

| Idea | Domain | Similarity | Distinct? |
|------|--------|------------|-----------|
| OI-price four-quadrant framework | All futures | High (same concept) | Yes — this alpha adds quantitative thresholds, lookback windows, normalization, and position sizing. The framework is qualitative; this alpha is quantitative. |
| Volume-price divergence | Equity / Crypto | Medium (substitute signal) | Yes — OI measures capital commitment (stock), volume measures flow (rate). They are complementary, not interchangeable. |
| Funding rate reversal (CRYPTO-001) | Crypto | Low (different signal) | Yes — funding rate is a cost-of-carry signal; OI is a market depth signal. Different mechanism, different holding period, different entry conditions. |
| COT positioning (Commodities) | Commodities | Low (conceptual) | Yes — CFTC COT is weekly, regulated, institutional. Crypto OI is real-time, unregulated, retail-dominated. Different data structure and interpretation. |

## 16. Research Confidence

| Dimension | Rating (1-10) | Notes |
|-----------|---------------|-------|
| Economic intuition | 8 | Well-established in traditional futures; two-layer mechanism (sentiment + structural depth) is sound |
| Source quality | 8 | 4 Tier 1 papers, all verified; practitioner sources document real-world usage |
| Data availability | 6 | OI data exists but quality concerns (misreporting, aggregation methodology) reduce confidence |
| Signal clarity | 9 | Unambiguous construction: two inputs (OI change, price change), simple transformation, clear entry/exit rules |
| Failure mode coverage | 8 | 6 failure modes documented with severity, trigger, and mitigation |
| Novelty | 5 | Core concept is textbook; novelty is in quantitative specification and crypto-specific calibration |

**Overall confidence:** Medium-high concept confidence. Data quality is the primary uncertainty. The signal is simple and well-founded, but OI data reliability and regime dependence need empirical validation before transitioning beyond researching status.

## 17. Handoff Readiness

- [x] References complete (5 sources, 4 Tier 1 papers + practitioner)
- [x] Data requirements specified (vendors, fields, frequency, coverage, known issues)
- [x] Signal construction clear (plain English, step-by-step, unambiguous)
- [x] Failure modes documented (6 modes with severity, trigger, mitigation)
- [ ] Data availability verified (needs check — OI data availability confirmed, but quality filter needs implementation)
- [ ] Review gate passed

## 18. Open Questions

1. **Can CoinGlass aggregated OI data be obtained with 3+ years of history?** The free tier shows current data; the paid API may provide historical data. If not, Binance API alone covers 2019+ for BTC and ETH — sufficient for initial testing.
2. **What is the optimal divergence threshold (1σ, 1.5σ, 2σ)?** Must be determined through walk-forward optimization. The theoretical argument favors 1.5σ as the minimum for meaningful divergence without being too restrictive.
3. **Does the signal add marginal predictive power over simple price momentum reversal?** This is the critical control test. If the OI-enhanced version does not outperform price-only reversal, the alpha should be rejected regardless of standalone performance.
4. **How does the signal behave in altcoin markets where OI data quality is worse?** Altcoin extension is a future direction, but the data quality issues documented by Giagkiozis & Said (2024) may be more severe for smaller assets.
5. **What is the actual capacity for the ETH leg in volatile conditions?** ETH perpetuals have thinner order books than BTC. Slippage estimates should be stress-tested with historical liquidation event data.

## 19. References (Structured)

| Ref ID | Title | Authors | Year | Venue | DOI/arXiv/SSRN | URL | Relevance |
|--------|-------|---------|------|-------|----------------|-----|-----------|
| CRYPTO-PAPER-008 | Reconciling OI with Traded Volume in Perpetual Swaps | Giagkiozis & Said | 2024 | Ledger, Vol. 9 | arXiv:2310.14973 | https://arxiv.org/abs/2310.14973 | OI data quality warning; quality filter design |
| CRYPTO-PAPER-009 | Dynamics of Solid, Liquid and Digital Gold Futures | Matsui, Al-Ali, Knottenbelt | 2022 | IEEE ICBC 2022 | arXiv:2202.09845 | https://arxiv.org/abs/2202.09845 | Confirms OI-volatility relationship for crypto |
| CRYPTO-PAPER-010 | DEX Designs and Trader Behavior on Perps | Chen, Ma, Nie | 2024 | arXiv preprint | arXiv:2402.03953 | https://arxiv.org/abs/2402.03953 | Scopes alpha to CLOB CEXs |
| CRYPTO-PAPER-011 | Price Volatility, Volume, and Market Depth | Bessembinder & Seguin | 1993 | JFQA, Vol. 28 | — | https://www.jstor.org/stable/2331234 | Foundation: OI as market depth proxy |
| CRYPTO-PRACT-001 | Open Interest (Wikipedia) | — | — | Encyclopedia | — | https://en.wikipedia.org/wiki/Open_interest | Four-quadrant framework documentation |
| CRYPTO-PRACT-005 | Glassnode Market Pulse | Glassnode | — | Institutional Research | — | https://insights.glassnode.com/ | Practitioner OI monitoring |

---

*Memo authored by: Research Agent*
*Domain: crypto*
*Next: Review Agent gate (after data availability check complete)*
