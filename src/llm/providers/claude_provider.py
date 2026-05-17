"""Claude (Anthropic) provider.

Reads ANTHROPIC_API_KEY from environment. Model names are configurable via models.yaml.
If the anthropic SDK is not installed, returns a clear configuration error without crashing.
"""

import logging
import os
import time
from typing import Any, Optional

from .base import BaseProvider

logger = logging.getLogger("llm_router.claude")

try:
    import anthropic

    _ANTHROPIC_AVAILABLE = True
except ImportError:
    _ANTHROPIC_AVAILABLE = False
    anthropic = None  # type: ignore


class ClaudeProvider(BaseProvider):
    """Provider for Anthropic Claude models via the Anthropic API."""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.name = "claude"
        self._api_key: Optional[str] = None
        self._client: Optional[Any] = None

    # ------------------------------------------------------------------
    # BaseProvider interface
    # ------------------------------------------------------------------

    @property
    def available_models(self) -> list[str]:
        return self.config.get("models", ["claude-sonnet-4-6", "claude-opus-4-7", "claude-haiku-4-5-20251001"])

    def call(
        self,
        prompt: str,
        model: str,
        max_tokens: int = 4096,
        temperature: float = 0.3,
        timeout_seconds: int = 120,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Call Claude API. Returns dict with success, content, tokens, cost, etc."""
        self._ensure_api_key()

        if not _ANTHROPIC_AVAILABLE:
            return _sdk_missing_result(model, "anthropic")
        if not self._api_key:
            return _api_key_missing_result(model, "ANTHROPIC_API_KEY")
        if not self._client:
            self._client = anthropic.Anthropic(api_key=self._api_key)

        try:
            t0 = time.monotonic()
            message = self._client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
                timeout=timeout_seconds,
            )
            latency_ms = int((time.monotonic() - t0) * 1000)
            latency_s = round(latency_ms / 1000, 3)

            content = _extract_content(message)
            input_tokens = getattr(message, "usage", None)
            if input_tokens is not None:
                in_tok = input_tokens.input_tokens
                out_tok = input_tokens.output_tokens
            else:
                in_tok, out_tok = None, None

            cost_est = self.estimate_cost(prompt, model, max_tokens)

            return {
                "success": True,
                "content": content,
                "error": None,
                "model": model,
                "latency_ms": latency_ms,
                "latency_seconds": latency_s,
                "input_tokens": in_tok,
                "output_tokens": out_tok,
                "estimated_tokens": False,
                "estimated_cost": cost_est.get("estimated_amount"),
            }
        except Exception as exc:
            logger.error("Claude call failed | model=%s error=%s", model, exc)
            return {
                "success": False,
                "content": None,
                "error": f"Claude API error: {exc}",
                "model": model,
                "latency_ms": 0,
                "latency_seconds": 0.0,
                "input_tokens": None,
                "output_tokens": None,
                "estimated_tokens": True,
                "estimated_cost": None,
            }

    def validate_config(self) -> bool:
        self._ensure_api_key()
        return _ANTHROPIC_AVAILABLE and bool(self._api_key)

    def estimate_cost(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
    ) -> dict[str, Any]:
        from ..utils.cost_estimator import estimate_cost

        from ..types import ProviderName

        return estimate_cost(ProviderName.CLAUDE, model, len(prompt), max_tokens)

    def health_check(self) -> bool:
        reasons = []
        if not _ANTHROPIC_AVAILABLE:
            reasons.append("anthropic SDK not installed")
        self._ensure_api_key()
        if not self._api_key:
            reasons.append("ANTHROPIC_API_KEY not set")
        if reasons:
            logger.warning("Claude health check: %s", ", ".join(reasons))
        return self.validate_config()

    def health_details(self) -> dict:
        """Return structured health information."""
        sdk_ok = _ANTHROPIC_AVAILABLE
        self._ensure_api_key()
        key_ok = bool(self._api_key)
        return {
            "available": sdk_ok and key_ok,
            "sdk_installed": sdk_ok,
            "api_key_set": key_ok,
            "reason": (
                "ready"
                if (sdk_ok and key_ok)
                else (
                    "anthropic SDK not installed"
                    if not sdk_ok
                    else "ANTHROPIC_API_KEY not set"
                )
            ),
            "configured_models": self.available_models,
            "default_model": self.config.get("default_model", "claude-sonnet-4-6"),
            "timeout_seconds": self.config.get("timeout_seconds", 120),
        }

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _ensure_api_key(self) -> None:
        if self._api_key is not None:
            return
        self._api_key = os.getenv("ANTHROPIC_API_KEY", "")


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _extract_content(message) -> str:
    """Extract text content from an Anthropic message."""
    if not message or not message.content:
        return ""
    blocks = message.content if isinstance(message.content, list) else [message.content]
    parts = []
    for block in blocks:
        if hasattr(block, "text"):
            parts.append(block.text)
        elif isinstance(block, dict) and "text" in block:
            parts.append(block["text"])
        elif isinstance(block, str):
            parts.append(block)
    return "\n".join(parts)


def _sdk_missing_result(model: str, sdk_name: str) -> dict[str, Any]:
    return {
        "success": False,
        "content": None,
        "error": f"{sdk_name} SDK not installed. Run: pip install {sdk_name}",
        "model": model,
        "latency_ms": 0,
        "latency_seconds": 0.0,
        "input_tokens": None,
        "output_tokens": None,
        "estimated_tokens": True,
        "estimated_cost": None,
    }


def _api_key_missing_result(model: str, env_var: str) -> dict[str, Any]:
    return {
        "success": False,
        "content": None,
        "error": f"{env_var} not set in environment",
        "model": model,
        "latency_ms": 0,
        "latency_seconds": 0.0,
        "input_tokens": None,
        "output_tokens": None,
        "estimated_tokens": True,
        "estimated_cost": None,
    }
