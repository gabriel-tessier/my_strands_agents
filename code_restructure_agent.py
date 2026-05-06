# file: code_restructure_agent.py

from __future__ import annotations

import argparse
from pathlib import Path

from strands import Agent
from strands.models.ollama import OllamaModel

# Tools
from tools.repo_walker import walk_repository
from tools.read_file import read_file
from tools.write_file import write_file


# ============================================================
# CONFIGURATION CONSTANTS
# ============================================================

RESTRUCTURE_PROMPT_FILE = "project_restructure.prompt"
OLLAMA_MODEL = "deepseek-coder-v2:latest"
OLLAMA_URL = "http://localhost:11434"

MODEL_TEMPERATURE = 0.2
MODEL_NUM_CTX = 160000
# ============================================================


def load_prompt(path: str | Path) -> str:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Prompt file not found: {p}")
    return p.read_text(encoding="utf-8").strip()


def build_restructure_agent() -> Agent:
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

def run_restructure(directory: str, prompt_path: str | Path = RESTRUCTURE_PROMPT_FILE):
    agent = build_restructure_agent()
    system_prompt = load_prompt(prompt_path)

    # Inject system prompt manually
    full_prompt = f"""
[SYSTEM PROMPT]
{system_prompt}

You have access to the following tools:
- walk_repository(directory)
- read_file(path)
- write_file(path, content)

Your task: restructure the project at this path:
{directory}

Begin by inspecting the repository and proposing a new structure.
Then rewrite files as needed using the tools.
"""

    response = agent(full_prompt)
    return str(response)


def main():
    parser = argparse.ArgumentParser(description="DeepSeek agent for restructuring a codebase.")
    parser.add_argument("path", help="Path to the repository to restructure.")
    parser.add_argument(
        "--prompt",
        help="Optional custom restructuring prompt file.",
        default=RESTRUCTURE_PROMPT_FILE,
    )
    args = parser.parse_args()

    target = Path(args.path)
    if not target.is_dir():
        raise SystemExit(f"Directory not found: {target}")

    result = run_restructure(str(target), prompt_path=args.prompt)
    print(result)


if __name__ == "__main__":
    main()
