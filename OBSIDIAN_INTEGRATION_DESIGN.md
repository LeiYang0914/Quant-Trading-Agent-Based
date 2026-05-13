# Obsidian Integration Design — Quant Research Agent

**Date:** 2026-05-13
**Status:** Design — Pending Implementation
**Author:** Quant Alpha Researcher Agent

---

This document specifies how Obsidian is integrated into the Quant Research Agent as its long-term research memory and alpha idea library. The Obsidian vault is the Research Agent's **single source of truth for research knowledge**. It does not replace the existing project memory files (`research_memory/`) — it extends them into a richer, interlinked knowledge graph.

---

## 1. Recommended Obsidian Vault Structure

```
Quant-Research-KB/
├── 00_Inbox/                    # Raw, unprocessed research captures
├── 01_Concepts/                 # Core quant concepts (reference library)
├── 02_Alpha_Ideas/              # Structured alpha idea notes
├── 03_Strategy_Hypotheses/      # Detailed strategy hypotheses
├── 04_Market_Regimes/           # Regime observations and classifications
├── 05_Paper_Notes/              # Paper/article summaries
├── 06_Data_Source_Notes/        # Data vendor and dataset documentation
├── 07_Risk_Failure_Modes/       # Systematic risk and failure mode catalog
├── 08_Backtest_Requests/        # Specifications for backtests (no code)
├── 09_Programmer_Handoffs/      # Structured handoff documents
├── 10_Research_Reviews/         # Weekly/monthly research reviews
├── 11_Rejected_Deprecated/      # Rejected and deprecated ideas (preserved)
├── 12_Agent_Prompts/            # Prompt templates and agent instructions
├── 99_Templates/                # Obsidian note templates
└── Dashboard.md                 # MOC (Map of Content) — entry point
```

### Folder Purposes

| Folder | Purpose | Who Writes | Who Reads |
|--------|---------|------------|-----------|
| `00_Inbox/` | Captured ideas, links, observations not yet processed. Low structure. Temporary staging. | Research Agent | Research Agent |
| `01_Concepts/` | Atomic notes for each quant concept: mean reversion, momentum, carry, volatility, etc. Each note is a linked reference. | Research Agent | Research Agent, Programmer Agent |
| `02_Alpha_Ideas/` | One note per alpha idea. The core library. Each note follows the Alpha Idea template. | Research Agent | Research Agent, Programmer Agent |
| `03_Strategy_Hypotheses/` | Expanded hypotheses derived from alpha ideas. More detailed than alpha ideas — includes precise signal logic, entry/exit rules, parameter ranges. | Research Agent | Programmer Agent |
| `04_Market_Regimes/` | Observations about market regime shifts, volatility clusters, correlation breakdowns, macro events. | Research Agent | Research Agent |
| `05_Paper_Notes/` | Summaries of academic papers, institutional reports, blog posts. One note per source. | Research Agent | Research Agent |
| `06_Data_Source_Notes/` | Documentation for each data vendor: what they provide, frequency, coverage, known issues, cost. | Research Agent | Research Agent, Programmer Agent |
| `07_Risk_Failure_Modes/` | Catalog of failure modes observed across ideas: overfitting, lookahead, crowding, regime change, cost underestimation. | Research Agent | Research Agent |
| `08_Backtest_Requests/` | Formal backtest request notes. Specify what to test without writing code. | Research Agent | Programmer Agent |
| `09_Programmer_Handoffs/` | Final handoff documents for the Quant Trading Programmer Agent. | Research Agent | Programmer Agent |
| `10_Research_Reviews/` | Weekly/monthly research reviews summarizing progress, dead ends, insights, and next priorities. | Research Agent | Research Agent |
| `11_Rejected_Deprecated/` | Ideas that were rejected or deprecated, with reasons. Never deleted — preserved as institutional memory. | Research Agent | Research Agent |
| `12_Agent_Prompts/` | Prompt templates for the Research Agent itself. Self-documenting operating procedures. | Research Agent | Research Agent |
| `99_Templates/` | Obsidian template files. Used via Obsidian's "Insert Template" or manually copied by the agent. | Research Agent | Research Agent |

### Dashboard.md (Map of Content)

The root `Dashboard.md` is the entry point. It contains:
- Links to active research
- Links to the alpha idea pipeline by status
- Links to recent paper notes
- Links to pending backtest requests
- Links to pending programmer handoffs
- Links to recent research reviews
- Quick-search links by tag

---

## 2. Markdown Templates

All templates use Obsidian YAML frontmatter. Tags use the `#tag` format. Backlinks use `[[wikilink]]` format.

### 2.1 Alpha Idea Note

```markdown
---
title: ""
type: alpha_idea
status: idea
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - alpha_idea
  - ""
concepts:
  - ""
markets:
  - ""
assets:
  - ""
timeframe: ""
source_papers:
  - ""
related_ideas:
  - ""
priority: medium
confidence: speculative
research_owner: Quant Research Agent
implementation_owner: Quant Trading Programmer Agent
---

# [Alpha Idea Title]

## One-Line Summary
[Single sentence describing the alpha and its economic mechanism.]

## Market & Universe
- Market: [crypto / commodities / cross-market]
- Assets: [specific assets]
- Venues: [exchanges / markets]
- Timeframe: [intraday / daily / weekly]

## Mechanism
[Explain the economic mechanism, market structure feature, or behavioral bias that generates the edge. Why does this exist?]

## Why the Edge Persists
[What prevents this alpha from being arbitraged away? Frictions, capacity constraints, behavioral biases, regulatory barriers?]

## Source Inspiration
- [[Paper Note 1]] — [What this source contributes]
- [[Paper Note 2]] — [What this source contributes]

## Alpha Hypothesis
> "[Precise, falsifiable statement of the expected relationship.]"

## Signal Sketch (Plain English)
- **Entry signal:** [Describe in plain English — no code]
- **Exit signal:** [Describe in plain English — no code]
- **Position sizing:** [Conceptual sizing rule]
- **Expected holding period:** [Duration]
- **Signal direction:** [Long / Short / Both]

## Data Requirements
| Dataset | Fields | Frequency | Vendor | Notes |
|---------|--------|-----------|--------|-------|
| | | | | |

## Assumptions
1. [Assumption 1]
2. [Assumption 2]

## Expected Edge
- [Expected return profile, Sharpe, drawdown expectation — qualitative only]

## Risk Factors
1. [Risk 1]
2. [Risk 2]

## Failure Modes
| Failure Mode | Severity (1-5) | Mitigation |
|-------------|----------------|------------|
| | | |

## What Would Disprove This
[Specific evidence that would falsify the hypothesis.]

## Related Concepts
- [[Concept 1]]
- [[Concept 2]]

## Related Alpha Ideas
- [[Alpha Idea 1]]
- [[Alpha Idea 2]]

## Open Questions
1. [Question 1]
2. [Question 2]

## Next Action
- [ ] [Next research step or handoff step]

---

*Research responsibility: Quant Research Agent*
*Implementation responsibility: Quant Trading Programmer Agent*
*Status: [[Alpha Idea Lifecycle#idea|idea]]*
```

