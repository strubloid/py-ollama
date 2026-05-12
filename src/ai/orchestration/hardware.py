"""
Hardware capability detection and model orchestration.

Automatically detects GPU, VRAM, memory bandwidth and selects
optimal model + configuration based on available resources.
"""

import subprocess
from dataclasses import dataclass, field
from enum import Enum


class CapabilityTier(Enum):
    HIGH = "high"        # RTX 4090, A100, etc - 24GB+ VRAM
    MEDIUM = "medium"    # RTX 4070 Ti, 3080, etc - 12-16GB VRAM
    LOW = "low"          # RTX 3060, 4060, etc - 8GB VRAM
    MINIMAL = "minimal"  # 4-6GB VRAM, CPU fallback


@dataclass
class HardwareProfile:
    tier: CapabilityTier
    gpu_name: str = ""
    vram_mb: int = 0
    vram_available_mb: int = 0
    memory_bandwidth_gb_s: int = 0
    cpu_cores: int = 0
    ram_gb: int = 0
    cuda_available: bool = False
    flash_attention: bool = False

    @property
    def vram_percent_used(self) -> float:
        if self.vram_mb == 0:
            return 0
        return (self.vram_mb / self.vram_available_mb * 100) if self.vram_available_mb > 0 else 0

    def can_run_model(self, model_size_gb: float, include_overhead: float = 2.0) -> bool:
        """Check if this hardware can run a model of given size."""
        required = model_size_gb + include_overhead
        return self.vram_available_mb >= (required * 1024)


@dataclass
class ModelProfile:
    name: str
    size_gb: float
    quantization: str
    tokens_per_second: int
    quality_score: int  # 1-100
    vram_required_mb: int
    recommended_for: list[CapabilityTier] = field(default_factory=list)


@dataclass
class ConfigurationProfile:
    name: str
    num_ctx: int
    num_predict: int
    num_gpu: int
    num_batch: int
    temperature: float
    top_p: float
    top_k: int
    use_mlock: bool
    use_mmap: bool
    f16_kv: bool
    system_prompt_length: str  # "minimal", "short", "medium", "long"


