import sys
import json
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime


CONFIG_DIR = Path(__file__).parent.parent.parent / "configs"
MODEL_CONFIG_FILE = CONFIG_DIR / "model_config.json"
PRESETS_CONFIG_FILE = CONFIG_DIR / "presets.json"


@dataclass
class ModelBenchmark:
    name: str
    size_gb: float
    quantization: str
    available: bool
    benchmark_time: float
    tokens_generated: int
    tokens_per_second: float
    status: str
    error: str = ""


def run_command(cmd: list[str], timeout: int = 60) -> tuple[int, str, str]:
    """Run command and return (returncode, stdout, stderr)"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except Exception as e:
        return -1, "", str(e)


def get_available_models() -> list[dict]:
    """Get all models available in Ollama."""
    returncode, stdout, _ = run_command(["ollama", "list"])
    if returncode != 0:
        return []

    models = []
    lines = stdout.strip().split('\n')
    for line in lines[1:]:
        if line.strip():
            parts = line.split()
            if parts:
                name = parts[0]
                size_gb = float(parts[2].replace('GB', '').replace('MB', '')) / 1000 if 'MB' in parts[2] else float(parts[2].replace('GB', ''))
                models.append({
                    'name': name,
                    'size_gb': size_gb,
                    'size_display': parts[2]
                })
    return models


def get_model_info(model_name: str) -> dict:
    """Get detailed info about a model."""
    returncode, stdout, _ = run_command(["ollama", "show", model_name])
    if returncode != 0:
        return {}

    info = {}
    for line in stdout.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            info[key.strip().lower()] = value.strip()
    return info


def benchmark_model(model_name: str, warmup: bool = True) -> ModelBenchmark:
    """Run benchmark on a single model."""
    result = ModelBenchmark(
        name=model_name,
        size_gb=0,
        quantization="unknown",
        available=True,
        benchmark_time=0,
        tokens_generated=0,
        tokens_per_second=0,
        status="unknown"
    )

    if warmup:
        run_command(["ollama", "run", model_name, "ping"], timeout=30)
        time.sleep(0.5)

    test_prompts = [
        "What is 2+2?",
        "Hello",
        "OK"
    ]
    prompt = test_prompts[0]

    start = time.perf_counter()
    returncode, stdout, stderr = run_command(
        ["ollama", "run", "--verbose", model_name, prompt],
        timeout=60
    )
    elapsed = time.perf_counter() - start

    result.benchmark_time = elapsed

    if returncode == 0:
        result.status = "success"

        stdout_clean = ''.join(c for c in stdout if c.isprintable() or c in '\n\r\t')

        for line in stdout_clean.split('\n'):
            if 'eval count' in line.lower():
                try:
                    result.tokens_generated = int(line.split(':')[1].strip().split()[0])
                except Exception:
                    pass
            if 'eval rate' in line.lower():
                try:
                    rate_str = line.split(':')[1].strip().split()[0]
                    result.tokens_per_second = float(rate_str)
                except Exception:
                    pass

        if result.tokens_generated == 0:
            result.tokens_generated = len(stdout_clean.split())

        info = get_model_info(model_name)
        result.quantization = info.get('quantization', 'unknown')
        try:
            result.size_gb = float(info.get('size', '0').replace('GB', ''))
        except Exception:
            result.size_gb = 0

    else:
        result.status = "failed"
        result.error = stderr[:100] if stderr else "Unknown error"

    return result


def detect_hardware() -> dict:
    """Detect hardware capabilities."""
    hardware = {
        'gpu_name': 'Unknown',
        'vram_total_mb': 0,
        'vram_used_mb': 0,
        'bandwidth_gb_s': 0,
        'cuda_available': False,
        'tier': 'unknown'
    }

    returncode, stdout, _ = run_command(
        ["nvidia-smi", "--query-gpu=name,memory.total,memory.used",
         "--format=csv,noheader"],
        timeout=10
    )

    if returncode == 0 and stdout.strip():
        parts = [p.strip() for p in stdout.strip().split(',')]
        hardware['gpu_name'] = parts[0]

        try:
            hardware['vram_total_mb'] = int(parts[1].split()[0])
            hardware['vram_used_mb'] = int(parts[2].split()[0])
        except Exception:
            pass

        bandwidth_map = {
            "4090": 1008, "4080": 736, "4070": 504,
            "3090": 912, "3080": 760, "3060": 360
        }
        for gpu, bw in bandwidth_map.items():
            if gpu.lower() in hardware['gpu_name'].lower():
                hardware['bandwidth_gb_s'] = bw
                break

        hardware['cuda_available'] = True

        if hardware['vram_total_mb'] >= 24000:
            hardware['tier'] = 'high'
        elif hardware['vram_total_mb'] >= 12000:
            hardware['tier'] = 'medium'
        elif hardware['vram_total_mb'] >= 8000:
            hardware['tier'] = 'low'
        else:
            hardware['tier'] = 'minimal'

    return hardware


def select_best_config(benchmark: ModelBenchmark, hardware: dict) -> dict:
    """Select best configuration based on benchmark and hardware."""
    tier = hardware.get('tier', 'medium')
    speed = benchmark.tokens_per_second

    if tier == 'high':
        num_gpu = 128
        num_batch = 512
    elif tier == 'medium':
        num_gpu = 64
        num_batch = 512
    else:
        num_gpu = 32
        num_batch = 256

    if speed > 60:
        num_ctx = 128
        num_predict = 8
        temperature = 0.0
    elif speed > 30:
        num_ctx = 256
        num_predict = 32
        temperature = 0.0
    else:
        num_ctx = 512
        num_predict = 64
        temperature = 0.1

    return {
        'num_ctx': num_ctx,
        'num_predict': num_predict,
        'num_gpu': num_gpu,
        'num_batch': num_batch,
        'temperature': temperature,
        'top_p': 1.0,
        'top_k': 1,
        'repeat_penalty': 1.0,
        'repeat_last_n': 0,
        'seed': 42,
        'use_mlock': True,
        'use_mmap': True,
        'f16_kv': True
    }


def generate_model_config(benchmarks: list[ModelBenchmark], hardware: dict) -> dict:
    """Generate model configuration file."""
    best_benchmark = None
    for b in benchmarks:
        if b.status == 'success' and b.tokens_per_second > 0:
            if best_benchmark is None or b.tokens_per_second > best_benchmark.tokens_per_second:
                best_benchmark = b

    best_config = {}
    if best_benchmark:
        best_config = select_best_config(best_benchmark, hardware)
    else:
        best_config = select_best_config(
            ModelBenchmark(
                name="default", size_gb=9, quantization="Q4_K_M",
                available=True, benchmark_time=3, tokens_generated=10,
                tokens_per_second=30, status="success"
            ),
            hardware
        )

    recommended_model = best_benchmark.name if best_benchmark else "qwen2.5-coder:14b"

    return {
        "metadata": {
            "version": "1.0.0",
            "description": f"Auto-generated config for {hardware.get('gpu_name', 'Unknown GPU')}",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hardware_tier": hardware.get('tier', 'unknown'),
            "recommended_model": recommended_model
        },
        "model_params": {
            "normal": {
                "name": "Normal",
                "description": "Default configuration for general tasks",
                **best_config
            },
            "coder": {
                "name": "Coder",
                "description": "Configuration optimized for code generation",
                "num_ctx": best_config["num_ctx"] * 2,
                "num_predict": best_config["num_predict"] * 2,
                **{k: v for k, v in best_config.items() if k not in ("num_ctx", "num_predict")}
            },
            "coder_fast": {
                "name": "Coder Fast",
                "description": "Fast configuration for quick coding tasks",
                "num_ctx": max(128, best_config["num_ctx"] // 2),
                "num_predict": max(4, best_config["num_predict"] // 2),
                **{k: v for k, v in best_config.items() if k not in ("num_ctx", "num_predict")}
            },
            "explained": {
                "name": "Explained",
                "description": "Configuration with detailed explanations",
                "num_predict": best_config["num_predict"] * 2,
                **{k: v for k, v in best_config.items() if k not in ("num_predict",)}
            }
        },
        "system_prompts": {
            "normal": "You are a helpful assistant. Answer concisely and accurately.",
            "coder": "You are an expert coding assistant. Provide clean, efficient code.",
            "coder_fast": "Quick coding assistant. Correctness first. Minimal explanation.",
            "explained": "You are a coding teacher. Explain thoroughly with examples."
        },
        "benchmarks": [
            {
                "model": b.name,
                "status": b.status,
                "tokens_per_second": b.tokens_per_second,
                "tokens_generated": b.tokens_generated,
                "benchmark_time": b.benchmark_time,
                "quantization": b.quantization,
                "error": b.error
            }
            for b in benchmarks if b.status == "success"
        ]
    }


def generate_presets_config(benchmarks: list[ModelBenchmark], hardware: dict) -> dict:
    """Generate presets configuration file."""
    best_benchmark = None
    for b in benchmarks:
        if b.status == 'success' and b.tokens_per_second > 0:
            if best_benchmark is None or b.tokens_per_second > best_benchmark.tokens_per_second:
                best_benchmark = b

    best_config = {}
    if best_benchmark:
        best_config = select_best_config(best_benchmark, hardware)
    else:
        best_config = select_best_config(
            ModelBenchmark(
                name="default", size_gb=9, quantization="Q4_K_M",
                available=True, benchmark_time=3, tokens_generated=10,
                tokens_per_second=30, status="success"
            ),
            hardware
        )

    presets = {
        "balanced": {
            "name": "Balanced",
            "description": "Balanced configuration for general use",
            "config": _config_to_string(best_config),
            "system": "You are a helpful AI assistant. Be efficient and accurate."
        },
        "coder": {
            "name": "Coder",
            "description": "Configuration optimized for code generation",
            "config": _config_to_string({**best_config, "num_ctx": best_config["num_ctx"] * 2, "num_predict": best_config["num_predict"] * 2}),
            "system": "Expert coding assistant. Provide clean, production-ready code."
        },
        "coder_fast": {
            "name": "CoderFast",
            "description": "Fast configuration for quick tasks",
            "config": _config_to_string({**best_config, "num_ctx": max(128, best_config["num_ctx"] // 2), "num_predict": max(4, best_config["num_predict"] // 2)}),
            "system": "Quick coding assistant. Correctness first. Minimal changes."
        },
        "coder_balanced": {
            "name": "CoderBalanced",
            "description": "Balanced coding configuration",
            "config": _config_to_string({**best_config, "num_ctx": best_config["num_ctx"] * 2, "num_predict": best_config["num_predict"]}),
            "system": "Expert coding agent. Read completely, plan all changes, execute fully."
        },
        "creative": {
            "name": "Creative",
            "description": "Creative configuration for brainstorming",
            "config": _config_to_string({**best_config, "temperature": 0.7}),
            "system": "Creative solution designer. Transform vague ideas into concrete solutions."
        },
        "long_context": {
            "name": "Long Context",
            "description": "Configuration for long context tasks",
            "config": _config_to_string({**best_config, "num_ctx": best_config["num_ctx"] * 4, "num_predict": best_config["num_predict"] * 2}),
            "system": "Coding teacher. Explain with trade-offs and examples."
        }
    }

    return {
        "metadata": {
            "version": "1.0.0",
            "description": f"Auto-generated presets for {hardware.get('gpu_name', 'Unknown GPU')}",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hardware_tier": hardware.get('tier', 'unknown')
        },
        "presets": presets
    }


def _config_to_string(cfg: dict) -> str:
    lines = []
    for key, value in sorted(cfg.items()):
        if key in ('name', 'description'):
            continue
        if key == 'stop':
            lines.append(f"PARAMETER {key} []")
        elif isinstance(value, bool):
            lines.append(f"PARAMETER {key} {str(value).lower()}")
        elif isinstance(value, list):
            lines.append(f"PARAMETER {key} {value}")
        else:
            lines.append(f"PARAMETER {key} {value}")
    return "\n".join(lines)


def save_config(data: dict, filepath: Path) -> None:
    """Save configuration to file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)


