import sys
import subprocess
from pathlib import Path


def run_speed_tests():
    """Run all speed tests for py-ollama model response times."""
    project_root = Path(__file__).parent.parent.parent
    tests_path = project_root / "tests"

    result = subprocess.run(
        [sys.executable, str(tests_path / "test_create_machine.py")],
        cwd=str(project_root),
    )
    sys.exit(result.returncode)
