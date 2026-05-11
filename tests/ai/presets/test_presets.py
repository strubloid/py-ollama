"""Tests for presets module."""

from ai.presets import PRESETS, list_preset_names, get_preset_by_name


class TestPresetsExist:
    """Tests for preset existence."""

    def test_presets_not_empty(self):
        """Test that PRESETS list is not empty."""
        assert len(PRESETS) > 0

    def test_required_presets_exist(self):
        """Test that all required presets exist."""
        required = {"Balanced", "Coder", "CoderFast", "CoderBalanced", "Creative", "Long Context"}
        available = {p.name for p in PRESETS}
        assert required.issubset(available)

    def test_all_presets_have_fields(self):
        """Test that all presets have required fields."""
        for preset in PRESETS:
            assert preset.name
            assert preset.config
            assert preset.system

    def test_all_configs_have_parameters(self):
        """Test that all configs contain PARAMETER."""
        for preset in PRESETS:
            assert "PARAMETER" in preset.config

    def test_all_names_unique(self):
        """Test that preset names are unique."""
        names = [p.name for p in PRESETS]
        assert len(names) == len(set(names))


class TestPresetsList:
    """Tests for list_preset_names function."""

    def test_returns_list(self):
        """Test that list_preset_names returns a list."""
        names = list_preset_names()
        assert isinstance(names, list)

    def test_returns_all_preset_names(self):
        """Test that all preset names are returned."""
        names = list_preset_names()
        assert len(names) == len(PRESETS)

    def test_contains_balanced(self):
        """Test that Balanced is in the list."""
        assert "Balanced" in list_preset_names()


class TestGetPresetByName:
    """Tests for get_preset_by_name function."""

    def test_returns_preset(self):
        """Test that preset is returned for valid name."""
        preset = get_preset_by_name("Balanced")
        assert preset is not None
        assert preset.name == "Balanced"

    def test_returns_none_for_invalid(self):
        """Test that None is returned for invalid name."""
        preset = get_preset_by_name("Invalid")
        assert preset is None

    def test_case_sensitive(self):
        """Test that lookup is case-sensitive."""
        assert get_preset_by_name("balanced") is None
        assert get_preset_by_name("BALANCED") is None


class TestSpecificPresets:
    """Tests for specific preset values."""

    def test_balanced_config(self):
        """Test Balanced preset config values."""
        preset = get_preset_by_name("Balanced")
        assert "num_ctx 8192" in preset.config
        assert "temperature 0.7" in preset.config

    def test_coder_config(self):
        """Test Coder preset config values."""
        preset = get_preset_by_name("Coder")
        assert "temperature 0.25" in preset.config

    def test_coder_fast_config(self):
        """Test CoderFast preset has threading."""
        preset = get_preset_by_name("CoderFast")
        assert "num_thread" in preset.config
        assert "num_batch" in preset.config

    def test_creative_config(self):
        """Test Creative preset has high temperature."""
        preset = get_preset_by_name("Creative")
        assert "temperature 0.95" in preset.config

    def test_long_context_config(self):
        """Test Long Context has large context."""
        preset = get_preset_by_name("Long Context")
        assert "num_ctx 16384" in preset.config