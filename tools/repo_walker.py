# file: tools/repo_walker.py

from __future__ import annotations
from pathlib import Path
from typing import List
from strands import tool


IGNORE_FILE_NAME = ".reviewignore"


def load_ignore_patterns(root: Path) -> List[str]:
    ignore_file = root / IGNORE_FILE_NAME
    if not ignore_file.is_file():
        return []

    patterns = []
    for line in ignore_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line)
    return patterns


def should_ignore(path: Path, patterns: List[str]) -> bool:
    for pattern in patterns:
        if path.match(pattern):
            return True
    return False


@tool
def walk_repository(directory: str) -> List[str]:
    """
    Walk a repository and return a list of Python files,
    respecting .reviewignore patterns.
    """
    root = Path(directory)
    if not root.is_dir():
        raise ValueError(f"Not a directory: {directory}")

    ignore_patterns = load_ignore_patterns(root)
    python_files = []

    for path in root.rglob("*.py"):
        if should_ignore(path, ignore_patterns):
            continue
        python_files.append(str(path))

    return python_files
