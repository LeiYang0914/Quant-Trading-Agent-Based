# Data Quality Report — `{data_source_name}`

**Data Agent**
**Date:** `{date}`
**Source:** `{vendor/API name}`
**Coverage period:** `{start} — {end}`

---

## Source Information

| Field | Value |
|-------|-------|
| Vendor | `{name}` |
| API endpoint | `{URL}` |
| Data type | `{OHLCV, funding rates, OI, etc.}` |
| Frequency | `{real-time, hourly, daily}` |
| Cost tier | `{free, freemium, paid}` |
| Reliability rating | `{A / B / C}` |

---

## Quality Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Expected row count | `{N}` | |
| Actual row count | `{N}` | |
| Missing rows | `{N} ({X%})` | |
| Outliers detected | `{N}` | |
| Stale data periods | `{list}` | |
| Duplicate rows | `{N}` | |

---

## Known Issues

| Issue | Severity | Description | Mitigation |
|-------|----------|-------------|------------|
| `{issue}` | `{high/med/low}` | `{description}` | `{how to handle}` |

---

## Exchange-Specific Quirks

`{Any exchange-specific data behaviors: funding rate calculation differences, OI reporting inconsistencies, delisting handling, timestamp conventions}`

---

## Survivorship Bias Assessment

`{Does this dataset include delisted assets? What is the survivorship bias risk?}`

---

## Recommendations

- `{Actionable recommendation}`
- `{Actionable recommendation}`
