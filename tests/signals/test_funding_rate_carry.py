"""Tests for funding_rate_carry.py — CRYPTO-001 signal module."""

import numpy as np
import pandas as pd
import pytest

from src.signals.funding_rate_carry import (
    FundingRateCarryConfig,
    FundingRateCarrySignal,
    SignalResult,
    compute_signals,
)
from src.data.funding_rate_loader import generate_sample_funding_data
from src.data.ohlcv_loader import generate_sample_ohlcv_data


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_test_data(n: int = 90, seed: int = 42) -> pd.DataFrame:
    """Build an aligned funding + OHLCV DataFrame for testing."""
    fr = generate_sample_funding_data("BTCUSDT", periods=n, seed=seed)
    ohlcv = generate_sample_ohlcv_data("BTCUSDT", periods=n, seed=seed)
    # Align on timestamp.
    merged = fr[["funding_time", "funding_rate"]].copy()
    merged = merged.rename(columns={"funding_time": "timestamp"})
    merged["spot_price"] = ohlcv["close"].values[:n]
    return merged


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestFundingRateCarryConfig:
    """Configuration defaults."""

    def test_default_values(self) -> None:
        cfg = FundingRateCarryConfig()
        assert cfg.funding_lookback_days == 30
        assert cfg.funding_threshold_pct == 5.0
        assert cfg.crowding_upper_pct == 90.0
        assert cfg.crowding_lower_pct == 10.0
        assert cfg.max_position_pct == 0.20

    def test_custom_values(self) -> None:
        cfg = FundingRateCarryConfig(
            funding_lookback_days=14,
            funding_threshold_pct=3.0,
            crowding_upper_pct=95.0,
        )
        assert cfg.funding_lookback_days == 14
        assert cfg.crowding_upper_pct == 95.0


