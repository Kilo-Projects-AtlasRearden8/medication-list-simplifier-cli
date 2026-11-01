"""Medication list parsing.

Turns free-form medication lines into structured records. Heuristic only;
for education use, never medical advice.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Medication:
    """A single parsed medication entry."""

    name: str
    dose: str | None
    frequency: str | None
    time_of_day: str | None
    raw: str

    def summary_line(self) -> str:
        parts = [self.name]
        for piece in (self.dose, self.frequency, self.time_of_day):
            if piece:
                parts.append(piece)
        return "; ".join(parts)


_DOSE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(mg|mcg|g|ml|units?|iu)\b", re.IGNORECASE)
_FREQUENCY_RE = re.compile(
    r"\b(once|twice|three times|four times|every\s+\d+\s+(?:hours?|hrs?))\b",
    re.IGNORECASE,
)
_TIME_RE = re.compile(
    r"(?:in\s+the\s+|at\s+|with\s+|before\s+|after\s+)?"
    r"(morning|afternoon|evening|bedtime|night|breakfast|lunch|dinner|supper)\b",
    re.IGNORECASE,
)
_COMMENT_RE = re.compile(r"^\s*#")
_BLANK_RE = re.compile(r"^\s*$")

_UNIT_WORDS = {"mg", "mcg", "g", "ml", "unit", "units", "iu"}
_FREQ_STARTERS = {"once", "twice", "three", "four", "every"}
_TIME_WORDS = {
    "morning",
    "afternoon",
    "evening",
    "bedtime",
    "night",
    "breakfast",
    "lunch",
    "dinner",
    "supper",
}


def _token_name(tokens: list[str]) -> str:
    kept: list[str] = []
    for token in tokens:
        low = token.lower().strip(".,;:")
        if re.search(r"\d", token):
            break
        if low in _UNIT_WORDS or low in _FREQ_STARTERS or low in _TIME_WORDS:
            break
        kept.append(token)
    return " ".join(kept).strip(" -,'.")


def parse_medication(line: str) -> Medication | None:
    """Parse one line into a Medication, or None if it has no usable name."""

    if _COMMENT_RE.match(line) or _BLANK_RE.match(line):
        return None

    raw = line.strip()
    tokens = raw.split()
    name = _token_name(tokens)
    if not name:
        return None

    dose_match = _DOSE_RE.search(raw)
    dose = None
    if dose_match:
        dose = f"{dose_match.group(1)} {dose_match.group(2).lower()}"

    freq_match = _FREQUENCY_RE.search(raw)
    frequency = freq_match.group(1).lower() if freq_match else None

    time_match = _TIME_RE.search(raw)
    time_of_day = time_match.group(1).lower() if time_match else None

    return Medication(
        name=name,
        dose=dose,
        frequency=frequency,
        time_of_day=time_of_day,
        raw=raw,
    )


def parse_medication_list(text: str) -> list[Medication]:
    """Parse a block of text into a list of Medication records."""

    results: list[Medication] = []
    for line in text.splitlines():
        med = parse_medication(line)
        if med is not None:
            results.append(med)
    return results
