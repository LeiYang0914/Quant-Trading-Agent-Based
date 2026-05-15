# Programmer Handoff: Cross-Sectional Altcoin Funding Rate Carry

**Date:** 2026-05-14
**Source Memo:** `research_memos/crypto/03_cross_sectional_altcoin_funding_carry.md`
**Status:** Pending Implementation

---

## 1. Alpha Summary (from Researcher)

A market-neutral, cross-sectional carry strategy that goes long the highest-funding-rate altcoin perpetual futures and short the lowest-funding-rate altcoin perpetual futures across a universe of 20-30 altcoins (excluding BTC, ETH, stablecoins). The strategy rebalances every 8 hours (aligned with funding settlement at 00:00, 08:00, 16:00 UTC), capturing the persistent funding rate spread that arises from concentrated retail leverage demand and structurally constrained arbitrage capital in smaller-cap crypto assets. The core academic reference (Fan, Jiao, Lu, Tong 2024) documents 43.4% annualized returns with Sharpe 0.74 for a similar cross-sectional crypto carry strategy. The key alpha source is the funding rate spread between top-quintile and bottom-quintile altcoins, which is harvested via a beta-neutral long-short perp portfolio.

---

## 2. Inputs

- **Binance USDM Perpetual Funding Rate History:** `GET /fapi/v1/fundingRate` for each symbol in the universe. Fields: `symbol`, `fundingRate` (string, parse as float), `fundingTime` (millisecond timestamp). Example: `GET /fapi/v1/fundingRate?symbol=SOLUSDT&limit=1000`.
- **Binance Spot OHLCV:** `GET /api/v3/klines` at 8-hour interval for each altcoin. Fields: open time, open, high, low, close, volume.
- **CoinGecko Market Cap (free API):** Daily market cap for universe construction. `GET /api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1`. Fields: `id`, `symbol`, `market_cap`, `total_volume`.
- **Binance Exchange Info (for listed perps):** `GET /fapi/v1/exchangeInfo` to get all currently listed USDM perpetual symbols and their contract details (for universe filtering and delisting tracking).

---

## 3. Preprocessing

1. **Funding rate parsing:** Parse `fundingRate` string to float. The Binance API returns funding rate as a decimal string (e.g., "0.00010000" = 0.01% per 8h). Convert to basis points (multiply by 10000) or percentage (multiply by 100) for readability. Annualize as `fundingRate * 3 * 365 * 100` for percentage annualized.

2. **Timestamp alignment:** Align funding rate `fundingTime` to the most recent prior 8-hour bar close (00:00, 08:00, 16:00 UTC). Each funding rate observation corresponds to the period that just settled, so the funding rate with `fundingTime = T` reflects the rate paid at time T for positions held during the [T-8h, T] period.

3. **Universe construction (point-in-time):**
   - At each rebalance date, fetch the top N altcoins by market cap from CoinGecko.
   - Exclude: BTC, ETH, any stablecoin (USDT, USDC, DAI, BUSD, TUSD, USDP, FRAX), wrapped tokens (WBTC, WETH), and any coin that does not have a corresponding Binance USDM perpetual.
   - Exclude coins listed less than 90 calendar days before the rebalance date (to avoid newly-listed volatility).
   - Exclude coins with delisting announcements active at the rebalance date.
   - Map CoinGecko `symbol` to Binance perpetual symbol (typically `{SYMBOL}USDT`). Handle symbol conflicts (e.g., multiple coins with same ticker) by matching CoinGecko `id` to the correct Binance pair.

4. **Liquidity filter:** At each rebalance date, exclude any altcoin perp with trailing 30-day average daily volume below a configurable threshold (default: $10M). This prevents the strategy from trading extremely illiquid pairs.

5. **Funding rate data quality filter:**
   - Forward-fill missing funding rate observations for up to 1 missing period (8 hours). If gap > 24 hours (3 missing periods), flag the coin and exclude from that rebalance period.
   - Flag and investigate funding rates that are exactly at the exchange cap (e.g., 0.375% or 0.75% per 8h on some pairs). These rates are censored and do not reflect true market demand.
   - If a coin has fewer than 30 days of funding history available, exclude it from the universe.

---

## 4. Signal Construction

### Primary Signal: Quintile Cross-Sectional Funding Rate Carry

At each rebalance time T (00:00, 08:00, 16:00 UTC):

1. **Collect the most recent settled funding rate** for every altcoin perpetual in the point-in-time universe. This is the funding rate with `fundingTime` equal to T (the settlement that just occurred).

