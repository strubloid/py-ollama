"""Performance tests for AI models across all modes.

This test suite measures response times for all models in all modes
to ensure consistent speed and identify performance regressions.

Run with: pytest tests/ai/test_performance.py -v -s

Note: Requires 'requests' library and Ollama server running.
      Install: pip install requests
      Start Ollama: ollama serve
"""

import sys
import time
from pathlib import Path

# Try to import requests, make it optional
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Add src directory to path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from ai.ollama import get_available_models  # noqa: E402
from ai.models import get_configs_for_model  # noqa: E402


class PerformanceMetrics:
    """Track performance metrics for a single query."""
    
    def __init__(self, model: str, mode: str):
        self.model = model
        self.mode = mode
        self.response_time: float | None = None
        self.token_count: int | None = None
        self.response_text: str | None = None
        self.error: str | None = None
    
    def __repr__(self):
        status = "✓" if self.error is None else "✗"
        time_str = f"{self.response_time:.2f}s" if self.response_time else "N/A"
        error_str = f" | ERROR: {self.error}" if self.error else ""
        return f"{status} {self.model:20} {self.mode:15} {time_str:8}{error_str}"


class PerformanceTest:
    """Test and benchmark AI model performance across all modes."""
    
    TEST_QUESTION = "What is your name?"
    TIMEOUT = 60  # seconds
    OLLAMA_API_URL = "http://localhost:11434"
    
    def __init__(self):
        if not HAS_REQUESTS:
            raise ImportError(
                "requests library not installed. "
                "Install with: pip install requests"
            )
        self.metrics = []
    
    def is_ollama_running(self) -> bool:
        """Check if Ollama server is running."""
        try:
            response = requests.get(
                f"{self.OLLAMA_API_URL}/api/tags",
                timeout=5
            )
            return response.status_code == 200  # type: ignore[no-any-return]
        except Exception:
            return False
    
    def get_available_models(self) -> list[str]:
        """Get list of available models from Ollama API."""
        try:
            models = get_available_models()
            return models if models else []
        except Exception:
            return []
    
    def measure_performance(self, model: str, mode: str) -> PerformanceMetrics:
        """Measure response time and performance for a model in a given mode."""
        metrics = PerformanceMetrics(model, mode)
        
        try:
            # Get config for this model and mode
            config = get_configs_for_model(model)
            if mode not in config:
                metrics.error = f"Mode '{mode}' not available"
                return metrics
            
            model_config = config[mode]
            
            # Extract parameters from config string
            temperature = self._extract_temperature(model_config.config)
            top_p = self._extract_top_p(model_config.config)
            top_k = self._extract_top_k(model_config.config)
            num_ctx = self._extract_num_ctx(model_config.config)
            num_predict = self._extract_num_predict(model_config.config)
            
            # Prepare request payload
            payload = {
                "model": model,
                "prompt": self.TEST_QUESTION,
                "system": model_config.system,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k,
                    "num_ctx": num_ctx,
                    "num_predict": num_predict,
                }
            }
            
            # Measure response time
            start_time = time.time()
            response = requests.post(
                f"{self.OLLAMA_API_URL}/api/generate",
                json=payload,
                timeout=self.TIMEOUT
            )
            end_time = time.time()
            
            if response.status_code != 200:
                metrics.error = f"API error: {response.status_code}"
                return metrics
            
            metrics.response_time = end_time - start_time
            response_data = response.json()
            metrics.response_text = response_data.get("response", "")
            
        except requests.Timeout:
            metrics.error = f"Timeout after {self.TIMEOUT}s"
        except requests.ConnectionError:
            metrics.error = "Connection refused - is Ollama running?"
        except Exception as e:
            metrics.error = str(e)
        
        return metrics
    
    def _extract_temperature(self, config_str: str) -> float:
        """Extract temperature parameter from config string."""
        for line in config_str.split("\n"):
            if "PARAMETER temperature" in line:
                try:
                    return float(line.split()[-1])
                except ValueError:
                    pass
        return 0.7
    
    def _extract_top_p(self, config_str: str) -> float:
        """Extract top_p parameter from config string."""
        for line in config_str.split("\n"):
            if "PARAMETER top_p" in line:
                try:
                    return float(line.split()[-1])
                except ValueError:
                    pass
        return 0.9
    
    def _extract_top_k(self, config_str: str) -> int:
        """Extract top_k parameter from config string."""
        for line in config_str.split("\n"):
            if "PARAMETER top_k" in line:
                try:
                    return int(line.split()[-1])
                except ValueError:
                    pass
        return 40
    
    def _extract_num_ctx(self, config_str: str) -> int:
        """Extract num_ctx parameter from config string."""
        for line in config_str.split("\n"):
            if "PARAMETER num_ctx" in line:
                try:
                    return int(line.split()[-1])
                except ValueError:
                    pass
        return 2048
    
    def _extract_num_predict(self, config_str: str) -> int:
        """Extract num_predict parameter from config string."""
        for line in config_str.split("\n"):
            if "PARAMETER num_predict" in line:
                try:
                    return int(line.split()[-1])
                except ValueError:
                    pass
        return 128
    
    def run_benchmark(self, models: list[str] | None = None) -> bool:
        """Run performance benchmark on all models and modes."""
        if not self.is_ollama_running():
            print("ERROR: Ollama server is not running on http://localhost:11434")
            print("Please start Ollama with: ollama serve")
            return False
        
        # Get available models if not specified
        if models is None:
            available = self.get_available_models()
            if not available:
                print("ERROR: No models available in Ollama")
                return False
            models = available
        
        modes = ["normal", "coder", "coder_fast", "explained"]
        
        print("\n" + "="*80)
        print("PERFORMANCE BENCHMARK - AI Model Response Times")
        print("="*80)
        print(f"Question: {self.TEST_QUESTION}")
        print(f"Models to test: {len(models)}")
        print(f"Modes per model: {len(modes)}")
        print(f"Total tests: {len(models) * len(modes)}")
        print("="*80 + "\n")
        
        # Run tests
        for model in models:
            print(f"Testing model: {model}")
            model_times = {}
            
            for mode in modes:
                metrics = self.measure_performance(model, mode)
                self.metrics.append(metrics)
                model_times[mode] = metrics.response_time if metrics.response_time else 0
                print(f"  {metrics}")
            
            # Print summary for this model
            if all(t > 0 for t in model_times.values()):
                avg_time = sum(model_times.values()) / len(model_times)
                min_time = min(model_times.values())
                max_time = max(model_times.values())
                variance = ((max_time - min_time) / avg_time * 100) if avg_time > 0 else 0
                
                print(f"  Summary: avg={avg_time:.2f}s, min={min_time:.2f}s, max={max_time:.2f}s, variance={variance:.1f}%")
                
                # Flag significant variance
                if variance > 30:
                    print(f"  ⚠️  HIGH VARIANCE DETECTED ({variance:.1f}%)")
            
            print()
        
        # Print overall summary
        self._print_summary()
        return True
    
    def _print_summary(self):
        """Print overall performance summary and analysis."""
        if not self.metrics:
            return
        
        print("="*80)
        print("OVERALL SUMMARY")
        print("="*80)
        
        # Group by mode
        by_mode = {}
        for metric in self.metrics:
            if metric.response_time:
                if metric.mode not in by_mode:
                    by_mode[metric.mode] = []
                by_mode[metric.mode].append(metric.response_time)
        
        print("\nPerformance by Mode:")
        for mode in ["normal", "coder", "coder_fast", "explained"]:
            if mode in by_mode:
                times = by_mode[mode]
                avg = sum(times) / len(times)
                min_t = min(times)
                max_t = max(times)
                print(f"  {mode:15}: avg={avg:.2f}s, min={min_t:.2f}s, max={max_t:.2f}s")
        
        # Analysis
        print("\n" + "="*80)
        print("ANALYSIS")
        print("="*80)
        
        coder_times = by_mode.get("coder", [])
        coder_fast_times = by_mode.get("coder_fast", [])
        
        if coder_times and coder_fast_times:
            coder_avg = sum(coder_times) / len(coder_times)
            coder_fast_avg = sum(coder_fast_times) / len(coder_fast_times)
            diff = coder_avg - coder_fast_avg
            pct_diff = (diff / coder_fast_avg * 100) if coder_fast_avg > 0 else 0
            
            print("\nCoder vs Coder_Fast:")
            print(f"  Coder avg:       {coder_avg:.2f}s")
            print(f"  Coder_fast avg:  {coder_fast_avg:.2f}s")
            print(f"  Difference:      {diff:.2f}s ({pct_diff:+.1f}%)")
            
            if pct_diff > 20:
                print(f"  ⚠️  Coder mode is {pct_diff:.1f}% SLOWER than Coder_fast")
                print("      This indicates configuration differences that should be investigated.")
            elif pct_diff < -20:
                print(f"  ⚠️  Coder mode is {abs(pct_diff):.1f}% FASTER than Coder_fast")
                print("      This is unexpected and should be investigated.")
            else:
                print(f"  ✓ Modes are within acceptable variance ({abs(pct_diff):.1f}%)")
        
        print("\n" + "="*80)


