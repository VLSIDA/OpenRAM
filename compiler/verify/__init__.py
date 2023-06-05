# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
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

from openram import debug
from openram.tech import drc_name
from openram.tech import lvs_name
from openram.tech import pex_name
from openram import OPTS, get_tool

debug.info(1, "Initializing verify...")
if not OPTS.check_lvsdrc:
    debug.info(1, "LVS/DRC/PEX disabled.")
    OPTS.drc_exe = None
    OPTS.lvs_exe = None
    OPTS.pex_exe = None
    # if OPTS.tech_name == "sky130":
    #     OPTS.magic_exe = None
else:
    debug.info(1, "Finding DRC/LVS/PEX tools.")
    OPTS.drc_exe = get_tool("DRC", ["klayout", "magic", "calibre", "assura"], drc_name)
    OPTS.lvs_exe = get_tool("LVS", ["klayout", "netgen", "calibre", "assura"], lvs_name)
    OPTS.pex_exe = get_tool("PEX", ["klayout", "magic", "calibre"], pex_name)
    # if OPTS.tech_name == "sky130":
    #     OPTS.magic_exe = get_tool("GDS", ["magic"])

if not OPTS.drc_exe:
    from .none import run_drc, print_drc_stats, write_drc_script
elif "klayout"==OPTS.drc_exe[0]:
    from .klayout import run_drc, print_drc_stats, write_drc_script
elif "calibre"==OPTS.drc_exe[0]:
    from .calibre import run_drc, print_drc_stats, write_drc_script
elif "assura"==OPTS.drc_exe[0]:
    from .assura import run_drc, print_drc_stats, write_drc_script
elif "magic"==OPTS.drc_exe[0]:
    from .magic import run_drc, print_drc_stats, write_drc_script
else:
    debug.error("Did not find a supported DRC tool."
                + "Disable DRC/LVS with check_lvsdrc=False to ignore.", 2)

if not OPTS.lvs_exe:
    from .none import run_lvs, print_lvs_stats, write_lvs_script
elif "klayout"==OPTS.lvs_exe[0]:
    from .klayout import run_lvs, print_lvs_stats, write_lvs_script
elif "calibre"==OPTS.lvs_exe[0]:
    from .calibre import run_lvs, print_lvs_stats, write_lvs_script
elif "assura"==OPTS.lvs_exe[0]:
    from .assura import run_lvs, print_lvs_stats, write_lvs_script
elif "netgen"==OPTS.lvs_exe[0]:
    from .magic import run_lvs, print_lvs_stats, write_lvs_script
else:
    debug.warning("Did not find a supported LVS tool."
                  + "Disable DRC/LVS with check_lvsdrc=False to ignore.", 2)


if not OPTS.pex_exe:
    from .none import run_pex, print_pex_stats
elif "klayout"==OPTS.pex_exe[0]:
    from .klayout import run_pex, print_pex_stats
elif "calibre"==OPTS.pex_exe[0]:
    from .calibre import run_pex, print_pex_stats
elif "magic"==OPTS.pex_exe[0]:
    from .magic import run_pex, print_pex_stats
else:
    debug.warning("Did not find a supported PEX tool."
                  + "Disable DRC/LVS with check_lvsdrc=False to ignore.", 2)

# if OPTS.tech_name == "sky130":
#     if OPTS.magic_exe and "magic"==OPTS.magic_exe[0]:
#         from .magic import filter_gds
#     else:
#         debug.warning("Did not find Magic.")
