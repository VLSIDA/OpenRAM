# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
This is a DRC/LVS interface for Assura. It implements completely two
functions: run_drc and run_lvs, that perform these functions in batch
mode and will return true/false if the result passes. All of the setup
(the rules, temp dirs, etc.) should be contained in this file.
Replacing with another DRC/LVS tool involves rewriting this code to
work properly. Porting to a new technology in Assura means pointing
the code to the proper DRC and LVS rule files.

LVS Notes:

For some processes the FET models are sub-circuits.  Meaning, the
first letter of their SPICE instantiation begins with 'X' not 'M'.
The former confuses Assura, however, so to get these sub-circuit models
to LVS properly, an empty sub-circuit must be inserted into the
LVS SPICE netlist.  The sub-circuits are pointed to using the
drc["lvs_subcircuits"] variable, and additional options must be
inserted in the runset.
"""

import os
import re
from openram import debug
from openram.verify.run_script import *
from openram import OPTS

# Keep track of statistics
num_drc_runs = 0
num_lvs_runs = 0
num_pex_runs = 0


def write_drc_script(cell_name, gds_name, extract, final_verification, output_path):
    from openram.tech import drc
    drc_rules = drc["drc_rules"]
    drc_runset = output_path + cell_name + ".rsf"
    drc_log_file = "{0}{1}.log".format(OPTS.openram_temp, name)

    # write the runset file
    # the runset file contains all the options to run Assura
    # different processes may require different options
    f = open(drc_runset, "w")
    f.write("avParameters(\n")
    f.write("  ?flagDotShapes t\n")
    f.write("  ?flagMalformed t\n")
    f.write("  ?flagPathNonManhattanSeg all\n")
    f.write("  ?flagPathShortSegments endOnlySmart\n")
    f.write("  ?maintain45 nil\n")
    f.write("  ?combineNearCollinearEdges  nil\n")
    f.write(")\n")
    f.write("\n")
    f.write("avParameters(\n")
    f.write("  ?inputLayout ( \"gds2\" \"{}\" )\n".format(gds_name))
    f.write("  ?cellName \"{}\"\n".format(cell_name))
    f.write("  ?workingDirectory \"{}\"\n".format(output_path))
    f.write("  ?rulesFile \"{}\"\n".format(drc_rules))
    f.write("  ?set ( \"GridCheck\" )\n")
    f.write("  ?avrpt t\n")
    f.write(")\n")
    f.close()

    # run drc
    run_file = output_path + "/run_drc.sh"
    f = open(run_file, "w")
    f.write("#!/bin/sh\n")
    f.write("assura {0} 2> {1} 1> {2}\n".format(drc_runset, drc_log_file, drc_log_file))
    f.close()


def run_drc(name, gds_name, final_verification=False):
    """Run DRC check on a given top-level name which is
       implemented in gds_name."""

    global num_drc_runs
    num_drc_runs += 1

    write_drc_script(name, gds_name, True, final_verification, OPTS.openram_temp)

    (outfile, errfile, resultsfile) = run_script(name, "drc")

    # count and report errors
    errors = 0
    try:
        f = open(OPTS.openram_temp + name +".err", "r")
    except:
        debug.error("Unable to retrieve DRC results file.", 1)
    results = f.readlines()
    f.close()
    for line in results:
        if re.match("Rule No.", line):
            if re.search("# INFO:", line) == None:
                errors = errors + 1
                debug.info(1, line)

    if errors > 0:
        debug.error("Errors: {}".format(errors))

    return errors


def write_lvs_script(cell_name, gds_name, sp_name, final_verification, output_path):

    from openram.tech import drc
    lvs_rules = drc["lvs_rules"]
    lvs_runset = output_path + name + ".rsf"
    # The LVS compare rules must be defined in the tech file for Assura.
    lvs_compare = drc["lvs_compare"]
    # Define the must-connect names for disconnected LVS nets for Assura
    lvs_bindings = drc["lvs_bindings"]
    lvs_log_file = "{0}{1}.log".format(output_path, name)
    # Needed when FET models are sub-circuits
    if "lvs_subcircuits" in drc:
        lvs_sub_file = drc["lvs_subcircuits"]
    else:
        lvs_sub_file = ""

    # write the runset file
    # the runset file contains all the options to run Assura
    # different processes may require different options
    f = open(lvs_runset, "w")
    f.write("avParameters(\n")
    f.write("  ?inputLayout ( \"gds2\" \"{}\" )\n".format(gds_name))
    f.write("  ?cellName \"{}\"\n".format(name))
    f.write("  ?workingDirectory \"{}\"\n".format(output_path))
    f.write("  ?rulesFile \"{}\"\n".format(lvs_rules))
    f.write("  ?autoGrid nil\n")
    f.write("  ?avrpt t\n")
    # The below options vary greatly between processes and cell-types
    f.write("  ?set (\"NO_SUBC_IN_GRLOGIC\")\n")
    f.write(")\n")
    f.write("\n")
    c = open(lvs_compare, "r")
    lines = c.read()
    c.close
    f.write(lines)
    f.write("\n")
    f.write("avCompareRules(\n")
    f.write("  schematic(\n")
    # Needed when FET models are sub-circuits
    if os.path.isfile(lvs_sub_file):
        f.write("    genericDevice(emptySubckt)\n")
        f.write("    netlist( spice \"{}\" )\n".format(lvs_sub_file))
    f.write("    netlist( spice \"{}\" )\n".format(sp_name))
    f.write("  )\n")
    f.write("  layout(\n")
    # Separate gnd shapes are sometimes not connected by metal, so this connects by name
    # The use of this option is not recommended for final DRC
    f.write("    joinNets( root \"gnd\" \"gnd*\" ) \n")
    f.write("  )\n")
    f.write("  bindingFile( \"{}\" )\n".format(lvs_bindings))
    f.write(")\n")
    f.write("\n")
    f.write("avLVS()\n")
    f.close()

    # run drc
    run_file = output_path + "/run_vls.sh"
    f = open(run_file, "w")
    f.write("#!/bin/sh\n")
    f.write("assura {0} 2> {1} 1> {2}\n".format(lvs_runset, lvs_log_file, lvs_log_file))
    f.close()


def run_lvs(name, gds_name, sp_name, final_verification=False):
    """Run LVS check on a given top-level name which is
       implemented in gds_name and sp_name. """

    global num_lvs_runs
    num_lvs_runs += 1

    write_lvs_script(name, gds_name, sp_name, final_verification, OPTS.openram_temp)

    (outfile, errfile, resultsfile) = run_script(name, "drc")

    errors = 0
    try:
        f = open(OPTS.openram_temp + name + ".csm", "r")
    except:
        debug.error("Unable to retrieve LVS results file.", 1)
    results = f.readlines()
    f.close()
    for line in results:
        if re.search("errors", line):
            errors = errors + 1
            debug.info(1, line)
        elif re.search("Schematic and Layout", line):
            debug.info(1, line)

    return errors


def run_pex(name, gds_name, sp_name, output=None, final_verification=False):
    """Run pex on a given top-level name which is
       implemented in gds_name and sp_name. """
    debug.error("PEX extraction not implemented with Assura.", -1)

    global num_pex_runs
    num_pex_runs += 1


def print_drc_stats():
    debug.info(1, "DRC runs: {0}".format(num_drc_runs))


def print_lvs_stats():
    debug.info(1, "LVS runs: {0}".format(num_lvs_runs))


def print_pex_stats():
    debug.info(1, "PEX runs: {0}".format(num_pex_runs))
