"""Tests for ollama check module."""

import pytest
from unittest.mock import patch
from ai.ollama.check import check_ollama_installed, require_ollama
from ai.ollama.exceptions import OllamaNotFoundError


class TestCheckOllamaInstalled:
    """Tests for check_ollama_installed function."""

    @patch("shutil.which")
    def test_returns_true_when_ollama_found(self, mock_which):
        """Test that True is returned when ollama is found."""
        mock_which.return_value = "/usr/bin/ollama"
        assert check_ollama_installed() is True
        mock_which.assert_called_once_with("ollama")

    @patch("shutil.which")
    def test_returns_false_when_ollama_not_found(self, mock_which):
        """Test that False is returned when ollama is not found."""
        mock_which.return_value = None
        assert check_ollama_installed() is False

    @patch("shutil.which")
    def test_ollama_check_called_with_correct_command(self, mock_which):
        """Test that shutil.which is called with 'ollama'."""
        check_ollama_installed()
        mock_which.assert_called_with("ollama")


class TestRequireOllama:
    """Tests for require_ollama function."""

    @patch("ai.ollama.check.check_ollama_installed")
    def test_does_not_raise_when_ollama_installed(self, mock_installed):
        """Test that no exception is raised when ollama is installed."""
        mock_installed.return_value = True
        require_ollama()  # Should not raise

    @patch("ai.ollama.check.check_ollama_installed")
    def test_raises_when_ollama_not_installed(self, mock_installed):
        """Test that OllamaNotFoundError is raised when ollama is not installed."""
        mock_installed.return_value = False
        with pytest.raises(OllamaNotFoundError) as exc_info:
            require_ollama()
        assert "ollama" in str(exc_info.value).lower()