"""
knowledge_os/progress.py

Tracks the current learning progress.

Responsibilities
----------------
- Load progress from state/progress.yaml
- Save progress
- Advance to the next lesson
- Return the current day
"""

from __future__ import annotations

from pathlib import Path

import yaml


class Progress:
    def __init__(
        self,
        progress_file: str | Path = "state/progress.yaml",
    ) -> None:
        self.progress_file = Path(progress_file)

        self.day = 1
        self.last_generated = None

    def load(self) -> None:
        """Load progress from disk."""

        if not self.progress_file.exists():
            self.save()
            return

        with self.progress_file.open(
            "r",
            encoding="utf-8",
        ) as f:
            data = yaml.safe_load(f) or {}

        self.day = int(data.get("day", 1))
        self.last_generated = data.get("last_generated")

    def save(self) -> None:
        """Save progress to disk."""

        self.progress_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.progress_file.open(
            "w",
            encoding="utf-8",
        ) as f:
            yaml.safe_dump(
                {
                    "day": self.day,
                    "last_generated": self.last_generated,
                },
                f,
                sort_keys=False,
                allow_unicode=True,
            )

    def advance(self) -> None:
        """Advance to the next lesson."""

        self.day += 1

    def today(self) -> int:
        """Return the current lesson/day."""

        return self.day