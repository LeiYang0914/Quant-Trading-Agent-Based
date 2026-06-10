"""CRYPTO-001: Funding Rate Carry and Crowding Signal.

Implements two sub-strategies from the research memo:

* **Carry Harvesting** — delta-neutral long-spot / short-perp position
  that collects positive funding payments when the annualized funding
  rate exceeds a threshold.

* **Crowding Reversal** — contrarian directional signal triggered when
  the current funding rate is in the extreme tails (>= 90th or <= 10th
  percentile) of its trailing 30-day distribution.

**No-lookahead-bias rule:** every signal at timestamp *t* uses only
data that would have been observable *before* or at the close of bar *t*.
The position is entered at the open of bar *t+1*.

Reference: ``research/memos/crypto/01_crypto_funding_rate_carry.md``
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass
class FundingRateCarryConfig:
    """Configurable parameters for the funding rate carry signal.

    Attributes:
        funding_lookback_days: Trailing window in days for percentile
            calculation (default 30).
        funding_threshold_pct: Annualized funding rate threshold below
            which the carry leg stays flat (default 5.0%).
        crowding_upper_pct: Percentile above which the crowding reversal
            triggers a short signal (default 90).
        crowding_lower_pct: Percentile below which the crowding reversal
            triggers a long signal (default 10).
        max_position_pct: Maximum position size as fraction of NAV
            (default 0.20 = 20%).
        rebalance_frequency_hours: How often positions are re-evaluated
            (default 8, aligned with funding settlement).
        dynamic_carry_cap_pct: Annualized rate at which carry position
            reaches full size (default 30.0%).
        fee_rate_bps: Taker fee in basis points (default 4.0).
        slippage_bps: Expected slippage in basis points (default 2.0).
    """

    funding_lookback_days: int = 30
    funding_threshold_pct: float = 5.0
    crowding_upper_pct: float = 90.0
    crowding_lower_pct: float = 10.0
    max_position_pct: float = 0.20
    rebalance_frequency_hours: int = 8
    dynamic_carry_cap_pct: float = 30.0
    fee_rate_bps: float = 4.0
    slippage_bps: float = 2.0


# ---------------------------------------------------------------------------
# Signal output type
# ---------------------------------------------------------------------------


@dataclass
class SignalResult:
    """Output of one signal evaluation.

    Attributes:
        timestamp: The decision timestamp (bar close).
        carry_weight: Position weight for the delta-neutral carry leg.
            Positive = long spot / short perp.
        crowding_signal: Directional signal from the crowding reversal.
            -1 = short, 0 = neutral, +1 = long.
        funding_rate: Raw 8h funding rate at decision time.
        funding_percentile: Percentile rank of the current rate.
        annualized_fr_pct: Annualized funding rate as a percentage.
        spot_price: Spot close price.
    """

    timestamp: pd.Timestamp
    carry_weight: float
    crowding_signal: int
    funding_rate: float
    funding_percentile: float
    annualized_fr_pct: float
    spot_price: float


# ---------------------------------------------------------------------------
# Signal computer
# ---------------------------------------------------------------------------


class FundingRateCarrySignal:
    """Compute CRYPTO-001 signals from aligned market data.

    Usage::

        config = FundingRateCarryConfig()
        signal = FundingRateCarrySignal(config)
        results = signal.compute(merged_data)
    """

    def __init__(self, config: FundingRateCarryConfig | None = None) -> None:
        self.config = config or FundingRateCarryConfig()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def compute(self, data: pd.DataFrame) -> list[SignalResult]:
        """Compute signals for every row of *data*.

        Parameters
        ----------
        data: DataFrame with columns:
            - ``timestamp`` (datetime)
            - ``funding_rate`` (float, raw 8h rate as decimal)
            - ``spot_price`` (float, close)
            - optionally ``mark_price``, ``basis_pct``

        Returns
        -------
        list[SignalResult]
            One result per row.  The signal is timestamped at bar *close*
            and intended for execution at the *next* bar open.
        """
        if data.empty:
            return []

        df = data.copy()
        df = df.sort_values("timestamp").reset_index(drop=True)

        # Derived columns.
        df["annualized_fr_pct"] = self._annualize(df["funding_rate"])
        df["funding_percentile"] = self._rolling_percentile(df["funding_rate"])

        results: list[SignalResult] = []
        for _, row in df.iterrows():
            carry_w = self._carry_weight(row["annualized_fr_pct"])
            crowd_s = self._crowding_signal(row["funding_percentile"])

            results.append(
                SignalResult(
                    timestamp=row["timestamp"],
                    carry_weight=carry_w,
                    crowding_signal=crowd_s,
                    funding_rate=float(row["funding_rate"]),
                    funding_percentile=float(row["funding_percentile"]),
                    annualized_fr_pct=float(row["annualized_fr_pct"]),
                    spot_price=float(row["spot_price"]),
                )
            )

        return results

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _annualize(self, rates: pd.Series) -> pd.Series:
        """Convert raw 8h decimal rate to annualized percentage.

        annualized_fr_pct = funding_rate_8h * 3 * 365 * 100
        """
        return rates * 3.0 * 365.0 * 100.0

    def _rolling_percentile(self, rates: pd.Series) -> pd.Series:
        """Compute rolling percentile rank within the lookback window.

        Uses ``expanding().rank(pct=True)`` for the first *lookback*
        observations and then a rolling window thereafter.  At each point
        *t* only data up to and including *t* is used — no lookahead.
        """
        window = self.config.funding_lookback_days * 3  # 3 observations/day
        if len(rates) == 0:
            return pd.Series(dtype=float)

        # Compute percentile within trailing window.
        # pandas .rolling() does NOT support rank(), so we use a manual
        # expanding + rolling implementation.
        result = pd.Series(np.nan, index=rates.index, dtype=float)
        for i in range(len(rates)):
            start = max(0, i - window + 1)
            window_data = rates.iloc[start : i + 1]
            # Percentile rank: fraction of values <= current value.
            rank = (window_data <= rates.iloc[i]).mean()
            result.iloc[i] = rank * 100.0  # as 0-100 scale
        return result

    def _carry_weight(self, annualized_fr_pct: float) -> float:
        """Scale carry position by annualized funding rate.

        Weight = 0 when |rate| < funding_threshold_pct.
        Weight ramps linearly from 0 to ±1.0 between threshold and cap.
        """
        cfg = self.config
        t = cfg.funding_threshold_pct
        cap = cfg.dynamic_carry_cap_pct
        if cap <= t:
            return 0.0

        abs_rate = abs(annualized_fr_pct)
        if abs_rate <= t:
            return 0.0

        weight = min(1.0, (abs_rate - t) / (cap - t))
        weight = min(weight, cfg.max_position_pct * 5.0)  # scale for carry (100% NAV)
        return weight if annualized_fr_pct > 0 else -weight

    def _crowding_signal(self, percentile: float) -> int:
        """Map percentile to crowding signal.

        percentile >= crowding_upper_pct  → short (-1)
        percentile <= crowding_lower_pct  → long  (+1)
        otherwise                         → neutral (0)
        """
        if pd.isna(percentile):
            return 0
        if percentile >= self.config.crowding_upper_pct:
            return -1  # crowded longs → fade with short
        if percentile <= self.config.crowding_lower_pct:
            return 1  # crowded shorts → fade with long
        return 0


# ---------------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------------


def compute_signals(
    data: pd.DataFrame,
    config: FundingRateCarryConfig | None = None,
) -> pd.DataFrame:
    """Compute CRYPTO-001 signals and return a DataFrame.

    Convenience wrapper around ``FundingRateCarrySignal``.
    """
    engine = FundingRateCarrySignal(config)
    results = engine.compute(data)
    if not results:
        return pd.DataFrame()
    return pd.DataFrame(
        [
            {
                "timestamp": r.timestamp,
                "carry_weight": r.carry_weight,
                "crowding_signal": r.crowding_signal,
                "funding_rate": r.funding_rate,
                "funding_percentile": r.funding_percentile,
                "annualized_fr_pct": r.annualized_fr_pct,
                "spot_price": r.spot_price,
            }
            for r in results
        ]
    )
