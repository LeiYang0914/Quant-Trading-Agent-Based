# Alpha Backlog

Ideas queued for research, grouped by domain. Process in order: crypto first, then commodities, then cross-market.

---

## Crypto Alpha Backlog

### High Priority

| Alpha ID | Title | Status | Priority | References | Data Status | Next Action |
|----------|-------|--------|----------|------------|-------------|-------------|
| CRYPTO-001 | Funding Rate Carry and Crowding Signal — delta-neutral BTC/ETH funding carry with crowding reversal overlay | MVP implemented — backtested 2026-06-10 | High | Sufficient (7 papers) | Available | Backtest report: `reports/backtests/CRYPTO-001_funding_rate_carry_backtest.md`. Next: real data, parameter sweep. |
| CRYPTO-002 | OI-Price Divergence Reversal — rising OI + price divergence as directional reversal signal | Conditional Pass — handed off | High | Sufficient (5 sources, 4 papers) | Available | Handed off to programmer. See `handoffs/pending/CRYPTO-002_oi_divergence_reversal.md` (5 conditions). |
| CRYPTO-003 | Cross-Sectional Altcoin Funding Carry — long high-FR, short low-FR across top 20 alts | Complete — Memo #03 | High | Sufficient (7 papers) | Available | Handed off to programmer |
| CRYPTO-004 | DEX Venue Funding Carry — Drift Protocol / ApolloX carry premium vs CEX | ready_for_review | High | Sufficient (10 sources: 6 academic + 4 official docs) | Unknown -- needs Data Agent check | Awaiting Review Agent evaluation. Memo: `research/memos/crypto/04_dex_venue_funding_carry.md` |

### Medium Priority

| Alpha ID | Title | Status | Priority | References | Data Status | Next Action |
|----------|-------|--------|----------|------------|-------------|-------------|
| CRYPTO-005 | Stablecoin Mint/Burn Flows — stablecoin supply changes as leading indicator of crypto spot demand | Not started | Medium | None | Unknown | Needs lit review |
| CRYPTO-006 | Exchange Inflow/Outflow Spikes — large exchange deposit/withdrawal spikes as short-term reversal signal | Not started | Medium | None | Unknown | Needs lit review |

### Low Priority

| Alpha ID | Title | Status | Priority | References | Data Status | Next Action |
|----------|-------|--------|----------|------------|-------------|-------------|
| CRYPTO-007 | Crypto Options Skew — put-call skew as directional predictor | Not started | Low | None | Unknown | Needs lit review |
| CRYPTO-008 | BTC ETF Flow Delta — daily ETF flow change as spot direction signal | Not started | Low | None | Unknown | Needs lit review |

---

## Commodities Alpha Backlog

### Medium Priority

| Alpha ID | Title | Status | Priority | References | Data Status | Next Action |
|----------|-------|--------|----------|------------|-------------|-------------|
| COMMOD-001 | Gold Futures Term Structure Slope — term structure steepness/flatness as macro regime classifier | Not started | Medium | None | Unknown | Needs lit review |
| COMMOD-002 | CFTC COT Positioning Extremes — speculative positioning extremes in gold/silver/crude as contrarian signal | Not started | Medium | None | Unknown | Needs lit review |

### Low Priority

| Alpha ID | Title | Status | Priority | References | Data Status | Next Action |
|----------|-------|--------|----------|------------|-------------|-------------|
| COMMOD-003 | Crude Oil Calendar Spread — calendar spread as inventory regime signal | Not started | Low | None | Unknown | Needs lit review |

---

## Cross-Market Alpha Backlog

### Low Priority

| Alpha ID | Title | Status | Priority | References | Data Status | Next Action |
|----------|-------|--------|----------|------------|-------------|-------------|
| CROSS-001 | Silver-Gold Ratio — silver-gold ratio as risk-on/risk-off regime indicator | Not started | Low | None | Unknown | Needs lit review |
| CROSS-002 | Crypto-Macro Surprise Correlation — crypto response to CPI, FOMC, NFP surprises as event alpha | Not started | Low | None | Unknown | Needs lit review |

---

## Backlog Process

1. **Default domain order:** crypto → commodities → cross_market.
2. Commodities research begins only after crypto priorities are complete or when explicitly requested.
3. New ideas: added to the correct domain table with next available alpha ID.
4. Status progression: Not started → Researching → needs_data_check → ready_for_review → (Review Agent) → conditional_pass | approved | rejected → ready_for_backtest.
5. References status: None → Partial → Sufficient (2+ credible, 1+ Tier 1/2).
6. Data status: Unknown → Needs check → Available → Unavailable.
7. Ideas are never deleted. Rejected ideas move to `research/ideas/rejected/{domain}/`.

## Summary

| Domain | Total | Complete | In Progress | Not Started |
|--------|-------|----------|-------------|-------------|
| Crypto | 8 | 3 | 1 | 4 |
| Commodities | 3 | 0 | 0 | 3 |
| Cross-market | 2 | 0 | 0 | 2 |
| **Total** | **13** | **3** | **1** | **9** |
