---
title: "CoinGlass — Aggregated Crypto Derivatives Data"
type: data_source
status: documented
created: 2026-05-14
updated: 2026-05-14
tags:
  - data_source
  - crypto
  - open_interest
  - funding_rate
concepts:
  - "[[Open Interest]]"
vendor: CoinGlass
access: Free tier available; paid for API access
url: https://www.coinglass.com/
---

# CoinGlass — Aggregated Crypto Derivatives Data

## What It Provides
- Multi-exchange aggregated open interest (OI-weighted)
- Funding rates across exchanges
- Liquidation data (long/short liquidations)
- Long/short ratio
- Bitcoin and Ethereum futures ETF flow data
- Options data (open interest, volume, max pain)
- Historical data via API

## Key Datasets for Alpha Research
| Dataset | Fields | Frequency | History |
|---------|--------|-----------|---------|
| Aggregated OI | OI by asset, by exchange, aggregated | Daily (intraday via API) | Multi-year |
| Funding rates | Per-exchange and aggregated | 8-hourly | Multi-year |
| Liquidations | Long/short liquidation volume | Daily | Multi-year |
| Long/Short ratio | By exchange, aggregated | Daily | Multi-year |

## Data Quality Notes
- CoinGlass aggregates and reconciles OI across exchanges, which is important given [[paper_giagkiozis_2024_oi_reconciliation_perps]] findings on exchange misreporting
- OI data is OI-weighted across exchanges (not simple sum)
- Methodology documentation is limited (educational URLs return 404)
- Generally considered the most reliable aggregated crypto derivatives data source by practitioners

## Relevant Alpha Ideas
- [[crypto_oi_momentum_reversal]] — Primary OI data source
- Any funding rate carry strategy

## Access
- Web: https://www.coinglass.com/
- API: https://www.coinglass.com/api (requires API key, paid tiers)
- Free tier shows recent data; historical depth requires subscription

## Limitations
- API documentation is sparse
- Methodology for OI reconciliation is not publicly documented in detail
- Paid tiers required for programmatic access
- Data updates near real-time, but exact latency not documented

---

*Research responsibility: Quant Research Agent*