def main():
    print("=" * 60)
    print("PY-OLLAMA CONFIG GENERATOR")
    print("=" * 60)

    print("\n[1/4] Detecting hardware...")
    hardware = detect_hardware()
    print(f"  GPU: {hardware.get('gpu_name', 'Unknown')}")
    print(f"  VRAM: {hardware.get('vram_used_mb', 0)} MB / {hardware.get('vram_total_mb', 0)} MB")
    print(f"  Tier: {hardware.get('tier', 'unknown').upper()}")
    print(f"  CUDA: {'Yes' if hardware.get('cuda_available') else 'No'}")

    print("\n[2/4] Detecting available models...")
    models = get_available_models()
    print(f"  Found {len(models)} models")
    for m in models[:5]:
        print(f"    - {m['name']} ({m['size_display']})")
    if len(models) > 5:
        print(f"    ... and {len(models) - 5} more")

    print("\n[3/4] Running benchmarks...")
    benchmarks = []
    for i, model in enumerate(models[:10]):
        name = model['name']
        print(f"  [{i+1}/{min(len(models), 10)}] Testing {name}...", end=" ", flush=True)

        benchmark = benchmark_model(name, warmup=(i == 0))
        benchmarks.append(benchmark)

        if benchmark.status == 'success':
            print(f"OK ({benchmark.tokens_per_second:.1f} tok/s)")
        else:
            print(f"FAIL ({benchmark.error[:30] if benchmark.error else 'error'})")

    print("\n[4/4] Generating configuration files...")

    model_config = generate_model_config(benchmarks, hardware)
    presets_config = generate_presets_config(benchmarks, hardware)

    save_config(model_config, MODEL_CONFIG_FILE)
    save_config(presets_config, PRESETS_CONFIG_FILE)

    print(f"  Saved: {MODEL_CONFIG_FILE}")
    print(f"  Saved: {PRESETS_CONFIG_FILE}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    successful = [b for b in benchmarks if b.status == 'success']
    if successful:
        best = max(successful, key=lambda x: x.tokens_per_second)
        print(f"  Best Model: {best.name}")
        print(f"  Speed: {best.tokens_per_second:.1f} tokens/second")

    print(f"  Config Directory: {CONFIG_DIR}")
    print("\n  Next Steps:")
    print("    1. Review generated configs in: configs/")
    print("    2. Restart py-ollama to use new configurations")
    print("    3. Run tests: pytest tests/")
    print("=" * 60)


def run_generate_configs():
    main()
    sys.exit(0)