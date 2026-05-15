# src/ — Source Code

This directory will contain all strategy implementation code. It is currently a placeholder for future implementation work by the Programmer Agent and Data Agent.

## Directory Purpose

| Subdirectory | Purpose | Owner |
|-------------|---------|-------|
| `data/` | Data loaders, API adapters, vendor integrations | Data Agent |
| `signals/` | Signal/alpha implementations | Programmer Agent |
| `backtest/` | Backtest engines and utilities | Programmer Agent |
| `execution/` | Execution simulation (fills, latency, fees) | Data Agent |
| `risk/` | Risk calculation utilities | Risk Agent |
| `portfolio/` | Portfolio construction and optimization | Risk Agent |
| `utils/` | Shared utilities | All agents |

## Status

No strategy code has been implemented yet. The system is currently in the architecture and alpha research phase.

## When Code Is Added

- All signal implementations must reference their source handoff document
- All backtests must include parameter sweeps, subperiod analysis, and cost sensitivity
- All data loaders must document their source vendor and known issues
- Configuration values belong in `configs/`, not hardcoded
