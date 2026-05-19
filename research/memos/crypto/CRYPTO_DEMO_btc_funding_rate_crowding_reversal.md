# Alpha Research Memo

**Alpha ID:** `CRYPTO-DEMO-001`
**Domain:** `crypto`
**Date:** 2026-05-19
**Status:** `demo — ready_for_review`
**Priority:** `high`

---

## 1. Title

`BTC Perpetual Funding Rate as a Crowding and Reversal Signal`

## 2. Market & Instrument

- **Market:** `crypto`
- **Asset universe:** `BTC only (Phase 1); ETH extension (Phase 2)`
- **Instrument type:** `perpetual futures`
- **Venues:** `Binance (primary), Bybit, OKX (cross-validation)`

## 3. One-Sentence Hypothesis

> When the 8-hour BTC perpetual funding rate exceeds the 90th percentile of its trailing 30-day distribution, forward BTC spot returns over the subsequent 8 to 48 hours are negatively skewed with negative expected value, driven by crowded leveraged-long positioning that is vulnerable to liquidation cascades on adverse price moves.

## 4. Economic Rationale

Crypto perpetual futures use a periodic funding payment to tether the contract price to the spot index. When the perpetual trades at a premium, longs pay shorts. Persistently high positive funding rates signal that the market is heavily net long — speculators are willing to pay an elevated recurring cost to maintain bullish exposure.

This crowded positioning creates structural fragility. When a critical mass of leveraged longs is paying high funding, even a modest adverse price move triggers liquidations. Liquidations are market-sell orders, which push price further down, which triggers more liquidations, creating a cascading feedback loop. The funding rate is therefore not just a cost-of-carry metric — at extremes, it is a forward indicator of potential deleveraging.

The mechanism has two reinforcing layers:
1. **Sentiment layer:** Extreme positive funding = excessive bullish consensus. When everyone who wants to be long is already long, marginal buyers are exhausted. The next large order is more likely to be a seller.
2. **Structural layer:** High funding = high leverage concentration. Leveraged positions have forced exit conditions (liquidation prices). When those levels are hit, selling is automatic and price-insensitive, amplifying any downward move.

## 5. Behavioral or Structural Source of Edge

This edge is primarily **behavioral** — retail speculators systematically overpay for leverage during bull markets, exhibiting overconfidence and lottery-preference biases. They anchor on the absolute funding rate (e.g., "0.01% per 8 hours is cheap") rather than the relative rate (90th percentile of recent history).

The edge persists because:
- Crowding can intensify before reversing — the 90th percentile can stay breached for multiple settlement periods, punishing early contrarians
- Timing the reversal is inherently difficult; no one knows when the cascade begins
- Institutional participants may amplify crowding (buying pressure pushes funding higher) before the reversal materializes
- The signal requires active monitoring and disciplined position sizing; it is not a passive strategy

## 6. Source Inspiration

### Primary Sources (Tier 1)

**Reference ID:** `CRYPTO-PAPER-002`
**Title:** Crypto Carry
**Authors / Organization:** Schmeling, Schrimpf, Todorov
**Year:** 2023
**Venue / Publisher:** BIS Working Paper No. 1087
**DOI / arXiv / SSRN:** —
**URL:** https://www.bis.org/publ/work1087.htm
**Relevance to alpha:** Documents that high absolute funding rates predict crashes for BTC/ETH — the fundamental reversal relationship. Observable fundamentals cannot explain the magnitude of crypto carry, pointing to market segmentation and limited arbitrage as primary drivers. This is the strongest institutional-quality evidence for the crowding mechanism.

**Reference ID:** `CRYPTO-PAPER-001`
**Title:** Fundamentals of Perpetual Futures
**Authors / Organization:** He, Manela, Ross, von Wachter
**Year:** 2022
**Venue / Publisher:** arXiv
**DOI / arXiv / SSRN:** arXiv:2212.06888
**URL:** https://arxiv.org/abs/2212.06888
**Relevance to alpha:** Derives no-arbitrage pricing for perpetual futures. Establishes the theoretical framework for understanding when funding rates deviate from fair value — deviations signal positioning imbalances that this strategy exploits.

**Reference ID:** `CRYPTO-PAPER-006`
**Title:** Predictability of Funding Rates
**Authors / Organization:** Inan
**Year:** 2025
**Venue / Publisher:** SSRN
**DOI / arXiv / SSRN:** SSRN:5576424
**URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5576424
**Relevance to alpha:** Documents that BTC/ETH funding rates are statistically predictable using double autoregressive models. Funding rate persistence supports using a trailing percentile rather than an absolute threshold — if funding were purely random, the percentile approach would have no edge.

