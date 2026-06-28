"""
knowledge_os/renderer.py

Renderer for Knowledge OS.

Responsibilities
----------------
- Render the OpenAI JSON response into:
    1. UTF-8 plain text (Apple Notes)
    2. Pretty JSON (archive/debug)

This module does NOT:
- Save files
- Call OpenAI
- Update progress
"""

from __future__ import annotations

import json
from datetime import date
from typing import Any


class Renderer:
    """Render today's lessons into text and JSON."""

    DIVIDER = "═" * 70

    def render(self, lesson: dict[str, Any]) -> dict[str, str]:
        """
        Render today's lesson.

        Parameters
        ----------
        lesson
            JSON returned by OpenAI.

        Returns
        -------
        dict
            {
                "text": "...",
                "json": "..."
            }
        """

        return {
            "text": self._render_text(lesson),
            "json": self._render_json(lesson),
        }

    # ------------------------------------------------------------------
    # JSON
    # ------------------------------------------------------------------

    def _render_json(
        self,
        lesson: dict[str, Any],
    ) -> str:
        return json.dumps(
            lesson,
            indent=2,
            ensure_ascii=False,
        )

    # ------------------------------------------------------------------
    # TEXT
    # ------------------------------------------------------------------

    def _render_text(
        self,
        lesson: dict[str, Any],
    ) -> str:
        lines: list[str] = []

        day = lesson.get("day", "?")

        today = lesson.get(
            "date",
            date.today().isoformat(),
        )

        lines.append("Knowledge OS")
        lines.append(f"Day {day:03}" if isinstance(day, int) else f"Day {day}")
        lines.append(today)
        lines.append("")
        lines.append(self.DIVIDER)
        lines.append("")

        for subject in lesson.get("subjects", []):

            self._render_subject(lines, subject)

        return "\n".join(lines).rstrip() + "\n"

    # ------------------------------------------------------------------
    # Subject
    # ------------------------------------------------------------------

    def _render_subject(
        self,
        lines: list[str],
        subject: dict[str, Any],
    ) -> None:

        title = subject.get("subject", "").upper()

        lines.append(title)
        lines.append("-" * len(title))
        lines.append("")

        self._section(
            lines,
            "Topic",
            subject.get("title"),
        )

        self._section(
            lines,
            "Lesson",
            subject.get("lesson"),
        )

        self._section(
            lines,
            "Example",
            subject.get("example"),
        )

        self._section(
            lines,
            "Scenario",
            subject.get("scenario"),
        )

        self._section(
            lines,
            "Reflection Question",
            subject.get("reflection_question"),
        )

        lines.append(self.DIVIDER)
        lines.append("")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _section(
        lines: list[str],
        heading: str,
        value: Any,
    ) -> None:

        if value is None:
            return

        text = str(value).strip()

        if not text:
            return

        lines.append(heading)
        lines.append("")
        lines.append(text)
        lines.append("")