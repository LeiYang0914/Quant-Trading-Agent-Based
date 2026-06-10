"""Data schemas for the quant trading system.

Defines the canonical record types used throughout the pipeline:
funding rate snapshots, OHLCV bars, and combined market data bundles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd


@dataclass
class FundingRateRecord:
    """A single funding rate settlement record.

    Attributes:
        symbol: Trading pair, e.g. 'BTCUSDT'.
        funding_rate: Raw per-8h funding rate (as a decimal, e.g. 0.0001 = 0.01%).
        funding_time: Timestamp of the funding settlement (UTC).
        mark_price: Mark price at settlement time, if available.
    """

    symbol: str
    funding_rate: float
    funding_time: datetime
    mark_price: Optional[float] = None


@dataclass
class OHLCVRecord:
    """A single OHLCV bar.

    Attributes:
        symbol: Trading pair.
        timestamp: Bar open timestamp (UTC).
        open: Open price.
        high: High price.
        low: Low price.
        close: Close price.
        volume: Volume in base currency.
    """

    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class MarketDataBundle:
    """Combined market data for a single timestamp, ready for signal evaluation.

    This is the canonical input to any signal function.  Every field that
    could leak future information must be timestamp-aligned so the signal
    never sees data that would not have been available at decision time.

    Attributes:
        timestamp: The decision timestamp (bar close time).
        symbol: Trading pair.
        funding_rate: Most recent 8h funding rate (settled BEFORE this timestamp).
        funding_rate_percentile: Rolling percentile rank of the funding rate
            within the trailing lookback window.
        annualized_funding_rate_pct: Annualized funding rate as a percentage.
        spot_price: Spot close price at this timestamp.
        mark_price: Perpetual mark price at this timestamp.
        basis_pct: (mark_price - spot_price) / spot_price * 100.
        open_interest: Open interest in USD, if available.
    """

    timestamp: datetime
    symbol: str
    funding_rate: float
    funding_rate_percentile: float
    annualized_funding_rate_pct: float
    spot_price: float
    mark_price: float = 0.0
    basis_pct: float = 0.0
    open_interest: Optional[float] = None


def funding_records_to_dataframe(records: list[FundingRateRecord]) -> pd.DataFrame:
    """Convert a list of FundingRateRecord to a sorted DataFrame."""
    df = pd.DataFrame(
        [
            {
                "funding_time": r.funding_time,
                "symbol": r.symbol,
                "funding_rate": r.funding_rate,
                "mark_price": r.mark_price,
            }
            for r in records
        ]
    )
    if df.empty:
        return df
    df["funding_time"] = pd.to_datetime(df["funding_time"])
    return df.sort_values("funding_time").reset_index(drop=True)


def ohlcv_records_to_dataframe(records: list[OHLCVRecord]) -> pd.DataFrame:
    """Convert a list of OHLCVRecord to a sorted DataFrame."""
    df = pd.DataFrame(
        [
            {
                "timestamp": r.timestamp,
                "symbol": r.symbol,
                "open": r.open,
                "high": r.high,
                "low": r.low,
                "close": r.close,
                "volume": r.volume,
            }
            for r in records
        ]
    )
    if df.empty:
        return df
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df.sort_values("timestamp").reset_index(drop=True)
