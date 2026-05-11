"""Check if the 'ollama' command is available on the system."""

import shutil

from .exceptions import OllamaNotFoundError


def check_ollama_installed() -> bool:
    """Check if the 'ollama' command is available on the system."""
    return shutil.which("ollama") is not None


def require_ollama() -> None:
    """Verify that 'ollama' is installed, raising an exception if not."""
    if not check_ollama_installed():
        raise OllamaNotFoundError("'ollama' command not found. Is Ollama installed?")