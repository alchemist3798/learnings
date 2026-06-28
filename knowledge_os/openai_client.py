"""
knowledge_os/openai_client.py

OpenAI client for Knowledge OS.

Responsibilities
----------------
- Send a prompt to OpenAI
- Expect JSON only
- Return a Python dictionary

No rendering.
No parsing business logic.
No progress management.
"""

from __future__ import annotations

import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


class OpenAIClient:
    """
    Thin wrapper around the OpenAI Responses API.
    """

    def __init__(
        self,
        model: str = "gpt-5",
    ) -> None:
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY not found in environment."
            )

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(
        self,
        prompt: str,
    ) -> dict[str, Any]:
        """
        Generate today's lessons.

        Parameters
        ----------
        prompt
            Prompt built by prompt.py

        Returns
        -------
        dict
            Parsed JSON returned by OpenAI.
        """

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            text={
                "format": {
                    "type": "json_object"
                }
            },
        )

        output = response.output_text.strip()

        if not output:
            raise RuntimeError(
                "OpenAI returned an empty response."
            )

        try:
            return json.loads(output)

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "OpenAI returned invalid JSON."
            ) from exc