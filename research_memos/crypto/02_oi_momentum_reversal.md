# Alpha Research Memo: Crypto Open Interest-Price Divergence as a Short-Term Reversal Signal

**Date:** 2026-05-14
**Status:** Research in Progress — needs_data_check
**Priority:** High
**Markets:** Crypto
**Assets:** BTC, ETH perpetual futures

---

## 1. One-Sentence Summary

When perpetual futures open interest and spot price diverge over a 7-day window (price up + OI down, or price down + OI up), the trend is losing structural participation and a short-term price reversal is more likely than continuation, with the signal modulated by funding rate extremes and absolute OI levels.

---

## 2. Market

- CLOB CEX perpetual futures: Binance, Bybit, OKX
- BTC and ETH only for initial test (best data quality, deepest markets)
- DEX perpetuals excluded — different OI mechanics (Chen, Ma, Nie 2024)

---

## 3. Research Motivation

### Mechanism

Open interest (OI) measures the total number of outstanding futures contracts. Changes in OI reflect capital flows into or out of the market:

- **Rising OI** = new positions opened = fresh capital committing = trend has support
- **Falling OI** = positions closed = capital exiting = trend losing foundation

When price moves in one direction but OI moves in the opposite direction (divergence), the price move is not supported by new capital. Existing participants are exiting rather than reinforcing the trend. This creates a structurally fragile price level.

The mechanism has two reinforcing layers:
1. **Sentiment layer:** Divergence signals that conviction behind the trend is waning
2. **Structural layer:** Falling OI means thinning market depth (Matsui et al. 2022, extending Bessembinder & Seguin 1993), which means each unit of order flow has larger price impact, making overshooting and reversal more likely

Additionally, in crypto perpetual futures, high-OI environments combined with one-sided positioning create liquidation cascade risk — when the reversal begins, forced liquidations amplify the move beyond fair value, increasing the alpha capture opportunity.

### Why Does the Edge Persist?

1. **Attention allocation:** Most traders focus on price. OI requires looking at a second data stream. Retail systematically underweights OI.
2. **Qualitative vs. quantitative:** Every trading guide mentions OI divergence as a warning sign, but few specify precise entry/exit thresholds or test the signal quantitatively.
3. **Liquidation amplification:** Crypto's unique liquidation mechanics (cross-margin cascades) amplify reversals beyond what pure mean reversion would predict.
4. **Structural depth:** OI is negatively related to volatility (foundational futures market finding, confirmed for crypto by Matsui et al. 2022). Falling OI = thinning depth = larger price impact per order = stronger reversal.

---

## 4. Source Inspiration

### Source 1: Giagkiozis & Said (2024) — "Reconciling Open Interest with Traded Volume in Perpetual Swaps"

**Citation:** Giagkiozis, Ioannis and Said, Emilio (2024). "Reconciling Open Interest with Traded Volume in Perpetual Swaps." Ledger, Volume 9, pp. 1-15.
**Link:** https://arxiv.org/abs/2310.14973
**Relevance:** Documents systematic OI misreporting by major crypto derivatives exchanges. This is a critical data quality warning for any OI-based alpha. Informs the recommendation to use single-exchange (Binance) or CoinGlass aggregated OI data.

### Source 2: Matsui, Al-Ali, Knottenbelt (2022) — "On the Dynamics of Solid, Liquid and Digital Gold Futures"

**Citation:** Matsui, Toshiko; Al-Ali, Ali; Knottenbelt, William J. (2022). "On the Dynamics of Solid, Liquid and Digital Gold Futures." 2022 IEEE International Conference on Blockchain and Cryptocurrency (ICBC).
**Link:** https://arxiv.org/abs/2202.09845
**Relevance:** Confirms the negative OI-volatility relationship (foundational in traditional futures via Bessembinder & Seguin 1993) extends to crypto. Provides the structural mechanism for why falling OI makes prices more vulnerable to reversal: thinning depth amplifies order flow impact.

### Source 3: Chen, Ma, Nie (2024) — "Exploring the Impact: How Decentralized Exchange Designs Shape Traders' Behavior on Perpetual Future Contracts"

