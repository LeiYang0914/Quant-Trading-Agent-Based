"""Rough cost estimation for LLM calls.

Used for logging and routing decisions, not for billing.
All figures are illustrative — actual costs depend on provider pricing.
"""

from typing import Optional

from ..types import ProviderName


_COST_PER_1K: dict[tuple[ProviderName, str], float] = {
    # Claude models (USD per 1K tokens, input estimate)
    (ProviderName.CLAUDE, "claude-opus-4-7"): 0.015,
    (ProviderName.CLAUDE, "claude-sonnet-4-6"): 0.003,
    (ProviderName.CLAUDE, "claude-haiku-4-5-20251001"): 0.001,
    # DeepSeek models (USD per 1K tokens, input estimate)
    (ProviderName.DEEPSEEK, "deepseek-v4-pro"): 0.002,
    (ProviderName.DEEPSEEK, "deepseek-v4-flash"): 0.0003,
}


def estimate_cost(
    provider: ProviderName,
    model: str,
    prompt_chars: int,
    max_tokens: int,
) -> dict:
    """Return a cost estimate dict.

    Uses rough token estimation (~4 chars per token).
    """
    estimated_input_tokens = max(prompt_chars // 4, 1)
    rate = _COST_PER_1K.get((provider, model), 0.001)
    estimated_amount = rate * (estimated_input_tokens / 1000 + max_tokens / 1000)
    estimated_amount = round(estimated_amount, 6)

    if estimated_amount < 0.001:
        level = "negligible"
    elif estimated_amount < 0.01:
        level = "low"
    elif estimated_amount < 0.10:
        level = "medium"
    else:
        level = "high"

    return {
        "level": level,
        "currency": "USD",
        "estimated_amount": estimated_amount,
        "estimated_input_tokens": estimated_input_tokens,
        "max_tokens": max_tokens,
        "note": f"{provider.value}/{model} @ ~${rate}/1K tokens (rough estimate)",
    }
