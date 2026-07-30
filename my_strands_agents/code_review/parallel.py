from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Iterator, List, Tuple


def _review_single_file(args: Tuple[str, str | None, str]) -> Tuple[str, str]:
    from my_strands_agents.code_review.agent import review_code

    file_path, context, prompt_path = args
    code = Path(file_path).read_text(encoding="utf-8")
    result = review_code(
        code,
        file_path=file_path,
        extra_context=context,
        prompt_path=prompt_path,
    )
    return file_path, result


def review_files_in_parallel(
    files: List[str],
    context: str | None,
    prompt_path: str,
    max_workers: int = 4,
) -> Iterator[Tuple[str, str]]:
    """Review multiple files in parallel using a process pool."""
    tasks = [(f, context, prompt_path) for f in files]

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for file_path, result in executor.map(_review_single_file, tasks):
            yield file_path, result


__all__ = ["review_files_in_parallel"]
