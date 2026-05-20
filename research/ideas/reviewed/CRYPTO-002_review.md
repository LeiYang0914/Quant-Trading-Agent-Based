# Review Report -- OI-Price Divergence Reversal

**Review Agent**
**Date:** 2026-05-20
**Idea ID:** CRYPTO-002
**Source Idea Note:** `research/ideas/proposed/crypto/CRYPTO-002_oi_price_divergence.md`
**Source Research Memo:** `research/memos/crypto/02_oi_momentum_reversal.md`

---

## Decision

**CONDITIONAL PASS** -- Approved with five mandatory implementation conditions.

The economic mechanism is sound, data exists (with documented quality caveats), no lookahead bias was detected, overfitting risk is manageable, and the idea is genuinely distinct from all existing approved alphas. However, five specific conditions must be satisfied in the backtest. If any condition cannot be met, the alpha should be rejected.

---

## Review Checklist

| Criterion | Pass/Fail | Notes |
|-----------|-----------|-------|
| Economic rationale is sound | PASS | Two-layer mechanism (sentiment + structural depth), grounded in Bessembinder & Seguin (1993) and Matsui et al. (2022). Credible reasons for edge persistence (attention asymmetry, quantification gap, directional risk deters arbitrageurs). |
| Hypothesis is falsifiable | PASS | Memo explicitly states: reject if OI-enhanced signal does not outperform pure price reversal in control test (Open Question #3). This is a clean, testable falsification criterion. |
| Data sources are available | CONDITIONAL PASS | Binance API provides OI, price, and funding rate data with 2019+ coverage. CoinGlass offers cross-validation. However, OI misreporting (Giagkiozis & Said 2024) is a genuine risk -- the data quality filter MUST be operational in backtest. |
| No lookahead bias detected | PASS | All signal inputs use trailing or contemporaneous data available at the 00:00 UTC evaluation time. 7-day OI/price changes, 30-day trailing volatility, and 30-day trailing funding rate deciles are all known at computation time. Expiry calendar is static. Exit uses holding-day count and trailing alignment, no forward-looking condition. |
| Overfitting risk is acceptable | CONDITIONAL PASS | ~8-10 free parameters is not excessive, but the 1.5-sigma divergence threshold has weak theoretical justification ("feels right"). The 7-day lookback is defended by a hand-wavy "participant attention window" argument. Saving grace: the memo explicitly proposes walk-forward optimization, parameter sensitivity sweeps, and out-of-sample validation. Must be enforced. |
| Transaction costs are survivable | PASS | Estimated round-trip costs 0.15-0.35% with 3x buffer requiring >0.24% gross return per signal. At 2-5 day hold, this is achievable if the signal has genuine predictive power. ETH slippage estimates may be optimistic during volatility -- stress-test at 2x and 3x in backtest. |
| No overlap with existing ideas | PASS | CRYPTO-001 (funding rate carry/crowding): LOW overlap -- different mechanism (cost-of-leverage vs. market-depth), different data, different trade structure. CRYPTO-001 is delta-neutral carry; CRYPTO-002 is directional reversal. CRYPTO-003 (cross-sectional altcoin carry): NO overlap. The memo correctly identifies the interaction (funding rate extremes are used as a filter in CRYPTO-002, avoiding signal collision). |

---

## Economic Rationale Assessment

This alpha exploits the divergence between perpetual futures open interest (OI) and spot price over a 7-day window. The economic mechanism has two reinforcing layers. Layer 1 (sentiment/conviction): when price and OI move in opposite directions, the price move lacks structural support -- participants who drove the trend are exiting rather than reinforcing it. Layer 2 (structural market depth): falling OI means thinning market depth (Bessembinder & Seguin 1993 established OI as a depth proxy; Matsui et al. 2022 confirmed this for crypto futures). Thinner depth means each unit of order flow produces larger price impact, making overshooting and reversal more likely. In crypto, cross-margin cascades amplify this further: forced liquidations in one position trigger liquidations in correlated positions, creating reversal overshoots beyond what pure mean reversion predicts.

The edge should persist because: (a) OI monitoring requires attention to a second data stream that retail traders systematically neglect; (b) the four-quadrant framework is widely known qualitatively but rarely operationalized with precise thresholds and position sizing; (c) unlike funding rate arbitrage (which has been compressed by institutional capital), trading OI divergence requires taking directional risk and tolerating drawdowns, which deters arbitrageur participation. The counterparties are late-entering trend followers and retail traders who add to positions in trending markets without checking OI.

The primary weakness in the economic story is that the core concept (OI-price four-quadrant framework) is textbook material -- the edge depends entirely on whether the *quantitative specification* (thresholds, normalization, timing) captures alpha that the qualitative consensus leaves on the table. This is plausible but not guaranteed.

## Overlap Check

| Existing Idea | Similarity | Distinct? |
|---------------|------------|-----------|
| CRYPTO-001 (Funding Rate Carry and Crowding Signal) | Low | Yes -- CRYPTO-001 uses funding rates as cost-of-leverage signal with delta-neutral carry and crowding reversal legs. CRYPTO-002 uses OI as a market-depth signal with directional reversal. Different mechanisms, different data, different trade structures. CRYPTO-002 explicitly uses funding rate extremes as a filter (skip signals when FR is in top/bottom decile), which prevents signal collision rather than creating redundancy. |
| CRYPTO-003 (Cross-Sectional Altcoin Funding Carry) | None | Yes -- CRYPTO-003 is cross-sectional carry capture across altcoins. CRYPTO-002 is time-series directional reversal on BTC/ETH. Different universes, different mechanisms, different holding periods. No overlap. |
| OI-price four-quadrant framework (practitioner literature) | High (conceptual) | Yes -- the framework is the qualitative foundation, but CRYPTO-002 adds quantitative thresholds, normalization, lookback windows, and position sizing that do not exist in the practitioner literature. The distinct contribution is operationalization, not concept discovery. |

## Key Risks to Watch (for Programmer Agent)

1. **OI data quality (PRIMARY RISK).** Giagkiozis & Said (2024) documented systematic OI misreporting across major exchanges. Bad OI data will generate false divergence signals. The OI-volume reconciliation filter (discard when delta-OI diverges from cumulative volume by >20%) must be operational. The backtest report must state what percentage of observations were filtered out.

2. **The control test is existential.** If the OI-enhanced reversal signal does not outperform a simple price momentum reversal on the same lookback/holding period, the alpha fails its own falsification criterion. The Programmer Agent must implement a clean A/B test: (A) pure price reversal, (B) OI-enhanced reversal, with identical holding periods.

3. **Regime dependence.** The signal almost certainly performs differently in trending vs. range-bound markets. If it only works in range-bound regimes and generates false signals in trends, the realized performance will be worse than the unconditional backtest suggests. Regime-conditional performance must be reported.

4. **Parameter stability across regimes.** The 1.5-sigma divergence threshold and 7-day lookback may be optimal for one market regime but harmful in another. Walk-forward optimization and sub-period analysis are mandatory.

---

## Approval Conditions (Mandatory)

The following five conditions must be met in the backtest. If any condition cannot be satisfied, CRYPTO-002 should be moved to `research/ideas/rejected/`:

### Condition 1: Control Test (Pure Price Reversal Benchmark)

The backtest must include a control signal that uses identical mechanics but WITHOUT the OI component: compute a 7-day price change, enter in the opposite direction (price reversal), hold for the same N-day sweep, with the same exit rules. The OI-enhanced signal must demonstrate meaningful improvement on at least two of: Sharpe ratio, hit rate, maximum drawdown, or Calmar ratio. If the OI-enhanced version does not outperform the price-only version, the alpha fails its own falsification criterion (Open Question #3 in the memo).

### Condition 2: Operational Data Quality Filter

The OI-volume reconciliation check must be implemented and applied before any signal is generated. Periods where the absolute difference between delta-OI and cumulative traded volume exceeds 20% of cumulative volume must be flagged and excluded. The backtest report must state: (a) what percentage of total observations were filtered out, (b) whether filtered periods cluster around specific dates/events, and (c) whether using CoinGlass aggregated OI (if available) changes the filter rate.

### Condition 3: Parameter Sensitivity Analysis

The backtest report must include a sensitivity table showing performance variation across:
- Divergence threshold: 1.0-sigma, 1.5-sigma, 2.0-sigma
- Lookback window: 3-day, 7-day, 14-day
- Funding rate decile filter: 5th/95th, 10th/90th, 15th/85th, no filter
- Volatility normalization window: 14-day, 30-day, 60-day

This is NOT an optimization step (parameters should be fixed ex ante for the primary backtest). This is a robustness check to determine whether performance is brittle to any single parameter choice.

### Condition 4: Regime-Conditional Performance

The backtest must classify each signal date into a market regime (trending up, trending down, range-bound) using a 30-day trend strength indicator (e.g., ADX or price vs. moving average slope). Performance must be reported separately for each regime, including: number of signals, hit rate, average return per signal, and Sharpe ratio. If the signal has negative expected return in any regime, this must be documented explicitly with a regime-filter recommendation.

### Condition 5: Out-of-Sample Validation

At minimum, the backtest must split the data into:
- In-sample / optimization period: 2019-2022
- Out-of-sample / validation period: 2023-2025

The holding period sweep (N = 1, 2, 3, 5, 7 days) may be optimized in-sample, but the chosen N must be fixed and tested out-of-sample. Both in-sample and out-of-sample results must be reported. If out-of-sample performance degrades materially relative to in-sample, the alpha should be rejected.

---

## Questions for Research Agent

None. The memo is thorough and the open questions are appropriate for empirical resolution via backtest.

---

## Reviewer Notes

The memo quality is high -- well-structured, well-referenced, and self-aware about limitations. The Research Agent correctly identified the key risks (OI data quality, regime dependence, redundancy with price reversal) and proposed mitigations. The confidence ratings are appropriately calibrated: high on economic intuition (8/10), moderate on data availability (6/10), and only average on novelty (5/10).

The primary concern is not with the research quality but with whether the edge survives empirical testing. The four-quadrant framework is one of the most widely-taught concepts in futures trading. If quantitative operationalization were sufficient to extract alpha, someone would have done it already. The backtest is the only way to resolve this question.

A secondary concern: the memo mentions a 3-day expiry exclusion window, but the KB note uses 2 days. This inconsistency is minor and should be resolved during implementation (3 days is safer).

The signal timing is specified as evaluation at 00:00 UTC with entry conditions checked at the same time. For crypto's 24/7 markets, this is clean. The Programmer Agent should confirm that Binance's OI endpoint provides data with zero or minimal lag at 00:00 UTC, or adjust the evaluation time accordingly.

---

*Review completed by: Review Agent*
*Next step: If approved by Research Agent for handoff, create programmer handoff document in `handoffs/pending/` and notify Programmer Agent.*
