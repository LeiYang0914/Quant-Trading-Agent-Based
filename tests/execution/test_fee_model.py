"""Tests for fee_model.py"""

import pytest

from src.execution.fee_model import DEFAULT_FEE_MODEL, FeeModel


class TestFeeModel:
    """Test transaction fee calculations."""

    def test_default_taker_fee(self) -> None:
        fm = DEFAULT_FEE_MODEL
        assert fm.taker_bps == 4.0
        assert fm.maker_bps == 2.0

    def test_fee_bps_taker(self) -> None:
        fm = FeeModel(maker_bps=1.0, taker_bps=3.0)
        assert fm.fee_bps(is_taker=True) == 3.0

    def test_fee_bps_maker(self) -> None:
        fm = FeeModel(maker_bps=1.0, taker_bps=3.0)
        assert fm.fee_bps(is_taker=False) == 1.0

    def test_apply_fee_taker(self) -> None:
        fm = FeeModel(taker_bps=4.0)  # 4 bps = 0.04%
        fee, net = fm.apply_fee(10000.0, is_taker=True)
        assert fee == pytest.approx(4.0)  # 10000 * 4/10000
        assert net == pytest.approx(9996.0)

    def test_apply_fee_maker(self) -> None:
        fm = FeeModel(maker_bps=2.0)
        fee, net = fm.apply_fee(10000.0, is_taker=False)
        assert fee == pytest.approx(2.0)
        assert net == pytest.approx(9998.0)

    def test_apply_fee_zero_notional(self) -> None:
        fm = DEFAULT_FEE_MODEL
        fee, net = fm.apply_fee(0.0)
        assert fee == 0.0
        assert net == 0.0

    def test_apply_fee_large_notional(self) -> None:
        fm = FeeModel(taker_bps=5.0)
        fee, net = fm.apply_fee(1_000_000.0)
        assert fee == pytest.approx(500.0)  # 1M * 5/10000
        assert net == pytest.approx(999_500.0)

    def test_round_trip_bps(self) -> None:
        fm = FeeModel(taker_bps=4.0)
        assert fm.round_trip_bps() == 8.0  # 2 × 4 bps

    def test_frozen_dataclass(self) -> None:
        fm = FeeModel()
        with pytest.raises(Exception):
            fm.taker_bps = 10.0  # type: ignore[misc]
