# Paper Summary

**Source ID:** CRYPTO-PAPER-008
**Domain:** crypto
**Source type:** journal
**Date reviewed:** 2026-05-16

---

## Paper Details

**Title:** Reconciling Open Interest with Traded Volume in Perpetual Swaps
**Authors:** Ioannis Giagkiozis, Emilio Said
**Year:** 2024
**Venue / Journal / Conference:** Ledger, Volume 9
**DOI / arXiv / SSRN:** arXiv:2310.14973
**URL:** https://arxiv.org/abs/2310.14973

---

## Research Question

How reliable is reported open interest data from major cryptocurrency derivatives exchanges? Can reported OI be reconciled with traded volume to detect data quality issues?

## Market Studied

Seven major crypto derivatives exchanges across two sample periods in 2023. Bitcoin perpetual swaps (BTCUSDT).

## Data Used

Tick-by-tick trade and OI data from exchange APIs. Two observation windows in 2023, covering multiple exchanges.

## Methodology

Cross-exchange comparison of reported OI levels. Reconciliation of OI changes with traded volume to detect implausible data. Statistical analysis of OI reporting patterns.

## Main Findings

1. Some exchanges systematically misreport OI at levels that are "wholly implausible" — OI values that cannot be reconciled with actual trading activity.
2. Other exchanges appear to delay reporting of liquidation events, smoothing OI changes that should be instantaneous.
3. OI can be cross-checked against cumulative traded volume as a data quality filter — periods where ΔOI and net traded volume diverge significantly indicate data quality issues.

## Limitations

1. Only covers Bitcoin perpetuals, not ETH or altcoins.
2. Sample periods in 2023 — exchange reporting practices may have changed.
3. Does not propose a specific data quality correction — identifies the problem but not the solution.

---

## Applicability Assessment

### Applicability to Crypto

Directly applicable. Every OI-based alpha in crypto must account for exchange-level OI misreporting. The paper's key insight — cross-check OI changes against volume — provides a practical data quality filter.

### Applicability to Commodities

Not directly applicable (commodity futures OI reporting is regulated and more reliable).

---

## Alpha Ideas Derived

| Alpha ID | Idea | Status |
|----------|------|--------|
| CRYPTO-002 | OI-Price Divergence Reversal | Researching — data quality warning |

---

## Reliability Assessment

**Reliability tier:** 1
**Justification:** Peer-reviewed journal paper (Ledger), published by the University of Pittsburgh. Dataset from primary exchange APIs. Methodology is sound and replicable.

---

## Notes for Future Review

- This is a critical data quality reference for CRYPTO-002. The OI signal must include a data quality filter based on the ΔOI-vs-volume reconciliation proposed here.
- Recommendation: use Binance-only OI as the primary source (Binance was among the better reporters in the study), with CoinGlass aggregated data as a secondary check.
