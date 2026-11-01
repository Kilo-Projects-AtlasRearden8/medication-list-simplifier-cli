"""Command line interface for medsplain."""

from __future__ import annotations

import argparse
import sys

from .client import DEFAULT_ENDPOINT, DEFAULT_MODEL, DEFAULT_TIMEOUT, LLMClient
from .formatter import format_chart_svg, format_chart_text, format_summary
from .parser import parse_medication_list


def _read_input(path: str | None) -> str:
    if path:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    return sys.stdin.read()


def _build_subparser_summarize(sub) -> argparse.ArgumentParser:
    parser = sub.add_parser("summarize", help="Summarize a medication list in plain English")
    parser.add_argument("-i", "--input", help="Medication list file (default: stdin)")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="OpenAI-compatible endpoint")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="Request timeout seconds")
    parser.add_argument("-o", "--output", help="Write summary to file instead of printing")
    parser.set_defaults(func=_run_summarize)
    return parser


def _build_subparser_chart(sub) -> argparse.ArgumentParser:
    parser = sub.add_parser("chart", help="Create a printable medication schedule chart")
    parser.add_argument("-i", "--input", help="Medication list file (default: stdin)")
    parser.add_argument("--format", choices=["svg", "text"], default="svg", help="Chart format")
    parser.add_argument("-o", "--output", help="Write chart to file instead of printing")
    parser.set_defaults(func=_run_chart)
    return parser


def _run_summarize(args) -> None:
    text = _read_input(args.input)
    medications = parse_medication_list(text)
    client = LLMClient(endpoint=args.endpoint, model=args.model, timeout=args.timeout)
    response = client.summarize(medications, raw_text=text)
    output = format_summary(medications, response)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(output)
    else:
        print(output)


def _run_chart(args) -> None:
    text = _read_input(args.input)
    medications = parse_medication_list(text)
    if args.format == "svg":
        output = format_chart_svg(medications)
    else:
        output = format_chart_text(medications)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(output)
    else:
        print(output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="medsplain",
        description=(
            "Turn medication lists into plain-English summaries and printable "
            "charts using a local OpenAI-compatible endpoint (default Ollama). "
            "Education only - never medical advice."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)
    _build_subparser_summarize(sub)
    _build_subparser_chart(sub)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # CLI boundary: show a clean message, not a traceback
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0