### 2.2 Strategy Hypothesis Note

```markdown
---
title: ""
type: strategy_hypothesis
status: researching
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - strategy_hypothesis
  - ""
concepts:
  - ""
markets:
  - ""
parent_alpha: ""
derived_from: ""
research_owner: Quant Research Agent
implementation_owner: Quant Trading Programmer Agent
---

# [Strategy Hypothesis Title]

## Parent Alpha Idea
- Derived from: [[Alpha Idea Name]]

## Hypothesis Statement
> "[Precise, testable statement of the strategy hypothesis.]"

## Signal Logic (Plain English)
### Entry Conditions
[Describe in plain English all entry conditions. No code.]

### Exit Conditions
[Describe in plain English all exit conditions. No code.]

### Filters
[Describe any filters applied before signal generation.]

### Parameter Ranges
| Parameter | Proposed Range | Rationale |
|-----------|---------------|-----------|
| | | |

## Expected Behavior
- **In-sample expectation:** [Qualitative]
- **Out-of-sample expectation:** [Qualitative]
- **Regimes where it should work:** [Conditions]
- **Regimes where it should fail:** [Conditions]

## Risk & Edge
- **Expected edge:** [Qualitative description]
- **Capacity estimate:** [Rough capacity range]
- **Transaction cost sensitivity:** [Low / Medium / High]

## Failure Modes
| Failure Mode | Severity | Detection Method |
|-------------|----------|-----------------|
| | | |

## Assumptions
1. [Assumption 1]
2. [Assumption 2]

## Required Testing
- [ ] [Test 1]
- [ ] [Test 2]

## Related
- [[Alpha Idea Name]]
- [[Market Regime Note]]
- [[Risk Note]]

## Next Action
- [ ] [Next step]

---

*Research responsibility: Quant Research Agent*
*Implementation responsibility: Quant Trading Programmer Agent*
```

### 2.3 Paper / Article Summary Note

```markdown
---
title: ""
type: paper_note
status: summarized
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - paper_note
  - ""
concepts:
  - ""
source_type: paper
authors: ""
year: 
journal: ""
url: ""
verified: false
---

# [Paper Title]

## Citation
**Authors:** [Authors]
**Year:** [YYYY]
**Journal / Venue:** [Journal or working paper series]
**Link:** [Full URL or DOI — must resolve]
**Verification:** [Confirmed exists / pending]

## One-Paragraph Summary
[Concise summary of the paper's main contribution.]

## Key Findings
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

## Methods Used
- [Method 1]
- [Method 2]

## Data Used
| Dataset | Period | Frequency | Source |
|---------|--------|-----------|--------|
| | | | |

## Relevance to Our Research
[What specific result, mechanism, or dataset is useful for our alpha research.]

## Applicable Alpha Ideas
- [[Alpha Idea 1]]
- [[Alpha Idea 2]]

## Critique & Limitations
1. [Limitation 1]
2. [Limitation 2]

## Key Quotes
> "[Important quote with page/section reference.]"

## Related Papers
- [[Paper Note 1]]
- [[Paper Note 2]]

## Tags
#paper #[[concept]] #[[market]]

---

*Research responsibility: Quant Research Agent*
```

### 2.4 Market Regime Observation Note

```markdown
---
title: ""
type: market_regime
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - market_regime
  - ""
markets:
  - ""
regime_type: ""
observation_period_start: YYYY-MM-DD
observation_period_end: YYYY-MM-DD
confidence: speculative
---

# [Market Regime Observation Title]

## Observation
[What was observed. Be specific: date range, assets, metrics.]

## Regime Classification
- **Type:** [Trending / Mean-reverting / High vol / Low vol / Crisis / Calm / Correlation shift / etc.]
- **Market:** [crypto / commodities / cross-market]
- **Assets affected:** [List]

## Evidence
1. [Specific data point or chart reference]
2. [Specific data point or chart reference]

## Hypothesized Cause
[Why this regime emerged. Macro event, structural change, flow-driven, etc.]

## Alpha Implications
- **Strategies that benefit:** [List]
- **Strategies that suffer:** [List]
- **New alpha opportunities:** [List]

## Expected Duration
- [Short-lived / Medium-term / Structural]

## Related Observations
- [[Market Regime Note 1]]
- [[Market Regime Note 2]]

## Related Alpha Ideas
- [[Alpha Idea 1]]

## Tags
#market_regime #[[regime_type]] #[[market]]

---

*Research responsibility: Quant Research Agent*
```

### 2.5 Risk / Failure Mode Note

