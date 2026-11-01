"""OpenAI-compatible LLM client, defaulting to a local Ollama endpoint.

No API keys are ever required. If the endpoint cannot be reached, a local
fallback summary is produced so the tool works completely offline.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass

from .parser import Medication


@dataclass(frozen=True)
class LLMResponse:
    text: str
    source: str  # "llm" or "fallback"


DEFAULT_ENDPOINT = "http://localhost:11434/v1"
DEFAULT_MODEL = "llama3"
DEFAULT_TIMEOUT = 30.0

_SYSTEM_PROMPT = (
    "You are an education-only assistant. Rewrite the medication list below "
    "in plain, warm, beginner-friendly English. Never give medical advice. "
    "Never tell the user to start, stop, or change any medication. Restate "
    "each medicine's name, dose, and timing simply, then remind the user to "
    "confirm everything with their pharmacist or prescriber. Do not invent "
    "indications or purposes for any medicine."
)


class LLMClient:
    def __init__(
        self,
        endpoint: str = DEFAULT_ENDPOINT,
        model: str = DEFAULT_MODEL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.timeout = timeout

    def summarize(self, medications: list[Medication], raw_text: str = "") -> LLMResponse:
        prompt = self._build_prompt(medications, raw_text)
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "temperature": 0.3,
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            request = urllib.request.Request(
                f"{self.endpoint}/chat/completions",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
            text = body["choices"][0]["message"]["content"].strip()
            if not text:
                raise ValueError("empty completion")
            return LLMResponse(text=text, source="llm")
        except (urllib.error.URLError, OSError, json.JSONDecodeError, KeyError, ValueError, IndexError):
            return LLMResponse(text=self._fallback_summary(medications), source="fallback")

    @staticmethod
    def _build_prompt(medications: list[Medication], raw_text: str) -> str:
        lines = ["Medications to summarize:"]
        for med in medications:
            lines.append(f"- {med.summary_line()}")
        if raw_text:
            lines.append("")
            lines.append("Original list:")
            lines.append(raw_text)
        return "\n".join(lines)

    @staticmethod
    def _fallback_summary(medications: list[Medication]) -> str:
        count = len(medications)
        lines = [
            f"Here is a plain-English summary of your {count} medication"
            + ("s" if count != 1 else "")
            + ":",
        ]
        for med in medications:
            lines.append(f"- {med.summary_line()}")
        lines.append("")
        lines.append(
            "Take each medicine exactly as prescribed by your healthcare "
            "provider. If anything here looks different from what your "
            "prescriber or pharmacist told you, ask them before taking it."
        )
        return "\n".join(lines)
