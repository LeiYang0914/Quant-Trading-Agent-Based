"""Read and parse LLM Router log files (usage.jsonl, routing_log.jsonl)."""

import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("dashboard.log_reader")

DEFAULT_USAGE_LOG = Path("logs/llm/usage.jsonl")
DEFAULT_ROUTING_LOG = Path("reports/llm_routing/routing_log.jsonl")


def read_usage_log(
    path: Optional[Path] = None,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    limit: int = 0,
) -> list[dict[str, Any]]:
    """Read usage.jsonl and return parsed entries.

    Args:
        path: Path to usage.jsonl. Defaults to logs/llm/usage.jsonl.
        since: Only include entries at or after this timestamp (UTC).
        until: Only include entries before this timestamp (UTC).
        limit: If > 0, return only the most recent N entries.

    Returns:
        List of parsed usage entries (empty list if file missing or empty).
    """
    log_path = Path(path) if path else DEFAULT_USAGE_LOG
    if not log_path.exists():
        return []

    entries: list[dict[str, Any]] = []
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not _in_time_range(entry, since, until):
                    continue
                entries.append(entry)
    except OSError as exc:
        logger.warning("Failed to read usage log %s: %s", log_path, exc)
        return []

    if limit > 0:
        return entries[-limit:]
    return entries


def read_routing_log(
    path: Optional[Path] = None,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
) -> list[dict[str, Any]]:
    """Read routing_log.jsonl and return parsed entries."""
    log_path = Path(path) if path else DEFAULT_ROUTING_LOG
    if not log_path.exists():
        return []

    entries: list[dict[str, Any]] = []
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not _in_time_range(entry, since, until):
                    continue
                entries.append(entry)
    except OSError as exc:
        logger.warning("Failed to read routing log %s: %s", log_path, exc)
        return []

    return entries


def log_file_exists(path: Optional[Path] = None) -> bool:
    """Check whether the usage log file exists and has content."""
    log_path = Path(path) if path else DEFAULT_USAGE_LOG
    if not log_path.exists():
        return False
    return log_path.stat().st_size > 0


def _in_time_range(
    entry: dict[str, Any],
    since: Optional[datetime],
    until: Optional[datetime],
) -> bool:
    """Check if an entry's timestamp falls within the given range."""
    ts_str = entry.get("timestamp")
    if not ts_str:
        return True  # No timestamp → include
    if not since and not until:
        return True
    try:
        ts = datetime.fromisoformat(ts_str)
    except (ValueError, TypeError):
        return True
    if since and ts < since:
        return False
    if until and ts > until:
        return False
    return True


def count_entries(path: Optional[Path] = None) -> int:
    """Count total lines in the usage log."""
    log_path = Path(path) if path else DEFAULT_USAGE_LOG
    if not log_path.exists():
        return 0
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            return sum(1 for line in f if line.strip())
    except OSError:
        return 0
