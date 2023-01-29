# See LICENSE for licensing information.
#
#Copyright (c) 2016-2023 Regents of the University of California and The Board
#of Regents for the Oklahoma Agricultural and Mechanical College
#(acting for and on behalf of Oklahoma State University)
#All rights reserved.
#
#!/usr/bin/python
"""
This type of setup script should be placed in the setup_scripts directory in the trunk
"""

import sys
import os

TECHNOLOGY = "scn3me_subm"


##########################
# CDK paths

# os.environ["CDK_DIR"] = CDK_DIR #PDK path
# os.environ["SYSTEM_CDS_LIB_DIR"] = "{0}/cdssetup".format(CDK_DIR)
# os.environ["CDS_SITE"] = CDK_DIR
os.environ["MGC_TMPDIR"] = "/tmp"

###########################
# OpenRAM Paths


try:
    DRCLVS_HOME = os.path.abspath(os.environ.get("DRCLVS_HOME"))
except:
    OPENRAM_TECH=os.path.abspath(os.environ.get("OPENRAM_TECH"))
    DRCLVS_HOME=OPENRAM_TECH+"/scn3me_subm/tech"
os.environ["DRCLVS_HOME"] = DRCLVS_HOME

os.environ["SPICE_MODEL_DIR"] = "{0}/models".format(os.path.dirname(__file__))

