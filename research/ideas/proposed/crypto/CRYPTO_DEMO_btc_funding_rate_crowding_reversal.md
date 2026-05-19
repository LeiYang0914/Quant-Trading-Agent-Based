# Alpha Discovery Note: BTC Funding Rate Crowding & Reversal

**Alpha ID:** `CRYPTO-DEMO-001`
**Domain:** `crypto`
**Discovery source:** Refinement of CRYPTO-001 Factor B — isolating the crowding-reversal signal as a standalone alpha
**Date:** 2026-05-19
**Status:** `demo — proposed (ready for Review Agent)`

---

## Raw Observation

When BTC perpetual funding rates reach extreme positive levels, they indicate that leveraged longs are paying a large premium to maintain bullish exposure. This crowded positioning has historically preceded sharp reversals — the market has run out of marginal buyers, and a critical mass of leveraged positions are vulnerable to liquidation cascades on even modest adverse price moves.

## Hypothesis

> When the 8-hour BTC perpetual funding rate exceeds the 90th percentile of its trailing 30-day distribution, forward BTC spot returns over the subsequent 8–48 hours are negatively skewed with negative expected value. The mechanism is forced deleveraging: extreme funding signals crowded leveraged-long positioning, elevated liquidation risk, and potential for cascading sell pressure.

## Why This May Be an Edge

1. **Behavioral persistence:** Retail overconfidence and lottery-preference bias are slow to arbitrage and unlikely to disappear from crypto markets
2. **Timing difficulty protects the edge:** Funding extremes can persist — the signal requires disciplined threshold-based entry rather than discretionary market timing
3. **Liquidation cascades are structural:** Cross-margin liquidation engines are hard-coded into exchange infrastructure. When they trigger, selling is automatic and price-insensitive, creating overshoots that a systematic contrarian can capture
4. **The signal is distinct from static carry:** Unlike delta-neutral funding carry (which has been compressed by institutional arbitrage capital), the directional crowding-reversal signal requires timing and active risk management — it cannot be passively harvested

## Market Structure Mechanism

- 8-hour funding settlement cycle (00:00, 08:00, 16:00 UTC) provides natural signal evaluation cadence
- Cross-margin liquidation systems on Binance/Bybit/OKX create cascade potential: liquidation → forced market sell → price decline → more liquidations
- CEX funding rate caps (~0.375% per 8h) may compress the observable extreme, requiring OI-weighted multi-exchange aggregation for cleaner signal
- The effect is likely strongest on BTC due to its central role in crypto market structure — BTC moves drive altcoin liquidations, so BTC-specific crowding has systemic implications

## Required Data

| Dataset | Source | Frequency | Availability |
|---------|--------|-----------|-------------|
| BTC-PERP funding rate (8h) | Binance API | 8h | Free, 2019–present |
| BTC spot OHLCV | Binance API | 1h / 8h | Free, 2017–present |
| BTC-PERP open interest | Binance API / CoinGlass | 1h | Free tier / paid API |
| OI-weighted multi-exchange funding rate | CoinGlass / Glassnode | 8h | Free tier / paid |

## Suggested Signal (Plain English)

At each 8-hour funding settlement, compute the current funding rate's percentile rank within the trailing 30-day (90-observation) window. If the rank is at or above the 90th percentile, enter a short BTC position at the next bar open. Close after 24 hours or when the percentile returns to the 25th–75th normal range, whichever comes first. Position size: 10% NAV. For long entries, use the 10th percentile threshold. Add a trend filter: only short when BTC is below its 50-day moving average.

## Similar Known Strategies

- **CRYPTO-001 Factor B:** Same mechanism, broader scope. This is a sharper, standalone calibration.
- **OI-Price Divergence (CRYPTO-002):** Different crowding indicator (OI vs price), same contrarian philosophy. Signals may be complementary.
- **Generalized mean-reversion on sentiment extremes:** Category includes VIX spike fading, put/call ratio extremes, CFTC COT positioning extremes — all share the same "fade the crowd at extremes" structure.

## What Could Invalidate It

1. **Institutional arbitrage of the signal itself:** If enough capital trades against funding extremes, the reversal window shortens to minutes rather than hours, eliminating retail-accessible alpha
2. **Structural regime change in funding mechanics:** If exchanges modify funding rate formulas, caps, or settlement frequency, historical relationships may break
3. **No empirical out-of-sample performance:** If walk-forward backtest on 2023–2025 data shows no edge (Sharpe < 0 after costs), the hypothesis is falsified
4. **Funding cap masking:** If the Binance 0.375% cap binds during true crowding events, the 90th percentile computed from capped data may not identify genuine extremes

## Minimum References Needed Before Memo

- [x] At least 2 credible references (have 6, including 4 Tier 1)
- [x] At least 1 Tier 1 or Tier 2 source (have BIS WP 1087, arXiv:2212.06888, SSRN:5576424, Mathematical Finance 2025)

## Current References

| Ref ID | Title | Tier | Key Insight |
|--------|-------|------|-------------|
| CRYPTO-PAPER-002 | Crypto Carry (BIS WP 1087) | 1 | High absolute funding predicts crashes |
| CRYPTO-PAPER-001 | Fundamentals of Perpetual Futures | 1 | Perpetual pricing; funding deviation from fair value |
| CRYPTO-PAPER-006 | Predictability of Funding Rates | 1 | Funding rates are statistically predictable |
| CRYPTO-PAPER-005 | Perpetual Futures Pricing | 1 | Theoretical pricing validation |
| CRYPTO-PRACT-005 | Glassnode Insights | 3 | Practitioner confirmation |
| CRYPTO-OFFICIAL-002 | BitMEX Q3 2025 Report | 2 | Funding regime change documentation |

---

## Review Agent Handoff Summary

**For:** Review Agent
**From:** Research Agent (demo mode)
**Date:** 2026-05-19

**One-paragraph mechanism summary:**
BTC perpetual funding rates act as a revealed-preference gauge of market positioning. When the 8-hour funding rate reaches the 90th percentile of its 30-day trailing distribution, it signals that leveraged longs are paying an extreme premium to maintain exposure — the market is crowded to one side. This crowding creates fragility: even a modest adverse price move triggers liquidations, which force automatic market-sell orders, which push price lower, which trigger more liquidations. The signal is a systematic contrarian entry timed to capture the mean-reversion and cascade dynamics that follow positioning extremes.

**Falsifiable hypothesis:**
If the 90th-percentile funding rate signal does NOT produce negative expected forward returns over 8–48 hours on out-of-sample data (2023–2025), after reasonable transaction costs, the hypothesis is falsified.

**Required data sources (availability confirmed):**
- Binance BTC-PERP funding rate: free API, 2019–present
- Binance BTC spot OHLCV: free API, 2017–present
- CoinGlass OI-weighted funding rate: free tier available

**Key failure modes (top 3):**
1. Bull market whipsaw: repeated short signals in a strong uptrend generate cumulative losses
2. Funding cap compression: Binance's 0.375% cap masks true crowding intensity
3. Crowding decay: the edge compresses as more participants trade the same signal

**Link to full research memo:** `research/memos/crypto/CRYPTO_DEMO_btc_funding_rate_crowding_reversal.md`

---

*Alpha discovery note authored by: Research Agent (demo mode)*
*Next: Review Agent evaluation (not executed in demo)*
*Disclaimer: Demo artifact for interview evidence. Not financial advice. No backtest validation performed.*
