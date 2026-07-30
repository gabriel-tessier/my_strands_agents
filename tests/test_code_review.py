"""Unit tests for my_strands_agents.code_review.agent."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from my_strands_agents.code_review.agent import load_prompt, build_agent, review_code


class TestLoadPrompt:
    def test_loads_and_strips_whitespace(self, tmp_path):
        prompt_file = tmp_path / "test.prompt"
        prompt_file.write_text("  Review this code.  ")

        result = load_prompt(prompt_file)

        assert result == "Review this code."

    def test_accepts_string_path(self, tmp_path):
        prompt_file = tmp_path / "test.prompt"
        prompt_file.write_text("Hello")

        result = load_prompt(str(prompt_file))

        assert result == "Hello"

    def test_raises_when_file_missing(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="Prompt file not found"):
            load_prompt(tmp_path / "nonexistent.prompt")


class TestBuildAgent:
    def test_returns_agent_instance(self):
        with (
            patch("my_strands_agents.code_review.agent.OllamaModel") as mock_model_cls,
            patch("my_strands_agents.code_review.agent.Agent") as mock_agent_cls,
        ):
            mock_model = MagicMock()
            mock_model_cls.return_value = mock_model
            mock_agent = MagicMock()
            mock_agent_cls.return_value = mock_agent

            result = build_agent()

            mock_model_cls.assert_called_once()
            mock_agent_cls.assert_called_once_with(model=mock_model)
            assert result is mock_agent

    def test_model_configured_with_correct_url(self):
        with (
            patch("my_strands_agents.code_review.agent.OllamaModel") as mock_model_cls,
            patch("my_strands_agents.code_review.agent.Agent"),
        ):
            build_agent()

            call_kwargs = mock_model_cls.call_args.kwargs
            assert call_kwargs["host"] == "http://localhost:11434"
            assert call_kwargs["model_id"] == "deepseek-coder-v2:latest"


class TestReviewCode:
    def _make_prompt(self, tmp_path, content="You are a code reviewer."):
        p = tmp_path / "test.prompt"
        p.write_text(content)
        return p

    def test_returns_agent_response(self, tmp_path):
        prompt_file = self._make_prompt(tmp_path)

        with patch("my_strands_agents.code_review.agent.build_agent") as mock_build:
            mock_agent = MagicMock()
            mock_agent.return_value = "Looks good!"
            mock_build.return_value = mock_agent

            result = review_code("print('hello')", prompt_path=prompt_file)

        assert result == "Looks good!"

    def test_includes_code_in_prompt(self, tmp_path):
        prompt_file = self._make_prompt(tmp_path)
        sample_code = "def foo(): pass"

        with patch("my_strands_agents.code_review.agent.build_agent") as mock_build:
            mock_agent = MagicMock()
            mock_agent.return_value = "OK"
            mock_build.return_value = mock_agent

            review_code(sample_code, prompt_path=prompt_file)

            call_args = mock_agent.call_args[0][0]
            assert sample_code in call_args

    def test_includes_file_path_when_provided(self, tmp_path):
        prompt_file = self._make_prompt(tmp_path)

        with patch("my_strands_agents.code_review.agent.build_agent") as mock_build:
            mock_agent = MagicMock()
            mock_agent.return_value = "Nice."
            mock_build.return_value = mock_agent

            review_code("x = 1", file_path="mymodule.py", prompt_path=prompt_file)

            call_args = mock_agent.call_args[0][0]
            assert "mymodule.py" in call_args

    def test_includes_extra_context_when_provided(self, tmp_path):
        prompt_file = self._make_prompt(tmp_path)

        with patch("my_strands_agents.code_review.agent.build_agent") as mock_build:
            mock_agent = MagicMock()
            mock_agent.return_value = "Done."
            mock_build.return_value = mock_agent

            review_code(
                "x = 1",
                extra_context="Billing service",
                prompt_path=prompt_file,
            )

            call_args = mock_agent.call_args[0][0]
            assert "Billing service" in call_args

    def test_omits_file_path_when_not_provided(self, tmp_path):
        prompt_file = self._make_prompt(tmp_path)

        with patch("my_strands_agents.code_review.agent.build_agent") as mock_build:
            mock_agent = MagicMock()
            mock_agent.return_value = "Done."
            mock_build.return_value = mock_agent

            review_code("x = 1", prompt_path=prompt_file)

            call_args = mock_agent.call_args[0][0]
            assert "File:" not in call_args
