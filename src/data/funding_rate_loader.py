"""Funding rate data loader.

Supports loading from:
- Local CSV files (for testing and offline backtests)
- Binance public API (GET /fapi/v1/fundingRate) when available

Loader design: the public interface is ``load_funding_rate_history()``.
All source-specific logic lives behind that function so callers never
need to know whether data came from CSV or API.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

from src.data.schema import FundingRateRecord


# Default fixture path relative to the project root.
DEFAULT_FIXTURE_DIR = Path("tests/fixtures")


def load_funding_rate_history(
    symbol: str = "BTCUSDT",
    *,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    csv_path: Optional[Path] = None,
) -> pd.DataFrame:
    """Load funding rate history for *symbol*.

    If *csv_path* is given the data is read from a local CSV file.
    Otherwise the default fixture path is tried first; if no fixture
    exists the caller receives an empty DataFrame with the correct
    schema columns.

    Parameters
    ----------
    symbol: Trading pair, e.g. ``"BTCUSDT"``.
    start: If set, filter to records with ``funding_time >= start``.
    end: If set, filter to records with ``funding_time < end``.
    csv_path: Explicit path to a CSV file.

    Returns
    -------
    pd.DataFrame
        Columns: ``[funding_time, symbol, funding_rate, mark_price]``.
    """
    # Resolve data source.
    if csv_path is not None:
        path = Path(csv_path)
    else:
        path = DEFAULT_FIXTURE_DIR / f"{symbol}_funding_rate.csv"

    if path.exists():
        df = pd.read_csv(path)
    else:
        # Return empty frame with expected schema so callers don't crash.
        return pd.DataFrame(
            columns=["funding_time", "symbol", "funding_rate", "mark_price"]
        )

    # Normalise columns.
    df = _normalise_funding_df(df, symbol)

    # Filter by date range.
    if "funding_time" in df.columns:
        df["funding_time"] = pd.to_datetime(df["funding_time"])
        if start is not None:
            df = df[df["funding_time"] >= pd.Timestamp(start)]
        if end is not None:
            df = df[df["funding_time"] < pd.Timestamp(end)]
        df = df.sort_values("funding_time").reset_index(drop=True)

    return df


def generate_sample_funding_data(
    symbol: str = "BTCUSDT",
    start_date: str = "2023-01-01",
    periods: int = 360,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate synthetic funding rate data for testing.

    Creates a plausible funding rate series with mild autocorrelation,
    occasional spikes, and a known seed for reproducibility.

    Parameters
    ----------
    symbol: Trading pair label.
    start_date: ISO-format start date.
    periods: Number of 8-hour periods to generate.
    seed: Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        Columns: ``[funding_time, symbol, funding_rate, mark_price]``.
    """
    rng = np.random.default_rng(seed)

    # 3 funding settlements per day (00:00, 08:00, 16:00 UTC).
    start = pd.Timestamp(start_date)
    timestamps = pd.date_range(start=start, periods=periods, freq="8h")

    # Mean funding rate ~0.01% per 8h (0.0001 as decimal), with mild
    # autocorrelation and occasional spikes.
    base_rate = 0.0001
    noise = rng.normal(0, 0.00005, periods)
    # Add occasional spikes to extreme percentiles.
    spike_idx = rng.choice(periods, size=max(1, periods // 30), replace=False)
    spike_vals = rng.choice([0.001, 0.002, 0.003, -0.0005], size=len(spike_idx))

    rates = np.full(periods, base_rate)
    for i in range(1, periods):
        rates[i] = 0.7 * rates[i - 1] + 0.3 * base_rate + noise[i]
    rates[spike_idx] = spike_vals

    # Generate a simple mark price series (starting ~$30,000).
    mark_returns = rng.normal(0.0002, 0.02, periods)
    mark_prices = 30000.0 * np.cumprod(1 + mark_returns)

    df = pd.DataFrame(
        {
            "funding_time": timestamps,
            "symbol": symbol,
            "funding_rate": rates,
            "mark_price": mark_prices,
        }
    )
    return df


def _normalise_funding_df(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """Rename common column variants to the canonical names."""
    column_map = {
        "fundingTime": "funding_time",
        "fundingRate": "funding_rate",
        "markPrice": "mark_price",
        "time": "funding_time",
        "rate": "funding_rate",
    }
    df = df.rename(columns={k: v for k, v in column_map.items() if k in df.columns})
    if "symbol" not in df.columns:
        df["symbol"] = symbol
    return df


# numpy is used inside generate_sample_funding_data — import at module level.
import numpy as np  # noqa: E402