class HardwareOrchestrator:
    """Detects hardware and orchestrates model selection."""

    MODELS = {
        "qwen2.5-coder:14b-q4_k_m": ModelProfile(
            name="qwen2.5-coder:14b",
            size_gb=9.0,
            quantization="Q4_K_M",
            tokens_per_second=47,
            quality_score=95,
            vram_required_mb=9200,
            recommended_for=[CapabilityTier.MEDIUM, CapabilityTier.HIGH],
        ),
        "qwen2.5-coder:14b-q3_k_m": ModelProfile(
            name="qwen2.5-coder:14b",
            size_gb=7.0,
            quantization="Q3_K_M",
            tokens_per_second=65,
            quality_score=88,
            vram_required_mb=7500,
            recommended_for=[CapabilityTier.LOW, CapabilityTier.MEDIUM],
        ),
        "qwen2.5-coder:14b-q2_k": ModelProfile(
            name="qwen2.5-coder:14b",
            size_gb=5.5,
            quantization="Q2_K",
            tokens_per_second=85,
            quality_score=80,
            vram_required_mb=6000,
            recommended_for=[CapabilityTier.LOW, CapabilityTier.MINIMAL],
        ),
        "qwen2.5-coder:7b-q4_k_m": ModelProfile(
            name="qwen2.5-coder:7b",
            size_gb=4.7,
            quantization="Q4_K_M",
            tokens_per_second=80,
            quality_score=90,
            vram_required_mb=5000,
            recommended_for=[CapabilityTier.LOW, CapabilityTier.MINIMAL],
        ),
        "qwen2.5:7b-q4_k_m": ModelProfile(
            name="qwen2.5:7b",
            size_gb=4.7,
            quantization="Q4_K_M",
            tokens_per_second=85,
            quality_score=88,
            vram_required_mb=5000,
            recommended_for=[CapabilityTier.LOW, CapabilityTier.MINIMAL],
        ),
        "llama3.2:3b": ModelProfile(
            name="llama3.2:3b",
            size_gb=2.0,
            quantization="Q4_K_M",
            tokens_per_second=120,
            quality_score=75,
            vram_required_mb=2500,
            recommended_for=[CapabilityTier.MINIMAL],
        ),
    }

    CONFIGS = {
        "speed": ConfigurationProfile(
            name="Speed",
            num_ctx=128,
            num_predict=4,
            num_gpu=64,
            num_batch=512,
            temperature=0.0,
            top_p=1.0,
            top_k=1,
            use_mlock=True,
            use_mmap=True,
            f16_kv=True,
            system_prompt_length="minimal",
        ),
        "balanced": ConfigurationProfile(
            name="Balanced",
            num_ctx=256,
            num_predict=32,
            num_gpu=64,
            num_batch=512,
            temperature=0.0,
            top_p=1.0,
            top_k=1,
            use_mlock=True,
            use_mmap=True,
            f16_kv=True,
            system_prompt_length="short",
        ),
        "quality": ConfigurationProfile(
            name="Quality",
            num_ctx=512,
            num_predict=128,
            num_gpu=64,
            num_batch=256,
            temperature=0.1,
            top_p=0.9,
            top_k=10,
            use_mlock=True,
            use_mmap=True,
            f16_kv=True,
            system_prompt_length="medium",
        ),
        "extended": ConfigurationProfile(
            name="Extended",
            num_ctx=1024,
            num_predict=256,
            num_gpu=32,
            num_batch=128,
            temperature=0.2,
            top_p=0.85,
            top_k=20,
            use_mlock=True,
            use_mmap=True,
            f16_kv=True,
            system_prompt_length="long",
        ),
    }

    def detect_hardware(self) -> HardwareProfile:
        """Auto-detect hardware capabilities."""
        profile = HardwareProfile(tier=CapabilityTier.MEDIUM)

        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total,memory.used",
                 "--format=csv,noheader"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                parts = [p.strip() for p in result.stdout.strip().split(',')]
                profile.gpu_name = parts[0]
                profile.vram_available_mb = int(parts[1].split()[0])
                profile.vram_mb = int(parts[2].split()[0])

                bandwidth_map = {
                    "4090": 1008,
                    "4080": 736,
                    "4070": 504,
                    "3090": 912,
                    "3080": 760,
                    "3060": 360,
                    "4060": 272,
                    "A100": 2039,
                    "A6000": 768,
                }
                for gpu, bw in bandwidth_map.items():
                    if gpu.lower() in profile.gpu_name.lower():
                        profile.memory_bandwidth_gb_s = bw
                        break

                profile.cuda_available = True

        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
            pass

        try:
            result = subprocess.run(
                ["nproc", "--all"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                profile.cpu_cores = int(result.stdout.strip())
        except Exception:
            pass

        result = subprocess.run(
            ["grep", "MemTotal", "/proc/meminfo"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            mem_kb = int(result.stdout.split()[1])
            profile.ram_gb = mem_kb // (1024 * 1024)

        result = subprocess.run(
            ["journalctl", "-u", "ollama", "-n", "50", "--no-pager"],
            capture_output=True, text=True, timeout=10
        )
        if "flash attention" in result.stdout.lower():
            profile.flash_attention = True

        profile.tier = self._classify_tier(profile)

        return profile

    def _classify_tier(self, profile: HardwareProfile) -> CapabilityTier:
        """Classify hardware into capability tier based on total VRAM."""
        total_vram = profile.vram_available_mb + profile.vram_mb

        if total_vram >= 24000:
            return CapabilityTier.HIGH
        elif total_vram >= 12000:
            return CapabilityTier.MEDIUM
        elif total_vram >= 8000:
            return CapabilityTier.LOW
        else:
            return CapabilityTier.MINIMAL

    def print_diagnostics(self, profile: HardwareProfile) -> None:
        """Print hardware diagnostics."""
        total_vram = profile.vram_available_mb + profile.vram_mb
        print("╔═══════════════════════════════════════════════════════════════════╗")
        print("║                    HARDWARE CAPABILITY DETECTION                     ║")
        print("╠═══════════════════════════════════════════════════════════════════╣")
        print(f"║  GPU:              {profile.gpu_name:<50} ║")
        print(f"║  VRAM:             {profile.vram_mb} MB used / {total_vram} MB total{' ':<20} ║")
        print(f"║  Bandwidth:        {profile.memory_bandwidth_gb_s} GB/s{' ':<35} ║")
        print(f"║  CPU Cores:        {profile.cpu_cores:<50} ║")
        print(f"║  RAM:              {profile.ram_gb} GB{' ':<41} ║")
        print(f"║  CUDA:             {'Yes' if profile.cuda_available else 'No':<50} ║")
        print(f"║  Flash Attention:  {'Yes' if profile.flash_attention else 'No':<50} ║")
        print("╠═══════════════════════════════════════════════════════════════════╣")
        print(f"║  Capability Tier:  {profile.tier.value.upper():<50} ║")
        print("╚═══════════════════════════════════════════════════════════════════╝")

    def recommend_optimization(self, hardware: HardwareProfile) -> dict:
        """Generate optimization recommendations based on hardware."""
        recommendations = {
            "tier": hardware.tier.value,
            "suggestions": [],
            "quantization": None,
            "expected_speedup": 0,
        }

        total_vram = hardware.vram_available_mb + hardware.vram_mb
        usage_percent = (hardware.vram_mb / total_vram * 100) if total_vram > 0 else 0

        if usage_percent > 90:
            recommendations["suggestions"].append({
                "priority": "HIGH",
                "issue": "VRAM usage above 90%",
                "fix": "Use lower quantization (Q3_K_M or Q2_K)",
                "impact": "30-50% speed improvement"
            })
            recommendations["quantization"] = "Q3_K_M"

        if total_vram < 10000:
            recommendations["suggestions"].append({
                "priority": "HIGH",
                "issue": "Limited VRAM (<10GB)",
                "fix": "Use smaller model (7B instead of 14B)",
                "impact": "2x speed improvement"
            })

        if not hardware.flash_attention:
            recommendations["suggestions"].append({
                "priority": "MEDIUM",
                "issue": "Flash Attention not detected",
                "fix": "Set OLLAMA_FLASH_ATTENTION=1",
                "impact": "20-30% prompt processing improvement"
            })

        if hardware.memory_bandwidth_gb_s < 600:
            recommendations["suggestions"].append({
                "priority": "LOW",
                "issue": "Limited memory bandwidth",
                "fix": "Model is bandwidth-limited, quantization won't help much",
                "impact": "Minimal"
            })

        if hardware.tier == CapabilityTier.LOW:
            recommendations["expected_speedup"] = 40
        elif hardware.tier == CapabilityTier.MINIMAL:
            recommendations["expected_speedup"] = 60
        else:
            recommendations["expected_speedup"] = 20

        return recommendations

    def get_optimal_model(self, hardware: HardwareProfile, priority: str = "speed") -> tuple[str, ConfigurationProfile]:
        """Get optimal model + config for hardware and priority."""
        tier = hardware.tier

        available_models = [
            (name, model) for name, model in self.MODELS.items()
            if tier in model.recommended_for
        ]

        if not available_models:
            available_models = list(self.MODELS.items())

        if priority == "speed":
            available_models.sort(key=lambda x: x[1].tokens_per_second, reverse=True)
        elif priority == "quality":
            available_models.sort(key=lambda x: x[1].quality_score, reverse=True)
        else:
            available_models.sort(key=lambda x: x[1].quality_score / x[1].size_gb, reverse=True)

        best_model_name = available_models[0][0]

        if priority == "speed":
            config_name = "speed"
        elif priority == "quality":
            config_name = "quality"
        else:
            config_name = "balanced"

        config = self.CONFIGS[config_name]

        if tier == CapabilityTier.LOW:
            config = self.CONFIGS["speed"]
        elif tier == CapabilityTier.HIGH:
            config = self.CONFIGS["balanced"]

        return best_model_name, config

    def generate_modelfile(self, model_name: str, config: ConfigurationProfile) -> str:
        """Generate Modelfile content from model and config."""
        lines = [
            f"FROM {model_name}",
            f"PARAMETER num_ctx {config.num_ctx}",
            f"PARAMETER num_predict {config.num_predict}",
            f"PARAMETER num_gpu {config.num_gpu}",
            f"PARAMETER num_batch {config.num_batch}",
            f"PARAMETER temperature {config.temperature}",
            f"PARAMETER top_p {config.top_p}",
            f"PARAMETER top_k {config.top_k}",
            f"PARAMETER use_mlock {int(config.use_mlock)}",
            f"PARAMETER use_mmap {int(config.use_mmap)}",
            f"PARAMETER f16_kv {int(config.f16_kv)}",
        ]
        return "\n".join(lines)


def orchestrate(priority: str = "balanced") -> tuple[HardwareProfile, str, ConfigurationProfile]:
    """Main orchestration entry point."""
    orchestrator = HardwareOrchestrator()

    hardware = orchestrator.detect_hardware()
    model_name, config = orchestrator.get_optimal_model(hardware, priority)

    return hardware, model_name, config


if __name__ == "__main__":
    hardware, model, config = orchestrate("speed")

    print("\n")
    orch = HardwareOrchestrator()
    orch.print_diagnostics(hardware)

    print("\n╔═══════════════════════════════════════════════════════════════════╗")
    print("║                      OPTIMAL CONFIGURATION                           ║")
    print("╠═══════════════════════════════════════════════════════════════════╣")
    print(f"║  Model:     {model:<53} ║")
    print(f"║  Config:    {config.name:<53} ║")
    print(f"║  num_ctx:   {config.num_ctx:<53} ║")
    print(f"║  num_gpu:   {config.num_gpu:<53} ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")

    recs = orch.recommend_optimization(hardware)
    print("\n╔═══════════════════════════════════════════════════════════════════╗")
    print("║                      RECOMMENDATIONS                                ║")
    print("╠═══════════════════════════════════════════════════════════════════╣")
    for rec in recs.get("suggestions", []):
        print(f"║  [{rec['priority']}] {rec['issue']:<50} ║")
        print(f"║      Fix: {rec['fix']:<51} ║")
        print(f"║      Impact: {rec['impact']:<48} ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")