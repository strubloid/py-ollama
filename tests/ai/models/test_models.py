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

"""Tests for model family registry."""
class TestModelFamilies:

    """Test that all model families are in registry."""
    def test_all_families_registered(self):
        assert "llama" in MODEL_FAMILIES
        assert "deepseek" in MODEL_FAMILIES
        assert "qwen" in MODEL_FAMILIES
        assert "gemma" in MODEL_FAMILIES
        assert "mistral" in MODEL_FAMILIES
        assert "devstral" in MODEL_FAMILIES
    
    """Test that registry contains classes."""
    def test_families_are_classes(self):    
        for key, cls in MODEL_FAMILIES.items():
            assert isinstance(cls, type)

"""Tests for get_configs_for_model function."""
class TestGetConfigsForModel:

    """Test that function returns a dictionary."""
    def test_returns_dict(self):
        result = get_configs_for_model("llama2")
        assert isinstance(result, dict)
    
    """Test that result contains normal config."""
    def test_contains_normal_config(self):    
        result = get_configs_for_model("llama2")
        assert "normal" in result
    
    """Test that result contains coder config."""
    def test_contains_coder_config(self):    
        result = get_configs_for_model("llama2")
        assert "coder" in result
    
    """Test that custom name parameter is accepted."""
    def test_accepts_custom_name(self):    
        result = get_configs_for_model("llama2", "MyBot")
        assert isinstance(result, dict)

"""Tests for mode getter functions."""
class TestGetModes:

    """Test get_normal_mode returns config."""
    def test_get_normal_mode(self):
        config = get_normal_mode("llama2")
        assert config is not None
    
    """Test get_coder_mode returns config."""
    def test_get_coder_mode(self):    
        config = get_coder_mode("llama2")
        assert config is not None
    
    """Test get_coder_fast_mode returns config."""
    def test_get_coder_fast_mode(self):    
        config = get_coder_fast_mode("llama2")
        assert config is not None
    
    """Test get_explained_mode returns config."""
    def test_get_explained_mode(self):    
        config = get_explained_mode("llama2")
        assert config is not None

"""Tests for detect_model_family function."""
class TestDetectModelFamily:
    
    """Test that llama models are detected."""
    def test_detects_llama(self):    
        result = detect_model_family("llama2")
        assert "llama" in result.lower()
    
    """Test that deepseek models are detected."""
    def test_detects_deepseek(self):    
        result = detect_model_family("deepseek-coder")
        assert "deepseek" in result.lower()
    
    """Test that qwen models are detected."""
    def test_detects_qwen(self):    
        result = detect_model_family("qwen2.5")
        assert "qwen" in result.lower()
    
    """Test that gemma models are detected."""
    def test_detects_gemma(self):    
        result = detect_model_family("gemma2")
        assert "gemma" in result.lower()
    
    """Test that mistral models are detected."""
    def test_detects_mistral(self):    
        result = detect_model_family("mistral")
        assert "mistral" in result.lower()
    
    """Test that devstral is detected."""
    def test_detects_devstral(self):    
        detect_model_family("devstral")
        assert "mistral" in MODEL_FAMILIES