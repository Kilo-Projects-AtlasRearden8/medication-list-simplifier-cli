# medsplain

Plain-English medication list summaries and printable charts, powered by a
configurable OpenAI-compatible endpoint (default: local Ollama).

Built and published by **Asdale Dynamics, LLC** (Indiana) — beginner-friendly
AI education, plain English, step by step, never condescending. See
[dylanasdale.github.io](https://dylanasdale.github.io) and *The Massive AI
Manual* by Dylan Asdale.

## ⚠️ Education only - never medical advice

This tool is for education only. It is **not medical advice**, not a
prescription, and not a substitute for a doctor, pharmacist, or other
qualified healthcare professional. Never start, stop, or change a medication
based on this output. Always confirm instructions with your prescriber or
pharmacist.

## Local-first, no keys

No API keys, no accounts, no cloud required by default. It talks to a local
Ollama server at `http://localhost:11434/v1` (OpenAI-compatible chat
completions). Point `--endpoint` at any OpenAI-compatible server (LLM Studio,
vLLM, etc.) if you prefer. If the endpoint cannot be reached, medsplain still
produces a plain summary from the parsed list so it works fully offline.

## Install

```bash
pip install .
```

or, to keep it isolated:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

## Usage

Save a medication list (one per line):

```
Lisinopril 10 mg once daily in the morning
Metformin 500 mg twice daily with breakfast and dinner
Atorvastatin 20 mg at bedtime
```

### Summarize

```bash
medsplain summarize -i meds.txt
```

With a different endpoint or model:

```bash
medsplain summarize -i meds.txt --endpoint http://localhost:1234/v1 --model mistral
```

Save to a file:

```bash
medsplain summarize -i meds.txt -o summary.txt
```

Read from stdin:

```bash
cat meds.txt | medsplain summarize
```

### Printable chart

```bash
medsplain chart -i meds.txt -o schedule.svg
```

The default chart is SVG (printable, scales cleanly). Use `--format text` for
a plain-text schedule chart.

```bash
medsplain chart -i meds.txt --format text
```

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
