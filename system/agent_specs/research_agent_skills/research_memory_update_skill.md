# research_memory_update_skill.md

## Purpose

Ensure every research session properly updates the project's persistent memory. This skill defines exactly what to update, how, and when. Consistent memory updates are what make the multi-agent system work across sessions.

## When to Use

At the **end of every research session**, after all research activity is complete. This is always the last skill invoked.

## Files to Update (Mandatory)

### 1. `memory/PROJECT_STATE.md`

Update:
- **Last updated** date
- **Active Research table:** Update status, add new ideas, mark completed
- **Completed Memos table:** Add any newly completed memos
- **Next Priorities:** Re-rank based on current backlog state
- **Recent Changes:** Add one-line entry for this session
- **Blockers:** Update if any new blockers emerged

Format for Recent Changes entry:
```
- YYYY-MM-DD: {session domain}. {one-sentence summary}. {key outputs}.
```

### 2. `memory/ALPHA_BACKLOG.md`

Update for the researched idea:
- **Status:** idea → researching → needs_data_check → ready_for_review
- **References status:** none → partial → sufficient
- **Data status:** unknown → needs_check → available → unavailable
- **Next action:** specific, actionable

If a new idea was added:
- Assign next available alpha ID in the correct domain
- Add to the correct domain section (Crypto, Commodities, Cross-Market)
- Set initial status, priority, references, and data status

### 3. `memory/RESEARCH_LOG.md`

Append a dated session entry at the top (after the header, before the first `---`).

Required format:
```
## YYYY-MM-DD — {Session Title}

**Session type:** {Alpha research / Paper analysis / Backlog grooming / etc.}
**Session domain:** {crypto | commodities | cross_market}

### Activity
- {Key activity 1}
- {Key activity 2}

### Sources Reviewed
| Ref ID | Title | Tier | New? |
|--------|-------|------|------|
| {ID} | {title} | {1/2/3} | {yes/no} |

### Outputs Created
- {file path 1}
- {file path 2}

### Next Session
- **Recommended domain:** {domain}
- **Recommended idea:** {alpha ID}
- **Recommended action:** {action}
```

### 4. `memory/SOURCE_TRACKER.md`

For every new source consulted:
- Add entry with structured Source ID, domain, type, title, authors, year, venue, DOI/arXiv/SSRN, URL, tier, ideas supported, and notes
- Add to the correct domain section (Crypto, Commodities, Cross-Market)
- Update the Source Counts summary table

### 5. `memory/DECISIONS.md` (Conditional)

Only if a significant methodological or architectural decision was made. Not every session requires this.

Format:
```
## YYYY-MM-DD — {Decision Title}

### Decision: {What was decided}
**What:** {Description}
**Why:** {Rationale}
```

## Session Summary Format

At the end of every session, the Research Agent should produce a brief summary:

```
Session: {date}
Domain: {crypto | commodities | cross_market}
Idea: {alpha ID} — {title}
Status: {before} → {after}
Sources added: {count}
Outputs: {file list}
Quality gates: {all pass / issues: ...}
Next: {recommended next action}
```

## How to Update Memory Efficiently

1. Update `memory/SOURCE_TRACKER.md` as soon as each source is verified (during research, not at the end)
2. Draft the RESEARCH_LOG.md entry while the research is fresh
3. Update PROJECT_STATE.md and ALPHA_BACKLOG.md last, when the final status is known
4. Only write to DECISIONS.md if a decision was actually made — do not inflate it

## Inputs

- Session activity (sources found, memos written, ideas created)
- Quality control results
- Domain and alpha ID

## Outputs

- Updated `memory/PROJECT_STATE.md`
- Updated `memory/ALPHA_BACKLOG.md`
- Updated `memory/RESEARCH_LOG.md` (new entry appended)
- Updated `memory/SOURCE_TRACKER.md` (new sources added)
- Updated `memory/DECISIONS.md` (if applicable)

## Anti-Patterns

- Ending a session without updating memory ("I'll do it next time")
- Updating some memory files but not all
- Writing vague RESEARCH_LOG entries ("did some research")
- Forgetting to update the source counts in SOURCE_TRACKER.md
- Leaving the Next Priorities in PROJECT_STATE.md stale
- Not updating the "Last updated" date at the top of PROJECT_STATE.md
