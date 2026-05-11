"""Ollama package for interacting with the Ollama CLI."""

from .ollama import (
    OllamaError,
    OllamaNotFoundError,
    OllamaCommandError,
    check_ollama_installed,
    get_available_models,
    create_model,
    delete_model,
    OllamaClient,
)

__all__ = [
    "OllamaError",
    "OllamaNotFoundError",
    "OllamaCommandError",
    "check_ollama_installed",
    "get_available_models",
    "create_model",
    "delete_model",
    "OllamaClient",
]