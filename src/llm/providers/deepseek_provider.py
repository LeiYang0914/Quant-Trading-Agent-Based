"""DeepSeek provider.

Reads DEEPSEEK_API_KEY from environment. Model names are configurable via models.yaml.
Uses OpenAI-compatible API. If the openai SDK is not installed, returns a clear error
without crashing.
"""

import logging
import os
import time
from typing import Any, Optional

from .base import BaseProvider

logger = logging.getLogger("llm_router.deepseek")

try:
    from openai import OpenAI

    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False
    OpenAI = None  # type: ignore


class DeepSeekProvider(BaseProvider):
    """Provider for DeepSeek models via the DeepSeek API (OpenAI-compatible)."""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.name = "deepseek"
        self._api_key: Optional[str] = None
        self._client: Optional[Any] = None

    # ------------------------------------------------------------------
    # BaseProvider interface
    # ------------------------------------------------------------------

    @property
    def available_models(self) -> list[str]:
        return self.config.get("models", ["deepseek-v4-pro", "deepseek-v4-flash"])

    def call(
        self,
        prompt: str,
        model: str,
        max_tokens: int = 4096,
        temperature: float = 0.3,
        timeout_seconds: int = 120,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Call DeepSeek API (OpenAI-compatible)."""
        self._ensure_api_key()

        if not _OPENAI_AVAILABLE:
            return _sdk_missing_result(model, "openai")
        if not self._api_key:
            return _api_key_missing_result(model, "DEEPSEEK_API_KEY")
        if not self._client:
            base_url = self.config.get("base_url", "https://api.deepseek.com")
            self._client = OpenAI(api_key=self._api_key, base_url=base_url)

        try:
            t0 = time.monotonic()
            response = self._client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
                timeout=timeout_seconds,
            )
            latency_ms = int((time.monotonic() - t0) * 1000)
            latency_s = round(latency_ms / 1000, 3)

            choice = response.choices[0] if response.choices else None
            content = choice.message.content if choice else ""
            usage = getattr(response, "usage", None)
            in_tok = usage.prompt_tokens if usage else None
            out_tok = usage.completion_tokens if usage else None

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
                "estimated_tokens": in_tok is None,
                "estimated_cost": cost_est.get("estimated_amount"),
            }
        except Exception as exc:
            logger.error("DeepSeek call failed | model=%s error=%s", model, exc)
            return {
                "success": False,
                "content": None,
                "error": f"DeepSeek API error: {exc}",
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
        return _OPENAI_AVAILABLE and bool(self._api_key)

    def estimate_cost(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
    ) -> dict[str, Any]:
        from ..utils.cost_estimator import estimate_cost

        from ..types import ProviderName

        return estimate_cost(ProviderName.DEEPSEEK, model, len(prompt), max_tokens)

    def health_check(self) -> bool:
        reasons = []
        if not _OPENAI_AVAILABLE:
            reasons.append("openai SDK not installed")
        self._ensure_api_key()
        if not self._api_key:
            reasons.append("DEEPSEEK_API_KEY not set")
        if reasons:
            logger.warning("DeepSeek health check: %s", ", ".join(reasons))
        return self.validate_config()

    def health_details(self) -> dict:
        """Return structured health information."""
        sdk_ok = _OPENAI_AVAILABLE
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
                    "openai SDK not installed"
                    if not sdk_ok
                    else "DEEPSEEK_API_KEY not set"
                )
            ),
            "configured_models": self.available_models,
            "default_model": self.config.get("default_model", "deepseek-v4-flash"),
            "timeout_seconds": self.config.get("timeout_seconds", 60),
        }

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _ensure_api_key(self) -> None:
        if self._api_key is not None:
            return
        self._api_key = os.getenv("DEEPSEEK_API_KEY", "")


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

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
