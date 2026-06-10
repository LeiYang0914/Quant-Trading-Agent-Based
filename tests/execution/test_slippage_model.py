"""Tests for slippage_model.py"""

import pytest

from src.execution.slippage_model import DEFAULT_SLIPPAGE_MODEL, SlippageModel


class TestSlippageModel:
    """Test slippage estimation."""

    def test_default_base_bps(self) -> None:
        sm = DEFAULT_SLIPPAGE_MODEL
        assert sm.base_bps == 2.0

    def test_estimate_bps_normal_size(self) -> None:
        sm = SlippageModel(base_bps=2.0, volume_pct_limit=0.05)
        # Notional = 5% of interval volume → exactly at limit, base_bps.
        bps = sm.estimate_bps(50_000.0, interval_volume=1_000_000.0)
        assert bps == 2.0

    def test_estimate_bps_small_size(self) -> None:
        sm = SlippageModel(base_bps=2.0, volume_pct_limit=0.05)
        bps = sm.estimate_bps(10_000.0, interval_volume=1_000_000.0)
        assert bps == 2.0  # Small fraction → base slippage.

    def test_estimate_bps_large_size_increases(self) -> None:
        sm = SlippageModel(base_bps=2.0, volume_pct_limit=0.05)
        # 20% of volume → 4× the limit → 4× base_bps.
        bps = sm.estimate_bps(200_000.0, interval_volume=1_000_000.0)
        assert bps > 2.0
        assert bps == pytest.approx(8.0)  # 4 × 2.0

    def test_estimate_bps_no_volume_info(self) -> None:
        sm = SlippageModel(base_bps=3.0)
        bps = sm.estimate_bps(1_000_000.0)
        assert bps == 3.0

    def test_estimate_bps_zero_volume(self) -> None:
        sm = SlippageModel(base_bps=3.0)
        bps = sm.estimate_bps(1_000_000.0, interval_volume=0.0)
        assert bps == 3.0

    def test_apply_slippage_buy(self) -> None:
        sm = SlippageModel(base_bps=10.0)  # 10 bps
        bps, exec_price = sm.apply_slippage(1000.0, 10000.0, "buy")
        assert bps == 10.0
        # 10 bps = 0.1% → buy at 1000 * 1.001 = 1001.0
        assert exec_price == pytest.approx(1001.0)

    def test_apply_slippage_sell(self) -> None:
        sm = SlippageModel(base_bps=10.0)
        bps, exec_price = sm.apply_slippage(1000.0, 10000.0, "sell")
        # Sell at 1000 * (1 - 0.001) = 999.0
        assert exec_price == pytest.approx(999.0)

    def test_slippage_symmetric(self) -> None:
        """Buy and sell should have symmetric absolute distance from mid."""
        sm = SlippageModel(base_bps=10.0)
        _, buy_price = sm.apply_slippage(1000.0, 10000.0, "buy")
        _, sell_price = sm.apply_slippage(1000.0, 10000.0, "sell")
        assert abs(1000.0 - buy_price) == pytest.approx(abs(1000.0 - sell_price))

    def test_frozen_dataclass(self) -> None:
        sm = SlippageModel()
        with pytest.raises(Exception):
            sm.base_bps = 10.0  # type: ignore[misc]
