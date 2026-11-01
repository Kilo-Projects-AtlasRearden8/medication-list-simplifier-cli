"""Output formatting: plain-English summaries and printable charts."""

from __future__ import annotations

from .disclaimer import BANNER, DISCLAIMER
from .parser import Medication

BUCKET_ORDER = ["Morning", "Midday", "Evening", "Bedtime"]
BUCKET_LABELS = {
    "Morning": "Morning (after waking / with breakfast)",
    "Midday": "Midday (around lunchtime)",
    "Evening": "Evening (with dinner / before bed)",
    "Bedtime": "Bedtime (at night)",
}


def format_summary(medications: list[Medication], response) -> str:
    lines: list[str] = []
    lines.append("=" * 70)
    lines.append(BANNER)
    lines.append("=" * 70)
    lines.append("")
    lines.append(response.text)
    lines.append("")
    lines.append("Parsed medications:")
    if medications:
        for med in medications:
            lines.append(f"  - {med.summary_line()}")
    else:
        lines.append("  (none parsed - paste your list and try again)")
    lines.append("")
    lines.append(DISCLAIMER)
    lines.append("")
    return "\n".join(lines)


def _bucket_for(med: Medication) -> set[str]:
    text = f"{med.raw} {med.time_of_day or ''} {med.frequency or ''}".lower()
    buckets: set[str] = set()
    if "bedtime" in text or "night" in text:
        buckets.add("Bedtime")
    if "morning" in text or "breakfast" in text:
        buckets.add("Morning")
    if "afternoon" in text:
        buckets.add("Midday")
    if "lunch" in text:
        buckets.add("Midday")
    if "evening" in text or "dinner" in text or "supper" in text:
        buckets.add("Evening")
    freq = med.frequency or ""
    if not buckets:
        if "twice" in freq:
            buckets |= {"Morning", "Evening"}
        elif "three times" in freq or "four times" in freq:
            buckets |= {"Morning", "Midday", "Evening"}
        elif "every" in freq:
            buckets |= {"Morning", "Midday", "Evening", "Bedtime"}
        else:
            buckets.add("Morning")
    return buckets


def _fit_cell(text: str, width: int) -> str:
    if len(text) <= width:
        return text
    words = text.split()
    result = ""
    for word in words:
        candidate = (result + " " + word).strip()
        if len(candidate) > width:
            break
        result = candidate
    return result if result else text[:width]


def format_chart_text(medications: list[Medication]) -> str:
    buckets = {name: [] for name in BUCKET_ORDER}
    for med in medications:
        for name in _bucket_for(med):
            buckets[name].append(med)

    width = 34
    lines: list[str] = []
    lines.append("=" * 70)
    lines.append(BANNER)
    lines.append("=" * 70)
    lines.append("")
    lines.append("PRINTABLE MEDICATION SCHEDULE CHART")
    lines.append("")
    header = "".join(name.ljust(width) for name in BUCKET_ORDER)
    lines.append(header)
    for name in BUCKET_ORDER:
        lines.append(f"  {name}: {BUCKET_LABELS[name]}")
    lines.append("-" * len(header))
    max_rows = max(len(v) for v in buckets.values()) if medications else 0
    for i in range(max_rows):
        row = ""
        for name in BUCKET_ORDER:
            med = buckets[name][i] if i < len(buckets[name]) else None
            cell = _fit_cell(med.summary_line(), width) if med else ""
            row += cell.ljust(width)
        lines.append(row)
    lines.append("")
    lines.append("Give each medicine exactly as your prescriber directed.")
    lines.append("If this chart does not match your prescription bottle, ask your pharmacist.")
    lines.append("")
    lines.append(DISCLAIMER)
    lines.append("")
    return "\n".join(lines)


def _svg_escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def format_chart_svg(medications: list[Medication]) -> str:
    buckets = {name: [] for name in BUCKET_ORDER}
    for med in medications:
        for name in _bucket_for(med):
            buckets[name].append(med)

    col_w = 150
    col_x = [60 + i * (col_w + 30) for i in range(len(BUCKET_ORDER))]
    row_h = 34
    header_h = 54
    pad_top = 70
    pad_bottom = 110
    height = pad_top + header_h + max(len(v) for v in buckets.values()) * row_h + pad_bottom
    width = 60 + len(BUCKET_ORDER) * (col_w + 30)

    parts: list[str] = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"')
    parts.append(' viewBox="0 0 ' + str(width) + " " + str(height) + '">')
    parts.append('<rect width="100%" height="100%" fill="white"/>')
    parts.append(
        '<text x="30" y="40" font-family="Helvetica, Arial, sans-serif" font-size="18"'
        ' font-weight="bold" fill="#1a1a1a">' + _svg_escape(BANNER) + "</text>"
    )
    parts.append(
        '<text x="30" y="62" font-family="Helvetica, Arial, sans-serif" font-size="11"'
        ' fill="#555555">Printable schedule chart - give each medicine exactly as prescribed</text>'
    )

    for i, name in enumerate(BUCKET_ORDER):
        x = col_x[i]
        parts.append(
            f'<rect x="{x}" y="pad_top" width="{col_w}" height="{header_h}" '
            'fill="#eef2f7" stroke="#9aa5b1" stroke-width="1" rx="4"/>'.replace("pad_top", str(pad_top))
        )
        parts.append(
            f'<text x="{x + col_w / 2}" y="{pad_top + 24}" font-family="Helvetica, Arial, sans-serif"'
            f' font-size="13" font-weight="bold" fill="#1a1a1a" text-anchor="middle">'
            f"{_svg_escape(BUCKET_LABELS[name])}</text>"
        )
        parts.append(
            f'<text x="{x + col_w / 2}" y="{pad_top + 44}" font-family="Helvetica, Arial, sans-serif"'
            f' font-size="10" fill="#555555" text-anchor="middle">'
            f"{len(buckets[name])} medicine(s)</text>"
        )
        for j, med in enumerate(buckets[name]):
            y = pad_top + header_h + j * row_h + 8
            parts.append(
                f'<rect x="{x + 6}" y="{y - 8}" width="{col_w - 12}" height="22" '
                'fill="#f7f9fc" stroke="#c9d2dc" stroke-width="1" rx="3"/>'
            )
            parts.append(
                f'<text x="{x + col_w / 2}" y="{y + 7}" font-family="Helvetica, Arial, sans-serif"'
                f' font-size="11" fill="#1a1a1a" text-anchor="middle">'
                f"{_svg_escape(med.summary_line())}</text>"
            )

    y = pad_top + header_h + max(len(v) for v in buckets.values()) * row_h + 30
    parts.append(
        f'<text x="30" y="{y}" font-family="Helvetica, Arial, sans-serif" font-size="10"'
        ' fill="#555555">Verify against your prescription bottle and pharmacy label.</text>'
    )
    parts.append(
        f'<text x="30" y="{y + 16}" font-family="Helvetica, Arial, sans-serif" font-size="10"'
        ' fill="#555555">' + _svg_escape(DISCLAIMER) + "</text>"
    )
    parts.append("</svg>")
    return "\n".join(parts)
