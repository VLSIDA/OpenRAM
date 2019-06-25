# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
#!/usr/bin/env python3

import re
import unittest
import sys,os
sys.path.append(os.path.join(sys.path[0],"../../compiler"))
import globals

(OPTS, args) = globals.parse_args()
del sys.argv[1:]

from testutils import header,openram_test
header(__file__, OPTS.tech_name)

# get a list of all files in the tests directory
files = os.listdir(sys.path[0])

# assume any file that ends in "test.py" in it is a regression test
nametest = re.compile("test\.py$", re.IGNORECASE)
tests = list(filter(nametest.search, files))
tests.sort()

# import all of the modules
filenameToModuleName = lambda f: os.path.splitext(f)[0]
moduleNames = map(filenameToModuleName, tests)
modules = map(__import__, moduleNames)
suite = unittest.TestSuite()
load = unittest.defaultTestLoader.loadTestsFromModule
suite.addTests(map(load, modules))

test_runner = unittest.TextTestRunner(verbosity=2,stream=sys.stderr)
test_result = test_runner.run(suite)

import verify
verify.print_drc_stats()
verify.print_lvs_stats()
verify.print_pex_stats()        

sys.exit(not test_result.wasSuccessful())
