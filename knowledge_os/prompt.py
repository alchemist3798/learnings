"""
knowledge_os/prompt.py

Prompt builder for Knowledge OS.

Responsibilities
----------------
- Convert today's study plan into a single OpenAI prompt.
- Define the JSON schema expected from the model.
- Keep prompt engineering isolated from the engine.

This module DOES NOT:
- Call OpenAI
- Parse JSON
- Render notes
"""

from __future__ import annotations

import json
from typing import Any


class PromptBuilder:
    """Builds the prompt sent to OpenAI."""

    SYSTEM_PROMPT = """
You are an exceptional private tutor.

Your goal is to help an intelligent beginner deeply understand today's
lessons.

Teaching style:

- Explain first principles before details.
- Keep each lesson readable in about 10 minutes.
- Be concise but never shallow.
- Use plain English.
- Avoid unnecessary jargon.
- Use headings naturally.
- Never mention tomorrow's lesson.
- Never include homework.
- Never include quizzes.
- Never apologise.
- Never mention you are an AI.
- Assume the lesson will be read inside Apple Notes.

For EVERY subject generate:

1. lesson
   A complete explanation.

2. example
   One memorable example.

3. scenario
   One practical real-world scenario.

4. reflection_question
   One thoughtful question that encourages deeper thinking.

Return ONLY valid JSON.

Do not wrap the JSON in markdown.
Do not include ```json fences.
"""

    def build(
        self,
        plan: dict[str, Any],
    ) -> str:
        """
        Build the prompt sent to OpenAI.

        Parameters
        ----------
        plan
            Output of Planner.today()

        Returns
        -------
        str
            Prompt ready for OpenAI.
        """

        schema = {
            "day": plan["day"],
            "subjects": [],
        }

        for lesson in plan["subjects"]:
            schema["subjects"].append(
                {
                    "subject": lesson["subject"],
                    "lesson_id": lesson["lesson_id"],
                    "title": lesson["title"],
                    "lesson": "...",
                    "example": "...",
                    "scenario": "...",
                    "reflection_question": "...",
                }
            )

        prompt = f"""
{self.SYSTEM_PROMPT}

Today's study plan
==================

{json.dumps(plan, indent=2, ensure_ascii=False)}

Return JSON matching EXACTLY this schema:

{json.dumps(schema, indent=2, ensure_ascii=False)}

Important:

- Preserve every subject.
- Preserve lesson_id.
- Preserve title.
- Do not invent new subjects.
- Do not remove subjects.
- Do not change the JSON structure.
- lesson should be approximately 700-900 words.
- example should be practical.
- scenario should feel realistic.
- reflection_question should require thought, not recall.

Return ONLY JSON.
"""

        return prompt.strip()