import re
from pathlib import Path
from .tree import generate_tree


def refresh_agents():
    """Generate tree and update AGENTS.md with current directory structure."""
    project_root = Path(__file__).parent.parent
    src_path = project_root
    agents_file = project_root.parent / "AGENTS.md"

    tree_lines = ["```", "src/"]
    tree_lines.extend(generate_tree(src_path))
    tree_lines.append("```")
    new_tree = "\n".join(tree_lines)

    content = agents_file.read_text()

    pattern = r'(### Directory Structure\n+\nRun `py-ollama-refresh` to update this structure\.\n+\n)```\nsrc/\n.*?\n```'
    replacement = r'\1' + new_tree

    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    agents_file.write_text(content)
    print("AGENTS.md updated successfully!")
