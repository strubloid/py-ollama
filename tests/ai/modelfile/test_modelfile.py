"""Tests for modelfile module."""

import pytest
from ai.modelfile.modelfile import build_modelfile_content, write_temporary_modelfile, cleanup_modelfile
from ai.modelfile.error import ModelfileError


class TestBuildModelfileContent:
    """Tests for build_modelfile_content function."""

    def test_success(self):
        """Test successful Modelfile generation."""
        content = build_modelfile_content(
            base_model="llama2",
            config_params="PARAMETER temperature 0.7",
            system_prompt="You are a helpful assistant.",
        )

        assert "FROM llama2" in content
        assert "PARAMETER temperature 0.7" in content
        assert 'SYSTEM "' in content
        assert "You are a helpful assistant." in content

    def test_multiline_system_prompt(self):
        """Test Modelfile with multiline system prompt."""
        content = build_modelfile_content(
            base_model="mistral",
            config_params="PARAMETER temperature 0.5",
            system_prompt="Line 1\nLine 2\nLine 3",
        )

        assert "FROM mistral" in content
        assert "Line 1\nLine 2\nLine 3" in content

    def test_empty_base_model_raises_error(self):
        """Test that empty base_model raises ModelfileError."""
        with pytest.raises(ModelfileError):
            build_modelfile_content("", "PARAMETER temp 0.7", "prompt")

    def test_empty_config_raises_error(self):
        """Test that empty config raises ModelfileError."""
        with pytest.raises(ModelfileError):
            build_modelfile_content("llama2", "", "prompt")

    def test_empty_system_raises_error(self):
        """Test that empty system raises ModelfileError."""
        with pytest.raises(ModelfileError):
            build_modelfile_content("llama2", "PARAMETER temp 0.7", "")

    def test_whitespace_base_model_raises_error(self):
        """Test that whitespace-only base_model raises error."""
        with pytest.raises(ModelfileError):
            build_modelfile_content("   ", "PARAMETER temp 0.7", "prompt")


class TestWriteTemporaryModelfile:
    """Tests for write_temporary_modelfile function."""

    def test_creates_file(self):
        """Test that temporary file is created."""
        path = write_temporary_modelfile("FROM llama2")

        import os
        assert os.path.exists(path)
        with open(path, "r") as f:
            assert f.read() == "FROM llama2"
        os.remove(path)

    def test_has_modelfile_suffix(self):
        """Test that file has .Modelfile suffix."""
        path = write_temporary_modelfile("content")
        import os
        assert path.endswith(".Modelfile")
        os.remove(path)


class TestCleanupModelfile:
    """Tests for cleanup_modelfile function."""

    def test_deletes_file(self):
        """Test that file is deleted."""
        path = write_temporary_modelfile("content")
        import os
        assert os.path.exists(path)

        cleanup_modelfile(path)
        assert not os.path.exists(path)

    def test_handles_nonexistent_file(self):
        """Test that cleanup handles nonexistent file gracefully."""
        cleanup_modelfile("/nonexistent/file")  # Should not raise