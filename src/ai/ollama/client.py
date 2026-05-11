import subprocess

from .check import require_ollama
from .exceptions import OllamaCommandError

"""Client for interacting with Ollama CLI."""
class OllamaClient:
    
    """Get a list of available models from 'ollama ls'."""
    def list_models(self) -> list[str]:
        
        require_ollama()

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

        models = []
        for line in lines[1:]:
            parts = line.split()
            if parts:
                models.append(parts[0])

        if not models:
            raise OllamaCommandError("No models found in 'ollama ls' output.")

        return models
    
    """Create a new Ollama model using the specified Modelfile."""
    def create_model(self, model_name: str, modelfile_path: str) -> None:
        
        require_ollama()

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
    
    """Delete an Ollama model."""
    def delete_model(self, model_name: str) -> None:
        
        require_ollama()

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