"""Structured logging for LLM Router decisions.

Logs every routing decision with enough detail for auditing and cost tracking.
Never logs API keys or full prompt contents.
"""

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from ..types import LLMResponse, RoutingDecision, TaskRequest

logger = logging.getLogger("llm_router")


class RoutingLogger:
    """Records routing decisions to a structured JSONL log file."""

    def __init__(self, log_dir: Optional[Path] = None):
        self.log_dir = Path(log_dir) if log_dir else Path("reports/llm_routing")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._log_path = self.log_dir / "routing_log.jsonl"

    def log_decision(
        self,
        request: TaskRequest,
        decision: RoutingDecision,
    ) -> None:
        """Write a routing decision entry to the JSONL log."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task_id": request.task_id,
            "agent_name": request.agent_name,
            "task_type": request.task_type.value,
            "domain": request.domain.value,
            "complexity": request.complexity.value,
            "requires_code": request.requires_code,
            "requires_long_context": request.requires_long_context,
            "cost_sensitive": request.cost_sensitive,
            "selected_provider": decision.selected_provider.value,
            "selected_model": decision.selected_model,
            "reason": decision.reason,
            "fallback_provider": decision.fallback_provider.value if decision.fallback_provider else None,
            "fallback_model": decision.fallback_model,
            "estimated_cost_level": decision.estimated_cost_level,
            "max_tokens": decision.max_tokens,
            "temperature": decision.temperature,
            "timeout_seconds": decision.timeout_seconds,
        }
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        logger.info(
            "ROUTE | task=%s agent=%s type=%s → %s/%s reason=%s",
            request.task_id,
            request.agent_name,
            request.task_type.value,
            decision.selected_provider.value,
            decision.selected_model,
            decision.reason,
        )

    def log_response(
        self,
        request: TaskRequest,
        decision: RoutingDecision,
        response: LLMResponse,
    ) -> None:
        """Log the full outcome after a provider call completes."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task_id": request.task_id,
            "agent_name": request.agent_name,
            "task_type": request.task_type.value,
            "selected_provider": decision.selected_provider.value,
            "selected_model": decision.selected_model,
            "success": response.success,
            "fallback_used": response.fallback_used,
            "latency_ms": response.latency_ms,
            "error_summary": (response.error[:200] if response.error else None),
        }
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        log_level = logging.INFO if response.success else logging.WARNING
        logger.log(
            log_level,
            "RESULT | task=%s provider=%s success=%s fallback=%s latency_ms=%s",
            request.task_id,
            decision.selected_provider.value,
            response.success,
            response.fallback_used,
            response.latency_ms,
        )

    def log_fallback(
        self,
        request: TaskRequest,
        primary_decision: RoutingDecision,
        fallback_decision: RoutingDecision,
        reason: str,
    ) -> None:
        """Log when a fallback was triggered."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "fallback_triggered",
            "task_id": request.task_id,
            "agent_name": request.agent_name,
            "task_type": request.task_type.value,
            "primary_provider": primary_decision.selected_provider.value,
            "primary_model": primary_decision.selected_model,
            "fallback_provider": fallback_decision.selected_provider.value,
            "fallback_model": fallback_decision.selected_model,
            "reason": reason,
        }
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        logger.warning(
            "FALLBACK | task=%s %s→%s reason=%s",
            request.task_id,
            primary_decision.selected_provider.value,
            fallback_decision.selected_provider.value,
            reason,
        )