```markdown
---
title: ""
type: risk_failure_mode
status: documented
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - risk_failure_mode
  - ""
concepts:
  - ""
severity: medium
frequency: ""
affected_ideas:
  - ""
---

# [Risk / Failure Mode Title]

## Category
- [Overfitting / Lookahead Bias / Crowding / Regime Change / Transaction Cost Underestimation / Slippage / Capacity / Data Error / Survivorship Bias / Selection Bias / Other]

## Description
[Detailed description of this risk or failure mode.]

## How It Manifests
[How to detect this failure mode. What the evidence looks like.]

## Examples from Research
1. [[Alpha Idea Name]] — [How this failure mode applied]
2. [[Alpha Idea Name]] — [How this failure mode applied]

## Mitigation Strategies
1. [Strategy 1]
2. [Strategy 2]

## Detection Tests
- [ ] [Test that would surface this failure mode]
- [ ] [Test that would surface this failure mode]

## Related Concepts
- [[Overfitting]]
- [[Transaction Cost]]
- [[Slippage]]
- [[Lookahead Bias]]

## Tags
#risk #failure_mode #[[category]]

---

*Research responsibility: Quant Research Agent*
```

### 2.6 Backtest Request Note

```markdown
---
title: ""
type: backtest_request
status: pending
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - backtest_request
  - ""
source_alpha: ""
requested_by: Quant Research Agent
assigned_to: Quant Trading Programmer Agent
priority: medium
---

# Backtest Request: [Alpha Idea Name]

## Source Alpha Idea
- [[Alpha Idea Name]]
- [[Strategy Hypothesis Name]]

## What to Test
[Plain English description of what the backtest should evaluate.]

## Signal Specification (Plain English)
### Entry Logic
[Describe entry logic in plain English. No code. May use high-level pseudocode.]

### Exit Logic
[Describe exit logic in plain English. No code.]

### Position Sizing
[Describe position sizing logic in plain English.]

### Filters
[Describe any filters.]

## Universe & Data
| Parameter | Value |
|-----------|-------|
| Assets | |
| Venues | |
| Data frequency | |
| Start date | |
| End date | |
| Data source | [[Data Source Note]] |

## Backtest Design
| Parameter | Value |
|-----------|-------|
| In-sample period | |
| Out-of-sample period | |
| Walk-forward design | |
| Benchmark | |
| Rebalance frequency | |
| Holding period | |
| Transaction cost model | [[Transaction Cost]] |
| Slippage model | [[Slippage]] |

## Expected Metrics to Report
- [ ] Equity curve
- [ ] Sharpe ratio
- [ ] Max drawdown
- [ ] Win rate
- [ ] Profit factor
- [ ] Turnover
- [ ] Parameter sensitivity heatmap
- [ ] Sub-period performance breakdown

## Robustness Checks Required
- [ ] Parameter sweep
- [ ] Sub-period analysis
- [ ] Out-of-sample test
- [ ] Alternative universe test
- [ ] Transaction cost stress test

## What NOT to Test
- [Anything explicitly excluded from scope.]

## Failure Mode Awareness
[Specific failure modes to watch for, from [[Risk Note]]]

## Acceptance Criteria
[What results would make this alpha worth pursuing further.]

## Rejection Criteria
[What results would lead to rejecting this alpha.]

## Related
- [[Alpha Idea Name]]
- [[Risk Note Name]]

---

*Requested by: Quant Research Agent*
*To be implemented by: Quant Trading Programmer Agent*
*This is a research specification only. No trading code.*
```

### 2.7 Programmer Handoff Note

```markdown
---
title: ""
type: programmer_handoff
status: pending
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - programmer_handoff
  - ""
source_alpha: ""
research_owner: Quant Research Agent
implementation_owner: Quant Trading Programmer Agent
handoff_version: 1
---

# Programmer Handoff: [Alpha Title]

## Handoff Summary
- **Alpha idea:** [[Alpha Idea Name]]
- **Research memo:** [Link to research memo in project]
- **Backtest request:** [[Backtest Request Name]]
- **Date handed off:** YYYY-MM-DD
- **Handoff version:** 1

## Alpha Summary
[One-paragraph summary of the alpha idea, mechanism, and expected behavior. Written by Research Agent.]

## Market & Universe
| Parameter | Value |
|-----------|-------|
| Market | |
| Assets | |
| Venues | |
| Timeframe | |

## Signal Specification (Plain English)
### Entry Logic
[Describe entry logic in plain English. Structural description, NOT code.]

### Exit Logic
[Describe exit logic in plain English. Structural description, NOT code.]

### Position Sizing
[Describe position sizing logic in plain English.]

### Risk Management
[Describe risk management logic in plain English.]

## Data Requirements
| Dataset | Fields | Frequency | Vendor | Access Method |
|---------|--------|-----------|--------|---------------|
| | | | | |

## Preprocessing Description
1. [Step 1 — describe in plain English, no code]
2. [Step 2 — describe in plain English, no code]

## Backtest Scope
| Parameter | Value |
|-----------|-------|
| In-sample | |
| Out-of-sample | |
| Benchmark | |
| Rebalance frequency | |
| Transaction cost assumption | |

## Known Risk Factors
1. [Risk 1]
2. [Risk 2]

## Failure Modes (Researcher's Notes)
| Failure Mode | Severity | What to Watch |
|-------------|----------|---------------|
| | | |

## Assumptions
1. [Assumption 1]
2. [Assumption 2]

## Expected Edge (Qualitative)
[Qualitative description of expected edge. No performance claims before backtesting.]

## What the Programmer Should Implement
- [ ] [Implementation task 1]
- [ ] [Implementation task 2]

## What the Programmer Should NOT Implement
- [ ] [Excluded scope 1]
- [ ] [Excluded scope 2]

## Open Research Questions
1. [Question for future research]
2. [Question for future research]

## Constraints
- **Do not** implement live trading
- **Do not** connect to broker APIs
- **Do not** place orders
- This is a research backtest only
- Return results to Research Agent for interpretation

## Acceptance Criteria
[What backtest results would indicate the alpha is worth further investigation.]

## Rejection Criteria
[What backtest results would indicate the alpha should be rejected or deprecated.]

## Related Documents
- [[Alpha Idea Name]]
- [[Strategy Hypothesis Name]]
- [[Backtest Request Name]]
- [[Risk Note Name]]
- [[Paper Note Name]]

---

*Handoff prepared by: Quant Research Agent*
*For: Quant Trading Programmer Agent*
*Implementation responsibility: Quant Trading Programmer Agent*
*Research responsibility: Quant Research Agent*
```

