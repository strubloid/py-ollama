"""Tests for model creation and response time validation."""

import json
import subprocess
import time
from pathlib import Path

from rich.console import Console
from rich.table import Table

CONFIG_FILE = Path(__file__).parent.parent / "configs" / "speed.config.json"
TEST_MODEL = "qwen2.5-coder:14b"
WARMUP_PROMPT = "hi"
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

RUNS_PER_MODEL = 3

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


def verify_num_gpu(model_name: str) -> bool:
    result = subprocess.run(
        ["ollama", "show", "--modelfile", model_name],
        capture_output=True,
        text=True,
    )
    return "num_gpu" in result.stdout.lower()


def warmup_model(model_name: str, runs: int = 3) -> float:
    total_time = 0.0
    for _ in range(runs):
        start = time.time()
        subprocess.run(
            ["ollama", "run", model_name, WARMUP_PROMPT],
            capture_output=True,
            text=True,
            timeout=30,
        )
        total_time += time.time() - start
    return total_time / runs


def cleanup_models() -> None:
    for model in CREATED_MODELS:
        try:
            subprocess.run(["ollama", "rm", model], capture_output=True, timeout=10)
        except Exception:
            pass


def cleanup_models_benchmark(model_names: list[str]) -> None:
    for model in model_names:
        try:
            subprocess.run(["ollama", "rm", model], capture_output=True, timeout=10)
        except Exception:
            pass


def run_model_benchmark(
    model_name: str,
    prompts: list[tuple[str, str]],
    max_time: float,
    warmup_runs: int = 3,
) -> dict:
    warmup_time = warmup_model(model_name, runs=warmup_runs)

    all_results = []
    for prompt_text, request_type in prompts:
        timings = []
        first_response = ""

        for run_idx in range(RUNS_PER_MODEL):
            try:
                elapsed, response = run_prompt(model_name, prompt_text, max_time + 5)
                timings.append(elapsed)
                if run_idx == 0:
                    first_response = response
            except subprocess.TimeoutExpired:
                timings.append(max_time + 5)
                if run_idx == 0:
                    first_response = "TIMEOUT"

        cold_time = timings[0] if timings else 0
        warm_timings = timings[1:] if len(timings) > 1 else timings
        warm_avg = sum(warm_timings) / len(warm_timings) if warm_timings else cold_time
        warm_min = min(warm_timings) if warm_timings else cold_time
        warm_max = max(warm_timings) if warm_timings else cold_time

        all_results.append({
            "prompt": prompt_text,
            "request_type": request_type,
            "cold_time": cold_time,
            "warm_avg": warm_avg,
            "warm_min": warm_min,
            "warm_max": warm_max,
            "all_timings": timings,
            "first_response": first_response,
            "passed": warm_avg <= max_time,
            "max_time": max_time,
        })

    return {
        "model_name": model_name,
        "warmup_avg": warmup_time,
        "results": all_results,
    }


def run_benchmark(
    prompt: str,
    prefix: str,
    request_type: str,
) -> list[dict]:
    config = load_config()
    config_limits = config.get("config_limits", {}).get(request_type, {})

    table = Table(title=f"{prompt}")
    table.add_column("Config", style="cyan", no_wrap=True)
    table.add_column("Model", style="magenta")
    table.add_column("GPU", justify="center", style="dim")
    table.add_column("Cold", justify="right", style="yellow")
    table.add_column("Warm Avg", justify="right", style="cyan")
    table.add_column("Warm Range", justify="right", style="dim")
    table.add_column("Response", style="green")
    table.add_column("Status", justify="center")

    results = []

    for config_num, config_key, config_name in CONFIGS:
        model_name = f"{prefix}_{config_num}"
        max_time = config_limits.get(config_key, 5)
        has_gpu = "[green]Y[/green]" if verify_num_gpu(model_name) else "[dim]-[/dim]"

        timings = []
        first_response = ""

        for run_idx in range(RUNS_PER_MODEL):
            try:
                elapsed, response = run_prompt(model_name, prompt, max_time + 5)
                timings.append(elapsed)
                if run_idx == 0:
                    first_response = response
            except subprocess.TimeoutExpired:
                timings.append(max_time + 5)
                if run_idx == 0:
                    first_response = "TIMEOUT"

        cold_time = timings[0] if timings else 0
        warm_timings = timings[1:] if len(timings) > 1 else timings
        warm_avg = sum(warm_timings) / len(warm_timings) if warm_timings else cold_time
        warm_min = min(warm_timings) if warm_timings else cold_time
        warm_max = max(warm_timings) if warm_timings else cold_time

        passed = warm_avg <= max_time

        results.append({
            "model": model_name,
            "config": config_name,
            "cold_time": cold_time,
            "warm_avg": warm_avg,
            "warm_min": warm_min,
            "warm_max": warm_max,
            "all_timings": timings,
            "response": first_response,
            "max": max_time,
            "passed": passed,
        })

        status = "[green]PASS[/green]" if passed else "[red]FAIL[/red]"
        short_resp = first_response[:25] + "..." if len(first_response) > 25 else first_response
        warm_range = f"{warm_min:.2f}-{warm_max:.2f}"

        table.add_row(
            config_name,
            model_name,
            has_gpu,
            f"{cold_time:.2f}s",
            f"{warm_avg:.2f}s",
            warm_range,
            short_resp,
            status,
        )

    console.print(table)
    console.print(f"[dim]type: {request_type}  limits: {config_limits}  runs: {RUNS_PER_MODEL} (first ignored for avg)[/dim]")

    return results


def test_model_response_time() -> None:
    console.rule("[bold]SPEED TESTS[/bold]")

    all_passed = True

    for prompt, prefix, request_type in BENCHMARKS:
        for config_num, _, config_name in CONFIGS:
            model_name = f"{prefix}_{config_num}"

            create_model(model_name, config_num)
            warmup_time = warmup_model(model_name, runs=3)
            console.print(f"[dim]  {model_name}: warmup={warmup_time:.2f}s[/dim]")

        results = run_benchmark(prompt, prefix, request_type)

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