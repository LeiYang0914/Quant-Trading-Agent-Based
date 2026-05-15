# Research Agent Skills — Master Index

Ten modular skills that define the Research Agent's complete workflow. Each skill is self-contained and invoked in a specific sequence.

## Skill Invocation Order

Every research session follows this sequence:

```
1. domain_queue_management_skill   → Choose domain and next idea
2. source_discovery_skill          → Find and verify sources
3. paper_analysis_skill            → Extract methodology from papers (when papers used)
4. crypto_market_structure_skill   → Apply crypto market microstructure (crypto domain)
   OR
   commodities_market_structure_skill → Apply commodity futures microstructure (commodities domain)
5. alpha_discovery_skill           → Build the alpha idea from evidence
6. memo_writing_skill              → Write the research memo
7. research_quality_control_skill  → Run quality checks
8. handoff_preparation_skill       → Prepare review/programmer handoff (if eligible)
9. research_memory_update_skill    → Update all memory files
```

## Skill Index

### 1. Domain Queue Management
**File:** `domain_queue_management_skill.md`
**When:** Start of every session
**Purpose:** Declare session domain (crypto/commodities/cross_market), select the next alpha idea from the backlog, prevent domain mixing.
**Inputs:** `memory/ALPHA_BACKLOG.md`, `memory/PROJECT_STATE.md`
**Outputs:** Session domain declaration, selected alpha ID
**Updates:** Nothing directly — sets session direction

### 2. Source Discovery
**File:** `source_discovery_skill.md`
**When:** After domain/idea selection, before any memo writing
**Purpose:** Search Tier 1/2/3 sources, verify URLs resolve, assign source IDs, reject weak sources.
**Inputs:** Alpha idea, domain context
**Outputs:** Verified source list with structured IDs
**Updates:** `memory/SOURCE_TRACKER.md` (incremental, as sources are verified)

### 3. Paper Analysis
**File:** `paper_analysis_skill.md`
**When:** When academic papers or working papers are among discovered sources
**Purpose:** Extract 14 structured sections from each paper: research question, methodology, data, findings, limitations, applicability assessment.
**Inputs:** Paper URL or DOI
**Outputs:** Paper summary following `templates/paper_summary.md`
**Updates:** Nothing directly — feeds into alpha discovery and memo writing

### 4. Crypto Market Structure
**File:** `crypto_market_structure_skill.md`
**When:** Every crypto-domain session, before writing the alpha discovery note
**Purpose:** Apply crypto market microstructure knowledge: funding rates, open interest, basis, liquidations, exchange-specific rules, altcoin liquidity, maker/taker fees, DEX vs CEX differences.
**Inputs:** Alpha idea, domain = crypto
**Outputs:** Market structure context for the memo
**Updates:** Nothing directly — informs memo sections

### 5. Commodities Market Structure
**File:** `commodities_market_structure_skill.md`
**When:** Every commodities-domain session, before writing the alpha discovery note
**Purpose:** Apply commodity futures microstructure knowledge: term structure, carry, roll yield, inventory data, CFTC COT, seasonality, macro sensitivity, contract specifications.
**Inputs:** Alpha idea, domain = commodities
**Outputs:** Market structure context for the memo
**Updates:** Nothing directly — informs memo sections

### 6. Alpha Discovery
**File:** `alpha_discovery_skill.md`
**When:** After sources are gathered and market structure is understood
**Purpose:** Progress an idea through 11 layers from raw observation to minimum evidence, apply 6 quality filter questions, set status.
**Inputs:** Verified sources, market structure context, paper summaries
**Outputs:** Alpha discovery note in `research/ideas/proposed/{domain}/`
**Updates:** `memory/ALPHA_BACKLOG.md` (idea status)

### 7. Memo Writing
**File:** `memo_writing_skill.md`
**When:** After alpha discovery note is complete and evidence is sufficient
**Purpose:** Write the 19-section research memo in plain English. No code. Separate facts from hypotheses. Document failure modes.
**Inputs:** Alpha discovery note, paper summaries, market structure context
**Outputs:** Research memo in `research/memos/{domain}/`
**Updates:** Nothing directly — feeds into quality control

