---
title: "OI Data Quality — Exchange Misreporting"
type: risk_failure_mode
status: documented
created: 2026-05-14
updated: 2026-05-14
tags:
  - risk_failure_mode
  - open_interest
  - data_quality
  - crypto
concepts:
  - "[[Open Interest]]"
severity: 4
frequency: ongoing
affected_ideas:
  - "[[crypto_oi_momentum_reversal]]"
---

# OI Data Quality — Exchange Misreporting

## Category
Data Error

## Description
Some of the largest crypto derivatives exchanges systematically misreport open interest, as documented by Giagkiozis & Said (2024). Some report "wholly implausible" OI figures that don't reconcile with traded volume. Others delay liquidation messages, causing OI to appear higher than it actually is (since liquidated positions haven't been removed from the OI tally).

## How It Manifests
- OI spikes that don't correspond to volume spikes (implausible OI/volume ratio)
- OI that remains flat during large price moves (delayed liquidation reporting)
- Divergent OI figures for the same contract across different data aggregators
- OI changes that reverse sharply within hours (data corrections, not genuine flows)

## Examples from Research
- [[paper_giagkiozis_2024_oi_reconciliation_perps]] — Systematic misreporting documented across 7 major exchanges in 2023
- A CryptoSlate article documented $15B in OI erased at quarter-end options expiry "without moving spot price" — purely mechanical, not sentiment-driven

## Mitigation Strategies
1. **Single-source OI:** Use Binance-only OI data (largest exchange, most scrutinized, least likely to misreport)
2. **Aggregated and reconciled OI:** Use CoinGlass or Coinalyze aggregated OI, which cross-references multiple exchanges
3. **OI-volume reconciliation check:** Flag OI changes where ΔOI/Volume ratio exceeds a plausibility threshold
4. **Multi-source cross-check:** Compare OI data from at least 2 independent sources before generating signals
5. **Expiry calendar filter:** Exclude periods around quarterly expiries where mechanical OI changes dominate

## Detection Tests
- [ ] Compare Binance-reported OI vs. CoinGlass aggregated OI for the same contract over 6 months — measure correlation and divergence frequency
- [ ] Flag all OI daily changes > 3 standard deviations for manual review
- [ ] Cross-reference OI changes against volume: OI change should not exceed daily volume by > 50%
- [ ] Monitor for exchanges where OI is perfectly flat for > 4 hours during active trading (delayed update detection)

## Related Concepts
- [[Open Interest]]
- [[Transaction Cost]]
- [[Market Microstructure]]

---

*Research responsibility: Quant Research Agent*
