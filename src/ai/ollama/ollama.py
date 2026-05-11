from .exceptions import OllamaError, OllamaNotFoundError, OllamaCommandError
from .check import check_ollama_installed
from .client import OllamaClient

get_available_models = OllamaClient().list_models
create_model = OllamaClient().create_model
delete_model = OllamaClient().delete_model

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