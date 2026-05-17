"""LLM Router — infrastructure layer for routing agent tasks to LLM providers.

Provides:
- TaskType / TaskRequest / RoutingDecision / LLMResponse types
- LLMRouter: the core routing engine with caching, rate limiting, circuit breaking
- Task classifier heuristics with agent awareness
- Provider implementations (Claude, DeepSeek) with real SDK wiring
- ResponseCache, RateLimiter, CircuitBreaker, UsageTracker utilities
- Routing logging and cost estimation utilities
"""

from .router import LLMRouter
from .types import (
    Complexity,
    Domain,
    LLMResponse,
    ProviderName,
    RoutingDecision,
    TaskRequest,
    TaskType,
)

__all__ = [
    "LLMRouter",
    "TaskType",
    "TaskRequest",
    "RoutingDecision",
    "LLMResponse",
    "Domain",
    "Complexity",
    "ProviderName",
]
