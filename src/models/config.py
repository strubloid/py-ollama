"""Shared ModelConfig dataclass for all models."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ModelConfig:
    """Configuration for a specific model variant."""
    name: str
    config: str
    system: str
    description: str = ""

    def get_params_table(self) -> list[list[str]]:
        """Parse config into a table of parameter names and values."""
        lines = self.config.strip().split("\n")
        rows = []
        for line in lines:
            line = line.strip()
            if line.startswith("PARAMETER"):
                parts = line.split(None, 2)
                if len(parts) == 3:
                    rows.append([parts[1], parts[2]])
        return rows

    def get_system_preview(self, max_length: int = 80) -> str:
        """Get a preview of the system prompt."""
        preview = self.system.strip().split("\n")[0]
        if len(preview) > max_length:
            return preview[:max_length] + "..."
        return preview