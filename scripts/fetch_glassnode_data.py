"""Fetch Glassnode data for CRYPTO-001 backtest.

Pulls BTC and ETH funding rates + spot OHLCV from Glassnode API
and saves resampled 8h Parquet files for the backtest engine.

Usage:
    PYTHONPATH=. python scripts/fetch_glassnode_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

from src.data.glassnode_loader import fetch_funding_rate, fetch_spot_ohlc

# Output directory.
DATA_DIR = Path("data/glassnode")
START = "2023-01-01"
END = "2025-12-31"
ASSETS = ["BTC", "ETH"]


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for asset in ASSETS:
        print(f"\n{'='*60}")
        print(f"Fetching {asset} data from Glassnode...")
        print(f"{'='*60}")

        # --- Funding Rate ---
        print(f"\n[1/2] {asset} funding rates (1h)...")
        fr_path = DATA_DIR / f"{asset}_funding_rate_1h.parquet"
        if fr_path.exists():
            print(f"  -> Already cached: {fr_path}")
        else:
            try:
                fr = fetch_funding_rate(
                    asset=asset, interval="1h", start=START, end=END
                )
                print(f"  -> Fetched {len(fr):,} rows")
                fr.to_parquet(fr_path)
                print(f"  -> Saved to {fr_path}")
            except Exception as e:
                print(f"  -> ERROR: {e}", file=sys.stderr)

        # --- Spot OHLC ---
        print(f"\n[2/2] {asset} spot OHLC (1h)...")
        ohlc_path = DATA_DIR / f"{asset}_spot_ohlc_1h.parquet"
        if ohlc_path.exists():
            print(f"  -> Already cached: {ohlc_path}")
        else:
            try:
                ohlc = fetch_spot_ohlc(
                    asset=asset, interval="1h", start=START, end=END
                )
                print(f"  -> Fetched {len(ohlc):,} rows")
                ohlc.to_parquet(ohlc_path)
                print(f"  -> Saved to {ohlc_path}")
            except Exception as e:
                print(f"  -> ERROR: {e}", file=sys.stderr)

    # --- Resample to 8h ---
    print(f"\n{'='*60}")
    print("Resampling to 8h frequency...")
    print(f"{'='*60}")

    for asset in ASSETS:
        fr_path = DATA_DIR / f"{asset}_funding_rate_1h.parquet"
        ohlc_path = DATA_DIR / f"{asset}_spot_ohlc_1h.parquet"

        if not fr_path.exists() or not ohlc_path.exists():
            print(f"  -> Skipping {asset}: missing source files")
            continue

        fr = pd.read_parquet(fr_path)
        ohlc = pd.read_parquet(ohlc_path)

        # Resample funding rate: last known rate in each 8h window.
        fr_8h = fr.set_index("timestamp").resample("8h").last().dropna().reset_index()
        fr_8h["asset"] = asset

        # Resample OHLC to 8h.
        ohlc_8h = (
            ohlc.set_index("timestamp")
            .resample("8h")
            .agg({"open": "first", "high": "max", "low": "min", "close": "last"})
            .dropna()
            .reset_index()
        )
        ohlc_8h["asset"] = asset

        # Save 8h files.
        fr_8h_path = DATA_DIR / f"{asset}_funding_rate_8h.parquet"
        ohlc_8h_path = DATA_DIR / f"{asset}_spot_ohlc_8h.parquet"

        fr_8h.to_parquet(fr_8h_path)
        ohlc_8h.to_parquet(ohlc_8h_path)

        print(f"  {asset}: {len(fr_8h):,} funding rows, {len(ohlc_8h):,} OHLC rows "
              f"({ohlc_8h['timestamp'].iloc[0]} -> {ohlc_8h['timestamp'].iloc[-1]})")

    print(f"\nDone. Data in {DATA_DIR.resolve()}/")
    print("Ready for CRYPTO-001 backtest with real data.")


if __name__ == "__main__":
    main()
