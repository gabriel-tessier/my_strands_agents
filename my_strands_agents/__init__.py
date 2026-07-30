"""my_strands_agents – AI-powered code review agents using the Strands Agents SDK."""

__version__ = "0.1.0"

from .agent import build_agent, letter_counter
from .code_review.agent import load_prompt, review_code
from .tools.repo_walker import walk_repository

__all__ = [
    "build_agent",
    "letter_counter",
    "load_prompt",
    "review_code",
    "walk_repository",
]
