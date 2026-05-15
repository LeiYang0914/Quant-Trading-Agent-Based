---
title: "Schmeling, Schrimpf, Todorov (2023) — Crypto Carry"
type: paper_note
status: summarized
created: 2026-05-14
updated: 2026-05-14
tags:
  - paper_note
  - crypto
  - carry
  - funding_rate
  - crowding
concepts:
  - "[[Funding Rate]]"
  - "[[Carry]]"
  - "[[Crowding]]"
source_type: paper
authors: "Maik Schmeling, Andreas Schrimpf, Karamfil Todorov"
year: 2023
journal: "BIS Working Paper No. 1087 (revised October 2025)"
url: "https://www.bis.org/publ/work1087.htm"
verified: true
---

# Schmeling, Schrimpf, Todorov (2023) — Crypto Carry

## Citation
**Authors:** Maik Schmeling, Andreas Schrimpf, Karamfil Todorov
**Year:** 2023 (revised October 2025)
**Journal / Venue:** BIS Working Paper No. 1087
**Link:** https://www.bis.org/publ/work1087.htm
**Verification:** Confirmed — WebFetch successful; full abstract and findings extracted.

## One-Paragraph Summary
Documents that crypto carry (futures-spot basis) averages above 10% annually and can exceed 40% at peaks. The carry premium is driven by retail trend-chasing demand interacting with limited arbitrage capital. Critically, finds that high absolute carry predicts future price crashes — a crowding/reversal signal distinct from carry capture. The paper focuses on aggregate BTC/ETH rather than cross-sectional altcoin strategies.

## Key Findings
1. Crypto carry averages above 10% annually, exceeding 40% at peaks
2. Carry is driven by retail trend-chasing demand meeting limited arbitrage capital
3. High absolute carry predicts future price crashes (crowding signal)
4. Arbitrage capital constraints are the binding friction preventing carry compression
5. Carry is time-varying and regime-dependent

## Methods Used
- Empirical carry return computation from futures-spot basis
- Predictive regressions of returns on carry levels
- Time-series analysis of carry dynamics

## Data Used
| Dataset | Period | Frequency | Source |
|---------|--------|-----------|--------|
| BTC and ETH futures and spot | 2017-2023 | Daily | Major exchanges |

## Relevance to Our Research
**Foundational mechanism paper.** The "high carry predicts crashes" finding is the basis for Memo #01's Factor B (crowding reversal signal). The "retail demand + limited arb capital" framework is the theoretical foundation for why cross-sectional altcoin carry (Memo #03) should work: the same forces produce funding rate dispersion across altcoins. The key distinction this paper supports: absolute carry extremes → reversal (crowding); relative carry rankings → persistence (carry capture).

## Critique & Limitations
- Focuses on BTC/ETH, does not test cross-sectional altcoin strategies
- The "crash prediction" finding is time-series (single asset), not cross-sectional
- Results may be period-specific (2017-2023 includes unusual crypto bull market)

## Key Quotes
> "The crypto carry trade has offered very high unconditional returns, averaging above 10% annually and exceeding 40% at times."

## Related Papers
- [[paper_fan_2024_crypto_carry_trade]] — Extends carry analysis to cross-sectional crypto
- [[paper_he_2022_perpetual_futures_fundamentals]] — No-arbitrage pricing framework
- [[paper_inan_2025_funding_rate_predictability]] — Funding rate persistence

---

*Research responsibility: Quant Research Agent*
