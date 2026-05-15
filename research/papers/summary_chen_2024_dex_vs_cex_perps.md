# Paper Summary

**Source ID:** CRYPTO-PAPER-010
**Domain:** crypto
**Source type:** working_paper
**Date reviewed:** 2026-05-16

---

## Paper Details

**Title:** Exploring the Impact: How Decentralized Exchange Designs Shape Traders' Behavior on Perpetual Future Contracts
**Authors:** Erdong Chen, Mengzhong Ma, Zixin Nie
**Year:** 2024
**Venue / Journal / Conference:** arXiv preprint
**DOI / arXiv / SSRN:** arXiv:2402.03953
**URL:** https://arxiv.org/abs/2402.03953

---

## Research Question

How do different exchange architectures (CEX vs. DEX) shape trader behavior in perpetual futures markets, particularly regarding leverage choice, liquidation dynamics, and OI asymmetries?

## Market Studied

Bitcoin perpetual futures across CEX (Binance-style CLOB) and DEX (VAMM-based and oracle-based) architectures.

## Data Used

Transaction-level data from multiple exchanges covering different perpetual derivatives architectures. Time period unspecified but likely 2022-2023.

## Methodology

Comparative analysis of trader behavior across three exchange architectures: CLOB CEX, VAMM DEX, and oracle-pricing DEX. Focus on leverage distributions, liquidation events, and OI dynamics.

## Main Findings

1. DEX perpetuals show a differential impact of OI on long versus short positions — an asymmetry not present in CLOB CEX markets, where OI impact is symmetric.
2. In oracle-pricing DEX models, traders are largely price takers whose actions respond directly to external price signals rather than internal exchange mechanics.
3. Less informed traders have a significant propensity to overreact to positive news by increasing long positions — a behavioral pattern amplified in DEX environments.

## Limitations

1. Preprint — not yet peer-reviewed.
2. DEX perpetual market structure evolves rapidly; findings about specific protocols may not generalize.
3. Does not directly test OI-price divergence as a trading signal — the OI asymmetry finding is incidental to the main research question.

---

## Applicability Assessment

### Applicability to Crypto

Important for scoping CRYPTO-002. The paper demonstrates that OI mechanics differ between CEX and DEX perpetuals. For CRYPTO-002, this means the signal should be scoped to CLOB CEXs (Binance, Bybit, OKX) where OI dynamics are symmetric and interpretable. DEX perpetuals (dYdX, Drift, ApolloX) require separate analysis.

### Applicability to Commodities

Not directly applicable.

---

## Alpha Ideas Derived

| Alpha ID | Idea | Status |
|----------|------|--------|
| CRYPTO-002 | OI-Price Divergence Reversal | Researching — confirms CEX-only scope |

---

## Reliability Assessment

**Reliability tier:** 1
**Justification:** arXiv preprint from quantitative finance. Authors are affiliated with academic institutions. Methodology is transparent and data sources are identified.

---

## Notes for Future Review

- The key takeaway for CRYPTO-002 is the scope restriction: CLOB CEXs only. The OI-price divergence signal relies on symmetric OI interpretation that holds on CEXs but not necessarily on DEXs.
- The behavioral finding (less informed traders overreacting to positive news) is relevant to the overall alpha thesis but not directly required for signal construction.
