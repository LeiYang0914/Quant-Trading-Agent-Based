---
title: "Funding Rate"
type: concept
status: reference
created: 2026-05-14
updated: 2026-05-14
tags:
  - concept
  - funding_rate
  - carry
  - perpetual_futures
aliases:
  - funding rates
  - perpetual funding
---

# Funding Rate

## Definition
A periodic payment exchanged between long and short holders of perpetual futures contracts, designed to tether the perpetual contract price to the underlying spot index price. When the perpetual trades above spot (premium), longs pay shorts. When the perpetual trades below spot (discount), shorts pay longs. Payments typically occur every 8 hours.

## Mechanism
- Funding rate is proportional to the basis (premium/discount of perp vs. spot)
- Typically includes an interest rate component (spread between base and quote currency rates) and a premium index component
- Most exchanges cap funding rates at a maximum (e.g., ±0.375% or ±0.75% per 8h) or use a clamp function
- The rate is determined at settlement time based on the premium over the preceding period

## Why Funding Rates Matter for Alpha
Funding rates reveal:
1. **Directional positioning imbalance:** Persistently positive funding = more longs than shorts (bullish sentiment). Persistently negative = more shorts than longs (bearish sentiment).
2. **Arbitrage capital constraints:** High absolute funding that persists indicates limited arbitrage capital — the carry trade is not being fully exploited.
3. **Crowding risk:** Extremely positive funding + high OI = crowded longs vulnerable to liquidation cascades.
4. **Cross-sectional dispersion:** Different assets have different funding rates at the same time — this dispersion is a harvestable alpha source.

## Absolute vs. Cross-Sectional Funding Rate Signals

| Dimension | Absolute (Time-Series) | Cross-Sectional |
|-----------|----------------------|-----------------|
| What it measures | Is this asset's funding rate high relative to its own history? | Is this asset's funding rate high relative to other assets right now? |
| Signal type | Reversal / crowding | Carry capture |
| Example alpha | BTC funding at 90th percentile of 30-day range → short | Altcoin perp has top-quintile FR among top-30 altcoins → long the perp |
| Direction risk | Exposed to market direction (single-asset) | Market-neutral (long-short across assets) |
| Key reference | Schmeling et al. (2023) — high carry predicts crashes | Fan et al. (2024) — cross-sectional carry Sharpe 0.74 |

## Crypto-Specific Considerations
- 8-hour funding settlement is standard across CEX venues (00:00, 08:00, 16:00 UTC)
- Funding is collected/received automatically — no action needed from the trader
- Funding rate can be annualized as: `FR * 3 * 365` for 8-hourly rates
- During extreme bull markets, funding rates can stay elevated for weeks (not mean-reverting in the short term)
- Data quality: some exchanges systematically misreport or delay funding rate updates

## Key Papers
- He, Manela, Ross, von Wachter (2022) — No-arbitrage perpetual pricing framework
- Schmeling, Schrimpf, Todorov (2023) — Crypto Carry, BIS WP 1087
- Fan, Jiao, Lu, Tong (2024) — Cross-sectional crypto carry, SSRN:4666425
- Inan (2025) — Funding rate predictability
- Ackerer, Hugonnier, Jermann (2025) — Perpetual futures pricing theory

## Related Concepts
- [[Carry]]
- [[Open Interest]]
- [[Crowding]]
- [[Momentum]]
- [[Volatility Regime]]
- [[Liquidity]]
