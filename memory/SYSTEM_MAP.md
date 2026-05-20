# SYSTEM_MAP — Where Everything Lives

A quick-reference map of the Quant Trading AI System directory structure.

## Top-Level Layout

```
.
├── README.md                  — Project overview (human-readable)
├── CLAUDE.md                  — Claude Code instructions (agent-readable)
├── pyproject.toml             — Python project metadata and dependencies
├── .claude/agents/            — Agent personality definitions (5 agents)
├── memory/                    — Persistent project state (session-to-session)
├── research/                  — Alpha research outputs (domain-separated)
├── handoffs/                  — Programmer handoff pipeline
├── knowledge/                 — Obsidian knowledge graph
├── system/                    — Architecture, workflows, protocols, specs
├── src/                       — Source code (future implementation)
├── configs/                   — Configuration files (future)
├── tests/                     — Unit and integration tests (future)
├── reports/                   — Backtest, risk, and data quality reports
├── paper_trading/             — Paper trading simulation logs and state
└── templates/                 — Document templates for all agents
```

## Detailed Map

### `.claude/agents/` — Agent Definitions
| File | Purpose |
|------|---------|
| `research-agent.md` | Research Agent: crypto-first domain separation, source-backed alpha discovery |
| `review-agent.md` | Review Agent: evaluates ideas, approves/rejects, overlap detection |
| `programmer-agent.md` | Programmer Agent: implements approved ideas, runs backtests |
| `data-agent.md` | Data Agent: manages data, quality, execution simulation |
| `risk-agent.md` | Risk Agent: final risk gate, position sizing, kill switches |

### `memory/` — Project Memory
| File | Purpose |
|------|---------|
| `PROJECT_STATE.md` | Current status, active research, default domain (crypto-first) |
| `ALPHA_BACKLOG.md` | Prioritized queue of alpha ideas (domain-grouped: crypto, commodities, cross_market) |
| `RESEARCH_LOG.md` | Dated journal of all research sessions |
| `SOURCE_TRACKER.md` | Registry of all sources with structured IDs (CRYPTO-PAPER-NNN, etc.) and reliability tiers |
| `DECISIONS.md` | Important project and methodological decisions |
| `SYSTEM_MAP.md` | This file — where everything lives |

### `research/` — Alpha Research (Domain-Separated)

```
research/
  memos/
    crypto/          — Crypto research memos (CRYPTO-NNN)
    commodities/     — Commodity research memos (COMMOD-NNN)
    cross_market/    — Cross-market research memos (CROSS-NNN)
  ideas/
    proposed/
      crypto/        — Crypto ideas for Review Agent
      commodities/   — Commodity ideas for Review Agent
      cross_market/  — Cross-market ideas for Review Agent
    approved/
      crypto/        — Crypto ideas approved by Review Agent
      commodities/   — Commodity ideas approved by Review Agent
      cross_market/  — Cross-market ideas approved by Review Agent
    rejected/
      crypto/        — Rejected crypto ideas (preserved)
      commodities/   — Rejected commodity ideas (preserved)
      cross_market/  — Rejected cross-market ideas (preserved)
    archived/
      crypto/        — Retired crypto strategies
      commodities/   — Retired commodity strategies
      cross_market/  — Retired cross-market strategies
  papers/            — Downloaded/saved academic papers
```

### `handoffs/` — Programmer Handoff Pipeline
| Path | Purpose |
|------|---------|
| `pending/` | Handoffs ready for Programmer Agent |
| `in_progress/` | Handoffs being implemented |
| `completed/` | Handoffs fully implemented and backtested |
| `archived/` | Old/retired handoffs |

### `knowledge/Quant-Research-KB/` — Obsidian Vault
| Path | Purpose |
|------|---------|
| `01_Concepts/` | Core concept notes (Funding Rate, Open Interest, etc.) |
| `02_Alpha_Ideas/` | Alpha idea notes with YAML frontmatter |
| `05_Paper_Notes/` | Academic paper summaries |
| `06_Data_Source_Notes/` | Data vendor documentation |
| `07_Risk_Failure_Modes/` | Risk and failure mode notes |
| `09_Programmer_Handoffs/` | Handoff notes linked to vault |
| `99_Templates/` | Obsidian note templates |
| `Dashboard.md` | Auto-populating Map of Content |

