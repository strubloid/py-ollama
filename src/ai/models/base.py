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
    num_predict=512,
    temperature=0.1,
    top_p=0.8,
    top_k=20,
    repeat_penalty=1.05,
    repeat_last_n=128,
    seed=-1,
    stop=[],
)

NORMAL_SYSTEM = """You are a helpful assistant. Be direct. Complete tasks efficiently with minimal explanation. Never assume—read context first. Use tools when needed. Success means: task done and verified."""


CODER_CONFIG = _build_config(
    num_ctx=4096,
    num_predict=512,
    temperature=0.1,
    top_p=0.8,
    top_k=20,
    repeat_penalty=1.05,
    repeat_last_n=128,
    seed=-1,
    stop=[],
)

CODER_SYSTEM = """You are a coding assistant. Write correct, efficient code. Read files completely first. Plan all changes before editing. Provide minimal, working solution. Validate: compile, lint, test."""


CODER_FAST_CONFIG = _build_config(
    num_ctx=4096,
    num_predict=256,
    temperature=0.1,
    top_p=0.8,
    top_k=20,
    repeat_penalty=1.05,
    repeat_last_n=128,
    seed=-1,
    stop=[],
)

CODER_FAST_SYSTEM = """Quick coding assistant. Write minimal working code. No explanation unless requested. Provide only what solves the problem."""


EXPLAINED_CONFIG = _build_config(
    num_ctx=4096,
    num_predict=512,
    temperature=0.1,
    top_p=0.8,
    top_k=20,
    repeat_penalty=1.05,
    repeat_last_n=128,
    seed=-1,
    stop=[],
)

EXPLAINED_SYSTEM = """Coding teacher. Be practical and concise. Explain key decisions and trade-offs. Focus on root causes, not symptoms. Show working code with brief reasoning."""


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