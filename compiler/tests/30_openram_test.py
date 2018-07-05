#!/usr/bin/env python2.7
"""
This tests the top-level executable. It checks that it generates the
appropriate files: .lef, .lib, .sp, .gds, .v. It DOES NOT, however,
check that these files are right.
"""

import unittest
from testutils import header,openram_test
import sys,os,re,shutil
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class openram_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        
        debug.info(1, "Testing top-level openram.py with 2-bit, 16 word SRAM.")
        out_file = "testsram"
        # make a temp directory for output
        out_path = "/tmp/testsram_{0}".format(OPTS.tech_name)

        # make sure we start without the files existing
        if os.path.exists(out_path):
            shutil.rmtree(out_path, ignore_errors=True)
        self.assertEqual(os.path.exists(out_path),False)

        try:
            os.makedirs(out_path, 0750)
        except OSError as e:
            if e.errno == 17:  # errno.EEXIST
                os.chmod(out_path, 0750)

        # specify the same verbosity for the system call
        verbosity = ""
        for i in range(OPTS.debug_level):
            verbosity += " -v"

            
        OPENRAM_HOME = os.path.abspath(os.environ.get("OPENRAM_HOME"))

        cmd = "python2.7 {0}/openram.py -n -o {1} -p {2} {3} config_20_{4}.py 2>&1 > {5}/output.log".format(OPENRAM_HOME,
                                                                                                            out_file,
                                                                                                            out_path,
                                                                                                            verbosity,
                                                                                                            OPTS.tech_name,
                                                                                                            out_path)
        debug.info(1, cmd)
        os.system(cmd)
        
        # assert an error until we actually check a resul
        for extension in ["gds", "v", "lef", "sp"]:
            filename = "{0}/{1}.{2}".format(out_path,out_file,extension)
            debug.info(1,"Checking for file: " + filename)
            self.assertEqual(os.path.exists(filename),True)

        # Make sure there is any .lib file
        import glob
        files = glob.glob('{0}/*.lib'.format(out_path))
        self.assertTrue(len(files)>0)

        # grep any errors from the output
        output = open("{0}/output.log".format(out_path),"r").read()
        self.assertEqual(len(re.findall('ERROR',output)),0)
        self.assertEqual(len(re.findall('WARNING',output)),0)

        # now clean up the directory
        if os.path.exists(out_path):
            shutil.rmtree(out_path, ignore_errors=True)
        self.assertEqual(os.path.exists(out_path),False)

        # The default was on, so disable it.
        OPTS.check_lvsdrc=False
        globals.end_openram()
        OPTS.check_lvsdrc=True        

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
