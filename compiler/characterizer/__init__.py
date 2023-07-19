# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os
from openram import debug
from openram import OPTS, find_exe, get_tool
from .lib import *
from .delay import *
from .elmore import *
from .linear_regression import *
from .neural_network import *
from .setup_hold import *
from .functional import *
from .simulation import *
from .measurements import *
from .model_check import *
from .analytical_util import *
from .fake_sram import *

debug.info(1, "Initializing characterizer...")
OPTS.spice_exe = ""

if not OPTS.analytical_delay or OPTS.top_process in ["memfunc", "memchar"]:
    if OPTS.spice_name:
        # Capitalize Xyce
        if OPTS.spice_name == "xyce":
            OPTS.spice_name = "Xyce"
        OPTS.spice_exe=find_exe(OPTS.spice_name)
        if OPTS.spice_exe=="" or OPTS.spice_exe==None:
            debug.error("{0} not found. Unable to perform characterization.".format(OPTS.spice_name), 1)
    else:
        (OPTS.spice_name, OPTS.spice_exe) = get_tool("spice", ["Xyce", "ngspice", "ngspice.exe", "hspice", "xa"])

    if OPTS.spice_name in ["Xyce", "xyce"]:
        (OPTS.mpi_name, OPTS.mpi_exe) = get_tool("mpi", ["mpirun"])
        OPTS.hier_seperator = ":"
    else:
        OPTS.mpi_name = None
        OPTS.mpi_exe = ""

    # set the input dir for spice files if using ngspice
    if OPTS.spice_name == "ngspice":
        os.environ["NGSPICE_INPUT_DIR"] = "{0}".format(OPTS.openram_temp)

    if not OPTS.spice_exe:
        debug.error("No recognizable spice version found. Unable to perform characterization.", 1)
    else:
        debug.info(1, "Finding spice simulator: {} ({})".format(OPTS.spice_name, OPTS.spice_exe))
        if OPTS.mpi_name:
            debug.info(1, "MPI for spice simulator: {} ({})".format(OPTS.mpi_name, OPTS.mpi_exe))
        debug.info(1, "Simulation threads: {}".format(OPTS.num_sim_threads))

else:
    debug.info(1, "Analytical model enabled.")

