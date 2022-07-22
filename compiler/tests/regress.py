#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

import re
import unittest
import sys, os
sys.path.append(os.getenv("OPENRAM_HOME"))
import globals
from subunit import ProtocolTestCase, TestProtocolClient
from testtools import ConcurrentTestSuite

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

num_threads = OPTS.num_threads


def partition_unit_tests(suite, num_threads):
    partitions = [list() for x in range(num_threads)]
    for index, test in enumerate(suite):
        partitions[index % num_threads].append(test)
    return partitions


def fork_tests(num_threads):
    results = []
    test_partitions = partition_unit_tests(suite, num_threads)
    suite._tests[:] = []
    
    def do_fork(suite):
        
        for test_partition in test_partitions:
            test_suite = unittest.TestSuite(test_partition)
            test_partition[:] = []
            c2pread, c2pwrite = os.pipe()
            pid = os.fork()
            if pid == 0:
                # PID of 0 is a child
                try:
                    # Open a stream to write to the parent
                    stream = os.fdopen(c2pwrite, 'wb', 0)
                    os.close(c2pread)
                    sys.stdin.close()
                    test_suite_result = TestProtocolClient(stream)
                    test_suite.run(test_suite_result)
                except EBADF:
                    try:
                        stream.write(traceback.format_exc())
                    finally:
                        os._exit(1)
                os._exit(0)
            else:
                # PID >0 is the parent
                # Collect all of the child streams and append to the results
                os.close(c2pwrite)
                stream = os.fdopen(c2pread, 'rb', 0)
                test = ProtocolTestCase(stream)
                results.append(test)
        return results
    return do_fork


# import all of the modules
filenameToModuleName = lambda f: os.path.splitext(f)[0]
moduleNames = map(filenameToModuleName, filtered_tests)
modules = map(__import__, moduleNames)

suite = unittest.TestSuite()
load = unittest.defaultTestLoader.loadTestsFromModule
suite.addTests(map(load, modules))

test_runner = unittest.TextTestRunner(verbosity=2, stream=sys.stderr)
if num_threads == 1:
    final_suite = suite
else:
    final_suite = ConcurrentTestSuite(suite, fork_tests(num_threads))
    
test_result = test_runner.run(final_suite)
    
# import verify
# verify.print_drc_stats()
# verify.print_lvs_stats()
# verify.print_pex_stats()

sys.exit(not test_result.wasSuccessful())
