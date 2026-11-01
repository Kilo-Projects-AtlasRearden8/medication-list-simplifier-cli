# medsplain

Plain-English medication list summaries and printable charts, powered by a
configurable OpenAI-compatible endpoint (default: local Ollama).

Built by **Asdale Dynamics, LLC** (Indiana) — beginner-friendly AI education,
plain English, step by step, never condescending. See
[dylanasdale.github.io](https://dylanasdale.github.io) and *The Massive AI
Manual* by Dylan Asdale.

## Education only - never medical advice

This tool is for education only. It is **not medical advice**, not a
prescription, and not a substitute for a doctor, pharmacist, or other
qualified healthcare professional. Never start, stop, or change a medication
based on this output. Always confirm instructions with your prescriber or
pharmacist before making changes.

Every summary and chart medsplain produces includes this reminder, so it
travels with the output wherever you print or share it.

## Local-first, no keys

No API keys, no accounts, no cloud required by default. medsplain talks to a
local Ollama server at `http://localhost:11434/v1` (OpenAI-compatible chat
completions). Point `--endpoint` at any OpenAI-compatible server (LLM Studio,
vLLM, etc.) if you prefer. If the endpoint cannot be reached, medsplain still
produces a plain summary from your parsed list, so it works fully offline.

## Install

A virtual environment keeps things tidy and isolated:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

Or install directly:

```bash
pip install .
```

## Usage

Save a medication list, one per line:

```
Lisinopril 10 mg once daily in the morning
Metformin 500 mg twice daily with breakfast and dinner
Atorvastatin 20 mg at bedtime
```

### Summarize a list in plain English

```bash
medsplain summarize -i meds.txt
```

Use a different endpoint or model:

```bash
medsplain summarize -i meds.txt --endpoint http://localhost:1234/v1 --model mistral
```

Save the summary to a file:

```bash
medsplain summarize -i meds.txt -o summary.txt
```

Read from stdin:

```bash
cat meds.txt | medsplain summarize
```

### Create a printable schedule chart

The default chart is SVG, which prints cleanly and scales to any paper size:

```bash
medsplain chart -i meds.txt -o schedule.svg
```

For a plain-text chart you can read in the terminal:

```bash
medsplain chart -i meds.txt --format text
```

Save a chart to a file:

```bash
medsplain chart -i meds.txt --format text -o schedule.txt
```

### What the output looks like

`medsplain summarize` prints something like this:

```
======================================================================
MEDICATION LIST SUMMARY - EDUCATION ONLY, NOT MEDICAL ADVICE
======================================================================

Here is a plain-English summary of your 3 medications:
- Lisinopril; 10 mg; once; morning
- Metformin; 500 mg; twice; breakfast
- Atorvastatin; 20 mg; bedtime

Take each medicine exactly as prescribed by your healthcare provider. If
anything here looks different from what your prescriber or pharmacist told
you, ask them before taking it.

Parsed medications:
  - Lisinopril; 10 mg; once; morning
  - Metformin; 500 mg; twice; breakfast
  - Atorvastatin; 20 mg; bedtime

IMPORTANT: This tool is for education only. It is not medical advice, not a
prescription, and not a substitute for a doctor, pharmacist, or other
qualified healthcare professional. Do not start, stop, or change any
medication based on this output. Always confirm instructions with your
prescriber or pharmacist before making changes.
```

`medsplain chart` arranges your medicines into Morning, Midday, Evening, and
Bedtime columns so you can see at a glance when each one is due.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

## About

Dylan Asdale is a registered nurse turned AI author and founder of Asdale
Dynamics, LLC. His book *The Massive AI Manual* and hub site
dylanasdale.github.io explain AI "like a friend would": plain English, step by
step, never condescending. medsplain is one of the LLC's open-source,
local-first health-education helpers.