def test_performance_basic():
    """Basic performance test - just check if test framework works."""
    try:
        tester = PerformanceTest()
    except ImportError:
        print("requests library not available - skipping performance test")
        return
    
    # Check if Ollama is running
    if not tester.is_ollama_running():
        print("Ollama is not running - skipping performance test")
        print("To run full benchmarks: ollama serve")
        return
    
    # Run benchmark on first available model
    available_models = tester.get_available_models()
    if available_models:
        print(f"Found {len(available_models)} available models")
        tester.run_benchmark(available_models[:1])  # Test just first model
    else:
        print("No models available")


def test_performance_all():
    """Full performance test - runs on all available models."""
    try:
        tester = PerformanceTest()
    except ImportError:
        print("requests library not available - skipping performance test")
        return
    
    if not tester.is_ollama_running():
        print("Ollama is not running - skipping performance test")
        return
    
    tester.run_benchmark()


def test_performance_specific_models():
    """Test specific models for comparison."""
    try:
        tester = PerformanceTest()
    except ImportError:
        print("requests library not available - skipping performance test")
        return
    
    if not tester.is_ollama_running():
        print("Ollama is not running - skipping performance test")
        return
    
    # Test common models
    test_models = ["qwen2.5-coder:14b", "deepseek-coder:6.7b", "llama2"]
    available = tester.get_available_models()
    models_to_test = [m for m in test_models if any(m in a for a in available)]
    
    if models_to_test:
        tester.run_benchmark(models_to_test)
    else:
        print(f"None of the target models are installed: {test_models}")
        print(f"Available models: {available}")


if __name__ == "__main__":
    # Run basic test
    test_performance_all()