### 2.8 Weekly Research Review Note

```markdown
---
title: "Research Review — YYYY-MM-DD"
type: research_review
status: complete
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - research_review
  - weekly_review
review_period_start: YYYY-MM-DD
review_period_end: YYYY-MM-DD
---

# Research Review — [Week Ending YYYY-MM-DD]

## Summary
[One-paragraph summary of the week's research activity.]

## Alpha Ideas Worked On
| Alpha Idea | Status Change | Key Finding |
|------------|--------------|-------------|
| [[Alpha 1]] | idea → researching | [Finding] |
| [[Alpha 2]] | researching → ready_for_backtest | [Finding] |

## New Alpha Ideas Added
- [[Alpha Idea Name]] — [One-line description]

## Ideas Rejected This Week
- [[Alpha Idea Name]] — [Reason for rejection]

## Papers Read
- [[Paper Note 1]]
- [[Paper Note 2]]

## Market Regime Observations
- [[Market Regime Note 1]]

## Backtest Requests Sent
- [[Backtest Request 1]] → [[Programmer Handoff 1]]

## Programmer Handoffs Completed
- [[Programmer Handoff 1]] — Status: pending

## Key Insights
1. [Insight 1]
2. [Insight 2]

## Dead Ends & Lessons
1. [Dead end or lesson 1]
2. [Dead end or lesson 2]

## Open Questions
1. [Question 1]
2. [Question 2]

## Next Week Priorities
1. [Priority 1]
2. [Priority 2]

## Backlog Changes
- Promoted: [[Alpha Idea Name]]
- Demoted: [[Alpha Idea Name]]
- Deprecated: [[Alpha Idea Name]]

---

*Research responsibility: Quant Research Agent*
```

### 2.9 Rejected Idea Note

```markdown
---
title: ""
type: rejected_idea
status: rejected
created: YYYY-MM-DD
rejected_date: YYYY-MM-DD
tags:
  - rejected_idea
  - ""
concepts:
  - ""
original_priority: ""
rejection_reason_category: ""
---

# [Rejected Idea Title]

## Original Alpha Idea
- [[Original Alpha Idea Note]]

## Original Hypothesis
> "[The original hypothesis.]"

## Why Rejected
[Detailed explanation of why this idea was rejected.]

## Rejection Category
- [ ] Overfitting / data mining artifact
- [ ] No economic mechanism (spurious)
- [ ] Edge too small after costs
- [ ] Capacity too low
- [ ] Regime-dependent (not robust)
- [ ] Implementation infeasible
- [ ] Already known / crowded
- [ ] Data not available
- [ ] Backtest showed no edge
- [ ] Assumptions violated
- [ ] Other: [specify]

## Evidence for Rejection
1. [Evidence point 1]
2. [Evidence point 2]

## What We Learned
[What this rejected idea taught us that might inform future research.]

## Could This Be Revisited?
- **Conditions for revisit:** [What would need to change — market structure, data availability, technology, etc.]
- **Likelihood of revisit:** [Low / Medium / High]

## Related Ideas (Avoid Similar)
- [[Alpha Idea Name]] — [Why this is similar and should be checked]
- [[Alpha Idea Name]] — [Why this is similar and should be checked]

## Tags
#rejected #[[rejection_category]] #[[market]]

---

*Research responsibility: Quant Research Agent*
*This idea is preserved for institutional memory. Do not delete.*
```

---

## 3. Research Agent Write Workflow

### 3.1 When to Create a New Note

| Trigger | Note Type | Folder | Template |
|---------|-----------|--------|----------|
| New alpha idea conceived | Alpha Idea | `02_Alpha_Ideas/` | Alpha Idea Note |
| Alpha idea refined with detailed signal logic | Strategy Hypothesis | `03_Strategy_Hypotheses/` | Strategy Hypothesis Note |
| Paper or article read and summarized | Paper Note | `05_Paper_Notes/` | Paper/Article Summary Note |
| Market regime shift observed | Market Regime | `04_Market_Regimes/` | Market Regime Observation Note |
| Risk or failure mode identified | Risk/Failure Mode | `07_Risk_Failure_Modes/` | Risk/Failure Mode Note |
| Backtest needed for an alpha | Backtest Request | `08_Backtest_Requests/` | Backtest Request Note |
| Alpha ready for programmer | Programmer Handoff | `09_Programmer_Handoffs/` | Programmer Handoff Note |
| Weekly review | Research Review | `10_Research_Reviews/` | Weekly Research Review Note |
| Idea rejected or deprecated | Rejected Idea | `11_Rejected_Deprecated/` | Rejected Idea Note |
| New concept defined | Concept Note | `01_Concepts/` | (concept template) |
| New data source documented | Data Source Note | `06_Data_Source_Notes/` | (data source template) |

### 3.2 When to Update an Existing Note (Not Create New)

| Situation | Action |
|-----------|--------|
| Status change (e.g., idea → researching) | Update `status` in YAML frontmatter. Update `updated` date. Append to note body if significant. |
| New evidence supports existing idea | Add to note body under a new subheading. Update `updated` date. |
| New failure mode discovered for existing idea | Add to Failure Modes table. Link to relevant Risk Note. |
| Market regime evolves | Update Market Regime note with new observations and evidence. |
| Backtest results returned | Update the source Alpha Idea note with results interpretation. Do NOT write code — interpret results only. |
| Paper re-read with new insight | Append to Paper Note under "Additional Notes" heading. |
| Assumption invalidated | Update Assumptions section. Mark invalidated assumptions with `~~strikethrough~~`. Add new assumptions. |

