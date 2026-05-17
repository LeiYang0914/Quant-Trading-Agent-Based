"""Circuit breaker for LLM providers.

Tracks consecutive failures per provider. Opens the circuit after N failures,
preventing further calls for a configurable cooldown period.
"""

import logging
import time
from typing import Any, Optional

logger = logging.getLogger("llm_router.circuit_breaker")

CIRCUIT_CLOSED = "closed"
CIRCUIT_OPEN = "open"
CIRCUIT_HALF_OPEN = "half_open"


class CircuitBreaker:
    """Tracks provider health and prevents calls to failing providers."""

    def __init__(self, config: Optional[dict[str, Any]] = None):
        """
        Args:
            config: e.g. {"enabled": true, "failure_threshold": 3,
                          "cooldown_seconds": 300, "half_open_max_requests": 1}
        """
        cfg = config or {}
        self.enabled = cfg.get("enabled", True)
        self.failure_threshold = cfg.get("failure_threshold", 3)
        self.cooldown_seconds = cfg.get("cooldown_seconds", 300)
        self.half_open_max_requests = cfg.get("half_open_max_requests", 1)

        self._failures: dict[str, int] = {}
        self._state: dict[str, str] = {}          # provider → closed/open/half_open
        self._opened_at: dict[str, float] = {}    # provider → timestamp
        self._half_open_count: dict[str, int] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def allow_request(self, provider: str) -> bool:
        """Check if a request to this provider should be allowed."""
        if not self.enabled:
            return True

        state = self._state.get(provider, CIRCUIT_CLOSED)

        if state == CIRCUIT_CLOSED:
            return True

        if state == CIRCUIT_OPEN:
            if self._cooldown_elapsed(provider):
                self._transition(provider, CIRCUIT_HALF_OPEN)
                logger.info("CIRCUIT | %s: open → half-open (cooldown elapsed)", provider)
                return True
            logger.warning("CIRCUIT | %s: open — request blocked", provider)
            return False

        # half-open: allow limited requests
        count = self._half_open_count.get(provider, 0)
        if count < self.half_open_max_requests:
            self._half_open_count[provider] = count + 1
            return True
        return False

    def record_success(self, provider: str) -> None:
        """Record a successful call — reset the circuit."""
        if not self.enabled:
            return
        self._failures[provider] = 0
        if self._state.get(provider) == CIRCUIT_HALF_OPEN:
            self._transition(provider, CIRCUIT_CLOSED)
            logger.info("CIRCUIT | %s: half-open → closed (success)", provider)
        self._half_open_count[provider] = 0

    def record_failure(self, provider: str) -> None:
        """Record a failed call — increment failure counter and maybe open circuit."""
        if not self.enabled:
            return
        self._failures[provider] = self._failures.get(provider, 0) + 1
        count = self._failures[provider]

        if count >= self.failure_threshold:
            self._transition(provider, CIRCUIT_OPEN)
            logger.warning(
                "CIRCUIT | %s: closed → open (%d consecutive failures)",
                provider,
                count,
            )

    def get_state(self, provider: str) -> str:
        """Return the current circuit state for a provider."""
        return self._state.get(provider, CIRCUIT_CLOSED)

    def is_available(self, provider: str) -> bool:
        """Return True if the provider is NOT in open state."""
        return self._state.get(provider, CIRCUIT_CLOSED) != CIRCUIT_OPEN or self._cooldown_elapsed(provider)

    def reset(self, provider: Optional[str] = None) -> None:
        """Reset circuit breaker state."""
        if provider:
            self._failures.pop(provider, None)
            self._state.pop(provider, None)
            self._opened_at.pop(provider, None)
            self._half_open_count.pop(provider, None)
        else:
            self._failures.clear()
            self._state.clear()
            self._opened_at.clear()
            self._half_open_count.clear()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _cooldown_elapsed(self, provider: str) -> bool:
        opened = self._opened_at.get(provider, 0)
        return (time.time() - opened) >= self.cooldown_seconds

    def _transition(self, provider: str, new_state: str) -> None:
        self._state[provider] = new_state
        if new_state == CIRCUIT_OPEN:
            self._opened_at[provider] = time.time()
        if new_state == CIRCUIT_HALF_OPEN:
            self._half_open_count[provider] = 0
