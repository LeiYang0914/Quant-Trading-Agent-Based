"""OHLCV data loader.

Supports loading from local CSV files and can be extended to pull from
exchange APIs.  The public interface is ``load_ohlcv_history()``.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


DEFAULT_FIXTURE_DIR = Path("tests/fixtures")


def load_ohlcv_history(
    symbol: str = "BTCUSDT",
    *,
    interval: str = "8h",
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    csv_path: Optional[Path] = None,
) -> pd.DataFrame:
    """Load OHLCV history for *symbol*.

    If *csv_path* is given the data is read from a local CSV file.
    Otherwise the default fixture path is tried first.

    Parameters
    ----------
    symbol: Trading pair, e.g. ``"BTCUSDT"``.
    interval: Bar interval (``"8h"``, ``"1h"``, ``"1d"``).
    start: If set, filter to bars with ``timestamp >= start``.
    end: If set, filter to bars with ``timestamp < end``.
    csv_path: Explicit path to a CSV file.

    Returns
    -------
    pd.DataFrame
        Columns: ``[timestamp, symbol, open, high, low, close, volume]``.
    """
    if csv_path is not None:
        path = Path(csv_path)
    else:
        path = DEFAULT_FIXTURE_DIR / f"{symbol}_ohlcv_{interval}.csv"

    if path.exists():
        df = pd.read_csv(path)
    else:
        return pd.DataFrame(
            columns=["timestamp", "symbol", "open", "high", "low", "close", "volume"]
        )

    df = _normalise_ohlcv_df(df, symbol)

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        if start is not None:
            df = df[df["timestamp"] >= pd.Timestamp(start)]
        if end is not None:
            df = df[df["timestamp"] < pd.Timestamp(end)]
        df = df.sort_values("timestamp").reset_index(drop=True)

    return df


def generate_sample_ohlcv_data(
    symbol: str = "BTCUSDT",
    start_date: str = "2023-01-01",
    periods: int = 360,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate synthetic OHLCV data for testing.

    Parameters
    ----------
    symbol: Trading pair label.
    start_date: ISO-format start date.
    periods: Number of 8-hour bars to generate.
    seed: Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        Columns: ``[timestamp, symbol, open, high, low, close, volume]``.
    """
    rng = np.random.default_rng(seed)

    start = pd.Timestamp(start_date)
    timestamps = pd.date_range(start=start, periods=periods, freq="8h")

    # Geometric Brownian motion with drift ~10% pa and vol ~60% pa.
    annual_drift = 0.10
    annual_vol = 0.60
    dt = 8 / (365 * 24)  # 8h fraction of a year.
    mu = annual_drift * dt
    sigma = annual_vol * np.sqrt(dt)

    returns = rng.normal(mu, sigma, periods)
    closes = 30000.0 * np.cumprod(1 + returns)

    # Generate OHLC around close.
    intra_noise = rng.normal(0, sigma * 0.5, periods)
    opens = np.concatenate([[closes[0] * (1 + intra_noise[0])], closes[:-1] * (1 + intra_noise[1:])])
    highs = np.maximum(opens, closes) * (1 + np.abs(rng.normal(0, sigma * 0.3, periods)))
    lows = np.minimum(opens, closes) * (1 - np.abs(rng.normal(0, sigma * 0.3, periods)))

    volumes = rng.lognormal(mean=np.log(5000), sigma=0.6, size=periods)

    df = pd.DataFrame(
        {
            "timestamp": timestamps,
            "symbol": symbol,
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes,
        }
    )
    return df


def _normalise_ohlcv_df(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """Rename common column variants to canonical names."""
    column_map = {
        "time": "timestamp",
        "open_time": "timestamp",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
    }
    df = df.rename(columns={k: v for k, v in column_map.items() if k in df.columns})
    if "symbol" not in df.columns:
        df["symbol"] = symbol
    return df
