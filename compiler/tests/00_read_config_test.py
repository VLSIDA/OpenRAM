#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2026 Regents of the University of California, Santa Cruz
# All rights reserved.
#
"""Check configuration loading without initializing a technology or simulator."""

import array
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


if __name__ == "__main__":
    openram.parse_args()
    del sys.argv[1:]
    unittest.main()
