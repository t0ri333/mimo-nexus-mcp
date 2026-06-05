"""Context Synthesizer - Local file scanning and context packaging.

Scans a directory, filters irrelevant files, and packages source code
into a structured Markdown payload optimized for LLM consumption.
"""

import os
from pathlib import Path

from .config import SKIP_DIRS, SKIP_EXTENSIONS, MAX_FILE_SIZE


def scan_directory(
    target_path: str,
    skip_dirs: set[str] | None = None,
    skip_extensions: set[str] | None = None,
    max_file_size: int = MAX_FILE_SIZE,
) -> list[tuple[str, str]]:
    """Recursively scan a directory and collect source files.

    Args:
        target_path: Root directory to scan
        skip_dirs: Directory names to skip (defaults to SKIP_DIRS)
        skip_extensions: File extensions to skip (defaults to SKIP_EXTENSIONS)
        max_file_size: Max file size in bytes

    Returns:
        List of (relative_path, file_content) tuples
    """
    skip_dirs = skip_dirs or SKIP_DIRS
    skip_extensions = skip_extensions or SKIP_EXTENSIONS
    root = Path(target_path).resolve()

    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {target_path}")
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {target_path}")

    files: list[tuple[str, str]] = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune skipped directories in-place
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]

        for filename in sorted(filenames):
            filepath = Path(dirpath) / filename
            ext = filepath.suffix.lower()

            if ext in skip_extensions:
                continue

            # Skip files without extension that are likely binary
            if not ext and _is_likely_binary(filepath):
                continue

            try:
                if filepath.stat().st_size > max_file_size:
                    continue
            except OSError:
                continue

            try:
                content = filepath.read_text(encoding="utf-8", errors="ignore")
            except (OSError, PermissionError):
                continue

            rel_path = filepath.relative_to(root)
            files.append((str(rel_path), content))

    return files


def _is_likely_binary(filepath: Path) -> bool:
    """Quick heuristic to detect binary files without extensions."""
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(8192)
            return b"\x00" in chunk
    except OSError:
        return True


def build_context_payload(
    files: list[tuple[str, str]],
    query: str,
    max_tokens_estimate: int = 800_000,
) -> str:
    """Package scanned files into a structured Markdown payload.

    Formats files with clear path headers for optimal LLM readability.
    Truncates if the combined payload exceeds the token estimate.

    Args:
        files: List of (relative_path, content) tuples
        query: The user's focus query to prepend
        max_tokens_estimate: Approximate character limit (chars ≈ tokens * 4)

    Returns:
        Formatted Markdown string ready for LLM consumption
    """
    header = f"""# Codebase Analysis Request

## Focus Question
{query}

## Project Source Files

"""
    sections: list[str] = []
    total_chars = len(header)
    char_limit = max_tokens_estimate * 4  # rough chars-to-tokens ratio

    for rel_path, content in files:
        section = f"""### `{rel_path}`
```
{content}
```

"""
        if total_chars + len(section) > char_limit:
            sections.append(f"\n> **Note:** {len(files) - len(sections)} files total. "
                            f"Remaining files truncated due to context limit.\n")
            break

        sections.append(section)
        total_chars += len(section)

    return header + "".join(sections)
