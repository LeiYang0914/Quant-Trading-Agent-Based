# paper_analysis_skill.md

## Purpose

Help the Research Agent read and analyze academic papers, official reports, and practitioner research like a disciplined institutional quant researcher. Every paper used as evidence must be understood, not just cited.

## When to Use

Whenever the Research Agent encounters a paper, working paper, official report, or substantive practitioner piece that may support an alpha idea. Apply before using the paper as a source in any discovery note or memo.

## Core Rule

**Do not treat a paper as evidence unless you understand its data, methodology, and limitations.**

## What to Extract from Every Paper

### 1. Research Question
What question does the paper try to answer? State in one sentence.

### 2. Hypothesis
What is the main testable hypothesis? Is it directional (X causes Y) or associational (X is correlated with Y)?

### 3. Market Studied
Which market? Crypto, equities, FX, commodities, fixed income? What specific assets?

### 4. Instruments Studied
What instruments? Spot, futures, perpetuals, options? What exchanges or venues?

### 5. Dataset
- Data source(s)
- Sample period (start date, end date)
- Frequency (tick, minute, hourly, daily, weekly)
- Number of assets or observations
- Survivorship bias handling

### 6. Methodology
- Empirical method (regression, portfolio sorts, event study, ML, GMM, etc.)
- Key independent and dependent variables
- Control variables
- Standard error treatment (Newey-West, clustered, bootstrap)

### 7. Assumptions
- What assumptions does the methodology rely on?
- Are these assumptions reasonable for the market studied?

### 8. Results
- Main finding(s) — economic magnitude, not just statistical significance
- Sharpe ratio, t-stat, R-squared, or other key metrics
- Robustness to alternative specifications

### 9. Robustness Checks
- Subperiod analysis
- Out-of-sample tests
- Alternative variable definitions
- Placebo tests

### 10. Limitations
- Stated limitations (authors' own caveats)
- Unstated limitations (what you notice that the authors did not address)
- Lookahead bias risk
- Data quality concerns

### 11. Possible Biases
- Selection bias
- Survivorship bias
- Data snooping / p-hacking risk
- Publication bias (is this a "successful" result?)
- Sample period bias (bull market only? post-2020 only?)

### 12. Relevance Assessment
- **Relevance to crypto:** How does this apply to crypto markets? What would need to be adapted? What would NOT translate?
- **Relevance to commodities:** How does this apply to commodity markets? What structural differences matter?
- **Domain classification:** Is the paper crypto, commodities, cross_market, or outside scope?

### 13. Alpha Ideas Derived
- What specific alpha idea(s) does this paper suggest?
- Is the idea original (direct from paper), adapted (modified for different market), or replicated (same idea, different market)?
- Assign tentative alpha ID(s)

### 14. Cross-Validation
- Do other papers confirm or contradict these findings?
- Has this result been replicated?

## How to Decide Whether the Paper Is Strong Enough to Support an Alpha

The paper is **strong evidence** if ALL of:
- Methodology is clearly described and appropriate
- Sample period is long enough and covers different regimes
- Out-of-sample or subperiod results are reported
- Transaction costs are discussed (or the result is large enough to survive them)
- Limitations are acknowledged
- Data sources are documented and accessible

The paper is **weak evidence** (flag it) if ANY of:
- Sample period is short or single-regime (e.g., 2020-2021 only)
- No out-of-sample or robustness testing
- Economic magnitude is small relative to transaction costs
- Methodology has obvious lookahead or survivorship bias
- Data is proprietary and unreproducible
- Only one paper reports this finding with no replication

## Paper Summary Output

Write a paper summary following `templates/paper_summary.md` and store it:
- In `knowledge/Quant-Research-KB/05_Paper_Notes/` (Obsidian, linked)
- Optionally save the PDF or link in `research/papers/`

## Inputs

- Paper (via WebFetch, direct download, or prior knowledge)
- Domain context (crypto, commodities, cross_market)

## Outputs

- Paper summary in `templates/paper_summary.md` format
- Entry in `knowledge/Quant-Research-KB/05_Paper_Notes/`
- Source recorded in `memory/SOURCE_TRACKER.md`
- Alpha ideas derived (if any) proposed to the alpha discovery workflow

## Anti-Patterns

- Citing a paper based on its abstract only
- Accepting a paper's conclusions without checking methodology
- Applying an equity-market paper to crypto without adaptation analysis
- Ignoring a paper's stated limitations
- Treating an arXiv preprint (not yet peer-reviewed) as equivalent to a journal publication
