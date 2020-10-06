# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os
import debug
import globals
from globals import OPTS,find_exe,get_tool
from .lib import *
from .delay import *
from .setup_hold import *
from .functional import *
from .simulation import *
from .measurements import *
from .model_check import *

debug.info(1,"Initializing characterizer...")
OPTS.spice_exe = ""

if not OPTS.analytical_delay:
    debug.info(1, "Finding spice simulator.")

    if OPTS.spice_name != "":
        OPTS.spice_exe=find_exe(OPTS.spice_name)
        if OPTS.spice_exe=="" or OPTS.spice_exe==None:
            debug.error("{0} not found. Unable to perform characterization.".format(OPTS.spice_name),1)
    else:
        (OPTS.spice_name,OPTS.spice_exe) = get_tool("spice",["hspice", "ngspice", "ngspice.exe", "xa", "alps"])

    # set the input dir for spice files if using ngspice 
    if OPTS.spice_name == "ngspice":
        os.environ["NGSPICE_INPUT_DIR"] = "{0}".format(OPTS.openram_temp)
    
    if OPTS.spice_exe == "":
        debug.error("No recognizable spice version found. Unable to perform characterization.",1)
else:
    debug.info(1,"Analytical model enabled.")


