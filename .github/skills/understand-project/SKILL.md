---
name: understand-project
description: Understand the py-ollama project structure, architecture, configs, presets, tests, and development rules before making changes
compatibility: opencode
metadata:
    audience: developers
---

You are analyzing this repository before doing any development work.

Do not edit files during this command. Only inspect, summarize, and identify risks.

## Goal

Build a practical understanding of the `py-ollama` project before making changes.

Focus on:

- project structure
- CLI entrypoints
- configuration loading
- preset loading
- model-family detection
- Modelfile generation
- tests
- development rules
- risks and invariants

## Required files to inspect

Read these first when they exist:

- `AGENTS.md`
- `AGENTS.PREFERENCES.md`
- `README.md`
- `pyproject.toml`

Then inspect:

- `speed.config.json`
- `src/ai/config/`
- `src/ai/presets/`
- `src/ai/models/`
- `src/ai/modelfile/`
- `tests/`

## Required output

Produce a concise but practical report with these sections:

1. Project Identity
2. CLI Entrypoints and Commands
3. Architecture Overview / Data Flow
4. Key Datatypes and Objects
5. Config and Preset Loading
6. Model Family System
7. Modelfile Generation
8. Tests and Quality Commands
9. Important Invariants
10. Change Impact Risks
11. Recommended Next Steps

## Rules

- Do not edit files.
- Do not assume stale details are still true.
- Prefer evidence from the current repository.
- Mention file paths when useful.
- Highlight risks before suggesting changes.
- Keep the summary actionable for development work.
