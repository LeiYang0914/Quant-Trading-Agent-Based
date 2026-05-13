# Source Tracker

Registry of sources consulted across all research memos.

## Format

Each entry: source citation, type (paper / institutional report / blog / data vendor / tool), memos that reference it, verification status, and a **full working URL** (never a shorthand like "BIS.org" or "SSRN:12345" — always the complete URL or DOI that resolves).

---

## Academic Papers

| # | Citation | Type | Referenced In | Verified | Link |
|---|---|---|---|---|---|
| 1 | He, Manela, Ross, von Wachter (2022). "Fundamentals of Perpetual Futures." | Paper | Memo #01 | Yes | https://arxiv.org/abs/2212.06888 |
| 2 | Schmeling, Schrimpf, Todorov (2023). "Crypto Carry." BIS WP No. 1087 | Paper | Memo #01 | Yes | https://www.bis.org/publ/work1087.htm |
| 3 | Christin, Routledge, Soska, Zetlin-Jones. "The Crypto Carry Trade." | Paper | Memo #01 | Yes | https://www.cmu.edu/tepper/faculty-and-research/research/working-papers/ |
| 4 | Fan, Jiao, Lu, Tong (2024). "The Risk and Return of Cryptocurrency Carry Trade." | Paper | Memo #01 | Yes | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4666425 |
| 5 | Ackerer, Hugonnier, Jermann (2025). "Perpetual Futures Pricing." Mathematical Finance | Paper | Memo #01 | Yes | https://onlinelibrary.wiley.com/doi/10.1111/mafi.12442 |
| 6 | Inan (2025). "Predictability of Funding Rates." | Paper | Memo #01 | Yes | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5576424 |
| 7 | Liu, Tsyvinski, Wu (2022). "Common Risk Factors in Cryptocurrency." Journal of Finance | Paper | Memo #01 | Yes | https://onlinelibrary.wiley.com/doi/10.1111/jofi.13195 |

## Institutional Reports

| # | Source | Type | Referenced In | Verified | Link |
|---|---|---|---|---|---|
| 1 | BitMEX 2025 Q3 Derivatives Report | Exchange report | Memo #01 | Yes | https://blog.bitmex.com/ |
| 2 | ScienceDirect (2025). "Exploring Risk and Return Profiles of Funding Rate Arbitrage on CEX and DEX" | Journal article | Memo #01 | Yes | https://www.sciencedirect.com/ |

## Data Vendors & Tools

| # | Name | What It Provides | Referenced In | Notes |
|---|---|---|---|---|
| 1 | Binance API | Funding rates, spot OHLCV, mark/index prices, open interest, liquidations | Memo #01 | Free, primary source |
| 2 | CoinGlass | Multi-exchange OI-weighted funding rates, liquidation data | Memo #01 | Free tier available |
| 3 | Tardis.dev | Historical crypto order book and trade data | Memo #01 | Paid, deep history |
| 4 | Kaiko | Institutional crypto market data | Memo #01 | Paid |
| 5 | Bybit API | Funding rates, mark prices | Memo #01 | Free |
| 6 | OKX API | Funding rates, mark prices | Memo #01 | Free |
| 7 | Coinalyze | Aggregated open interest, liquidations | Memo #01 | Free tier |
| 8 | Glassnode Pro | On-chain and derivatives metrics | Memo #01 | Paid |
| 9 | CryptoQuant | Exchange flows, on-chain data | Memo #01 | Paid |

## Sources Added 2026-05-14 (Memo #02)

### Academic Papers

| # | Citation | Type | Referenced In | Verified | Link |
|---|---|---|---|---|---|
| 8 | Giagkiozis & Said (2024). "Reconciling Open Interest with Traded Volume in Perpetual Swaps." Ledger, Vol. 9 | Paper | Memo #02 | Yes | https://arxiv.org/abs/2310.14973 |
| 9 | Matsui, Al-Ali, Knottenbelt (2022). "On the Dynamics of Solid, Liquid and Digital Gold Futures." IEEE ICBC 2022 | Paper | Memo #02 | Yes | https://arxiv.org/abs/2202.09845 |
| 10 | Chen, Ma, Nie (2024). "Exploring the Impact: How Decentralized Exchange Designs Shape Traders' Behavior on Perpetual Future Contracts." | Paper | Memo #02 | Yes | https://arxiv.org/abs/2402.03953 |
| 11 | Bessembinder & Seguin (1993). "Price Volatility, Trading Volume, and Market Depth: Evidence from Futures Markets." JFQA, Vol. 28, No. 1 | Paper | Memo #02 | Yes | https://www.jstor.org/stable/2331234 |

### Practitioner / Institutional Sources

| # | Source | Type | Referenced In | Verified | Link |
|---|---|---|---|---|---|
| 3 | Wikipedia — "Open interest" (four-quadrant framework) | Encyclopedia | Memo #02 | Yes | https://en.wikipedia.org/wiki/Open_interest |
| 4 | CryptoSlate — Open Interest Tag Archive | News/Analysis | Memo #02 | Yes | https://cryptoslate.com/tag/open-interest/ |
| 5 | Crypto-News-Flash — CME Bitcoin OI Analysis | News/Analysis | Memo #02 | Yes | https://crypto-news-flash.com/glossary/open-interest/ |
| 6 | Medium / Coinmonks — "OI and Funding Rate: The Two Market Signals Most Crypto Traders Ignore" | Blog | Memo #02 | Yes | https://medium.com/tag/open-interest |
| 7 | Glassnode Insights — Market Pulse | Institutional Research | Memo #02 | Yes | https://insights.glassnode.com/ |

### Data Vendors & Tools

| # | Name | What It Provides | Referenced In | Notes |
|---|---|---|---|---|
| 10 | CoinGlass | Multi-exchange aggregated OI, funding rates, liquidations, long/short ratio | Memo #02, Memo #03 | Free tier; API paid. OI-weighted aggregation across exchanges. |
| 11 | CoinGecko API | Cryptocurrency market cap, circulating supply, trading volume (daily) | Memo #03 | Free tier; used for point-in-time universe construction by market cap rank. `GET /api/v3/coins/markets`.

## Sources Added 2026-05-14 (Memo #03)

### Data Vendors & Tools

| # | Name | What It Provides | Referenced In | Notes |
|---|---|---|---|---|
| 11 | CoinGecko API | Cryptocurrency market cap, circulating supply, trading volume (daily) | Memo #03 | Free tier; used for point-in-time universe construction by market cap rank. `GET /api/v3/coins/markets`.

### Note on Existing Sources Reused

Memo #03 reuses seven academic and institutional sources previously verified and tracked for Memo #01: Fan et al. 2024 (#4), Schmeling et al. 2023 (#2), Inan 2025 (#6), Liu et al. 2022 (#7), ScienceDirect 2025 (Institutional #2), He et al. 2022 (#1), and Ackerer et al. 2025 (#5). No new academic papers were added. The CoinGlass data vendor entry (#10) was updated to reflect usage in both Memo #02 and Memo #03.
