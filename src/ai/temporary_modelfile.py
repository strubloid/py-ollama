"""Temporary Modelfile context manager."""

from typing import Optional

from .modelfile import write_temporary_modelfile, cleanup_modelfile


class TemporaryModelfile:
    """
    Context manager for creating and cleaning up temporary Modelfiles.

    Usage:
        with TemporaryModelfile(content) as modelfile_path:
            ollama.create_model("my-model", modelfile_path)
        # File is automatically cleaned up after the with block
    """

    def __init__(self, content: str) -> None:
        """
        Initialize the context manager.

        Args:
            content: The Modelfile content to write.
        """
        self.content = content
        self.file_path: Optional[str] = None

    def __enter__(self) -> str:
        """
        Create the temporary Modelfile.

        Returns:
            The path to the temporary Modelfile.
        """
        self.file_path = write_temporary_modelfile(self.content)
        return self.file_path

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Clean up the temporary Modelfile.

        Args:
            exc_type: Exception type if an exception occurred.
            exc_val: Exception value if an exception occurred.
            exc_tb: Exception traceback if an exception occurred.
        """
        if self.file_path:
            cleanup_modelfile(self.file_path)