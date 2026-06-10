"""Tests for drawdown.py"""

import pytest

from src.risk.drawdown import DrawdownLevel, DrawdownTracker


class TestDrawdownTracker:
    """Test drawdown tracking and risk level signals."""

    def test_initial_state_normal(self) -> None:
        tracker = DrawdownTracker()
        assert tracker.level() == DrawdownLevel.NORMAL
        assert tracker.current_drawdown_pct == 0.0

    def test_peak_tracking(self) -> None:
        tracker = DrawdownTracker()
        tracker.update(100.0)
        tracker.update(110.0)
        assert tracker.peak_equity == 110.0
        assert tracker.current_drawdown_pct == 0.0

    def test_drawdown_detection(self) -> None:
        tracker = DrawdownTracker()
        tracker.update(100.0)
        tracker.update(95.0)
        assert tracker.current_drawdown_pct == pytest.approx(5.0)

    def test_warning_threshold(self) -> None:
        tracker = DrawdownTracker(warning_threshold_pct=10.0)
        tracker.update(100.0)
        level = tracker.update(89.0)  # 11% drawdown
        assert level == DrawdownLevel.WARNING
        assert tracker.current_drawdown_pct == pytest.approx(11.0)

    def test_critical_threshold(self) -> None:
        tracker = DrawdownTracker(critical_threshold_pct=20.0)
        tracker.update(100.0)
        level = tracker.update(79.0)  # 21% drawdown
        assert level == DrawdownLevel.CRITICAL

    def test_recovery_resets_drawdown(self) -> None:
        tracker = DrawdownTracker()
        tracker.update(100.0)
        tracker.update(90.0)  # 10% DD
        assert tracker.current_drawdown_pct == pytest.approx(10.0)
        tracker.update(110.0)  # new peak
        assert tracker.current_drawdown_pct == 0.0
        assert tracker.level() == DrawdownLevel.NORMAL

    def test_max_drawdown_persists(self) -> None:
        tracker = DrawdownTracker()
        tracker.update(100.0)
        tracker.update(80.0)  # 20% DD
        tracker.update(120.0)  # new peak, current DD resets
        assert tracker.max_drawdown_pct == pytest.approx(20.0)
        assert tracker.current_drawdown_pct == 0.0

    def test_position_scalar_normal(self) -> None:
        tracker = DrawdownTracker()
        tracker.update(100.0)
        tracker.update(101.0)
        assert tracker.position_scalar() == 1.0

    def test_position_scalar_warning(self) -> None:
        tracker = DrawdownTracker(warning_threshold_pct=10.0)
        tracker.update(100.0)
        tracker.update(89.0)
        assert tracker.position_scalar() == 0.5

    def test_position_scalar_critical(self) -> None:
        tracker = DrawdownTracker(critical_threshold_pct=20.0)
        tracker.update(100.0)
        tracker.update(79.0)
        assert tracker.position_scalar() == 0.0

    def test_is_in_drawdown(self) -> None:
        tracker = DrawdownTracker()
        assert not tracker.is_in_drawdown
        tracker.update(100.0)
        tracker.update(95.0)
        assert tracker.is_in_drawdown

    def test_bars_in_drawdown_count(self) -> None:
        tracker = DrawdownTracker()
        tracker.update(100.0)
        for _ in range(5):
            tracker.update(99.0)  # no new peak
        assert tracker.bars_in_current_drawdown == 5

    def test_custom_thresholds(self) -> None:
        tracker = DrawdownTracker(warning_threshold_pct=5.0, critical_threshold_pct=10.0)
        tracker.update(100.0)
        assert tracker.update(94.0) == DrawdownLevel.WARNING  # 6% DD
        assert tracker.update(89.0) == DrawdownLevel.CRITICAL  # 11% DD

    def test_zero_equity_no_crash(self) -> None:
        tracker = DrawdownTracker()
        level = tracker.update(0.0)
        # Should not crash; peak remains 0.
        assert isinstance(level, DrawdownLevel)