**Citation:** Chen, Erdong; Ma, Mengzhong; Nie, Zixin (2024). "Exploring the Impact: How Decentralized Exchange Designs Shape Traders' Behavior on Perpetual Future Contracts."
**Link:** https://arxiv.org/abs/2402.03953
**Relevance:** Shows OI dynamics differ between CEX (CLOB) and DEX (VAMM, Oracle) perpetuals. Informs the decision to scope this alpha to CLOB CEXs only, where OI signals are cleaner and more interpretable.

### Source 4: Bessembinder & Seguin (1993) — "Price Volatility, Trading Volume, and Market Depth: Evidence from Futures Markets"

**Citation:** Bessembinder, Hendrik and Seguin, Paul J. (1993). "Price Volatility, Trading Volume, and Market Depth: Evidence from Futures Markets." Journal of Financial and Quantitative Analysis, Vol. 28, No. 1, pp. 21-39.
**Link:** https://www.jstor.org/stable/2331234
**Relevance:** The foundational paper establishing OI as a proxy for market depth and documenting its negative relationship with volatility. This is the theoretical ancestor of all OI-based alpha research.

### Source 5: Practitioner Consensus — The Four-Quadrant OI-Price Framework

**Citation:** Documented consistently across Wikipedia (https://en.wikipedia.org/wiki/Open_interest), CryptoSlate (https://cryptoslate.com/tag/open-interest/), and Medium trading guides.
**Relevance:** The four-quadrant framework (Price Up/Down × OI Up/Down → Bullish/Bearish/Reversal) is the practitioner standard for interpreting OI-price relationships. Our quantitative specification builds on this framework by adding precise thresholds, lookbacks, and filters.

---

## 5. Alpha Hypothesis

> "When the 7-day change in perpetual futures OI and the 7-day change in spot price have opposite signs, and the divergence magnitude exceeds a threshold normalized by 30-day historical volatility, price will revert toward the OI-implied direction over the subsequent 1-7 days. Signal strength increases when OI is at extreme levels (high absolute OI) and when funding rates are not already at extremes in the signal direction."

**Falsification criteria:**
- OI divergence fails to predict reversals better than a coin flip in out-of-sample data
- Signal is entirely subsumed by simple price momentum reversal (OI adds zero information)
- Transaction costs consume the edge at any reasonable holding period
- Signal works only in one regime period (e.g., only 2021 bull market)

---

## 6. Factor Definition

| Parameter | Specification |
|---|---|
| Raw input | Daily OI (BTC/ETH terms), daily spot price, 8h funding rate |
| Lookback window | 7-day OI change, 7-day price change |
| Transformation | OI-Price Divergence Score = sign(ΔPrice_7d) × sign(ΔOI_7d). Negative = divergence. Normalize magnitude by 30-day realized vol. |
| Entry condition | Divergence score negative AND abs(normalized divergence) > 1.5σ AND funding rate not extreme in signal direction AND outside expiry window |
| Exit condition | Close after N days (N=1-7, to be optimized) OR if OI and price re-align for 2 consecutive days |
| Position size | 1% risk per trade, max 3 concurrent positions |
| Signal frequency | Daily signal check at EOD |
| Expected holding period | 1-7 days |
| Signal direction | Both (long on bearish divergence, short on bullish divergence) |

---

## 7. Required Data

| Dataset | Fields | Frequency | Vendor Options | Min Coverage | Known Issues |
|---|---|---|---|---|---|
| BTC/ETH perpetual OI | Open interest (contracts, USD) | Daily EOD | Binance API, CoinGlass | 3 years | Exchange misreporting (Giagkiozis & Said 2024) |
| BTC/ETH spot price | OHLCV | Daily | Binance | 3 years | Standard |
| Funding rate | 8h rate, aggregated daily | 8-hourly → daily mean | Binance, CoinGlass | 3 years | Gaps during exchange downtime |
| Futures expiry calendar | Expiry dates | Static | Exchange docs | Current year | Quarterly and monthly dates |

---

## 8. Failure Modes

| Failure Mode | Severity | Notes |
|---|---|---|
| OI data misreporting generates false signals | 4 (High) | Use Binance-only or CoinGlass reconciled OI; cross-check ΔOI vs. volume |
| Signal is redundant with price momentum reversal | 3 (Medium) | Must test OI-enhanced vs. price-only reversal; OI must add predictive power |
| Expiry-driven OI changes trigger false signals | 3 (Medium) | Calendar filter; validate OI changes against roll activity |
| Signal fails in trending regimes | 4 (High) | Must test conditional on trend strength; may only work in range-bound markets |
| Crowding compresses edge | 3 (Medium) | Monitor OI extremes as crowding indicator; scale inversely with crowding |
| Slippage on reversal entry consumes edge | 3 (Medium) | Test with conservative slippage assumptions (2-3x baseline spread) |

---

## 9. Evaluation Metrics

- Hit rate: % of signals where price moves in predicted direction within holding period
- Win/loss ratio: average gain on correct vs. average loss on incorrect
- Signal-by-regime: separate performance in trending vs. mean-reverting vs. high-vol markets
- Divergence magnitude bucket analysis: does stronger divergence → larger reversal?
- Parameter stability: lookback and threshold stability across sub-periods

---

## 10. Robustness Tests

- Walk-forward optimization: in-sample optimization, out-of-sample validation
- Sub-period: 2020-2021 bull, 2022 bear, 2023-2024 recovery separately
- Universe: BTC only, ETH only, combined, top-10 alts
- OI source sensitivity: Binance-only vs. CoinGlass aggregated
- Funding rate interaction: does funding extreme enhance or dilute the OI signal?
- Cost stress test: 2x and 3x transaction cost assumptions

---

## 11. Risk Notes

*This is research documentation, not a trading recommendation.*

1. OI data quality is the #1 risk — systematic misreporting by exchanges documented in academic literature
2. The four-quadrant framework is widely known among practitioners; the naive signal may already be crowded
3. Crypto market structure changes rapidly (post-FTX, ETF approvals); historical relationships may not persist
4. Liquidation cascades can produce violent reversals with slippage far exceeding assumptions
5. Signal performance is likely regime-dependent; a trending market will produce many false signals

---

## 12. Priority Score

| Dimension | Score (1-10) | Notes |
|---|---|---|
| Economic Intuition | 8 | Well-established in traditional futures; structural mechanism (market depth) is sound |
| Data Availability | 6 | OI data exists but quality concerns (misreporting) reduce score |
| Implementation Difficulty | 7 | Relatively simple signal construction (two inputs, daily frequency) |
| Expected Alpha Potential | 5 | Likely modest; widely-known concept, but quantitative specification may preserve edge |
| Robustness Likelihood | 5 | Regime-dependent; likely fails in strong trends |
| Capacity | 7 | Daily BTC/ETH signals can absorb meaningful size |
| Novelty | 4 | The four-quadrant framework is textbook material; novelty is in quantitative specification |

**Overall Research Priority: High** (strong mechanism, modest expected alpha, good capacity, data quality manageable with safeguards)

---

## 13. Next Steps for Quant Programmer Agent

- [ ] Verify data access: confirm Binance OI and CoinGlass OI data is available with 3+ years history
- [ ] Implement signal construction: 7-day OI change, 7-day price change, divergence score, normalization
- [ ] Implement filters: funding rate check, expiry calendar, OI data quality (OI/volume ratio plausibility)
- [ ] Run walk-forward backtest with parameter sweep on lookback (3d, 7d, 14d, 21d) and entry threshold (1σ, 1.5σ, 2σ)
- [ ] Report: equity curve, Sharpe, max drawdown, hit rate, win/loss, by-regime performance, parameter sensitivity
- [ ] Compare: OI-enhanced reversal vs. pure price reversal (control test)
- [ ] Return results to Research Agent for interpretation

---

*Memo authored by: Quant Alpha Researcher Agent*
*Handoff status: Pending — data availability check in progress*
