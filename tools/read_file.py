from __future__ import annotations
from pathlib import Path
from strands import tool

@tool
def read_file(path: str) -> str:
    """
    Read a file and return its content.
    """
    p = Path(path)
    if not p.is_file():
        return f"File not found: {p}"
    return p.read_text(encoding="utf-8")
