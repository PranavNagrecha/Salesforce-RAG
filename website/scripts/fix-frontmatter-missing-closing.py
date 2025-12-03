#!/usr/bin/env python3
"""
Quick fixer for RAG markdown files that are missing a closing --- in Jekyll frontmatter.

Context:
- validate-frontmatter.py reports "Invalid frontmatter format (no closing ---)"
- These files already start with --- and have required keys, but never close the block.

Strategy:
- For all markdown files under rag/ (excluding the same special files as the validator):
  - If the file starts with --- and has no subsequent --- line:
    - Insert a closing --- just before the first obvious content line
      (heading, list item, numbered list) or before the first blank line.
"""

from pathlib import Path
import re


def needs_closing_frontmatter(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines:
        return False
    if lines[0].strip() != "---":
        return False

    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            # Already has a closing marker
            return False
    return True


def insert_closing_frontmatter(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return False

    # Find where to close frontmatter:
    # - before first blank line
    # - or before first likely content line (heading, list, numbered list)
    closing_idx = None
    for i in range(1, len(lines)):
        stripped = lines[i].lstrip()

        if stripped == "":
            closing_idx = i
            break

        if re.match(r"^(#{1,6}\s|\- |\* |\d+\. )", stripped):
            closing_idx = i
            break

    if closing_idx is None:
        # Fall back to closing at end of file
        closing_idx = len(lines)

    # Insert closing --- at the chosen location if not already present there
    if closing_idx > 0 and lines[closing_idx - 1].strip() == "---":
        return False

    lines.insert(closing_idx, "---")
    new_text = "\n".join(lines) + "\n"
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    rag_dir = Path("rag")
    if not rag_dir.exists():
        print("rag/ directory not found; nothing to do.")
        return

    excluded = {
        "rag-index.md",
        "README.md",
        "CONTRIBUTING.md",
        "MAINTENANCE.md",
        "code-examples-index.md",
    }

    md_files = [
        f
        for f in rag_dir.rglob("*.md")
        if f.name not in excluded
    ]

    fixed = []
    skipped = []
    for path in sorted(md_files):
        if needs_closing_frontmatter(path):
            if insert_closing_frontmatter(path):
                fixed.append(path)
            else:
                skipped.append(path)
        else:
            skipped.append(path)

    print(f"Processed {len(md_files)} markdown files under rag/")
    print(f"Fixed {len(fixed)} files with missing closing frontmatter marker.")
    if fixed:
        print("Fixed files:")
        for p in fixed:
            print(f"  - {p}")


if __name__ == "__main__":
    main()


