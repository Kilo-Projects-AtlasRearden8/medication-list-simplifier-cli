"""Tests for medication list parsing."""

import unittest

from medsplain.parser import Medication, parse_medication, parse_medication_list


class ParseMedicationTests(unittest.TestCase):
    def test_full_line(self):
        med = parse_medication("Lisinopril 10 mg once daily in the morning")
        self.assertIsNotNone(med)
        self.assertEqual(med.name, "Lisinopril")
        self.assertEqual(med.dose, "10 mg")
        self.assertEqual(med.frequency, "once")
        self.assertEqual(med.time_of_day, "morning")
        self.assertEqual(med.raw, "Lisinopril 10 mg once daily in the morning")

    def test_attached_dose_and_bedtime(self):
        med = parse_medication("Atorvastatin 20mg at bedtime")
        self.assertIsNotNone(med)
        self.assertEqual(med.name, "Atorvastatin")
        self.assertEqual(med.dose, "20 mg")
        self.assertIsNone(med.frequency)
        self.assertEqual(med.time_of_day, "bedtime")

    def test_twice_daily_with_meals(self):
        med = parse_medication("Metformin 500mg twice daily with breakfast and dinner")
        self.assertIsNotNone(med)
        self.assertEqual(med.name, "Metformin")
        self.assertEqual(med.dose, "500 mg")
        self.assertEqual(med.frequency, "twice")
        self.assertEqual(med.time_of_day, "breakfast")

    def test_every_n_hours(self):
        med = parse_medication("Acetaminophen 500 mg every 6 hours as needed")
        self.assertIsNotNone(med)
        self.assertEqual(med.name, "Acetaminophen")
        self.assertEqual(med.dose, "500 mg")
        self.assertEqual(med.frequency, "every 6 hours")

    def test_case_insensitive(self):
        med = parse_medication("lisinopril 10 MG ONCE DAILY IN THE MORNING")
        self.assertIsNotNone(med)
        self.assertEqual(med.name, "lisinopril")
        self.assertEqual(med.dose, "10 mg")
        self.assertEqual(med.frequency, "once")
        self.assertEqual(med.time_of_day, "morning")

    def test_comment_lines_skipped(self):
        med = parse_medication("# this is a comment")
        self.assertIsNone(med)

    def test_blank_lines_skipped(self):
        self.assertIsNone(parse_medication(""))
        self.assertIsNone(parse_medication("   "))

    def test_name_only_line(self):
        med = parse_medication("Just Some Medicine")
        self.assertIsNotNone(med)
        self.assertEqual(med.name, "Just Some Medicine")
        self.assertIsNone(med.dose)
        self.assertIsNone(med.frequency)
        self.assertIsNone(med.time_of_day)


class ParseListTests(unittest.TestCase):
    def test_multiple_lines(self):
        text = "\n".join(
            [
                "# My meds",
                "",
                "Lisinopril 10 mg once daily in the morning",
                "Metformin 500mg twice daily with breakfast and dinner",
                "",
                "Atorvastatin 20mg at bedtime",
            ]
        )
        meds = parse_medication_list(text)
        self.assertEqual(len(meds), 3)
        self.assertEqual([m.name for m in meds], ["Lisinopril", "Metformin", "Atorvastatin"])

    def test_empty_input(self):
        self.assertEqual(parse_medication_list(""), [])
        self.assertEqual(parse_medication_list("# only comments\n"), [])


if __name__ == "__main__":
    unittest.main()
