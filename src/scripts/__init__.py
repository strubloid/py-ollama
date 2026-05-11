"""Generate directory tree for the project."""

from pathlib import Path


def generate_tree(dir_path: Path, prefix: str = "", is_last: bool = True, is_root: bool = True) -> list[str]:
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
            lines.extend(generate_tree(entry, prefix + extension, is_last_entry, False))
    
    return lines


def main():
    src_path = Path(__file__).parent.parent
    lines = ["src/"]
    lines.extend(generate_tree(src_path))
    print("\n".join(lines))


if __name__ == "__main__":
    main()