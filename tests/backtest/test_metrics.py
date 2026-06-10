"""Tests for backtest metrics module."""

import numpy as np
import pandas as pd
import pytest

from src.backtest.metrics import (
    BacktestMetrics,
    PERIODS_PER_YEAR,
    _max_drawdown,
    compute_metrics,
)


class TestMaxDrawdown:
    """Unit tests for the _max_drawdown helper."""

    def test_no_drawdown(self) -> None:
        equity = pd.Series([100.0, 101.0, 102.0, 103.0])
        dd, dur = _max_drawdown(equity)
        assert dd == 0.0
        assert dur == 0

    def test_simple_drawdown(self) -> None:
        equity = pd.Series([100.0, 95.0, 90.0, 100.0])
        dd, dur = _max_drawdown(equity)
        assert dd == pytest.approx(0.10)  # 10% from peak 100 to trough 90
        assert dur > 0

    def test_multiple_drawdowns_returns_max(self) -> None:
        equity = pd.Series([100.0, 90.0, 95.0, 80.0, 100.0])
        dd, _ = _max_drawdown(equity)
        assert dd == pytest.approx(0.20)  # 20% = max of 10% and 20%

    def test_empty_equity(self) -> None:
        dd, dur = _max_drawdown(pd.Series([], dtype=float))
        assert dd == 0.0
        assert dur == 0

    def test_single_point(self) -> None:
        dd, dur = _max_drawdown(pd.Series([100.0]))
        assert dd == 0.0
        assert dur == 0

    def test_recovery_then_new_drawdown(self) -> None:
        equity = pd.Series([100.0, 95.0, 100.0, 110.0, 100.0])
        dd, _ = _max_drawdown(equity)
        # Max DD is from peak 110 → trough 100 = 9.09%.
        assert dd == pytest.approx(0.09090909, abs=0.001)


class TestComputeMetrics:
    """Integration tests for compute_metrics."""

    @staticmethod
    def _flat_equity(n: int = 100) -> pd.Series:
        """Constant equity for edge case testing."""
        return pd.Series([100.0] * n)

    @staticmethod
    def _trending_equity(n: int = 200) -> pd.Series:
        """Smoothly trending equity — ~20% annual return, low vol."""
        rng = np.random.default_rng(42)
        returns = rng.normal(0.0002, 0.005, n)  # ~20% pa with ~30% vol
        prices = 100.0 * np.cumprod(1 + returns)
        return pd.Series(prices)

    def test_flat_equity_zero_return(self) -> None:
        m = compute_metrics(self._flat_equity())
        assert m.total_return_pct == pytest.approx(0.0, abs=0.01)
        assert m.max_drawdown_pct == pytest.approx(0.0, abs=0.01)

    def test_returns_all_fields_set(self) -> None:
        equity = self._trending_equity()
        m = compute_metrics(equity)
        assert isinstance(m.total_return_pct, float)
        assert isinstance(m.annualized_return_pct, float)
        assert isinstance(m.annualized_volatility_pct, float)
        assert isinstance(m.max_drawdown_pct, float)
        assert m.annualized_volatility_pct > 0

    def test_sharpe_computed_for_trending(self) -> None:
        equity = self._trending_equity()
        m = compute_metrics(equity)
        assert m.sharpe_ratio is not None

    def test_sharpe_none_for_short_series(self) -> None:
        m = compute_metrics(pd.Series([100.0, 100.0]))
        assert m.sharpe_ratio is None

    def test_risk_free_rate_used(self) -> None:
        equity = self._trending_equity()
        m_high = compute_metrics(equity, risk_free_rate_annual_pct=20.0)
        m_low = compute_metrics(equity, risk_free_rate_annual_pct=0.0)
        # Higher risk-free rate → lower Sharpe (excess returns shrink).
        if m_high.sharpe_ratio is not None and m_low.sharpe_ratio is not None:
            assert m_high.sharpe_ratio < m_low.sharpe_ratio

    def test_with_trades_wr(self) -> None:
        """Win rate should be computed when trades are provided."""
        equity = self._trending_equity()
        trades = pd.DataFrame(
            {
                "entry_time": pd.date_range("2023-01-01", periods=10, freq="8h"),
                "exit_time": pd.date_range("2023-01-02", periods=10, freq="8h"),
                "pnl": [100.0, -50.0, 200.0, -30.0, 150.0, -20.0, 80.0, -10.0, 60.0, -40.0],
                "notional": [10000.0] * 10,
            }
        )
        m = compute_metrics(equity, trades)
        assert m.total_trades == 10
        assert 0.0 <= m.win_rate_pct <= 100.0
        assert m.avg_win_loss_ratio is not None

    def test_turnover_from_trades(self) -> None:
        equity = self._trending_equity()
        trades = pd.DataFrame(
            {
                "entry_time": pd.date_range("2023-01-01", periods=5, freq="8h"),
                "exit_time": pd.date_range("2023-01-02", periods=5, freq="8h"),
                "pnl": [50.0] * 5,
                "notional": [5000.0] * 5,
            }
        )
        m = compute_metrics(equity, trades)
        assert m.turnover_pct > 0.0

    def test_periods_per_year_affects_annualisation(self) -> None:
        equity = self._trending_equity(365)
        m_daily = compute_metrics(equity, periods_per_year=365)
        m_8h = compute_metrics(equity, periods_per_year=PERIODS_PER_YEAR)
        # 8h periods → fewer years → higher annualised return.
        assert abs(m_8h.annualized_return_pct) > abs(m_daily.annualized_return_pct)

    def test_max_drawdown_equals_peak_to_trough(self) -> None:
        """A known drawdown should be captured exactly."""
        equity = pd.Series([100, 105, 90, 95, 110])
        m = compute_metrics(equity)
        # Peak=105, trough=90 → DD = (105-90)/105 ≈ 14.29%.
        assert m.max_drawdown_pct == pytest.approx((105 - 90) / 105 * 100, abs=0.1)

    def test_sortino_ratio_computed_for_trending(self) -> None:
        equity = self._trending_equity()
        m = compute_metrics(equity)
        assert m.sortino_ratio is not None
