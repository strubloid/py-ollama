"""
Interaction with the Ollama command-line tool.

Handles:
- Detecting if 'ollama' is installed
- Running 'ollama ls' and parsing model names
- Running 'ollama create' to create new models
"""

import subprocess
import shutil


class OllamaError(Exception):
    """Base exception for Ollama-related errors."""

    pass


class OllamaNotFoundError(OllamaError):
    """Raised when 'ollama' command is not found."""

    pass


class OllamaCommandError(OllamaError):
    """Raised when an Ollama command fails."""

    pass


def check_ollama_installed() -> bool:
    """
    Check if the 'ollama' command is available on the system.

    Returns:
        True if ollama is installed, False otherwise.
    """
    return shutil.which("ollama") is not None


def get_available_models() -> list[str]:
    """
    Get a list of available models from 'ollama ls'.

    Runs the command: ollama ls
    Parses the output to extract model names (first column after header).

    Returns:
        A list of model names.

    Raises:
        OllamaNotFoundError: If 'ollama' is not installed.
        OllamaCommandError: If the command fails or returns no models.
    """
    if not check_ollama_installed():
        raise OllamaNotFoundError("'ollama' command not found. Is Ollama installed?")

    try:
        result = subprocess.run(
            ["ollama", "ls"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise OllamaCommandError(f"'ollama ls' failed: {e.stderr}") from e

    lines = result.stdout.strip().split("\n")
    if len(lines) < 2:
        raise OllamaCommandError("No models found. Run 'ollama pull <model>' first.")

    # Skip header line (index 0), extract first column (model name)
    models = []
    for line in lines[1:]:
        parts = line.split()
        if parts:
            models.append(parts[0])

    if not models:
        raise OllamaCommandError("No models found in 'ollama ls' output.")

    return models


def create_model(model_name: str, modelfile_path: str) -> None:
    """
    Create a new Ollama model using the specified Modelfile.

    Runs the command: ollama create <model_name> -f <modelfile_path>

    Args:
        model_name: The name of the new model to create.
        modelfile_path: The path to the Modelfile to use.

    Raises:
        OllamaNotFoundError: If 'ollama' is not installed.
        OllamaCommandError: If the command fails.
    """
    if not check_ollama_installed():
        raise OllamaNotFoundError("'ollama' command not found. Is Ollama installed?")

    try:
        result = subprocess.run(
            ["ollama", "create", model_name, "-f", modelfile_path],
            capture_output=True,
            text=True,
            check=True,
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        raise OllamaCommandError(
            f"'ollama create' failed: {e.stderr or e.stdout}"
        ) from e


def delete_model(model_name: str) -> None:
    """
    Delete an Ollama model.

    Runs the command: ollama rm <model_name>

    Args:
        model_name: The name of the model to delete.

    Raises:
        OllamaNotFoundError: If 'ollama' is not installed.
        OllamaCommandError: If the command fails.
    """
    if not check_ollama_installed():
        raise OllamaNotFoundError("'ollama' command not found. Is Ollama installed?")

    try:
        subprocess.run(
            ["ollama", "rm", model_name],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise OllamaCommandError(
            f"'ollama rm' failed: {e.stderr or e.stdout}"
        ) from e