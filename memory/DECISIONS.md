# Decisions Log

Important project decisions and their rationale.

---

## 2026-06-14 — API Key Security: Env-Var-Only Policy for All Credentials

### Decision: All API keys must be environment-variable-only — no hardcoded fallbacks
**What:** All API keys (Glassnode, Anthropic, DeepSeek) MUST be read from environment variables or the gitignored `.env` file. Hardcoded fallback values in source code are prohibited.
**Why:** A Glassnode API key was accidentally hardcoded as a fallback in `glassnode_loader.py` and `glassnode_btc_etf_flows.py` (`os.getenv("GLASSNODE_API_KEY") or "32YB16..."`). The key was committed and pushed to GitHub, making it publicly accessible. The git history required a `filter-branch` scrub and force push to clean. The key is now being rotated on Glassnode.
**Remediation applied:**
1. Removed hardcoded fallback from both files — env var only, with clear ValueError when unset
2. Added key to gitignored `.env` file
3. Set persistent Windows user-level environment variable `GLASSNODE_API_KEY`
4. Scrubbed entire git history via `git filter-branch --tree-filter`
5. Force-pushed cleaned history to GitHub
6. Started Glassnode key rotation (in progress — user must complete at glassnode.com)

---

## 2026-05-20 — CRYPTO-002 Conditional Pass with Five Implementation Conditions

### Decision: CRYPTO-002 (OI-Price Divergence Reversal) passes review with conditions attached
**What:** The Review Agent evaluated CRYPTO-002 and issued a CONDITIONAL PASS -- approved for programmer handoff, but only if five mandatory conditions are satisfied in the backtest.
**Why:** The economic mechanism (OI-price divergence as reversal signal, grounded in Bessembinder & Seguin 1993 and Matsui et al. 2022) is sound, no lookahead bias was found, data exists (with quality caveats), and there is low overlap with existing approved ideas (CRYPTO-001, CRYPTO-003). However, the core concept (four-quadrant framework) is textbook material with low novelty, meaning the edge depends entirely on quantitative operationalization. The five conditions ensure the backtest validates genuine alpha rather than data-mined parameters or spurious patterns.
**Conditions:** (1) Control test: OI-enhanced must outperform pure price reversal benchmark. (2) Data quality filter: OI-volume reconciliation must be operational and filtering rate reported. (3) Parameter sensitivity: performance must be reported across threshold/lookback/decile sweeps. (4) Regime-conditional: performance must be broken out by trending vs. range-bound regimes. (5) Out-of-sample: parameters optimized on 2019-2022, tested on 2023-2025.
**Falsification criterion:** If the OI-enhanced signal does not meaningfully outperform a pure price reversal control (same lookback, same holding period, no OI), the alpha must be rejected -- this is the memo's own Open Question #3.

### Decision: "Conditional pass" as a formal review outcome
**What:** The Review Agent introduced a third review outcome beyond Approved and Rejected: Conditional Pass. This means the idea is approved in principle but the backtest must satisfy specific, testable conditions before the alpha can move to Risk Agent review or paper trading.
**Why:** Not all ideas fit neatly into binary approve/reject. Some alphas have sound mechanisms but unresolved empirical questions that can only be answered by backtesting. Conditional pass allows the idea to move forward while ensuring the empirical tests are actually performed. If conditions are not met, the alpha is rejected regardless of standalone performance. This is stricter than a simple approval because it attaches binding requirements.

---

## 2026-05-15 — Five-Agent System Architecture

### Decision: Restructure from research workspace to five-agent Quant Trading AI System
**What:** The project was refactored from a simple research workspace (single Research Agent + future Programmer Agent) into a five-agent system: Research, Review, Programmer, Data, Risk.
**Why:** A single research agent with a direct-to-programmer pipeline lacks quality gates. The five-agent architecture creates clear separation of concerns: research (discover), review (validate), programming (implement), data (infrastructure), and risk (final gate). Each agent has absolute boundaries — no agent does everything. This prevents scope creep and ensures every alpha idea is independently reviewed before code is written and independently risk-assessed before any capital is put at risk.

### Decision: Two mandatory gates — Review and Risk
**What:** Every alpha idea must pass through two independent gates: the Review Agent (economic rationale, data availability, lookahead bias, overfitting, overlap) and the Risk Agent (drawdown, volatility, correlation, capacity, position sizing, kill switches).
**Why:** Research quality and risk management are distinct concerns. The Review Agent validates that an idea makes sense before anyone writes code. The Risk Agent validates that a strategy is safe before it moves toward paper trading. Neither gate can be bypassed.

### Decision: Clean directory structure with short, simple folder names
**What:** The top-level structure uses simple names: `memory/`, `research/`, `handoffs/`, `knowledge/`, `system/`, `src/`, `configs/`, `tests/`, `reports/`, `paper_trading/`, `templates/`.
**Why:** The old structure (`research_memory/`, `research_memos/`, `handoff_to_programmer/`) was verbose and mixed concerns. The new structure separates research output from project memory, and gives each function a clear, self-explanatory home.

