from .speed import run_speed_tests
from .bench import run_bench
from .tree import generate_tree, print_tree
from .generate import run_generate_configs
from .refresh import refresh_agents

def run_bench_cmd():
    import sys
    model = sys.argv[1] if len(sys.argv) > 1 else "qwen2.5-coder:14b"
    run_bench(model)

__all__ = [
    "run_speed_tests",
    "run_bench",
    "run_bench_cmd",
    "generate_tree",
    "print_tree",
    "run_generate_configs",
    "refresh_agents",
]