### 3.3 When to Reject an Idea (Move to `11_Rejected_Deprecated/`)

An idea should be rejected when:
- Backtest shows no statistically significant edge
- Economic mechanism is disproven
- Data required is unavailable or prohibitively expensive
- Implementation is infeasible at current scale
- Idea is a near-duplicate of an already-rejected idea
- Assumptions are violated by current market structure

**Process:**
1. Create a Rejected Idea Note in `11_Rejected_Deprecated/`
2. Link back to the original Alpha Idea note
3. Update the original Alpha Idea note's status to `rejected` and add a link to the Rejected Idea Note
4. Document **why** it was rejected and what was learned
5. List similar ideas that should be checked against this rejection
6. **Never delete** the original note — it stays in `02_Alpha_Ideas/` with status `rejected`

### 3.4 When to Create a Programmer Handoff

A programmer handoff is created when:
- Alpha idea status is `ready_for_backtest` or `ready_for_programmer`
- Signal logic is specified in plain English
- Data requirements are documented
- Failure modes are identified
- Backtest scope is defined
- Assumptions are documented
- Risk factors are cataloged

**Process:**
1. Verify all prerequisites are met
2. Create a Programmer Handoff Note in `09_Programmer_Handoffs/`
3. Link to source Alpha Idea, Strategy Hypothesis, Backtest Request, and Risk Notes
4. Update the Alpha Idea status to `waiting_for_programmer`
5. Include explicit "What NOT to implement" section
6. Include acceptance and rejection criteria

### 3.5 File Naming Conventions

```
Alpha Ideas:       [market]_[short_descriptive_slug].md
                   Example: crypto_funding_rate_carry_crowding.md
                   Example: commodities_gold_term_structure_regime.md

Strategy Hypotheses: [parent_alpha_slug]_hypothesis_[descriptor].md
                   Example: crypto_funding_rate_carry_crowding_hypothesis_dynamic_scaling.md

Paper Notes:       paper_[first_author_lastname]_[year]_[short_topic].md
                   Example: paper_he_2022_perpetual_futures_fundamentals.md

Market Regimes:    regime_[YYYY-MM-DD]_[market]_[regime_type].md
                   Example: regime_2026-05-13_crypto_high_vol_correlation_breakdown.md

Backtest Requests:  bt_request_[alpha_slug].md
                   Example: bt_request_crypto_funding_rate_carry_crowding.md

Programmer Handoffs: handoff_[alpha_slug].md
                   Example: handoff_crypto_funding_rate_carry_crowding.md

Research Reviews:  review_[YYYY-MM-DD].md
                   Example: review_2026-05-13.md

Rejected Ideas:    rejected_[original_alpha_slug].md
                   Example: rejected_crypto_oi_momentum_reversal.md
```

### 3.6 How to Assign Statuses

Statuses follow the Alpha Idea Lifecycle (see Section 5). The status is always in the YAML frontmatter:

```yaml
status: idea | researching | needs_data_check | ready_for_backtest | waiting_for_programmer | in_backtest | validated | rejected | deprecated
```

### 3.7 How to Add Tags

Tags are always in the YAML frontmatter `tags` list. Use hierarchical tags where Obsidian supports them:

```yaml
tags:
  - alpha_idea
  - crypto
  - mean_reversion
  - funding_rate
  - high_priority
```

Standard tag taxonomy:
- **Note type:** `alpha_idea`, `strategy_hypothesis`, `paper_note`, `market_regime`, `risk_failure_mode`, `backtest_request`, `programmer_handoff`, `research_review`, `rejected_idea`, `concept`, `data_source`
- **Market:** `crypto`, `commodities`, `cross_market`
- **Asset:** `btc`, `eth`, `altcoins`, `gold`, `silver`, `crude_oil`
- **Concept:** `mean_reversion`, `momentum`, `carry`, `volatility`, `liquidity`, `market_microstructure`, `funding_rate`, `open_interest`, `term_structure`, `flow`, `sentiment`, `options`, `macro`
- **Priority:** `high_priority`, `medium_priority`, `low_priority`
- **Confidence:** `speculative`, `hypothesized`, `backed_by_literature`, `backtested`, `validated`

### 3.8 How to Create Backlinks

Backlinks use Obsidian's `[[wikilink]]` syntax. The Research Agent should create backlinks:

1. **In the `concepts` YAML field** — link to concept notes in `01_Concepts/`
2. **In the `related_ideas` YAML field** — link to related alpha ideas
3. **In the note body** — inline links to related notes, concepts, papers, risk notes
4. **In the `source_papers` YAML field** — link to paper notes
5. **In the `parent_alpha` field** — link upstream (hypothesis → alpha idea; programmer handoff → alpha idea)

Example:
```markdown
## Related Concepts
- [[Mean Reversion]] — core mechanism
- [[Funding Rate]] — signal input
- [[Carry Trade]] — related strategy family
- [[Crowding]] — primary failure mode risk
```

### 3.9 How to Avoid Duplicate Alpha Ideas

Before creating a new Alpha Idea note, the Research Agent must:

1. **Search** `02_Alpha_Ideas/` for similar concept names and keywords
2. **Search** `11_Rejected_Deprecated/` for rejected ideas with similar mechanisms
3. **Check** the `related_ideas` links in existing notes
4. **Compare** the economic mechanism, not just the asset or market
5. If a similar idea exists:
   - **If active:** Add a comment or refinement to the existing note instead of creating a duplicate
   - **If rejected:** Review the rejection reason. If conditions have changed, create a new note with a `revisited_from` link to the rejected idea
   - **If deprecated:** Check if the deprecation reason still applies

### 3.10 How to Preserve Research History

