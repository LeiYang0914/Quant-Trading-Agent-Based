# alpha_discovery_skill.md

## Purpose

Help the Research Agent convert raw observations, paper findings, and market anomalies into structured, testable alpha ideas. This skill separates speculation from hypothesis formation and prevents weak ideas from consuming research time.

## When to Use

After sources are discovered and papers are analyzed. Apply before writing any alpha discovery note or research memo.

## From Observation to Alpha Idea

The Research Agent must separate these layers clearly:

### Layer 1: Raw Observation
What was seen? A fact, a data pattern, a price behavior, a market event.
*Example: "BTC perpetual funding rates on Binance are negative 80% of the time in Q1 2024."*

### Layer 2: Market Anomaly
Why is the observation surprising relative to efficient markets or standard models?
*Example: "If funding rates reflect net positioning demand, persistently negative funding suggests persistent short demand that should drive spot prices down — but spot was rising."*

### Layer 3: Economic Intuition
What economic force could explain this anomaly?
- Risk premium: compensation for bearing a specific risk
- Behavioral: systematic investor mistake or attention bias
- Structural: institutional constraint, regulation, market design
- Flow-driven: predictable order flow from a known participant type

### Layer 4: Behavioral Explanation (if applicable)
Is there a behavioral bias at work? Overconfidence, attention, anchoring, disposition effect, herding?
*Example: "Retail traders chase altcoin pumps, opening leveraged longs at local tops. Funding rates spike as a result, then mean-revert as the pump fades."*

### Layer 5: Structural Explanation (if applicable)
Is there a structural mechanism? Arbitrage constraints, custody fragmentation, regulatory asymmetry, exchange rules?
*Example: "Altcoin perpetual arbitrage requires spot borrowing on fragmented venues. The operational cost of arbitraging each additional altcoin creates a persistent cross-sectional carry spread."*

### Layer 6: Possible Signal
Describe in plain English how the observation could become a trading signal.
- What is measured?
- Over what lookback?
- What threshold triggers action?
- Direction: long, short, or both?

### Layer 7: Required Data
- What data is needed to compute this signal?
- Is it currently available? From which vendors?
- What frequency is required?

### Layer 8: Trading Universe
- Which assets? How many?
- How is the universe filtered? (market cap, liquidity, exchange listing)
- How often is the universe reconstituted?

### Layer 9: Expected Horizon
- Intraday, daily, weekly, monthly?
- What is the expected holding period?
- How quickly would the edge decay if discovered?

### Layer 10: Possible Invalidation
What evidence would disprove this alpha?
- If signal works in-sample but fails out-of-sample
- If signal disappears after accounting for transaction costs
- If signal is explained by a known factor (momentum, carry, vol)
- If signal only works in one market regime
- If data quality issues explain the apparent edge

### Layer 11: Minimum Evidence Required
What is the minimum evidence needed before this becomes a research memo?
- At least 2 credible references (1+ Tier 1/2)
- Data availability confirmed or a clear path to obtaining data
- Falsifiable hypothesis stated
- Signal defined in plain English

## Quality Filter Questions

Before writing an alpha discovery note, the Research Agent must answer:

1. **Is this causal or only correlational?**
   Correlational is weaker. If you cannot articulate WHY X causes Y, flag the confidence as low.

2. **Is this likely crowded?**
   Is the idea already widely known? Has it been written about extensively? Are there ETFs or products based on it? Crowded ideas are not automatically rejected, but the bar is higher.

3. **Can the data be obtained?**
   If the required data is proprietary, expensive, or not historically available, flag it. An idea without obtainable data is not actionable.

4. **Would fees and slippage destroy the edge?**
   Estimate rough transaction costs. If the expected gross return is within 2x of estimated costs, flag it.

5. **Is this domain-specific or accidentally mixed?**
   Does the idea accidentally blend crypto and commodities concepts? If so, classify as cross_market or split into two ideas.

6. **Is there enough literature or official documentation?**
   If the idea relies entirely on one blog post or one tweet, reject it. Minimum 2 credible sources required.

## Alpha Discovery Note Output

Write to `research/ideas/proposed/{domain}/{alpha_id}_{slug}.md` following `templates/alpha_discovery_note.md`.

Required fields:
- Alpha ID
- Domain
- Discovery source
- Raw observation
- Hypothesis (falsifiable)
- Why this may be an edge
- Market structure mechanism
- Required data (with source candidates)
- Suggested signal (plain English)
- Similar known strategies
- What could invalidate it
- Minimum references needed before memo
- Current references (with tier classification)
- Status

## Status Progression

```
idea → researching → needs_data_check → needs_more_sources → ready_for_review
```

- `idea`: just documented, no sources yet
- `researching`: actively collecting sources and defining the signal
- `needs_data_check`: signal defined, waiting for data availability confirmation
- `needs_more_sources`: not enough credible references — blocked
- `ready_for_review`: all quality gates passed

## Inputs

- Raw observation, paper findings, or backlog idea
- Sources from `source_discovery_skill`
- Paper analysis from `paper_analysis_skill`
- Domain market structure context

## Outputs

- Alpha discovery note in `research/ideas/proposed/{domain}/`
- Updated `memory/ALPHA_BACKLOG.md`

## Anti-Patterns

- Writing a discovery note for every fleeting thought — filter first
- Treating a correlation as causal without explanation
- Proposing an idea with zero references
- Mixing crypto and commodities in one discovery note without cross_market classification
- Skipping the invalidation question — if you cannot say what would disprove it, the hypothesis is not falsifiable
