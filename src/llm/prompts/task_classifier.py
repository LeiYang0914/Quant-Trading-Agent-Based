"""Task classification heuristics for the LLM Router.

Produces a TaskType from free-text task descriptions when the agent does not
supply an explicit task type. This is a heuristic fallback, not an LLM call.
"""

from typing import Optional

from ..types import Complexity, TaskType

_KEYWORD_MAP: list[tuple[TaskType, list[str]]] = [
    # More-specific matchers must come before broader ones that share substrings.
    # Code-related (ordered: plan → generate → review → debug)
    (TaskType.CODE_PLANNING, [
        "plan the code", "design the implementation", "code architecture",
        "how should I implement", "plan the implementation", "architecture plan",
        "design pattern", "system design for",
    ]),
    (TaskType.CODE_GENERATION, [
        "write code", "write a function", "write a script", "write a class",
        "build a function", "create a script", "generate code",
        "implement a", "implement the", "implement this",
        "code this", "code the",
        "write the backtest", "write the test",
        "program this", "develop a",
    ]),
    (TaskType.CODE_REVIEW, [
        "review this code", "code review", "check this code",
        "audit the code", "review the code", "look over this code",
        "inspect this code", "review my code", "code audit",
    ]),
    (TaskType.DEBUGGING, [
        "debug", "fix this bug", "fix the bug",
        "why does this error", "traceback", "stack trace",
        "why is this failing", "what is wrong with", "troubleshoot",
        "why isn't this", "fix this issue", "find the bug",
        "why does it crash",
    ]),
    # Risk (before general "review")
    (TaskType.RISK_REVIEW, [
        "risk review", "risk assessment", "review risk",
        "drawdown analysis", "volatility assessment",
        "position sizing", "kill switch",
        "risk report", "risk profile", "risk limit",
        "var calculation", "expected shortfall", "stress test",
    ]),
    # Memo (before general "write")
    (TaskType.MEMO_WRITING, [
        "write memo", "draft memo", "memo writing",
        "research memo", "write the memo", "draft the memo",
        "write a memo", "prepare memo",
    ]),
    # Architecture
    (TaskType.SYSTEM_ARCHITECTURE, [
        "system architecture", "design the system",
        "infrastructure design", "architecture design",
        "design the architecture", "architect the",
    ]),
    # Paper analysis (before general "research"/"analyze")
    (TaskType.PAPER_ANALYSIS, [
        "analyze this paper", "paper analysis", "read this paper",
        "understand this paper", "academic paper", "journal paper",
        "ssrn", "arxiv", "working paper", "literature review",
        "summarize this paper", "paper summary", "extract from paper",
    ]),
    # Alpha generation
    (TaskType.ALPHA_IDEA_GENERATION, [
        "alpha idea", "trading signal", "strategy idea",
        "new alpha", "alpha generation", "signal idea",
        "generate alpha", "trading strategy",
        "new trading idea", "alpha research",
    ]),
    # Research reasoning (broad — place after paper/alpha)
    (TaskType.RESEARCH_REASONING, [
        "research question", "reason about", "investigate why",
        "explore the relationship", "hypothesis", "mechanism",
        "what drives", "what causes", "economic rationale",
        "market microstructure", "analyze the relationship",
        "explain the relationship", "factor analysis",
    ]),
    # Data grabbing
    (TaskType.DATA_GRABBING, [
        "fetch data", "grab data", "download data",
        "api call", "get the data", "pull data",
        "retrieve data", "download the", "scrape",
        "get ohlcv", "get market data", "query the",
    ]),
    # Source screening
    (TaskType.WEB_SOURCE_SCREENING, [
        "source screening", "source check", "verify source",
        "pre-screen", "filter sources", "screen sources",
        "check this source", "validate source", "verify this link",
        "is this source reliable", "source verification",
    ]),
    # Git activity
    (TaskType.GIT_ACTIVITY_SUMMARY, [
        "git log", "git summary", "commit summary",
        "activity summary", "git activity", "commit history",
        "what changed", "recent changes",
    ]),
    # Summarization
    (TaskType.SUMMARIZATION, [
        "summarize", "summary", "tldr", "sum up",
        "brief overview", "give me the gist", "in short",
        "key points", "bullet points of",
    ]),
    # Text cleanup
    (TaskType.TEXT_CLEANUP, [
        "format this", "clean up", "reformat", "fix markdown",
        "lint", "cleanup", "fix formatting", "fix the formatting",
        "correct the markdown", "proper markdown",
    ]),
    # Classification
    (TaskType.CLASSIFICATION, [
        "classify", "categorize", "label these", "tagging",
        "sort into", "group these", "assign category",
    ]),
    # Memory update
    (TaskType.MEMORY_UPDATE, [
        "memory update", "update memory", "save to memory",
        "remember this", "update the memory", "save this to",
        "store in memory",
    ]),
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
# Sub-activity hints: within an agent, certain phrases suggest a specific task type.
_ACTIVITY_HINTS: list[tuple[str, TaskType]] = [
    ("source pre-screen", TaskType.WEB_SOURCE_SCREENING),
    ("source discovery", TaskType.WEB_SOURCE_SCREENING),
    ("source screening", TaskType.WEB_SOURCE_SCREENING),
    ("paper analysis", TaskType.PAPER_ANALYSIS),
    ("memo synthesis", TaskType.MEMO_WRITING),
    ("memo writing", TaskType.MEMO_WRITING),
    ("final synthesis", TaskType.RESEARCH_REASONING),
    ("discovery note", TaskType.ALPHA_IDEA_GENERATION),
    ("memory update", TaskType.MEMORY_UPDATE),
    ("idea evaluation", TaskType.RESEARCH_REASONING),
    ("overlap detection", TaskType.RESEARCH_REASONING),
    ("test generation", TaskType.CODE_GENERATION),
    ("backtest report", TaskType.SUMMARIZATION),
    ("simple data fetch", TaskType.DATA_GRABBING),
    ("data quality analysis", TaskType.RESEARCH_REASONING),
    ("architecture planning", TaskType.SYSTEM_ARCHITECTURE),
    ("api adapter", TaskType.CODE_GENERATION),
    ("position sizing", TaskType.RISK_REVIEW),
    ("kill switch", TaskType.RISK_REVIEW),
]


def classify_task(
    description: str,
    agent_name: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> TaskType:
    """Classify a task description into a TaskType using keyword matching.

    Agent name is used as a hint when the text is ambiguous.
    Activity hints (from agent activity routing config) provide secondary signals.
    Returns TaskType.GENERAL_QA when no strong match is found.
    """
    lowered = description.lower()

    # 1. Keyword map (most specific matchers first)
    for task_type, keywords in _KEYWORD_MAP:
        if not keywords:
            continue
        for kw in keywords:
            if kw.lower() in lowered:
                return task_type

    # 2. Activity hints (semi-specific phrases)
    for phrase, task_type in _ACTIVITY_HINTS:
        if phrase in lowered:
            return task_type

    # 3. Agent-name hint for truly ambiguous text
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
