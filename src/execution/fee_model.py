"""Transaction fee model.

Models exchange trading fees with separate maker/taker rates.
Default values match Binance standard fee tier.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class FeeModel:
    """Exchange fee schedule.

    Attributes:
        maker_bps: Maker fee in basis points (1 bp = 0.01%).
        taker_bps: Taker fee in basis points.
    """

    maker_bps: float = 2.0
    taker_bps: float = 4.0

    def fee_bps(self, is_taker: bool = True) -> float:
        """Return the applicable fee in basis points."""
        return self.taker_bps if is_taker else self.maker_bps

    def apply_fee(
        self, notional: float, is_taker: bool = True
    ) -> tuple[float, float]:
        """Calculate fee on a trade.

        Parameters
        ----------
        notional: Trade notional in quote currency.
        is_taker: True for taker orders, False for maker.

        Returns
        -------
        (fee_amount, notional_after_fee)
            fee_amount is the absolute fee deducted.
            notional_after_fee is the net amount after fee.
        """
        rate_bps = self.fee_bps(is_taker)
        fee = notional * rate_bps / 10_000.0
        return fee, notional - fee

    def round_trip_bps(self) -> float:
        """Round-trip cost in basis points (taker entry + taker exit)."""
        return self.taker_bps * 2


# Default fee model using Binance standard tier (taker 4 bps).
DEFAULT_FEE_MODEL = FeeModel()
