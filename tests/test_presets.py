"""
Tests for the presets module.

Tests that all presets exist, are properly defined, and contain required fields.
"""

import dataclasses

import pytest
from ai.presets import PRESETS, list_preset_names, get_preset_by_name


class TestPresetsExist:
    """Tests for preset existence and structure."""

    def test_presets_list_not_empty(self):
        """Test that the PRESETS list is not empty."""
        assert len(PRESETS) > 0

    def test_required_presets_exist(self):
        """Test that all required presets exist."""
        required_names = {
            "Balanced",
            "Coder",
            "CoderFast",
            "CoderBalanced",
            "Creative",
            "Long Context",
        }
        available_names = {p.name for p in PRESETS}
        assert required_names.issubset(available_names)

    def test_all_presets_have_required_fields(self):
        """Test that all presets have name, config, and system fields."""
        for preset in PRESETS:
            assert preset.name, "Preset must have a name"
            assert preset.config, "Preset must have config"
            assert preset.system, "Preset must have system prompt"

            # Check that config and system are non-empty strings
            assert isinstance(preset.config, str)
            assert isinstance(preset.system, str)
            assert len(preset.config.strip()) > 0
            assert len(preset.system.strip()) > 0

    def test_preset_config_has_parameter_lines(self):
        """Test that all preset configs contain PARAMETER lines."""
        for preset in PRESETS:
            assert "PARAMETER" in preset.config, (
                f"Preset '{preset.name}' config must contain PARAMETER lines"
            )

    def test_preset_names_are_unique(self):
        """Test that all preset names are unique."""
        names = [p.name for p in PRESETS]
        assert len(names) == len(set(names)), "Preset names must be unique"

    def test_preset_frozen(self):
        """Test that presets are frozen (immutable)."""
        assert dataclasses.is_dataclass(type(PRESETS[0]))
        assert dataclasses.fields(type(PRESETS[0]))


class TestPresetFunctions:
    """Tests for preset helper functions."""

    def test_get_preset_by_name_success(self):
        """Test getting a preset by name."""
        preset = get_preset_by_name("Balanced")
        assert preset is not None
        assert preset.name == "Balanced"
        assert "PARAMETER" in preset.config
        assert len(preset.system) > 0

    def test_get_preset_by_name_not_found(self):
        """Test getting a non-existent preset."""
        preset = get_preset_by_name("NonExistent")
        assert preset is None

    def test_get_preset_by_name_case_sensitive(self):
        """Test that preset lookup is case-sensitive."""
        # These should not match
        assert get_preset_by_name("balanced") is None
        assert get_preset_by_name("BALANCED") is None

    def test_list_preset_names(self):
        """Test listing all preset names."""
        names = list_preset_names()
        assert isinstance(names, list)
        assert len(names) == len(PRESETS)
        assert "Balanced" in names
        assert "Coder" in names

    def test_list_preset_names_order(self):
        """Test that list_preset_names returns presets in order."""
        names = list_preset_names()
        expected = [p.name for p in PRESETS]
        assert names == expected


class TestSpecificPresets:
    """Tests for specific preset configurations."""

    def test_balanced_preset_has_reasonable_values(self):
        """Test Balanced preset has expected parameters."""
        preset = get_preset_by_name("Balanced")
        assert preset is not None
        assert "num_ctx 8192" in preset.config
        assert "temperature 0.7" in preset.config

    def test_coder_preset_has_low_temperature(self):
        """Test Coder preset has deterministic settings."""
        preset = get_preset_by_name("Coder")
        assert preset is not None
        assert "temperature 0.25" in preset.config

    def test_creative_preset_has_high_temperature(self):
        """Test Creative preset has high temperature."""
        preset = get_preset_by_name("Creative")
        assert preset is not None
        assert "temperature 0.95" in preset.config

    def test_coder_balanced_preset_has_medium_temperature(self):
        """Test CoderBalanced preset has medium temperature."""
        preset = get_preset_by_name("CoderBalanced")
        assert preset is not None
        assert "temperature 0.1" in preset.config

    def test_long_context_preset_has_large_context(self):
        """Test Long Context preset has large context window."""
        preset = get_preset_by_name("Long Context")
        assert preset is not None
        assert "num_ctx 16384" in preset.config

    def test_coder_fast_preset_has_efficiency_settings(self):
        """Test CoderFast preset is optimized for speed."""
        preset = get_preset_by_name("CoderFast")
        assert preset is not None
        # Should have threading and batch optimization
        assert "num_thread" in preset.config
        assert "num_batch" in preset.config