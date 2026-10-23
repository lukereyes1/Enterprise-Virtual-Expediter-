#!/usr/bin/env python3
"""PostToolUse hook: strip invisible Unicode marks from prose files Claude writes.

Runs the clean-user-facing-text skill's deterministic Layer A pass on any
prose file touched by Write/Edit/MultiEdit. Spaces are not normalized, so
NBSP and similar layout characters survive. Never blocks the tool call.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROSE_EXTENSIONS = {".md", ".mdx", ".markdown", ".txt", ".rst", ".html", ".htm"}
SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "clean-user-facing-text" / "scripts"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    file_path = (payload.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0
    path = Path(file_path)
    if path.suffix.lower() not in PROSE_EXTENSIONS or not path.is_file():
        return 0

    sys.path.insert(0, str(SCRIPTS))
    from text_unicode import clean_text

    try:
        original = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return 0

    cleaned, stats = clean_text(original, normalize_spaces=False)
    if cleaned != original:
        path.write_text(cleaned, encoding="utf-8")
        print(
            f"clean-user-facing-text: {path.name} removed={stats['removed_count']} "
            f"replaced={stats['replaced_count']}",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
