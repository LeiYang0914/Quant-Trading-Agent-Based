# SYSTEM_MAP — Where Everything Lives

A quick-reference map of the Quant Trading AI System directory structure.

## Top-Level Layout

```
.
├── README.md                  — Project overview (human-readable)
├── CLAUDE.md                  — Claude Code instructions (agent-readable)
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
| `architecture/system_overview.md` | Full system architecture with agent diagram |
| `architecture/obsidian_integration_design.md` | Obsidian vault integration design |
| `workflows/alpha_lifecycle.md` | Complete alpha lifecycle from idea to live candidate |
| `protocols/research_protocol.md` | Research Agent 10-step workflow with quality gates |
| `protocols/handoff_protocol.md` | Inter-agent handoff formats and rules |
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

### `src/` — Source Code (future implementation)
| Path | Purpose |
|------|---------|
| `data/` | Data loaders, API adapters, vendor integrations |
| `signals/` | Signal/alpha implementations |
| `backtest/` | Backtest engines and utilities |
| `execution/` | Execution simulation (fills, latency, fees) |
| `risk/` | Risk calculation utilities |
| `portfolio/` | Portfolio construction and optimization |
| `utils/` | Shared utilities |

### `configs/` — Configuration (future)
| Path | Purpose |
|------|---------|
| `markets/` | Market definitions, trading hours, contract specs |
| `strategies/` | Strategy parameters (lookbacks, thresholds, weights) |
| `data/` | Data vendor configs, fee schedules, slippage models |
| `risk/` | Risk limits, position sizing rules, kill switches |

### `tests/` — Tests (future)
| Path | Purpose |
|------|---------|
| `data/` | Data loader tests |
| `signals/` | Signal logic tests |
| `backtest/` | Backtest correctness tests |
| `risk/` | Risk calculation tests |

### `reports/` — Reports
| Path | Purpose |
|------|---------|
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
