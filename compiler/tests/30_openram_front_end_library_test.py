#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
import sys, os, re
import shutil
import getpass
import unittest
from testutils import *

import openram
from openram import debug
from openram import OPTS


class openram_front_end_library_test(openram_test):

    def runTest(self):
        global OPTS
        # Set output name and path before calling init_openram()
        out_file = "testsram"
        out_path = "/tmp/testsram_{0}_{1}_{2}/".format(OPTS.tech_name, getpass.getuser(), os.getpid())
        OPTS.output_name = out_file
        OPTS.output_path = out_path

        OPENRAM_HOME = os.path.abspath(os.environ.get("OPENRAM_HOME"))
        config_file = "{}/tests/configs/config_front_end".format(os.getenv("OPENRAM_HOME"))
        # FIXME: is_unit_test=True causes error
        openram.init_openram(config_file, is_unit_test=False)

        debug.info(1, "Testing top-level front-end library with 2-bit, 16 word SRAM.")

        # make sure we start without the files existing
        if os.path.exists(out_path):
            shutil.rmtree(out_path, ignore_errors=True)
        self.assertEqual(os.path.exists(out_path), False)

        try:
            os.makedirs(out_path, 0o0750)
        except OSError as e:
            if e.errno == 17:  # errno.EEXIST
                os.chmod(out_path, 0o0750)

        # Update OPTS to match sram_compiler library test
        OPTS.output_name = out_file
        OPTS.output_path = out_path
        OPTS.check_lvsdrc = False
        OPTS.num_threads = 2

        # Create an SRAM using the library
        from openram import sram
        s = sram()
        s.save()

        # assert an error until we actually check a result
        for extension in ["v", "lef", "sp", "gds"]:
            filename = "{0}{1}.{2}".format(out_path, out_file, extension)
            debug.info(1, "Checking for file: " + filename)
            self.assertEqual(os.path.exists(filename), True)

        # Make sure there is any .lib file
        import glob
        files = glob.glob('{0}*.lib'.format(out_path))
        self.assertTrue(len(files)>0)

        # Make sure there is any .html file
        if os.path.exists(out_path):
            datasheets = glob.glob('{0}*html'.format(out_path))
            self.assertTrue(len(datasheets)>0)

        # grep any errors from the output
        output_log = open("{0}{1}.log".format(out_path, out_file), "r")
        output = output_log.read()
        output_log.close()
        self.assertEqual(len(re.findall('ERROR', output)), 0)
        self.assertEqual(len(re.findall('WARNING', output)), 0)

        # now clean up the directory
        if not OPTS.keep_temp:
            if os.path.exists(out_path):
                shutil.rmtree(out_path, ignore_errors=True)
            self.assertEqual(os.path.exists(out_path), False)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