2. **Cross-sectionally rank** all altcoins by this funding rate, from highest to lowest.

3. **Assign quintiles:**
   - Q5: Top 20% (highest funding rates) -- these are the "long" candidates.
   - Q4: 60th-80th percentile.
   - Q3: 40th-60th percentile.
   - Q2: 20th-40th percentile.
   - Q1: Bottom 20% (lowest funding rates) -- these are the "short" candidates.

4. **Generate signals:**
   - For each altcoin in Q5: signal = +1 (long the perpetual, collecting funding)
   - For each altcoin in Q1: signal = -1 (short the perpetual, paying minimal/receiving negative funding)
   - For all other altcoins: signal = 0 (no position)

5. **Timing discipline (lookahead protection):** The signal is computed using funding rates that settled at time T. Positions are entered at the open of the next bar (time T, effective immediately after the settlement). The first funding payment for the new position occurs at time T+8h.

### Alternative Signal: Z-Score Proportional

Instead of binary quintile membership:

1. Compute cross-sectional z-score for each altcoin's funding rate: `z_i = (fr_i - mean(fr)) / std(fr)`, where mean and std are computed across the current universe at this rebalance period.

2. For altcoins with z_i > 0: `signal = min(2.0, z_i)` (long, capped at 2 std dev).
3. For altcoins with z_i < 0: `signal = max(-2.0, z_i)` (short, capped at 2 std dev).
4. For altcoins with |z_i| < 0.25: `signal = 0` (neutral zone to reduce turnover on near-median coins).
5. Position weight = signal / sum(abs(all positive or negative signals for that leg)).

### Alternative Signal: Momentum-Orthogonalized

1. At each rebalance, also compute trailing 7-day spot return for each altcoin.
2. Cross-sectionally rank returns and compute return z-scores.
3. Regress funding rate z-scores on return z-scores (cross-sectionally).
4. Use the residual from this regression as the orthogonalized signal.
5. Assign quintiles or z-scores on the orthogonalized residual.

---

## 5. Portfolio Construction

| Parameter | Value |
|---|---|
| **Unit size** | Equal weight within each leg. Each altcoin in the long quintile gets equal notional. Each altcoin in the short quintile gets equal notional. Long leg total notional = Short leg total notional (market-neutral). |
| **Total gross exposure** | 200% (100% long + 100% short). Alternatively, can be scaled by target volatility. |
| **Target annualized volatility** | Optional: scale gross exposure to target 15-20% annualized volatility using trailing 30-day portfolio volatility. |
| **Max position per altcoin** | Cap at 10% of gross exposure per single altcoin to avoid concentration. |
| **Max sector exposure** | Optional: cap at 40% of gross exposure for any single crypto sector (L1, L2, DeFi, meme, AI, gaming). |
| **Leverage** | 1x (no leverage). Each unit of notional long is matched by one unit of notional short. |
| **Rebalance frequency** | Every 8 hours at funding settlement (00:00, 08:00, 16:00 UTC). |
| **Execution assumption** | Positions entered at the open of the bar following signal computation. Assume taker orders for all entries and exits. |

---

## 6. Transaction Cost Assumptions

Costs are tiered by altcoin liquidity bucket, based on trailing 30-day average daily volume:

| Liquidity Bucket | Daily Volume | Taker Fee | Estimated Spread | Slippage (at $50K notional) | Total One-Way Cost |
|---|---|---|---|---|---|
| Tier 1 (top 5 alts) | > $500M | 0.04% | 0.02% | 0.01% | 0.07% |
| Tier 2 (alts 6-10) | $100M-$500M | 0.04% | 0.05% | 0.02% | 0.11% |
| Tier 3 (alts 11-20) | $50M-$100M | 0.05% | 0.08% | 0.04% | 0.17% |
| Tier 4 (alts 21-30) | $10M-$50M | 0.06% | 0.12% | 0.08% | 0.26% |

- **Round-trip cost (entry + exit):** 2x one-way cost.
- **Funding rate fees:** The funding rate itself (long receives, short pays, or vice versa when negative) is part of the P&L, not a separate transaction cost.
- **Default VIP tier assumption:** Assume standard tier (no VIP discount). If VIP tiers are available, model more favorable rates.

---

## 7. Backtest Specification

