"""
Tests for the loans module.

Run with:  python -m unittest discover tests
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import config  # noqa: E402
import fixtures  # noqa: E402


class TestAvailability(unittest.TestCase):

    def test_available_copies(self):
        available = [b["copies"] - b["on_loan"] for b in fixtures.SAMPLE_BOOKS]
        self.assertEqual(available, [19, 18, 0])

    def test_fully_loaned_title_has_none_available(self):
        book = fixtures.SAMPLE_BOOKS[2]
        self.assertEqual(book["copies"] - book["on_loan"], 0)


class TestFines(unittest.TestCase):

    def test_fine_matches_days_overdue(self):
        for loan in fixtures.SAMPLE_OVERDUE:
            expected = round(loan["days"] * config.FINE_PER_DAY, 2)
            self.assertAlmostEqual(expected, loan["days"] * 0.20, places=2)

    def test_no_fine_when_not_overdue(self):
        self.assertEqual(0 * config.FINE_PER_DAY, 0)


if __name__ == "__main__":
    unittest.main()
