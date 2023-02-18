# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
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
# Cadence FreePDK45 paths
#PDK_PATH=os.environ.get("FREEPDK45")
#if PDK_PATH==None:
#    debug.error("Must define FREEPDK45 to point to PDK.", -1)
#PDK_DIR=os.path.abspath(os.path.expanduser(PDK_PATH))
#os.environ["PDK_DIR"] = PDK_DIR
#os.environ["SYSTEM_CDS_LIB_DIR"] = "{0}/ncsu_basekit/cdssetup".format(PDK_DIR)
#os.environ["CDS_SITE"] = PDK_DIR
#os.environ["MGC_TMPDIR"] = "/tmp"
#os.environ["SYSTEM_CDS_LIB_DIR"] = "{0}/ncsu_basekit/cdssetup".format(PDK_DIR)

###########################
#OpenRAM Paths

try:
    DRCLVS_HOME = os.path.abspath(os.environ.get("DRCLVS_HOME"))
except:
    DRCLVS_HOME = "{0}/tech".format(os.path.dirname(__file__))

# If you are using Cadence, you should set the DRCLVS_HOME environment variable
# to the FreePDK45 PDK location:
# DRCLVS_HOME= PDK_DIR+"/ncsu_basekit/techfile/calibre"
os.environ["DRCLVS_HOME"] = DRCLVS_HOME

os.environ["SPICE_MODEL_DIR"] = "{0}/models/tran_models".format(os.path.dirname(__file__))
