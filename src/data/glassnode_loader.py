"""Glassnode API data loader.

Provides a reusable client for fetching crypto market data from Glassnode.
Uses the same authentication pattern as the existing glassnode_btc_etf_flows.py.

Endpoints used:
- /v1/metrics/derivatives/futures_funding_rate_perpetual — perpetual funding rate
- /v1/metrics/market/price_usd_ohlc — OHLC spot price data
- /v1/metrics/market/price_usd_close — spot close price

API reference: https://docs.glassnode.com/basic-api/endpoints/
"""

from __future__ import annotations

import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pandas as pd
import requests


# Default API key — prefers env var, falls back to hardcoded key from user's script.
_DEFAULT_API_KEY = os.getenv("GLASSNODE_API_KEY", "")

BASE_URL = "https://api.glassnode.com"

# Known good endpoints.
ENDPOINTS = {
    "funding_rate": "/v1/metrics/derivatives/futures_funding_rate_perpetual",
    "price_ohlc": "/v1/metrics/market/price_usd_ohlc",
    "price_close": "/v1/metrics/market/price_usd_close",
    "open_interest": "/v1/metrics/derivatives/futures_open_interest_perpetual_sum",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _to_unix(ts: str | datetime | int | float) -> int:
    """Convert a date-like value to Unix seconds (UTC)."""
    if isinstance(ts, (int, float)):
        return int(ts)
    if isinstance(ts, str):
        ts = pd.Timestamp(ts)
    if isinstance(ts, (datetime, pd.Timestamp)):
        return int(ts.replace(tzinfo=timezone.utc).timestamp())
    raise ValueError(f"Unsupported timestamp type: {type(ts)}")


def _fetch_paginated(
    endpoint: str,
    asset: str,
    interval: str,
    start: str | datetime | int,
    end: Optional[str | datetime | int] = None,
    *,
    api_key: str | None = None,
    max_retries: int = 5,
    backoff: float = 1.6,
    chunk_days: int = 90,
) -> pd.DataFrame:
    """Fetch data from a Glassnode endpoint with pagination.

    Glassnode returns at most ~5000 points per request.  For long
    histories we paginate by chunking the time range into *chunk_days*
    slices and concatenating.

    Parameters
    ----------
    endpoint: Full URL path, e.g. ``"/v1/metrics/derivatives/..."``.
    asset: Asset symbol: ``"BTC"``, ``"ETH"``.
    interval: Bar interval: ``"1h"``, ``"24h"``.
    start: Start date (ISO string, datetime, or Unix int).
    end: End date.  Defaults to now.
    api_key: Glassnode API key.  Falls back to env / default.
    max_retries: Retries on 429 / 5xx.
    backoff: Exponential backoff base.
    chunk_days: Days per pagination chunk.

    Returns
    -------
    pd.DataFrame
        Columns: ``[timestamp, value]`` (plus ``asset``, ``interval``).
    """
    key = api_key or _DEFAULT_API_KEY
    if not key:
        raise ValueError(
            "GLASSNODE_API_KEY is not set. "
            "Set it via PowerShell: $env:GLASSNODE_API_KEY = 'your-key', "
            "or add it to the project .env file."
        )
    if end is None:
        end = int(datetime.now(timezone.utc).timestamp())
    else:
        end = _to_unix(end)
    start_unix = _to_unix(start)

    all_frames: list[pd.DataFrame] = []
    chunk_start = start_unix
    chunk_secs = chunk_days * 86400

    while chunk_start < end:
        chunk_end = min(chunk_start + chunk_secs, end)

        params: dict = {
            "api_key": key,
            "a": asset.upper(),
            "i": interval,
            "s": chunk_start,
            "u": chunk_end,
            "f": "json",
            "timestamp_format": "unix",
        }

        data = None
        for attempt in range(1, max_retries + 2):
            try:
                resp = requests.get(BASE_URL + endpoint, params=params, timeout=60)
                if resp.status_code in (429, 500, 502, 503, 504) and attempt <= max_retries:
                    time.sleep(backoff**attempt)
                    continue
                resp.raise_for_status()
                data = resp.json()
                break
            except requests.exceptions.RequestException:
                if attempt <= max_retries:
                    time.sleep(backoff**attempt)
                else:
                    raise

        if data and isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            df = df.rename(columns={"t": "timestamp", "v": "value"})
            # Handle nested OHLC object.
            if "o" in df.columns:
                ohlc_df = pd.json_normalize(df["o"])
                ohlc_df.columns = ["close", "high", "low", "open"]
                df = pd.concat([df[["timestamp"]], ohlc_df], axis=1)
            else:
                df["value"] = df["value"].astype(float)

            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", utc=True)
            df["asset"] = asset.upper()
            df["interval"] = interval
            all_frames.append(df)

        chunk_start = chunk_end
        # Small delay between chunks to be polite.
        if chunk_start < end:
            time.sleep(0.3)

    if not all_frames:
        return pd.DataFrame()

    result = pd.concat(all_frames, ignore_index=True)
    result = result.drop_duplicates(subset=["timestamp"]).sort_values("timestamp")
    result = result.reset_index(drop=True)
    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def fetch_funding_rate(
    asset: str = "BTC",
    interval: str = "1h",
    start: str = "2023-01-01",
    end: Optional[str] = None,
    *,
    api_key: str | None = None,
    chunk_days: int = 90,
) -> pd.DataFrame:
    """Fetch perpetual funding rate history.

    Parameters
    ----------
    asset: ``"BTC"`` or ``"ETH"``.
    interval: ``"1h"`` or ``"24h"``.  Use ``"1h"`` for resampling to 8h.
    start: Start date (ISO string).
    end: End date.  Defaults to now.
    api_key: Glassnode API key override.
    chunk_days: Pagination chunk size in days.

    Returns
    -------
    pd.DataFrame
        Columns: ``[timestamp, funding_rate, asset, interval]``.
    """
    df = _fetch_paginated(
        ENDPOINTS["funding_rate"],
        asset=asset,
        interval=interval,
        start=start,
        end=end,
        api_key=api_key,
        chunk_days=chunk_days,
    )
    if df.empty:
        return df
    df = df.rename(columns={"value": "funding_rate"})
    return df


def fetch_spot_ohlc(
    asset: str = "BTC",
    interval: str = "1h",
    start: str = "2023-01-01",
    end: Optional[str] = None,
    *,
    api_key: str | None = None,
    chunk_days: int = 90,
) -> pd.DataFrame:
    """Fetch spot OHLC price history.

    Parameters
    ----------
    asset: ``"BTC"`` or ``"ETH"``.
    interval: ``"1h"``, ``"24h"``, ``"10m"``.
    start: Start date (ISO string).
    end: End date.  Defaults to now.
    api_key: Glassnode API key override.
    chunk_days: Pagination chunk size in days.

    Returns
    -------
    pd.DataFrame
        Columns: ``[timestamp, open, high, low, close, asset, interval]``.
    """
    df = _fetch_paginated(
        ENDPOINTS["price_ohlc"],
        asset=asset,
        interval=interval,
        start=start,
        end=end,
        api_key=api_key,
        chunk_days=chunk_days,
    )
    return df


def fetch_spot_close(
    asset: str = "BTC",
    interval: str = "1h",
    start: str = "2023-01-01",
    end: Optional[str] = None,
    *,
    api_key: str | None = None,
    chunk_days: int = 90,
) -> pd.DataFrame:
    """Fetch spot close price history.

    Returns
    -------
    pd.DataFrame
        Columns: ``[timestamp, close, asset, interval]``.
    """
    df = _fetch_paginated(
        ENDPOINTS["price_close"],
        asset=asset,
        interval=interval,
        start=start,
        end=end,
        api_key=api_key,
        chunk_days=chunk_days,
    )
    if df.empty:
        return df
    df = df.rename(columns={"value": "close"})
    return df


def fetch_open_interest(
    asset: str = "BTC",
    interval: str = "1h",
    start: str = "2023-01-01",
    end: Optional[str] = None,
    *,
    api_key: str | None = None,
    chunk_days: int = 90,
) -> pd.DataFrame:
    """Fetch perpetual futures open interest.

    Returns
    -------
    pd.DataFrame
        Columns: ``[timestamp, open_interest, asset, interval]``.
    """
    df = _fetch_paginated(
        ENDPOINTS["open_interest"],
        asset=asset,
        interval=interval,
        start=start,
        end=end,
        api_key=api_key,
        chunk_days=chunk_days,
    )
    if df.empty:
        return df
    df = df.rename(columns={"value": "open_interest"})
    return df
