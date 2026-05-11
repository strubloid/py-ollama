import pytest
from ai.ollama import OllamaError, OllamaNotFoundError, OllamaCommandError

"""Tests for Ollama exceptions."""
class TestOllamaError:
    
    """Test that OllamaError is an Exception subclass."""
    def test_ollama_error_is_exception(self):
        assert issubclass(OllamaError, Exception)
    
    """Test that OllamaNotFoundError inherits from OllamaError."""
    def test_ollama_not_found_error_is_ollama_error(self):
        assert issubclass(OllamaNotFoundError, OllamaError)
    
    """Test that OllamaCommandError inherits from OllamaError."""
    def test_ollama_command_error_is_ollama_error(self):    
        assert issubclass(OllamaCommandError, OllamaError)
    
    """Test that OllamaError can be raised with a message."""
    def test_ollama_error_can_be_raised(self):    
        with pytest.raises(OllamaError) as exc_info:
            raise OllamaError("test message")
        assert str(exc_info.value) == "test message"
    
    """Test that OllamaNotFoundError can be raised."""
    def test_ollama_not_found_error_can_be_raised(self):    
        with pytest.raises(OllamaNotFoundError) as exc_info:
            raise OllamaNotFoundError("ollama not found")
        assert "ollama not found" in str(exc_info.value)
    
    """Test that OllamaCommandError can be raised."""
    def test_ollama_command_error_can_be_raised(self):    
        with pytest.raises(OllamaCommandError) as exc_info:
            raise OllamaCommandError("command failed")
        assert "command failed" in str(exc_info.value)