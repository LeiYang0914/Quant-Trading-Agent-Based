# memo_writing_skill.md

## Purpose

Help the Research Agent write consistent, professional, institution-grade research memos. Every memo should be self-contained, traceable, and reviewable — another quant researcher should be able to read it and understand the alpha without additional context.

## When to Use

After sources are discovered, papers are analyzed, and the alpha idea is defined. Apply when drafting the research memo in `research/memos/{domain}/`.

## Required Memo Sections

Every research memo MUST include ALL sections defined in `templates/research_memo.md`. No section may be skipped. If a section is not applicable, write "Not applicable" and explain why.

The 19 required sections:
1. Title
2. Market & Instrument
3. One-Sentence Hypothesis
4. Economic Rationale
5. Behavioral or Structural Source of Edge
6. Source Inspiration (Primary + Supplementary)
7. Required Data
8. Signal Construction (Plain English Only)
9. Portfolio Construction Idea
10. Transaction Cost Sensitivity
11. Liquidity Constraints
12. Known Risks
13. Failure Modes
14. Data Quality Concerns
15. Similar Existing Ideas
16. Research Confidence
17. Handoff Readiness
18. Open Questions
19. References (Structured)

## Writing Style

- **Precise, not poetic.** Avoid adjectives like "interesting," "exciting," "powerful." State facts and reasoning.
- **Plain English always.** No code. No math notation that implies code. "The signal is the z-score of the 7-day funding rate" is acceptable; "`df['signal'] = (df['fr'] - df['fr'].rolling(7).mean()) / df['fr'].rolling(7).std()`" is not.
- **Active voice.** "The arbitrageur buys spot and shorts the perpetual" — not "spot is bought and the perpetual is shorted."
- **Short paragraphs.** One idea per paragraph. No walls of text.
- **Quantified when possible.** "Sharpe ~0.5" is better than "moderate Sharpe." "Capacity ~$20M" is better than "reasonable capacity."

## How to State Uncertainty

- **Confidence levels:** Use the 1-10 confidence scale in the memo. Be honest.
- **Conditional statements:** "If the funding rate spread persists (evidence from Fan et al. 2024 suggests it does), then..." — not "The funding rate spread persists, therefore..."
- **Acknowledge what is unknown:** Use the Open Questions section explicitly. "We do not know whether DEX funding rates behave similarly to CEX funding rates during liquidation cascades."
- **Avoid overstatement:** "This strategy generates alpha" → "This strategy may generate alpha if the cross-sectional funding rate spread persists after transaction costs."

## How to Separate Facts from Hypotheses

| Type | Example | How to Present |
|------|---------|---------------|
| **Fact (verified)** | "Binance charges 0.02% maker and 0.04% taker for BTCUSDT perps." | State directly. Cite source. |
| **Fact (from paper)** | "Fan et al. (2024) report a cross-sectional carry Sharpe of 0.74." | State directly. Cite the paper. |
| **Hypothesis (this memo's claim)** | "This cross-sectional carry strategy will generate positive risk-adjusted returns." | Use qualifiers: "may," "we hypothesize," "if the mechanism holds." |
| **Assumption** | "We assume altcoin liquidity is sufficient for $10M notional." | State as assumption. Flag in Open Questions if uncertain. |
| **Opinion / Judgment** | "We rate the economic intuition 8/10." | Clearly label as assessment. |

## How to Describe Signal Construction Without Code

Use structured plain English:

```
Signal: Cross-Sectional Funding Rate Z-Score

Step 1: At each rebalance time (daily 00:00 UTC), collect the current
funding rate for every asset in the universe from Binance.

Step 2: For each asset, compute its funding rate z-score relative to
all assets in the universe: subtract the cross-sectional mean, divide
by the cross-sectional standard deviation.

Step 3: Rank assets by z-score from highest to lowest.

Step 4: Go long the top quintile (highest relative funding rates).
Go short the bottom quintile (lowest relative funding rates).

Step 5: Equal-weight positions within each quintile.
Re-calculate at each rebalance.
```

This is acceptable. It describes the logic precisely without being executable.

## How to Document Failure Modes

Each failure mode must include:
- **What fails:** Specific mechanism that breaks
- **Severity:** High (destroys strategy) / Medium (reduces returns significantly) / Low (minor impact)
- **Trigger:** Observable condition that signals this failure
- **Mitigation:** What to do if this failure occurs

Example:
```
Failure Mode: Funding Rate Convergence
Severity: High
Trigger: The cross-sectional dispersion of funding rates collapses
         (standard deviation of funding rates across the universe
         falls below 0.005% per 8h).
Effect: The carry spread between top and bottom quintile narrows
        to below transaction costs, eliminating the alpha.
Mitigation: Monitor funding rate dispersion weekly. If dispersion
            falls below threshold, pause the strategy.
```

## How to Decide Handoff Readiness

A memo is ready for handoff (after Review Agent approval) when:

- [ ] All 19 sections are complete
- [ ] All references have working URLs
- [ ] Signal construction is unambiguous
- [ ] Data requirements include specific vendors and fields
- [ ] Edge cases (minimum 5) are listed with expected behavior
- [ ] Quality control checklist (from `research_quality_control_skill.md`) is all PASS
- [ ] Review Agent has approved

## Writing What You Don't Know

The Open Questions section is NOT a weakness — it is a sign of research quality. Explicitly state:
- Data availability uncertainties
- Regime assumptions that need testing
- Cost estimates that need refinement
- Alternative specifications that could be tested

## Inputs

- Alpha discovery note
- Paper summaries
- Market structure analysis (from crypto or commodities skill)
- Source tracker entries

## Outputs

- Research memo in `research/memos/{domain}/{alpha_id}_{slug}.md`
- Updated alpha discovery note status

## Anti-Patterns

- Skipping sections because "they don't apply" without explanation
- Writing signal logic as executable code
- Overstating confidence
- Hiding uncertainties instead of documenting them in Open Questions
- Using different terminology for the same concept across sections
- Copy-pasting source citations without verifying the URL resolves
