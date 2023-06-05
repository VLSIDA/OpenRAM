# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
This is a DRC/LVS/PEX interface file the case with no DRC/LVS tools.
"""

from openram import debug

# Only print the warning once.
drc_warned = False
lvs_warned = False
pex_warned = False


def write_drc_script(cell_name, gds_name, extract, final_verification=False, output_path=None, sp_name=None):
    debug.error("Cannot write DRC script for unknown tool", -1)


def run_drc(cell_name, gds_name, sp_name, extract=False, final_verification=False, output_path=None):
    global drc_warned
    if not drc_warned:
        debug.error("DRC unable to run.", -1)
        drc_warned=True
    # Since we warned, return a failing test.
    return 1


def write_lvs_script(cell_name, gds_name, sp_name, final_verification=False, output_path=None):
    pass


def run_lvs(cell_name, gds_name, sp_name, final_verification=False, output_path=None):
    global lvs_warned
    if not lvs_warned:
        debug.error("LVS unable to run.", -1)
        lvs_warned=True
    # Since we warned, return a failing test.
    return 1


def run_pex(name, gds_name, sp_name, output=None, final_verification=False, output_path=None):
    global pex_warned
    if not pex_warned:
        debug.error("PEX unable to run.", -1)
        pex_warned=True
    # Since we warned, return a failing test.
    return 1


def print_drc_stats():
    pass


def print_lvs_stats():
    pass


def print_pex_stats():
    pass
