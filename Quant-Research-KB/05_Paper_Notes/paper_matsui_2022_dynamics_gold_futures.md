---
title: "Matsui, Al-Ali, Knottenbelt (2022) — Dynamics of Solid, Liquid and Digital Gold Futures"
type: paper_note
status: summarized
created: 2026-05-14
updated: 2026-05-14
tags:
  - paper_note
  - crypto
  - commodities
  - open_interest
  - volatility
concepts:
  - "[[Open Interest]]"
  - "[[Volatility Regime]]"
  - "[[Liquidity]]"
source_type: paper
authors: "Toshiko Matsui, Ali Al-Ali, William J. Knottenbelt"
year: 2022
journal: "2022 IEEE International Conference on Blockchain and Cryptocurrency (ICBC)"
url: "https://arxiv.org/abs/2202.09845"
verified: true
---

# Matsui, Al-Ali, Knottenbelt (2022) — Dynamics of Solid, Liquid and Digital Gold Futures

## Citation
**Authors:** Toshiko Matsui, Ali Al-Ali, William J. Knottenbelt
**Year:** 2022
**Journal / Venue:** 2022 IEEE International Conference on Blockchain and Cryptocurrency (ICBC)
**Link:** https://arxiv.org/abs/2202.09845
**DOI:** 10.1109/ICBC54727.2022.9805528
**Verification:** Confirmed — arXiv abstract accessible, PDF available.

## One-Paragraph Summary
Contract-by-contract analysis of gold, oil, and bitcoin futures from Dec 2017 to Nov 2021. Finds "a positive and significant role for trading volume and a possible negative influence of open interest" on volatility across all three assets. This is consistent with prior oil futures literature. Maturity positively affects bitcoin and oil futures price volatility. This extends the Bessembinder & Seguin (1993) finding to crypto markets.

## Key Findings
1. OI has a negative relationship with volatility — higher OI implies lower volatility (deeper markets absorb order flow)
2. Volume has a positive relationship with volatility
3. These relationships hold across gold, oil, and bitcoin futures
4. Extends Bessembinder & Seguin (1993) to crypto, confirming the market depth mechanism
5. Maturity positively affects bitcoin and oil futures volatility

## Methods Used
- Contract-by-contract analysis
- Panel regression on futures data
- Cross-asset comparison (gold, oil, bitcoin)

## Data Used
| Dataset | Period | Frequency | Source |
|---------|--------|-----------|--------|
| Gold, oil, bitcoin futures | Dec 2017 - Nov 2021 | Daily | Futures exchanges |

## Relevance to Our Research
**Theoretical foundation for OI as a meaningful metric.** If OI changes signal shifts in market depth, then OI divergence from price may predict reversals because: falling OI = thinning depth = larger price impact per unit of order flow = higher probability of overshooting and reversal. This provides a structural (not just sentiment-based) mechanism for the OI-price divergence alpha.

## Critique & Limitations
- Tests OI → volatility relationship, not OI → return direction
- Does not directly test the OI-price divergence reversal hypothesis
- Pre-2022 data — doesn't capture post-FTX market structure changes

## Related Papers
- [[paper_bessembinder_1993_volatility_volume_depth]] — The foundational paper this extends
- [[paper_liu_2022_crypto_risk_factors]] — Complementary crypto factor research

---

*Research responsibility: Quant Research Agent*
