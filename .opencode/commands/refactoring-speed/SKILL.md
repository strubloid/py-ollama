---
name: refactoring-speed
description: Py-ollama places to update speed When refactoring.
compatibility: opencode
metadata:
    audience: developers
    workflow: refactoring
---

## What I do

When the user triggers `/speed`, I:

1. Read `configs/speed.config.json` - Contains performance limits and benchmark configuration
2. Read `configs/model_config.json` - Contains model-specific parameters (normal, coder, coder_fast, explained)
3. Read `configs/presets.json` - Contains preset configurations (balanced, coder, coder_fast, coder_balanced, creative, long_context)

## When to use me

- Any refactoring task involving configuration files
- Performance optimization tasks
- Model parameter adjustments
- Preset-related changes

## How to use

Trigger with `/refactoring-speed` command - I will automatically load and analyze the relevant configuration files before proceeding.
