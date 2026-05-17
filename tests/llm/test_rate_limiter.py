"""Tests for RateLimiter."""

import time

import pytest

from src.llm.utils.rate_limiter import RateLimiter


@pytest.fixture
def limiter():
    return RateLimiter({
        "claude": {"requests_per_minute": 3, "enabled": True},
        "deepseek": {"requests_per_minute": 5, "enabled": True},
    })


class TestRateLimiter:
    def test_acquire_allows_up_to_limit(self, limiter):
        for _ in range(3):
            assert limiter.acquire("claude") is True

    def test_acquire_blocks_after_limit(self, limiter):
        for _ in range(3):
            limiter.acquire("claude")
        assert limiter.acquire("claude") is False

    def test_disabled_provider_always_allows(self, limiter):
        for _ in range(20):
            assert limiter.acquire("unknown-provider") is True

    def test_remaining_reports_correct_count(self, limiter):
        limiter.acquire("deepseek")
        assert limiter.remaining("deepseek") == 4
        limiter.acquire("deepseek")
        assert limiter.remaining("deepseek") == 3

    def test_reset_clears_limits(self, limiter):
        for _ in range(3):
            limiter.acquire("claude")
        assert limiter.acquire("claude") is False
        limiter.reset("claude")
        assert limiter.acquire("claude") is True

    def test_reset_all_clears_all(self, limiter):
        for _ in range(3):
            limiter.acquire("claude")
        for _ in range(5):
            limiter.acquire("deepseek")
        limiter.reset()
        assert limiter.acquire("claude") is True
        assert limiter.acquire("deepseek") is True

    def test_disabled_provider_returns_none_remaining(self, limiter):
        assert limiter.remaining("unknown") is None

    def test_not_enabled_in_config(self):
        limiter = RateLimiter({
            "claude": {"requests_per_minute": 10, "enabled": False},
        })
        for _ in range(20):
            assert limiter.acquire("claude") is True
