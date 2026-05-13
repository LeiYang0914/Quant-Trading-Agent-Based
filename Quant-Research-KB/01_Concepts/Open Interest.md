---
title: "Open Interest"
type: concept
status: reference
created: 2026-05-14
updated: 2026-05-14
tags:
  - concept
  - open_interest
aliases:
  - OI
  - open interest
---

# Open Interest

## Definition
The total number of outstanding futures or options contracts that have not been settled, closed, or exercised. Each open contract represents one long and one short position. OI increases when a new buyer and seller enter a trade; decreases when both close existing positions; stays flat when one existing holder closes to a new entrant.

## Why OI Matters for Alpha
OI measures **market participation**, not direction. It answers: "Is new capital entering or exiting this market?" This is distinct from price (which measures valuation) and volume (which measures activity). The three together — price, volume, OI — provide a more complete picture than any single metric.

## Key Relationships
- **OI + Price:** Four-quadrant framework mapping trend strength/weakness
- **OI + Volatility:** Negative relationship — higher OI = deeper markets = lower vol (Bessembinder & Seguin 1993; Matsui et al. 2022)
- **OI + Funding Rate:** High OI + extreme funding = crowded directional positioning, vulnerable to unwind
- **OI + Volume:** OI/volume ratio reveals whether activity is opening new positions or closing existing ones

## Four-Quadrant Interpretation Framework

| Price Trend | OI Trend | Signal |
|-------------|----------|--------|
| Up | Up | Bullish — new money supports trend |
| Up | Down | Bearish reversal — uptrend losing participation |
| Down | Up | Reversal risk — shorts entering or longs capitulating |
| Down | Down | Bearish — trend unwinding, no new interest |

## Crypto-Specific Considerations
- Perpetual futures dominate OI (no expiry, continuous roll)
- OI data quality varies by exchange (Giagkiozis & Said 2024)
- Funding rate mechanism creates unique OI dynamics (crowded longs pay shorts)
- Liquidation cascades can rapidly change OI (forced closes)
- DEX perpetuals have different OI mechanics than CEX (Chen, Ma, Nie 2024)

## Data Sources
- CoinGlass (aggregated, reconciled OI across exchanges)
- Coinalyze (similar aggregation)
- Binance API (single-exchange, high quality)
- Bybit, OKX APIs (alternative single-exchange sources)

## Key Papers
- Bessembinder & Seguin (1993) — OI-volume-volatility relationship in futures (foundational)
- Giagkiozis & Said (2024) — OI misreporting in crypto perpetual swaps
- Matsui, Al-Ali, Knottenbelt (2022) — Extends B&S 1993 to crypto futures

## Related Concepts
- [[Mean Reversion]]
- [[Momentum]]
- [[Crowding]]
- [[Volatility Regime]]
- [[Liquidity]]
- [[Market Microstructure]]
