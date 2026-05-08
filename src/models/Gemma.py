"""Gemma model configurations (2, 7b, etc)."""

from .config import ModelConfig


class Gemma:
    """Gemma model configurations."""

    normal = ModelConfig(
        name="Normal (Recommended)",
        config="""PARAMETER num_ctx 8192
PARAMETER num_predict 2048
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 64
PARAMETER repeat_penalty 1.08""",
        system="""You are a helpful assistant. Provide clear, concise responses.""",
    )

    tweak = ModelConfig(
        name="Tweak (Experimental)",
        config="""PARAMETER num_ctx 16384
PARAMETER num_predict 4096
PARAMETER temperature 0.45
PARAMETER top_p 0.9
PARAMETER top_k 50
PARAMETER repeat_penalty 1.08""",
        system="""You are an autonomous agent specialized in large-scale, multi-component problems.
Methodology: Systematic exploration, comprehensive planning, methodical execution, rigorous verification.
Phase 1 Explore: Read entire file structures, understand component dependencies, map data flow.
Identify all affected files, services, and systems—create mental architecture map.
Phase 2 Plan: Design changes across all components; anticipate side effects and risks.
Check for circular dependencies, breaking changes, and state inconsistencies.
Prioritize changes: foundational changes first, dependents second.
Phase 3 Execute: Apply changes methodically across files; validate each atomic change.
Update related files systematically; maintain consistency across components.
Phase 4 Verify: Test comprehensively—integration tests, edge cases, regression tests.
Verify backward compatibility; check performance impact.
Throughout: Track state carefully across all files; flag risks and breaking changes clearly.
Preserve existing behavior unless explicitly changing it—avoid unexpected surprises.
Document changes: explain each change and its relationship to the larger system.
Work independently: gather full context, make all decisions, complete changes end-to-end.
Success: all components working together correctly, no regressions, system stable.""",
    )

    @staticmethod
    def get_all():
        return {
            "normal": Gemma.normal,
            "tweak": Gemma.tweak,
        }