#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from asyncio import subprocess
import unittest
from testutils import *
import sys, os, re, shutil
sys.path.append(os.getenv("OPENRAM_HOME"))
import globals
from globals import OPTS
import debug
import getpass


class openram_front_end_test(openram_test):

    def runTest(self):
        OPENRAM_HOME = os.path.abspath(os.environ.get("OPENRAM_HOME"))
        config_file = "{}/tests/configs/config_mem_char_func".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)

        debug.info(1, "Testing commandline functional simulator script memfunc.py with 2-bit, 16 word SRAM.")
        out_file = "testsram"
        out_path = "/tmp/testsram_{0}_{1}_{2}".format(OPTS.tech_name, getpass.getuser(), os.getpid())

        # make sure we start without the files existing
        if os.path.exists(out_path):
            shutil.rmtree(out_path, ignore_errors=True)
        self.assertEqual(os.path.exists(out_path), False)

        try:
            os.makedirs(out_path, 0o0750)
        except OSError as e:
            if e.errno == 17:  # errno.EEXIST
                os.chmod(out_path, 0o0750)

        # copy the 2x16 sram spice file into out_path because memfunc.py expects it there
        sp_src_file = "{0}/tests/golden/sram_2_16_1_{1}.sp".format(OPENRAM_HOME, OPTS.tech_name)
        sp_dst_file = out_path + "/" + OPTS.output_name + ".sp"
        shutil.copy(sp_src_file, sp_dst_file)

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
            exe_name = "{0}/memfunc.py ".format(OPENRAM_HOME)
        else:
            exe_name = "{0}{1}/memfunc.py ".format(OPTS.coverage_exe, OPENRAM_HOME)
        config_name = "{0}/tests/configs/config_mem_char_func.py".format(OPENRAM_HOME)
        period_and_cycles = 10
        cmd = "{0} -n -o {1} -p {2} {3} {4} {5} {5} 2>&1 > {6}/output.log".format(exe_name,
                                                                          out_file,
                                                                          out_path,
                                                                          options,
                                                                          config_name,
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

        globals.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
