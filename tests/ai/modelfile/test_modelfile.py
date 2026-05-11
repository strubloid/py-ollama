"""Tests for modelfile module."""

import pytest
from ai.modelfile.modelfile import build_modelfile_content, write_temporary_modelfile, cleanup_modelfile
from ai.modelfile.error import ModelfileError

"""Tests for build_modelfile_content function."""
class TestBuildModelfileContent:

    """Test successful Modelfile generation."""
    def test_success(self):
        content = build_modelfile_content(
            base_model="llama2",
            config_params="PARAMETER temperature 0.7",
            system_prompt="You are a helpful assistant.",
        )

        assert "FROM llama2" in content
        assert "PARAMETER temperature 0.7" in content
        assert 'SYSTEM "' in content
        assert "You are a helpful assistant." in content
    
    """Test Modelfile with multiline system prompt."""
    def test_multiline_system_prompt(self):    
        content = build_modelfile_content(
            base_model="mistral",
            config_params="PARAMETER temperature 0.5",
            system_prompt="Line 1\nLine 2\nLine 3",
        )

        assert "FROM mistral" in content
        assert "Line 1\nLine 2\nLine 3" in content
    
    """Test that empty base_model raises ModelfileError."""
    def test_empty_base_model_raises_error(self):    
        with pytest.raises(ModelfileError):
            build_modelfile_content("", "PARAMETER temp 0.7", "prompt")
    
    """Test that empty config raises ModelfileError."""
    def test_empty_config_raises_error(self):    
        with pytest.raises(ModelfileError):
            build_modelfile_content("llama2", "", "prompt")
    
    """Test that empty system raises ModelfileError."""
    def test_empty_system_raises_error(self):    
        with pytest.raises(ModelfileError):
            build_modelfile_content("llama2", "PARAMETER temp 0.7", "")
    
    """Test that whitespace-only base_model raises error."""
    def test_whitespace_base_model_raises_error(self):    
        with pytest.raises(ModelfileError):
            build_modelfile_content("   ", "PARAMETER temp 0.7", "prompt")

"""Tests for write_temporary_modelfile function."""
class TestWriteTemporaryModelfile:

    """Test that temporary file is created."""
    def test_creates_file(self):
        path = write_temporary_modelfile("FROM llama2")

        import os
        assert os.path.exists(path)
        with open(path, "r") as f:
            assert f.read() == "FROM llama2"
        os.remove(path)
    
    """Test that file has .Modelfile suffix."""
    def test_has_modelfile_suffix(self):    
        path = write_temporary_modelfile("content")
        import os
        assert path.endswith(".Modelfile")
        os.remove(path)

"""Tests for cleanup_modelfile function."""
class TestCleanupModelfile:

    """Test that file is deleted."""
    def test_deletes_file(self):
        path = write_temporary_modelfile("content")
        import os
        assert os.path.exists(path)

        cleanup_modelfile(path)
        assert not os.path.exists(path)
    
    """Test that cleanup handles nonexistent file gracefully."""
    def test_handles_nonexistent_file(self):
        
        cleanup_modelfile("/nonexistent/file")  # Should not raise