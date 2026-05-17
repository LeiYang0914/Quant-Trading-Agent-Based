"""Task classification heuristics for the LLM Router.

Produces a TaskType from free-text task descriptions when the agent does not
supply an explicit task type. This is a heuristic fallback, not an LLM call.
"""

from typing import Optional

from ..types import Complexity, TaskType

_KEYWORD_MAP: list[tuple[TaskType, list[str]]] = [
    # More-specific matchers must come before broader ones that share substrings.
    (TaskType.CODE_PLANNING, ["plan the code", "design the implementation", "code architecture", "how should I implement"]),
    (TaskType.CODE_GENERATION, ["write code", "implement", "build a function", "create a script", "generate code"]),
    (TaskType.CODE_REVIEW, ["review this code", "code review", "check this code", "audit the code"]),
    (TaskType.DEBUGGING, ["debug", "fix this bug", "why does this error", "traceback", "stack trace"]),
    (TaskType.RISK_REVIEW, ["risk review", "risk assessment", "review risk", "drawdown analysis", "volatility assessment", "position sizing", "kill switch"]),
    (TaskType.MEMO_WRITING, ["write memo", "draft memo", "memo writing", "research memo", "write the memo"]),
    (TaskType.SYSTEM_ARCHITECTURE, ["system architecture", "design the system", "infrastructure design"]),
    (TaskType.RESEARCH_REASONING, ["research", "analyze", "investigate", "explore", "hypothesis", "mechanism"]),
    (TaskType.PAPER_ANALYSIS, ["analyze this paper", "paper analysis", "read this paper", "understand this paper", "academic", "journal", "ssrn", "arxiv", "working paper", "literature"]),
    (TaskType.ALPHA_IDEA_GENERATION, ["alpha idea", "trading signal", "strategy idea", "new alpha"]),
    (TaskType.DATA_GRABBING, ["fetch data", "grab data", "download", "api call", "get the data", "pull data"]),
    (TaskType.WEB_SOURCE_SCREENING, ["screening", "source check", "verify source", "pre-screen", "filter sources"]),
    (TaskType.GIT_ACTIVITY_SUMMARY, ["git log", "git summary", "commit summary", "activity summary"]),
    (TaskType.SUMMARIZATION, ["summarize", "summary", "tldr", "sum up", "brief"]),
    (TaskType.TEXT_CLEANUP, ["format", "clean up", "reformat", "fix markdown", "lint", "cleanup"]),
    (TaskType.CLASSIFICATION, ["classify", "categorize", "label", "tagging"]),
    (TaskType.MEMORY_UPDATE, ["memory update", "update memory", "save to memory", "remember this"]),
    (TaskType.GENERAL_QA, []),
]

_HIGH_COMPLEXITY_TYPES: set[TaskType] = {
    TaskType.SYSTEM_ARCHITECTURE,
    TaskType.RESEARCH_REASONING,
    TaskType.PAPER_ANALYSIS,
    TaskType.ALPHA_IDEA_GENERATION,
    TaskType.CODE_PLANNING,
    TaskType.CODE_GENERATION,
    TaskType.CODE_REVIEW,
    TaskType.DEBUGGING,
    TaskType.RISK_REVIEW,
    TaskType.MEMO_WRITING,
}

_LOW_COMPLEXITY_TYPES: set[TaskType] = {
    TaskType.SUMMARIZATION,
    TaskType.TEXT_CLEANUP,
    TaskType.GIT_ACTIVITY_SUMMARY,
    TaskType.CLASSIFICATION,
    TaskType.MEMORY_UPDATE,
    TaskType.DATA_GRABBING,
    TaskType.WEB_SOURCE_SCREENING,
}

_CODE_TASK_TYPES: set[TaskType] = {
    TaskType.CODE_GENERATION,
    TaskType.CODE_PLANNING,
    TaskType.CODE_REVIEW,
    TaskType.DEBUGGING,
}

_COST_SENSITIVE_TYPES: set[TaskType] = {
    TaskType.SUMMARIZATION,
    TaskType.TEXT_CLEANUP,
    TaskType.CLASSIFICATION,
    TaskType.MEMORY_UPDATE,
    TaskType.GIT_ACTIVITY_SUMMARY,
    TaskType.DATA_GRABBING,
    TaskType.WEB_SOURCE_SCREENING,
}

