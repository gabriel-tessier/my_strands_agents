"""Unit tests for my_strands_agents.agent (letter_counter tool)."""

import pytest

# Import only the pure-Python function, not the full module that would
# trigger strands/Ollama imports at collection time.
from my_strands_agents.agent import letter_counter


class TestLetterCounter:
    def test_basic_count(self):
        assert letter_counter("strawberry", "r") == 3

    def test_case_insensitive_lower(self):
        assert letter_counter("Hello", "l") == 2

    def test_case_insensitive_upper(self):
        assert letter_counter("Hello", "L") == 2

    def test_zero_occurrences(self):
        assert letter_counter("apple", "z") == 0

    def test_entire_word_same_letter(self):
        assert letter_counter("aaa", "a") == 3

    def test_non_string_word_returns_zero(self):
        assert letter_counter(123, "r") == 0  # type: ignore[arg-type]

    def test_non_string_letter_returns_zero(self):
        assert letter_counter("word", 42) == 0  # type: ignore[arg-type]

    def test_multi_char_letter_raises(self):
        with pytest.raises(ValueError, match="single character"):
            letter_counter("word", "ab")

    def test_empty_letter_raises(self):
        with pytest.raises(ValueError, match="single character"):
            letter_counter("word", "")

    def test_empty_word(self):
        assert letter_counter("", "a") == 0
