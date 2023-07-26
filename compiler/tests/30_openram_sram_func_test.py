#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
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


class sram_func_test(openram_test):

    def runTest(self):
        global OPTS
        out_file = "sram_2_16_1_{0}".format(OPTS.tech_name)
        out_path = "{0}/testsram_{1}_{2}_{3}".format(OPTS.openram_temp, OPTS.tech_name, getpass.getuser(), os.getpid())
        OPTS.output_name = out_file
        OPTS.output_path = out_path

        OPENRAM_HOME = os.path.abspath(os.environ.get("OPENRAM_HOME"))
        config_file = "{}/tests/configs/config_mem_char_func".format(OPENRAM_HOME)

        openram.init_openram(config_file, is_unit_test=False)
        sp_file = "{0}/tests/sp_files/{1}.sp".format(OPENRAM_HOME, OPTS.output_name)

        debug.info(1, "Testing commandline functional simulator script sram_char.py with 2-bit, 16 word SRAM.")

        # make sure we start without the files existing
        if os.path.exists(out_path):
            shutil.rmtree(out_path, ignore_errors=True)
        self.assertEqual(os.path.exists(out_path), False)

        try:
            os.makedirs(out_path, 0o0750)
        except OSError as e:
            if e.errno == 17:  # errno.EEXIST
                os.chmod(out_path, 0o0750)

        # specify the same verbosity for the system call
        options = ""
        for i in range(OPTS.verbose_level):
            options += " -v"

        if OPTS.spice_name:
            options += " -s {}".format(OPTS.spice_name)

        if OPTS.tech_name:
            options += " -t {}".format(OPTS.tech_name)

        options += " -j 2"

        # Always perform code coverage
        if OPTS.coverage == 0:
            debug.warning("Failed to find coverage installation. This can be installed with pip3 install coverage")
            exe_name = "{0}/../sram_func.py ".format(OPENRAM_HOME)
        else:
            exe_name = "{0}{1}/../sram_func.py ".format(OPTS.coverage_exe, OPENRAM_HOME)
        config_name = "{0}/tests/configs/config_mem_char_func.py".format(OPENRAM_HOME)
        period_and_cycles = 10
        cmd = "{0} -n -o {1} -p {2} {3} {4} {5} {6} {6} 2>&1 > {7}/output.log".format(exe_name,
                                                                          out_file,
                                                                          out_path,
                                                                          options,
                                                                          config_name,
                                                                          sp_file,
                                                                          period_and_cycles,
                                                                          out_path)
        debug.info(1, cmd)
        os.system(cmd)

        # grep any errors from the output
        output_log = open("{0}/output.log".format(out_path), "r")
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
