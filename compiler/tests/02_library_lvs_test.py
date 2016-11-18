#!/usr/bin/env python2.7
"Run a regresion test the library cells for LVS"

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre
import re

OPTS = globals.OPTS

#@unittest.skip("SKIPPING 02_lvs_test")


class library_lvs_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))

        (gds_dir, sp_dir, allnames) = setup_files()
        lvs_errors = 0
        debug.info(1, "Performing LVS on: " + ", ".join(allnames))

        for f in allnames:
            gds_name = "{0}/{1}.gds".format(gds_dir, f)
            sp_name = "{0}/{1}.sp".format(sp_dir, f)
            if not os.path.isfile(gds_name):
                lvs_errors += 1
                debug.error("Missing GDS file {}".format(gds_name))
            if not os.path.isfile(sp_name):
                lvs_errors += 1
                debug.error("Missing SPICE file {}".format(gds_name))
            lvs_errors += calibre.run_lvs(f, gds_name, sp_name)

        # fail if the error count is not zero
        self.assertEqual(lvs_errors, 0)
        globals.end_openram()

def setup_files():
    gds_dir = OPTS.openram_tech + "/gds_lib"
    sp_dir = OPTS.openram_tech + "/sp_lib"
    files = os.listdir(gds_dir)
    nametest = re.compile("\.gds$", re.IGNORECASE)
    gds_files = filter(nametest.search, files)
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

    # remove duplicate base names
    nameset = set(tempnames)
    allnames = list(nameset)

    return (gds_dir, sp_dir, allnames)

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