- **Never delete** notes. Status changes are recorded in YAML frontmatter.
- **Rejected ideas** are moved to `11_Rejected_Deprecated/` but the original note persists.
- **Deprecated ideas** stay in `11_Rejected_Deprecated/` with deprecation reasons.
- **Research Reviews** serve as timestamped snapshots of the research state.
- **Updated dates** in YAML frontmatter track when notes were last modified.
- **`RESEARCH_LOG.md`** in the project tracks session-level activity.

### 3.11 How to Prevent Writing Implementation Code

The Research Agent must follow these rules when writing any Obsidian note:

1. **Signal logic must be in plain English** — no Python, no Pine Script, no code of any language
2. **"Signal Sketch" sections** use structural descriptions: "compute the z-score of X over N periods, enter long when z < -2, exit when z crosses above 0"
3. **No executable pseudocode** — structural pseudocode is acceptable only if it cannot be copy-pasted and run
4. **Backtest requests** specify what to test, not how to code it
5. **Programmer handoffs** describe logic structurally, not algorithmically
6. **Data sections** list datasets and fields, not API calls or database queries
7. If tempted to write code, the Research Agent should instead write: "The Programmer Agent should implement [description of logic] using [suggested approach]."

---

## 4. Research Agent Retrieval Workflow

### 4.1 Retrieval Triggers

The Research Agent retrieves context from Obsidian before:
- Proposing a new alpha idea
- Refining an existing alpha idea
- Writing a strategy hypothesis
- Preparing a backtest request
- Preparing a programmer handoff
- Evaluating whether an idea is novel
- Conducting a research review

### 4.2 Retrieval Priority

When the Research Agent needs context, it searches in this priority order:

1. **`02_Alpha_Ideas/`** — Check for similar existing ideas (highest priority — avoid duplicates)
2. **`11_Rejected_Deprecated/`** — Check for rejected/deprecated ideas with similar mechanisms
3. **`01_Concepts/`** — Retrieve relevant concept notes for the mechanism
4. **`03_Strategy_Hypotheses/`** — Check for related hypotheses
5. **`05_Paper_Notes/`** — Retrieve relevant paper summaries
6. **`07_Risk_Failure_Modes/`** — Retrieve relevant failure mode documentation
7. **`04_Market_Regimes/`** — Check current and historical regime context
8. **`10_Research_Reviews/`** — Review recent research priorities and dead ends

### 4.3 Search Strategy

The Research Agent uses multiple search methods:

1. **Tag search** — Filter by YAML tags (e.g., all notes tagged `#mean_reversion` and `#crypto`)
2. **Backlink traversal** — Follow `[[wikilinks]]` from concept notes to alpha ideas to paper notes
3. **Keyword grep** — Search note bodies for specific terms (e.g., "funding rate carry", "open interest divergence")
4. **Status filter** — Filter by `status` in YAML frontmatter (e.g., only `validated` or `in_backtest` ideas)
5. **Date filter** — Filter by `created` or `updated` date (e.g., ideas from the last 6 months)
6. **Folder scope** — Limit search to specific folders (e.g., only `02_Alpha_Ideas/` and `11_Rejected_Deprecated/`)

### 4.4 How to Use Tags for Retrieval

Tags are the primary retrieval mechanism. The Research Agent should:

1. **Start with concept tags** — For a mean reversion idea, search `#mean_reversion`
2. **Intersect with market tags** — Narrow by `#crypto` or `#commodities`
3. **Filter by status** — Only notes with `status: validated` or `status: in_backtest` may have performance data
4. **Exclude rejected** — Exclude `#rejected_idea` unless checking for prior art

### 4.5 How to Use Backlinks for Retrieval

Backlinks create a navigable knowledge graph:

1. **Start at a Concept note** (e.g., `[[Mean Reversion]]`) — see all alpha ideas that use mean reversion
2. **Start at a Paper note** — see all alpha ideas inspired by that paper
3. **Start at a Risk note** (e.g., `[[Overfitting]]`) — see all ideas susceptible to that risk
4. **Start at a Market Regime note** — see all alpha ideas relevant to that regime

### 4.6 How to Handle Outdated Notes

- **Market Regime notes older than 6 months** — Flag as potentially outdated. Compare to current market conditions.
- **Alpha Ideas with `updated` date > 3 months ago and status still `idea` or `researching`** — Stale. Either progress or deprecate.
- **Paper notes on fast-moving topics (crypto)** — Flag if > 2 years old without recent corroboration.
- **Data Source notes** — Check if the vendor/data is still available before relying on them.

### 4.7 How to Rank Relevant Notes

When multiple notes match a search, rank them by:

1. **Concept match quality** — Does the mechanism align? (highest weight)
2. **Market match** — Same market > cross-market > different market
3. **Recency** — Newer notes > older notes
4. **Status** — Validated > in backtest > researching > rejected
5. **Priority** — High priority ideas > low priority ideas
6. **Link density** — Notes with more backlinks to relevant concepts are likely more important

### 4.8 How to Detect Repeated Ideas

Before proposing a new alpha idea, the Research Agent runs a "duplicate check":

1. Search `02_Alpha_Ideas/` for notes with the same concept tags
2. Search `11_Rejected_Deprecated/` for rejected ideas with the same mechanism
3. Check if the new idea's **economic mechanism** matches an existing idea's mechanism
4. If the mechanism is the same but the market/asset is different, it's a **variant**, not a duplicate — link to the original
5. If the mechanism AND market/asset are the same, it's a **duplicate** — add to the existing note, don't create a new one
6. If the mechanism is the same but was rejected, and conditions have changed, it's a **revisit** — create a new note with `revisited_from: [[rejected_idea]]`

### 4.9 How to Distinguish Old Assumptions from Current Market Conditions

- Assumptions are documented in Alpha Idea notes under the `## Assumptions` section
- When retrieving an old idea, the Research Agent evaluates each assumption against current market conditions
- If an assumption is invalidated, the idea's status should be downgraded or the idea deprecated
- Market Regime notes provide the "current conditions" reference point
- The Research Agent should ask: "Would this assumption hold in the current regime documented in [[relevant regime note]]?"

