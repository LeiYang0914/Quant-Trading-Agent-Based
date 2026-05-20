"""Load .env file into os.environ before providers read API keys.

Uses python-dotenv if installed. Silently skips if the package or .env file
is absent — this keeps dry-run and tests working without any setup.
"""

import logging
import os
from pathlib import Path

logger = logging.getLogger("llm_router.env")

_LOADED = False


def load_dotenv_if_available(env_path: str | None = None) -> None:
    """Load .env once at module import time.

    Safe to call multiple times — only loads once per process.
    Searches project root for .env by default.
    """
    global _LOADED
    if _LOADED:
        return

    target = Path(env_path) if env_path else _find_project_root() / ".env"

    try:
        from dotenv import load_dotenv  # type: ignore[import-untyped]

        if target.exists():
            load_dotenv(target, override=False)
            logger.info(".env loaded from %s", target)
        else:
            logger.debug("No .env file found at %s", target)
    except ImportError:
        logger.debug("python-dotenv not installed — skipping .env load")
    except Exception as exc:
        logger.warning("Failed to load .env: %s", exc)

    _LOADED = True


def _find_project_root() -> Path:
    """Walk upward from this file to find the project root (has CLAUDE.md)."""
    current = Path(__file__).resolve().parent
    for _ in range(8):
        if (current / "CLAUDE.md").exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    # Fallback: assume we're at src/llm/utils/env_loader.py → project root is 3 levels up
    return Path(__file__).resolve().parent.parent.parent.parent
