"""
Tests for the modelfile module.

Tests Modelfile generation, temporary file handling, and cleanup.
"""

import pytest
import os
from ai.modelfile import (
    build_modelfile_content,
    TemporaryModelfile,
    ModelfileError,
)


class TestBuildModelfileContent:
    """Tests for building Modelfile content."""

    def test_build_modelfile_content_success(self):
        """Test successful Modelfile generation."""
        content = build_modelfile_content(
            base_model="llama2",
            config_params="PARAMETER temperature 0.7\nPARAMETER top_p 0.9",
            system_prompt="You are a helpful assistant.",
        )

        assert "FROM llama2" in content
        assert "PARAMETER temperature 0.7" in content
        assert "PARAMETER top_p 0.9" in content
        assert 'SYSTEM "' in content
        assert "You are a helpful assistant." in content

    def test_build_modelfile_content_multiline(self):
        """Test Modelfile with multiline system prompt."""
        content = build_modelfile_content(
            base_model="mistral",
            config_params="PARAMETER temperature 0.5",
            system_prompt="Line 1\nLine 2\nLine 3",
        )

        assert "FROM mistral" in content
        assert "Line 1\nLine 2\nLine 3" in content

    def test_build_modelfile_empty_base_model(self):
        """Test that empty base_model raises an error."""
        with pytest.raises(ModelfileError):
            build_modelfile_content(
                base_model="",
                config_params="PARAMETER temperature 0.7",
                system_prompt="Prompt",
            )

    def test_build_modelfile_empty_config(self):
        """Test that empty config_params raises an error."""
        with pytest.raises(ModelfileError):
            build_modelfile_content(
                base_model="llama2",
                config_params="",
                system_prompt="Prompt",
            )

    def test_build_modelfile_empty_system(self):
        """Test that empty system_prompt raises an error."""
        with pytest.raises(ModelfileError):
            build_modelfile_content(
                base_model="llama2",
                config_params="PARAMETER temperature 0.7",
                system_prompt="",
            )


class TestTemporaryModelfile:
    """Tests for TemporaryModelfile context manager."""

    def test_temporary_modelfile_creates_file(self):
        """Test that the context manager creates a file."""
        content = "FROM llama2\nPARAMETER temperature 0.7"

        with TemporaryModelfile(content) as tmp_path:
            assert os.path.exists(tmp_path)
            with open(tmp_path, "r") as f:
                file_content = f.read()
            assert file_content == content

    def test_temporary_modelfile_cleanup(self):
        """Test that the context manager cleans up the file."""
        content = "FROM llama2\nPARAMETER temperature 0.7"

        tmp_path = None
        with TemporaryModelfile(content) as tmp:
            tmp_path = tmp
            assert os.path.exists(tmp_path)

        # After exiting the context, the file should be deleted
        assert not os.path.exists(tmp_path)

    def test_temporary_modelfile_creates_unique_files(self):
        """Test that multiple context managers create different files."""
        content1 = "FROM llama2\nPARAMETER temperature 0.7"
        content2 = "FROM mistral\nPARAMETER temperature 0.5"

        with TemporaryModelfile(content1) as tmp1:
            with TemporaryModelfile(content2) as tmp2:
                assert tmp1 != tmp2
                assert os.path.exists(tmp1)
                assert os.path.exists(tmp2)