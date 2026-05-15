# Source Tracker

Registry of all sources consulted across all research memos. Each source has a structured ID, domain classification, and reliability tier.

## Source ID Format

```
{DOMAIN}-{TYPE}-{NNN}

Domain: CRYPTO | COMMOD | CROSS
Type:  PAPER | OFFICIAL | DATA | PRACT
```

## Source Tiers

| Tier | Description | Requirement |
|------|-------------|-------------|
| 1 | Peer-reviewed journals, conference papers, SSRN, arXiv, NBER, BIS, IMF, Fed, ECB | Preferred |
| 2 | Official exchange docs, CFTC, SEC, EIA, LBMA, World Gold Council | Acceptable |
| 3 | Practitioner research, institutional reports, well-known quant blogs | Supplementary only |

---

## Crypto — Academic Papers

| Source ID | Authors | Year | Title | Venue | DOI/arXiv/SSRN | URL | Tier | Ideas Supported | Verified |
|-----------|---------|------|-------|-------|----------------|-----|------|-----------------|----------|
| CRYPTO-PAPER-001 | He, Manela, Ross, von Wachter | 2022 | Fundamentals of Perpetual Futures | arXiv | arXiv:2212.06888 | https://arxiv.org/abs/2212.06888 | 1 | CRYPTO-001, CRYPTO-003 | Yes |
| CRYPTO-PAPER-002 | Schmeling, Schrimpf, Todorov | 2023 | Crypto Carry | BIS WP No. 1087 | — | https://www.bis.org/publ/work1087.htm | 1 | CRYPTO-001, CRYPTO-003 | Yes |
| CRYPTO-PAPER-003 | Christin, Routledge, Soska, Zetlin-Jones | — | The Crypto Carry Trade | CMU Working Paper | — | https://www.cmu.edu/tepper/faculty-and-research/research/working-papers/ | 1 | CRYPTO-001 | Yes |
| CRYPTO-PAPER-004 | Fan, Jiao, Lu, Tong | 2024 | The Risk and Return of Cryptocurrency Carry Trade | SSRN | SSRN:4666425 | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4666425 | 1 | CRYPTO-001, CRYPTO-003 | Yes |
| CRYPTO-PAPER-005 | Ackerer, Hugonnier, Jermann | 2025 | Perpetual Futures Pricing | Mathematical Finance | DOI:10.1111/mafi.12442 | https://onlinelibrary.wiley.com/doi/10.1111/mafi.12442 | 1 | CRYPTO-001 | Yes |
| CRYPTO-PAPER-006 | Inan | 2025 | Predictability of Funding Rates | SSRN | SSRN:5576424 | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5576424 | 1 | CRYPTO-001, CRYPTO-003 | Yes |
| CRYPTO-PAPER-007 | Liu, Tsyvinski, Wu | 2022 | Common Risk Factors in Cryptocurrency | Journal of Finance | DOI:10.1111/jofi.13195 | https://onlinelibrary.wiley.com/doi/10.1111/jofi.13195 | 1 | CRYPTO-001, CRYPTO-003 | Yes |
| CRYPTO-PAPER-008 | Giagkiozis & Said | 2024 | Reconciling Open Interest with Traded Volume in Perpetual Swaps | Ledger, Vol. 9 | arXiv:2310.14973 | https://arxiv.org/abs/2310.14973 | 1 | CRYPTO-002 | Yes |
| CRYPTO-PAPER-009 | Matsui, Al-Ali, Knottenbelt | 2022 | On the Dynamics of Solid, Liquid and Digital Gold Futures | IEEE ICBC 2022 | arXiv:2202.09845 | https://arxiv.org/abs/2202.09845 | 1 | CRYPTO-002 | Yes |
| CRYPTO-PAPER-010 | Chen, Ma, Nie | 2024 | Exploring the Impact: How Decentralized Exchange Designs Shape Traders' Behavior on Perpetual Future Contracts | arXiv | arXiv:2402.03953 | https://arxiv.org/abs/2402.03953 | 1 | CRYPTO-002 | Yes |
| CRYPTO-PAPER-011 | Bessembinder & Seguin | 1993 | Price Volatility, Trading Volume, and Market Depth: Evidence from Futures Markets | JFQA, Vol. 28, No. 1 | — | https://www.jstor.org/stable/2331234 | 1 | CRYPTO-002 | Yes |

## Crypto — Official / Institutional

| Source ID | Organization | Year | Title | URL | Tier | Ideas Supported | Verified |
|-----------|-------------|------|-------|-----|------|-----------------|----------|
| CRYPTO-OFFICIAL-001 | ScienceDirect | 2025 | Exploring Risk and Return Profiles of Funding Rate Arbitrage on CEX and DEX | https://www.sciencedirect.com/ | 2 | CRYPTO-001, CRYPTO-003 | Yes |
| CRYPTO-OFFICIAL-002 | BitMEX | 2025 | Q3 Derivatives Report | https://blog.bitmex.com/ | 2 | CRYPTO-001 | Yes |

