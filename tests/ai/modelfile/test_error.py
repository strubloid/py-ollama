import pytest
from ai.modelfile.error import ModelfileError

"""Tests for ModelfileError exception."""
class TestModelfileError:

    """Test that ModelfileError is an Exception subclass."""
    def test_is_exception_subclass(self):
        assert issubclass(ModelfileError, Exception)
    
    """Test that ModelfileError can be raised with a message."""
    def test_can_be_raised_with_message(self):    
        with pytest.raises(ModelfileError) as exc_info:
            raise ModelfileError("test error message")
        assert str(exc_info.value) == "test error message"
    
    """Test that ModelfileError can be caught as Exception."""
    def test_can_catch_base_exception(self):    
        with pytest.raises(Exception):
            raise ModelfileError("test")