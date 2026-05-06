"""Unit tests for my_strands_agents.code_review.parallel."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from my_strands_agents.code_review.parallel import review_files_in_parallel


class TestReviewFilesInParallel:
    def test_yields_file_and_result_pairs(self, tmp_path):
        file1 = tmp_path / "a.py"
        file2 = tmp_path / "b.py"
        file1.write_text("# a")
        file2.write_text("# b")

        prompt_file = tmp_path / "test.prompt"
        prompt_file.write_text("Review code.")

        expected = [(str(file1), "Review a"), (str(file2), "Review b")]

        with patch(
            "my_strands_agents.code_review.parallel.ProcessPoolExecutor"
        ) as mock_executor_cls:
            mock_executor = MagicMock()
            mock_executor_cls.return_value.__enter__.return_value = mock_executor
            mock_executor_cls.return_value.__exit__.return_value = False
            mock_executor.map.return_value = iter(expected)

            results = list(
                review_files_in_parallel(
                    [str(file1), str(file2)],
                    context=None,
                    prompt_path=str(prompt_file),
                )
            )

        assert results == expected

    def test_passes_correct_tasks_to_executor(self, tmp_path):
        file1 = tmp_path / "c.py"
        file1.write_text("# c")

        prompt_file = tmp_path / "p.prompt"
        prompt_file.write_text("p")

        with patch(
            "my_strands_agents.code_review.parallel.ProcessPoolExecutor"
        ) as mock_executor_cls:
            mock_executor = MagicMock()
            mock_executor_cls.return_value.__enter__.return_value = mock_executor
            mock_executor_cls.return_value.__exit__.return_value = False
            mock_executor.map.return_value = iter([(str(file1), "ok")])

            list(
                review_files_in_parallel(
                    [str(file1)],
                    context="ctx",
                    prompt_path=str(prompt_file),
                    max_workers=2,
                )
            )

            mock_executor_cls.assert_called_once_with(max_workers=2)
            tasks_arg = mock_executor.map.call_args[0][1]
            assert tasks_arg == [(str(file1), "ctx", str(prompt_file))]

    def test_empty_file_list_yields_nothing(self, tmp_path):
        with patch(
            "my_strands_agents.code_review.parallel.ProcessPoolExecutor"
        ) as mock_executor_cls:
            mock_executor = MagicMock()
            mock_executor_cls.return_value.__enter__.return_value = mock_executor
            mock_executor_cls.return_value.__exit__.return_value = False
            mock_executor.map.return_value = iter([])

            results = list(
                review_files_in_parallel([], context=None, prompt_path="p.prompt")
            )

        assert results == []
