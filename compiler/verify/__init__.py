# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
This is a module that will import the correct DRC/LVS/PEX 
module based on what tools are found. It is a layer of indirection
to enable multiple verification tool support.

Each DRC/LVS/PEX tool should implement the functions run_drc, run_lvs, and
run_pex, repsectively. If there is an error, they should abort and report the errors.
If not, OpenRAM will continue as if nothing happened!
"""

import os
import debug
from globals import OPTS,find_exe,get_tool
import sys

debug.info(1,"Initializing verify...")

if not OPTS.check_lvsdrc:
    debug.info(1,"LVS/DRC/PEX disabled.")
    OPTS.drc_exe = None
    OPTS.lvs_exe = None
    OPTS.pex_exe = None
else:
    debug.info(1, "Finding DRC/LVS/PEX tools.")    
    OPTS.drc_exe = get_tool("DRC", ["calibre","assura","magic"], OPTS.drc_name)
    OPTS.lvs_exe = get_tool("LVS", ["calibre","assura","netgen"], OPTS.lvs_name)
    OPTS.pex_exe = get_tool("PEX", ["calibre","magic"], OPTS.pex_name)

if OPTS.drc_exe == None:
    from .none import run_drc,print_drc_stats
elif "calibre"==OPTS.drc_exe[0]:
    from .calibre import run_drc,print_drc_stats
elif "assura"==OPTS.drc_exe[0]:
    from .assura import run_drc,print_drc_stats
elif "magic"==OPTS.drc_exe[0]:
    from .magic import run_drc,print_drc_stats
else:
    debug.warning("Did not find a supported DRC tool.")

if OPTS.lvs_exe == None:
    from .none import run_lvs,print_lvs_stats
elif "calibre"==OPTS.lvs_exe[0]:
    from .calibre import run_lvs,print_lvs_stats
elif "assura"==OPTS.lvs_exe[0]:
    from .assura import run_lvs,print_lvs_stats
elif "netgen"==OPTS.lvs_exe[0]:
    from .magic import run_lvs,print_lvs_stats
else:
    debug.warning("Did not find a supported LVS tool.")


if OPTS.pex_exe == None:
    from .none import run_pex,print_pex_stats
elif "calibre"==OPTS.pex_exe[0]:
    from .calibre import run_pex,print_pex_stats
elif "magic"==OPTS.pex_exe[0]:
    from .magic import run_pex,print_pex_stats
else:
    debug.warning("Did not find a supported PEX tool.")
    
