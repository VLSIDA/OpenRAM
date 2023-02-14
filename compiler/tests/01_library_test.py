#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import sys, os, re
import unittest
from testutils import *

import openram
from openram import debug
from openram import OPTS


class library_lvs_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        from openram import verify

        (gds_dir, sp_dir, allnames) = setup_files()
        drc_errors = 0
        lvs_errors = 0
        debug.info(1, "Performing LVS on: " + ", ".join(allnames))

        for f in allnames:
            gds_name = "{0}/{1}.gds".format(gds_dir, f)
            sp_name = "{0}/{1}.sp".format(sp_dir, f)
            name = re.sub('\.gds$', '', f)
            if not os.path.isfile(gds_name):
                lvs_errors += 1
                debug.error("Missing GDS file {}".format(gds_name))
            if not os.path.isfile(sp_name):
                lvs_errors += 1
                debug.error("Missing SPICE file {}".format(sp_name))
            drc_errors += verify.run_drc(name, gds_name, sp_name)
            lvs_errors += verify.run_lvs(f, gds_name, sp_name)

        # fail if the error count is not zero
        self.assertEqual(drc_errors + lvs_errors, 0)
        openram.end_openram()


def setup_files():
    gds_dir = OPTS.openram_tech + "/gds_lib"
    sp_dir = OPTS.openram_tech + "/lvs_lib"
    if not os.path.exists(sp_dir):
        sp_dir = OPTS.openram_tech + "/sp_lib"
    files = os.listdir(gds_dir)
    nametest = re.compile("\.gds$", re.IGNORECASE)
    gds_files = list(filter(nametest.search, files))
    files = os.listdir(sp_dir)
    nametest = re.compile("\.sp$", re.IGNORECASE)
    sp_files = filter(nametest.search, files)

    # make a list of all the gds and spice files
    tempnames = gds_files
    tempnames.extend(sp_files)

    # remove the .gds and .sp suffixes
    for i in range(len(tempnames)):
        tempnames[i] = re.sub('\.gds$', '', tempnames[i])
        tempnames[i] = re.sub('\.sp$', '', tempnames[i])

    try:
        from openram.tech import blackbox_cells
        nameset = list(set(tempnames) - set(blackbox_cells))
    except ImportError:
        # remove duplicate base names
        nameset = set(tempnames)

    allnames = list(nameset)

    return (gds_dir, sp_dir, allnames)

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
