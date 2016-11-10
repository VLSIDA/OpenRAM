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
OPENRAM_TECH=os.path.abspath(os.environ.get("OPENRAM_TECH"))
DRCLVS_HOME=OPENRAM_TECH+"/scn3me_subm/tech"
os.environ["DRCLVS_HOME"] = DRCLVS_HOME
# You can override the spice model diretory in the environment
try:
    SPICE_MODEL_DIR = os.path.abspath(os.environ.get("SPICE_MODEL_DIR"))
except:
    os.environ["SPICE_MODEL_DIR"] = "/mada/software/techfiles/scn3me_subm"

##########################
# Paths required for OPENRAM to function

LOCAL = "{0}/..".format(os.path.dirname(__file__)) 
sys.path.append("{0}/{1}".format(LOCAL,TECHNOLOGY))
