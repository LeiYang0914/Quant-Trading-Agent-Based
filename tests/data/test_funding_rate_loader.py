"""Tests for funding_rate_loader.py"""

from pathlib import Path

import pandas as pd
import pytest

from src.data.funding_rate_loader import (
    DEFAULT_FIXTURE_DIR,
    generate_sample_funding_data,
    load_funding_rate_history,
)


class TestLoadFundingRateHistory:
    """Test loading funding rate data from CSV."""

    def test_load_from_fixture(self) -> None:
        """Should load BTCUSDT funding rate from default fixture."""
        df = load_funding_rate_history("BTCUSDT")
        assert not df.empty
        assert "funding_time" in df.columns
        assert "funding_rate" in df.columns
        assert "symbol" in df.columns
        assert len(df) > 0

    def test_load_missing_symbol_returns_empty(self) -> None:
        """Should return empty DataFrame for missing symbols."""
        df = load_funding_rate_history("NONEXIST")
        assert df.empty

    def test_load_with_date_filter(self) -> None:
        """Should filter by start/end dates."""
        df = load_funding_rate_history("BTCUSDT")
        start = df["funding_time"].min()
        end = df["funding_time"].max()
        filtered = load_funding_rate_history("BTCUSDT", start=start, end=end)
        assert len(filtered) <= len(df)

    def test_load_with_explicit_csv_path(self) -> None:
        """Should load from explicit path."""
        path = DEFAULT_FIXTURE_DIR / "BTCUSDT_funding_rate.csv"
        if path.exists():
            df = load_funding_rate_history("BTCUSDT", csv_path=path)
            assert not df.empty

    def test_columns_match_schema(self) -> None:
        """All returned columns should match the expected schema."""
        df = load_funding_rate_history("BTCUSDT")
        expected_cols = {"funding_time", "symbol", "funding_rate", "mark_price"}
        assert expected_cols.issubset(set(df.columns))


class TestGenerateSampleFundingData:
    """Test synthetic data generation."""

    def test_generates_correct_length(self) -> None:
        df = generate_sample_funding_data(periods=100)
        assert len(df) == 100

    def test_generates_correct_columns(self) -> None:
        df = generate_sample_funding_data()
        assert "funding_time" in df.columns
        assert "funding_rate" in df.columns
        assert "symbol" in df.columns

    def test_seed_reproducibility(self) -> None:
        df1 = generate_sample_funding_data(seed=42)
        df2 = generate_sample_funding_data(seed=42)
        pd.testing.assert_series_equal(df1["funding_rate"], df2["funding_rate"])

    def test_different_seeds_different(self) -> None:
        df1 = generate_sample_funding_data(seed=42)
        df2 = generate_sample_funding_data(seed=123)
        assert not df1["funding_rate"].equals(df2["funding_rate"])

    def test_funding_rates_have_spikes(self) -> None:
        """At least one rate should be an extreme value due to synthetic spikes."""
        df = generate_sample_funding_data(periods=360)
        max_rate = df["funding_rate"].max()
        # Some rate should exceed 0.0005 (0.05%) due to spikes.
        assert max_rate > 0.0005

    def test_eth_symbol(self) -> None:
        df = generate_sample_funding_data("ETHUSDT")
        assert (df["symbol"] == "ETHUSDT").all()

    def test_mark_price_positive(self) -> None:
        df = generate_sample_funding_data()
        assert (df["mark_price"] > 0).all()
