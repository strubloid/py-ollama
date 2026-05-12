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
    num_gpu: int = 0,
) -> str:
    lines = [
        f"PARAMETER num_ctx {num_ctx}",
        f"PARAMETER num_predict {num_predict}",
        f"PARAMETER num_gpu {num_gpu}",
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
    num_ctx=256,
    num_predict=4,
    temperature=0.0,
    top_p=1.0,
    top_k=1,
    repeat_penalty=1.0,
    repeat_last_n=0,
    seed=42,
    stop=[],
    num_gpu=128,
)

CODER_CONFIG = _build_config(
    num_ctx=1024,
    num_predict=24,
    temperature=0.0,
    top_p=1.0,
    top_k=1,
    repeat_penalty=1.0,
    repeat_last_n=0,
    seed=42,
    stop=[],
    num_gpu=128,
)

CODER_FAST_CONFIG = _build_config(
    num_ctx=128,
    num_predict=8,
    temperature=0.9,
    top_p=0.99,
    top_k=1,
    repeat_penalty=1.5,
    repeat_last_n=2,
    seed=-1,
    stop=[],
    num_gpu=128,
)

EXPLAINED_CONFIG = _build_config(
    num_ctx=512,
    num_predict=16,
    temperature=0.1,
    top_p=0.9,
    top_k=5,
    repeat_penalty=1.0,
    repeat_last_n=0,
    seed=42,
    stop=[],
    num_gpu=128,
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
    num_ctx=1024,
    num_predict=48,
    temperature=0.15,
    top_p=0.8,
    top_k=20,
    repeat_penalty=1.08,
    repeat_last_n=96,
    seed=-1,
    stop=[],
    num_gpu=128,
)

CODER_SYSTEM = """Expert coding agent. Core: correct, efficient, production-ready code.
1. Read code completely first.
2. Plan ALL changes—no partial fixes.
3. Execute complete solution.
4. Validate: compile, lint, test.
Report what changed. Never claim success unless working."""


CODER_FAST_CONFIG = _build_config(
    num_ctx=256,
    num_predict=4,
    temperature=0.0,
    top_p=1.0,
    top_k=1,
    repeat_penalty=1.0,
    repeat_last_n=0,
    seed=42,
    stop=[],
    num_gpu=128,
)

CODER_FAST_SYSTEM = """Quick coding assistant. Correctness first. Minimal changes. No invented APIs. Provide working code only."""


EXPLAINED_CONFIG = _build_config(
    num_ctx=512,
    num_predict=32,
    temperature=0.2,
    top_p=0.85,
    top_k=30,
    repeat_penalty=1.1,
    repeat_last_n=128,
    seed=-1,
    stop=[],
    num_gpu=128,
)

EXPLAINED_SYSTEM = """Coding teacher. For each task:
1. Explain problem and assumptions.
2. Walk through approach with trade-offs.
3. Show code with reasoning.
4. Note edge cases and testing.

Be concise but thorough."""


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