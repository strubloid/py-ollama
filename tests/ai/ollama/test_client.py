"""Tests for ollama client module."""

import subprocess

import pytest
from unittest.mock import patch, MagicMock
from ai.ollama.client import OllamaClient
from ai.ollama.exceptions import OllamaCommandError


@pytest.fixture
def client():
    """Create an OllamaClient instance."""
    return OllamaClient()


class TestListModels:
    """Tests for list_models method."""

    @patch("subprocess.run")
    @patch("ai.ollama.client.require_ollama")
    def test_returns_list_of_model_names(self, mock_require, mock_run, client):
        """Test that list_models returns a list of model names."""
        mock_result = MagicMock()
        mock_result.stdout = """NAME                ID          SIZE      MODIFIED
llama2              abc123      3.8GB     2 days ago
mistral             def456      4.1GB     3 days ago
"""
        mock_run.return_value = mock_result

        models = client.list_models()

        assert models == ["llama2", "mistral"]

    @patch("subprocess.run")
    @patch("ai.ollama.client.require_ollama")
    def test_raises_when_no_models(self, mock_require, mock_run, client):
        """Test that OllamaCommandError is raised when no models found."""
        mock_result = MagicMock()
        mock_result.stdout = "NAME"
        mock_run.return_value = mock_result

        with pytest.raises(OllamaCommandError):
            client.list_models()

    @patch("subprocess.run")
    @patch("ai.ollama.client.require_ollama")
    def test_raises_on_command_failure(self, mock_require, mock_run, client):
        """Test that OllamaCommandError is raised on command failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "ollama ls", stderr="command failed")

        with pytest.raises(OllamaCommandError):
            client.list_models()


class TestCreateModel:
    """Tests for create_model method."""

    @patch("subprocess.run")
    @patch("ai.ollama.client.require_ollama")
    def test_creates_model_successfully(self, mock_require, mock_run, client):
        """Test that create_model runs successfully."""
        mock_result = MagicMock()
        mock_result.stdout = "Creating model... Done"
        mock_run.return_value = mock_result

        client.create_model("my-model", "/path/to/modelfile")

        mock_run.assert_called_once_with(
            ["ollama", "create", "my-model", "-f", "/path/to/modelfile"],
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("subprocess.run")
    @patch("ai.ollama.client.require_ollama")
    def test_raises_on_command_failure(self, mock_require, mock_run, client):
        """Test that OllamaCommandError is raised on failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "cmd", stderr="create failed")

        with pytest.raises(OllamaCommandError):
            client.create_model("my-model", "/path/to/modelfile")


class TestDeleteModel:
    """Tests for delete_model method."""

    @patch("subprocess.run")
    @patch("ai.ollama.client.require_ollama")
    def test_deletes_model_successfully(self, mock_require, mock_run, client):
        """Test that delete_model runs successfully."""
        mock_result = MagicMock()
        mock_run.return_value = mock_result

        client.delete_model("my-model")

        mock_run.assert_called_once_with(
            ["ollama", "rm", "my-model"],
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("subprocess.run")
    @patch("ai.ollama.client.require_ollama")
    def test_raises_on_command_failure(self, mock_require, mock_run, client):
        """Test that OllamaCommandError is raised on failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "cmd", stderr="delete failed")

        with pytest.raises(OllamaCommandError):
            client.delete_model("my-model")