### 8. Research Quality Control
**File:** `research_quality_control_skill.md`
**When:** After memo draft is complete, before setting `ready_for_review`
**Purpose:** Run 20 checks across 5 categories (bias, risk/cost, logic/evidence, structural, completeness). Each scored PASS/FAIL/NEEDS_MORE_WORK.
**Inputs:** Draft research memo, alpha discovery note, `memory/SOURCE_TRACKER.md`
**Outputs:** Completed QC checklist, fix list if needed
**Updates:** Nothing directly — gates the `ready_for_review` status

### 9. Handoff Preparation
**File:** `handoff_preparation_skill.md`
**When:** After QC passes and memo is ready for review; again after Review Agent approval (for programmer handoff)
**Purpose:** Prepare clean handoffs: Research→Review (alpha discovery note + memo) or Research→Programmer (20-field implementation spec, after approval).
**Inputs:** Approved alpha discovery note, research memo, Review Agent approval (for programmer path)
**Outputs:** Programmer handoff in `handoffs/pending/`
**Updates:** `memory/PROJECT_STATE.md`

### 10. Research Memory Update
**File:** `research_memory_update_skill.md`
**When:** End of every session — always the last skill invoked
**Purpose:** Update all 5 memory files with session results, new sources, status changes, and next-session recommendations.
**Inputs:** Session activity, QC results, domain and alpha ID
**Outputs:** Updated memory files
**Updates:** `memory/PROJECT_STATE.md`, `memory/ALPHA_BACKLOG.md`, `memory/RESEARCH_LOG.md`, `memory/SOURCE_TRACKER.md`, `memory/DECISIONS.md` (conditional)

## What the Research Agent Is Forbidden From Doing

These prohibitions apply regardless of which skill is active:

- **No code:** Never write Python, SQL, Pine Script, Rust, or any executable code in any output
- **No backtests:** Never implement or run backtests
- **No trading:** Never make trading recommendations, set position sizes, or approve risk
- **No self-approval:** Never skip the Review Agent gate — all ideas go through review
- **No domain mixing:** Never mix crypto and commodities in the same memo without `cross_market` labeling
- **No vague citations:** Never write "research suggests" or "studies show" without an exact reference
- **No API connections:** Never connect to broker APIs, exchanges, or data vendor APIs
- **No performance claims:** Never state expected returns, Sharpe ratios, or P&L as fact

## Skill Dependency Graph

```
domain_queue_management
    │
    ▼
source_discovery ──→ paper_analysis (when papers found)
    │                     │
    ▼                     ▼
market_structure ──→ alpha_discovery
(crypto OR              │
 commodities)            ▼
                     memo_writing
                         │
                         ▼
                  research_quality_control
                         │
                         ▼
                  handoff_preparation (if eligible)
                         │
                         ▼
                  research_memory_update
```

## File Summary

| # | Skill File | What It Produces | Memory Files Updated |
|---|-----------|-----------------|---------------------|
| 1 | `domain_queue_management_skill.md` | Session declaration | None |
| 2 | `source_discovery_skill.md` | Verified sources with IDs | SOURCE_TRACKER.md |
| 3 | `paper_analysis_skill.md` | Paper summaries | None |
| 4 | `crypto_market_structure_skill.md` | Market structure context | None |
| 5 | `commodities_market_structure_skill.md` | Market structure context | None |
| 6 | `alpha_discovery_skill.md` | Alpha discovery note | ALPHA_BACKLOG.md |
| 7 | `memo_writing_skill.md` | Research memo | None |
| 8 | `research_quality_control_skill.md` | QC checklist | None |
| 9 | `handoff_preparation_skill.md` | Programmer handoff | PROJECT_STATE.md |
| 10 | `research_memory_update_skill.md` | Session summary | All 5 memory files |
