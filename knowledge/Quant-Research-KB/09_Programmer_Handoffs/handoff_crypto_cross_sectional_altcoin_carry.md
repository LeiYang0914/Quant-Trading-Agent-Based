---
title: "Programmer Handoff: Cross-Sectional Altcoin Funding Rate Carry"
type: programmer_handoff
status: pending
created: 2026-05-14
updated: 2026-05-14
tags:
  - programmer_handoff
  - crypto
  - carry
  - funding_rate
  - cross_sectional
source_alpha: "[[crypto_cross_sectional_altcoin_carry]]"
research_owner: Quant Research Agent
implementation_owner: Quant Trading Programmer Agent
handoff_version: 1
---

# Programmer Handoff: Cross-Sectional Altcoin Funding Rate Carry

## Handoff Summary
- **Alpha idea:** [[crypto_cross_sectional_altcoin_carry]]
- **Research memo:** `research_memos/crypto/03_cross_sectional_altcoin_funding_carry.md`
- **Full handoff:** `handoff_to_programmer/pending/03_cross_sectional_altcoin_funding_carry_handoff.md`
- **Date handed off:** 2026-05-14
- **Handoff version:** 1

## Alpha Summary
A market-neutral, cross-sectional carry strategy that goes long the highest-funding-rate altcoin perpetual futures and short the lowest-funding-rate altcoin perpetual futures across a universe of 20-30 altcoins (excluding BTC, ETH, stablecoins). Rebalances every 8 hours at funding settlement. Core academic reference: Fan et al. (2024) documents Sharpe 0.74 for similar construction.

## Market & Universe
| Parameter | Value |
|-----------|-------|
| Market | Crypto perpetual futures |
| Assets | Top 20-30 altcoins by market cap |
| Venues | Binance USDM (primary), Bybit, OKX |
| Timeframe | 8-hourly, aligned with funding settlement |

## Signal Specification (Plain English)
### Entry Logic
At each 8-hour funding settlement (00:00, 08:00, 16:00 UTC):
1. Collect most recent settled funding rate for each altcoin in the point-in-time universe
2. Rank altcoins cross-sectionally by funding rate (highest to lowest)
3. Q5 (top 20%) → go long the perpetual (collect high funding)
4. Q1 (bottom 20%) → go short the perpetual (pay low funding)
5. Enter positions at next bar open

### Exit Logic
- Rebalance at each funding settlement
- Position exits when funding rate rank drops below Q5 threshold (longs) or rises above Q1 threshold (shorts)
- Optional: minimum 24h holding period to reduce turnover whipsaw

### Position Sizing
- Equal weight within each leg; total long notional = total short notional (market-neutral)
- Cap single-position at 10% of gross exposure
- Winsorize funding rates at 5th/95th percentile before ranking

## Data Requirements
| Dataset | Fields | Frequency | Vendor | Access Method |
|---------|--------|-----------|--------|---------------|
| Altcoin perp funding rates | symbol, fundingRate, fundingTime | 8-hour | Binance API | `GET /fapi/v1/fundingRate` |
| Altcoin spot OHLCV | open, high, low, close, volume | 8-hour | Binance API | `GET /api/v3/klines` |
| Market cap | marketCap, totalVolume | Daily | CoinGecko API | `GET /api/v3/coins/markets` |
| Exchange info | listed symbols, contract details | Static | Binance API | `GET /fapi/v1/exchangeInfo` |

## Backtest Scope
| Parameter | Value |
|-----------|-------|
| In-sample | 2022-01-01 to 2023-12-31 |
| Out-of-sample | 2024-01-01 to 2025-12-31 |
| Walk-forward | 12-month expanding window |
| Benchmark | BTC spot B&H + cross-sectional momentum on same universe |
| Rebalance frequency | 8-hour (also test daily) |
| Transaction cost assumption | Tiered by altcoin liquidity bucket (0.07%-0.26% one-way) |

## Known Risk Factors
1. **Transaction cost overwhelm:** Altcoin spreads and fees can consume carry spread
2. **Momentum overlap:** High-FR alts = recent winners; must orthogonalize
3. **Survivorship bias:** Requires point-in-time universe construction
4. **Capacity limits:** $5-20M total notional
5. **Regime shift:** Arb capital migration may compress alpha over time

## What the Programmer Should Implement
- [ ] Pull funding rate + OHLCV + market cap data
- [ ] Construct point-in-time universe at each rebalance
- [ ] Implement quintile-based long-short signal
- [ ] Run walk-forward backtest with all robustness tests
- [ ] Report all evaluation metrics
- [ ] Test momentum-orthogonalized variant
- [ ] Estimate capacity curve

## What the Programmer Should NOT Implement
- [ ] Live trading or broker API connections
- [ ] Real-time signal generation
- [ ] Order placement or execution logic
- [ ] Multi-exchange deployment or routing

## Acceptance Criteria
- Net-of-costs Sharpe > 0.3 in out-of-sample (2024-2025)
- Alpha survives momentum orthogonalization (orthogonalized Sharpe > 0)
- Quintile returns show monotonicity (Q5 > Q1)

## Rejection Criteria
- Net-of-costs Sharpe < 0 in out-of-sample
- Signal is entirely momentum (zero alpha after orthogonalization)
- Turnover > 200% per day at any tested rebalance frequency

## Related Documents
- [[crypto_cross_sectional_altcoin_carry]] — Source alpha idea
- [[paper_fan_2024_crypto_carry_trade]] — Central academic reference
- [[paper_schmeling_2023_crypto_carry_bis]] — Carry economics
- [[Funding Rate]] — Core concept

---

*Handoff prepared by: Quant Research Agent*
*For: Quant Trading Programmer Agent*
*Implementation responsibility: Quant Trading Programmer Agent*
*Research responsibility: Quant Research Agent*
