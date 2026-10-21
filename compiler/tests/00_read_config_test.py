#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2026 Regents of the University of California, Santa Cruz
# All rights reserved.
#
"""Check configuration loading without initializing a technology or simulator."""

import array
from contextlib import redirect_stderr
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import openram
from openram import globals, options


class read_config_test(unittest.TestCase):

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.addCleanup(setattr, sys, "path", sys.path[:])
        self.reset_options()

    def reset_options(self):
        replacement = patch.object(globals, "OPTS", options.options())
        replacement.start()
        self.addCleanup(replacement.stop)

    def config(self, name, word_size=8, extra=""):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("word_size = {0}\nnum_words = 16\n".format(word_size) + extra,
                        encoding="utf-8")
        return path

    def test_cached_standard_module(self):
        path = self.config("array.py")
        globals.read_config(str(path))
        self.assertEqual(globals.OPTS.word_size, 8)
        self.assertEqual(globals.OPTS.write_size, 8)
        self.assertIs(sys.modules["array"], array)

    def test_builtin_module_name(self):
        path = self.config("sys.py")
        globals.read_config(str(path))
        self.assertEqual(globals.OPTS.word_size, 8)
        self.assertIs(sys.modules["sys"], sys)

    def test_same_basename_in_different_directories(self):
        first = self.config("first/settings.py", 8)
        second = self.config("second/settings.py", 32)
        globals.read_config(str(first))
        self.assertEqual(globals.OPTS.word_size, 8)
        self.reset_options()
        globals.read_config(str(second))
        self.assertEqual(globals.OPTS.word_size, 32)

    def test_sibling_import_and_file_path(self):
        self.config("sibling/config_values.py", extra="value = 24\n")
        path = self.config("sibling/settings.py", extra=(
            "from config_values import value\nword_size = value\n"
            "source_path = __file__\n"))
        self.addCleanup(sys.modules.pop, "config_values", None)
        globals.read_config(str(path.with_suffix("")))
        self.assertEqual(globals.OPTS.word_size, 24)
        self.assertEqual(globals.OPTS.source_path, str(path))

    def test_repeated_read_uses_cached_configuration(self):
        path = self.config("cached_settings.py", extra="marker = object()\n")
        globals.read_config(str(path))
        marker = globals.OPTS.marker
        path.write_text("raise RuntimeError('configuration was executed twice')\n",
                        encoding="utf-8")
        self.reset_options()
        globals.read_config(str(path))
        self.assertIs(globals.OPTS.marker, marker)

    def test_command_line_options_take_precedence(self):
        path = self.config("precedence.py", extra="tech_name = 'config_tech'\n")
        globals.OPTS.word_size = 64
        globals.OPTS.tech_name = "command_line_tech"
        globals.read_config(str(path))
        self.assertEqual(globals.OPTS.word_size, 64)
        self.assertEqual(globals.OPTS.tech_name, "config_tech")

    def test_missing_file_does_not_import_builtin(self):
        with patch.object(globals.debug, "error", side_effect=AssertionError) as error:
            with self.assertRaises(AssertionError):
                globals.read_config(str(self.root / "sys.py"))
        self.assertIn("Unable to read configuration file", error.call_args.args[0])

    def test_syntax_errors_use_configuration_diagnostic(self):
        cases = [
            ("missing_colon", "if True\n    pass\n", 3),
            ("missing_indentation", "if True:\npass\n", 4),
            ("mixed_indentation", "if True:\n\tword_size = 32\n        num_words = 32\n", 5),
        ]
        for name, source, line in cases:
            with self.subTest(name=name):
                path = self.config(name + ".py", extra=source)
                output = io.StringIO()
                with redirect_stderr(output), self.assertRaises(AssertionError):
                    globals.read_config(str(path))
                self.assertIn("Unable to read configuration file: " + str(path), output.getvalue())
                self.assertIn("{0}, line {1}".format(path.name, line), output.getvalue())

    def test_syntax_error_in_sibling_import_identifies_source(self):
        helper = self.config("syntax_values.py", extra="if True\n    pass\n")
        path = self.config("settings.py", extra="import syntax_values\n")
        self.addCleanup(sys.modules.pop, "syntax_values", None)
        output = io.StringIO()
        with redirect_stderr(output), self.assertRaises(AssertionError):
            globals.read_config(str(path))
        self.assertIn("Unable to read configuration file: " + str(path), output.getvalue())
        self.assertIn(helper.name + ", line 3", output.getvalue())

    def test_configuration_can_be_retried_after_syntax_fix(self):
        path = self.config("retry_settings.py", extra="if True\n    pass\n")
        with redirect_stderr(io.StringIO()), self.assertRaises(AssertionError):
            globals.read_config(str(path))
        self.assertNotIn(str(path), globals._config_modules)
        self.assertNotIn("word_size", globals.OPTS.__dict__)
        self.config("retry_settings.py", word_size=32)
        globals.read_config(str(path))
        self.assertEqual(globals.OPTS.word_size, 32)

    def test_runtime_errors_are_not_reclassified(self):
        path = self.config("runtime_error.py", extra="raise RuntimeError('configuration calculation failed')\n")
        with self.assertRaisesRegex(RuntimeError, "configuration calculation failed"):
            globals.read_config(str(path))


if __name__ == "__main__":
    openram.parse_args()
    del sys.argv[1:]
    unittest.main()