### `system/` — System Documentation
| Path | Purpose |
|------|---------|
| `architecture/system_overview.md` | Full system architecture with agent diagram and LLM Router |
| `architecture/llm_router_design.md` | LLM Router architecture: provider abstraction, routing, fallback |
| `architecture/llm_dashboard_design.md` | LLM Dashboard architecture: layers, data flow, security, chart strategy |
| `architecture/obsidian_integration_design.md` | Obsidian vault integration design |
| `workflows/alpha_lifecycle.md` | Complete alpha lifecycle from idea to live candidate |
| `protocols/research_protocol.md` | Research Agent 10-step workflow with quality gates |
| `protocols/handoff_protocol.md` | Inter-agent handoff formats and rules |
| `protocols/llm_routing_protocol.md` | LLM routing protocol: request format, rules, fallback, forbidden behavior |
| `protocols/llm_dashboard_protocol.md` | LLM Dashboard protocol: launch, navigation, metrics, security rules |
| `agent_specs/research-agent.md` | Research Agent detailed specification |
| `agent_specs/review-agent.md` | Review Agent detailed specification |
| `agent_specs/programmer-agent.md` | Programmer Agent detailed specification |
| `agent_specs/data-agent.md` | Data Agent detailed specification |
| `agent_specs/risk-agent.md` | Risk Agent detailed specification |
| `agent_specs/research_agent_skills/` | **Research Agent skills layer (10 modular skills)** |
| `agent_specs/research_agent_skills/README.md` | Master index — skill descriptions, invocation order, dependency graph |
| `agent_specs/research_agent_skills/domain_queue_management_skill.md` | Skill 1: Choose domain and next idea from backlog |
| `agent_specs/research_agent_skills/source_discovery_skill.md` | Skill 2: Find, verify, and record sources |
| `agent_specs/research_agent_skills/paper_analysis_skill.md` | Skill 3: Extract methodology and findings from papers |
| `agent_specs/research_agent_skills/crypto_market_structure_skill.md` | Skill 4: Crypto market microstructure context |
| `agent_specs/research_agent_skills/commodities_market_structure_skill.md` | Skill 5: Commodity futures microstructure context |
| `agent_specs/research_agent_skills/alpha_discovery_skill.md` | Skill 6: Build alpha idea from evidence |
| `agent_specs/research_agent_skills/memo_writing_skill.md` | Skill 7: Write 19-section research memo |
| `agent_specs/research_agent_skills/research_quality_control_skill.md` | Skill 8: Run 20 quality checks before review |
| `agent_specs/research_agent_skills/handoff_preparation_skill.md` | Skill 9: Prepare review and programmer handoffs |
| `agent_specs/research_agent_skills/research_memory_update_skill.md` | Skill 10: Update all memory files |

### `src/` — Source Code
| Path | Purpose |
|------|---------|
| `llm/` | **LLM Router — infrastructure layer (implemented 2026-05-17)** |
| `llm/router.py` | Core LLMRouter: routing, fallback, caching, circuit breaker, ask() API |
| `llm/types.py` | TaskType (19 types), TaskRequest, RoutingDecision, LLMResponse types |
| `llm/providers/base.py` | BaseProvider abstract interface (call, validate_config, health_check) |
| `llm/providers/claude_provider.py` | Claude (Anthropic) provider — real SDK wiring, graceful degradation |
| `llm/providers/deepseek_provider.py` | DeepSeek provider — OpenAI-compatible SDK, graceful degradation |
| `llm/prompts/task_classifier.py` | Three-tier task classification: keyword map → activity hints → agent fallback; complexity/cost/long-context inference |
| `llm/utils/logging.py` | RoutingLogger — JSONL audit log |
| `llm/utils/cost_estimator.py` | Rough per-call cost estimation |
| `llm/utils/cache.py` | ResponseCache — file-based JSON index with TTL, eviction, exclusions |
| `llm/utils/rate_limiter.py` | RateLimiter — sliding-window per-provider rate limiting |
| `llm/utils/circuit_breaker.py` | CircuitBreaker — CLOSED→OPEN→HALF_OPEN→CLOSED state machine |
| `llm/utils/usage_tracker.py` | UsageTracker — JSONL-based cost/performance tracking with aggregation |
| `llm/utils/env_loader.py` | Env loader — loads .env via python-dotenv if installed |
| `data/` | Data loaders, API adapters, vendor integrations |
| `signals/` | Signal/alpha implementations |
| `backtest/` | Backtest engines and utilities |
| `execution/` | Execution simulation (fills, latency, fees) |
| `risk/` | Risk calculation utilities |
| `portfolio/` | Portfolio construction and optimization |
| `utils/` | Shared utilities |

