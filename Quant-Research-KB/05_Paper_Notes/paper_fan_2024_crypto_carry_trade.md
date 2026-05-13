---
title: "Fan, Jiao, Lu, Tong (2024) — The Risk and Return of Cryptocurrency Carry Trade"
type: paper_note
status: summarized
created: 2026-05-14
updated: 2026-05-14
tags:
  - paper_note
  - crypto
  - carry
  - funding_rate
  - cross_sectional
  - altcoins
concepts:
  - "[[Funding Rate]]"
  - "[[Carry]]"
  - "[[Momentum]]"
source_type: paper
authors: "Fan, Jiao, Lu, Tong"
year: 2024
journal: "SSRN Working Paper"
url: "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4666425"
verified: true
---

# Fan, Jiao, Lu, Tong (2024) — The Risk and Return of Cryptocurrency Carry Trade

## Citation
**Authors:** Fan, Jiao, Lu, Tong
**Year:** 2024
**Journal / Venue:** SSRN Working Paper
**Link:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4666425
**Verification:** Confirmed — accessible via browser; previously verified in Memo #01.

## One-Paragraph Summary
The central academic paper for cross-sectional crypto carry. The authors construct a cross-sectional carry trade across multiple crypto assets — going long the highest-funding-rate crypto perpetuals and short the lowest-funding-rate — documenting 43.4% annualized returns with Sharpe ratio of 0.74. Establishes that the cross-sectional funding rate spread is a harvestable alpha source distinct from directional crypto exposure.

## Key Findings
1. Cross-sectional crypto carry yields 43.4% annualized return with Sharpe 0.74
2. The alpha comes from persistent cross-sectional differences in funding rates
3. The strategy is market-neutral (long-short across assets), hedging directional risk
4. Funding rate rankings show cross-sectional persistence — high-FR assets tend to stay high-FR
5. The effect is strongest in smaller-cap crypto assets where arbitrage capital is most constrained

## Methods Used
- Cross-sectional portfolio sorts on funding rate
- Quintile-based long-short construction
- Multi-asset crypto carry return decomposition

## Data Used
| Dataset | Period | Frequency | Source |
|---------|--------|-----------|--------|
| Multi-asset crypto perpetual futures | Multi-year | Daily/8-hourly | Major CEX venues |

## Relevance to Our Research
This is the primary academic reference for Memo #03 (Cross-Sectional Altcoin Funding Rate Carry). The 43.4% / Sharpe 0.74 finding provides the benchmark expectation. The paper validates the carry capture direction (going WITH high relative funding, not against it). The finding that cross-sectional carry works better in smaller-cap assets directly supports the altcoin-focused scope.

## Critique & Limitations
- Returns may be overstated if survivorship bias is not fully addressed
- Transaction costs for altcoin perps (especially smaller caps) may be understated
- Sample period likely includes the 2020-2021 highly anomalous crypto bull market
- Working paper — not yet published in a peer-reviewed journal

## Key Quotes
> "A cross-sectional carry trade across multiple crypto assets yields 43.4% annualized returns with Sharpe ratio of 0.74."

## Related Papers
- [[paper_schmeling_2023_crypto_carry_bis]] — Foundational crypto carry economics
- [[paper_liu_2022_crypto_risk_factors]] — Cross-sectional momentum in crypto (factor overlap concern)
- [[paper_inan_2025_funding_rate_predictability]] — Funding rate persistence evidence

---

*Research responsibility: Quant Research Agent*
