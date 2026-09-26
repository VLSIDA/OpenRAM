#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""Exercise the real file comparator without a PDK or SPICE simulation."""

import tempfile
import unittest
import sys
from pathlib import Path

import openram
from testutils import openram_test


class approx_diff_test(unittest.TestCase):

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.comparator = openram_test()

    def compare(self, first, second, tolerance=0.001):
        first_file = Path(self.directory.name) / "first.lib"
        second_file = Path(self.directory.name) / "second.lib"
        first_file.write_text(first, encoding="utf-8")
        second_file.write_text(second, encoding="utf-8")
        return self.comparator.isapproxdiff(str(first_file), str(second_file), tolerance)

    def test_same_values(self):
        self.assertTrue(self.compare("value: 1.0\n", "value: 1.0\n"))

    def test_large_numeric_difference(self):
        self.assertFalse(self.compare("value: 1.0\n", "value: 9.0\n"))

    def test_within_tolerance(self):
        self.assertTrue(self.compare("value: 1.0\n", "value: 1.005\n", 0.01))

    def test_outside_tolerance(self):
        self.assertFalse(self.compare("value: 1.0\n", "value: 1.02\n", 0.01))

    def test_different_numeric_counts(self):
        # Removing both signed tokens leaves the same text, so this exercises the length check.
        self.assertFalse(self.compare("values: 1.0+2.0\n", "values: 1.0\n"))

    def test_scientific_notation(self):
        self.assertTrue(self.compare("value: 1.0e-3\n", "value: 1.005e-3\n", 0.01))
        self.assertFalse(self.compare("value: 1.0e-3\n", "value: 9.0e-3\n"))

    def test_nonnumeric_difference(self):
        self.assertFalse(self.compare("width: 1.0\n", "height: 1.0\n"))

    def test_equal_zero_values(self):
        self.assertTrue(self.compare("value: 0.0\n", "value: 0.0\n"))


if __name__ == "__main__":
    # The regression Makefile passes OpenRAM options to every test script.
    openram.parse_args()
    del sys.argv[1:]
    unittest.main()
