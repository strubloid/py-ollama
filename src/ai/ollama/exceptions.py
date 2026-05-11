"""Ollama-related exceptions."""


class OllamaError(Exception):
    """Base exception for Ollama-related errors."""

    pass


class OllamaNotFoundError(OllamaError):
    """Raised when 'ollama' command is not found."""

    pass


class OllamaCommandError(OllamaError):
    """Raised when an Ollama command fails."""

    pass