### Decision: All agent specs, workflows, protocols, and architecture docs live under `system/`
**What:** `system/architecture/`, `system/workflows/`, `system/protocols/`, `system/agent_specs/`.
**Why:** Centralizes system-level documentation in one place. Separates agent definitions (`.claude/agents/` — how Claude invokes them) from agent specifications (`system/agent_specs/` — detailed capability and boundary documentation).

---

## 2026-05-17 — LLM Router Production Upgrade

### Decision: Response caching with code/risk task exclusions
**What:** File-based JSON response cache keyed by hash of provider + model + task_type + prompt. CODE_GENERATION, CODE_PLANNING, CODE_REVIEW, DEBUGGING, and RISK_REVIEW are never cached.
**Why:** Cache reduces duplicate API costs for idempotent tasks (summarization, classification, memory updates). Code and risk tasks produce non-deterministic outputs that should not be cached — stale code could contain bugs, stale risk reviews could miss new market conditions.

### Decision: Cache disabled during dry_run mode
**What:** Cache.put() and .get() are bypassed when router is in dry_run mode.
**Why:** Prevents placeholder responses from polluting the cache, which would cause subsequent real calls to return dummy data.

### Decision: Circuit breaker with CLOSED→OPEN→HALF_OPEN→CLOSED state machine
**What:** Per-provider circuit breaker trips after 3 consecutive failures (configurable). After 5-minute cooldown (configurable), allows one probe request in HALF_OPEN state. Success returns to CLOSED; failure re-opens.
**Why:** Prevents cascading failures when a provider is down. Without a circuit breaker, every failed request would retry the down provider, adding latency and consuming rate limit budget.

### Decision: Sliding-window rate limiting per provider
**What:** In-memory sliding-window rate limiter with configurable requests_per_minute per provider. Skipped providers with exhausted windows during routing.
**Why:** Prevents API quota exhaustion. When the limit is hit, the router falls back to the alternative provider rather than failing.

### Decision: `router.ask()` as convenience API for simple cases
**What:** `ask()` accepts a prompt and auto-classifies the task type, complexity, domain, etc. Supports optional overrides for all fields.
**Why:** Reduces boilerplate for common agent requests. Agents can call `router.ask(prompt="Summarize this", agent_name="research-agent")` instead of constructing a full TaskRequest.

### Decision: Graceful provider degradation on missing SDKs
**What:** Both ClaudeProvider and DeepSeekProvider return structured error responses when the SDK is not installed or API key is missing, rather than crashing.
**Why:** The system must remain operational for testing and development without requiring both SDKs to be installed or both API keys to be configured.

---

## 2026-05-17 — LLM Router Architecture

### Decision: Add LLM Router as shared infrastructure beneath all five agents
**What:** A central LLM Router layer (`src/llm/`) that all agents use for LLM calls. Agents never call providers directly.
**Why:** Centralized routing enables consistent cost control, model selection by task type, fallback handling, and audit logging. Without a router, each agent would independently decide which model to use, leading to inconsistent decisions and untracked costs.

### Decision: Claude for complex tasks, DeepSeek for cost-efficient throughput
**What:** Tasks are split: Claude handles system architecture, research reasoning, paper analysis, alpha generation, code planning/generation/review, debugging, high-complexity, and risk-critical decisions. DeepSeek handles summarization, text cleanup, source screening, data grabbing, git summaries, classification, and memory updates.
**Why:** Claude models excel at careful reasoning and code generation. DeepSeek models offer competitive performance at lower cost for simpler, repetitive tasks. Splitting by task type optimizes cost without degrading quality on work that matters.

### Decision: Code generation never falls back Claude→DeepSeek by default
**What:** The router blocks fallback from Claude to DeepSeek for CODE_GENERATION, CODE_PLANNING, CODE_REVIEW, and DEBUGGING task types. Fallback is only allowed if the agent explicitly sets `fallback_allowed_for_code_tasks` in metadata.
**Why:** Code quality is critical — a cheaper model producing subtly incorrect code could introduce bugs into trading strategies. The cost savings are not worth the risk.

### Decision: Risk Agent and Review Agent always route to Claude
**What:** Both gate agents (Review — quality gate, Risk — safety gate) are hard-coded to prefer Claude regardless of task type. No low-cost fallback for their decisions.
**Why:** These agents make high-stakes go/no-go decisions. Review approves ideas for implementation; Risk approves strategies for paper trading. Neither decision should be made by a lower-capability model.

### Decision: Dry run mode as default for testing
**What:** The router defaults to `dry_run=True`. Provider skeletons return placeholder responses. Full routing logic executes, decisions are logged, but no real API calls are made.
**Why:** Enables testing routing logic, fallback behavior, and agent integration without consuming API credits or requiring API keys.

### Decision: API keys via environment variables only
**What:** `ANTHROPIC_API_KEY` and `DEEPSEEK_API_KEY` read from environment. Never stored in config files, never committed to git.
**Why:** Security. Config files are committed; environment variables are not.

### Decision: Provider-specific code isolated in `src/llm/providers/`
**What:** Each provider has its own file implementing `BaseProvider`. Adding a new provider means adding one new file and one entry in `models.yaml`.
**Why:** Extensibility. The router logic is provider-agnostic.

