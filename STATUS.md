# STATUS

## What was built

`medsplain` (v0.1.0) - a local-first Python CLI that turns medication lists
into plain-English summaries and printable schedule charts, using a
configurable OpenAI-compatible LLM endpoint (default: local Ollama at
http://localhost:11434/v1).

- `medsplain summarize -i meds.txt` - plain-English summary of a medication
  list, with the LLM response (or an offline fallback summary if the endpoint
  is unreachable).
- `medsplain chart -i meds.txt -o schedule.svg` - printable SVG schedule chart
  (Morning / Midday / Evening / Bedtime buckets). `--format text` for a
  plain-text chart; `-o` writes to a file, otherwise prints to stdout.
- Reads from a file (`-i`) or stdin.
- `--endpoint`, `--model`, and `--timeout` are configurable; no API keys or
  accounts required.
- Parser (`src/medsplain/parser.py`) extracts name, dose, frequency, and time
  of day from free-form lines; blank lines and `#` comments are skipped.
- Every output carries a prominent education-only disclaimer: not medical
  advice, not a prescription, consult a prescriber/pharmacist before changes.

## How to run

```bash
# install (isolated venv recommended)
python3 -m venv .venv
source .venv/bin/activate
pip install .

# example list: Lisinopril 10 mg once daily in the morning
medsplain summarize -i meds.txt
medsplain chart -i meds.txt -o schedule.svg
cat meds.txt | medsplain summarize
medsplain chart -i meds.txt --format text
```

Endpoint example: `medsplain summarize -i meds.txt --endpoint http://localhost:1234/v1 --model mistral`

## Verification results

- `pip install -e .` - OK (built and installed in a venv; system Python is
  PEP 668 externally managed, so a venv is required).
- `python3 -m unittest discover -s tests -v` - OK: 10 tests, 10 passed,
  covering name/dose/frequency/time parsing, case insensitivity, comment and
  blank line handling, name-only lines, and multi-line lists.
- CLI smoke test (offline, no Ollama running): `summarize` prints a full
  summary with disclaimer and falls back to the local fallback summary;
  `chart --format svg` produces a valid SVG (parsed with xml.dom.minidom);
  `chart --format text` prints a readable schedule chart.
- No .github/workflows added. No secrets, API keys, or personal data in any
  file. Git initialized with one commit, identity Dylan Asdale
  (dylanasdale@users.noreply.github.com), no remote, not pushed.

## Known gaps

- No Ollama server available in this environment, so the LLM code path was
  not exercised end-to-end; the offline fallback path was verified instead.
- Chart text cells are fixed-width (34 chars); very long entries may
  truncate.
- SVG chart is basic (no color coding by day, no per-day columns).
- Parser is heuristic: unusual medication names or free-form wording may
  parse partially; always verify parsed output against the prescription
  bottle.
- Education only - not for clinical decisions.

## Files

- LICENSE - MIT, Copyright (c) 2026 Asdale Dynamics, LLC
- README.md - usage, disclaimer, credits Asdale Dynamics, LLC
- pyproject.toml - package metadata + `medsplain` console script
- src/medsplain/ - CLI, LLM client, parser, formatters, disclaimer
- tests/test_parser.py - 10 parser tests
- .gitignore - venv and build artifacts
