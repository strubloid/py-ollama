"""Tests for temporary modelfile module."""

import os
from ai.modelfile.temporary import TemporaryModelfile

"""Tests for TemporaryModelfile context manager."""
class TestTemporaryModelfile:

    """Test that file is created when entering context."""
    def test_creates_file_on_enter(self):
        content = "FROM llama2\nPARAMETER temperature 0.7"
        with TemporaryModelfile(content) as tmp_path:
            assert os.path.exists(tmp_path)
            with open(tmp_path, "r") as f:
                assert f.read() == content
    
    """Test that file is deleted after exiting context."""
    def test_cleans_up_file_on_exit(self):    
        content = "FROM llama2\nPARAMETER temperature 0.7"

        tmp_path = None
        with TemporaryModelfile(content) as tmp:
            tmp_path = tmp
            assert os.path.exists(tmp_path)

        assert not os.path.exists(tmp_path)
    
    """Test that each context manager creates a unique file."""
    def test_creates_unique_files(self):
        
        content1 = "FROM llama2\nPARAMETER temperature 0.7"
        content2 = "FROM mistral\nPARAMETER temperature 0.5"

        with TemporaryModelfile(content1) as tmp1:
            with TemporaryModelfile(content2) as tmp2:
                assert tmp1 != tmp2
                assert os.path.exists(tmp1)
                assert os.path.exists(tmp2)
    
    """Test that __enter__ returns the file path."""
    def test_returns_path(self):    
        with TemporaryModelfile("content") as path:
            assert isinstance(path, str)
            assert len(path) > 0