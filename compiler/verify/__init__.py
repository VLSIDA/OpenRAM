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
    drc_exe = None
    lvs_exe = None
    pex_exe = None
else:
    drc_exe = get_tool("DRC",["calibre","assura","magic"])
    lvs_exe = get_tool("LVS",["calibre","assura","netgen"])
    pex_exe = get_tool("PEX",["calibre","magic"])


if drc_exe == None:
    pass
elif "calibre" in drc_exe:
    from calibre import run_drc
elif "assura" in drc_exe:
    from assura import run_drc
elif "magic" in drc_exe:
    from magic import run_drc
else:
    debug.warning("Did not find a supported DRC tool.")

if lvs_exe == None:
    pass
elif "calibre" in lvs_exe:
    from calibre import run_lvs
elif "assura" in lvs_exe:
    from assura import run_lvs
elif "netgen" in lvs_exe:
    from magic import run_lvs
else:
    debug.warning("Did not find a supported LVS tool.")


if pex_exe == None:
    pass
elif "calibre" in pex_exe:
    from calibre import run_pex
elif "magic" in pex_exe:
    from magic import run_pex
else:
    debug.warning("Did not find a supported PEX tool.")
    
