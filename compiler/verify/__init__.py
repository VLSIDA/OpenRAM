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

debug.info(2,"Initializing verify...")

if not OPTS.check_lvsdrc:
    debug.info(1,"LVS/DRC/PEX disabled.")
    OPTS.drc_exe = None
    OPTS.lvs_exe = None
    OPTS.pex_exe = None
else:
    OPTS.drc_exe = get_tool("DRC",["calibre","assura","magic"])
    OPTS.lvs_exe = get_tool("LVS",["calibre","assura","netgen"])
    OPTS.pex_exe = get_tool("PEX",["calibre","magic"])

if OPTS.check_lvsdrc and OPTS.tech_name == "freepdk45":
    debug.check(OPTS.drc_exe[0]!="magic","Magic does not support FreePDK45 for DRC.")
    
if OPTS.drc_exe == None:
    pass
elif "calibre"==OPTS.drc_exe[0]:
    from calibre import run_drc
elif "assura"==OPTS.drc_exe[0]:
    from assura import run_drc
elif "magic"==OPTS.drc_exe[0]:
    from magic import run_drc
else:
    debug.warning("Did not find a supported DRC tool.")

if OPTS.lvs_exe == None:
    pass
elif "calibre"==OPTS.lvs_exe[0]:
    from calibre import run_lvs
elif "assura"==OPTS.lvs_exe[0]:
    from assura import run_lvs
elif "netgen"==OPTS.lvs_exe[0]:
    from magic import run_lvs
else:
    debug.warning("Did not find a supported LVS tool.")


if OPTS.pex_exe == None:
    pass
elif "calibre"==OPTS.pex_exe[0]:
    from calibre import run_pex
elif "magic"==OPTS.pex_exe[0]:
    from magic import run_pex
else:
    debug.warning("Did not find a supported PEX tool.")
    
