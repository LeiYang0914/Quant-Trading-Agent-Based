# pip install requests pandas python-dateutil
import os
import time
import requests
import pandas as pd
from datetime import datetime, timezone
from dateutil import parser as dtparser

GLASSNODE_API_KEY = os.getenv("GLASSNODE_API_KEY") or "REDACTED_ROTATE_THIS_KEY"

BASE_URL = "https://api.glassnode.com"
ENDPOINT = "/v1/metrics/institutions/purpose_etf_flows_sum"

def to_unix_utc(ts):
    """Accepts 'YYYY-mm-dd' str | datetime | int and returns unix seconds (UTC)."""
    if ts is None:
        return None
    if isinstance(ts, (int, float)):
        return int(ts)
    if isinstance(ts, str):
        ts = dtparser.parse(ts)
    if isinstance(ts, datetime):
        return int(ts.replace(tzinfo=timezone.utc).timestamp())
    raise ValueError("Unsupported timestamp type")

def fetch_purpose_etf_flows(asset="BTC",
                            interval="24h",
                            start="2021-01-01",
                            end=None,
                            max_retries=5,
                            backoff=1.6) -> pd.DataFrame:
    """
    Fetch Purpose Bitcoin ETF flows (sum) from Glassnode.
    Returns DataFrame with columns: time, flow, asset, interval
    """
    if end is None:
        end = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    params = {
        "api_key": GLASSNODE_API_KEY,
        "a": asset.upper(),           # asset code; BTC for Purpose BTC ETF flows
        "i": interval,                # 24h recommended
        "s": to_unix_utc(start),
        "u": to_unix_utc(end),
        "f": "json",
        "timestamp_format": "unix",
    }
    # remove None values
    params = {k: v for k, v in params.items() if v is not None}

    url = BASE_URL + ENDPOINT
    attempt = 0
    while True:
        attempt += 1
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code in (429, 500, 502, 503, 504) and attempt <= max_retries:
            time.sleep(backoff ** attempt)
            continue
        resp.raise_for_status()
        data = resp.json()
        break

    # Expected schema: [{"t": 1694822400, "v": 12345.67}, ...]
    df = pd.DataFrame(data)
    if df.empty:
        return pd.DataFrame(columns=["time", "flow", "asset", "interval"])

    df["time"] = pd.to_datetime(df["t"], unit="s", utc=True)
    df["flow"] = df["v"].astype(float)
    df["asset"] = asset.upper()
    df["interval"] = interval
    df = df[["time", "flow", "asset", "interval"]].sort_values("time").reset_index(drop=True)
    return df

if __name__ == "__main__":
    # Example: all data since 2021-01-01 (Purpose ETF launched in 2021)
    df = fetch_purpose_etf_flows(asset="BTC",
                                 interval="24h",
                                 start="2021-01-01",
                                 end=None)

    print(f"rows: {len(df)}")
    print(df.head(3))
    print(df.tail(3))

    out_name = "glassnode_purpose_etf_flows_sum_BTC_24h_20210101_to_latest.csv"
    df.to_csv(out_name, index=False)
    print(f"Saved -> {out_name}")
