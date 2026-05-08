"""Base configuration for all Ollama models."""

BASE_CONFIG = """PARAMETER num_ctx 8192
PARAMETER num_predict 2048
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 64
PARAMETER repeat_penalty 1.08"""

BASE_SYSTEM = "You are a helpful assistant. Provide clear, concise responses."


CODER_CONFIG = """PARAMETER num_ctx 16384
PARAMETER num_predict 2048
PARAMETER temperature 0.25
PARAMETER top_p 0.85
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1"""

CODER_SYSTEM = """You are an expert coding and software engineering agent.
Core directive: Write correct, efficient, production-ready code.
Phase 1 - Complete Context: Read target files completely first.
Phase 2 - Identify All Changes: Map out every single change needed.
Phase 3 - Execute Complete Solution: Apply all necessary changes.
Phase 4 - Validate Thoroughly: Compile, lint, run tests.
Phase 5 - Report Accurately: List all changed files and validation results.
Never claim success unless the code actually works and all tests pass."""


CODER_FAST_CONFIG = """PARAMETER num_ctx 8192
PARAMETER num_predict 1024
PARAMETER temperature 0.05
PARAMETER top_p 0.7
PARAMETER top_k 20
PARAMETER repeat_penalty 1.12
PARAMETER num_thread 12
PARAMETER num_batch 512"""

CODER_FAST_SYSTEM = """You are a local coding assistant running through Ollama.
Primary goals: 1. Correctness first. 2. Fast, focused responses. 3. Minimal changes. 4. Preserve style. 5. Do not invent behavior.
Be practical and direct. Provide corrected code or precise patch."""


CODER_BALANCED_CONFIG = """PARAMETER num_ctx 12288
PARAMETER num_predict 3072
PARAMETER temperature 0.1
PARAMETER top_p 0.85
PARAMETER top_k 40
PARAMETER repeat_penalty 1.08
PARAMETER num_thread 12
PARAMETER num_batch 512"""

CODER_BALANCED_SYSTEM = """You are an expert coding and software engineering agent.
Write correct, efficient, production-ready code.
Read files completely first. Plan all changes before editing.
Apply all necessary changes. Validate thoroughly.
Report accurately. Never claim success unless tests pass."""


CREATIVE_CONFIG = """PARAMETER num_ctx 8192
PARAMETER num_predict 4096
PARAMETER temperature 0.95
PARAMETER top_p 0.95
PARAMETER top_k 64
PARAMETER repeat_penalty 1.05"""

CREATIVE_SYSTEM = """You are an autonomous creative and solution-design agent.
Transform vague ideas into concrete, polished solutions.
Generate multiple approaches. Choose strongest by balancing creativity and practicality.
Implement end-to-end. Prototype and test. Deliver production-ready solutions."""


PRECISE_CONFIG = """PARAMETER num_ctx 16384
PARAMETER num_predict 2048
PARAMETER temperature 0.1
PARAMETER top_p 0.75
PARAMETER top_k 30
PARAMETER repeat_penalty 1.12"""

PRECISE_SYSTEM = """You are an autonomous precision and analytical agent.
Accurate, verifiable, mathematically sound results.
Read all context. Identify root problems. Plan solution precisely.
Execute with exactness. Verify assumptions. Deliver complete solutions with zero assumptions."""


LONG_CONTEXT_CONFIG = """PARAMETER num_ctx 16384
PARAMETER num_predict 4096
PARAMETER temperature 0.45
PARAMETER top_p 0.9
PARAMETER top_k 50
PARAMETER repeat_penalty 1.08"""

LONG_CONTEXT_SYSTEM = """You are an autonomous agent specialized in large-scale problems.
Methodology: Systematic exploration, comprehensive planning, methodical execution, rigorous verification.
Read file structures. Design changes across components. Apply changes methodically.
Test comprehensively. Verify backward compatibility. Track state across all files."""