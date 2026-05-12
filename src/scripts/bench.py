"""Simple benchmark runner using existing ai.models system."""

import sys
import subprocess
import time
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel


TEST_MODEL = "qwen2.5-coder:14b"
WARMUP_PROMPT = "hi"
CONFIGS = [
    ("1", "normal", "Normal"),
    ("2", "coder", "Coder"),
    ("3", "coder_fast", "Coder Fast"),
    ("4", "explained", "Explained"),
]
BENCHMARKS = [
    ("What is your name?", "bench1", "quick"),
    ("Explain recursion.", "bench2", "reasoning"),
    ("Count to 3.", "bench3", "count"),
    ("Sky color?", "bench4", "fact"),
]
RUNS_PER_CONFIG = 3
DEFAULT_LIMIT = 3.5

console = Console()


def load_config() -> dict:
    config_path = Path(__file__).parent.parent.parent / "speed.config.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {"config_limits": {}}


def cleanup_model(model_name: str) -> None:
    try:
        subprocess.run(["ollama", "rm", model_name], capture_output=True, timeout=10)
    except Exception:
        pass


def run_prompt(model_name: str, prompt: str, timeout: float) -> tuple[float, str]:
    start = time.perf_counter()
    result = subprocess.run(
        ["ollama", "run", model_name, prompt],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    elapsed = time.perf_counter() - start
    if result.returncode != 0:
        return elapsed, f"ERROR: {result.stderr[:100]}"
    return elapsed, result.stdout.strip()


def create_model(model_name: str, config_num: str) -> str:
    result = subprocess.run(
        ["py-ollama", TEST_MODEL, model_name, config_num],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        return result.stderr[:100]
    return ""


def verify_gpu(model_name: str) -> bool:
    result = subprocess.run(
        ["ollama", "show", "--modelfile", model_name],
        capture_output=True,
        text=True,
    )
    return "num_gpu" in result.stdout.lower()


def warmup(model_name: str, runs: int = 2) -> float:
    total = 0.0
    for _ in range(runs):
        start = time.perf_counter()
        subprocess.run(
            ["ollama", "run", model_name, WARMUP_PROMPT],
            capture_output=True,
            text=True,
            timeout=15,
        )
        total += time.perf_counter() - start
    return total / runs


def run_bench():
    config = load_config()
    limits = config.get("config_limits", {})

    console.rule("[bold]PY-OLLAMA BENCHMARK[/bold]")
    console.print(f"[dim]Model: {TEST_MODEL} | Configs: {len(CONFIGS)} | Benchmarks: {len(BENCHMARKS)}[/dim]\n")

    all_passed = True
    summary = {"passed": 0, "failed": 0}

    for prompt, prefix, limit_type in BENCHMARKS:
        max_time = limits.get(limit_type, DEFAULT_LIMIT)
        results = []

        for config_num, config_key, config_name in CONFIGS:
            model_name = f"{prefix}_{config_num}"

            cleanup_model(model_name)
            error = create_model(model_name, config_num)

            if error:
                results.append({
                    "config": config_name,
                    "gpu": False,
                    "warmup": 0,
                    "cold": 0,
                    "warm_avg": 0,
                    "warm_range": "0-0",
                    "response": f"CREATE FAIL: {error}",
                    "passed": False,
                })
                continue

            warm = warmup(model_name, runs=2)

            timings = []
            response = ""

            for i in range(RUNS_PER_CONFIG):
                elapsed, resp = run_prompt(model_name, prompt, max_time + 5)
                timings.append(elapsed)
                if i == 0:
                    response = resp[:60]

            cleanup_model(model_name)

            cold = timings[0]
            warm_timings = timings[1:]
            warm_avg = sum(warm_timings) / len(warm_timings) if warm_timings else cold
            warm_min = min(warm_timings) if warm_timings else cold
            warm_max = max(warm_timings) if warm_timings else cold
            passed = warm_avg <= max_time

            results.append({
                "config": config_name,
                "gpu": verify_gpu(model_name),
                "warmup": warm,
                "cold": cold,
                "warm_avg": warm_avg,
                "warm_range": f"{warm_min:.2f}-{warm_max:.2f}",
                "response": response,
                "passed": passed,
            })

        table = Table(title=f"Prompt: {prompt}")
        table.add_column("Config", style="cyan", no_wrap=True)
        table.add_column("GPU", justify="center")
        table.add_column("Warmup", justify="right", style="dim")
        table.add_column("Cold", justify="right", style="yellow")
        table.add_column("Warm Avg", justify="right", style="green")
        table.add_column("Range", justify="right", style="dim")
        table.add_column("Status", justify="center")

        for r in results:
            status = "[green]PASS[/green]" if r["passed"] else "[red]FAIL[/red]"
            gpu = "[green]Y[/green]" if r["gpu"] else "[dim]-[/dim]"
            table.add_row(
                r["config"],
                gpu,
                f"{r['warmup']:.2f}s",
                f"{r['cold']:.2f}s",
                f"{r['warm_avg']:.2f}s",
                r["warm_range"],
                status,
            )

        console.print(table)
        console.print(f"[dim]limit: {max_time}s | type: {limit_type}[/dim]\n")

        for r in results:
            if r["passed"]:
                summary["passed"] += 1
            else:
                summary["failed"] += 1
                all_passed = False

    console.rule()

    total = summary["passed"] + summary["failed"]
    if all_passed:
        console.print(Panel(
            f"[bold green]ALL PASSED[/bold green]\n"
            f"Passed: {summary['passed']}/{total}",
            border_style="green",
        ))
    else:
        console.print(Panel(
            f"[bold red]SOME FAILED[/bold red]\n"
            f"Passed: {summary['passed']} | Failed: {summary['failed']}",
            border_style="red",
        ))
        sys.exit(1)


if __name__ == "__main__":
    run_bench()