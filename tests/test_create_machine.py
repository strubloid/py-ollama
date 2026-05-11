"""Tests for model creation and response time validation."""

import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "speed.config.json"
TEST_MODEL = "qwen2.5-coder:14b"
WARMUP_PROMPT = "ok"
CREATED_MODELS: list[str] = []

CONFIGS = [
    ("1", "normal", "Normal (Recommended)"),
    ("2", "coder", "Coder"),
    ("3", "coder_fast", "Coder Fast"),
    ("4", "explained", "Explained"),
]


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")

    with open(CONFIG_FILE) as f:
        return json.load(f)


def run_prompt(model_name: str, prompt: str, timeout: float) -> tuple[float, str]:
    start_time = time.time()

    result = subprocess.run(
        ["ollama", "run", model_name, prompt],
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    elapsed = time.time() - start_time

    if result.returncode != 0:
        raise RuntimeError(f"Ollama failed: {result.stderr}")

    return elapsed, result.stdout.strip()


def create_model(model_name: str, config_num: str) -> None:
    result = subprocess.run(
        ["py-ollama", TEST_MODEL, model_name, config_num],
        capture_output=True,
        text=True,
        timeout=60,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to create model: {result.stderr}")

    CREATED_MODELS.append(model_name)


def warmup_model(model_name: str) -> None:
    subprocess.run(
        ["ollama", "run", model_name, WARMUP_PROMPT],
        capture_output=True,
        text=True,
        timeout=15,
    )


def warmup_parallel(model_names: list[str], max_workers: int = 4) -> None:
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(warmup_model, model_names)


def cleanup_models() -> None:
    for model in CREATED_MODELS:
        try:
            subprocess.run(["ollama", "rm", model], capture_output=True, timeout=10)
        except Exception:
            pass


def print_row(config_name: str, model_name: str, response: str, elapsed: float, max_time: float, passed: bool) -> None:
    status = "PASS" if passed else "FAIL"
    truncated = response[:40] + "..." if len(response) > 40 else response
    print(f"{config_name:24} | {model_name:12} | {truncated:43} | {elapsed:5.2f}s / {max_time}s - {status}")


def run_benchmark(prompt: str, prefix: str, request_type: str) -> list[dict]:
    config = load_config()
    config_limits = config.get("config_limits", {}).get(request_type, {})

    print(f"\nPrompt: {prompt}")
    print(f"Request type: {request_type}")
    print(f"Limits: {config_limits}")
    print("=" * 100)
    print(f"{'Test name':24} | {'name machine':12} | {'response':43} | time")
    print("-" * 100)

    model_names = []
    for config_num, _, _ in CONFIGS:
        model_name = f"{prefix}_{config_num}"
        create_model(model_name, config_num)
        model_names.append(model_name)

    warmup_parallel(model_names)

    results = []
    for config_num, config_key, config_name in CONFIGS:
        model_name = f"{prefix}_{config_num}"
        max_time = config_limits.get(config_key, 5)

        try:
            elapsed, response = run_prompt(model_name, prompt, max_time + 5)
            passed = elapsed <= max_time
        except subprocess.TimeoutExpired:
            elapsed, response = max_time + 5, "TIMEOUT"
            passed = False

        results.append({
            "model": model_name,
            "config": config_name,
            "response": response,
            "elapsed": elapsed,
            "max": max_time,
            "passed": passed,
        })

        print_row(config_name, model_name, response, elapsed, max_time, passed)

    for model in model_names:
        try:
            subprocess.run(["ollama", "rm", model], capture_output=True, timeout=10)
        except Exception:
            pass

    print("=" * 100)

    return results


def test_model_response_time() -> None:
    print(f"Model: {TEST_MODEL}")

    benchmarks = [
        ("What is your name?", "rafael", "quick_request"),
        ("What are your principles?", "principles", "normal_request"),
    ]

    all_passed = True

    for prompt, prefix, request_type in benchmarks:
        results = run_benchmark(prompt, prefix, request_type)

        if any(not r["passed"] for r in results):
            all_passed = False
            failed = [r["model"] for r in results if not r["passed"]]
            print(f"FAILED: {', '.join(failed)}\n")

    print("ALL TESTS PASSED!" if all_passed else "SOME TESTS FAILED")
    

    if not all_passed:
        raise AssertionError("Some benchmarks failed")


if __name__ == "__main__":
    try:
        test_model_response_time()
    finally:
        cleanup_models()