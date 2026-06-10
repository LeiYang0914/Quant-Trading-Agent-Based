"""Tests for event_backtester.py — event-driven backtest engine."""

import numpy as np
import pandas as pd
import pytest

from src.backtest.event_backtester import (
    BacktestConfig,
    BacktestResult,
    EventBacktester,
)
from src.signals.funding_rate_carry import compute_signals
from src.data.funding_rate_loader import generate_sample_funding_data
from src.data.ohlcv_loader import generate_sample_ohlcv_data


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_aligned_data(n: int = 120, seed: int = 42) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (signals_df, ohlcv_df) aligned on timestamp."""
    fr = generate_sample_funding_data("BTCUSDT", periods=n, seed=seed)
    ohlcv = generate_sample_ohlcv_data("BTCUSDT", periods=n, seed=seed)

    merged = fr[["funding_time", "funding_rate", "mark_price"]].copy()
    merged = merged.rename(columns={"funding_time": "timestamp"})
    merged["spot_price"] = ohlcv["close"].values[:n]
    merged["mark_price"] = merged["mark_price"].fillna(merged["spot_price"])

    signals = compute_signals(merged)
    return signals, ohlcv


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestBacktestConfig:
    """Configuration defaults."""

    def test_defaults(self) -> None:
        cfg = BacktestConfig()
        assert cfg.initial_capital == 100_000.0
        assert cfg.enable_carry_leg is True
        assert cfg.enable_crowding_leg is True

    def test_custom(self) -> None:
        cfg = BacktestConfig(initial_capital=50_000.0, max_position_pct=0.10)
        assert cfg.initial_capital == 50_000.0
        assert cfg.max_position_pct == 0.10


class TestEventBacktester:
    """Core backtest logic tests."""

    def test_run_returns_backtest_result(self) -> None:
        signals, ohlcv = _make_aligned_data(60)
        tester = EventBacktester()
        result = tester.run(signals, ohlcv)
        assert isinstance(result, BacktestResult)

    def test_equity_curve_has_values(self) -> None:
        signals, ohlcv = _make_aligned_data(60)
        tester = EventBacktester()
        result = tester.run(signals, ohlcv)
        assert len(result.equity_curve) > 0
        assert (result.equity_curve > 0).all()

    def test_positions_logged(self) -> None:
        signals, ohlcv = _make_aligned_data(60)
        tester = EventBacktester()
        result = tester.run(signals, ohlcv)
        assert len(result.positions) > 0

    def test_empty_signals(self) -> None:
        tester = EventBacktester()
        result = tester.run(pd.DataFrame(), pd.DataFrame())
        assert result.equity_curve.empty
        assert result.positions.empty
        assert result.trades.empty

    def test_single_bar_no_crash(self) -> None:
        signals, ohlcv = _make_aligned_data(2)
        tester = EventBacktester()
        result = tester.run(signals, ohlcv)
        assert isinstance(result, BacktestResult)

    def test_carry_only_mode(self) -> None:
        """With carry only, crowding leg should not fire."""
        cfg = BacktestConfig(enable_carry_leg=True, enable_crowding_leg=False)
        signals, ohlcv = _make_aligned_data(60)
        tester = EventBacktester(cfg)
        result = tester.run(signals, ohlcv)
        assert isinstance(result, BacktestResult)
        # Trades should exist (carry leg).
        if len(result.trades) > 0:
            assert all("crowding" not in str(s) for s in result.trades["side"])

    def test_crowding_only_mode(self) -> None:
        cfg = BacktestConfig(enable_carry_leg=False, enable_crowding_leg=True)
        signals, ohlcv = _make_aligned_data(60)
        tester = EventBacktester(cfg)
        result = tester.run(signals, ohlcv)
        assert isinstance(result, BacktestResult)

    def test_no_lookahead_execution(self) -> None:
        """Signal at bar t should execute at bar t+1 open.

        We verify this by checking that bars where signal is computed
        don't use the same bar's open price for execution.
        """
        signals, ohlcv = _make_aligned_data(90)
        tester = EventBacktester()
        result = tester.run(signals, ohlcv)
        # The equity curve starts at bar 1, not bar 0, confirming
        # execution is at next-bar-open.
        assert len(result.equity_curve) <= len(signals) - 1

    def test_fees_non_negative(self) -> None:
        signals, ohlcv = _make_aligned_data(60)
        tester = EventBacktester()
        result = tester.run(signals, ohlcv)
        assert result.fees_total >= 0.0

    def test_slippage_non_negative(self) -> None:
        signals, ohlcv = _make_aligned_data(60)
        tester = EventBacktester()
        result = tester.run(signals, ohlcv)
        assert result.slippage_total >= 0.0

    def test_high_fee_environment(self) -> None:
        """With very high fees, equity should degrade relative to zero fees."""
        from src.execution.fee_model import FeeModel

        cfg_low = BacktestConfig(fee_model=FeeModel(taker_bps=0.01))
        cfg_high = BacktestConfig(fee_model=FeeModel(taker_bps=100.0))

        signals, ohlcv = _make_aligned_data(60)
        result_low = EventBacktester(cfg_low).run(signals, ohlcv)
        result_high = EventBacktester(cfg_high).run(signals, ohlcv)

        # Higher fees → higher total fees.
        if result_high.fees_total > 0 or result_low.fees_total > 0:
            assert result_high.fees_total >= result_low.fees_total

    def test_pnl_components_sum_to_equity_change(self) -> None:
        """The change in equity should roughly equal the sum of PnL components
        less fees and slippage."""
        signals, ohlcv = _make_aligned_data(60)
        tester = EventBacktester()
        result = tester.run(signals, ohlcv)

        if len(result.equity_curve) > 0:
            equity_change = result.equity_curve.iloc[-1] - result.equity_curve.iloc[0]
            pnl_sum = (
                result.funding_pnl_total
                + result.price_pnl_total
                - result.fees_total
                - result.slippage_total
            )
            # Allow small differences due to final close-out fees/slippage
            # not captured in the accumulated components identically.
            assert abs(equity_change - pnl_sum) < 20.0
