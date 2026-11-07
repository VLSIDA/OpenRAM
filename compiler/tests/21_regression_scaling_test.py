#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2026 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""Held-out rows must not determine the regression's training scalers."""

import importlib
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import MinMaxScaler

import openram
from openram import OPTS
from testutils import openram_test, header, debugTestRunner


class RecordingRidge(Ridge):
    """Keep the actual fitted inputs without changing Ridge's computation."""

    fits = []

    def fit(self, X, y, sample_weight=None):
        self.fits.append((X.copy(), y.copy()))
        return super().fit(X, y, sample_weight=sample_weight)


class regression_scaling_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        self.addCleanup(openram.end_openram)

        from openram.characterizer import linear_regression
        regression = importlib.import_module("openram.characterizer.regression_model")
        tech_root = Path(openram.__file__).resolve().parent / "technology"
        outputs = ["rise_delay", "leakage_power"]

        for technology in ("freepdk45", "scn4m_subm"):
            path = str(tech_root / technology / "sim_data" / "sim_data.csv")
            names = regression.get_data_names(path)
            data = np.asarray(regression.get_data(path)).T
            features = data[:, :9]
            folds = list(KFold(n_splits=10).split(features))
            model = linear_regression.__new__(linear_regression)
            RecordingRidge.fits = []
            with patch.object(regression, "data_path", path), \
                 patch.object(model, "get_model", return_value=RecordingRidge()):
                actual = model.cross_validation(outputs)

            self.assertEqual(len(RecordingRidge.fits), 20)
            for index, (X, y) in enumerate(RecordingRidge.fits):
                with self.subTest(technology=technology,
                                  output=outputs[index // 10], fold=index % 10):
                    # Every variable seen by this fitted Ridge must span its
                    # own [0, 1] training range. Global extrema in a held-out
                    # row must not shrink the range of the training fold.
                    varying = np.ptp(X, axis=0) > 1e-12
                    np.testing.assert_allclose(X[:, varying].min(axis=0), 0,
                                               atol=1e-12)
                    np.testing.assert_allclose(X[:, varying].max(axis=0), 1,
                                               atol=1e-12)
                    self.assertAlmostEqual(float(y.min()), 0, places=12)
                    self.assertAlmostEqual(float(y.max()), 1, places=12)

            # Independently fit each scaler on the training indices and score
            # inverse-transformed predictions in the original target units.
            for output in outputs:
                target = data[:, names.index(output)]
                expected = []
                for train, test in folds:
                    xs = MinMaxScaler().fit(features[train])
                    ys = MinMaxScaler().fit(target[train, None])
                    fitted = Ridge().fit(xs.transform(features[train]),
                                         ys.transform(target[train, None]).ravel())
                    prediction = fitted.predict(xs.transform(features[test]))
                    prediction = ys.inverse_transform(prediction[:, None]).ravel()
                    expected.append(r2_score(target[test], prediction))
                with self.subTest(technology=technology, output=output,
                                  original_unit_score=True):
                    self.assertAlmostEqual(actual[output], np.mean(expected), places=12)


if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
