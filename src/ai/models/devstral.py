"""Devstral model family."""

from .base import BaseModelFamily, NORMAL_SYSTEM, CODER_SYSTEM, CODER_FAST_SYSTEM, EXPLAINED_SYSTEM


class Devstral(BaseModelFamily):
    family_name = "devstral"
    model_name = "devstral:latest"

    def normal(self, custom_name: str = "") -> dict:
        system = self.getModelName(custom_name) + "\n" + NORMAL_SYSTEM
        return {
            "base_model": self.model_name,
            "system_prompt": system,
        }

    def coder(self, custom_name: str = "") -> dict:
        system = self.getModelName(custom_name) + "\n" + CODER_SYSTEM
        return {
            "base_model": self.model_name,
            "system_prompt": system,
        }

    def coder_fast(self, custom_name: str = "") -> dict:
        system = self.getModelName(custom_name) + "\n" + CODER_FAST_SYSTEM
        return {
            "base_model": self.model_name,
            "system_prompt": system,
        }

    def explained(self, custom_name: str = "") -> dict:
        system = self.getModelName(custom_name) + "\n" + EXPLAINED_SYSTEM
        return {
            "base_model": self.model_name,
            "system_prompt": system,
        }


__all__ = ["Devstral"]