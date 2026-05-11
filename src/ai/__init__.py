"""AI modules for Ollama interaction."""

from .modelfile import (
    ModelfileError,
    build_modelfile_content,
    write_temporary_modelfile,
    cleanup_modelfile,
    TemporaryModelfile,
)

from .ollama import (
    OllamaError,
    OllamaNotFoundError,
    OllamaCommandError,
    check_ollama_installed,
    get_available_models,
    create_model,
    delete_model,
)

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