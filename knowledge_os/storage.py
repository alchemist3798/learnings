"""
knowledge_os/storage.py

Storage layer for Knowledge OS.

Responsibilities
----------------
- Save the latest lesson output.
- Archive every generated lesson.
- Create directories automatically.
- Return the generated file paths.

Directory Structure
-------------------

output/
│
├── latest.txt
├── latest.json
│
└── archive/
    ├── Day001.txt
    ├── Day001.json
    ├── Day002.txt
    ├── Day002.json
    └── ...
"""

from __future__ import annotations

from pathlib import Path


class Storage:
    """Handles saving Knowledge OS output files."""

    def __init__(
        self,
        output_dir: str | Path = "output",
    ) -> None:

        self.output_dir = Path(output_dir)
        self.archive_dir = self.output_dir / "archive"

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.archive_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def save(
        self,
        day: int,
        rendered: dict[str, str],
    ) -> dict[str, str]:
        """
        Save rendered output.

        Parameters
        ----------
        day
            Current lesson number.

        rendered
            Output from Renderer.render().

            {
                "text": "...",
                "json": "..."
            }

        Returns
        -------
        dict

            {
                "latest_text_path": "...",
                "latest_json_path": "...",
                "archive_text_path": "...",
                "archive_json_path": "..."
            }
        """

        self._validate(rendered)

        filename = f"Day{day:03}"

        latest_text = self.output_dir / "latest.txt"
        latest_json = self.output_dir / "latest.json"

        archive_text = self.archive_dir / f"{filename}.txt"
        archive_json = self.archive_dir / f"{filename}.json"

        # -------------------------------------------------------------- #
        # Latest
        # -------------------------------------------------------------- #

        latest_text.write_text(
            rendered["text"],
            encoding="utf-8",
        )

        latest_json.write_text(
            rendered["json"],
            encoding="utf-8",
        )

        # -------------------------------------------------------------- #
        # Archive
        # -------------------------------------------------------------- #

        archive_text.write_text(
            rendered["text"],
            encoding="utf-8",
        )

        archive_json.write_text(
            rendered["json"],
            encoding="utf-8",
        )

        return {
            "latest_text_path": str(latest_text.resolve()),
            "latest_json_path": str(latest_json.resolve()),
            "archive_text_path": str(archive_text.resolve()),
            "archive_json_path": str(archive_json.resolve()),
        }

    # ------------------------------------------------------------------ #
    # Internal
    # ------------------------------------------------------------------ #

    @staticmethod
    def _validate(
        rendered: dict[str, str],
    ) -> None:
        """
        Ensure renderer output contains everything required.
        """

        required = {
            "text",
            "json",
        }

        missing = required.difference(rendered.keys())

        if missing:
            raise ValueError(
                f"Renderer output missing keys: {', '.join(sorted(missing))}"
            )