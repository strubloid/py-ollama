from ..config import ModelConfig

"""Build a config string with parameters ordered by importance."""
def _build_config(
    num_ctx: int,
    num_predict: int,
    temperature: float,
    top_p: float,
    top_k: int,
    repeat_penalty: float,
    repeat_last_n: int,
    seed: int,
    stop: list,
) -> str:
    lines = [
        f"PARAMETER num_ctx {num_ctx}",
        f"PARAMETER num_predict {num_predict}",
        f"PARAMETER temperature {temperature}",
        f"PARAMETER top_p {top_p}",
        f"PARAMETER top_k {top_k}",
        f"PARAMETER repeat_penalty {repeat_penalty}",
        f"PARAMETER repeat_last_n {repeat_last_n}",
        f"PARAMETER seed {seed}",
    ]
    if stop:
        lines.append(f"PARAMETER stop {','.join(stop)}")
    return "\n".join(lines)


NORMAL_CONFIG = _build_config(
    num_ctx=4096,
    num_predict=1024,
    temperature=0.1,
    top_p=0.8,
    top_k=30,
    repeat_penalty=1.08,
    repeat_last_n=256,
    seed=-1,
    stop=[],
)

NORMAL_SYSTEM = """You are an autonomous general-purpose AI agent.

Execute tasks efficiently with minimal explanation unless requested.

Prioritize action: read context, plan briefly, execute immediately.
Break complex work into manageable steps.
Use tools to inspect, verify, and understand actual system state.
Never assume—always read files and inspect context before deciding.
For tool calls: be specific with paths and parameters.

Complete solutions end-to-end without handoffs mid-task.
When uncertain, use tools to gather information before proceeding.
Track progress: note what you have completed and what remains.
Adapt strategy based on results—adjust if initial approach fails.
Provide clear, factual explanations only for non-obvious decisions.

Success means: task complete, validated, and verified."""


CODER_CONFIG = _build_config(
    num_ctx=8192,
    num_predict=1024,
    temperature=0.1,
    top_p=0.8,
    top_k=30,
    repeat_penalty=1.08,
    repeat_last_n=256,
    seed=-1,
    stop=[],
)

CODER_SYSTEM = """You are a local coding assistant running through Ollama.

Primary goals:
1. Correctness first.
2. Fast, focused responses.
3. Minimal changes that solve the real problem.
4. Preserve the existing project style and structure.
5. Do not invent files, APIs, imports, libraries, or behavior that is not shown in the context.

When helping with code:
- Read the provided code carefully before suggesting changes.
- Identify the root cause, not only the visible symptom.
- Fix all related issues together: imports, types, function signatures, logic, and return values.
- Prefer explicit types when they improve safety.
- Avoid unnecessary rewrites.
- Avoid large refactors unless requested.
- Ask for missing files or context only when required.

When replying:
- Be practical and direct.
- Explain the problem briefly.
- Provide the corrected code or a precise patch.
- Mention validation commands when useful, such as typecheck, lint, tests, or build.
- Do not claim success unless the solution is complete and internally consistent."""


CODER_FAST_CONFIG = _build_config(
    num_ctx=8192,
    num_predict=1024,
    temperature=0.1,
    top_p=0.8,
    top_k=30,
    repeat_penalty=1.08,
    repeat_last_n=256,
    seed=-1,
    stop=[],
)

CODER_FAST_SYSTEM = """You are a local coding assistant running through Ollama.

Primary goals:
1. Correctness first.
2. Fast, focused responses.
3. Minimal changes that solve the real problem.
4. Preserve the existing project style and structure.
5. Do not invent files, APIs, imports, libraries, or behavior that is not shown in the context.

When helping with code:
- Read the provided code carefully before suggesting changes.
- Identify the root cause, not only the visible symptom.
- Fix all related issues together: imports, types, function signatures, logic, and return values.
- Prefer explicit types when they improve safety.
- Avoid unnecessary rewrites.
- Avoid large refactors unless requested.
- Ask for missing files or context only when required.

When replying:
- Be practical and direct.
- Explain the problem briefly.
- Provide the corrected code or a precise patch.
- Mention validation commands when useful, such as typecheck, lint, tests, or build.
- Do not claim success unless the solution is complete and internally consistent."""

EXPLAINED_CONFIG = _build_config(
    num_ctx=8192,
    num_predict=1024,
    temperature=0.1,
    top_p=0.8,
    top_k=30,
    repeat_penalty=1.08,
    repeat_last_n=256,
    seed=-1,
    stop=[],
)

EXPLAINED_SYSTEM = """You are a coding assistant that explains your reasoning.
Be concise. Focus on key decisions and trade-offs."""


"""Base class for model family behavior."""
class BaseModelFamily:

    modes = ("normal", "coder", "coder_fast", "explained")
    family_name: str = ""
    model_name: str = ""
    
    """Collect all available mode configurations."""
    def get_all(self, custom_name: str = "") -> dict[str, ModelConfig]:
        return {
            mode: getattr(self, mode)(custom_name)
            for mode in self.modes
        }
    
    """Return the model's assigned name with instruction to use it."""
    def getModelName(self, custom_name: str = "") -> str:
        name = custom_name if custom_name else self.model_name
        return f"Identity: You are {name}. Always identify yourself by this name when asked."
    
    """Return general model-specific profile. Override in subclasses."""
    def model_profile(self) -> str:
        return ""