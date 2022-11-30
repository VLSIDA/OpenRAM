# See LICENSE for licensing information.
#
# Copyright (c) 2016-2022 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
#!/usr/bin/python
"""
This type of setup script should be placed in the setup_scripts directory in
the trunk
"""

import sys
import os
from openram import debug

TECHNOLOGY = "freepdk45"

##########################
# FreePDK45 paths

PDK_PATH=os.environ.get("FREEPDK45")
if PDK_PATH==None:
    debug.error("Must define FREEPDK45 to point to PDK.", -1)
PDK_DIR=os.path.abspath(PDK_PATH)
os.environ["PDK_DIR"] = PDK_DIR
os.environ["SYSTEM_CDS_LIB_DIR"] = "{0}/ncsu_basekit/cdssetup".format(PDK_DIR)
os.environ["CDS_SITE"] = PDK_DIR
os.environ["MGC_TMPDIR"] = "/tmp"

###########################
#OpenRAM Paths

try:
    DRCLVS_HOME = os.path.abspath(os.environ.get("DRCLVS_HOME"))
except:
    DRCLVS_HOME= PDK_DIR+"/ncsu_basekit/techfile/calibre"
os.environ["DRCLVS_HOME"] = DRCLVS_HOME

# try:
#      SPICE_MODEL_DIR = os.path.abspath(os.environ.get("SPICE_MODEL_DIR"))
# except:
# Always use the one in the PDK dir for FreePDK45
os.environ["SPICE_MODEL_DIR"] = PDK_DIR+"/ncsu_basekit/models/hspice/tran_models"
