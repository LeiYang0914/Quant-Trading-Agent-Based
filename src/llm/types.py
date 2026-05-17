"""Core types for the LLM Router layer."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class TaskType(str, Enum):
    """Task categories that drive routing decisions."""

    SYSTEM_ARCHITECTURE = "SYSTEM_ARCHITECTURE"
    RESEARCH_REASONING = "RESEARCH_REASONING"
    PAPER_ANALYSIS = "PAPER_ANALYSIS"
    ALPHA_IDEA_GENERATION = "ALPHA_IDEA_GENERATION"
    CODE_PLANNING = "CODE_PLANNING"
    CODE_GENERATION = "CODE_GENERATION"
    CODE_REVIEW = "CODE_REVIEW"
    DEBUGGING = "DEBUGGING"
    DATA_GRABBING = "DATA_GRABBING"
    WEB_SOURCE_SCREENING = "WEB_SOURCE_SCREENING"
    SUMMARIZATION = "SUMMARIZATION"
    TEXT_CLEANUP = "TEXT_CLEANUP"
    GIT_ACTIVITY_SUMMARY = "GIT_ACTIVITY_SUMMARY"
    CLASSIFICATION = "CLASSIFICATION"
    MEMORY_UPDATE = "MEMORY_UPDATE"
    MEMO_WRITING = "MEMO_WRITING"
    RISK_REVIEW = "RISK_REVIEW"
    GENERAL_QA = "GENERAL_QA"


class Domain(str, Enum):
    CRYPTO = "crypto"
    COMMODITIES = "commodities"
    CROSS_MARKET = "cross_market"
    SYSTEM = "system"


class Complexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ProviderName(str, Enum):
    CLAUDE = "claude"
    DEEPSEEK = "deepseek"


@dataclass
class TaskRequest:
    """Request sent by an agent to the LLM Router."""

    task_id: str
    agent_name: str
    task_type: TaskType
    prompt: str
    domain: Domain = Domain.SYSTEM
    complexity: Complexity = Complexity.MEDIUM
    requires_code: bool = False
    requires_long_context: bool = False
    cost_sensitive: bool = False
    timeout_seconds: int = 120
    preferred_provider: Optional[ProviderName] = None
    fallback_allowed: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RoutingDecision:
    """Decision produced by the LLM Router for a given TaskRequest."""

    selected_provider: ProviderName
    selected_model: str
    reason: str
    fallback_provider: Optional[ProviderName] = None
    fallback_model: Optional[str] = None
    estimated_cost_level: str = "unknown"
    max_tokens: int = 4096
    temperature: float = 0.3
    timeout_seconds: int = 120
    cacheable: bool = False


@dataclass
class LLMResponse:
    """Structured response returned to the calling agent."""

    task_id: str
    success: bool
    provider: ProviderName
    model: str
    content: Optional[str] = None
    error: Optional[str] = None
    fallback_used: bool = False
    routing_decision: Optional[RoutingDecision] = None
    latency_ms: Optional[int] = None
    latency_seconds: Optional[float] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    estimated_tokens: bool = False
    estimated_cost: Optional[float] = None
    cache_hit: bool = False
    rate_limited: bool = False
