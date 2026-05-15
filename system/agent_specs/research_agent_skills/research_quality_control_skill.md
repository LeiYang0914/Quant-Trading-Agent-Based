# research_quality_control_skill.md

## Purpose

Act as an internal quality checklist before a research memo can be marked `ready_for_review`. This skill catches methodological errors, data issues, logical gaps, and presentation weaknesses before the Review Agent sees the work.

## When to Use

After a research memo draft is complete and before setting status to `ready_for_review`. Apply to every memo. This is the last internal gate before external review.

## Quality Control Checklist

Each item below receives a result: **PASS** / **FAIL** / **NEEDS_MORE_WORK**.

### A. Bias Checks

| Check | Description | Result |
|-------|-------------|--------|
| **Lookahead bias** | Does the signal use only data that would have been available at the time of the trade? Check timestamp alignment, data release schedules, and index construction dates. | |
| **Survivorship bias** | Does the universe include delisted or failed assets? If analyzing altcoins, are coins that went to zero included in historical data? | |
| **Data snooping** | How many signal variations were tested? Was the signal chosen after seeing results? If only one specification is presented, is there implicit snooping from the literature? | |
| **Sample period bias** | Is the sample period representative? Does it include bull, bear, and sideways markets? Is it long enough? | |

### B. Risk and Cost Checks

| Check | Description | Result |
|-------|-------------|--------|
| **Overfitting risk** | How many parameters? How many combinations could be tried? Is there a clear economic rationale for each parameter choice, or is any parameter "optimized"? | |
| **Regime dependence** | Does the signal only work in one market regime? Is there a plausible story for WHY it would work in that regime and not others? | |
| **Fee sensitivity** | What are the estimated one-way and round-trip costs? Is the expected gross return at least 3x the estimated transaction cost? If not, flag it. | |
| **Liquidity constraints** | Is the strategy capacity reasonable? Can the target position size be executed without excessive market impact? | |
| **Crowding risk** | Is this idea widely known? Are there ETFs, funds, or well-known strategies based on it? Crowding reduces expected returns and increases correlation with systematic deleveraging events. | |

### C. Logic and Evidence Checks

| Check | Description | Result |
|-------|-------------|--------|
| **Causal vs. correlational** | Is the economic mechanism causal (X causes Y for a specific reason) or purely correlational (X and Y move together for unknown reasons)? Causal is stronger. | |
| **Falsifiability** | Can the hypothesis be disproven? What specific evidence would show the alpha is not real? If nothing could disprove it, it's not a testable hypothesis. | |
| **Reference quality** | Are there at least 2 credible references? At least 1 Tier 1 or Tier 2 source? Are all URLs working? | |
| **No vague claims** | Does the memo contain any unsupported statements like "research suggests," "it is well known," or "studies show" without an accompanying citation? | |

### D. Structural Checks

| Check | Description | Result |
|-------|-------------|--------|
| **Domain clarity** | Is the domain (crypto, commodities, cross_market) clearly stated and consistently applied? No crypto concepts are accidentally applied to commodities, or vice versa. | |
| **Signal definition clarity** | Is the signal described unambiguously in plain English? Can a Programmer Agent implement it without asking for clarification? | |
| **Data requirements clarity** | Are data sources, fields, frequency, and coverage period specified? Are vendor options provided? | |
| **Failure modes documented** | Are at least 3 specific failure modes described, ranked by severity? Does each have a trigger condition and mitigation? | |
| **No code** | Does the memo contain any Python, SQL, Pine Script, or other executable code? Structural pseudocode is acceptable only if it cannot be copy-pasted and run. | |

### E. Completeness Checks

| Check | Description | Result |
|-------|-------------|--------|
| **All template sections filled** | Does the memo include every required section from `templates/research_memo.md`? | |
| **References table complete** | Does the references table include Ref ID, Title, Authors, Year, Venue, DOI/arXiv/SSRN, URL, and Relevance for every source? | |
| **Open questions documented** | Are unresolved questions explicitly listed rather than hidden? | |
| **Handoff readiness assessed** | Is the handoff readiness checklist completed honestly? | |

## Overall Result

After checking all items:

- **PASS:** All items PASS. Ready for `ready_for_review`.
- **NEEDS_MORE_WORK:** 1-2 items FAIL or NEEDS_MORE_WORK. Fix the issues, re-run the checklist, then proceed.
- **FAIL:** 3+ items FAIL or a critical item (lookahead bias, no references, domain mixing) FAILs. The memo needs substantial revision before it can be reviewed.

## How to Fix Common FAIL Items

| Failure | Fix |
|---------|-----|
| Lookahead bias | Add explicit timestamp alignment check. Document data release schedule. |
| No Tier 1/2 source | Search SSRN, arXiv, BIS, or exchange docs for a primary source. If none exists, document why and flag confidence as low. |
| Vague claims | Replace each vague claim with a specific citation from the references table. |
| Domain mixing | Re-read `domain_queue_management_skill.md`. If cross_market is appropriate, reclassify. If not, split the idea. |
| Signal unclear | Re-describe the signal step by step in plain English. Have a colleague (or another agent) read it back. |
| Failure modes missing | Brainstorm: what if the data source disappears? What if fees double? What if the regime changes? What if the strategy gets too large? |

## Inputs

- Draft research memo
- Alpha discovery note
- `memory/SOURCE_TRACKER.md`
- Domain market structure skill output

## Outputs

- Completed quality control checklist with PASS / FAIL / NEEDS_MORE_WORK results
- Documented issues to fix (if any)
- Final assessment: ready for review or not

## Anti-Patterns

- Skipping the checklist because "it looks fine"
- Giving a PASS to an item that should be FAIL ("the signal is mostly clear")
- Ignoring fee sensitivity because "we'll figure it out later"
- Relying on a single source because "it's a really good paper"
