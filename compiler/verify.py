"""
This is a module that will import the correct DRC/LVS/PEX 
module based on what tools are found. It is a layer of indirection
to enable multiple verification tool support.

Each DRC/LVS/PEX tool should implement the functions run_drc, run_lvs, and
run_pex, repsectively. If there is an error, they should abort and report the errors.
If not, OpenRAM will continue as if nothing happened!
"""

import debug
import tech

if tech.drc_version=="calibre":
    from calibre import run_drc
elif tech.drc_version=="magic":
    from magic import run_drc
else:
    debug.warning("Did not find a supported DRC tool.")

if tech.lvs_version=="calibre":
    from calibre import run_lvs
elif tech.lvs_version=="netgen":
    from magic import run_lvs
else:
    debug.warning("Did not find a supported LVS tool.")


if tech.pex_version=="calibre":
    from calibre import run_pex
elif tech.pex_version=="magic":
    from magic import run_pex
else:
    debug.warning("Did not find a supported PEX tool.")
    