### 4.10 How to Surface Uncertainty

The Research Agent must be explicit about uncertainty:

- **`confidence` field in YAML** — `speculative | hypothesized | backed_by_literature | backtested | validated`
- **"What Would Disprove This" section** — Every alpha idea must include falsification criteria
- **"Open Questions" section** — Document what is unknown
- **"Assumptions" section** — Document what is assumed but unverified
- **Risk/Failure Mode links** — Link to relevant failure mode notes

---

## 5. Alpha Idea Lifecycle

### 5.1 Status Definitions

| Status | Meaning | Owner of Next Step | When to Advance |
|--------|---------|-------------------|-----------------|
| `idea` | Raw idea captured. Not yet researched. | Research Agent | Initial research begins. |
| `researching` | Active research in progress. Papers being read, mechanism being evaluated. | Research Agent | Mechanism is understood, data availability checked, hypothesis formulated. |
| `needs_data_check` | Hypothesis formed but data availability unverified. | Research Agent | Data sources confirmed and documented. |
| `ready_for_backtest` | Signal logic specified, data requirements documented, failure modes identified. Ready for backtest specification. | Research Agent | Backtest Request written and handed off. |
| `waiting_for_programmer` | Handoff document created. Waiting for Programmer Agent to implement backtest. | Programmer Agent | Programmer Agent picks up the handoff. |
| `in_backtest` | Programmer Agent is implementing the backtest. | Programmer Agent | Backtest completes, results returned to Research Agent. |
| `validated` | Backtest shows promising results. Alpha is worth further investigation (paper trading, deeper robustness testing). | Research Agent | Further research or paper trading. |
| `rejected` | Alpha did not pass backtest, assumptions invalidated, or mechanism disproven. Preserved for institutional memory. | No one (archived) | Only if market conditions change substantially (→ create a `revisited_from` note). |
| `deprecated` | Alpha was once valid but no longer works. Edge has decayed or regime has shifted permanently. Different from rejected: this used to work. | No one (archived) | Only if regime reverts (unlikely). |

### 5.2 Lifecycle Diagram (Text)

```
idea
  │
  ▼
researching ──────► rejected (mechanism disproven during research)
  │
  ▼
needs_data_check ─► rejected (data unavailable or prohibitively expensive)
  │
  ▼
ready_for_backtest
  │
  ▼
waiting_for_programmer
  │
  ▼
in_backtest ──────► rejected (backtest shows no edge)
  │
  ▼
validated ────────► deprecated (edge decays over time)
```

### 5.3 Ownership Boundaries

- **Research Agent owns:** `idea` → `researching` → `needs_data_check` → `ready_for_backtest` → `waiting_for_programmer`
- **Programmer Agent owns:** `in_backtest`
- **Research Agent owns (after backtest):** `validated`, `rejected`, `deprecated` (interprets results, classifies outcome)

### 5.4 What Must Be Included Before Handoff to Programmer

Before setting status to `waiting_for_programmer`, the following must be complete:

1. Alpha Idea note with all sections filled
2. Strategy Hypothesis note (if applicable) with plain-English signal logic
3. Backtest Request note with full specification
4. Programmer Handoff note with all sections filled
5. Links to relevant Paper Notes, Concept Notes, Risk Notes, Data Source Notes
6. All assumptions documented
7. All failure modes identified and severity-ranked
8. Acceptance and rejection criteria specified
9. "What NOT to implement" section filled
10. All related notes cross-linked

---

## 6. Programmer Handoff Format

### 6.1 Handoff Interface

The handoff from Research Agent to Quant Trading Programmer Agent includes:

1. **Programmer Handoff Note** in `09_Programmer_Handoffs/` (primary document)
2. **Linked Alpha Idea Note** (background and mechanism)
3. **Linked Strategy Hypothesis Note** (detailed signal logic)
4. **Linked Backtest Request Note** (test specification)
5. **Linked Data Source Notes** (data access documentation)
6. **Linked Risk/Failure Mode Notes** (known risks)

### 6.2 Required Content Checklist

The handoff document must include:

- [x] Alpha idea name (descriptive, unique)
- [x] Research summary (mechanism, why edge exists)
- [x] Market / asset universe (specific assets, venues)
- [x] Timeframe (intraday, daily, weekly)
- [x] Signal hypothesis (falsifiable statement)
- [x] Candidate features (plain English list)
- [x] Entry logic (plain English, structural)
- [x] Exit logic (plain English, structural)
- [x] Risk considerations (linked to Risk Notes)
- [x] Transaction cost concerns (documented assumptions)
- [x] Required data (specific datasets, fields, frequency, vendors)
- [x] Suggested backtest scope (in-sample, out-of-sample, benchmark)
- [x] Expected edge (qualitative only — no performance claims)
- [x] Failure modes (cataloged, severity-ranked)
- [x] Assumptions (explicitly listed)
- [x] What needs to be tested (specific list)
- [x] What should NOT be implemented (exclusion list)
- [x] Open research questions (for future investigation)
- [x] Acceptance criteria (what "good" looks like)
- [x] Rejection criteria (what "bad" looks like)

### 6.3 What the Handoff Must NOT Include

- Python code
- Pine Script
- SQL queries
- API calls
- Broker connection logic
- Deployment scripts
- Production trading instructions
- Performance claims ("this will make 20% annually")
- Financial advice or investment recommendations

### 6.4 Pseudocode Policy

Pseudocode may be included **only** if:
- It is high-level and non-executable
- It uses plain English mixed with structural notation
- It cannot be copy-pasted into a Python file and run
- It describes **what** to compute, not **how** to compute it

**Acceptable:**
```
For each asset in universe:
  Compute rolling z-score of funding rate over 30 days
  If z-score < -2: enter long
  If z-score > +2: enter short
  Exit when z-score crosses 0
```

