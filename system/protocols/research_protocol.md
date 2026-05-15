# Research Protocol

The detailed research workflow for the Research Agent in the Quant Trading AI System.

## Skill Invocation Sequence

Every research session follows the 9-skill sequence defined in `system/agent_specs/research_agent_skills/README.md`. Each skill is a self-contained module with its own specification file. The steps below map the protocol steps to their corresponding skills.

## Step 1: Domain Queue Management (Skill 1)

Invoke: `domain_queue_management_skill.md`

Choose exactly one domain for the session:
- `crypto`
- `commodities`
- `cross_market`

**Default rule:** Process crypto first. Move to commodities only after crypto priorities are complete or when explicitly requested.

Read `memory/ALPHA_BACKLOG.md`. Find the highest-priority idea in the current session domain.

Priority within a domain is determined by:
1. Status: incomplete ideas before new ideas
2. Priority label: High → Medium → Low
3. Age: older entries first within the same priority

Declare at session start:

```
Session domain: {domain}
Objective: {one sentence}
Idea ID: {DOMAIN-NNN}
Status: {idea | researching | needs_data_check | ready_for_review}
```

## Step 2: Source Discovery (Skill 2)

Invoke: `source_discovery_skill.md`

Use WebSearch and WebFetch. Follow the source quality hierarchy:

| Tier | Sources | Requirement |
|------|---------|-------------|
| Tier 1 | Peer-reviewed journals, conference papers, SSRN, arXiv, NBER, BIS, IMF, Fed, ECB | Preferred |
| Tier 2 | Official exchange docs, CFTC, SEC, EIA, LBMA, World Gold Council | Acceptable |
| Tier 3 | Practitioner research, institutional reports, well-known quant blogs | Supplementary only |

**Reject sources that are:** anonymous tweets, unsourced blogs, marketing pages, SEO articles, forum speculation, AI-generated summaries without source links.

**Minimum bar for a research memo:** at least 2 credible references, at least 1 from Tier 1 or Tier 2 (unless explicitly justified).

For every source consulted, record in `memory/SOURCE_TRACKER.md`:

```
Source ID: {DOMAIN-TYPE-NNN}
Domain: {crypto | commodities | cross_market}
Type: {journal | conference | working_paper | official_doc | data_vendor | practitioner_research}
Title: {full title}
Authors / Organization: {names or org}
Year: {YYYY}
DOI / arXiv / SSRN: {if available}
URL: {full working URL}
Reliability Tier: {1 | 2 | 3}
Ideas Supported: {alpha IDs}
Notes: {why relevant}
```

Source ID format:
- `CRYPTO-PAPER-NNN` — crypto academic paper
- `CRYPTO-OFFICIAL-NNN` — crypto official documentation
- `COMMOD-PAPER-NNN` — commodities academic paper
- `COMMOD-OFFICIAL-NNN` — commodities official documentation
- `CROSS-PAPER-NNN` — cross-market paper

## Step 3: Paper Analysis (Skill 3, When Papers Used)

Invoke: `paper_analysis_skill.md`

Extract 14 structured sections from each paper: research question, methodology, data, findings, limitations, applicability assessment. Write paper summary following `templates/paper_summary.md`.

## Step 4: Market Structure Analysis (Skill 4 or 5)

Invoke: `crypto_market_structure_skill.md` (crypto domain) OR `commodities_market_structure_skill.md` (commodities domain)

Apply domain-specific market microstructure knowledge before writing the alpha discovery note.

## Step 5: Alpha Discovery (Skill 6)

Invoke: `alpha_discovery_skill.md`

Write to `research/ideas/proposed/{domain}/{alpha_id}_{slug}.md` following `templates/alpha_discovery_note.md`.

Progress idea through 11 layers from raw observation to minimum evidence. Apply 6 quality filter questions.

Required fields:
- Alpha ID
- Domain
- Discovery source
- Raw observation
- Hypothesis
- Why this may be an edge
- Market structure mechanism
- Required data
- Suggested signal (plain English)
- Similar known strategies
- What could invalidate it
- Minimum references needed before memo
- Current references
- Status

**Rule:** No alpha discovery note can become a research memo unless it has at least 2 credible references, including at least 1 Tier 1 or Tier 2 source.

## Step 6: Memo Writing (Skill 7)

Invoke: `memo_writing_skill.md`

Write to `research/memos/{domain}/{alpha_id}_{slug}.md` following `templates/research_memo.md`.

All 19 sections required. Plain English only. No code. Separate facts from hypotheses. Document failure modes with severity, trigger, effect, and mitigation.

**If evidence is insufficient:** flag the idea as `needs_more_sources` and move to the next idea. Do not write a memo on a weak foundation.

## Step 7: Research Quality Control (Skill 8)

Invoke: `research_quality_control_skill.md`

Run 20 checks across 5 categories (bias, risk/cost, logic/evidence, structural, completeness). Each scored PASS/FAIL/NEEDS_MORE_WORK. All must pass before `ready_for_review`.

## Step 8: Handoff Preparation (Skill 9, If Eligible)

Invoke: `handoff_preparation_skill.md`

**If QC passes:** Prepare Research→Review handoff (alpha discovery note + memo).

**After Review Agent approval:** Prepare Research→Programmer handoff in `handoffs/pending/` (20-field implementation spec, no code).

## Step 9: Research Memory Update (Skill 10)

Invoke: `research_memory_update_skill.md` — always the last skill.

Update all 5 memory files:
- `memory/PROJECT_STATE.md` — current status, active research, next priorities
- `memory/ALPHA_BACKLOG.md` — update idea statuses, references status, data status
- `memory/RESEARCH_LOG.md` — append dated session entry
- `memory/SOURCE_TRACKER.md` — new sources with structured IDs
- `memory/DECISIONS.md` — if important methodological decisions were made

## Domain-Specific Data Sources

### Crypto (preferred)
- Exchange APIs: Binance, Bybit, OKX, Deribit
- Aggregators: CoinGlass, Coinalyze, Kaiko, Tardis.dev
- On-chain: Glassnode, CryptoQuant, Dune Analytics
- Academic: SSRN crypto papers, arXiv q-fin, BIS working papers

### Commodities (preferred)
- Official: CFTC COT reports, EIA data, LBMA, World Gold Council
- Exchange: CME Group, ICE, LME
- Data: Bloomberg, Refinitiv, Quandl, FRED (St. Louis Fed)
- Academic: SSRN commodities papers, NBER, BIS

## Session Discipline Rules

1. **One domain per session** — do not jump between crypto and commodities.
2. **Crypto first by default** — process crypto backlog before commodities.
3. **No memo without sources** — if references are insufficient, flag the idea; do not write a weak memo.
4. **No vague citations** — never write "research suggests" without an exact reference.
5. **No code** — plain English only in all research output.
6. **No self-approval** — all ideas go through the Review Agent gate.
