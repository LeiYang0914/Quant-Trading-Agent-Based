---
title: "Giagkiozis & Said (2024) — Reconciling Open Interest with Traded Volume in Perpetual Swaps"
type: paper_note
status: summarized
created: 2026-05-14
updated: 2026-05-14
tags:
  - paper_note
  - crypto
  - open_interest
  - data_quality
concepts:
  - "[[Open Interest]]"
  - "[[Perpetual Futures]]"
source_type: paper
authors: "Ioannis Giagkiozis, Emilio Said"
year: 2024
journal: "Ledger, Volume 9, pp. 1-15"
url: "https://arxiv.org/abs/2310.14973"
verified: true
---

# Giagkiozis & Said (2024) — Reconciling Open Interest with Traded Volume in Perpetual Swaps

## Citation
**Authors:** Ioannis Giagkiozis, Emilio Said
**Year:** 2024
**Journal / Venue:** Ledger, Volume 9, pp. 1-15
**Link:** https://arxiv.org/abs/2310.14973
**Full PDF:** https://arxiv.org/pdf/2310.14973
**Verification:** Confirmed — arXiv abstract page accessible, PDF available.

## One-Paragraph Summary
Analyzed tick-by-tick data from seven major crypto derivatives exchanges in 2023. Found that open interest in Bitcoin perpetual swaps is systematically misquoted by some of the largest derivatives exchanges — some reporting "wholly implausible" OI figures, others delaying liquidation messages. Frames OI as "a critical metric in derivatives markets" for assessing "market activity, sentiment, and overall liquidity." Also notes that cumulative OI across markets, combined with proof of reserves, can reveal "unsustainable levels of leverage."

## Key Findings
1. OI is systematically misquoted by some large derivatives exchanges
2. Some exchanges report implausible OI figures that don't reconcile with traded volume
3. Some exchanges delay liquidation messages, distorting OI signals
4. Cross-exchange OI aggregation without reconciliation can be contaminated
5. Cumulative OI + proof of reserves can reveal unsustainable leverage levels

## Methods Used
- Tick-by-tick data from 7 major crypto derivatives exchanges
- OI-volume reconciliation
- Cross-exchange comparison of OI reporting

## Data Used
| Dataset | Period | Frequency | Source |
|---------|--------|-----------|--------|
| Tick-level perpetual swap data | 2023 | Tick | 7 major crypto derivatives exchanges |

## Relevance to Our Research
**Critical data quality warning.** Any alpha using OI as a signal input MUST use verified, reconciled OI data. Recommendations:
- Prefer single-exchange OI data from known-reliable venues (Binance)
- Use CoinGlass/Coinalyze aggregated OI which reconciles across exchanges
- Be aware that OI spikes may be artifacts of misreporting, not genuine sentiment shifts
- Cross-check OI changes against volume changes for plausibility

## Applicable Alpha Ideas
- [[crypto_oi_momentum_reversal]] — Data quality directly impacts signal reliability

## Critique & Limitations
- Study covers only 2023 data — misreporting patterns may have changed since
- Limited to 7 exchanges; smaller venues not covered
- Does not quantify the signal distortion from misreporting (qualitative finding)

## Key Quotes
> "Open interest in Bitcoin perpetual swaps is systematically misquoted by some of the largest derivatives exchanges."

---

*Research responsibility: Quant Research Agent*
