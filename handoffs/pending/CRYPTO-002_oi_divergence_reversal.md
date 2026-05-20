# Programmer Handoff: OI-Price Divergence Reversal

**Date:** 2026-05-20
**Alpha ID:** CRYPTO-002
**Source Memo:** `research/memos/crypto/02_oi_momentum_reversal.md`
**Review Report:** `research/ideas/reviewed/CRYPTO-002_review.md`
**Status:** Pending Implementation

---

## 1. Alpha Summary

When perpetual futures open interest (OI) and spot price diverge in direction over a 7-day window — OI rising while price falls, or OI falling while price rises — the price move lacks structural support. Open interest measures capital commitment; when price moves against the OI signal, the trend is built on thinning depth. This creates a short-term reversal opportunity over 1-7 days. The signal is normalized by 30-day trailing volatility and filtered by funding rate extremes and quarterly expiry proximity. The signal is directional (long or short) on BTC and ETH perpetual futures.

**Verdict:** Conditional Pass — 5 mandatory conditions must be verified in the backtest (see Section 9).

---

## 2. Inputs

| Dataset | Fields | Frequency | Source | Min Coverage |
|---------|--------|-----------|--------|--------------|
| BTC perpetual OI | Open interest (USD) | Daily EOD | Binance API | 2019+ (3+ years) |
| ETH perpetual OI | Open interest (USD) | Daily EOD | Binance API | 2019+ (3+ years) |
| BTC spot price | OHLCV | Daily | Binance API | 2019+ |
| ETH spot price | OHLCV | Daily | Binance API | 2019+ |
| BTC 8h funding rate | Rate per 8h interval | 8h → daily mean | Binance API | 2019+ |
| ETH 8h funding rate | Rate per 8h interval | 8h → daily mean | Binance API | 2019+ |
| Futures expiry calendar | Quarterly/monthly expiry dates | Static | Exchange docs | Current year |

**Secondary source (cross-validation):** CoinGlass aggregated OI (paid API for historical data).

---

## 3. Preprocessing

1. **OI data quality filter (MANDATORY — Condition 2):** Cross-check daily OI change against cumulative traded volume. If the absolute difference between |ΔOI| and cumulative volume exceeds 20% of cumulative volume, discard the observation. The backtest report MUST state what percentage of observations were filtered out and whether filtered periods cluster around specific events.

2. **Funding rate aggregation:** Compute daily mean from 8h snapshots.

3. **Expiry filter:** Exclude any entry within 3 days of quarterly or monthly futures expiry.

4. **OI data source:** Binance API as primary. If CoinGlass aggregated OI is available, run the backtest on both and compare.

---

## 4. Signal Construction

**Step 1 — Compute 7-day changes:**
```
ΔOI_7d = (OI_today - OI_7d_ago) / OI_7d_ago
ΔPrice_7d = (Price_today - Price_7d_ago) / Price_7d_ago
```

**Step 2 — Detect divergence:**
```
DivScore = sign(ΔPrice_7d) × sign(ΔOI_7d)
```
Negative DivScore = divergence present.

**Step 3 — Compute divergence magnitude:**
```
DivMag = |ΔPrice_7d - ΔOI_7d|
```

**Step 4 — Normalize by trailing volatility:**
```
σ_30d = 30-day rolling standard deviation of daily price returns
NormDiv = DivMag / σ_30d
```

**Step 5 — Entry conditions (ALL must be true):**
- DivScore < 0 (divergence present)
- NormDiv > 1.5 (divergence is significant relative to recent vol)
- Funding rate is NOT in top or bottom decile of its 30-day range (avoid catching extremes)
- Position is not within 3 days of quarterly/monthly expiry

**Step 6 — Signal direction:**
- If ΔOI_7d > 0 and ΔPrice_7d < 0 → LONG (OI rising, price falling — capital is flowing in opposite direction to price)
- If ΔOI_7d < 0 and ΔPrice_7d > 0 → SHORT (OI falling, price rising — trend lacks structural support)

**Step 7 — Entry timing:** 00:00 UTC daily evaluation. Enter at the earliest available price after signal generation.

**Step 8 — Exit conditions (ANY triggers exit):**
- Holding period reaches N days (sweep N = 1, 2, 3, 5, 7)
- OI and price re-align (same direction) for 2 consecutive days
- Stop-loss hit at 2 × ATR(14) from entry

---

## 5. Portfolio Construction

| Parameter | Value |
|-----------|-------|
| Position sizing | 1% risk per trade; position size = (1% of capital) / (ATR × contract multiplier) |
| Max concurrent positions | 3 (across both BTC and ETH) |
| Leverage | None (cash-funded) |
| Rebalance frequency | Daily signal check at 00:00 UTC |
| Universe filtering | Exclude during 3-day expiry windows; exclude if OI quality flag triggered |

---

## 6. Transaction Cost Assumptions

| Item | Assumption |
|------|------------|
| Taker fee | 0.04% per trade (Binance tier) |
| Round-trip cost | 0.08% per signal |
| BTC slippage | 0.01-0.03% (stress-test at 0.06%) |
| ETH slippage | 0.03-0.08% (stress-test at 0.16%) |
| Funding cost (variable) | 0.006-0.15% over 2-5 day hold |
| **Total mean scenario** | **0.15-0.35% round-trip** |
| Gross return target | Must exceed 1% per signal to be viable after costs |

---

## 7. Backtest Specification

