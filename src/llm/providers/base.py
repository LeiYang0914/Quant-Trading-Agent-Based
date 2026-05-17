"""Abstract base class for LLM providers."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseProvider(ABC):
    """Interface that all LLM providers must implement."""

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.name: str = "base"

    @property
    @abstractmethod
    def available_models(self) -> list[str]:
        """Return the list of model names available for this provider."""

    @abstractmethod
    def call(
        self,
        prompt: str,
        model: str,
        max_tokens: int = 4096,
        temperature: float = 0.3,
        timeout_seconds: int = 120,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Invoke the provider with the given parameters.

        Returns a dict with keys: success (bool), content (str | None),
        error (str | None), model (str), latency_ms (int).
        """

    @abstractmethod
    def validate_config(self) -> bool:
        """Check that required configuration and API keys are present."""

    @abstractmethod
    def estimate_cost(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
    ) -> dict[str, Any]:
        """Return a cost estimate dict with keys: level (str), currency (str),
        estimated_amount (float | None), note (str).
        """

    @abstractmethod
    def health_check(self) -> bool:
        """Return True if the provider is reachable and configured correctly."""

    def resolve_model(self, requested: Optional[str] = None) -> str:
        """Resolve a model name, falling back to the configured default."""
        if requested and requested in self.available_models:
            return requested
        return self.config.get("default_model", self.available_models[0])
