"""Deliberately narrow tools: inspect locally, propose changes, never mutate automatically."""
from __future__ import annotations

import os
import platform
from pathlib import Path


def inspect_system() -> dict:
    return {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "working_directory": str(Path.cwd()),
        "mode": "read-only inspection",
    }


def plan_file_action(action: str, path: str) -> dict:
    if action not in {"read", "write", "delete"}:
        raise ValueError("Unsupported action.")
    candidate = Path(path).expanduser()
    return {
        "action": action,
        "path": str(candidate),
        "status": "approval_required",
        "message": "This public demo records a proposed file action only. It does not access or modify files.",
    }
