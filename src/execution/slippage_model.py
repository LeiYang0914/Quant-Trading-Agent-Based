"""Slippage model.

Models expected slippage as a function of trade size relative to volume.
For the MVP, a simple linear-in-notional model is used.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SlippageModel:
    """Simple slippage model.

    Attributes:
        base_bps: Base slippage in basis points for normal-sized trades.
        volume_pct_limit: Maximum trade size as fraction of interval volume
            before slippage increases.
    """

    base_bps: float = 2.0
    volume_pct_limit: float = 0.05  # 5% of interval volume

    def estimate_bps(
        self, notional: float, interval_volume: float | None = None
    ) -> float:
        """Estimate slippage in basis points for a trade.

        Parameters
        ----------
        notional: Trade notional in quote currency.
        interval_volume: Trading volume over the relevant interval (e.g. 8h).
            If None or zero, base_bps is returned.

        Returns
        -------
        Slippage estimate in basis points.
        """
        if interval_volume is None or interval_volume <= 0:
            return self.base_bps

        volume_fraction = notional / interval_volume
        if volume_fraction <= self.volume_pct_limit:
            return self.base_bps
        # Linear increase beyond the limit.
        multiplier = volume_fraction / self.volume_pct_limit
        return self.base_bps * multiplier

    def apply_slippage(
        self,
        price: float,
        notional: float,
        side: str = "buy",
        interval_volume: float | None = None,
    ) -> tuple[float, float]:
        """Apply slippage to an execution price.

        Parameters
        ----------
        price: Mid / reference price.
        notional: Trade notional in quote currency.
        side: 'buy' or 'sell'.
        interval_volume: Relevant interval volume.

        Returns
        -------
        (slippage_bps, executed_price)
        """
        bps = self.estimate_bps(notional, interval_volume)
        if side == "buy":
            executed = price * (1 + bps / 10_000.0)
        else:
            executed = price * (1 - bps / 10_000.0)
        return bps, executed


# Default slippage model: 2 bps base for BTC/ETH size.
DEFAULT_SLIPPAGE_MODEL = SlippageModel()
