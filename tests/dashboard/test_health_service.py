"""Tests for dashboard backend health_service module."""

import pytest

from src.dashboard.backend.health_service import get_health, _sanitize, _redact_keys, _offline_health


class TestGetHealth:
    def test_offline_when_router_is_none(self):
        result = get_health(None)
        assert result["claude"]["available"] is False
        assert result["deepseek"]["available"] is False
        assert result["claude"]["reason"] == "Router not available"

    def test_offline_when_router_raises(self):
        class BrokenRouter:
            def health_check(self):
                raise RuntimeError("boom")

        result = get_health(BrokenRouter())
        assert result["claude"]["available"] is False


class TestSanitize:
    def test_redacts_sk_keys_in_reason(self):
        info = {"available": True, "reason": "ready", "configured_models": ["claude-sonnet-4-6"]}
        safe = _sanitize("claude", info)
        assert safe["available"] is True
        assert safe["reason"] == "ready"
        assert safe["configured_models"] == ["claude-sonnet-4-6"]

    def test_strips_api_key_fields(self):
        info = {"available": True, "api_key": "sk-ant-secret123", "reason": "ready"}
        safe = _sanitize("claude", info)
        assert "api_key" not in safe
        assert "_api_key" not in safe

    def test_sanitize_does_not_expose_keys(self):
        info = {"available": True, "reason": "missing API_KEY ANTHROPIC_API_KEY", "api_key": "sk-ant-abc123xyz098"}
        safe = _sanitize("claude", info)
        assert "sk-ant-abc123" not in str(safe)
        assert "api_key" not in safe


class TestRedactKeys:
    def test_redacts_sk_prefix_keys(self):
        assert _redact_keys("key is sk-ant-secret123key here") == "key is [REDACTED] here"
        assert _redact_keys("using sk-deepseek-key12345") == "using [REDACTED]"

    def test_does_not_redact_short_sk_strings(self):
        text = "sk-short"
        assert _redact_keys(text) == "sk-short"

    def test_handles_non_string_input(self):
        assert _redact_keys(42) == "42"
        assert _redact_keys(None) == "None"


class TestOfflineHealth:
    def test_returns_expected_structure(self):
        result = _offline_health()
        assert "claude" in result
        assert "deepseek" in result
        for key in ["claude", "deepseek"]:
            assert result[key]["available"] is False
            assert result[key]["reason"] == "Router not available"
            assert result[key]["configured_models"] == []
            assert result[key]["circuit_state"] == "unknown"
            assert result[key]["rate_limit_remaining"] is None