| Parameter | Value |
|---|---|
| **In-sample period** | 2022-01-01 to 2023-12-31 |
| **Out-of-sample period** | 2024-01-01 to 2025-12-31 |
| **Walk-forward design** | 12-month expanding window. Re-estimate universe composition and any rolling parameters each window. First window: 2022 in-sample, 2023 test. Second window: 2022-2023 in-sample, 2024 test. Final window: 2022-2024 in-sample, 2025 test. |
| **Benchmark 1** | BTC spot buy-and-hold (for beta comparison) |
| **Benchmark 2** | Equal-weighted long-short cross-sectional momentum on the same universe (same quintiles, same rebalance, but ranked by trailing 7-day return instead of funding rate). This isolates whether the alpha is from funding carry or momentum. |
| **Benchmark 3** | Cross-sectional carry on BTC + ETH only (2-asset long-short). This tests whether expanding to altcoins adds value beyond the simplest form of this strategy. |
| **Universe** | Top 20 altcoins by market cap with Binance USDM perpetuals (configurable: 10, 15, 20, 25, 30). |
| **Rebalance frequency** | Every 8 hours (at funding settlement). Test daily (once per 3 settlements) as a less-frequent alternative. |
| **Holding period** | Variable (determined by quintile membership). Test minimum holding period of 24 hours (3 settlements). |
| **Transaction costs** | Included. Use tiered cost model from Section 6. |
| **Funding payments** | Included. Each period, long positions receive (fundingRate * notional), short positions pay (fundingRate * notional). When fundingRate is negative, longs pay and shorts receive. Account for the sign correctly. |
| **Risk controls** | Max drawdown stop at 20% of cumulative P&L. Reduce position size by 50% if drawdown exceeds 10%. |

---

## 8. Edge Cases

- **Negative funding rates (both legs):** In bear markets, most altcoin funding rates may be negative (shorts pay longs). In this case, the long-short cross-sectional logic still applies: go long the MOST negative funding rates (you pay the least, or receive the most), short the LEAST negative funding rates. The quintile ranking always sorts by rate from highest to lowest; do not change the direction based on whether the median rate is positive or negative.

- **Exchange-delisted perpetual:** If an altcoin perpetual is delisted mid-strategy, the position must be closed at the delisting effective time. This may result in forced exit at unfavorable prices. In backtesting, the position should be closed at the last available mark price before delisting and flagged as a forced exit event with a note. In the point-in-time universe construction, delisted coins should not appear in universes after their delisting date.

- **Funding rate at exchange cap:** Some exchanges cap funding rates at a maximum (e.g., 0.75% per 8h for some altcoin pairs on Binance). When multiple altcoins are at the cap, the quintile ranking loses discriminatory power (they all have the exact same rate). Handling options: (a) treat capped coins as tied in rank and use a secondary signal (e.g., basis size) to break ties, or (b) exclude capped coins from the universe for that period. Option (b) is simpler and recommended for the initial backtest.

- **Zero or missing funding rate:** If a coin has a funding rate of exactly 0 or null, investigate: it may indicate the perpetual contract was newly listed and has not yet had its first settlement, or the exchange stopped updating the rate. Exclude coins with 0 funding rate until they have at least 3 consecutive non-zero settlements.

- **Holiday/thin trading periods:** Around Christmas/New Year, altcoin volumes can drop significantly. The strategy may hold positions through thin liquidity, increasing slippage. Consider a calendar-based shutdown (e.g., close all positions Dec 24 - Jan 2) or a volume-based circuit breaker (if trailing 3-day average volume drops > 50%, reduce position size by 50%).

- **Single-asset dominance:** In extreme cases, one altcoin's funding rate may be so far above the rest of the cross-section that it dominates the long quintile's return. To prevent this: (a) cap single-position notional at 10% of the leg, (b) winsorize funding rates at the 5th and 95th percentile of the cross-section before ranking.

- **Funding rate formula changes:** Binance and other exchanges occasionally change funding rate formulas (e.g., changing the clamp, changing from interest-rate-based to premium-index-based components). These events should be documented and any data around formula change dates flagged for investigation.

- **USDT/USDC depeg events:** During stablecoin stress, perp prices may diverge from spot in unusual ways, distorting funding rates. Flag major depeg events (e.g., March 2023 USDC depeg, August 2023 USDT wobble) and test performance excluding these periods.

---

## 9. Validation Checks

- [ ] **Funding payment accounting:** For any 30-day window, verify that the sum of funding payments received/paid in the backtest matches the theoretical sum (fundingRate * notional * number_of_settlements) computed from the raw funding rate data. This catches sign errors and settlement-counting bugs.

