# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
#!/usr/bin/python
"""
This type of setup script should be placed in the setup_scripts directory in the trunk
"""

import sys
import os

TECHNOLOGY = "gf180mcu"

os.environ["MGC_TMPDIR"] = "/tmp"

###########################
# OpenRAM Paths

# OpenPDK needed for magicrc, tech file and spice models of transistors
if 'PDK_ROOT' in os.environ:
    open_pdks = os.path.join(os.environ['PDK_ROOT'], 'gf180mcuD', 'libs.tech')
else:
    raise SystemError("Unable to find open_pdks tech file. Set PDK_ROOT.")

# The ngspice models work with Xyce too now
spice_model_dir = os.path.join(open_pdks, "ngspice")
gf180_lib_ngspice = os.path.join(open_pdks, "ngspice", "sm141064.ngspice")
if not os.path.exists(gf180_lib_ngspice):
    raise SystemError("Did not find {} under {}".format(gf180_lib_ngspice, open_pdks))
os.environ["SPICE_MODEL_DIR"] = spice_model_dir

open_pdks = os.path.abspath(open_pdks)
gf180_magicrc = os.path.join(open_pdks, 'magic', "gf180mcuD.magicrc")
if not os.path.exists(gf180_magicrc):
    raise SystemError("Did not find {} under {}".format(gf180_magicrc, open_pdks))
os.environ["OPENRAM_MAGICRC"] = gf180_magicrc
gf180_netgenrc = os.path.join(open_pdks, 'netgen', "setup.tcl")
if not os.path.exists(gf180_netgenrc):
    raise SystemError("Did not find {} under {}".format(gf180_netgenrc, open_pdks))
os.environ["OPENRAM_NETGENRC"] = gf180_netgenrc

try:
    DRCLVS_HOME = os.path.abspath(os.environ.get("DRCLVS_HOME"))
except:
    DRCLVS_HOME= "not-found"
os.environ["DRCLVS_HOME"] = DRCLVS_HOME