**Not acceptable:**
```python
def compute_signal(df, window=30):
    df['zscore'] = (df['funding_rate'] - df['funding_rate'].rolling(window).mean()) / df['funding_rate'].rolling(window).std()
    df['signal'] = np.where(df['zscore'] < -2, 1, np.where(df['zscore'] > 2, -1, 0))
    return df
```

---

## 7. Agent Policy

### 7.1 Core Operating Policy

The Quant Research Agent operates under the following strict policy:

#### 7.1.1 Code Prohibition
- **The Research Agent must not write implementation code.** This includes but is not limited to: Python, R, MATLAB, C++, Rust, Pine Script, SQL queries, API calls, or any executable code.
- Signal logic must be expressed in plain English or high-level structural pseudocode only.
- If the Research Agent finds itself writing syntax that could be executed, it must stop and rewrite in plain English.

#### 7.1.2 Trading Prohibition
- **The Research Agent must not execute trades or generate live trading signals.**
- **The Research Agent must not connect to broker APIs or exchange APIs.**
- **The Research Agent must not manage positions, orders, or portfolios.**

#### 7.1.3 Performance Claims Prohibition
- **The Research Agent must not claim an alpha is profitable before backtesting.**
- All performance expectations must be qualified as "hypothesized," "expected," or "projected" — never "will."
- The Research Agent must distinguish clearly between: hypothesis (untested), backtest result (historical simulation), and live result (real trading).

#### 7.1.4 Documentation Requirements
- **The Research Agent must document all assumptions** in every alpha idea note.
- **The Research Agent must document expected edge and failure modes** for every alpha idea.
- **The Research Agent must include falsification criteria** ("What Would Disprove This") in every alpha idea.
- **The Research Agent must document uncertainty** — use the `confidence` field and "Open Questions" section.

#### 7.1.5 Obsidian Discipline
- **The Research Agent must check existing Obsidian notes before proposing similar ideas.** Run the duplicate detection workflow (Section 4.8) before creating any new Alpha Idea note.
- **The Research Agent must preserve rejected ideas** — move to `11_Rejected_Deprecated/`, never delete.
- **The Research Agent must not treat Obsidian as a live trading source of truth.** Obsidian stores research artifacts, not production trading state.

#### 7.1.6 Handoff Responsibility
- **The Research Agent must hand off ready ideas to the Quant Trading Programmer Agent** via the formal Programmer Handoff format (Section 6).
- **The Research Agent must not implement backtests** — it specifies them; the Programmer Agent implements them.
- **The Research Agent interprets backtest results** returned by the Programmer Agent but does not run backtests itself.

#### 7.1.7 Source Integrity
- **Every source citation must include a full, working URL or DOI.**
- **Every source must be verified before inclusion** — the paper must exist, the URL must resolve.
- **Never cite by name alone** — no "BIS.org", no "SSRN:12345" without the full URL.

#### 7.1.8 Research Integrity
- **The Research Agent must not cherry-pick evidence** to support a preferred hypothesis.
- **The Research Agent must report negative results and dead ends** in research reviews.
- **The Research Agent must update notes when assumptions are invalidated** rather than letting stale information persist.

### 7.2 Policy Enforcement

These policies are enforced by:
1. **The CLAUDE.md project instructions** (system-level)
2. **The quant-alpha-researcher agent definition** (agent-level)
3. **The Obsidian templates** (note-level — they don't have fields for code)
4. **The Programmer Handoff format** (interface-level — specifies "what NOT to implement")

### 7.3 Policy for Handling Edge Cases

| Situation | Policy |
|-----------|--------|
| Research Agent discovers a coding bug in the backtest (reported by Programmer Agent) | Document the bug in the Alpha Idea note. Do NOT fix the code. Request the Programmer Agent to fix it. |
| Research Agent finds a new data source | Document in `06_Data_Source_Notes/`. Link to relevant Alpha Ideas. Do NOT write data fetching code. |
| Research Agent wants to visualize a concept | Describe the visualization in plain English. The Programmer Agent or a separate visualization tool creates it. |
| User asks Research Agent to "just write a quick backtest" | Refuse. Explain the boundary. Offer to create a Backtest Request for the Programmer Agent instead. |
| User asks Research Agent to predict market direction | Refuse. The Research Agent documents hypotheses, not predictions. Direct the user to the Alpha Idea library for research context. |
| An alpha idea was rejected but market conditions have changed | Create a new Alpha Idea note with `revisited_from: [[rejected_idea]]`. Document what changed. Do NOT modify the rejected note. |

---

## 8. Recommended Next Steps

### Phase 1: Vault Creation (immediate)
1. Create the Obsidian vault directory structure on disk
2. Write all 9 templates to `99_Templates/`
3. Create `Dashboard.md` as the Map of Content
4. Create initial Concept notes in `01_Concepts/` (mean reversion, momentum, carry, volatility, etc.)

### Phase 2: Migration (short-term)
1. Migrate existing `alpha_idea/01_crypto_funding_rate_carry.md` into the Obsidian format as an Alpha Idea note + Programmer Handoff note
2. Port existing paper notes from `SOURCE_TRACKER.md` into individual Paper Notes
3. Port backlog items from `ALPHA_BACKLOG.md` into Alpha Idea notes with status `idea`

### Phase 3: Integration (medium-term)
1. Update `CLAUDE.md` to reference the Obsidian vault as the primary research knowledge base
2. Update the quant-alpha-researcher agent definition to include Obsidian read/write workflows
3. Define the interface contract between Research Agent and Programmer Agent more formally
4. Create a `12_Agent_Prompts/research_agent_system_prompt.md` that encodes the full agent policy

### Phase 4: Programmer Agent (future)
1. Define the Quant Trading Programmer Agent
2. Create the Programmer Agent's Obsidian read workflow (read handoffs, write results)
3. Close the loop: Research Agent → Handoff → Programmer Agent → Backtest Results → Research Agent interprets

---

*This design was produced by the Quant Alpha Researcher Agent.*
*Status: Design complete. Awaiting approval to begin Phase 1 implementation.*