## Crypto — Practitioner

| Source ID | Source | Type | URL | Tier | Ideas Supported | Verified |
|-----------|--------|------|-----|------|-----------------|----------|
| CRYPTO-PRACT-001 | Wikipedia — Open interest (four-quadrant framework) | Encyclopedia | https://en.wikipedia.org/wiki/Open_interest | 3 | CRYPTO-002 | Yes |
| CRYPTO-PRACT-002 | CryptoSlate — Open Interest Tag Archive | News/Analysis | https://cryptoslate.com/tag/open-interest/ | 3 | CRYPTO-002 | Yes |
| CRYPTO-PRACT-003 | Crypto-News-Flash — CME Bitcoin OI Analysis | News/Analysis | https://crypto-news-flash.com/glossary/open-interest/ | 3 | CRYPTO-002 | Yes |
| CRYPTO-PRACT-004 | Medium / Coinmonks — OI and Funding Rate: The Two Market Signals Most Crypto Traders Ignore | Blog | https://medium.com/tag/open-interest | 3 | CRYPTO-002 | Yes |
| CRYPTO-PRACT-005 | Glassnode Insights — Market Pulse | Institutional Research | https://insights.glassnode.com/ | 3 | CRYPTO-002 | Yes |

## Crypto — Data Vendors

| Source ID | Name | What It Provides | Referenced In | Notes |
|-----------|------|------------------|---------------|-------|
| CRYPTO-DATA-001 | Binance API | Funding rates, spot OHLCV, mark/index prices, open interest, liquidations | CRYPTO-001 | Free, primary source |
| CRYPTO-DATA-002 | CoinGlass | Multi-exchange OI-weighted funding rates, liquidation data, long/short ratio | CRYPTO-001, CRYPTO-002, CRYPTO-003 | Free tier; API paid |
| CRYPTO-DATA-003 | Tardis.dev | Historical crypto order book and trade data | CRYPTO-001 | Paid, deep history |
| CRYPTO-DATA-004 | Kaiko | Institutional crypto market data | CRYPTO-001 | Paid |
| CRYPTO-DATA-005 | Bybit API | Funding rates, mark prices | CRYPTO-001 | Free |
| CRYPTO-DATA-006 | OKX API | Funding rates, mark prices | CRYPTO-001 | Free |
| CRYPTO-DATA-007 | Coinalyze | Aggregated open interest, liquidations | CRYPTO-001 | Free tier |
| CRYPTO-DATA-008 | Glassnode Pro | On-chain and derivatives metrics | CRYPTO-001 | Paid |
| CRYPTO-DATA-009 | CryptoQuant | Exchange flows, on-chain data | CRYPTO-001 | Paid |
| CRYPTO-DATA-010 | CoinGecko API | Cryptocurrency market cap, circulating supply, trading volume (daily) | CRYPTO-003 | Free tier; point-in-time universe construction |

---

## Commodities — Academic Papers

| Source ID | Authors | Year | Title | Venue | DOI/arXiv/SSRN | URL | Tier | Ideas Supported | Verified |
|-----------|---------|------|-------|-------|----------------|-----|------|-----------------|----------|
| *(No commodities academic sources recorded yet)* | | | | | | | | | |

## Commodities — Official / Institutional

| Source ID | Organization | Year | Title | URL | Tier | Ideas Supported | Verified |
|-----------|-------------|------|-------|-----|------|-----------------|----------|
| *(No commodities official sources recorded yet)* | | | | | | | | |

## Commodities — Practitioner

| Source ID | Source | Type | URL | Tier | Ideas Supported | Verified |
|-----------|--------|------|-----|------|-----------------|----------|
| *(No commodities practitioner sources recorded yet)* | | | | | | | | |

## Commodities — Data Vendors

| Source ID | Name | What It Provides | Referenced In | Notes |
|-----------|------|------------------|---------------|-------|
| *(No commodities data vendors recorded yet)* | | | | | |

---

## Cross-Market — Academic Papers

| Source ID | Authors | Year | Title | Venue | DOI/arXiv/SSRN | URL | Tier | Ideas Supported | Verified |
|-----------|---------|------|-------|-------|----------------|-----|------|-----------------|----------|
| *(No cross-market academic sources recorded yet)* | | | | | | | | |

---

## Source Counts

| Domain | Tier 1 | Tier 2 | Tier 3 | Data Vendors | Total |
|--------|--------|--------|--------|-------------|-------|
| Crypto | 11 | 2 | 5 | 10 | 28 |
| Commodities | 0 | 0 | 0 | 0 | 0 |
| Cross-market | 0 | 0 | 0 | 0 | 0 |
| **Total** | **11** | **2** | **5** | **10** | **28** |
