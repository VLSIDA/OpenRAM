#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""Selecting outputs must not change which target a CV score measures."""

import importlib
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import openram
from openram import OPTS
from testutils import openram_test, header, debugTestRunner


class regression_cross_validation_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        self.addCleanup(openram.end_openram)

        from openram.characterizer import linear_regression
        regression = importlib.import_module("openram.characterizer.regression_model")
        tech_root = Path(openram.__file__).resolve().parent / "technology"

        # Cross-validation needs only the training table and estimator, not a
        # constructed SRAM or SPICE simulation. Use both shipped datasets.
        for technology in ("freepdk45", "scn4m_subm"):
            data_path = str(tech_root / technology / "sim_data" / "sim_data.csv")
            with patch.object(regression, "data_path", data_path):
                model = linear_regression.__new__(linear_regression)
                reference = model.cross_validation()
                self.assertNotAlmostEqual(reference["rise_delay"],
                                          reference["leakage_power"])
                selections = (["leakage_power"],
                              ["leakage_power", "rise_slew"])
                for outputs in selections:
                    with self.subTest(technology=technology, outputs=outputs):
                        selected = model.cross_validation(outputs)
                        self.assertEqual(list(selected), outputs)
                        for output in outputs:
                            self.assertAlmostEqual(selected[output],
                                                   reference[output], places=12)

                with self.subTest(technology=technology, outputs=[]):
                    self.assertEqual(model.cross_validation([]), {})
                with self.subTest(technology=technology, outputs=["not_an_output"]):
                    with self.assertRaises(ValueError):
                        model.cross_validation(["not_an_output"])


if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
