# Programmer Handoff: BTC Funding Rate Crowding & Reversal Signal

**Date:** 2026-05-19
**Source Memo:** `research/memos/crypto/CRYPTO_DEMO_btc_funding_rate_crowding_reversal.md`
**Source Idea Note:** `research/ideas/proposed/crypto/CRYPTO_DEMO_btc_funding_rate_crowding_reversal.md`
**Status:** Demo — Pending Implementation
**Alpha ID:** CRYPTO-DEMO-001

---

## 1. Alpha Summary (from Researcher)

When the 8-hour BTC perpetual funding rate reaches extreme positive levels (≥90th percentile of trailing 30-day distribution), it signals crowded leveraged-long positioning. This crowding creates structural fragility: adverse price moves trigger liquidations, which force automatic market-sell orders, which push price lower, which trigger more liquidations — a cascading feedback loop. The signal enters a contrarian short position at the next bar open after an extreme reading, and exits after 24 hours or when the funding rate normalizes to the 25th–75th percentile range. The mechanism is grounded in the BIS Crypto Carry paper (Schmeling et al. 2023) and perpetual futures pricing theory (He et al. 2022; Ackerer et al. 2025).

---

## 2. Inputs

- **Binance BTC-PERP funding rate history:** `GET /fapi/v1/fundingRate` — 8-hour interval, from 2019-01-01 to present
- **Binance BTC/USDT spot OHLCV:** `GET /api/v3/klines` — 8-hour interval (aligned to 00:00, 08:00, 16:00 UTC), from 2019-01-01 to present
- **Binance BTC-PERP open interest (optional enhancement):** `GET /fapi/v1/openInterest` — 1-hour interval, for filtering/confirmation
- **CoinGlass OI-weighted multi-exchange funding rate (optional cross-validation):** API or CSV export, 8-hour interval

---

## 3. Preprocessing

1. Pull Binance BTC-PERP funding rate history. Parse `fundingRate` (decimal) and `fundingTime` (Unix ms).
2. Pull Binance BTC/USDT spot OHLCV at 8h frequency. Align timestamps to funding settlement times (00:00, 08:00, 16:00 UTC).
3. Merge funding rate data with spot OHLCV data on timestamp. Forward-fill missing funding rate for up to 1 period (8h). If gap exceeds 24 hours (3 periods), mark those bars as invalid and exclude from signal generation.
4. Compute annualized funding rate for reference: `annualized_fr = funding_rate * 3 * 365 * 100` (percentage).
5. Note the Binance funding formula change in 2021. Document which periods used which formula. Flag any normalization applied.
6. Compute BTC 50-day simple moving average from spot close for the trend filter.

---

## 4. Signal Construction

1. **Rolling percentile computation:** At each 8h bar close, collect the trailing 90 funding rate observations. Compute the empirical percentile rank of the current bar's funding rate within this window. If fewer than 60 observations are available (warm-up or gap period), output no signal (0).
2. **Short entry (crowding fade):** Signal = -1 when funding rate percentile rank ≥ 0.90 AND BTC spot close < 50-day SMA (trend filter active). If trend filter is disabled, ignore the SMA condition.
3. **Long entry (oversold fade):** Signal = +1 when funding rate percentile rank ≤ 0.10. No trend filter for long entries (extreme negative funding is rare enough to not require filtering).
4. **No signal:** 0 when percentile rank is between 0.10 and 0.90.
5. **Position management (pseudocode, plain English):** If no position is active and signal is non-zero, enter a position of 10% NAV in the signal direction at the next bar's open price. Track the entry bar index. At each subsequent bar close, check exit conditions. Exit at the next bar open if conditions are met.

---

## 5. Portfolio Construction

- Unit size: 10% of NAV per trade
- Max position: 10% NAV (single position; no concurrent signals; no pyramiding)
- Rebalance frequency: Signal evaluated every 8h at bar close; entry/exit at next bar open
- Leverage: None (1x notional). The position is directional BTC — no leverage applied
- Benchmark: BTC spot buy-and-hold; US 3-month T-bill return (risk-free proxy)

---

## 6. Transaction Cost Assumptions

| Item | Assumption |
|---|---|
| Binance taker fee | 0.04% per side |
| BTC spot slippage (10% NAV entry) | 0.02% per side |
| Total round-trip cost | ~0.12% |
| Cost sweep (sensitivity) | Test at 0.5x (0.06%), 1x (0.12%), 2x (0.24%) baseline |
| Funding P&L while in position | If short while funding is positive, receive funding (positive carry tailwind); if short while funding turns negative, pay funding (headwind). Track funding P&L separately from price P&L. |

---