| Parameter | Value |
|-----------|-------|
| In-sample period | 2019-01-01 to 2022-12-31 |
| Out-of-sample period | 2023-01-01 to 2025-12-31 |
| Walk-forward design | Fixed in-sample/out-of-sample split (not rolling) |
| Benchmark | Buy-and-hold BTC and ETH; also condition 1 control test |
| Universe | BTC perpetual, ETH perpetual (spot-referenced) |
| Rebalance frequency | Daily at 00:00 UTC |
| Holding period sweep | N = 1, 2, 3, 5, 7 days |
| Data frequency | Daily EOD bars |
| Position type | Directional long or short |

---

## 8. Edge Cases

- **Quarterly expiry:** OI contracts mechanically during roll periods, generating false divergence. Mitigation: calendar filter.
- **Zero or negative OI:** OI can approach zero for less-liquid contracts. Mitigation: exclude when OI < minimum threshold ($10M).
- **Exchange downtime:** Binance API may have gaps. Mitigation: forward-fill OI for up to 24h; discard period if gap > 24h.
- **Extreme volatility events:** Flash crashes produce transient OI spikes from liquidations. Mitigation: NormDiv threshold; also Cap DivMag at 99.5th percentile.
- **Concurrent signals in same direction:** Both BTC and ETH may fire simultaneously. Mitigation: allow up to 3 concurrent positions; allocate risk-parity.
- **Multi-leg entry/exit timing:** Signal fires at 00:00 UTC, but entry price may differ. Use daily close of signal day as entry price (simulating limit orders).
- **Funding rate data gaps:** Exchange may skip 8h funding intervals. Mitigation: use most recent available rate; if gap > 24h, treat as missing and skip signal.

---

## 9. Validation Checks (5 Mandatory Conditions from Review)

### Condition 1: Control Test — Pure Price Reversal Benchmark
- [ ] Implement a control signal using identical mechanics but WITHOUT the OI component: compute 7-day price change, enter opposite direction, same hold/exits
- [ ] OI-enhanced signal must outperform on ≥2 of: Sharpe ratio, hit rate, max drawdown, Calmar ratio
- [ ] If OI-enhanced does not beat pure reversal → alpha fails; move to `research/ideas/rejected/`

### Condition 2: Operational Data Quality Filter
- [ ] OI-volume reconciliation check is applied before any signal generation
- [ ] Report % of observations filtered out
- [ ] Report whether filtered periods cluster around specific dates/events
- [ ] Optionally: compare filter rate for Binance vs CoinGlass OI

### Condition 3: Parameter Sensitivity Analysis
- [ ] Divergence threshold sweep: 1.0σ, 1.5σ (default), 2.0σ
- [ ] Lookback window sweep: 3-day, 7-day (default), 14-day
- [ ] Funding rate decile filter sweep: 5th/95th, 10th/90th (default), 15th/85th, no filter
- [ ] Volatility normalization window sweep: 14-day, 30-day (default), 60-day
- [ ] Report performance for each combination — not an optimization step, a robustness check

### Condition 4: Regime-Conditional Performance
- [ ] Classify each signal date into regime: trending up, trending down, range-bound (using 30-day ADX or equivalent)
- [ ] Report per-regime: signal count, hit rate, avg return/signal, Sharpe ratio
- [ ] If any regime has negative expected return, document with regime-filter recommendation

### Condition 5: Out-of-Sample Validation
- [ ] Train/optimize on 2019-2022
- [ ] Test on 2023-2025
- [ ] Report both in-sample and out-of-sample results
- [ ] If OOS performance degrades materially vs IS → reject the alpha

---

## 10. Outputs Expected

- [ ] **Metrics table:** Sharpe (annualized), hit rate, total return, max drawdown, Calmar ratio, avg holding period, number of signals, avg return per signal
- [ ] **Equity curve:** Cumulative PnL plot with in-sample / out-of-sample split marked
- [ ] **Control test comparison:** Side-by-side metrics for OI-enhanced vs pure price reversal
- [ ] **Parameter sensitivity heatmap:** Sharpe across threshold × lookback grid
- [ ] **Regime-conditional table:** Per-regime performance metrics
- [ ] **Data quality report:** % filtered, clustering analysis
- [ ] **Monthly return heatmap:** Calendar heatmap of monthly returns
- [ ] **Trade log:** CSV of every signal with entry/exit dates, direction, return, holding period, regime classification

---

## 11. Constraints

- **Do not** implement live trading or connect to broker APIs
- **Do not** place orders or simulate real-time monitoring
- **Do not** use any OI data from DEX venues (Chen, Ma, Nie 2024)
- **Do not** hardcode API keys. Use `.env` file with python-dotenv loading
- **Do not** modify the five-agent architecture, LLM Router, or any existing agent definitions
- This is a research backtest only — not a production trading signal

---

## 12. Data Source Contact

| Source | Endpoint | Key Required | Historical Available |
|--------|----------|-------------|---------------------|
| Binance API | `https://api.binance.com/api/v3/klines` (spot) | No (public) | 2017+ |
| Binance API | `https://fapi.binance.com/fapi/v1/openInterestHist` (perp OI) | No (public) | 2019+ |
| Binance API | `https://fapi.binance.com/fapi/v1/fundingRate` | No (public) | 2019+ |
| CoinGlass | `https://api.coinglass.com/api/...` | Yes (free tier available) | Varies by plan |

---

*Handoff prepared by: Research Agent*
*For: Programmer Agent*
*Review gate: Passed (Conditional — 5 conditions must be verified)*
