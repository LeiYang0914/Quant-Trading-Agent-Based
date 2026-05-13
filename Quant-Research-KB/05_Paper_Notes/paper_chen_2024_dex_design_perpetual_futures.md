---
title: "Chen, Ma, Nie (2024) — How DEX Designs Shape Traders' Behavior on Perpetual Futures"
type: paper_note
status: summarized
created: 2026-05-14
updated: 2026-05-14
tags:
  - paper_note
  - crypto
  - open_interest
  - market_microstructure
  - dex
concepts:
  - "[[Open Interest]]"
  - "[[Perpetual Futures]]"
  - "[[Market Microstructure]]"
source_type: paper
authors: "Erdong Chen, Mengzhong Ma, Zixin Nie"
year: 2024
journal: "arXiv preprint"
url: "https://arxiv.org/abs/2402.03953"
verified: true
---

# Chen, Ma, Nie (2024) — How DEX Designs Shape Traders' Behavior on Perpetual Futures

## Citation
**Authors:** Erdong Chen, Mengzhong Ma, Zixin Nie
**Year:** 2024
**Journal / Venue:** arXiv preprint
**Link:** https://arxiv.org/abs/2402.03953
**Verification:** Confirmed — arXiv abstract accessible.

## One-Paragraph Summary
Categorizes perpetual exchange architectures into three models: VAMM DEX, Oracle Pricing DEX, and CLOB CEX. Finds that in VAMM-based DEXs, OI has a "differential impact on open interest on long versus short positions." Less informed traders "overreact to positive news, as demonstrated by an increase in long positions." Under Oracle Pricing models, traders act as price takers whose "trading actions reflect direct responses to price movements."

## Key Findings
1. OI dynamics differ between CEX and DEX perpetuals — the signal is not uniform
2. On VAMM DEXs: OI has differential impact on long vs. short positions
3. Less informed traders on DEXs overreact to positive news (long OI spike)
4. Oracle Pricing DEXs: traders are price takers responding directly to price
5. CLOB CEXs have the most interpretable OI signals

## Methods Used
- Classification of exchange architectures
- Behavioral analysis of trader types by venue

## Data Used
| Dataset | Period | Frequency | Source |
|---------|--------|-----------|--------|
| DEX and CEX perpetual futures data | Not specified | Not specified | Multiple venues |

## Relevance to Our Research
**Venue scoping for OI signals.** For OI-based alpha, CLOB CEX data is preferred. DEX OI signals are contaminated by AMM mechanics and behave differently. Recommendation: scope the OI reversal alpha to CEX perpetuals only (Binance, Bybit, OKX). DEX OI patterns (Drift, ApolloX, Hyperliquid) could be a separate alpha idea.

## Critique & Limitations
- Preprint — not yet peer reviewed
- Does not quantify the magnitude of DEX vs. CEX OI signal differences
- Behavioral claims about "less informed traders" need stronger identification

## Related Papers
- [[paper_giagkiozis_2024_oi_reconciliation_perps]] — Complementary OI data quality concerns

---

*Research responsibility: Quant Research Agent*
