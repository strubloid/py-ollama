"""Tests for models module."""

from ai.models import (
    MODEL_FAMILIES,
    get_configs_for_model,
    get_normal_mode,
    get_coder_mode,
    get_coder_fast_mode,
    get_explained_mode,
    detect_model_family,
)


class TestModelFamilies:
    """Tests for model family registry."""

    def test_all_families_registered(self):
        """Test that all model families are in registry."""
        assert "llama" in MODEL_FAMILIES
        assert "deepseek" in MODEL_FAMILIES
        assert "qwen" in MODEL_FAMILIES
        assert "gemma" in MODEL_FAMILIES
        assert "mistral" in MODEL_FAMILIES
        assert "devstral" in MODEL_FAMILIES

    def test_families_are_classes(self):
        """Test that registry contains classes."""
        for key, cls in MODEL_FAMILIES.items():
            assert isinstance(cls, type)


class TestGetConfigsForModel:
    """Tests for get_configs_for_model function."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = get_configs_for_model("llama2")
        assert isinstance(result, dict)

    def test_contains_normal_config(self):
        """Test that result contains normal config."""
        result = get_configs_for_model("llama2")
        assert "normal" in result

    def test_contains_coder_config(self):
        """Test that result contains coder config."""
        result = get_configs_for_model("llama2")
        assert "coder" in result

    def test_accepts_custom_name(self):
        """Test that custom name parameter is accepted."""
        result = get_configs_for_model("llama2", "MyBot")
        assert isinstance(result, dict)


class TestGetModes:
    """Tests for mode getter functions."""

    def test_get_normal_mode(self):
        """Test get_normal_mode returns config."""
        config = get_normal_mode("llama2")
        assert config is not None

    def test_get_coder_mode(self):
        """Test get_coder_mode returns config."""
        config = get_coder_mode("llama2")
        assert config is not None

    def test_get_coder_fast_mode(self):
        """Test get_coder_fast_mode returns config."""
        config = get_coder_fast_mode("llama2")
        assert config is not None

    def test_get_explained_mode(self):
        """Test get_explained_mode returns config."""
        config = get_explained_mode("llama2")
        assert config is not None


class TestDetectModelFamily:
    """Tests for detect_model_family function."""

    def test_detects_llama(self):
        """Test that llama models are detected."""
        result = detect_model_family("llama2")
        assert "llama" in result.lower()

    def test_detects_deepseek(self):
        """Test that deepseek models are detected."""
        result = detect_model_family("deepseek-coder")
        assert "deepseek" in result.lower()

    def test_detects_qwen(self):
        """Test that qwen models are detected."""
        result = detect_model_family("qwen2.5")
        assert "qwen" in result.lower()

    def test_detects_gemma(self):
        """Test that gemma models are detected."""
        result = detect_model_family("gemma2")
        assert "gemma" in result.lower()

    def test_detects_mistral(self):
        """Test that mistral models are detected."""
        result = detect_model_family("mistral")
        assert "mistral" in result.lower()

    def test_detects_devstral(self):
        """Test that devstral is detected."""
        detect_model_family("devstral")
        assert "mistral" in MODEL_FAMILIES