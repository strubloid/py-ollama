"""Simple benchmark runner using existing ai.models system."""

import sys
import subprocess
import time
import json
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel


WARMUP_PROMPT = "hi"
CONFIGS = [
    ("1", "normal", "Normal"),
    ("2", "coder", "Coder"),
    ("3", "coder_fast", "Coder Fast"),
    ("4", "explained", "Explained"),
]
BENCHMARKS = [
    ("What is your name?", "quick"),
    ("Explain recursion.", "reasoning"),
    ("Count to 3.", "count"),
    ("Sky color?", "fact"),
]
RUNS_PER_CONFIG = 3
DEFAULT_LIMIT = 3.5

console = Console()


def load_config() -> dict:
    config_path = Path(__file__).parent.parent.parent / "configs" / "speed.config.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {"config_limits": {}}


def get_available_models() -> list[tuple[str, float]]:
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True,
    )
    models = []
    for line in result.stdout.strip().split("\n")[1:]:
        if line.strip():
            parts = line.split()
            if len(parts) >= 4:
                name = parts[0]
                size_num = parts[2]
                size_unit = parts[3] if len(parts) > 3 else "GB"
                if size_unit == "GB":
                    size = float(size_num)
                elif size_unit == "MB":
                    size = float(size_num) / 1000
                else:
                    size = 0
                models.append((name, size))
    return sorted(models, key=lambda x: x[1])


def select_diverse_models(models: list[tuple[str, float]], max_per_size: int = 2) -> list[str]:
    if not models:
        return []
    selected = []
    size_categories = [
        (0, 3),    # tiny < 3GB
        (3, 6),    # small 3-6GB
        (6, 10),   # medium 6-10GB
        (10, 20),  # large 10-20GB
        (20, 999), # huge > 20GB
    ]
    for low, high in size_categories:
        category_models = [m for m in models if low <= m[1] < high]
        selected.extend([m[0] for m in category_models[:max_per_size]])
    return selected


def select_by_family(models: list[tuple[str, float]]) -> list[str]:
    from ai.models import detect_model_family
    family_map = {}
    for name, size in models:
        family = detect_model_family(name)
        if family not in family_map:
            family_map[family] = (name, size)
        elif size < family_map[family][1]:
            family_map[family] = (name, size)
    return [v[0] for v in family_map.values()]


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


def create_model(model_name: str, config_num: str, base_model: str) -> str:
    result = subprocess.run(
        ["py-ollama", base_model, model_name, config_num],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        return result.stderr[:100]
    return ""


def warmup(model_name: str, runs: int = 2) -> float:
    total = 0.0
    for _ in range(runs):
        start = time.perf_counter()
        try:
            subprocess.run(
                ["ollama", "run", model_name, WARMUP_PROMPT],
                capture_output=True,
                text=True,
                timeout=60,
            )
        except subprocess.TimeoutExpired:
            pass
        total += time.perf_counter() - start
    return total / runs


def run_model_bench(
    base_model: str,
    config: dict,
    limits: dict,
) -> list[dict]:
    results = []

    for prompt, limit_type in BENCHMARKS:
        max_time = limits.get(limit_type, DEFAULT_LIMIT)
        bench_name = f"bench_{base_model.replace(':', '_').replace('-', '_')}"

        cleanup_model(bench_name)
        error = create_model(bench_name, "1", base_model)

        if error:
            results.append({
                "model": base_model,
                "prompt": prompt[:30],
                "warmup": 0,
                "cold": 0,
                "warm_avg": 0,
                "passed": False,
                "error": error[:50],
            })
            continue

        warm = warmup(bench_name, runs=2)

        timings = []
        for _ in range(RUNS_PER_CONFIG):
            elapsed, _ = run_prompt(bench_name, prompt, max_time + 5)
            timings.append(elapsed)

        cleanup_model(bench_name)

        cold = timings[0]
        warm_timings = timings[1:]
        warm_avg = sum(warm_timings) / len(warm_timings) if warm_timings else cold
        passed = warm_avg <= max_time

        results.append({
            "model": base_model,
            "prompt": prompt[:30],
            "warmup": warm,
            "cold": cold,
            "warm_avg": warm_avg,
            "passed": passed,
            "error": "",
        })

    return results


def run_bench() -> None:
    config = load_config()
    limits = config.get("config_limits", {})
    by_family = "--by-family" in sys.argv

    console.rule("[bold]PY-OLLAMA BENCHMARK[/bold]")

    models = get_available_models()
    console.print(f"[dim]Found {len(models)} models[/dim]")

    if by_family:
        selected = select_by_family(models)
        console.print(f"[dim]Testing one model per family ({len(selected)} families):[/dim]")
    else:
        selected = select_diverse_models(models, max_per_size=1)
        console.print(f"[dim]Testing {len(selected)} diverse models:[/dim]")
    for m in selected:
        console.print(f"  [cyan]- {m}[/cyan]")

    console.print()

    all_results = []
    for base_model in selected:
        results = run_model_bench(base_model, config, limits)
        all_results.extend(results)

    table = Table(title="Benchmark Results")
    table.add_column("Model", style="cyan", no_wrap=True)
    table.add_column("Prompt", style="dim")
    table.add_column("Warmup", justify="right", style="dim")
    table.add_column("Cold", justify="right", style="yellow")
    table.add_column("Warm Avg", justify="right", style="green")
    table.add_column("Status", justify="center")

    for r in all_results:
        status = "[green]PASS[/green]" if r["passed"] else "[red]FAIL[/red]"
        warmup_str = f"{r['warmup']:.2f}s" if r['warmup'] > 0 else "-"
        cold_str = f"{r['cold']:.2f}s" if r['cold'] > 0 else "-"
        warm_str = f"{r['warm_avg']:.2f}s" if r['warm_avg'] > 0 else "-"
        error_str = f" ({r['error']})" if r['error'] else ""
        table.add_row(
            r["model"][:25],
            r["prompt"],
            warmup_str,
            cold_str,
            warm_str,
            status + error_str,
        )

    console.print(table)

    passed = sum(1 for r in all_results if r["passed"])
    total = len(all_results)
    failed = total - passed

    console.rule()

    if failed == 0:
        console.print(Panel(
            f"[bold green]ALL PASSED[/bold green]\nPassed: {passed}/{total}",
            border_style="green",
        ))
    else:
        console.print(Panel(
            f"[bold red]SOME FAILED[/bold red]\nPassed: {passed} | Failed: {failed}",
            border_style="red",
        ))
        sys.exit(1)


if __name__ == "__main__":
    run_bench()