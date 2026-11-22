# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
Setup script for the ASAP7 predictive 7nm FinFET PDK (Arizona State University
and ARM, BSD-3-Clause, https://github.com/The-OpenROAD-Project/asap7).

This port is netlist-only. models/ holds the BSIM-CMG models from
asap7_pdk_r1p7 (HSPICE syntax, level 72). The library cells in gds_lib/,
except dff.gds, are abstracts (boundary and pin shapes) that give OpenRAM
cell sizes and pin locations; they are not DRC/LVS-clean layouts.
"""

import os

TECHNOLOGY = "asap7"

os.environ["SPICE_MODEL_DIR"] = "{0}/models".format(os.path.dirname(__file__))

# The Calibre rule decks are not part of OpenRAM, nor of the public
# asap7_pdk_r1p7 repository; they come with the full ASAP7 PDK release.
# Point ASAP7_PDK_HOME at that asap7PDK_r1p7 directory to use them.
PDK_HOME = os.environ.get("ASAP7_PDK_HOME")
if PDK_HOME:
    os.environ["DRCLVS_HOME"] = os.path.join(os.path.abspath(os.path.expanduser(PDK_HOME)), "calibre")
else:
    os.environ["DRCLVS_HOME"] = "{0}/tech".format(os.path.dirname(__file__))
