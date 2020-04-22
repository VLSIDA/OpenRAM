#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import unittest
from testutils import *
import sys,os,re,shutil
sys.path.append(os.getenv("OPENRAM_HOME"))
import globals
from globals import OPTS
from sram_factory import factory
import debug
import getpass

class openram_back_end_test(openram_test):

    def runTest(self):
        OPENRAM_HOME = os.path.abspath(os.environ.get("OPENRAM_HOME"))
        config_file = "{}/tests/configs/config_back_end".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)

        debug.info(1, "Testing top-level back-end openram.py with 2-bit, 16 word SRAM.")
        out_file = "testsram"
        out_path = "/tmp/testsram_{0}_{1}_{2}/".format(OPTS.tech_name,getpass.getuser(),os.getpid())

        # make sure we start without the files existing
        if os.path.exists(out_path):
            shutil.rmtree(out_path, ignore_errors=True)
        self.assertEqual(os.path.exists(out_path),False)

        try:
            os.makedirs(out_path, 0o0750)
        except OSError as e:
            if e.errno == 17:  # errno.EEXIST
                os.chmod(out_path, 0o0750)

        # specify the same verbosity for the system call
        options = ""
        for i in range(OPTS.debug_level):
            options += " -v"

        if OPTS.spice_name:
            options += " -s {}".format(OPTS.spice_name)
            
        # Always perform code coverage
        if OPTS.coverage == 0:
            debug.warning("Failed to find coverage installation. This can be installed with pip3 install coverage")
            exe_name = "{0}/openram.py ".format(OPENRAM_HOME)
        else:
            exe_name = "coverage run -p {0}/openram.py ".format(OPENRAM_HOME)
        config_name = "{0}/tests/configs/config_back_end.py".format(OPENRAM_HOME)
        cmd = "{0} -n -o {1} -p {2} {3} {4} 2>&1 > {5}/output.log".format(exe_name,
                                                                          out_file,
                                                                          out_path,
                                                                          options,
                                                                          config_name,
                                                                          out_path)
        debug.info(1, cmd)
        os.system(cmd)
        
        # assert an error until we actually check a resul
        for extension in ["gds", "v", "lef", "sp"]:
            filename = "{0}/{1}.{2}".format(out_path, out_file, extension)
            debug.info(1, "Checking for file: " + filename)
            self.assertEqual(os.path.exists(filename), True)

        # Make sure there is any .lib file
        import glob
        files = glob.glob('{0}/*.lib'.format(out_path))
        self.assertTrue(len(files)>0)
        
        # Make sure there is any .html file
        if os.path.exists(out_path):
            datasheets = glob.glob('{0}/*html'.format(out_path))
            self.assertTrue(len(datasheets)>0)
        
        # grep any errors from the output
        output_log = open("{0}/output.log".format(out_path), "r")
        output = output_log.read()
        output_log.close()
        self.assertEqual(len(re.findall('ERROR', output)), 0)
        self.assertEqual(len(re.findall('WARNING', output)), 0)

        # now clean up the directory
        if OPTS.purge_temp:
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
