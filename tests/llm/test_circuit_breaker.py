"""Tests for CircuitBreaker."""

import pytest

from src.llm.utils.circuit_breaker import (
    CIRCUIT_CLOSED,
    CIRCUIT_HALF_OPEN,
    CIRCUIT_OPEN,
    CircuitBreaker,
)


@pytest.fixture
def breaker():
    return CircuitBreaker({
        "enabled": True,
        "failure_threshold": 3,
        "cooldown_seconds": 300,
        "half_open_max_requests": 1,
    })


class TestCircuitBreakerNormal:
    def test_initially_closed(self, breaker):
        assert breaker.get_state("claude") == CIRCUIT_CLOSED
        assert breaker.allow_request("claude") is True

    def test_single_failure_keeps_closed(self, breaker):
        breaker.record_failure("claude")
        assert breaker.get_state("claude") == CIRCUIT_CLOSED
        assert breaker.allow_request("claude") is True

    def test_threshold_failures_opens_circuit(self, breaker):
        for _ in range(3):
            breaker.record_failure("claude")
        assert breaker.get_state("claude") == CIRCUIT_OPEN
        assert breaker.allow_request("claude") is False

    def test_success_resets_failures(self, breaker):
        breaker.record_failure("claude")
        breaker.record_failure("claude")
        breaker.record_success("claude")
        breaker.record_failure("claude")
        breaker.record_failure("claude")
        assert breaker.get_state("claude") == CIRCUIT_CLOSED

    def test_record_success_on_closed_is_noop(self, breaker):
        breaker.record_success("claude")
        assert breaker.get_state("claude") == CIRCUIT_CLOSED

    def test_is_available_false_when_open(self, breaker):
        for _ in range(3):
            breaker.record_failure("claude")
        assert breaker.is_available("claude") is False

    def test_reset_clears_state(self, breaker):
        for _ in range(3):
            breaker.record_failure("claude")
        breaker.reset("claude")
        assert breaker.get_state("claude") == CIRCUIT_CLOSED
        assert breaker.allow_request("claude") is True


class TestCircuitBreakerHalfOpen:
    def test_cooldown_transitions_to_half_open(self, breaker):
        breaker = CircuitBreaker({
            "enabled": True,
            "failure_threshold": 3,
            "cooldown_seconds": -1,  # Already elapsed
            "half_open_max_requests": 1,
        })
        for _ in range(3):
            breaker.record_failure("claude")
        assert breaker.get_state("claude") == CIRCUIT_OPEN
        # Next request should transition to half-open because cooldown elapsed
        assert breaker.allow_request("claude") is True
        assert breaker.get_state("claude") == CIRCUIT_HALF_OPEN

    def test_success_in_half_open_closes(self, breaker):
        breaker = CircuitBreaker({
            "enabled": True,
            "failure_threshold": 3,
            "cooldown_seconds": -1,
            "half_open_max_requests": 1,
        })
        for _ in range(3):
            breaker.record_failure("claude")
        breaker.allow_request("claude")  # transition to half-open
        breaker.record_success("claude")  # test call succeeds
        assert breaker.get_state("claude") == CIRCUIT_CLOSED

    def test_failure_in_half_open_reopens(self, breaker):
        breaker = CircuitBreaker({
            "enabled": True,
            "failure_threshold": 3,
            "cooldown_seconds": -1,
            "half_open_max_requests": 1,
        })
        for _ in range(3):
            breaker.record_failure("claude")
        breaker.allow_request("claude")  # transition to half-open
        breaker.record_failure("claude")  # test call fails
        assert breaker.get_state("claude") == CIRCUIT_OPEN


class TestCircuitBreakerDisabled:
    def test_disabled_always_allows(self):
        breaker = CircuitBreaker({"enabled": False})
        for _ in range(10):
            breaker.record_failure("claude")
        assert breaker.allow_request("claude") is True
        assert breaker.get_state("claude") == CIRCUIT_CLOSED