### `src/dashboard/` — LLM Router Dashboard
| Path | Purpose |
|------|---------|
| `app.py` | Main Streamlit app: 8 pages, sidebar navigation, empty state handling |
| `backend/log_reader.py` | Read usage.jsonl and routing_log.jsonl with time/limit filters |
| `backend/metrics_service.py` | Pure-function metrics: overview, providers, agents, failures, cache |
| `backend/aggregation.py` | Group-by and time-bucket aggregation helpers |
| `backend/health_service.py` | Router health check with API key redaction, offline fallback |
| `components/metric_cards.py` | Metric card renderers: overview, provider, agent cards |
| `components/charts.py` | Plotly charts: requests over time, cost over time, distributions |
| `components/tables.py` | Dataframe tables: routing, failures, agent summary, cost |
| `components/filters.py` | Sidebar filter controls and filter logic |

### `scripts/` — CLI and Utility Scripts
| Path | Purpose |
|------|---------|
| `scripts/llm_router_cli.py` | LLM Router CLI: health check, usage summary, cache management |
| `scripts/run_dashboard.py` | Launch the LLM Router Dashboard in default browser |

### `configs/` — Configuration
| Path | Purpose |
|------|---------|
| `llm/models.yaml` | LLM provider model configs (Claude, DeepSeek) |
| `llm/routing_rules.yaml` | Routing rules, overrides, fallback, per-agent mappings |
| `dashboard/dashboard.yaml` | Dashboard config: port, log paths, refresh, page visibility, charts, redaction |
| `markets/` | Market definitions, trading hours, contract specs |
| `strategies/` | Strategy parameters (lookbacks, thresholds, weights) |
| `data/` | Data vendor configs, fee schedules, slippage models |
| `risk/` | Risk limits, position sizing rules, kill switches |

### `tests/` — Tests
| Path | Purpose |
|------|---------|
| `llm/test_router.py` | LLM Router routing decision tests (30 tests) |
| `llm/test_router_advanced.py` | Advanced router tests: ask(), health, cache, circuits (16 tests) |
| `llm/test_router_production.py` | Production-readiness tests: provider config, health check, cache, rate limiter, circuit breaker, usage tracker, ask(), fallback, classifier, CLI (69 tests) |
| `llm/test_task_classification.py` | Task classifier keyword and complexity tests (16 tests) |
| `llm/test_fallbacks.py` | Fallback behavior and permissions tests (6 tests) |
| `llm/test_cache.py` | Response cache operations and exclusions (13 tests) |
| `llm/test_circuit_breaker.py` | Circuit breaker state machine tests (11 tests) |
| `llm/test_rate_limiter.py` | Rate limiter acquire/block/reset tests (8 tests) |
| `llm/test_usage_tracker.py` | Usage tracker recording and aggregation tests (11 tests) |
| `dashboard/` | Dashboard backend tests: log_reader, metrics_service, aggregation, health_service |
| `data/` | Data loader tests |
| `signals/` | Signal logic tests |
| `backtest/` | Backtest correctness tests |
| `risk/` | Risk calculation tests |

### `reports/` — Reports
| Path | Purpose |
|------|---------|
| `llm_routing/` | LLM Router decision audit logs (JSONL) |
| `backtests/` | Backtest reports from Programmer Agent |
| `paper_trading/` | Paper trading performance reports |
| `risk_reviews/` | Risk review reports from Risk Agent |
| `data_quality/` | Data quality reports from Data Agent |

### `paper_trading/` — Paper Trading
| Path | Purpose |
|------|---------|
| `logs/` | Paper trading execution logs |
| `state/` | Current paper trading state (positions, P&L) |

### `templates/` — Document Templates
| File | Purpose |
|------|---------|
| `research_memo.md` | Alpha research memo (domain-aware, structured references) |
| `alpha_discovery_note.md` | Alpha discovery note (pre-memo, reference requirements) |
| `paper_summary.md` | Academic/industry paper summary |
| `research_session_log.md` | Per-session research activity log |
| `review_report.md` | Review Agent decision template |
| `programmer_handoff.md` | Programmer implementation handoff template |
| `backtest_report.md` | Backtest results report template |
| `data_quality_report.md` | Data quality report template |
| `risk_review.md` | Risk review report template |
| `llm_task_request.md` | LLM Router task request template with examples |
| `llm_routing_log.md` | LLM routing log entry formats and field reference |
