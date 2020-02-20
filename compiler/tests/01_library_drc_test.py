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
import sys,os,re
#sys.path.append(os.getenv("OPENRAM_HOME"))
import globals
from globals import OPTS
import debug

class library_drc_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)
        import verify

        (gds_dir, allnames) = setup_files()
        drc_errors = 0
        debug.info(1, "\nPerforming DRC on: " + ", ".join(allnames))
        for f in allnames:
            gds_name = "{0}/{1}.gds".format(gds_dir, f)            
            if not os.path.isfile(gds_name):
                drc_errors += 1
                debug.error("Missing GDS file: {}".format(gds_name))
            drc_errors += verify.run_drc(f, gds_name)

        # fails if there are any DRC errors on any cells
        self.assertEqual(drc_errors, 0)
        globals.end_openram()


def setup_files():
    gds_dir = OPTS.openram_tech + "/gds_lib"
    files = os.listdir(gds_dir)
    nametest = re.compile("\.gds$", re.IGNORECASE)
    gds_files = list(filter(nametest.search, files))

    tempnames = gds_files
    
    # remove the .gds and .sp suffixes
    for i in range(len(tempnames)):
        gds_files[i] = re.sub('\.gds$', '', tempnames[i])

    try:
        from tech import blackbox_cells
        nameset = list(set(tempnames) - set(blackbox_cells))
    except ImportError:
        # remove duplicate base names
        nameset = set(tempnames)

    allnames = list(nameset)

    return (gds_dir, allnames)


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())

