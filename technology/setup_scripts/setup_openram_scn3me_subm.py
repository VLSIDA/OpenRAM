#!/usr/bin/python
"""
This type of setup script should be placed in the setup_scripts directory in the trunk
"""

import sys
import os

TECHNOLOGY = "scn3me_subm"


##########################
# CDK paths?

#os.environ["CDK_DIR"] = CDK_DIR #PDK path
#os.environ["SYSTEM_CDS_LIB_DIR"] = "{0}/cdssetup".format(CDK_DIR) #CDS library path
#os.environ["CDS_SITE"] = CDK_DIR #CDS path
os.environ["MGC_TMPDIR"] = "/tmp" #temp folder path

###########################
#Openram Paths
# DON'T DELETE THIS LINE
DRCLVS_HOME="/mada/software/techfiles/scn3me_subm"
os.environ["DRCLVS_HOME"] = DRCLVS_HOME #DRC and LVS path

##########################
#Paths required for OPENRAM to function
LOCAL = "{0}/..".format(os.path.dirname(__file__)) #OPENRAM Trunk path
sys.path.append("{0}/{1}".format(LOCAL,TECHNOLOGY))
