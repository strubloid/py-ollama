"""Base exception for Ollama-related errors."""
class OllamaError(Exception):
    pass

"""Raised when 'ollama' command is not found."""
class OllamaNotFoundError(OllamaError):
    pass

"""Raised when an Ollama command fails."""
class OllamaCommandError(OllamaError):
    pass