_RISK_CRITICAL_TYPES: set[TaskType] = {
    TaskType.RISK_REVIEW,
}

_RISK_AGENT_PATTERN = "risk-agent"
_AGENT_KEYWORD_HINTS: dict[str, TaskType] = {
    "research-agent": TaskType.RESEARCH_REASONING,
    "programmer-agent": TaskType.CODE_GENERATION,
    "risk-agent": TaskType.RISK_REVIEW,
    "review-agent": TaskType.RESEARCH_REASONING,
    "data-agent": TaskType.DATA_GRABBING,
}


def classify_task(
    description: str,
    agent_name: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> TaskType:
    """Classify a task description into a TaskType using keyword matching.

    Agent name is used as a hint when the text is ambiguous.
    Returns TaskType.GENERAL_QA when no strong match is found.
    """
    lowered = description.lower()
    for task_type, keywords in _KEYWORD_MAP:
        if not keywords:
            continue
        for kw in keywords:
            if kw.lower() in lowered:
                return task_type

    # Agent-name hint for ambiguous tasks
    if agent_name and agent_name.lower().strip() in _AGENT_KEYWORD_HINTS:
        return _AGENT_KEYWORD_HINTS[agent_name.lower().strip()]

    return TaskType.GENERAL_QA


def infer_complexity(
    description: str = "",
    task_type: Optional[TaskType] = None,
    requires_code: bool = False,
    long_context: bool = False,
    metadata: Optional[dict] = None,
) -> Complexity:
    """Infer complexity level from task type and description signals.

    Returns Complexity.LOW, MEDIUM, or HIGH.
    """
    if task_type and task_type in _HIGH_COMPLEXITY_TYPES:
        return Complexity.HIGH
    if task_type and task_type in _LOW_COMPLEXITY_TYPES:
        return Complexity.LOW
    if requires_code or long_context:
        return Complexity.HIGH

    lowered = description.lower()
    complex_signals = ["complex", "difficult", "careful", "nuanced", "multi-step", "tricky", "advanced"]
    simple_signals = ["simple", "quick", "trivial", "small", "tiny", "easy", "basic"]
    if any(s in lowered for s in complex_signals):
        return Complexity.HIGH
    if any(s in lowered for s in simple_signals):
        return Complexity.LOW
    return Complexity.MEDIUM


def infer_cost_sensitivity(
    task_type: TaskType,
    complexity: Complexity,
    metadata: Optional[dict] = None,
) -> bool:
    """Infer whether cost sensitivity matters for this task.

    Low-complexity, throughput-oriented tasks are cost-sensitive.
    High-complexity, code, and risk tasks are not.
    """
    if metadata and metadata.get("cost_sensitive") is not None:
        return bool(metadata["cost_sensitive"])
    if task_type in _COST_SENSITIVE_TYPES and complexity == Complexity.LOW:
        return True
    if task_type in _CODE_TASK_TYPES or task_type in _RISK_CRITICAL_TYPES:
        return False
    if complexity == Complexity.HIGH:
        return False
    return False


def infer_long_context(
    description: str = "",
    metadata: Optional[dict] = None,
) -> bool:
    """Infer whether a task likely requires long context."""
    if metadata and metadata.get("requires_long_context") is not None:
        return bool(metadata["requires_long_context"])
    lowered = description.lower()
    signals = [
        "long document", "full paper", "multi-page", "entire codebase",
        "complete backtest", "full report", "whole memo", "entire",
        "long paper", "multiple papers",
    ]
    return any(s in lowered for s in signals)


def is_cacheable(task_type: TaskType, metadata: Optional[dict] = None) -> bool:
    """Return True if the task type is safe to cache."""
    if metadata and metadata.get("no_cache"):
        return False
    never_cache = {
        TaskType.CODE_GENERATION,
        TaskType.CODE_PLANNING,
        TaskType.CODE_REVIEW,
        TaskType.DEBUGGING,
        TaskType.RISK_REVIEW,
    }
    return task_type not in never_cache
