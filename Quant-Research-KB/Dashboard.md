# Quant Research KB — Dashboard

**Last updated:** 2026-05-14
**Vault:** Quant Alpha Research Knowledge Base

---

## Quick Links

- [[Open Interest]] — Core concept
- [[Funding Rate]] — Core concept
- [[crypto_oi_momentum_reversal]] — Active research (Memo #02)
- [[crypto_cross_sectional_altcoin_carry]] — Ready for programmer (Memo #03)
- [[handoff_crypto_cross_sectional_altcoin_carry]] — Programmer handoff
- `99_Templates/` — Note templates (Ctrl+T to insert)

---

## Alpha Pipeline

### Active Research
```dataview
TABLE status, priority, markets, updated
FROM "02_Alpha_Ideas"
WHERE status != "rejected" AND status != "deprecated"
SORT priority ASC
```

### Ready for Programmer
```dataview
TABLE source_alpha, created
FROM "09_Programmer_Handoffs"
WHERE status = "pending"
SORT created DESC
```

### Rejected / Deprecated
```dataview
TABLE rejection_reason_category, rejected_date
FROM "11_Rejected_Deprecated"
SORT rejected_date DESC
```

---

## Research at a Glance

| Memo | Alpha | Status | Vault Note |
|------|-------|--------|------------|
| #01 | Funding Rate Carry + Crowding | Complete, handed off | *(legacy)* |
| #02 | OI-Price Divergence Reversal | needs_data_check | [[crypto_oi_momentum_reversal]] |
| #03 | Cross-Sectional Altcoin Carry | waiting_for_programmer | [[crypto_cross_sectional_altcoin_carry]] |

## Recent Paper Notes
```dataview
TABLE authors, year, journal
FROM "05_Paper_Notes"
SORT created DESC
LIMIT 10
```

## Risk & Failure Mode Catalog
```dataview
TABLE severity, frequency, affected_ideas
FROM "07_Risk_Failure_Modes"
SORT severity DESC
```

---

## Browse by Folder

| Folder | Notes |
|--------|-------|
| `01_Concepts/` | [[Open Interest]], [[Funding Rate]] |
| `02_Alpha_Ideas/` | [[crypto_oi_momentum_reversal]], [[crypto_cross_sectional_altcoin_carry]] |
| `05_Paper_Notes/` | 5 paper notes from Memos #02 and #03 |
| `06_Data_Source_Notes/` | [[coinglass_aggregated_derivatives]] |
| `07_Risk_Failure_Modes/` | [[oi_data_quality_misreporting]] |
| `09_Programmer_Handoffs/` | [[handoff_crypto_cross_sectional_altcoin_carry]] |

---

## Agent Interface

- **Research Agent:** Reads and writes all notes. Owns the research lifecycle. Never writes code.
- **Programmer Agent:** Reads `09_Programmer_Handoffs/`. Implements backtests. Returns results.
- **Boundary:** Research specifies what to test. Programmer decides how to code it.