**Reference ID:** `CRYPTO-PAPER-005`
**Title:** Perpetual Futures Pricing
**Authors / Organization:** Ackerer, Hugonnier, Jermann
**Year:** 2025
**Venue / Publisher:** Mathematical Finance
**DOI / arXiv / SSRN:** DOI:10.1111/mafi.12442
**URL:** https://onlinelibrary.wiley.com/doi/10.1111/mafi.12442
**Relevance to alpha:** Published in a top-tier finance journal. Validates the theoretical pricing framework. When actual funding deviates from model-implied fair funding, it indicates positioning-driven distortion that should eventually mean-revert.

### Supplementary Sources (Tier 3)

**Reference ID:** `CRYPTO-PRACT-005`
**Title:** Glassnode Insights — Market Pulse
**Authors / Organization:** Glassnode
**Year:** Ongoing
**URL:** https://insights.glassnode.com/
**Relevance to alpha:** Practitioner confirmation that extreme funding rate environments are widely monitored. The signal may be partially crowded, but Glassnode's own analytics show that funding extremes precede drawdowns with economically meaningful frequency.

**Reference ID:** `CRYPTO-OFFICIAL-002`
**Title:** Q3 Derivatives Report
**Authors / Organization:** BitMEX
**Year:** 2025
**URL:** https://blog.bitmex.com/
**Relevance to alpha:** Documents that BTC funding was positive 92% of the time in Q3 2025, confirming regime change toward persistently positive funding. This affects how the 90th percentile threshold should be calibrated — in a regime where funding is almost always positive, the reversal signal may need to use a higher threshold (95th or 98th percentile) to identify true extremes.

## 7. Required Data

| Dataset | Fields | Frequency | Vendor Options | Min Coverage | Known Issues |
|----------|--------|-----------|----------------|--------------|--------------|
| BTC-PERP funding rate | symbol, fundingRate, fundingTime | 8h | Binance API (free), Bybit API (free), OKX API (free), CoinGlass | 2019–present | Some early gaps; Binance formula changed in 2021; caps at ±0.375%/8h may compress extremes |
| BTC spot OHLCV | open, high, low, close, volume | 1h / 8h | Binance API (free), Kaiko (paid), Tardis.dev (paid) | 2017–present | — |
| BTC-PERP open interest | openInterest, timestamp | 1h | Binance API, CoinGlass, Coinalyze | 2019–present | Denominated in BTC or USD depending on contract; normalize |
| OI-weighted multi-exchange funding | aggregated rate, per-exchange rates | 8h | CoinGlass, Glassnode Pro | 2020–present | CoinGlass methodology less documented than Glassnode; prefer Glassnode for signal, CoinGlass for cross-check |

**Data source candidates:**
- Binance API (`GET /fapi/v1/fundingRate`, `GET /fapi/v1/openInterest`) — free, sufficient for initial backtest
- CoinGlass — OI-weighted multi-exchange aggregation; better signal than single-exchange

## 8. Signal Construction (Plain English Only)

**Raw input:** 8-hour BTC perpetual funding rate from Binance (USDM pair), supplemented by OI-weighted multi-exchange rate from CoinGlass

**Lookback window:** 30 calendar days (approximately 90 observations at 8-hour frequency)

**Transformation:**
1. Collect the trailing 90 funding rate observations (8-hour frequency, aligned to 00:00, 08:00, 16:00 UTC settlement times)
2. Compute the empirical percentile rank of the current period's funding rate within this trailing window
3. Ignore periods where fewer than 60 observations are available (e.g., exchange downtime) — do not generate a signal

**Entry condition (short):** Funding rate percentile rank ≥ 90th percentile of trailing 30-day window → enter short BTC position at next bar open

**Entry condition (long):** Funding rate percentile rank ≤ 10th percentile of trailing 30-day window → enter long BTC position at next bar open

**Exit condition:** Close position after exactly 24 hours (3 funding settlement periods), OR if funding rate percentile rank returns to the 25th–75th range (whichever comes first)

**Position size:** 10% of NAV per signal. Maximum one active position at a time (no pyramiding). If a new signal fires while a position is active, ignore the new signal.

**Signal frequency:** Evaluated every 8 hours at funding settlement. Most periods produce no signal (percentile between 10 and 90).

