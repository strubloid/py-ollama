"""Tests for config module."""

import pytest
from ai.config import detect_model_family, ModelConfig


class TestDetectModelFamily:
    """Tests for detect_model_family function."""

    def test_returns_string(self):
        """Test that function returns a string."""
        result = detect_model_family("llama2")
        assert isinstance(result, str)

    def test_detects_known_families(self):
        """Test detection of known model families."""
        families = [
            ("llama2", "llama"),
            ("llama3", "llama"),
            ("llama3.1", "llama"),
            ("deepseek-coder", "deepseek"),
            ("deepseek-v2", "deepseek"),
            ("qwen2", "qwen"),
            ("qwen2.5", "qwen"),
            ("gemma2", "gemma"),
            ("gemma3", "gemma"),
            ("mistral", "mistral"),
        ]

        for model, expected_family in families:
            result = detect_model_family(model)
            assert expected_family.lower() in result.lower(), f"Expected {expected_family} in {result}"


class TestModelConfig:
    """Tests for ModelConfig dataclass."""

    def test_has_required_fields(self):
        """Test that ModelConfig has required fields."""
        config = ModelConfig(
            name="test",
            config="PARAMETER temperature 0.7",
            system="You are a helpful assistant.",
        )
        assert config.name == "test"
        assert config.system == "You are a helpful assistant."
        assert config.config == "PARAMETER temperature 0.7"

    def test_is_frozen(self):
        """Test that ModelConfig is frozen (immutable)."""
        config = ModelConfig(
            name="test",
            system="system",
            config="config",
        )
        with pytest.raises(Exception):  # FrozenInstanceError
            config.name = "modified"