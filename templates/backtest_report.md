# Backtest Report — `{strategy_name}`

**Programmer Agent**
**Date:** `{date}`
**Source Handoff:** `handoffs/pending/{handoff_file}.md`
**Implementation:** `src/signals/{signal_file}.py`
**Backtest:** `src/backtest/{backtest_file}.py`

---

## Backtest Configuration

| Parameter | Value |
|-----------|-------|
| Universe | `{assets, filters}` |
| Frequency | `{daily, hourly, etc.}` |
| Lookback window | `{N days}` |
| Entry condition | `{summary}` |
| Exit condition | `{summary}` |
| Position sizing | `{method}` |
| Transaction costs | `{bps} bps one-way` |
| Slippage | `{bps} bps` |
| Start date | `{YYYY-MM-DD}` |
| End date | `{YYYY-MM-DD}` |

---

## Performance Summary

| Metric | Value |
|--------|-------|
| Total return | `{X%}` |
| Annualized return | `{X%}` |
| Annualized volatility | `{X%}` |
| Sharpe ratio | `{X.XX}` |
| Calmar ratio | `{X.XX}` |
| Max drawdown | `{-X%}` |
| Max drawdown duration | `{N} days` |
| Win rate | `{X%}` |
| Avg win / avg loss | `{X.XX}` |
| Total trades | `{N}` |

---

## Equity Curve

`{Description of equity curve characteristics — no chart embedding required, describe key features}`

---

## Parameter Sweep

| Parameter | Range Tested | Optimal | Sensitivity |
|-----------|-------------|---------|-------------|
| `{param1}` | `{min} - {max}` | `{value}` | `{low/medium/high}` |

---

## Subperiod Analysis

| Period | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| Full period | `{ }` | `{ }` | `{ }` |
| First half | `{ }` | `{ }` | `{ }` |
| Second half | `{ }` | `{ }` | `{ }` |
| Bull regime | `{ }` | `{ }` | `{ }` |
| Bear regime | `{ }` | `{ }` | `{ }` |

---

## Transaction Cost Sensitivity

| Cost Multiplier | Return | Sharpe |
|-----------------|--------|--------|
| 0.5x baseline | `{ }` | `{ }` |
| 1.0x baseline | `{ }` | `{ }` |
| 2.0x baseline | `{ }` | `{ }` |

---

## Edge Case Results

| Edge Case | Behavior | Pass? |
|-----------|----------|-------|
| `{case from handoff}` | `{observed behavior}` | `{ }` |

---

## Known Issues

`{Any implementation issues, data problems, or deviations from the handoff spec}`
