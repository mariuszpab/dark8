"""UCI/autonomic interface stubs for DARK8.

This module provides a safe `run_agent_auto(cmd)` function used by the UI.
Implementations are minimal stubs and use ASCII-only docstrings to avoid
parser issues reported by linters.
"""

import os
from typing import Any, Dict


def ensure_backend_ready() -> None:
    """Ensure backend is ready (stub)."""
    return


def analyze_dark8_project(project_root: str) -> str:
    return "(analysis stub)"


def auto_fix_dark8_project(project_root: str, out_root: str) -> str:
    return "(auto-fix stub)"


def run_autonomic_task(cmd: str) -> Dict[str, Any]:
    return {"plan": "(plan stub)", "result": "(result stub)"}


def run_agent_auto(cmd: str) -> str:
    """Main UCI gateway (minimal, safe behavior).

    Returns a string summarizing the performed stub action.
    """
    ensure_backend_ready()
    cmd_clean = cmd.strip()
    cmd_lower = cmd_clean.lower()

    project_root = os.path.abspath(os.getcwd())
    auto_fix_root = os.path.join(project_root, "projekty", "auto_fix")

    output = []

    if "przeanalizuj dark8" in cmd_lower or "analiza dark8" in cmd_lower:
        output.append("[AUTO] analysis (stub)")
        output.append(analyze_dark8_project(project_root))
        return "\n".join(output)

    if any(x in cmd_lower for x in ("napraw dark8", "auto-fix dark8", "autofix dark8")):
        output.append("[AUTO] auto-fix (stub)")
        output.append(auto_fix_dark8_project(project_root, auto_fix_root))
        return "\n".join(output)

    result = run_autonomic_task(cmd_clean)
    output.append("[AUTO] plan:")
    output.append(result.get("plan", ""))
    output.append("[AUTO] result:")
    output.append(result.get("result", ""))
    return "\n".join(output)
