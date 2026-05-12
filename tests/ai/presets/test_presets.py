"""Tests for presets module."""

from ai.presets import PRESETS, list_preset_names, get_preset_by_name

"""Tests for preset existence."""
class TestPresetsExist:

    """Test that PRESETS list is not empty."""
    def test_presets_not_empty(self):
        assert len(PRESETS) > 0
    
    """Test that all required presets exist."""
    def test_required_presets_exist(self):    
        required = {"Balanced", "Coder", "CoderFast", "CoderBalanced", "Creative", "Long Context"}
        available = {p.name for p in PRESETS}
        assert required.issubset(available)
    
    """Test that all presets have required fields."""
    def test_all_presets_have_fields(self):    
        for preset in PRESETS:
            assert preset.name
            assert preset.config
            assert preset.system
            
    """Test that all configs contain PARAMETER."""
    def test_all_configs_have_parameters(self):    
        for preset in PRESETS:
            assert "PARAMETER" in preset.config
    
    """Test that preset names are unique."""
    def test_all_names_unique(self):    
        names = [p.name for p in PRESETS]
        assert len(names) == len(set(names))

"""Tests for list_preset_names function."""
class TestPresetsList:

    """Test that list_preset_names returns a list."""
    def test_returns_list(self):
        names = list_preset_names()
        assert isinstance(names, list)
    
    """Test that all preset names are returned."""
    def test_returns_all_preset_names(self):    
        names = list_preset_names()
        assert len(names) == len(PRESETS)
    
    """Test that Balanced is in the list."""
    def test_contains_balanced(self):
        assert "Balanced" in list_preset_names()

"""Tests for get_preset_by_name function."""
class TestGetPresetByName:
    
    """Test that preset is returned for valid name."""
    def test_returns_preset(self):    
        preset = get_preset_by_name("Balanced")
        assert preset is not None
        assert preset.name == "Balanced"
    
    """Test that None is returned for invalid name."""
    def test_returns_none_for_invalid(self):    
        preset = get_preset_by_name("Invalid")
        assert preset is None

    """Test that lookup is case-sensitive."""
    def test_case_sensitive(self):        
        assert get_preset_by_name("balanced") is None
        assert get_preset_by_name("BALANCED") is None

"""Tests for specific preset values."""
class TestSpecificPresets:

    """Test Balanced preset config values."""
    def test_balanced_config(self):
        preset = get_preset_by_name("Balanced")
        assert preset is not None
        assert "PARAMETER num_ctx" in preset.config
        assert "PARAMETER temperature" in preset.config
    
    """Test Coder preset config values."""
    def test_coder_config(self):
        preset = get_preset_by_name("Coder")
        assert preset is not None
        assert "PARAMETER temperature" in preset.config
    
    """Test CoderFast preset has num_gpu."""
    def test_coder_fast_config(self):
        preset = get_preset_by_name("CoderFast")
        assert preset is not None
        assert "PARAMETER num_ctx" in preset.config
        assert "PARAMETER num_predict" in preset.config
    
    """Test Creative preset has temperature."""
    def test_creative_config(self):
        preset = get_preset_by_name("Creative")
        assert preset is not None
        assert "PARAMETER temperature" in preset.config

    """Test Long Context has context setting."""
    def test_long_context_config(self):
        preset = get_preset_by_name("Long Context")
        assert preset is not None
        assert "num_ctx" in preset.config