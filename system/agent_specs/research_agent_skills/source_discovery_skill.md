# source_discovery_skill.md

## Purpose

Help the Research Agent find, evaluate, and record high-quality sources for alpha research. Enforce the source quality hierarchy and ensure every source is traceable.

## When to Use

After the domain is declared and the alpha idea is selected. Use before writing any discovery note or memo. Repeat whenever additional sources are needed during research.

## Source Quality Hierarchy

### Tier 1 — Preferred (Academic & Official Research)
- Peer-reviewed journal papers (Journal of Finance, Review of Financial Studies, etc.)
- Conference papers (IEEE ICBC, ACM, NeurIPS fin-ml workshops)
- SSRN working papers (ssrn.com)
- arXiv preprints (q-fin, stat, cs.CE categories)
- NBER working papers (nber.org)
- BIS working papers and reports (bis.org)
- IMF working papers (imf.org)
- Federal Reserve / ECB working papers
- Bank for International Settlements publications

**Search strategy for Tier 1:**
- SSRN: search by topic keywords, filter by download count and date
- arXiv: search q-fin.TR (trading), q-fin.ST (statistics), q-fin.RM (risk management)
- Google Scholar: search by topic, check citation count and recency, follow citation chains
- BIS.org: check working papers and quarterly reviews
- NBER.org: search by program (Asset Pricing, International Finance)
- Institutional author pages: check recent publications by known quant finance academics

### Tier 2 — Acceptable (Official & Exchange Documentation)
- Exchange documentation: CME, ICE, LME, Binance, OKX, Bybit, Deribit
- CFTC Commitments of Traders reports (cftc.gov)
- SEC filings and reports
- EIA (Energy Information Administration) data and reports
- LBMA (London Bullion Market Association) data
- World Gold Council reports
- Official data vendor methodology documentation (CoinGlass, Kaiko, Glassnode methodology pages)

**Search strategy for Tier 2:**
- Exchange official websites: look for API docs, fee schedules, contract specs, methodology pages
- CFTC.gov: COT reports, market reports, enforcement actions
- EIA.gov: STEO, weekly petroleum status, natural gas storage
- World Gold Council: gold demand trends, ETF flows
- Data vendor websites: methodology and coverage documentation

### Tier 3 — Supplementary Only (Practitioner Research)
- Reputable practitioner research (Two Sigma Insights, AQR papers, Man AHL)
- Institutional research (J.P. Morgan, Goldman Sachs, Citadel — when publicly available)
- Exchange research reports (Binance Research, Bybit Research)
- Well-known quant blogs (Quantocracy, Alpha Architect, FactorResearch — only when methodology is explicit)

### Rejected Sources (Never Use)
- Anonymous tweets or social media posts
- Unsourced blog posts
- Marketing pages and promotional content
- Low-quality SEO articles
- Forum speculation (Reddit, 4chan, Discord)
- AI-generated summaries without verifiable source links
- Any source that does not provide a verifiable URL or DOI

## Minimum Source Requirements Per Alpha Idea

Before a discovery note can become a research memo:
- **At least 2 credible references**
- **At least 1 Tier 1 or Tier 2 source** (unless explicitly justified)
- All sources must have working URLs or DOIs

## How to Record a Source

Every source must be recorded in `memory/SOURCE_TRACKER.md` with:

```
Source ID: {DOMAIN-TYPE-NNN}
Domain: {crypto | commodities | cross_market}
Source type: {journal | conference | working_paper | official_doc | data_vendor | practitioner_research}
Title: {full title}
Authors / Organization: {names or organization}
Year: {YYYY}
Venue / Publisher: {journal, conference, or institution}
DOI / arXiv / SSRN: {ID if available}
URL: {full working URL — must resolve}
Reliability Tier: {1 | 2 | 3}
Ideas Supported: {alpha IDs}
Notes: {why this source is relevant — one sentence minimum}
```

Source ID format:
- `CRYPTO-PAPER-NNN` — crypto academic paper
- `CRYPTO-OFFICIAL-NNN` — crypto exchange or official documentation
- `CRYPTO-DATA-NNN` — crypto data vendor
- `CRYPTO-PRACT-NNN` — crypto practitioner source
- `COMMOD-PAPER-NNN` — commodities academic paper
- `COMMOD-OFFICIAL-NNN` — commodities official documentation
- `CROSS-PAPER-NNN` — cross-market paper

## How to Identify Weak Sources

A source should be **rejected or flagged** if:
- No author name or institution is provided
- No publication date
- No methodology description
- Claims are not backed by data or references
- The URL is dead or redirects to unrelated content
- The source is a content farm or SEO-optimized article
- The source makes exaggerated claims ("guaranteed alpha," "100% win rate")

## Verifying Sources

- If a source is a paper: confirm it exists on SSRN, arXiv, the journal website, or the author's institutional page
- If a source is an exchange document: confirm it exists on the official exchange website
- If a source is from a data vendor: confirm the methodology page is current
- Cross-check major claims against at least one other source

## Inputs

- Alpha idea and domain
- WebSearch and WebFetch results
- `memory/SOURCE_TRACKER.md` — existing sources (avoid duplication)

## Outputs

- Updated `memory/SOURCE_TRACKER.md` with new structured entries
- Source list for the alpha discovery note or research memo

## Anti-Patterns

- Citing a source by name only without a URL ("BIS paper on crypto carry")
- Using Tier 3 sources when Tier 1/2 sources exist on the same topic
- Recording a source without checking if the URL resolves
- Accepting AI-generated summaries as authoritative without verifying the original source
