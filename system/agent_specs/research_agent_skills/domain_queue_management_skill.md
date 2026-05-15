# domain_queue_management_skill.md

## Purpose

Prevent the Research Agent from jumping between crypto and commodities research. Enforce the default domain priority order and ensure every session has a declared domain.

## When to Use

At the **start of every research session**, before any research activity begins. This is always the first skill invoked.

## Default Priority Order

1. **crypto** — active by default, always processed first
2. **commodities** — only after crypto priorities are complete or when explicitly requested
3. **cross_market** — only when explicitly requested

## When Commodities Research Is Allowed

Commodities research may begin only when ONE of these conditions is met:
- The user explicitly asks for commodities research
- All crypto ideas in `memory/ALPHA_BACKLOG.md` with `High` and `Medium` priority are complete
- `memory/PROJECT_STATE.md` explicitly sets the default domain to `commodities`

## When Cross-Market Research Is Allowed

Cross-market research may begin only when ONE of these conditions is met:
- The user explicitly asks for cross-market research
- A clear, well-defined cross-domain link is identified during crypto or commodities research
- A paper explicitly tests a hypothesis that spans both domains

## Session Domain Declaration

At the start of every session, the Research Agent must declare:

```
Session domain: {crypto | commodities | cross_market}
Objective: {one sentence}
Idea ID: {CRYPTO-NNN | COMMOD-NNN | CROSS-NNN}
Status before session: {status}
```

## How to Choose the Next Idea

1. Read `memory/PROJECT_STATE.md` — confirm the default domain
2. Read `memory/ALPHA_BACKLOG.md` — find ideas in the current domain
3. Within the domain, prioritize:
   - **Status:** incomplete > not started
   - **Priority label:** High > Medium > Low
   - **Age:** older entries first within same priority
4. If no ideas exist in the current domain and domain is crypto, check for any incomplete crypto ideas
5. If all crypto ideas are complete, check PROJECT_STATE.md before switching to commodities

## How to Avoid Mixing Domains

- One domain per session. Never research crypto and commodities in the same session unless the session domain is `cross_market`.
- A cross_market session must explicitly acknowledge both domains and explain why they are linked.
- If a crypto idea accidentally mentions commodity concepts, flag it — it may need to be split or reclassified as cross_market.

## How to Update the Backlog by Domain

After each session, update `memory/ALPHA_BACKLOG.md`:
- Update the status and next action for the researched idea
- Keep ideas in their correct domain section (Crypto, Commodities, Cross-Market)
- Assign the correct alpha ID prefix (CRYPTO-, COMMOD-, CROSS-)

## Inputs

- `memory/PROJECT_STATE.md` — default domain
- `memory/ALPHA_BACKLOG.md` — idea queue (domain-grouped)

## Outputs

- Session domain declaration (written or stated at session start)
- Updated session objective

## Anti-Patterns (Do Not Do)

- Starting a session without declaring the domain
- Researching crypto in the morning and commodities in the afternoon of the same session
- Treating "crypto gold" or "tokenized gold" as commodities — they are crypto unless proven otherwise
- Mixing CFTC COT analysis into a crypto funding rate memo
- Switching to commodities because "crypto research is hard" — flag the difficulty instead
