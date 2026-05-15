# paper_trading/ — Paper Trading Simulation

This directory contains the paper trading simulation infrastructure.

## Directory Purpose

| Subdirectory | Purpose |
|-------------|---------|
| `logs/` | Execution logs for paper-traded strategies |
| `state/` | Current state (positions, P&L, orders) |

## Status

Paper trading is not yet active. This directory will be populated when strategies pass the Risk Agent gate and are approved for paper trading.

## When Active

- The Data Agent manages paper trading infrastructure
- All fills are simulated using realistic fee and slippage assumptions from `configs/data/`
- Paper trading logs are used by the Risk Agent to compare live signal behavior against backtest expectations
