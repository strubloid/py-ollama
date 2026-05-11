"""AI modules for Ollama interaction."""

from .modelfile import (
    build_modelfile_content,
    write_temporary_modelfile,
    cleanup_modelfile,
)

from .modelfile_error import ModelfileError

from .temporary_modelfile import TemporaryModelfile

from .ollama import (
    OllamaError,
    OllamaNotFoundError,
    OllamaCommandError,
    check_ollama_installed,
    get_available_models,
    create_model,
    delete_model,
)

# Import submodules for direct access (e.g., ai.ollama.check_ollama_installed())
from . import modelfile
from . import ollama


__all__ = [
    # modelfile
    "ModelfileError",
    "build_modelfile_content",
    "write_temporary_modelfile",
    "cleanup_modelfile",
    "TemporaryModelfile",
    "modelfile",
    # ollama
    "OllamaError",
    "OllamaNotFoundError",
    "OllamaCommandError",
    "check_ollama_installed",
    "get_available_models",
    "create_model",
    "delete_model",
    "ollama",
]