class TestFundingRateCarrySignal:
    """Core signal computation tests."""

    def test_compute_returns_correct_count(self) -> None:
        data = _make_test_data(50)
        signal = FundingRateCarrySignal()
        results = signal.compute(data)
        assert len(results) == 50

    def test_empty_data(self) -> None:
        signal = FundingRateCarrySignal()
        results = signal.compute(pd.DataFrame())
        assert results == []

    def test_result_has_all_fields(self) -> None:
        data = _make_test_data(30)
        signal = FundingRateCarrySignal()
        results = signal.compute(data)
        r = results[0]
        assert isinstance(r, SignalResult)
        assert r.timestamp is not None
        assert isinstance(r.carry_weight, float)
        assert r.crowding_signal in (-1, 0, 1)
        assert isinstance(r.funding_percentile, float)

    # ------------------------------------------------------------------
    # No-lookahead bias tests
    # ------------------------------------------------------------------

    def test_no_lookahead_percentile(self) -> None:
        """Percentile at time t must not use data from t+1 or later."""
        data = _make_test_data(90)
        signal = FundingRateCarrySignal()
        results = signal.compute(data)

        for i, r in enumerate(results):
            window_end = i + 1
            manual_data = data["funding_rate"].iloc[:window_end]
            manual_pct = (manual_data <= data["funding_rate"].iloc[i]).mean() * 100.0
            assert abs(r.funding_percentile - manual_pct) < 0.001, (
                f"Mismatch at i={i}: computed={r.funding_percentile:.4f}, "
                f"manual={manual_pct:.4f}"
            )

    def test_earliest_point_is_self_only(self) -> None:
        """At i=0, the percentile should be 100 (only self in window)."""
        data = _make_test_data(30)
        signal = FundingRateCarrySignal()
        results = signal.compute(data)
        # First point: only one observation in window → always 100%.
        assert results[0].funding_percentile == pytest.approx(100.0)

    # ------------------------------------------------------------------
    # Crowding signal tests
    # ------------------------------------------------------------------

    def test_high_percentile_triggers_short(self) -> None:
        """Percentile >= 90 should produce crowding_signal = -1."""
        signal = FundingRateCarrySignal(
            FundingRateCarryConfig(crowding_upper_pct=90.0)
        )
        assert signal._crowding_signal(90.0) == -1
        assert signal._crowding_signal(95.0) == -1
        assert signal._crowding_signal(99.9) == -1

    def test_low_percentile_triggers_long(self) -> None:
        """Percentile <= 10 should produce crowding_signal = +1."""
        signal = FundingRateCarrySignal(
            FundingRateCarryConfig(crowding_lower_pct=10.0)
        )
        assert signal._crowding_signal(10.0) == 1
        assert signal._crowding_signal(5.0) == 1
        assert signal._crowding_signal(0.0) == 1

    def test_mid_percentile_is_neutral(self) -> None:
        signal = FundingRateCarrySignal()
        assert signal._crowding_signal(50.0) == 0
        assert signal._crowding_signal(11.0) == 0
        assert signal._crowding_signal(89.0) == 0

    def test_nan_percentile_is_neutral(self) -> None:
        signal = FundingRateCarrySignal()
        assert signal._crowding_signal(float("nan")) == 0

    # ------------------------------------------------------------------
    # Carry weight tests
    # ------------------------------------------------------------------

    def test_carry_weight_below_threshold_is_zero(self) -> None:
        signal = FundingRateCarrySignal(
            FundingRateCarryConfig(funding_threshold_pct=5.0)
        )
        assert signal._carry_weight(4.0) == 0.0
        assert signal._carry_weight(-3.0) == 0.0
        assert signal._carry_weight(0.0) == 0.0

    def test_carry_weight_positive_rate(self) -> None:
        signal = FundingRateCarrySignal(
            FundingRateCarryConfig(funding_threshold_pct=5.0, dynamic_carry_cap_pct=30.0)
        )
        w = signal._carry_weight(17.5)  # midpoint between 5 and 30
        assert w > 0.0
        assert w < 1.0

    def test_carry_weight_negative_rate(self) -> None:
        signal = FundingRateCarrySignal(
            FundingRateCarryConfig(funding_threshold_pct=5.0, dynamic_carry_cap_pct=30.0)
        )
        w = signal._carry_weight(-17.5)
        assert w < 0.0

    def test_carry_weight_at_cap_is_one(self) -> None:
        signal = FundingRateCarrySignal(
            FundingRateCarryConfig(funding_threshold_pct=5.0, dynamic_carry_cap_pct=30.0)
        )
        assert signal._carry_weight(30.0) == pytest.approx(1.0)

    def test_carry_weight_above_cap_capped_at_one(self) -> None:
        signal = FundingRateCarrySignal()
        w = signal._carry_weight(100.0)
        assert w <= 1.0

    # ------------------------------------------------------------------
    # Annualisation
    # ------------------------------------------------------------------

    def test_annualize_positive_rate(self) -> None:
        signal = FundingRateCarrySignal()
        s = pd.Series([0.0001])  # 0.01% per 8h
        result = signal._annualize(s)
        expected = 0.0001 * 3 * 365 * 100  # ≈ 10.95%
        assert result.iloc[0] == pytest.approx(expected)

    def test_annualize_zero_rate(self) -> None:
        signal = FundingRateCarrySignal()
        s = pd.Series([0.0])
        result = signal._annualize(s)
        assert result.iloc[0] == 0.0

    # ------------------------------------------------------------------
    # Edge cases
    # ------------------------------------------------------------------

    def test_unchanging_funding_rate(self) -> None:
        """All identical rates → all percentiles = 100 (tied)."""
        df = pd.DataFrame(
            {
                "timestamp": pd.date_range("2023-01-01", periods=30, freq="8h"),
                "funding_rate": [0.0001] * 30,
                "spot_price": [30000.0] * 30,
            }
        )
        signal = FundingRateCarrySignal()
        results = signal.compute(df)
        # All identical → each is at the maximum of its window.
        for r in results:
            assert r.funding_percentile == pytest.approx(100.0)
            assert r.crowding_signal == -1  # ≥ 90th percentile

    def test_rising_funding_rates(self) -> None:
        """Monotonically increasing rates → percentile should trend toward 100."""
        n = 90
        df = pd.DataFrame(
            {
                "timestamp": pd.date_range("2023-01-01", periods=n, freq="8h"),
                "funding_rate": np.linspace(0.00001, 0.001, n),
                "spot_price": [30000.0] * n,
            }
        )
        signal = FundingRateCarrySignal()
        results = signal.compute(df)
        # Last point should have high percentile.
        assert results[-1].funding_percentile > 50.0


class TestComputeSignals:
    """Convenience function tests."""

    def test_returns_dataframe(self) -> None:
        data = _make_test_data(20)
        df = compute_signals(data)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 20
        assert "carry_weight" in df.columns
        assert "crowding_signal" in df.columns

    def test_empty_input(self) -> None:
        df = compute_signals(pd.DataFrame())
        assert df.empty
