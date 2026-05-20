"""Health check service: integrates with LLMRouter.health_check().

Always redacts API key values. Safe to call from the dashboard.
"""

import logging
from typing import Any, Optional

logger = logging.getLogger("dashboard.health")


def get_health(router: Optional[Any] = None) -> dict[str, Any]:
    """Get health status from the router, or return offline status if no router.

    Args:
        router: An LLMRouter instance, or None if not available.

    Returns:
        Dict with claude/deepseek health info. Never exposes API keys.
    """
    if router is None:
        return _offline_health()

    try:
        raw = router.health_check()
    except Exception as exc:
        logger.warning("health_check() raised: %s", exc)
        return _offline_health()

    # Redact any key-like strings just in case
    result: dict[str, Any] = {}
    for provider in ["claude", "deepseek"]:
        info = raw.get(provider, {})
        result[provider] = _sanitize(provider, info)
    return result


def _sanitize(provider: str, info: dict[str, Any]) -> dict[str, Any]:
    """Remove any sensitive fields and redact key-like strings."""
    safe: dict[str, Any] = {
        "provider": provider,
        "available": info.get("available", False),
        "reason": _redact_keys(info.get("reason", "unknown")),
        "configured_models": info.get("configured_models", []),
        "circuit_state": info.get("circuit_state", "unknown"),
        "rate_limit_remaining": info.get("rate_limit_remaining"),
    }
    # Never forward raw API keys
    safe.pop("api_key", None)
    safe.pop("_api_key", None)
    return safe


def _redact_keys(text: str) -> str:
    """Redact any API-key-like substrings from a string."""
    if not isinstance(text, str):
        return str(text)
    # Replace anything that looks like sk-... with [REDACTED]
    import re

    return re.sub(r"(sk-[a-zA-Z0-9_-]{10,})", "[REDACTED]", text)


def _offline_health() -> dict[str, Any]:
    return {
        "claude": {
            "provider": "claude",
            "available": False,
            "reason": "Router not available",
            "configured_models": [],
            "circuit_state": "unknown",
            "rate_limit_remaining": None,
        },
        "deepseek": {
            "provider": "deepseek",
            "available": False,
            "reason": "Router not available",
            "configured_models": [],
            "circuit_state": "unknown",
            "rate_limit_remaining": None,
        },
    }