## 7. Backtest Specification

| Parameter | Value |
|---|---|
| In-sample period | 2019-01-01 to 2022-12-31 |
| Out-of-sample period | 2023-01-01 to 2025-12-31 |
| Walk-forward design | 6-month expanding windows; re-estimate percentile thresholds each window using only data available at that time |
| Benchmark | BTC spot buy-and-hold |
| Universe | BTC only |
| Rebalance frequency | 8-hour (signal evaluation at bar close; entry/exit at next bar open) |
| Holding period | 24 hours base case; sweep 8h, 24h, 48h |

---

## 8. Edge Cases

1. **Consecutive signals:** If a signal fires while a position is already active (e.g., extreme funding persists for multiple periods), ignore the new signal. Only one position at a time.
2. **Data gap during position:** If the funding rate data feed is interrupted while a position is active, hold the position and continue checking exit conditions using the last known funding rate. Force-close if gap exceeds 24 hours.
3. **Funding rate cap binding:** If the raw funding rate equals the Binance cap (0.375% per 8h) for 3+ consecutive periods, flag as "cap-binding event." The true unconstrained funding rate may be higher. Optionally override the signal to active short regardless of percentile rank (conservative — assume true crowding is extreme enough to trigger).
4. **Exchange downtime:** Remove bars where Binance was known to be down. These are not zero-funding periods — they are missing data.
5. **Formula change crossover:** The 2021 Binance formula change means funding rates before and after the change are not directly comparable. Split the in-sample period at the change date and compute percentiles separately for pre-change and post-change data. Document the split date and normalization.
6. **Survivorship / pre-2019 sparsity:** Pre-2019 funding rate data may be sparse or unreliable. If fewer than 60 observations exist in the first 90-bar lookback window, extend the lookback to accumulate 60 valid observations before generating the first signal.
7. **Signal reversal during position:** If a short position is active and a long signal fires (funding drops to ≤10th percentile), close the short immediately and open the long. This is a rare event (requires funding to swing from ≥90th to ≤10th percentile within 24h) but should be handled.

---

## 9. Validation Checks

- [ ] Confirm that percentile ranks are computed using only data available at signal time (no lookahead — the current bar's funding rate is compared to the previous 90 bars, not including itself if using a strict ranking). Decide whether to include or exclude current bar from ranking window and document the choice.
- [ ] Verify that walk-forward percentile thresholds are re-estimated using only in-window data. The 90th percentile from 2019 should not influence 2024 signals.
- [ ] Confirm no lookahead bias: entry at next bar open, not current bar close or open.
- [ ] Verify that exit P&L is computed at the bar open price after the exit condition is met, not the bar close that triggered the exit.
- [ ] Cross-check signal generation on a small sample (e.g., 30 days) with a manual spreadsheet calculation.
- [ ] Confirm funding P&L is tracked correctly: short position receiving funding should show positive carry; if funding is negative while short, P&L should show a debit.

---

## 10. Outputs Expected

- [ ] Equity curve (daily and 8h frequency) — price return, funding return, and total return separated
- [ ] Metrics table: annualized return, annualized volatility, Sharpe ratio, Sortino ratio, max drawdown, Calmar ratio, hit rate, average win/loss ratio, profit factor
- [ ] Performance by regime: BTC above 200d MA (bull), below 200d MA (bear), within ±5% of 200d MA (sideways)
- [ ] Performance by funding environment: low funding (<5% ann.), medium (5–20% ann.), high (>20% ann.)
- [ ] Parameter sweep heatmaps: percentile threshold (80/85/90/95/98) vs holding period (8h/16h/24h/48h)
- [ ] Transaction cost sensitivity table: Sharpe at 0.5x, 1x, 2x assumed costs
- [ ] Subperiod table: 2019–2020, 2021, 2022, 2023–2025 (separate rows)
- [ ] Signal count by year: how many signals fired, how many were profitable
- [ ] Drawdown chart (underwater plot, daily)

---

## 11. Constraints

- **Do not** implement live trading or connect to broker APIs
- **Do not** place orders on any exchange
- **Do not** use future data in signal construction (strict no-lookahead)
- **Do not** hardcode the percentile thresholds — they must be computed from rolling data at each bar
- **Do not** apply leverage to the position (1x notional only)
- This is a research backtest only. Output is a backtest report, not a trading signal feed.

---

*Handoff prepared by: Research Agent (demo mode)*
*For: Programmer Agent*
*Prerequisite: Review Agent approval (not executed in demo)*
*Disclaimer: Demo artifact for interview evidence. This is not a production implementation request. No backtest has been run. Signal parameters are informed by literature but not empirically calibrated.*
