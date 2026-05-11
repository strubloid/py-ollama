"""Tests for model creation and response time validation."""

import json
import subprocess
import time
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "speed.config.json"
TEST_MODEL = "qwen2.5-coder:14b"
CREATED_MODELS = []


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")

    with open(CONFIG_FILE) as f:
        return json.load(f)


def run_ollama_prompt(model_name: str, prompt: str, max_time: float, warmup: bool = False) -> tuple[float, str]:
    if warmup:
        subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True,
            text=True,
            timeout=max_time + 5,
        )
        return 0.0, ""

    start_time = time.time()

    result = subprocess.run(
        ["ollama", "run", model_name, prompt],
        capture_output=True,
        text=True,
        timeout=max_time + 5,
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


def cleanup_models() -> None:
    for model in CREATED_MODELS:
        try:
            subprocess.run(
                ["ollama", "rm", model],
                capture_output=True,
                timeout=10,
            )
            print(f"  Cleaned up: {model}")
        except Exception as e:
            print(f"  Failed to clean up {model}: {e}")


def run_test(prompt: str, prefix: str, request_type: str) -> None:
    
    config = load_config()
    config_limits = config.get("config_limits", {}).get(request_type, {})

    print(f"Prompt: {prompt}")
    print(f"Request type: {request_type}")
    print(f"Limits: {config_limits}")
    print("=" * 60)

    configs = [
        ("1", "normal", "Normal (Recommended)"),
        ("2", "coder", "Coder"),
        ("3", "coder_fast", "Coder Fast"),
        ("4", "explained", "Explained"),
    ]

    results = []

    try:
        for config_num, config_key, config_name in configs:
            model_name = f"{prefix}_{config_num}"
            max_time = config_limits.get(config_key, 5)

            print(f"\n--- Testing {config_name} ({config_num}) ---")

            create_model(model_name, config_num)
            print(f"Created: {model_name}")

            print("  Warming up...")
            run_ollama_prompt(model_name, "hi", max_time, warmup=True)

            try:
                elapsed, response = run_ollama_prompt(model_name, prompt, max_time)
                passed = elapsed <= max_time

                results.append({
                    "model": model_name,
                    "config": config_name,
                    "elapsed": elapsed,
                    "max": max_time,
                    "passed": passed,
                    "response": response[:50] + "..." if len(response) > 50 else response,
                })

                status = "PASS" if passed else "FAIL"
                print(f"Response: {results[-1]['response']}")
                print(f"Response time: {elapsed:.2f}s / {max_time}s - {status}")

            except subprocess.TimeoutExpired:
                elapsed = max_time + 5
                results.append({
                    "model": model_name,
                    "config": config_name,
                    "elapsed": elapsed,
                    "max": max_time,
                    "passed": False,
                    "response": "TIMEOUT",
                })
                print("Response: TIMEOUT")
                print("Response time: TIMEOUT - FAIL")

    finally:
        print("\n" + "=" * 60)
        print("Cleanup")
        print("=" * 60)
        cleanup_models()

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(
            f"{r['model']:12} {r['config']:20} "
            f"{r['elapsed']:6.2f}s / {r['max']}s - {status}"
        )

    print("=" * 60)

    failed = [r for r in results if not r["passed"]]
    if failed:
        failed_names = ", ".join(r["model"] for r in failed)
        raise AssertionError(f"Failed models: {failed_names}")

    print("Test passed!\n")


def test_model_response_time() -> None:
    
    print("Model Response Time Tests")
    print(f"Model: {TEST_MODEL}")

    run_test("What is your name?", "rafael", "quick_request")
    run_test("What are your principles?", "principles", "normal_request")

    print("ALL TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    test_model_response_time()