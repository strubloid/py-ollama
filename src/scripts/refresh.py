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

    header_pattern = r'### Directory Structure\n\nRun `py-ollama-refresh` to update this structure\.\n\n'
    tree_pattern = r'```\nsrc/\n.*?```'

    has_header = bool(re.search(header_pattern, content))
    tree_match = re.search(tree_pattern, content, flags=re.DOTALL)

    if has_header and tree_match:
        current_tree = tree_match.group()
        if current_tree != new_tree:
            new_content = content.replace(current_tree, new_tree, 1)
            agents_file.write_text(new_content)
            print("AGENTS.md updated successfully!")
        else:
            print("AGENTS.md already up to date.")
    else:
        print("Warning: AGENTS.md is missing Directory Structure section. Skipping update.")