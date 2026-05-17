"""Local file-based response cache for the LLM Router.

Stores cached responses keyed by a hash of provider, model, task_type, and prompt.
Respects cache exclusions (code gen, risk review never cached by default).
"""

import hashlib
import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Optional

from ..types import LLMResponse, TaskRequest, TaskType

logger = logging.getLogger("llm_router.cache")

_NEVER_CACHE: set[TaskType] = {
    TaskType.CODE_GENERATION,
    TaskType.CODE_PLANNING,
    TaskType.CODE_REVIEW,
    TaskType.DEBUGGING,
    TaskType.RISK_REVIEW,
}


class ResponseCache:
    """JSON-file-based cache for LLM responses."""

    def __init__(
        self,
        cache_dir: str = ".cache/llm",
        ttl_seconds: int = 86400,
        max_entries: int = 10000,
        enabled: bool = True,
    ):
        self.cache_dir = Path(cache_dir)
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries
        self.enabled = enabled
        self._index_path = self.cache_dir / "cache_index.json"
        self._index: dict = {}

        if self.enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            self._index = self._load_index()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, request: TaskRequest, provider: str, model: str) -> Optional[LLMResponse]:
        """Look up a cached response. Returns None on miss."""
        if not self.enabled:
            return None
        if not self._is_cacheable(request):
            return None
        key = self._make_key(request, provider, model)
        entry = self._index.get(key)
        if entry is None:
            return None
        if self._expired(entry):
            self._remove(key)
            return None
        # Reconstruct response from cached entry
        data = entry.get("data", {})
        return LLMResponse(
            task_id=request.task_id,
            success=True,
            provider=data.get("provider"),
            model=data.get("model"),
            content=data.get("content"),
            cache_hit=True,
            estimated_cost=data.get("estimated_cost"),
            latency_ms=0,
            latency_seconds=0.0,
        )

    def put(
        self,
        request: TaskRequest,
        provider: str,
        model: str,
        response: LLMResponse,
    ) -> None:
        """Store a successful response in the cache."""
        if not self.enabled:
            return
        if not self._is_cacheable(request):
            return
        if not response.success or response.content is None:
            return
        key = self._make_key(request, provider, model)
        entry = {
            "created_at": time.time(),
            "prompt_hash": self._hash_text(request.prompt),
            "task_type": request.task_type.value,
            "agent_name": request.agent_name,
            "data": {
                "provider": response.provider.value,
                "model": response.model,
                "content": response.content,
                "estimated_cost": response.estimated_cost,
            },
        }
        self._index[key] = entry
        self._maybe_evict()
        self._save_index()

    def clear(self) -> int:
        """Clear all cached entries. Returns count removed."""
        count = len(self._index)
        self._index = {}
        if self._index_path.exists():
            self._index_path.unlink()
        logger.info("Cache cleared: %d entries removed", count)
        return count

    @property
    def size(self) -> int:
        return len(self._index)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _is_cacheable(self, request: TaskRequest) -> bool:
        if request.task_type in _NEVER_CACHE:
            return False
        if request.metadata.get("no_cache"):
            return False
        return True

    def _make_key(self, request: TaskRequest, provider: str, model: str) -> str:
        parts = [
            provider,
            model,
            request.task_type.value,
            self._hash_text(request.prompt),
        ]
        return hashlib.sha256("|".join(parts).encode()).hexdigest()[:32]

    @staticmethod
    def _hash_text(text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()[:16]

    def _expired(self, entry: dict) -> bool:
        age = time.time() - entry.get("created_at", 0)
        return age > self.ttl_seconds

    def _remove(self, key: str) -> None:
        self._index.pop(key, None)
        self._save_index()

    def _maybe_evict(self) -> None:
        if len(self._index) <= self.max_entries:
            return
        # Evict oldest entries
        sorted_keys = sorted(self._index.keys(), key=lambda k: self._index[k].get("created_at", 0))
        to_remove = len(self._index) - self.max_entries
        for key in sorted_keys[:to_remove]:
            self._index.pop(key, None)
        logger.info("Cache evicted %d entries", to_remove)

    def _load_index(self) -> dict:
        if not self._index_path.exists():
            return {}
        try:
            with open(self._index_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_index(self) -> None:
        try:
            with open(self._index_path, "w", encoding="utf-8") as f:
                json.dump(self._index, f, indent=2)
        except OSError as exc:
            logger.warning("Failed to save cache index: %s", exc)
