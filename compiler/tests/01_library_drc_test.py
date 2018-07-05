#!/usr/bin/env python2.7
"Run a regresion test the library cells for DRC"

import unittest
from testutils import header,openram_test
import sys,os,re
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class library_drc_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        global verify
        import verify

        (gds_dir, gds_files) = setup_files()
        drc_errors = 0
        debug.info(1, "\nPerforming DRC on: " + ", ".join(gds_files))
        for f in gds_files:
            name = re.sub('\.gds$', '', f)
            gds_name = "{0}/{1}".format(gds_dir, f)
            if not os.path.isfile(gds_name):
                drc_errors += 1
                debug.error("Missing GDS file: {}".format(gds_name))
            drc_errors += verify.run_drc(name, gds_name)

        # fails if there are any DRC errors on any cells
        self.assertEqual(drc_errors, 0)
        globals.end_openram()

def setup_files():
    gds_dir = OPTS.openram_tech + "/gds_lib"
    files = os.listdir(gds_dir)
    nametest = re.compile("\.gds$", re.IGNORECASE)
    gds_files = filter(nametest.search, files)
    return (gds_dir, gds_files)


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
