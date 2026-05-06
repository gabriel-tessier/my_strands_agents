from __future__ import annotations
from pathlib import Path
from strands import tool

@tool
def write_file(path: str, content: str) -> str:
    """
    Write content to a file, creating directories if needed.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"File written: {p}"
