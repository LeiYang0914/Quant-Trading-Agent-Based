"""Simple time-window rate limiter for LLM providers.

Tracks request timestamps per provider and blocks when the configured
requests-per-minute limit is exceeded.
"""

import logging
import time
from collections import defaultdict
from typing import Any, Optional

logger = logging.getLogger("llm_router.rate_limiter")


class RateLimiter:
    """In-memory sliding-window rate limiter per provider."""

    def __init__(self, config: Optional[dict[str, Any]] = None):
        """
        Args:
            config: e.g. {"claude": {"requests_per_minute": 30, "enabled": true},
                          "deepseek": {"requests_per_minute": 60, "enabled": true}}
        """
        cfg = config or {}
        self._limits: dict[str, int] = {}
        self._enabled: dict[str, bool] = {}
        for provider, pc in cfg.items():
            if isinstance(pc, dict) and pc.get("enabled", True):
                self._limits[provider] = pc.get("requests_per_minute", 60)
                self._enabled[provider] = True
        self._timestamps: dict[str, list[float]] = defaultdict(list)
        self._window_seconds = 60.0

    def acquire(self, provider: str) -> bool:
        """Try to acquire a rate-limit token for the given provider.

        Returns True if the request is allowed, False if rate-limited.
        """
        if not self._enabled.get(provider, False):
            return True

        limit = self._limits.get(provider)
        if limit is None:
            return True

        now = time.monotonic()
        stamps = self._timestamps[provider]

        # Prune timestamps outside the window
        cutoff = now - self._window_seconds
        while stamps and stamps[0] < cutoff:
            stamps.pop(0)

        if len(stamps) >= limit:
            wait = self._window_seconds - (now - stamps[0]) if stamps else 0
            logger.warning(
                "RATE_LIMIT | provider=%s limit=%d/min blocked=1 wait_remaining=%.1fs",
                provider,
                limit,
                wait,
            )
            return False

        stamps.append(now)
        return True

    def remaining(self, provider: str) -> Optional[int]:
        """Return remaining requests allowed in the current window, or None if not enabled."""
        if not self._enabled.get(provider):
            return None
        limit = self._limits.get(provider)
        if limit is None:
            return None
        now = time.monotonic()
        stamps = self._timestamps[provider]
        cutoff = now - self._window_seconds
        while stamps and stamps[0] < cutoff:
            stamps.pop(0)
        return max(0, limit - len(stamps))

    def reset(self, provider: Optional[str] = None) -> None:
        """Reset rate limiter for a specific provider or all providers."""
        if provider:
            self._timestamps.pop(provider, None)
        else:
            self._timestamps.clear()
        logger.info("Rate limiter reset (provider=%s)", provider or "all")