---

## 2026-05-14 — Cross-Sectional vs. Absolute Carry Distinction

### Decision: Cross-sectional funding carry is a carry CAPTURE strategy, not a reversal strategy
**What:** For cross-sectional altcoin funding rate strategies, the alpha direction is to go long (with) high relative funding rate altcoins and short low relative funding rate altcoins -- capturing the persistent carry spread. This is distinguished from absolute (time-series) funding rate strategies where extreme funding predicts reversals (crowding/crash signal).
**Why:** The BIS paper (Schmeling et al. 2023) documents that high absolute funding rates predict crashes for BTC/ETH -- a reversal relationship. However, cross-sectional strategies rank altcoins RELATIVE to each other at the same point in time, which hedges out the market-directional crash risk that affects absolute carry. The carry spread between top and bottom quintile altcoins is driven by structurally persistent forces (retail attention concentration, constrained arbitrage capital) that support a carry capture direction. Fan et al. (2024) empirically validates this direction with Sharpe 0.74 for long high-FR / short low-FR. This distinction is foundational for all future cross-sectional alpha research.

### Decision: Every citation must include a full working URL or DOI
**What:** No source may be cited without a resolvable link. Shorthand references like "BIS.org", "SSRN:12345", "arXiv:2212.06888" are not acceptable — the full URL must be included in the memo and in `memory/SOURCE_TRACKER.md`.
**Why:** Makes every source instantly verifiable by a human reader or another agent. Removes ambiguity about where to find the paper. Prevents dead citations that can't be located later.

---

## 2026-05-13 — Obsidian Integration Decisions

### Decision: Obsidian vault is the Research Agent's long-term memory, separate from project memory files
**What:** The Obsidian vault (`knowledge/Quant-Research-KB/`) stores research knowledge (alpha ideas, paper notes, concepts, etc.) while `memory/` files remain the project coordination layer (state, backlog, log, sources, decisions).
**Why:** Obsidian excels at interlinked knowledge graphs with backlinks and tags. The project memory files are flat coordination artifacts. They serve different purposes and should not be merged.

### Decision: 9-status alpha lifecycle with clear Research/Programmer ownership boundaries
**What:** Ideas flow through: idea → researching → needs_data_check → ready_for_backtest → waiting_for_programmer → in_backtest → validated | rejected | deprecated. Research Agent owns all statuses except `in_backtest` (Programmer Agent) and post-backtest classification (Research Agent). **Note:** This has been superseded by the broader lifecycle in `system/workflows/alpha_lifecycle.md` which adds Review and Risk gates.
**Why:** Prevents ownership ambiguity. The Research Agent never implements; the Programmer Agent never decides what to test.

### Decision: Rejected and deprecated ideas are preserved, never deleted
**What:** Rejected and deprecated alpha ideas move to `research/ideas/rejected/` but the original notes persist with updated status.
**Why:** Institutional memory prevents repeating dead ends. Knowing what failed and why is as valuable as knowing what worked.

### Decision: Signal logic must be plain English; high-level structural pseudocode allowed but must not be executable
**What:** Plain English is the default. Structural pseudocode is acceptable only if it cannot be copy-pasted and run. Python, Pine Script, SQL, and any executable code are prohibited in all Research Agent output.
**Why:** Enforces the boundary between research (what to test) and implementation (how to code it).

### Decision: Templated YAML frontmatter with standardized tags for all Obsidian notes
**What:** Every Obsidian note uses YAML frontmatter with `type`, `status`, `tags`, `created`, `updated`, `concepts`, and type-specific fields.
**Why:** Enables programmatic retrieval by tag, status, and date.

### Decision: Duplicate detection required before creating any new Alpha Idea note
**What:** The Research Agent must search existing Alpha Ideas and Rejected Ideas for similar mechanisms before creating a new note.
**Why:** Prevents alpha idea clutter.

### Decision: Source verification required
**What:** Every source cited in a research memo must be verified (paper confirmed to exist, URL resolves, claims cross-checked).
**Why:** Prevents hallucinated citations from entering the research record.

---

## 2026-05-12 — Project Structure Decisions

### Decision: Separate research and programming concerns
**What:** Research memos and programmer handoffs are separate artifacts. The researcher documents the alpha idea; the programmer implements the backtest.
**Why:** Prevents scope creep and keeps research focused on idea generation.

### Decision: Memory files use flat markdown, not a database
**What:** All project memory is stored as markdown files in `memory/`.
**Why:** Markdown is human-readable, works with git diff, requires no tooling.

### Decision: Research scope limited to crypto and commodities
**What:** Markets covered are crypto (spot, perps, on-chain) and commodity futures (gold, silver, crude oil).
**Why:** These markets have rich data availability, well-documented inefficiencies, and distinct alpha drivers.

### Decision: No backtests, no trading code, no broker connections
**What:** This project produces research documentation only. Implementation is deferred to the Programmer Agent.
**Why:** Maintains a clear boundary between alpha discovery and strategy implementation.
