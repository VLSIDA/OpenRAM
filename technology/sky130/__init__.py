#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

"""
This type of setup script should be placed in the setup_scripts directory in
the trunk
"""

import os

TECHNOLOGY = "sky130"

os.environ["MGC_TMPDIR"] = "/tmp"

###########################
# OpenRAM Paths

# OpenPDK needed for magicrc, tech file and spice models of transistors
if 'PDK_ROOT' in os.environ:
    open_pdks = os.path.join(os.environ['PDK_ROOT'], 'sky130A', 'libs.tech')
else:
    raise SystemError("Unable to find open_pdks tech file. Set PDK_ROOT.")

# The ngspice models work with Xyce too now
spice_model_dir = os.path.join(open_pdks, "ngspice")
sky130_lib_ngspice = os.path.join(open_pdks, "ngspice", "sky130.lib.spice")
if not os.path.exists(sky130_lib_ngspice):
    raise SystemError("Did not find {} under {}".format(sky130_lib_ngspice, open_pdks))
os.environ["SPICE_MODEL_DIR"] = spice_model_dir

open_pdks = os.path.abspath(open_pdks)
sky130_magicrc = os.path.join(open_pdks, 'magic', "sky130A.magicrc")
if not os.path.exists(sky130_magicrc):
    raise SystemError("Did not find {} under {}".format(sky130_magicrc, open_pdks))
os.environ["OPENRAM_MAGICRC"] = sky130_magicrc
sky130_netgenrc = os.path.join(open_pdks, 'netgen', "setup.tcl")
if not os.path.exists(sky130_netgenrc):
    raise SystemError("Did not find {} under {}".format(sky130_netgenrc, open_pdks))
os.environ["OPENRAM_NETGENRC"] = sky130_netgenrc

try:
    DRCLVS_HOME = os.path.abspath(os.environ.get("DRCLVS_HOME"))
except:
    DRCLVS_HOME= "not-found"
os.environ["DRCLVS_HOME"] = DRCLVS_HOME
