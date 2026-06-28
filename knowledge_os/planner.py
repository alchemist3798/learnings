"""
knowledge_os/planner.py

Planner for Knowledge OS.

Responsibilities
----------------
- Read progress.yaml
- Read every curriculum YAML in the curriculums/ directory
- Flatten modules into a single ordered lesson list
- Select today's lesson from each curriculum
- Return one study plan dictionary

The planner DOES NOT:
- Call OpenAI
- Build prompts
- Render notes
- Update progress
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from .progress import Progress

progress = Progress()
progress.load()

day = progress.today()

import yaml


class Planner:
    """Creates today's study plan from the curricula."""

    def __init__(
        self,
        curriculum_dir: str | Path = "curriculums",
        progress_file: str | Path = "state/progress.yaml",
    ) -> None:
        self.curriculum_dir = Path(curriculum_dir)
        self.progress_file = Path(progress_file)

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #

    def today(self) -> dict[str, Any]:
        """
        Return today's study plan.

        Example
        -------
        {
            "day": 7,
            "subjects": [
                {
                    "subject": "microeconomics",
                    "lesson_number": 7,
                    "lesson_id": "MICRO-007",
                    "title": "...",
                    "difficulty": "Beginner",
                    "estimated_time": 10,
                    "objectives": [...],
                    "mental_models": [...],
                    "prerequisites": [...],
                    "tags": [...],
                    "project": False
                }
            ]
        }
        """
        progress = Progress()
        progress.load()

        day = progress.today()

        subjects: list[dict[str, Any]] = []

        for curriculum in sorted(self.curriculum_dir.glob("*.yaml")):
            subjects.append(self._lesson_for_day(curriculum, day))

        return {
            "day": day,
            "subjects": subjects,
        }

    # --------------------------------------------------------------------- #
    # Internal
    # --------------------------------------------------------------------- #

    def _lesson_for_day(
        self,
        curriculum_file: Path,
        day: int,
    ) -> dict[str, Any]:
        curriculum = self._load_curriculum(curriculum_file)

        lessons = self._flatten_lessons(curriculum)

        if day > len(lessons):
            raise ValueError(
                f"{curriculum['subject']} only contains "
                f"{len(lessons)} lessons "
                f"(requested Day {day})."
            )

        lesson = lessons[day - 1]

        return {
            "subject": curriculum["subject"],
            "lesson_number": day,
            "lesson_id": lesson["id"],
            "title": lesson["title"],
            "difficulty": lesson.get("difficulty"),
            "estimated_time": lesson.get(
                "estimated_time",
                curriculum.get("reading_time_per_lesson", 10),
            ),
            "objectives": lesson.get("objectives", []),
            "mental_models": lesson.get("mental_models", []),
            "prerequisites": lesson.get("prerequisites", []),
            "tags": lesson.get("tags", []),
            "project": lesson.get("project", False),
        }

    @staticmethod
    def _load_curriculum(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @staticmethod
    def _flatten_lessons(curriculum: dict[str, Any]) -> list[dict[str, Any]]:
        lessons: list[dict[str, Any]] = []

        for module in curriculum.get("modules", []):
            for lesson in module.get("lessons", []):
                lessons.append(lesson)

        return lessons