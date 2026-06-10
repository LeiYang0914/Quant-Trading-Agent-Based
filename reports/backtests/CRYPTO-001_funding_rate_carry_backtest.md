# Backtest Report — CRYPTO-001: Funding Rate Carry & Crowding Signal

**Programmer Agent**
**Date:** 2026-06-10
**Source Memo:** `research/memos/crypto/01_crypto_funding_rate_carry.md`
**Implementation:** `src/signals/funding_rate_carry.py`
**Backtest Engine:** `src/backtest/event_backtester.py`

---

## Backtest Configuration

| Parameter | Value |
|-----------|-------|
| Universe | BTCUSDT perpetual futures (synthetic) |
| Frequency | 8-hour (aligned with funding settlement) |
| Lookback window | 30 days |
| Funding threshold | 5.0% annualized |
| Crowding upper percentile | 90.0 |
| Crowding lower percentile | 10.0 |
| Max position size | 20% NAV |
| Rebalance frequency | 8h |
| Dynamic carry cap | 30.0% annualized |
| Taker fee | 4.0 bps |
| Maker fee | 2.0 bps |
| Slippage | 2.0 bps base |
| Initial capital | $100,000 |
| Carry leg enabled | True |
| Crowding leg enabled | True |
| Start date | 2024-01-01 08:00:00 |
| End date | 2024-12-30 16:00:00 |
| Bars simulated | 1094 |

---

## Performance Summary

| Metric | Value |
|--------|-------|
| Total return | -17.35% |
| Annualized return | -17.38% |
| Annualized volatility | 2.75% |
| Sharpe ratio | -8.38 |
| Sortino ratio | -11.01 |
| Calmar ratio | -0.98 |
| Max drawdown | 17.66% |
| Max drawdown duration | 361.3 days |
| Win rate | 0.0% |
| Avg win / avg loss | N/A |
| Total trades | 916 |
| Turnover | 14364% pa |
| Start equity | $100,000.00 |
| End equity | $82,639.81 |

---

## PnL Attribution

| Component | Value |
|-----------|-------|
| Funding PnL | $2,117.19 |
| Price PnL | $1,672.27 |
| Total fees | $14,099.77 |
| Total slippage | $7,049.88 |
| **Net PnL** | **$-17,360.19** |

---

## Signal Statistics

| Metric | Value |
|--------|-------|
| Total signal evaluations | 1095 |
| Carry-active periods | 871 (79.5%) |
| Crowding long signals | 110 |
| Crowding short signals | 123 |
| Crowding neutral periods | 862 |

### Funding Rate Distribution

| Statistic | Raw 8h Rate | Annualized % |
|-----------|------------|--------------|
| Mean | 0.000143 | 15.61% |
| Std | 0.000352 | 38.57% |
| Min | -0.000500 | -54.75% |
| 25% | 0.000047 | 5.20% |
| 50% | 0.000098 | 10.77% |
| 75% | 0.000148 | 16.22% |
| Max | 0.003000 | 328.50% |

---

## Equity Curve

The equity curve shows the NAV evolution bar-by-bar across the simulation period.
The initial capital of $100,000 ended at $82,639.81,
representing a total return of -17.35%.

Key characteristics:
- **Sharpe ratio:** -8.38 — Low (<0.5)
- **Max drawdown:** 17.66% — Moderate (10-20%)
- **Win rate:** 0.0%

---

## Transaction Cost Sensitivity

| Cost Multiplier | Notes |
|-----------------|-------|
| 0.5x baseline (2 bps taker) | Not simulated — synthetic data limits cost analysis |
| 1.0x baseline (4 bps taker) | Default Binance taker tier |
| 2.0x baseline (8 bps taker) | Stress scenario — expected Sharpe degradation |

---

## Edge Case Handling

| Edge Case | Behavior | Pass? |
|-----------|----------|-------|
| Empty input (no data) | Returns empty equity curve and positions | PASS |
| Single bar (no trade possible) | Returns empty result gracefully | PASS |
| Negative funding rate | Carry weight goes negative (short spot, long perp) | PASS |
| Extreme percentile (≥90) | Crowding signal = -1 (short) | PASS |
| Extreme percentile (≤10) | Crowding signal = +1 (long) | PASS |
| Missing funding data gaps | Forward-fill up to 1 period; discard if >24h gap | PASS |
| Multi-constraint position sizing | Tightest limit (NAV%, leverage, ATR, liquidity) wins | PASS |
| Drawdown risk limits | 10% → half size; 20% → stop; new peak → resume | PASS |
| NaN percentile input | Treated as neutral (signal = 0) | PASS |

---

## Backtest Assumptions

1. **Synthetic data:** The backtest uses generated data with plausible
   crypto-like statistical properties (autocorrelated funding rates,
   GBM spot prices with ~60% annual vol). Real Binance data should
   replace this for production use.

2. **No lookahead bias:** Signals are computed at bar *t* close using
   only data available through *t*. Positions are entered at bar *t+1*
   open. This is verified by the test suite.

3. **Liquidity unlimited:** The backtest assumes trades can be filled
   at the modeled slippage without market impact beyond the slippage
   model's linear assumption.

4. **No exchange downtime:** All bars are continuous. Real exchange
   maintenance windows and API outages are not modeled.

5. **Funding formula constant:** Assumes Binance's current funding
   formula throughout. Does not account for the 2021 formula change.

6. **Counterparty risk ignored:** No exchange failure modeling.
   The research memo flags this as a real risk.

7. **Single exchange:** All execution on one venue. Cross-exchange
   arbitrage complexities not modeled.

---

## Limitations & Next Steps

### MVP Limitations

1. **Synthetic data only** — real Binance API data needed for credible
   backtest results.
2. **Single asset** — BTCUSDT only; ETHUSDT and altcoin extension
   planned for v2.
3. **No parameter sweep** — thresholds not yet optimized via grid search.
4. **No regime analysis** — performance not yet split by bull/bear/sideways.
5. **No walk-forward** — in-sample only; out-of-sample validation pending.
6. **Fixed cost model** — no dynamic fee tiers or volume-based discounts.

### Next Steps (v2)

- [ ] Pull real Binance BTC/ETH funding rate + OHLCV data via API
- [ ] Run parameter sweep on lookback, thresholds, holding period
- [ ] Split performance by BTC regime (above/below 200d MA)
- [ ] Extend to ETHUSDT and top 5 alts
- [ ] Walk-forward validation with 6-month expanding windows
- [ ] Cost stress test (0.5x, 1x, 2x baseline)
- [ ] Compare crowding reversal standalone vs carry + crowding combined

---

## Test Results

All 106 trading-system tests pass (366 total passing out of 369;
3 pre-existing dashboard/LLM failures unrelated to CRYPTO-001):

| Test Suite | Tests | Status |
|------------|-------|--------|
| `tests/data/test_funding_rate_loader.py` | 12 | PASS All pass |
| `tests/signals/test_funding_rate_carry.py` | 25 | PASS All pass |
| `tests/backtest/test_metrics.py` | 16 | PASS All pass |
| `tests/backtest/test_event_backtester.py` | 13 | PASS All pass |
| `tests/execution/test_fee_model.py` | 9 | PASS All pass |
| `tests/execution/test_slippage_model.py` | 9 | PASS All pass |
| `tests/risk/test_drawdown.py` | 13 | PASS All pass |
| `tests/risk/test_position_sizing.py` | 9 | PASS All pass |
| **Total** | **106** | **100% pass** |

---

*Report generated by Programmer Agent*
*Reference: CRYPTO-001 | research/memos/crypto/01_crypto_funding_rate_carry.md*
