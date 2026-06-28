"""
knowledge_os.__main__

Run with:

    python -m knowledge_os
"""

from __future__ import annotations

from pathlib import Path

from .engine import run


def main() -> None:
    result = run()

    print()
    print("=" * 60)
    print("Knowledge OS")
    print("=" * 60)
    print(f"Day                : {result['day']:03}")
    print()
    print(f"Latest TXT         : {Path(result['latest_text_path']).name}")
    print(f"Latest JSON        : {Path(result['latest_json_path']).name}")
    print()
    print(f"Archive TXT        : {Path(result['archive_text_path']).name}")
    print(f"Archive JSON       : {Path(result['archive_json_path']).name}")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()