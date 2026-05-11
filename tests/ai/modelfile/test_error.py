"""Tests for modelfile error module."""

import pytest
from ai.modelfile.error import ModelfileError


class TestModelfileError:
    """Tests for ModelfileError exception."""

    def test_is_exception_subclass(self):
        """Test that ModelfileError is an Exception subclass."""
        assert issubclass(ModelfileError, Exception)

    def test_can_be_raised_with_message(self):
        """Test that ModelfileError can be raised with a message."""
        with pytest.raises(ModelfileError) as exc_info:
            raise ModelfileError("test error message")
        assert str(exc_info.value) == "test error message"

    def test_can_catch_base_exception(self):
        """Test that ModelfileError can be caught as Exception."""
        with pytest.raises(Exception):
            raise ModelfileError("test")