**Expected holding period:** 8 to 48 hours. Base case 24 hours. Maximum 48 hours (forced exit regardless of P&L).

## 9. Portfolio Construction Idea

- **Rebalance frequency:** Signal evaluated every 8 hours; position opened/closed at next bar open
- **Position sizing:** 10% NAV per signal; no leverage on the position itself
- **Leverage:** None (1x notional). The signal is directional BTC exposure — adding leverage would amplify the already-concentrated single-asset risk
- **Max position:** 10% NAV (single signal); no concurrent signals
- **Universe filtering:** BTC only (Phase 1). Minimum daily volume filter: only trade if BTC 24h spot volume > $5B to ensure sufficient liquidity

## 10. Transaction Cost Sensitivity

| Cost Item | Estimate | Impact on Signal |
|-----------|----------|------------------|
| Trading fee | 0.04% taker per side (Binance) | 0.08% round-trip; manageable for a signal targeting 1–3% moves |
| Slippage | 0.02% per side at 10% NAV size | 0.04% round-trip; likely conservative at current BTC liquidity |
| Funding cost (while in position) | Variable; if funding remains positive while short, receive funding payments (positive carry) | Funding received while short partially offsets fees; this is a tailwind for the short-entry case |
| Total round-trip | ~0.08–0.12% | Signal must generate gross alpha of at least 0.3% per trade to be net profitable after costs |

## 11. Liquidity Constraints

- **Capacity estimate:** ~$50M notional per signal (10% of $500M book). At current BTC daily spot volume (~$10B+), a $50M position represents ~0.5% of daily volume — acceptable.
- **Liquidity bottleneck:** The short leg (BTC-PERP) has effectively unlimited capacity on Binance. The constraint is entering spot BTC during the exit — if the reversal is driven by cascading liquidations, spot order books may thin temporarily.
- **Scalability assessment:** Medium capacity. Signal frequency is low (only fires at extremes), so total turnover is modest. Could scale to ~$200M notional before market impact becomes material.

## 12. Known Risks

1. **Crowding decay (severity: high):** The signal is based on a well-known relationship. As more participants trade against funding extremes, the reversal may become faster and sharper, reducing the window for profitable entry. The 90th percentile threshold may need periodic recalibration.
2. **Cascade non-event (severity: medium):** High funding can persist for days or weeks without a reversal. The signal may trigger repeatedly and generate multiple small losses before a large winning trade. Position sizing must survive a sequence of consecutive losses.

## 13. Failure Modes

| Failure Mode | Severity | Trigger | Mitigation |
|-------------|----------|---------|------------|
| Funding rate cap compression | Medium | Binance caps funding at ±0.375%/8h; if true crowding would imply higher rates, the cap masks the extreme and the 90th percentile becomes compressed | Use OI-weighted multi-exchange rate (CoinGlass) that is less affected by single-exchange caps; monitor for cap-binding events |
| Bull market whipsaw | High | Strong bull trend with persistent positive funding; signal repeatedly shorts into a rising market, accumulating losses | Add trend filter: only enter short when BTC is below its 50-day moving average; during strong uptrends, only take long signals (≤10th percentile) |
| Regime shift in funding behavior | Medium | Post-2024 institutional entry, funding is positive ~92% of the time; the 10th percentile may never trigger long entries | Recalibrate percentile thresholds quarterly; consider asymmetric thresholds (95th for short, 20th for long) |
| Exchange-specific data artifacts | Low | Binance funding rate API returns stale or incorrect values during extreme volatility | Cross-validate against at least one other exchange (Bybit, OKX) before generating a signal; discard if rates diverge by >50% |
| Lookahead bias in testing | High | Using the full-sample 90th percentile to evaluate historical signals; the 30-day trailing window must be strictly expanding in backtests | Use only data available at signal time; walk-forward threshold estimation with 6-month expanding windows |

## 14. Data Quality Concerns

- Binance changed its funding rate formula in 2021. Pre- and post-change funding rates are not directly comparable. The backtest must either normalize rates across the break or split into pre-2021 and post-2021 subperiods.
- Some exchanges systematically misreport or delay funding rate updates. CoinGlass OI-weighted aggregation partially mitigates this, but the underlying exchange-level data quality varies.
- Funding rate caps (0.375% per 8h on Binance) create a hard ceiling. During extreme crowding events, the true unconstrained funding rate would be higher, meaning the 90th percentile computed from capped data is downward-biased.

