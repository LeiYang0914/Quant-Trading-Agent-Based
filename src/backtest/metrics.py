"""Performance metrics for backtest evaluation.

Computes standard portfolio metrics from an equity curve:
total return, Sharpe ratio, max drawdown, win rate, turnover, etc.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd

# 8h bars → annualisation factor: 3 per day × 365 days.
PERIODS_PER_YEAR = 3 * 365


@dataclass
class BacktestMetrics:
    """Container for all computed performance metrics.

    Attributes that are still ``None`` indicate computation was skipped
    (e.g. because the equity series was too short).
    """

    total_return_pct: float = 0.0
    annualized_return_pct: float = 0.0
    annualized_volatility_pct: float = 0.0
    sharpe_ratio: Optional[float] = None
    sortino_ratio: Optional[float] = None
    calmar_ratio: Optional[float] = None
    max_drawdown_pct: float = 0.0
    max_drawdown_duration_days: float = 0.0
    win_rate_pct: float = 0.0
    avg_win_loss_ratio: Optional[float] = None
    total_trades: int = 0
    turnover_pct: float = 0.0
    average_exposure_pct: float = 0.0
    risk_free_rate_annual_pct: float = 4.0


def compute_metrics(
    equity: pd.Series,
    trades: pd.DataFrame | None = None,
    *,
    periods_per_year: int = PERIODS_PER_YEAR,
    risk_free_rate_annual_pct: float = 4.0,
) -> BacktestMetrics:
    """Compute a full set of performance metrics from an equity curve.

    Parameters
    ----------
    equity: Time-indexed equity series (NAV per bar).
    trades: Optional DataFrame of individual trades with columns
        ``[entry_time, exit_time, pnl, notional]``.
    periods_per_year: Number of bars per year for annualisation.
    risk_free_rate_annual_pct: Annual risk-free rate (percentage).

    Returns
    -------
    BacktestMetrics
    """
    m = BacktestMetrics()
    m.risk_free_rate_annual_pct = risk_free_rate_annual_pct

    if len(equity) < 2:
        return m

    # Returns.
    returns = equity.pct_change().dropna()
    if len(returns) == 0:
        return m

    start_eq = equity.iloc[0]
    end_eq = equity.iloc[-1]

    m.total_return_pct = ((end_eq / start_eq) - 1.0) * 100.0

    # Annualised return.
    n_years = len(returns) / periods_per_year
    if n_years > 0 and start_eq > 0 and end_eq > 0:
        m.annualized_return_pct = (
            ((end_eq / start_eq) ** (1.0 / n_years) - 1.0) * 100.0
        )
    else:
        m.annualized_return_pct = 0.0

    # Volatility.
    period_vol = returns.std()
    m.annualized_volatility_pct = period_vol * np.sqrt(periods_per_year) * 100.0

    # Sharpe ratio (annualised).
    excess_daily = returns - (risk_free_rate_annual_pct / 100.0) / periods_per_year
    if period_vol > 0 and len(returns) > 1:
        m.sharpe_ratio = (
            excess_daily.mean() / period_vol * np.sqrt(periods_per_year)
        )
    else:
        m.sharpe_ratio = None

    # Sortino ratio.
    downside = returns[returns < 0]
    if len(downside) > 1 and downside.std() > 0:
        m.sortino_ratio = (
            excess_daily.mean() / downside.std() * np.sqrt(periods_per_year)
        )
    else:
        m.sortino_ratio = None

    # Maximum drawdown.
    dd_pct, dd_duration = _max_drawdown(equity)
    m.max_drawdown_pct = dd_pct * 100.0
    m.max_drawdown_duration_days = dd_duration / 3.0  # 8h bars → days

    # Calmar ratio.
    if m.max_drawdown_pct != 0 and m.max_drawdown_pct > 0.001:
        m.calmar_ratio = m.annualized_return_pct / abs(m.max_drawdown_pct)
    else:
        m.calmar_ratio = None

    # Win rate and trade stats.
    if trades is not None and len(trades) > 0:
        m.total_trades = len(trades)
        winning = trades[trades["pnl"] > 0]
        losing = trades[trades["pnl"] <= 0]
        m.win_rate_pct = (len(winning) / len(trades)) * 100.0 if len(trades) > 0 else 0.0
        avg_win = winning["pnl"].mean() if len(winning) > 0 else 0.0
        avg_loss = abs(losing["pnl"].mean()) if len(losing) > 0 else 0.0
        m.avg_win_loss_ratio = (avg_win / avg_loss) if avg_loss > 0 else None
        total_notional = trades["notional"].sum()
        avg_equity = equity.mean()
        if avg_equity > 0:
            m.turnover_pct = (total_notional / (avg_equity * len(equity) / periods_per_year)) * 100.0
    else:
        # Estimate from equity changes.
        trade_signals = (equity.diff().fillna(0) != 0).sum()
        m.total_trades = int(trade_signals)

    # Average exposure (from returns volatility relative to benchmark vol — rough).
    m.average_exposure_pct = (
        m.annualized_volatility_pct / 60.0 * 100.0
    )  # relative to ~60% BTC vol

    return m


def _max_drawdown(equity: pd.Series) -> tuple[float, int]:
    """Compute maximum drawdown from peak and its duration in bars.

    Returns
    -------
    (max_drawdown_fraction, max_duration_bars)
    """
    if len(equity) < 2:
        return 0.0, 0

    peak = equity.iloc[0]
    max_dd = 0.0
    max_duration = 0
    current_duration = 0

    for val in equity:
        if val >= peak:
            peak = val
            current_duration = 0
        else:
            dd = (peak - val) / peak
            current_duration += 1
            if dd > max_dd:
                max_dd = dd
            if current_duration > max_duration:
                max_duration = current_duration

    return max_dd, max_duration
