import os
import debug
from globals import OPTS,find_exe,get_tool
import lib
import delay
import setup_hold


debug.info(2,"Initializing characterizer...")

spice_exe = ""

if not OPTS.analytical_delay:
    if OPTS.spice_name != "":
        spice_exe=find_exe(OPTS.spice_name)
        if spice_exe=="":
            debug.error("{0} not found. Unable to perform characterization.".format(OPTS.spice_name),1)
    else:
        (choice,spice_exe) = get_tool("spice",["xa", "hspice", "ngspice", "ngspice.exe"])
        OPTS.spice_name = choice

    # set the input dir for spice files if using ngspice 
    if OPTS.spice_name == "ngspice":
        os.environ["NGSPICE_INPUT_DIR"] = "{0}".format(OPTS.openram_temp)
    
    if spice_exe == "":
        debug.error("No recognizable spice version found. Unable to perform characterization.",1)


