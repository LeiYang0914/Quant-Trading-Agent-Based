"""Token and cost usage tracker for LLM Router.

Logs per-call usage to JSONL and provides aggregate query methods.
"""

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("llm_router.usage")


class UsageTracker:
    """Tracks per-call LLM usage and costs to a JSONL log file."""

    def __init__(self, log_dir: str = "logs/llm"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._usage_path = self.log_dir / "usage.jsonl"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def record(
        self,
        task_id: str,
        agent_name: str,
        task_type: str,
        provider: str,
        model: str,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        estimated_tokens: bool = False,
        estimated_cost: Optional[float] = None,
        cache_hit: bool = False,
        fallback_used: bool = False,
        success: bool = True,
        latency_ms: Optional[int] = None,
    ) -> None:
        """Record a single LLM call."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task_id": task_id,
            "agent_name": agent_name,
            "task_type": task_type,
            "provider": provider,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_tokens": estimated_tokens,
            "estimated_cost": estimated_cost,
            "cache_hit": cache_hit,
            "fallback_used": fallback_used,
            "success": success,
            "latency_ms": latency_ms,
        }
        with open(self._usage_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def get_total_cost(self) -> float:
        """Return total estimated cost across all calls."""
        return sum(
            entry.get("estimated_cost") or 0
            for entry in self._read_all()
        )

    def get_cost_by_agent(self) -> dict[str, float]:
        """Return estimated cost grouped by agent."""
        costs: dict[str, float] = {}
        for entry in self._read_all():
            agent = entry.get("agent_name", "unknown")
            cost = entry.get("estimated_cost") or 0
            costs[agent] = costs.get(agent, 0) + cost
        return costs

    def get_cost_by_provider(self) -> dict[str, float]:
        """Return estimated cost grouped by provider."""
        costs: dict[str, float] = {}
        for entry in self._read_all():
            provider = entry.get("provider", "unknown")
            cost = entry.get("estimated_cost") or 0
            costs[provider] = costs.get(provider, 0) + cost
        return costs

    def get_cost_by_task_type(self) -> dict[str, float]:
        """Return estimated cost grouped by task type."""
        costs: dict[str, float] = {}
        for entry in self._read_all():
            tt = entry.get("task_type", "unknown")
            cost = entry.get("estimated_cost") or 0
            costs[tt] = costs.get(tt, 0) + cost
        return costs

    def get_recent_usage(self, limit: int = 50) -> list[dict[str, Any]]:
        """Return the most recent usage entries."""
        entries = self._read_all()
        return entries[-limit:]

    def get_total_calls(self) -> int:
        """Return total number of recorded calls."""
        return len(self._read_all())

    def get_cache_hit_ratio(self) -> float:
        """Return cache hit ratio (0.0 to 1.0)."""
        entries = self._read_all()
        if not entries:
            return 0.0
        hits = sum(1 for e in entries if e.get("cache_hit"))
        return hits / len(entries)

    def get_fallback_ratio(self) -> float:
        """Return fallback usage ratio."""
        entries = self._read_all()
        if not entries:
            return 0.0
        fb = sum(1 for e in entries if e.get("fallback_used"))
        return fb / len(entries)

    def get_success_rate(self) -> float:
        """Return overall success rate."""
        entries = self._read_all()
        if not entries:
            return 1.0
        successes = sum(1 for e in entries if e.get("success"))
        return successes / len(entries)

    def clear(self) -> int:
        """Clear all usage records. Returns count removed."""
        entries = self._read_all()
        count = len(entries)
        if self._usage_path.exists():
            self._usage_path.unlink()
        logger.info("Usage tracker cleared: %d entries", count)
        return count

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _read_all(self) -> list[dict[str, Any]]:
        if not self._usage_path.exists():
            return []
        entries = []
        with open(self._usage_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        return entries
