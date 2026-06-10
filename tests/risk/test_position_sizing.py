"""Tests for position_sizing.py"""

import pytest

from src.risk.position_sizing import PositionSizer


class TestPositionSizer:
    """Test position sizing logic."""

    def test_default_max_notional(self) -> None:
        sizer = PositionSizer()
        notional = sizer.size_position(nav=100_000.0, price=1000.0)
        assert notional == 20_000.0  # 20% of NAV

    def test_zero_nav_returns_zero(self) -> None:
        sizer = PositionSizer()
        assert sizer.size_position(nav=0.0, price=1000.0) == 0.0
        assert sizer.size_position(nav=-100.0, price=1000.0) == 0.0

    def test_zero_price_returns_zero(self) -> None:
        sizer = PositionSizer()
        assert sizer.size_position(nav=100_000.0, price=0.0) == 0.0

    def test_leverage_cap(self) -> None:
        sizer = PositionSizer(max_notional_pct=1.0, max_leverage=1.5)
        notional = sizer.size_position(nav=100_000.0, price=1000.0)
        assert notional <= 150_000.0  # 1.5 × NAV

    def test_atr_based_sizing_reduces_notional(self) -> None:
        """High volatility should reduce position size."""
        sizer = PositionSizer(max_notional_pct=1.0, risk_per_trade_pct=1.0)
        base_notional = sizer.size_position(nav=100_000.0, price=1000.0)
        atr_notional = sizer.size_position(
            nav=100_000.0, price=1000.0, atr=100.0  # 10% ATR!
        )
        assert atr_notional < base_notional

    def test_liquidity_constraint(self) -> None:
        sizer = PositionSizer(max_notional_pct=1.0, min_volume_ratio=0.05)
        notional = sizer.size_position(
            nav=100_000.0, price=1000.0, interval_volume=200_000.0
        )
        assert notional <= 10_000.0  # 5% of $200k

    def test_multiple_constraints_min_wins(self) -> None:
        """When all constraints are active, the tightest should win."""
        sizer = PositionSizer(
            max_notional_pct=0.20,
            max_leverage=2.0,
            risk_per_trade_pct=0.5,  # very tight risk
            atr_multiple=10.0,  # very wide stop
        )
        notional = sizer.size_position(
            nav=100_000.0,
            price=1000.0,
            atr=100.0,  # extremely high vol
        )
        # Risk constraint: risk_amount = 100k * 0.005 = $500
        # units = 500 / (10 * 100) = 0.5
        # notional = 0.5 * 1000 = $500
        assert notional <= 20_000.0

    def test_units_from_notional(self) -> None:
        sizer = PositionSizer()
        units = sizer.units_from_notional(10_000.0, 1000.0)
        assert units == 10.0

    def test_units_from_notional_zero_price(self) -> None:
        sizer = PositionSizer()
        assert sizer.units_from_notional(10_000.0, 0.0) == 0.0
