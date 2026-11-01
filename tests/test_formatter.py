"""Tests for output formatting."""

import unittest

from medsplain.disclaimer import DISCLAIMER
from medsplain.formatter import (
    BUCKET_ORDER,
    format_chart_svg,
    format_chart_text,
    format_summary,
    _fit_cell,
    _bucket_for,
)
from medsplain.parser import Medication


MEDS = [
    Medication("Lisinopril", "10 mg", "once", "morning", "Lisinopril 10 mg once daily in the morning"),
    Medication("Metformin", "500 mg", "twice", "breakfast", "Metformin 500 mg twice daily with breakfast and dinner"),
    Medication("Atorvastatin", "20 mg", None, "bedtime", "Atorvastatin 20 mg at bedtime"),
]


class FakeResponse:
    def __init__(self, text, source="llm"):
        self.text = text
        self.source = source


class FitCellTests(unittest.TestCase):
    def test_short_text_unchanged(self):
        self.assertEqual(_fit_cell("Lisinopril", 20), "Lisinopril")

    def test_truncates_at_word_boundary(self):
        result = _fit_cell("Lisinopril 10 mg once", 20)
        self.assertEqual(result, "Lisinopril 10 mg")
        self.assertTrue(len(result) <= 20)

    def test_empty_result_falls_back_to_hard_slice(self):
        result = _fit_cell("Supercalifragilisticexpialidocious", 10)
        self.assertEqual(result, "Supercalif")


class BucketTests(unittest.TestCase):
    def test_morning_breakfast(self):
        med = Medication("A", "10 mg", "once", "breakfast", "A 10 mg at breakfast")
        self.assertIn("Morning", _bucket_for(med))

    def test_dinner_evening(self):
        med = Medication("A", "10 mg", "once", "dinner", "A 10 mg at dinner")
        self.assertIn("Evening", _bucket_for(med))

    def test_bedtime_night(self):
        med = Medication("A", "10 mg", "once", "night", "A 10 mg at night")
        self.assertIn("Bedtime", _bucket_for(med))

    def test_twice_daily_defaults(self):
        med = Medication("A", "10 mg", "twice", None, "A 10 mg twice daily")
        self.assertEqual(_bucket_for(med), {"Morning", "Evening"})


class SummaryFormatTests(unittest.TestCase):
    def test_includes_llm_text_and_disclaimer(self):
        out = format_summary(MEDS, FakeResponse("Take your meds.", "llm"))
        self.assertIn("Take your meds.", out)
        self.assertIn(DISCLAIMER, out)
        self.assertIn("EDUCATION ONLY", out)

    def test_includes_fallback_text_and_disclaimer(self):
        out = format_summary(MEDS, FakeResponse("Fallback summary.", "fallback"))
        self.assertIn("Fallback summary.", out)
        self.assertIn(DISCLAIMER, out)

    def test_lists_parsed_medications(self):
        out = format_summary(MEDS, FakeResponse("Summary text."))
        for med in MEDS:
            self.assertIn(med.summary_line(), out)


class ChartTextTests(unittest.TestCase):
    def test_includes_banner_and_disclaimer(self):
        out = format_chart_text(MEDS)
        self.assertIn("EDUCATION ONLY", out)
        self.assertIn(DISCLAIMER, out)
        self.assertIn("PRINTABLE MEDICATION SCHEDULE CHART", out)
        for name in BUCKET_ORDER:
            self.assertIn(name, out)

    def test_places_meds_in_correct_buckets(self):
        out = format_chart_text(MEDS)
        self.assertIn("Lisinopril; 10 mg; once; morning", out)
        self.assertIn("Atorvastatin; 20 mg; bedtime", out)


class ChartSVGTests(unittest.TestCase):
    def test_valid_svg_structure(self):
        out = format_chart_svg(MEDS)
        self.assertTrue(out.startswith("<svg"))
        self.assertTrue(out.endswith("</svg>"))
        self.assertIn('xmlns="http://www.w3.org/2000/svg"', out)
        self.assertIn("EDUCATION ONLY", out)
        self.assertIn(DISCLAIMER, out)
        for med in MEDS:
            self.assertIn(med.summary_line(), out)


if __name__ == "__main__":
    unittest.main()
