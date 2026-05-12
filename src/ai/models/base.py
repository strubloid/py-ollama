from ..config import ModelConfig
from ..config.config_loader import get_model_params, get_system_prompt, config_to_string

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
    num_thread: int = 0,
    num_batch: int = 512,
    use_mlock: bool = True,
    use_mmap: bool = True,
    f16_kv: bool = True,
) -> str:
    lines = [
        f"PARAMETER num_ctx {num_ctx}",
        f"PARAMETER num_predict {num_predict}",
        f"PARAMETER num_gpu {num_gpu}",
        f"PARAMETER num_thread {num_thread}" if num_thread > 0 else "",
        f"PARAMETER num_batch {num_batch}",
        f"PARAMETER use_mlock {int(use_mlock)}",
        f"PARAMETER use_mmap {int(use_mmap)}",
        f"PARAMETER f16_kv {int(f16_kv)}",
        f"PARAMETER temperature {temperature}",
        f"PARAMETER top_p {top_p}",
        f"PARAMETER top_k {top_k}",
        f"PARAMETER repeat_penalty {repeat_penalty}",
        f"PARAMETER repeat_last_n {repeat_last_n}",
        f"PARAMETER seed {seed}",
    ]
    lines = [line for line in lines if line]
    if stop:
        lines.append(f"PARAMETER stop {','.join(stop)}")
    return "\n".join(lines)


def _get_config(mode: str) -> tuple[str, str]:
    """Get config string and system prompt for a mode from config files."""
    params = get_model_params(mode)
    system = get_system_prompt(mode)

    if params:
        config_str = config_to_string(params)
    else:
        config_str = _build_config(
            num_ctx=256,
            num_predict=32,
            temperature=0.0,
            top_p=1.0,
            top_k=1,
            repeat_penalty=1.0,
            repeat_last_n=0,
            seed=42,
            stop=[],
            num_gpu=64,
            num_batch=512,
            use_mlock=True,
            use_mmap=True,
            f16_kv=True,
        )

    if not system:
        system = "You are a helpful AI assistant."

    return config_str, system


NORMAL_CONFIG, NORMAL_SYSTEM = _get_config("normal")
CODER_CONFIG, CODER_SYSTEM = _get_config("coder")
CODER_FAST_CONFIG, CODER_FAST_SYSTEM = _get_config("coder_fast")
EXPLAINED_CONFIG, EXPLAINED_SYSTEM = _get_config("explained")


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