- [ ] **Market neutrality:** The rolling 30-day beta of the portfolio to BTC should be less than 0.15 in magnitude. If beta exceeds 0.15, investigate sector concentration or a systematic imbalance between long and short leg exposures.

- [ ] **Gross-to-net spread:** Plot the time series of gross return (before transaction costs) vs. net return (after transaction costs). The spread should be relatively stable. Sudden jumps in the spread indicate a data error or a period of abnormally high turnover.

- [ ] **Lookahead bias check:** Shift the funding rate signal forward by one period (use the NEXT settlement's funding rate as if it were known at signal time). If this "future-informed" strategy shows dramatically higher performance than the base strategy, lookahead bias may already be present in the base signal (e.g., if predicted funding is being used instead of settled funding).

- [ ] **Quintile monotonicity:** Over the full backtest, verify that the annualized return of Q5 > Q4 > Q3 > Q2 > Q1. If this monotonicity breaks (e.g., Q4 outperforms Q5), the signal may not be picking up a clean funding rate effect.

- [ ] **Survivorship bias check:** Compare the point-in-time universe (only coins that existed at each rebalance date) against a "survivor-only" universe (only coins that still exist at the end of the backtest). The survivor-only version should show higher returns. Quantify the difference; if it is large (>20% of alpha), survivorship bias is material.

- [ ] **Turnover sanity:** Daily turnover should not exceed 200% (implying the entire book turns over twice per day). If turnover is excessive (>150%/day), investigate whether quintile boundaries are too tight or funding rates are too noisy.

- [ ] **Delisting tracking:** Maintain a log of all delisting events during the backtest period. Verify that the strategy did not trade any delisted symbol after its delisting date.

- [ ] **Cross-exchange consistency:** Run the same logic on Bybit data (where available). The quintile ranking should be directionally consistent across exchanges for the same altcoins. Large discrepancies (>2 quintile jump for the same coin across exchanges) indicate data quality issues or exchange-specific manipulation.

---

## 10. Outputs Expected

- [ ] **Equity curve:** Time series of cumulative P&L, both gross and net of transaction costs. Plot on log scale.
- [ ] **Metrics table:** All evaluation metrics from Section 9 of the research memo (Sharpe, Sortino, max drawdown, Calmar, hit rate, turnover, alpha to momentum, beta to BTC/ETH, average FR spread, capacity estimates, tail risk metrics).
- [ ] **Quintile return decomposition:** Bar chart showing annualized return for each quintile (Q1 through Q5). Include error bars (standard errors).
- [ ] **Turnover analysis:** Time series of daily turnover (% of portfolio). Histogram of per-coin holding periods.
- [ ] **Transaction cost breakdown:** Pie chart showing total costs split between taker fees, spread costs, and slippage.
- [ ] **Parameter sensitivity heatmap:** Heatmap of net Sharpe across (rebalance frequency x universe size) grid. Additional heatmap for (quintile threshold x minimum holding period).
- [ ] **Regime performance table:** Net Sharpe and annualized return split by bull/bear/sideways regimes (BTC above/below 200d MA) and by high/normal/low volatility regimes.
- [ ] **Momentum overlap analysis:** Scatter plot of funding rate rank vs. trailing return rank. Correlation coefficient. Time series of this correlation to see if it varies by regime.
- [ ] **Orthogonalized signal performance:** Comparison table: base signal vs. momentum-orthogonalized signal (Sharpe, alpha, turnover).
- [ ] **Capacity curve:** Plot of net Sharpe vs. position notional ($1K to $50M), showing where slippage degradation thresholds are crossed.
- [ ] **Worst drawdown analysis:** Table of the 10 largest drawdowns with dates, duration, and market context annotation.
- [ ] **Rolling 90-day Sharpe:** Time series plot to visualize alpha decay over time.
- [ ] **Walk-forward OOS summary:** Table with one row per walk-forward window, showing in-sample and out-of-sample Sharpe, return, and turnover.

---

## 11. Constraints

- **Do not** implement live trading or connect to broker APIs.
- **Do not** place orders or interact with any exchange.
- **Do not** generate real-time trading signals.
- **Do not** produce a trading bot or automated system.
- This is a **research backtest only**. The output is analysis and visualization, not a production system.

---

*Handoff prepared by: Quant Alpha Researcher Agent*
*For: Quant Programmer Agent*
