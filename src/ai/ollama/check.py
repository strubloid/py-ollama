import shutil

from .exceptions import OllamaNotFoundError

"""Check if the 'ollama' command is available on the system."""
def check_ollama_installed() -> bool:
    return shutil.which("ollama") is not None

"""Verify that 'ollama' is installed, raising an exception if not."""
def require_ollama() -> None:
    if not check_ollama_installed():
        raise OllamaNotFoundError("'ollama' command not found. Is Ollama installed?")