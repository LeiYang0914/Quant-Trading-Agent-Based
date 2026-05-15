# Alpha Research Memo

**Alpha ID:** `{CRYPTO-NNN | COMMOD-NNN | CROSS-NNN}`
**Domain:** `{crypto | commodities | cross_market}`
**Date:** YYYY-MM-DD
**Status:** `{researching | needs_data_check | ready_for_review | ready_for_backtest | archived}`
**Priority:** `{high | medium | low}`

---

## 1. Title

`{Descriptive title}`

## 2. Market & Instrument

- **Market:** `{crypto / commodities / cross_market}`
- **Asset universe:** `{specific assets or universe filter}`
- **Instrument type:** `{perpetual futures / spot / futures / options}`
- **Venues:** `{exchanges or trading venues}`

## 3. One-Sentence Hypothesis

> `{Precise, falsifiable statement of the expected relationship.}`

## 4. Economic Rationale

`{Explain the economic mechanism. Why should this edge exist? What market structure feature, behavioral bias, or institutional constraint creates it?}`

## 5. Behavioral or Structural Source of Edge

`{Is this edge driven by behavior (retail crowding, attention, sentiment) or structure (arbitrage constraints, regulation, custody, capital flows)? Why does it persist?}`

## 6. Source Inspiration

### Primary Sources (Tier 1 or Tier 2)

**Reference ID:** `{DOMAIN-TYPE-NNN}`
**Title:**
**Authors / Organization:**
**Year:**
**Venue / Publisher:**
**DOI / arXiv / SSRN:**
**URL:**
**Relevance to alpha:** `{What specific result, mechanism, or data is used from this source.}`

*(Repeat for each primary source — minimum 1 required)*

### Supplementary Sources (Tier 3)

**Reference ID:** `{DOMAIN-TYPE-NNN}`
**Title:**
**Authors / Organization:**
**Year:**
**URL:**
**Relevance to alpha:**

*(Repeat for each supplementary source)*

## 7. Required Data

| Dataset | Fields | Frequency | Vendor Options | Min Coverage | Known Issues |
|----------|--------|-----------|----------------|--------------|--------------|
| `{data}` | `{fields}` | `{freq}` | `{vendors}` | `{period}` | `{issues}` |

**Data source candidates:**
- `{Tier 1/2 source option 1}`
- `{Tier 1/2 source option 2}`

## 8. Signal Construction (Plain English Only)

**Raw input:** `{Data fields used}`
**Lookback window:** `{N periods}`
**Transformation:** `{Describe in plain English — no code}`
**Entry condition:** `{When to enter — unambiguous}`
**Exit condition:** `{When to exit — unambiguous}`
**Position size:** `{Sizing rule}`
**Signal frequency:** `{How often the signal updates}`
**Expected holding period:** `{Typical trade duration}`

## 9. Portfolio Construction Idea

- **Rebalance frequency:** `{daily, weekly, etc.}`
- **Position sizing:** `{equal weight, risk parity, etc.}`
- **Leverage:** `{none, 1x, etc.}`
- **Max position:** `{% of book}`
- **Universe filtering:** `{minimum liquidity, market cap, etc.}`

## 10. Transaction Cost Sensitivity

| Cost Item | Estimate | Impact on Signal |
|-----------|----------|------------------|
| Trading fee | `{bps}` | `{description}` |
| Slippage | `{bps}` | `{description}` |
| Funding cost | `{rate}` | `{description}` |

## 11. Liquidity Constraints

- **Capacity estimate:** `{$X M notional}`
- **Liquidity bottleneck:** `{which leg, which asset, which venue}`
- **Scalability assessment:** `{small / medium / large capacity}`

## 12. Known Risks

1. `{Risk 1 — severity: high/medium/low}`
2. `{Risk 2 — severity: high/medium/low}`

## 13. Failure Modes

| Failure Mode | Severity | Trigger | Mitigation |
|-------------|----------|---------|------------|
| `{mode}` | `{high/med/low}` | `{what causes it}` | `{how to detect or prevent}` |

## 14. Data Quality Concerns

- `{Concern 1}`
- `{Concern 2}`

## 15. Similar Existing Ideas

| Idea | Domain | Similarity | Distinct? |
|------|--------|------------|-----------|
| `{alpha ID or description}` | `{domain}` | `{low/medium/high}` | `{yes/no — why}` |

## 16. Research Confidence

| Dimension | Rating (1-10) | Notes |
|-----------|---------------|-------|
| Economic intuition | | |
| Source quality | | |
| Data availability | | |
| Signal clarity | | |
| Failure mode coverage | | |
| Novelty | | |

**Overall confidence:** `{high / medium / low}`

## 17. Handoff Readiness

- [ ] References complete (2+ credible, 1+ Tier 1/2)
- [ ] Data requirements specified
- [ ] Signal construction clear (plain English)
- [ ] Failure modes documented
- [ ] Review gate passed

## 18. Open Questions

1. `{Question 1}`
2. `{Question 2}`

## 19. References (Structured)

| Ref ID | Title | Authors | Year | Venue | DOI/arXiv/SSRN | URL | Relevance |
|--------|-------|---------|------|-------|----------------|-----|-----------|
| `{ID}` | `{title}` | `{authors}` | `{year}` | `{venue}` | `{id}` | `{url}` | `{why relevant}` |

---

*Memo authored by: Research Agent*
*Domain: {crypto | commodities | cross_market}*
*Next: Review Agent gate*
