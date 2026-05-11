"""Base extension interface for model extensions."""

from abc import ABC, abstractmethod


class BaseExtension(ABC):
    """Base class for model extensions."""

    @staticmethod
    @abstractmethod
    def get_normal(custom_name: str = "") -> str:
        """Get normal mode extension."""
        pass

    @staticmethod
    @abstractmethod
    def get_coder(custom_name: str = "") -> str:
        """Get coder mode extension."""
        pass

    @staticmethod
    @abstractmethod
    def get_coder_fast(custom_name: str = "") -> str:
        """Get coder_fast mode extension."""
        pass

    @staticmethod
    @abstractmethod
    def get_explained(custom_name: str = "") -> str:
        """Get explained mode extension."""
        pass