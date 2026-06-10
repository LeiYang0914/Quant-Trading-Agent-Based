# Backtest Report — CRYPTO-001: Funding Rate Carry & Crowding Signal

**Programmer Agent**
**Date:** 2026-06-11
**Data Source:** Glassnode API (real market data)
**Source Memo:** `research/memos/crypto/01_crypto_funding_rate_carry.md`
**Implementation:** `src/signals/funding_rate_carry.py`
**Backtest Engine:** `src/backtest/event_backtester.py`

---

## Backtest Configuration

| Parameter | Value |
|-----------|-------|
| Universe | BTCUSDT perpetual futures |
| Frequency | 8-hour (aligned with funding settlement) |
| Data source | Glassnode API (`futures_funding_rate_perpetual`, `price_usd_ohlc`) |
| Lookback window | 30 days |
| Funding threshold | 5.0% annualized |
| Crowding upper percentile | 90.0 |
| Crowding lower percentile | 10.0 |
| Max position size | 20% NAV |
| Rebalance threshold | 0.05 |
| Dynamic carry cap | 30.0% annualized |
| Taker fee | 4.0 bps |
| Maker fee | 2.0 bps |
| Slippage | 2.0 bps base |
| Initial capital | $100,000 |
| Carry leg | Enabled |
| Crowding leg | Enabled |
| In-sample period | 2023-01-01 to 2023-12-31 |
| Out-of-sample period | 2024-01-01 to 2025-12-31 |
| Bars simulated | 3,284 |

---

## Performance Summary

### Full Period (2023–2025)

| Metric | Value |
|--------|-------|
| Total return | -25.15% |
| Annualized return | -9.21% |
| Annualized volatility | 2.55% |
| Sharpe ratio | -5.35 |
| Sortino ratio | -6.21 |
| Calmar ratio | -0.35 |
| Max drawdown | 26.27% |
| Max drawdown duration | 1021.0 days |
| Win rate | 0.0% |
| Total trades | 1932 |
| Turnover | 8622% pa |
| Start equity | $100,000.00 |
| End equity | $74,844.92 |

### Subperiod Comparison

| Period | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| Full (2023–2025) | -25.15% | -5.35 | 26.27% |
| In-sample (2023) | -5.03% | -4.07 | 6.13% |
| Out-of-sample (2024–2025) | -21.08% | -5.90 | 22.02% |

---

## PnL Attribution (Full Period)

| Component | Value |
|-----------|-------|
| Funding PnL | $3,349.61 |
| Price PnL | $5,596.49 |
| Total fees | $22,734.12 |
| Total slippage | $11,367.06 |
| **Net PnL** | **$-25,155.08** |

---

## Signal Statistics (BTC, Full Period)

| Metric | Value |
|--------|-------|
| Total signal evaluations | 3,285 |
| Carry-active periods | 2,208 (67.2%) |
| Crowding long signals | 421 |
| Crowding short signals | 500 |

### Funding Rate Distribution (Real Data)

| Statistic | Raw 8h Rate | Annualized % |
|-----------|------------|--------------|
| Mean | 0.000076 | 8.29% |
| Std | 0.000087 | 9.49% |
| Min | -0.000376 | -41.22% |
| 25% | 0.000034 | 3.76% |
| 50% | 0.000064 | 7.06% |
| 75% | 0.000094 | 10.33% |
| Max | 0.000947 | 103.67% |

---

## Key Observations

1. **Data source:** Real Glassnode perpetual funding rate data (1h interval,
   resampled to 8h).  Funding rates represent the aggregate perpetual
   futures funding rate across major exchanges.

2. **In-sample vs out-of-sample:** The backtest distinguishes the 2023
   calibration period from the 2024–2025 forward test.  This aligns with
   the research memo's walk-forward design.

3. **No lookahead bias:** Signals are evaluated at bar *t* close using
   only data through *t*.  Positions are entered at bar *t+1* open.
   This is verified by the test suite.

4. **Funding rate regime:** The 2023–2025 period covers:
   - 2023: Crypto recovery / early bull
   - 2024: Bitcoin ETF approvals, institutional inflows, halving
   - 2025: Mature bull / potential regime shift in funding dynamics

5. **Cost sensitivity:** Base fees (4 bps taker + 2 bps slippage) are
   conservative for BTC-sized trades.  A cost sensitivity sweep is
   planned for v2.

---

## Comparison: Real vs Synthetic Data

| Metric | Synthetic (Report v1) | Real Glassnode |
|--------|----------------------|----------------|
| Data | GBM random walk | Actual market data |
| Funding rate | Random noise with spikes | Real exchange funding rates |
| Price | Simulated ~60% vol | Actual BTC spot prices |
| Date range | Simulated 2024 | 2023-01-01 to 2025-12-31 |

---

## Backtest Assumptions

1. **Real Glassnode funding rates** — aggregated across major exchanges.
   Individual exchange-level rates may differ (Binance vs Bybit vs OKX).

2. **No exchange downtime** — Glassnode data is continuous. Real exchange
   maintenance windows not modeled.

3. **Liquidity unlimited** — assumes fills at slippage model without
   market impact beyond linear assumption.

4. **Mark price ≈ spot price** — for PnL calculation. In reality, the
   perpetual mark price can diverge from spot (basis).

5. **Direct data access** — no API rate limits or authentication
   failures in the fetched dataset.

---

## Limitations & Next Steps

### v1 (Real Data)

- [x] Real Glassnode BTC funding rate data
- [x] In-sample vs out-of-sample split
- [x] 8h frequency backtest
- [ ] ETHUSDT extension (data loaded, backtest pending)
- [ ] Parameter sweep (lookback, thresholds)
- [ ] Regime analysis (bull/bear/sideways)
- [ ] Cost sensitivity sweep
- [ ] Walk-forward with expanding windows
- [ ] Real mark price data (currently approximating with spot)

### v2 (Planned)

- [ ] Multi-exchange funding rate data (Binance, Bybit, OKX individual)
- [ ] DEX venue comparison (Drift, Hyperliquid)
- [ ] Cross-sectional altcoin carry (top 20 by OI)
- [ ] Dynamic parameter optimization
- [ ] Live paper trading simulation

---

## Test Results

All 106 trading-system tests pass (validated with the same signal and
backtest modules used in this report — the only change is the data input).

---

*Report generated by Programmer Agent*
*Data: Glassnode API via `src/data/glassnode_loader.py`*
*Reference: CRYPTO-001 | research/memos/crypto/01_crypto_funding_rate_carry.md*
