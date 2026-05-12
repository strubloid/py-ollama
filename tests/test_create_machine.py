"""Tests for model creation and response time validation."""

import json
import subprocess
import time
from pathlib import Path

from rich.console import Console
from rich.table import Table

CONFIG_FILE = Path(__file__).parent.parent / "speed.config.json"
TEST_MODEL = "qwen2.5-coder:14b"
WARMUP_PROMPT = "ok"
CREATED_MODELS: list[str] = []

CONFIGS = [
    ("1", "normal", "Normal"),
    ("2", "coder", "Coder"),
    ("3", "coder_fast", "Coder Fast"),
    ("4", "explained", "Explained"),
]

BENCHMARKS = [
    ("What is your name?", "rafael", "quick_request"),
    ("What are your principles?", "principles", "normal_request"),
]

console = Console()


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


def warmup_model(model_name: str) -> float:
    start = time.time()
    subprocess.run(
        ["ollama", "run", model_name, "hi"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return time.time() - start


def cleanup_models() -> None:
    for model in CREATED_MODELS:
        try:
            subprocess.run(["ollama", "rm", model], capture_output=True, timeout=10)
        except Exception:
            pass


def create_and_warmup_all(prefix: str) -> dict[str, float]:
    model_names = {}
    for config_num, _, _ in CONFIGS:
        model_name = f"{prefix}_{config_num}"
        create_model(model_name, config_num)
        model_names[model_name] = 0.0

    for model_name in model_names:
        warmup_time = warmup_model(model_name)
        model_names[model_name] = warmup_time

    return model_names


def cleanup_models_benchmark(model_names: list[str]) -> None:
    for model in model_names:
        try:
            subprocess.run(["ollama", "rm", model], capture_output=True, timeout=10)
        except Exception:
            pass


def run_benchmark(
    prompt: str,
    prefix: str,
    request_type: str,
    model_warmup_times: dict[str, float],
) -> list[dict]:
    config = load_config()
    config_limits = config.get("config_limits", {}).get(request_type, {})

    table = Table(title=f"{prompt}")
    table.add_column("Config", style="cyan", no_wrap=True)
    table.add_column("Model", style="magenta")
    table.add_column("Warmup", justify="right", style="yellow")
    table.add_column("Response", style="green")
    table.add_column("Time", justify="right", style="blue")
    table.add_column("Status", justify="center")

    results = []
    for config_num, config_key, config_name in CONFIGS:
        model_name = f"{prefix}_{config_num}"
        max_time = config_limits.get(config_key, 5)
        warmup = model_warmup_times.get(model_name, 0.0)

        try:
            elapsed, response = run_prompt(model_name, prompt, max_time + 5)
            passed = elapsed <= max_time
        except subprocess.TimeoutExpired:
            elapsed, passed = max_time + 5, False
            response = "TIMEOUT"

        results.append({
            "model": model_name,
            "config": config_name,
            "warmup": warmup,
            "response": response,
            "elapsed": elapsed,
            "max": max_time,
            "passed": passed,
        })

        status = "[green]PASS[/green]" if passed else "[red]FAIL[/red]"
        short_resp = response[:40] + "..." if len(response) > 40 else response
        time_str = f"{elapsed:.2f}s / {max_time}s"

        table.add_row(
            config_name,
            model_name,
            f"{warmup:.2f}s",
            short_resp,
            time_str,
            status,
        )

    console.print(table)
    console.print(f"[dim]type: {request_type}  limits: {config_limits}[/dim]")

    return results


def test_model_response_time() -> None:
    console.rule("[bold]SPEED TESTS[/bold]")

    all_passed = True

    for prompt, prefix, request_type in BENCHMARKS:
        warmup_times = create_and_warmup_all(prefix)
        results = run_benchmark(prompt, prefix, request_type, warmup_times)

        if any(not r["passed"] for r in results):
            all_passed = False
            failed = [r["model"] for r in results if not r["passed"]]
            console.print(f"[red]!! FAILED: {', '.join(failed)}[/red]")

        model_names = [f"{prefix}_{c[0]}" for c in CONFIGS]
        cleanup_models_benchmark(model_names)

    console.rule()
    if all_passed:
        console.print("[bold green]ALL PASSED[/bold green]")
    else:
        console.print("[bold red]SOME FAILED[/bold red]")
        raise AssertionError("Some benchmarks failed")


if __name__ == "__main__":
    try:
        test_model_response_time()
    except AssertionError:
        pass
    finally:
        cleanup_models()