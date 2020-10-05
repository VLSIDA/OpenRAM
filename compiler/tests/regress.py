#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

import re
import unittest
import sys, os
sys.path.append(os.getenv("OPENRAM_HOME"))
import globals

(OPTS, args) = globals.parse_args()
del sys.argv[1:]

from testutils import *
header(__file__, OPTS.tech_name)

# get a list of all files in the tests directory
files = os.listdir(sys.path[0])

# load a file with all tests to skip in a given technology
# since tech_name is dynamically loaded, we can't use @skip directives
try:
    skip_file_name = "{0}/tests/skip_tests_{1}.txt".format(os.getenv("OPENRAM_HOME"), OPTS.tech_name)
    skip_file = open(skip_file_name, "r")
    skip_tests = skip_file.read().splitlines()
    for st in skip_tests:
        debug.warning("Skipping: " + st)
except FileNotFoundError:
    skip_tests = []

# assume any file that ends in "test.py" in it is a regression test
nametest = re.compile("test\.py$", re.IGNORECASE)
all_tests = list(filter(nametest.search, files))
filtered_tests = list(filter(lambda i: i not in skip_tests, all_tests))
filtered_tests.sort()

# import all of the modules
filenameToModuleName = lambda f: os.path.splitext(f)[0]
moduleNames = map(filenameToModuleName, filtered_tests)
modules = map(__import__, moduleNames)
suite = unittest.TestSuite()
load = unittest.defaultTestLoader.loadTestsFromModule
suite.addTests(map(load, modules))

test_runner = unittest.TextTestRunner(verbosity=2, stream=sys.stderr)
test_result = test_runner.run(suite)

import verify
verify.print_drc_stats()
verify.print_lvs_stats()
verify.print_pex_stats()

sys.exit(not test_result.wasSuccessful())
