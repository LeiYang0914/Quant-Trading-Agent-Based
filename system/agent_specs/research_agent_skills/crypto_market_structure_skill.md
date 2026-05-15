# crypto_market_structure_skill.md

## Purpose

Ensure crypto alpha research is professional, venue-aware, and grounded in real market microstructure. Every crypto research memo must demonstrate understanding of how crypto markets actually operate.

## When to Use

Whenever the session domain is `crypto`. Apply before writing a crypto alpha discovery note or research memo. This skill provides the structural context that separates professional crypto research from superficial pattern-spotting.

## Core Market Structure Topics

### 1. Perpetual Futures (Primary Instrument)
- **Funding rate mechanism:** Periodic payments between longs and shorts to anchor perp to spot. Typically every 8 hours on major CEXs.
- **Funding rate formula:** `FR = premium_index + clamp(impact_bid/ask - index, -0.05%, 0.05%)` (varies by exchange)
- **Funding rate as sentiment:** Persistently positive = bullish leverage demand. Persistently negative = bearish.
- **Funding rate as carry:** Can be harvested via delta-neutral spot+perp positions.
- **Funding rate extremes as reversal signal:** Extreme positive funding → long crowding → liquidation cascade risk.

### 2. Open Interest
- **Definition:** Total number of outstanding contracts (long+short).
- **OI vs. volume:** OI is a stock (positions held); volume is a flow (positions traded).
- **OI + price framework:** Rising OI + rising price = bullish (new money entering). Rising OI + falling price = bearish. Falling OI + rising price = weak rally. Falling OI + falling price = liquidation-driven.
- **OI data quality:** Exchanges vary in reporting. CoinGlass and Coinalyze aggregate across venues. Some exchanges have been documented to misreport OI (Giagkiozis & Said 2024).
- **OI as liquidity proxy:** Higher OI = deeper order books = lower slippage (Bessembinder & Seguin 1993).

### 3. Basis (Spot-Perp Spread)
- **Definition:** Difference between perpetual futures price and spot price.
- **Basis = funding expectations:** Positive basis implies expected positive funding; negative basis implies expected negative funding.
- **Basis trading:** Buy spot, short perp → collect funding while hedged. Returns = funding received minus trading costs and cost of spot capital.

### 4. Liquidation Mechanics
- **Liquidation:** When margin falls below maintenance margin, the position is force-closed.
- **Cascades:** Large liquidations move price → more positions cross threshold → more liquidations → feedback loop.
- **Data:** Binance, Bybit, OKX report liquidation data. CoinGlass aggregates across venues.
- **Alpha relevance:** Liquidation clusters can signal local price extremes and reversal opportunities.

### 5. Exchange-Specific Rules (Must Identify Per Memo)

Every crypto memo must identify the relevant venue(s) and their specific rules:

| Exchange | Funding Interval | Key Features |
|----------|-----------------|--------------|
| Binance | 8 hours | Largest volume, most liquid perps |
| OKX | 8 hours | Unified account, portfolio margin |
| Bybit | 8 hours | USDC and USDT perps |
| Deribit | 8 hours | Options + perps, institutional focus |
| DEX (Hyperliquid, dYdX, Drift, ApolloX) | Varies (1h to 24h) | On-chain, different liquidity profiles |

### 6. Stablecoin Liquidity
- Stablecoin market cap changes (USDT, USDC mint/burn) can signal crypto-wide demand shifts.
- Stablecoin exchange inflows = buying power entering.
- Stablecoin dominance as a risk-off indicator.

### 7. Spot/Perp Relationships
- Spot volume precedes perp volume in some regimes.
- Spot-perp arbitrage keeps prices aligned under normal conditions.
- Divergence between spot and perp can signal stress or manipulation.

### 8. Borrow and Margin Mechanics
- Cross margin vs. isolated margin
- Initial margin vs. maintenance margin
- Auto-deleveraging (ADL) on some exchanges

### 9. Altcoin Liquidity Fragmentation
- Altcoin perps have lower liquidity than BTC/ETH perps.
- Altcoin spot-perp arbitrage is harder: fragmented spot custody, higher volatility, lower liquidity.
- This fragmentation is WHY cross-sectional altcoin strategies may have persistent alpha.

### 10. Maker/Taker Fees
- Typical fee tiers: maker 0.01-0.02%, taker 0.04-0.075% on major CEXs.
- Altcoin perps and DEX venues can have higher fees.
- Fee tiers depend on 30-day volume.

### 11. Cross-Exchange Data Differences
- Funding rates are NOT identical across exchanges — they reflect venue-specific positioning.
- OI data may differ across venues due to reporting methodology.
- CoinGlass and Coinalyze provide OI-weighted aggregates — preferred for research.

### 12. Common Crypto Data Quality Problems
- **Exchange misreporting:** Some venues inflate volume or OI (Giagkiozis & Said 2024).
- **Survivorship bias:** Delisted altcoins disappear from historical data.
- **Lookahead bias risk:** Universe constituents change over time; point-in-time construction is critical.
- **Timestamp conventions:** Exchanges may differ in timezone and bar alignment.

## Required Fields for Every Crypto Memo

Every crypto research memo must clearly identify:
- **Venue(s):** Which exchange(s) is the signal designed for?
- **Instrument type:** Perpetual futures, spot, or both?
- **Settlement asset:** USDT, USDC, inverse (coin-margined)?
- **Funding interval:** 8 hours, 1 hour, variable?
- **Leverage relevance:** Is this a delta-neutral strategy or directional? Does leverage amplify risk?
- **Liquidity constraints:** What is the capacity? Which leg is the bottleneck?
- **Data vendor candidate(s):** Where would the Programmer Agent get this data?

## Inputs

- Domain context (always crypto for this skill)
- Alpha idea specifics
- Exchange documentation and data vendor methodology pages

## Outputs

- Market structure context integrated into the alpha discovery note or research memo
- Venue identification
- Liquidity and data quality assessment

## Anti-Patterns

- Writing about "funding rates" without specifying which exchange
- Treating all altcoins as having the same liquidity as BTC/ETH
- Ignoring exchange-specific OI reporting differences
- Assuming data quality is uniform across vendors
- Proposing a strategy without identifying the specific venue and its fee structure
