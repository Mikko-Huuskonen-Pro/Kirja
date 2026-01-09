#!/usr/bin/env python3
"""
Translation Manager for Rust Book
Helps manage translations by identifying missing files and providing utilities
"""

import os
import sys
from pathlib import Path
from typing import Set, List, Tuple

# Base paths
BASE_DIR = Path(__file__).parent.parent
EN_SRC = BASE_DIR / "src"
FI_SRC = BASE_DIR / "src" / "fi"

# Files to exclude from comparison
EXCLUDE_FILES = {"SUMMARY.md", "img"}


def get_markdown_files(directory: Path) -> Set[str]:
    """Get all markdown files from a directory, excluding certain files."""
    files = set()
    for file_path in directory.rglob("*.md"):
        relative = file_path.relative_to(directory)
        # Skip files in subdirectories like img/
        if relative.parts[0] not in EXCLUDE_FILES:
            files.add(str(relative))
    return files


def find_missing_translations() -> Tuple[List[str], List[str]]:
    """Find files that are missing in Finnish translation."""
    en_files = get_markdown_files(EN_SRC)
    fi_files = get_markdown_files(FI_SRC)
    
    missing = sorted(en_files - fi_files)
    extra = sorted(fi_files - en_files)
    
    return missing, extra


def check_translation_status():
    """Check and report translation status."""
    missing, extra = find_missing_translations()
    
    print("=" * 60)
    print("Translation Status Report")
    print("=" * 60)
    print(f"\nMissing Finnish translations ({len(missing)} files):")
    if missing:
        for file in missing:
            print(f"  - {file}")
    else:
        print("  ✓ All files translated!")
    
    if extra:
        print(f"\nExtra files in Finnish directory ({len(extra)} files):")
        for file in extra:
            print(f"  - {file}")
    
    print("\n" + "=" * 60)
    
    return missing, extra


def generate_translation_template(missing_file: str):
    """Generate a template for translating a file."""
    en_path = EN_SRC / missing_file
    fi_path = FI_SRC / missing_file
    
    if not en_path.exists():
        print(f"Error: {en_path} does not exist")
        return
    
    # Create directory if needed
    fi_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Read English file
    with open(en_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Write template (for now, just copy - translation should be done manually)
    with open(fi_path, "w", encoding="utf-8") as f:
        f.write(f"# TODO: Translate this file from {missing_file}\n\n")
        f.write(content)
    
    print(f"Created translation template: {fi_path}")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "status":
            check_translation_status()
        elif command == "missing":
            missing, _ = find_missing_translations()
            for file in missing:
                print(file)
        elif command == "template" and len(sys.argv) > 2:
            generate_translation_template(sys.argv[2])
        else:
            print("Usage:")
            print("  python translation-manager.py status      - Show translation status")
            print("  python translation-manager.py missing     - List missing files")
            print("  python translation-manager.py template <file> - Create template for file")
    else:
        check_translation_status()


if __name__ == "__main__":
    main()
