# file: code_review_agent.py

from __future__ import annotations

import argparse
from pathlib import Path

from strands import Agent
from strands.models.ollama import OllamaModel

from tools.repo_walker import walk_repository
from parallel_review import review_files_in_parallel


# ============================================================
# CONFIGURATION CONSTANTS
# ============================================================

PROMPT_FILE = "django_code_review.prompt"   # Your prompt file
OLLAMA_MODEL = "deepseek-coder-v2:latest"      # Change to 32b or latest if needed
OLLAMA_URL = "http://localhost:11434"       # Default Ollama endpoint

# Optional: tweak model behavior
MODEL_TEMPERATURE = 0.7
MODEL_NUM_CTX = 160000   # DeepSeek supports 160k context
# ============================================================


def load_prompt(path: str | Path) -> str:
    """Load the system prompt from a text file."""
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Prompt file not found: {p}")
    print('Loaded system prompt from:', p)
    return p.read_text(encoding="utf-8").strip()


def build_agent() -> Agent:
    """
    Create a Strands agent that uses Ollama + DeepSeek for Django/AWS code review.
    """

    return Agent(
        model=OllamaModel(
            host=OLLAMA_URL,
            model_id=OLLAMA_MODEL,
            temperature=MODEL_TEMPERATURE,
            max_tokens=MODEL_NUM_CTX,  # Ensure we can utilize the full context window
            keep_alive="10m",
            options={"top_k": 40},
        )
    )


def review_code(
    code: str,
    file_path: str | None = None,
    extra_context: str | None = None,
    prompt_path: str | Path = PROMPT_FILE,
) -> str:
    """
    High-level helper to send code to the agent for review.
    """
    system_prompt = load_prompt(prompt_path)
    agent = build_agent()

    # Manually prepend system prompt because OllamaModel ignores system_prompt
    prompt_parts = [
        f"[SYSTEM PROMPT]\n{system_prompt}\n\n",
    ]

    if file_path:
        prompt_parts.append(f"File: {file_path}")

    if extra_context:
        prompt_parts.append(f"Context:\n{extra_context}")

    prompt_parts.append("Review the following code according to the system prompt.\n")
    prompt_parts.append("CODE:\n")
    prompt_parts.append(code)

    full_prompt = "\n\n".join(prompt_parts)

    response = agent(full_prompt)
    return str(response)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run DeepSeek code review via Strands + Ollama.")
    parser.add_argument("path", help="Path to a file OR directory to review.")
    parser.add_argument("--context", default=None)
    parser.add_argument("--prompt", default=PROMPT_FILE)
    parser.add_argument("--parallel", action="store_true", help="Enable parallel review")
    parser.add_argument("--workers", type=int, default=4, help="Parallel workers")
    args = parser.parse_args()

    target = Path(args.path)

    # ---------------------------------------------------------
    # CASE 1: Directory → use RepoWalkerTool
    # ---------------------------------------------------------
    if target.is_dir():
        print(f"Walking repository: {target}")
        files = walk_repository(str(target))

        if not files:
            print("No Python files found.")
            return

        print(f"Found {len(files)} Python files.")

        if args.parallel:
            print(f"Running parallel review with {args.workers} workers...\n")
            for file_path, result in review_files_in_parallel(
                files,
                context=args.context,
                prompt_path=args.prompt,
                max_workers=args.workers,
            ):
                print(f"\n=== Review: {file_path} ===\n")
                print(result)
        else:
            print("Running sequential review...\n")
            for file_path in files:
                print(f"\n=== Review: {file_path} ===\n")
                code = Path(file_path).read_text(encoding="utf-8")
                result = review_code(
                    code,
                    file_path=file_path,
                    extra_context=args.context,
                    prompt_path=args.prompt,
                )
                print(result)

        return

    # ---------------------------------------------------------
    # CASE 2: Single file
    # ---------------------------------------------------------
    if target.is_file():
        code = target.read_text(encoding="utf-8")
        result = review_code(
            code,
            file_path=str(target),
            extra_context=args.context,
            prompt_path=args.prompt,
        )
        print(result)
        return

    raise SystemExit(f"Path not found: {target}")


if __name__ == "__main__":
    main()
