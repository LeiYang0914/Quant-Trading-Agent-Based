# Alpha Discovery Note: OI-Price Divergence Reversal

**Alpha ID:** CRYPTO-002
**Domain:** crypto
**Date:** 2026-05-16
**Status:** ready_for_review

---

## Discovery

**Discovery source:** Practitioner observation (four-quadrant OI-price framework commonly used by crypto traders) + theoretical foundation from Bessembinder & Seguin (1993) on OI as market depth proxy.

**Raw observation:** When perpetual futures open interest and spot price diverge over a multi-day window (price up + OI down, or price down + OI up), the trend lacks structural support and frequently reverses. The practitioner "four-quadrant framework" treats this as a warning signal, but no quantitative specification with entry/exit thresholds exists in the literature for crypto markets.

## Hypothesis

> When the 7-day change in perpetual futures OI and the 7-day change in spot price have opposite signs, and the divergence magnitude exceeds a threshold normalized by 30-day historical volatility, price will revert toward the OI-implied direction over the subsequent 1-7 days. Signal strength increases when OI is at extreme absolute levels and when funding rates are not already at extremes in the signal direction.

## Why This May Be an Edge

1. **Attention asymmetry:** Most traders focus on price action. OI requires monitoring a second data stream and cross-referencing it with price. Retail systematically underweights OI.
2. **Quantification gap:** The four-quadrant framework is widely known qualitatively but rarely specified quantitatively with precise thresholds and holding periods.
3. **Crypto-specific amplification:** Liquidation cascades in perpetual futures amplify reversals beyond what pure mean reversion predicts, creating a larger alpha capture window.
4. **Structural depth mechanism:** Falling OI = thinning market depth = larger price impact per unit of order flow = stronger reversal force (confirmed for crypto by Matsui et al. 2022).

## Market Structure Mechanism

The edge is structural, not behavioral:

- Open interest measures outstanding capital committed to directional positions
- Rising OI = fresh capital entering = trend has structural support
- Falling OI = capital exiting = trend losing foundation
- When price and OI diverge, the price move is happening on thinning market depth, making it fragile
- In crypto perpetuals specifically, high-OI environments with one-sided positioning create liquidation cascade risk — the initial reversal triggers forced liquidations that amplify the move

Key crypto-specific microstructure factors:
- **Cross-margin cascades:** BTC losses → ETH margin liquidations → contagion across positions
- **Retail herding in OI:** Retail tends to pile into trending positions late, inflating OI near tops and bottoms — the OI extreme itself becomes a reversal signal
- **Clearing-house mechanics:** Perpetual futures on the same exchange share margin, creating cross-contamination that traditional futures lack

## Required Data

| Dataset | Source Candidates | Availability |
|---------|-------------------|--------------|
| BTC/ETH perpetual OI (daily) | Binance API, CoinGlass, Coinalyze | Needs check — Binance has REST endpoint; CoinGlass has free tier + paid API |
| BTC/ETH spot price (daily) | Binance API | Available — free tier |
| 8h funding rate | Binance API, CoinGlass | Available — free tier |
| Futures expiry calendar | Exchange docs | Available — static list |

## Suggested Signal (Plain English)

**Step 1:** At each daily close, compute the 7-day percentage change in perpetual futures OI and the 7-day percentage change in spot price for BTC and ETH separately.

**Step 2:** Determine divergence sign: if sign(ΔPrice_7d) ≠ sign(ΔOI_7d), a divergence is present. Score = ΔPrice_7d × ΔOI_7d (negative = divergence).

**Step 3:** Normalize divergence magnitude by dividing by the 30-day rolling standard deviation of daily price returns. This gives a Z-score-equivalent: how unusual is this divergence relative to recent volatility.

**Step 4:** Entry: enter when divergence score is negative AND normalized divergence > 1.5σ AND funding rate is not in the top/bottom 10th percentile (avoid catching extremes that are already due for reversal).

**Step 5:** Exit after N days (sweep 1-7) or if OI and price re-align for 2 consecutive days. Early exit if stop-loss hit (2× ATR).

## Similar Known Strategies

| Strategy | Domain | Similarity | Reference |
|----------|--------|------------|-----------|
| OI-price four-quadrant framework | Traditional futures | High (same concept) | Practitioner literature |
| OI-volume-price divergence | Equity futures | Medium | Market profile / volume analysis |
| Funding rate reversal (CRYPTO-001) | Crypto | Low (different signal — funding rates vs OI) | Our own work |

## What Could Invalidate It

1. OI data is too noisy or misreported to generate reliable signals (Giagkiozis & Said 2024 documents systematic OI misreporting by major exchanges)
2. Signal is entirely subsumed by simple price momentum reversal — OI adds zero marginal predictive power
3. Transaction costs (0.04% taker fee + slippage) consume the edge in all regimes
4. Edge only exists in bull/bear trending markets but fails in range-bound markets where most signals cluster

## Reference Requirements

**Minimum references needed before memo:** 2 credible, including 1 Tier 1 or Tier 2.

**Current references:**

| Ref ID | Title | Authors | Year | Tier | URL | Status |
|--------|-------|---------|------|------|-----|--------|
| CRYPTO-PAPER-008 | Reconciling Open Interest with Traded Volume in Perpetual Swaps | Giagkiozis & Said | 2024 | 1 | https://arxiv.org/abs/2310.14973 | Verified |
| CRYPTO-PAPER-009 | On the Dynamics of Solid, Liquid and Digital Gold Futures | Matsui, Al-Ali, Knottenbelt | 2022 | 1 | https://arxiv.org/abs/2202.09845 | Verified |
| CRYPTO-PAPER-010 | Exploring the Impact: How Decentralized Exchange Designs Shape Traders' Behavior | Chen, Ma, Nie | 2024 | 1 | https://arxiv.org/abs/2402.03953 | Verified |
| CRYPTO-PAPER-011 | Price Volatility, Trading Volume, and Market Depth: Evidence from Futures Markets | Bessembinder & Seguin | 1993 | 1 | https://www.jstor.org/stable/2331234 | Verified (paywalled) |

**References status:** Sufficient

## Status Tracking

- [x] 2+ credible references found (5 sources, 4 papers + practitioner)
- [x] 1+ Tier 1/2 source confirmed (4 Tier 1 papers)
- [ ] Data availability checked — CoinGlass and Binance OI data available but quality concerns need resolution
- [x] Signal defined in plain English
- [x] Failure modes identified
- [x] Ready for research memo (memo already exists)

---

*Note: This discovery note cannot become a research memo until reference requirements are met.*
