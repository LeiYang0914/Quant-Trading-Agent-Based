"""Position sizing rules.

Determines maximum trade notional based on NAV, risk limits, and
liquidity constraints.

Reference: ``research/memos/crypto/01_crypto_funding_rate_carry.md`` §8
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PositionSizer:
    """Compute position sizes that respect risk limits.

    Attributes:
        max_notional_pct: Maximum notional as fraction of NAV (default 0.20).
        max_leverage: Maximum gross leverage (default 2.0).
        risk_per_trade_pct: Max NAV loss per trade as percentage (default 1.0).
        atr_multiple: Multiplier on ATR for stop-loss distance.
        min_volume_ratio: Minimum ratio of trade notional to interval volume.
    """

    max_notional_pct: float = 0.20
    max_leverage: float = 2.0
    risk_per_trade_pct: float = 1.0
    atr_multiple: float = 2.0
    min_volume_ratio: float = 0.05

    def size_position(
        self,
        nav: float,
        price: float,
        *,
        atr: float | None = None,
        interval_volume: float | None = None,
    ) -> float:
        """Return the maximum notional for a single trade.

        Parameters
        ----------
        nav: Current net asset value.
        price: Current instrument price.
        atr: Average true range (for volatility-based sizing).
        interval_volume: Recent interval volume in quote currency.

        Returns
        -------
        Max notional in quote currency.
        """
        if nav <= 0 or price <= 0:
            return 0.0

        # Rule 1: percent-of-NAV cap.
        notional = nav * self.max_notional_pct

        # Rule 2: leverage cap (total gross exposure ≤ max_leverage × NAV).
        max_by_leverage = nav * self.max_leverage
        notional = min(notional, max_by_leverage)

        # Rule 3: volatility-based sizing (1 ATR move ≤ risk_per_trade_pct).
        if atr is not None and atr > 0:
            risk_amount = nav * self.risk_per_trade_pct / 100.0
            units_from_risk = risk_amount / (self.atr_multiple * atr)
            risk_notional = units_from_risk * price
            notional = min(notional, risk_notional)

        # Rule 4: liquidity constraint.
        if interval_volume is not None and interval_volume > 0:
            liquidity_notional = interval_volume * self.min_volume_ratio
            notional = min(notional, liquidity_notional)

        return max(notional, 0.0)

    def units_from_notional(self, notional: float, price: float) -> float:
        """Convert notional to asset units."""
        if price <= 0:
            return 0.0
        return notional / price
