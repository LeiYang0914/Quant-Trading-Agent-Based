"""Drawdown tracking and risk-limit enforcement.

Monitors peak-to-trough equity drawdown and signals when
pre-configured risk limits are breached.

Reference: ``research/memos/crypto/01_crypto_funding_rate_carry.md`` §9
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class DrawdownLevel(Enum):
    """Risk action levels based on drawdown severity."""

    NORMAL = "normal"
    WARNING = "warning"  # 10% DD → reduce position 50%
    CRITICAL = "critical"  # 20% DD → stop trading


@dataclass
class DrawdownTracker:
    """Track peak-to-trough drawdown and signal risk actions.

    Attributes:
        warning_threshold_pct: Drawdown level triggering a warning (default 10%).
        critical_threshold_pct: Drawdown level triggering a stop (default 20%).
        peak_equity: Running peak of the equity curve.
        current_drawdown_pct: Current drawdown from peak.
    """

    warning_threshold_pct: float = 10.0
    critical_threshold_pct: float = 20.0
    peak_equity: float = 0.0
    current_drawdown_pct: float = 0.0
    _max_drawdown_pct: float = field(default=0.0, init=False)
    _in_drawdown: bool = field(default=False, init=False)
    _bars_in_drawdown: int = field(default=0, init=False)

    def update(self, equity: float) -> DrawdownLevel:
        """Update the tracker with the latest equity value.

        Parameters
        ----------
        equity: Current NAV.

        Returns
        -------
        DrawdownLevel
            The current risk action level.
        """
        if equity > self.peak_equity:
            self.peak_equity = equity
            self._in_drawdown = False
            self._bars_in_drawdown = 0
            self.current_drawdown_pct = 0.0
        else:
            self._in_drawdown = True
            self._bars_in_drawdown += 1
            if self.peak_equity > 0:
                self.current_drawdown_pct = (
                    (self.peak_equity - equity) / self.peak_equity
                ) * 100.0

        self._max_drawdown_pct = max(self._max_drawdown_pct, self.current_drawdown_pct)

        return self.level()

    def level(self) -> DrawdownLevel:
        """Return the current risk action level."""
        if self.current_drawdown_pct >= self.critical_threshold_pct:
            return DrawdownLevel.CRITICAL
        if self.current_drawdown_pct >= self.warning_threshold_pct:
            return DrawdownLevel.WARNING
        return DrawdownLevel.NORMAL

    @property
    def max_drawdown_pct(self) -> float:
        """Maximum drawdown observed so far."""
        return self._max_drawdown_pct

    @property
    def is_in_drawdown(self) -> bool:
        """True if equity is currently below its peak."""
        return self._in_drawdown

    @property
    def bars_in_current_drawdown(self) -> int:
        """Number of bars since the peak was last refreshed."""
        return self._bars_in_drawdown

    def position_scalar(self) -> float:
        """Return a scalar in [0, 1] to multiply positions by.

        Normal → 1.0 (full size).
        Warning → 0.5 (half size).
        Critical → 0.0 (no new positions).
        """
        lvl = self.level()
        if lvl == DrawdownLevel.CRITICAL:
            return 0.0
        if lvl == DrawdownLevel.WARNING:
            return 0.5
        return 1.0