## 15. Similar Existing Ideas

| Idea | Domain | Similarity | Distinct? |
|------|--------|------------|-----------|
| CRYPTO-001 — Funding Rate Carry and Crowding Signal (Factor B) | Crypto | High — same mechanism, broader scope | Yes — CRYPTO-001 Factor B is a sub-hypothesis within a three-factor memo. This demo isolates the crowding-reversal signal with sharper calibration (exact percentile thresholds, holding period, trend filter) and a dedicated implementation spec. |
| CRYPTO-002 — OI-Price Divergence Reversal | Crypto | Medium — both are directional reversal signals | Yes — CRYPTO-002 uses OI-price divergence as the crowding indicator; this uses funding rate percentile. The signals may be complementary (high funding + OI divergence = stronger signal) but the mechanisms are distinct. |

## 16. Research Confidence

| Dimension | Rating (1-10) | Notes |
|-----------|---------------|-------|
| Economic intuition | 9 | Liquidation cascade mechanism is well-understood and documented |
| Source quality | 8 | Multiple Tier 1 academic sources; BIS working paper is strong institutional evidence |
| Data availability | 9 | Binance API provides free, high-quality funding rate data from 2019 |
| Signal clarity | 7 | Entry/exit rules are unambiguous; percentile threshold calibration is the main open question |
| Failure mode coverage | 7 | Primary risks identified; bull market whipsaw is the hardest to mitigate without regime filters |
| Novelty | 4 | Well-known relationship; edge lies in systematic execution, not discovery |

**Overall confidence:** `medium-high`

## 17. Handoff Readiness

- [x] References complete (6 credible, 4 Tier 1)
- [x] Data requirements specified
- [x] Signal construction clear (plain English)
- [x] Failure modes documented
- [ ] Review gate passed (not executed — demo mode)

## 18. Open Questions

1. What is the optimal percentile threshold (90th, 95th, 98th) and holding period (8h, 24h, 48h) as measured by out-of-sample Sharpe on walk-forward data from 2023–2025?
2. Does adding a trend filter (only fade the crowd against the prevailing trend) improve risk-adjusted returns, or does it filter out the most profitable contrarian entries?
3. How does the signal perform when combined with open interest — does high funding + rising OI produce a stronger reversal signal than high funding alone?
4. Does the signal work on ETH, or is it BTC-specific due to BTC's dominant role in the crypto market structure?

## 19. References (Structured)

| Ref ID | Title | Authors | Year | Venue | DOI/arXiv/SSRN | URL | Relevance |
|--------|-------|---------|------|-------|----------------|-----|-----------|
| CRYPTO-PAPER-002 | Crypto Carry | Schmeling, Schrimpf, Todorov | 2023 | BIS WP 1087 | — | https://www.bis.org/publ/work1087.htm | High funding predicts crashes — core reversal mechanism |
| CRYPTO-PAPER-001 | Fundamentals of Perpetual Futures | He, Manela, Ross, von Wachter | 2022 | arXiv | arXiv:2212.06888 | https://arxiv.org/abs/2212.06888 | Perpetual pricing theory; funding deviation from fair value |
| CRYPTO-PAPER-006 | Predictability of Funding Rates | Inan | 2025 | SSRN | SSRN:5576424 | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5576424 | Funding rate persistence supports percentile approach |
| CRYPTO-PAPER-005 | Perpetual Futures Pricing | Ackerer, Hugonnier, Jermann | 2025 | Mathematical Finance | DOI:10.1111/mafi.12442 | https://onlinelibrary.wiley.com/doi/10.1111/mafi.12442 | Theoretical validation of funding fair value |
| CRYPTO-PRACT-005 | Glassnode Insights — Market Pulse | Glassnode | Ongoing | Institutional Research | — | https://insights.glassnode.com/ | Practitioner confirmation of funding extremes as warning signal |
| CRYPTO-OFFICIAL-002 | Q3 Derivatives Report | BitMEX | 2025 | Exchange Report | — | https://blog.bitmex.com/ | Funding regime change — 92% positive in Q3 2025 |

---

*Memo authored by: Research Agent (demo mode)*
*Domain: crypto*
*Next: Review Agent gate (not executed in demo)*
*Disclaimer: This is a demo research memo for interview evidence. It does not constitute financial advice, trading recommendations, or claims of verified predictive power. Signal parameters are informed by literature but not empirically calibrated.*
