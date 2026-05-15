# Paper Summary

**Source ID:** CRYPTO-PAPER-011
**Domain:** crypto
**Source type:** journal
**Date reviewed:** 2026-05-16

---

## Paper Details

**Title:** Price Volatility, Trading Volume, and Market Depth: Evidence from Futures Markets
**Authors:** Hendrik Bessembinder, Paul J. Seguin
**Year:** 1993
**Venue / Journal / Conference:** Journal of Financial and Quantitative Analysis, Vol. 28, No. 1
**DOI / arXiv / SSRN:** — (JSTOR)
**URL:** https://www.jstor.org/stable/2331234

---

## Research Question

What are the relationships between price volatility, trading volume, and open interest in futures markets? Does OI serve as a proxy for market depth?

## Market Studied

Eight different futures markets across multiple asset classes over a multi-year period. Includes both financial and commodity futures.

## Data Used

Daily futures prices, trading volume, and open interest from major US futures exchanges. Multi-year sample.

## Methodology

Time-series regression of volatility on volume and OI. Decomposition of expected and unexpected components of volume and OI. Controls for contract maturity and day-of-week effects.

## Main Findings

1. OI is a proxy for market depth. Higher OI = deeper market = ability to absorb larger orders with less price impact.
2. Unexpected increases in OI are associated with lower volatility, consistent with the interpretation that OI reflects the entry of additional liquidity providers.
3. Volume and OI have opposite effects on volatility: volume increases it, OI decreases it. This is the foundational finding for all OI-based alpha research.
4. The negative OI-volatility relationship is robust across different futures markets and time periods.

## Limitations

1. Data from 1970s-1980s — traditional futures markets only (no crypto, no electronic trading).
2. Daily frequency — within-day OI and volatility dynamics are not captured.
3. Does not test OI-price divergence as a trading signal — only establishes the OI-volatility relationship.

---

## Applicability Assessment

### Applicability to Crypto

Foundational. This paper provides the theoretical basis for treating OI as a market depth proxy in any futures market, including crypto. The extension to crypto is empirically supported by Matsui et al. (2022) for CME Bitcoin futures and, by extension, for perpetual swaps (with caveats about exchange reporting quality).

### Applicability to Commodities

Directly applicable — commodity futures are part of the original study. The OI-depth relationship is a general futures market property.

---

## Alpha Ideas Derived

| Alpha ID | Idea | Status |
|----------|------|--------|
| CRYPTO-002 | OI-Price Divergence Reversal | Researching — theoretical foundation |

---

## Reliability Assessment

**Reliability tier:** 1
**Justification:** Peer-reviewed journal paper (JFQA). One of the most cited papers in futures market microstructure. Findings replicated across multiple markets and time periods.

---

## Notes for Future Review

- This is the theoretical ancestor of the OI-price divergence alpha. The mechanism: falling OI → thinning depth → larger price impact → stronger reversal force.
- The finding that unexpected OI increases reduce volatility is symmetric to the price divergence mechanism: if unexpected OI increases stabilize prices, then unexpected OI decreases (which we detect through the divergence) should destabilize prices.
- Critically, the paper establishes that OI contains information about market depth that is NOT captured by trading volume alone — justifying the use of OI-price divergence as a distinct signal from volume-price divergence.
