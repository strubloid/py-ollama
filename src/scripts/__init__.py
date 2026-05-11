"""Scripts for py-ollama project."""

from pathlib import Path
import re


def generate_tree(dir_path: Path, prefix: str = "") -> list[str]:
    """Recursively generate tree structure."""
    lines = []
    
    entries = sorted(
        [e for e in dir_path.iterdir() 
         if e.name != "__pycache__" and not e.name.endswith(".egg-info")],
        key=lambda x: (not x.is_dir(), x.name)
    )
    
    for i, entry in enumerate(entries):
        is_last_entry = i == len(entries) - 1
        connector = "└── " if is_last_entry else "├── "
        lines.append(f"{prefix}{connector}{entry.name}")
        
        if entry.is_dir():
            extension = "    " if is_last_entry else "│   "
            lines.extend(generate_tree(entry, prefix + extension))
    
    return lines


def main():
    """Generate and print directory tree."""
    project_root = Path(__file__).parent.parent
    src_path = project_root
    
    lines = ["src/"]
    lines.extend(generate_tree(src_path))
    print("\n".join(lines))


def refresh():
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