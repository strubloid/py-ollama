#!/usr/bin/env python3
"""
Hardware orchestration CLI.

Usage:
    python -m ai.orchestration.hardware
    python -m ai.orchestration.hardware --priority speed
    python -m ai.orchestration.hardware --priority quality
    python -m ai.orchestration.hardware --priority balanced
    python -m ai.orchestration.hardware --diagnose
    python -m ai.orchestration.hardware --modelfile-only
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Hardware-aware model orchestration")
    parser.add_argument(
        "--priority",
        choices=["speed", "quality", "balanced"],
        default="balanced",
        help="Optimization priority"
    )
    parser.add_argument(
        "--diagnose",
        action="store_true",
        help="Run hardware diagnostics"
    )
    parser.add_argument(
        "--modelfile-only",
        action="store_true",
        help="Only output modelfile content"
    )
    parser.add_argument(
        "--model",
        help="Override model selection"
    )
    parser.add_argument(
        "--config",
        choices=["speed", "balanced", "quality", "extended"],
        help="Override config selection"
    )

    args = parser.parse_args()

    from ai.orchestration.hardware import HardwareOrchestrator, orchestrate

    orchestrator = HardwareOrchestrator()
    hardware = orchestrator.detect_hardware()

    if args.diagnose:
        orchestrator.print_diagnostics(hardware)
        recs = orchestrator.recommend_optimization(hardware)

        print("\n╔═══════════════════════════════════════════════════════════════════╗")
        print("║                      RECOMMENDATIONS                                ║")
        print("╠═══════════════════════════════════════════════════════════════════╣")
        if recs.get("suggestions"):
            for rec in recs["suggestions"]:
                print(f"║  [{rec['priority']:^6}] {rec['issue']:<50} ║")
                print(f"║            Fix: {rec['fix']:<47} ║")
                print(f"║            Impact: {rec['impact']:<42} ║")
        else:
            print("║  No specific recommendations. Hardware appears optimal.        ║")
        print("╚═══════════════════════════════════════════════════════════════════╝")
        return 0

    if args.model:
        model_name = args.model
        if args.config:
            config = orchestrator.CONFIGS[args.config]
        else:
            _, config = orchestrator.get_optimal_model(hardware, args.priority)
    else:
        _, model_name, config = orchestrate(args.priority)
        if args.config:
            config = orchestrator.CONFIGS[args.config]

    modelfile = orchestrator.generate_modelfile(model_name, config)

    if args.modelfile_only:
        print(modelfile)
    else:
        print("╔═══════════════════════════════════════════════════════════════════╗")
        print("║            HARDWARE-OPTIMIZED CONFIGURATION                        ║")
        print("╠═══════════════════════════════════════════════════════════════════╣")
        print(f"║  Hardware Tier: {hardware.tier.value.upper():<45} ║")
        print(f"║  GPU: {hardware.gpu_name or 'Unknown':<56} ║")
        print(f"║  VRAM Available: {hardware.vram_available_mb} MB{' ':<39} ║")
        print("╠═══════════════════════════════════════════════════════════════════╣")
        print(f"║  Recommended Model: {model_name:<49} ║")
        print(f"║  Configuration: {config.name:<50} ║")
        print("╠═══════════════════════════════════════════════════════════════════╣")
        print("║  GENERATED MODELFILE:                                              ║")
        print("╠═══════════════════════════════════════════════════════════════════╣")
        for line in modelfile.split('\n'):
            print(f"║  {line:<65} ║")
        print("╚═══════════════════════════════════════════════════════════════════╝")

        print("\nTo use this configuration:")
        print(f"  py-ollama {model_name} my-custom-model 2")
        print("\nOr create manually with the modelfile above.")

    return 0


if __name__ == "__main__":
    sys.exit(main())