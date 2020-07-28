# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California
# All rights reserved.
#
#!/usr/bin/python
"""
This type of setup script should be placed in the setup_scripts directory in
the trunk
"""

import sys
import os

TECHNOLOGY = "sky130"

##########################
# S8 Paths

PDK_DIR=os.path.abspath(os.environ.get("SW_PDK_ROOT"))
os.environ["MGC_TMPDIR"] = "/tmp" 

###########################
#OpenRAM Paths

try:
    DRCLVS_HOME = os.path.abspath(os.environ.get("DRCLVS_HOME"))
except:
    DRCLVS_HOME= PDK_DIR+"/ncsu_basekit/techfile/calibre"
os.environ["DRCLVS_HOME"] = DRCLVS_HOME

#try to load explicit spice model environment variable
try:
    SPICE_MODEL_DIR = os.path.abspath(os.environ.get("SW_SPICE_MODEL"))
except:
    #otherwise try to guess based on set S8 pdk install directory
    try:
        SPICE_MODEL_DIR = os.path.abspath(os.environ.get("SW_PDK_ROOT"))+"/sky130A/libs.ref"
    #default to S8 defauly install directory
    except:
        SPICE_MODEL_DIR = os.path.abspath(os.environ.get("HOME"))+"/projects/foundry/skywater-pdk/miscellaneous/s8_spice_models"
os.environ["SPICE_MODEL_DIR"] = SPICE_MODEL_DIR
