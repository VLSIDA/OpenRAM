# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
This is a DRC/LVS/PEX interface file for klayout.

"""

import os
import re
import shutil
from openram import debug
from openram import OPTS
from .run_script import *

# Keep track of statistics
num_drc_runs = 0
num_lvs_runs = 0
num_pex_runs = 0


def write_drc_script(cell_name, gds_name, extract, final_verification, output_path, sp_name=None):
    """
    Write a klayout script to perform DRC and optionally extraction.
    """
    global OPTS

    # DRC:
    # klayout -b -r drc_FreePDK45.lydrc -rd input=sram_8_256_freepdk45.gds -rd topcell=sram_8_256_freepdk45 -rd output=drc_FreePDK45.lyrdb

    # Copy .lydrc file into the output directory
    full_drc_file = OPTS.openram_tech + "tech/{}.lydrc".format(OPTS.tech_name)
    drc_file = os.path.basename(full_drc_file)
    if os.path.exists(full_drc_file):
        shutil.copy(full_drc_file, output_path)
    else:
        debug.warning("Could not locate file: {}".format(full_drc_file))

    # Copy .gds file into the output directory
    if os.path.isabs(gds_name):
        shutil.copy(gds_name, output_path)
        gds_name = os.path.basename(gds_name)

    # Copy .sp file into the output directory
    if sp_name and os.path.isabs(sp_name):
        shutil.copy(sp_name, output_path)
        sp_name = os.path.basename(sp_name)

    # Create an auxiliary script to run calibre with the runset
    run_file = output_path + "run_drc.sh"
    f = open(run_file, "w")
    f.write("#!/bin/sh\n")
    cmd = "{0} -b -r {1} -rd input={2} -rd topcell={3} -rd output={3}.drc.report".format(OPTS.drc_exe[1],
                                                                                         drc_file,
                                                                                         gds_name,
                                                                                         cell_name)

    f.write(cmd)
    f.write("\n")
    f.close()
    os.system("chmod u+x {}".format(run_file))


def run_drc(cell_name, gds_name, sp_name=None, extract=True, final_verification=False):
    """Run DRC check on a cell which is implemented in gds_name."""

    global num_drc_runs
    num_drc_runs += 1

    write_drc_script(cell_name, gds_name, extract, final_verification, OPTS.openram_temp, sp_name=sp_name)

    (outfile, errfile, resultsfile) = run_script(cell_name, "drc")

    # Check the result for these lines in the summary:
    # Total DRC errors found: 0
    # The count is shown in this format:
    # Cell replica_cell_6t has 3 error tiles.
    # Cell tri_gate_array has 8 error tiles.
    # etc.
    try:
        f = open(resultsfile, "r")
    except FileNotFoundError:
        debug.error("Unable to load DRC results file from {}. Is klayout set up?".format(resultsfile), 1)

    results = f.readlines()
    f.close()
    errors=len([x for x in results if "<visited>" in x])

    # always display this summary
    result_str = "DRC Errors {0}\t{1}".format(cell_name, errors)
    if errors > 0:
        debug.warning(result_str)
    else:
        debug.info(1, result_str)

    return errors


def write_lvs_script(cell_name, gds_name, sp_name, final_verification=False, output_path=None):
    """ Write a klayout script to perform LVS. """

    # LVS:
    # klayout -b -rd input=sram_32_2048_freepdk45.gds -rd report=my_report.lyrdb -rd schematic=sram_32_2048_freepdk45.sp -rd target_netlist=sram_32_2048_freepdk45_extracted.cir -r lvs_freepdk45.lvs

    global OPTS

    if not output_path:
        output_path = OPTS.openram_temp

    # Copy .lylvs file into the output directory
    full_lvs_file = OPTS.openram_tech + "tech/{}.lylvs".format(OPTS.tech_name)
    lvs_file = os.path.basename(full_lvs_file)

    if os.path.exists(full_lvs_file):
        shutil.copy(full_lvs_file, output_path)
    else:
        debug.warning("Could not locate file: {}".format(full_lvs_file))

    # Copy .gds file into the output directory
    if os.path.isabs(gds_name):
        shutil.copy(gds_name, output_path)
        gds_name = os.path.basename(gds_name)

    # Copy .sp file into the output directory
    if os.path.isabs(sp_name):
        shutil.copy(sp_name, output_path)
        sp_name = os.path.basename(sp_name)

    run_file = output_path + "/run_lvs.sh"
    f = open(run_file, "w")
    f.write("#!/bin/sh\n")
    if final_verification:
        connect_supplies = ""
    else:
        connect_supplies = "-rd connect_supplies=1"
    cmd = "{0} -b -r {1} -rd input={2} -rd report={4}.lvs.report -rd schematic={3} -rd target_netlist={4}.spice {5}".format(OPTS.lvs_exe[1],
                                                                                                                            lvs_file,
                                                                                                                            gds_name,
                                                                                                                            sp_name,
                                                                                                                            cell_name,
                                                                                                                            connect_supplies)
    f.write(cmd)
    f.write("\n")
    f.close()
    os.system("chmod u+x {}".format(run_file))


def run_lvs(cell_name, gds_name, sp_name, final_verification=False, output_path=None):
    """Run LVS check on a given top-level name which is
    implemented in gds_name and sp_name. Final verification will
    ensure that there are no remaining virtual conections. """

    global num_lvs_runs
    num_lvs_runs += 1

    if not output_path:
        output_path = OPTS.openram_temp

    write_lvs_script(cell_name, gds_name, sp_name, final_verification)

    (outfile, errfile, resultsfile) = run_script(cell_name, "lvs")

    # check the result for these lines in the summary:
    try:
        f = open(outfile, "r")
    except FileNotFoundError:
        debug.error("Unable to load LVS results from {}".format(outfile), 1)

    results = f.readlines()
    f.close()
    # Look for CONGRATULATIONS or ERROR
    congrats = len([x for x in results if "CONGRATULATIONS" in x])
    total_errors = len([x for x in results if "ERROR" in x])

    if total_errors>0:
        debug.error("{0}\tLVS mismatch (results in {1})".format(cell_name, resultsfile))
    elif congrats>0:
        debug.info(1, "{0}\tLVS matches".format(cell_name))
    else:
        debug.info(1, "{0}\tNo LVS result".format(cell_name))
        total_errors += 1

    return total_errors


def run_pex(name, gds_name, sp_name, output=None, final_verification=False, output_path=None):
    """Run pex on a given top-level name which is
       implemented in gds_name and sp_name. """

    debug.error("PEX not implemented", -1)

    global num_pex_runs
    num_pex_runs += 1

    if not output_path:
        output_path = OPTS.openram_temp

    os.chdir(output_path)

    if not output_path:
        output_path = OPTS.openram_temp

    if output == None:
        output = name + ".pex.netlist"

    # check if lvs report has been done
    # if not run drc and lvs
    if not os.path.isfile(name + ".lvs.report"):
        run_drc(name, gds_name)
        run_lvs(name, gds_name, sp_name)

    # # pex_fix did run the pex using a script while dev orignial method
    # # use batch mode.
    # # the dev old code using batch mode does not run and is split into functions
    # pex_runset = write_script_pex_rule(gds_name, name, sp_name, output)

    # errfile = "{0}{1}.pex.err".format(output_path, name)
    # outfile = "{0}{1}.pex.out".format(output_path, name)

    # script_cmd = "{0} 2> {1} 1> {2}".format(pex_runset,
    #                                         errfile,
    #                                         outfile)
    # cmd = script_cmd
    # debug.info(2, cmd)
    # os.system(cmd)

    # # rename technology models
    # pex_nelist = open(output, 'r')
    # s = pex_nelist.read()
    # pex_nelist.close()
    # s = s.replace('pfet', 'p')
    # s = s.replace('nfet', 'n')
    # f = open(output, 'w')
    # f.write(s)
    # f.close()

    # # also check the output file
    # f = open(outfile, "r")
    # results = f.readlines()
    # f.close()
    # out_errors = find_error(results)
    # debug.check(os.path.isfile(output), "Couldn't find PEX extracted output.")

    # correct_port(name, output, sp_name)
    return out_errors


def write_batch_pex_rule(gds_name, name, sp_name, output):
    """
    """
    # write the runset file
    file = OPTS.openram_temp + "pex_runset"
    f = open(file, "w")

    f.close()
    return file


def write_script_pex_rule(gds_name, cell_name, sp_name, output):
    global OPTS
    run_file = OPTS.openram_temp + "run_pex.sh"
    f = open(run_file, "w")
    f.write("#!/bin/sh\n")
    f.write('export OPENRAM_TECH="{}"\n'.format(os.environ['OPENRAM_TECH']))
    f.write('echo "$(date): Starting PEX using Klayout {}"\n'.format(OPTS.drc_exe[1]))

    f.write("retcode=$?\n")
    f.write("mv {0}.spice {1}\n".format(cell_name, output))
    f.write('echo "$(date): Finished PEX using Klayout {}"\n'.format(OPTS.drc_exe[1]))
    f.write("exit $retcode\n")

    f.close()
    os.system("chmod u+x {}".format(run_file))
    return run_file


def print_drc_stats():
    debug.info(1, "DRC runs: {0}".format(num_drc_runs))


def print_lvs_stats():
    debug.info(1, "LVS runs: {0}".format(num_lvs_runs))


def print_pex_stats():
    debug.info(1, "PEX runs: {0}".format(num_pex_runs))
