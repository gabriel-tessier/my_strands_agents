"""Unit tests for my_strands_agents.tools.repo_walker."""

from pathlib import Path

import pytest

from my_strands_agents.tools.repo_walker import (
    load_ignore_patterns,
    should_ignore,
    walk_repository,
)


class TestLoadIgnorePatterns:
    def test_no_ignore_file_returns_empty(self, tmp_path):
        assert load_ignore_patterns(tmp_path) == []

    def test_ignores_blank_lines_and_comments(self, tmp_path):
        (tmp_path / ".reviewignore").write_text("# comment\n\n*.pyc\n")
        assert load_ignore_patterns(tmp_path) == ["*.pyc"]

    def test_multiple_patterns(self, tmp_path):
        (tmp_path / ".reviewignore").write_text("*.pyc\nvenv/\ntests/**\n")
        assert load_ignore_patterns(tmp_path) == ["*.pyc", "venv/", "tests/**"]

    def test_strips_leading_and_trailing_whitespace(self, tmp_path):
        (tmp_path / ".reviewignore").write_text("  *.pyc  \n  venv/  \n")
        assert load_ignore_patterns(tmp_path) == ["*.pyc", "venv/"]


class TestShouldIgnore:
    def test_empty_patterns_never_ignores(self):
        assert should_ignore(Path("src/main.py"), []) is False

    def test_matching_pattern_returns_true(self):
        # Path.match("venv/*") matches direct children only
        assert should_ignore(Path("venv/something.py"), ["venv/*"]) is True

    def test_non_matching_pattern_returns_false(self):
        assert should_ignore(Path("src/main.py"), ["venv/*"]) is False

    def test_first_matching_pattern_short_circuits(self):
        assert should_ignore(Path("tests/test_foo.py"), ["tests/**", "src/**"]) is True

    def test_wildcard_extension(self):
        assert should_ignore(Path("app/cache.pyc"), ["*.pyc"]) is True


class TestWalkRepository:
    def test_finds_python_files(self, tmp_path):
        (tmp_path / "a.py").write_text("# a")
        (tmp_path / "b.py").write_text("# b")
        (tmp_path / "readme.txt").write_text("text")

        files = walk_repository(str(tmp_path))

        assert len(files) == 2
        assert all(f.endswith(".py") for f in files)

    def test_recursive_discovery(self, tmp_path):
        sub = tmp_path / "sub"
        sub.mkdir()
        (tmp_path / "top.py").write_text("# top")
        (sub / "inner.py").write_text("# inner")

        files = walk_repository(str(tmp_path))

        assert len(files) == 2

    def test_respects_reviewignore(self, tmp_path):
        (tmp_path / "keep.py").write_text("# keep")
        (tmp_path / "skip.py").write_text("# skip")
        (tmp_path / ".reviewignore").write_text("skip.py\n")

        files = walk_repository(str(tmp_path))

        assert len(files) == 1
        assert not any("skip" in f for f in files)

    def test_empty_directory(self, tmp_path):
        assert walk_repository(str(tmp_path)) == []

    def test_invalid_directory_raises(self):
        with pytest.raises(ValueError, match="Not a directory"):
            walk_repository("/nonexistent/path/that/does/not/exist")
