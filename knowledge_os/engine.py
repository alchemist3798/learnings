"""
knowledge_os/engine.py

Coordinates the Knowledge OS workflow.

Workflow
--------
1. Load progress.
2. Read today's study plan.
3. Build the OpenAI prompt.
4. Generate today's lessons.
5. Render text and JSON.
6. Save latest + archive files.
7. Advance progress.
8. Return generated file paths.
"""

from __future__ import annotations

from .openai_client import OpenAIClient
from .planner import Planner
from .progress import Progress
from .prompt import PromptBuilder
from .renderer import Renderer
from .storage import Storage


class Engine:
    """Main Knowledge OS engine."""

    def __init__(self) -> None:
        self.progress = Progress()
        self.planner = Planner()
        self.prompt_builder = PromptBuilder()
        self.client = OpenAIClient()
        self.renderer = Renderer()
        self.storage = Storage()

    def run(self) -> dict[str, str]:
        """
        Execute the complete Knowledge OS workflow.

        Returns
        -------
        dict
            {
                "day": 1,
                "latest_text_path": "...",
                "latest_json_path": "...",
                "archive_text_path": "...",
                "archive_json_path": "..."
            }
        """

        # --------------------------------------------------------------
        # Load current progress
        # --------------------------------------------------------------

        self.progress.load()

        # --------------------------------------------------------------
        # Build today's study plan
        # --------------------------------------------------------------

        plan = self.planner.today()

        # --------------------------------------------------------------
        # Build prompt
        # --------------------------------------------------------------

        prompt = self.prompt_builder.build(plan)

        # --------------------------------------------------------------
        # Generate lessons
        # --------------------------------------------------------------

        lesson = self.client.generate(prompt)

        # Ensure renderer always has today's metadata
        lesson["day"] = plan["day"]

        # --------------------------------------------------------------
        # Render output
        # --------------------------------------------------------------

        rendered = self.renderer.render(lesson)

        # --------------------------------------------------------------
        # Save output
        # --------------------------------------------------------------

        paths = self.storage.save(
            day=plan["day"],
            rendered=rendered,
        )

        # --------------------------------------------------------------
        # Advance progress
        # --------------------------------------------------------------

        self.progress.advance()
        self.progress.save()

        # --------------------------------------------------------------
        # Return generated files
        # --------------------------------------------------------------

        return {
            "day": plan["day"],
            "latest_text_path": paths["latest_text_path"],
            "latest_json_path": paths["latest_json_path"],
            "archive_text_path": paths["archive_text_path"],
            "archive_json_path": paths["archive_json_path"],
        }


def run() -> dict[str, str]:
    """
    Convenience entry point.

    Example
    -------
    >>> from knowledge_os.engine import run
    >>> result = run()
    """

    return Engine().run()