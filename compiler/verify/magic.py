# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
This is a DRC/LVS/PEX interface file for magic + netgen.

We include the tech file for SCN4M_SUBM in the tech directory,
that is included in OpenRAM during DRC.
You can use this interactively by appending the magic system path in
your .magicrc file
path sys /Users/mrg/openram/technology/scn3me_subm/tech

We require the version 30 Magic rules which allow via stacking.
We obtained this file from Qflow ( http://opencircuitdesign.com/qflow/index.html )
and include its appropriate license.
"""


import os
import re
import shutil
import debug
from globals import OPTS
from run_script import *

# Keep track of statistics
num_drc_runs = 0
num_lvs_runs = 0
num_pex_runs = 0


def filter_gds(cell_name, input_gds, output_gds):
    """ Run the gds through magic for any layer processing """
    global OPTS

    # Copy .magicrc file into temp dir
    magic_file = OPTS.openram_tech + "tech/.magicrc"
    if os.path.exists(magic_file):
        shutil.copy(magic_file, OPTS.openram_temp)
    else:
        debug.warning("Could not locate .magicrc file: {}".format(magic_file))
    

    run_file = OPTS.openram_temp + "run_filter.sh"
    f = open(run_file, "w")
    f.write("#!/bin/sh\n")
    f.write("{0} -dnull -noconsole << EOF\n".format(OPTS.magic_exe[0]))
    f.write("gds polygon subcell true\n")
    f.write("gds warning default\n")
    f.write("gds read {}\n".format(input_gds))
    f.write("load {}\n".format(cell_name))
    f.write("cellname delete \\(UNNAMED\\)\n")
    #f.write("writeall force\n")
    f.write("select top cell\n")
    f.write("gds write {}\n".format(output_gds))
    f.write("quit -noprompt\n")
    f.write("EOF\n")

    f.close()
    os.system("chmod u+x {}".format(run_file))

    (outfile, errfile, resultsfile) = run_script(cell_name, "filter")

    
def write_magic_script(cell_name, extract=False, final_verification=False):
    """ Write a magic script to perform DRC and optionally extraction. """

    global OPTS

    run_file = OPTS.openram_temp + "run_drc.sh"
    f = open(run_file, "w")
    f.write("#!/bin/sh\n")
    f.write("{} -T ~/woow/SW.2/sky130A/libs.tech/magic/current/sky130A.tech -dnull -noconsole << EOF\n".format(OPTS.drc_exe[1]))
    f.write("gds polygon subcell true\n")
    f.write("gds warning default\n")
    f.write("gds readonly true\n")
    f.write("gds read {}.gds\n".format(cell_name))
    f.write("load {}\n".format(cell_name))
    # Flatten the cell to get rid of DRCs spanning multiple layers
    # (e.g. with routes)
    #f.write("flatten {}_new\n".format(cell_name))
    #f.write("load {}_new\n".format(cell_name))
    #f.write("cellname rename {0}_new {0}\n".format(cell_name))
    #f.write("load {}\n".format(cell_name))
    f.write("cellname delete \\(UNNAMED\\)\n")
    f.write("writeall force\n")
    f.write("select top cell\n")
    f.write("expand\n")
    f.write("drc check\n")
    f.write("drc catchup\n")
    f.write("drc count total\n")
    f.write("drc count\n")
    f.write("port makeall\n")
    if not extract:
        pre = "#"
    else:
        pre = ""
    if final_verification:
        f.write(pre + "extract unique all\n".format(cell_name))
    # Hack to work around unit scales in SkyWater
    if OPTS.tech_name=="sky130":
        f.write(pre + "extract style ngspice(si)\n")
    f.write(pre + "extract\n".format(cell_name))
    # f.write(pre + "ext2spice hierarchy on\n")
    # f.write(pre + "ext2spice scale off\n")
    # lvs exists in 8.2.79, but be backword compatible for now
    # f.write(pre + "ext2spice lvs\n")
    f.write(pre + "ext2spice hierarchy on\n")
    f.write(pre + "ext2spice format ngspice\n")
    f.write(pre + "ext2spice cthresh infinite\n")
    f.write(pre + "ext2spice rthresh infinite\n")
    f.write(pre + "ext2spice renumber off\n")
    f.write(pre + "ext2spice scale off\n")
    f.write(pre + "ext2spice blackbox on\n")
    f.write(pre + "ext2spice subcircuit top auto\n")
    f.write(pre + "ext2spice global off\n")

    # Can choose hspice, ngspice, or spice3,
    # but they all seem compatible enough.
    #f.write(pre + "ext2spice format ngspice\n")
    f.write(pre + "ext2spice {}\n".format(cell_name))
    f.write("quit -noprompt\n")
    f.write("EOF\n")

    f.close()
    os.system("chmod u+x {}".format(run_file))


def write_netgen_script(cell_name):
    """ Write a netgen script to perform LVS. """

    global OPTS

    setup_file = "sky130A_setup.tcl" 
    full_setup_file = "/home/me/open_pdks/sky130/sky130A/libs.tech/netgen/sky130A_setup.tcl"
    if os.path.exists(full_setup_file):
        # Copy setup.tcl file into temp dir
        shutil.copy(full_setup_file, OPTS.openram_temp)
    else:
        setup_file = 'nosetup'

    run_file = OPTS.openram_temp + "run_lvs.sh"
    f = open(run_file, "w")
    f.write("#!/bin/sh\n")
    f.write("{} -noconsole << EOF\n".format(OPTS.lvs_exe[1]))
    f.write("readnet spice {0}.spice\n".format(cell_name))
    f.write("readnet spice {0}.sp\n".format(cell_name))
    f.write("lvs {{{0}.spice {0}}} {{{0}.sp {0}}} {1} {0}.lvs.report\n".format(cell_name, setup_file))
    f.write("quit\n")
    f.write("EOF\n")
    f.close()
    os.system("chmod u+x {}".format(run_file))


def run_drc(cell_name, gds_name, extract=True, final_verification=False):
    """Run DRC check on a cell which is implemented in gds_name."""

    global num_drc_runs
    num_drc_runs += 1

    # Copy file to local dir if it isn't already
    if os.path.dirname(gds_name)!=OPTS.openram_temp.rstrip('/'):
        shutil.copy(gds_name, OPTS.openram_temp)

    # Copy .magicrc file into temp dir
    magic_file = OPTS.openram_tech + "tech/.magicrc"
    if os.path.exists(magic_file):
        shutil.copy(magic_file, OPTS.openram_temp)
    else:
        debug.warning("Could not locate .magicrc file: {}".format(magic_file))

    write_magic_script(cell_name, extract, final_verification)

    (outfile, errfile, resultsfile) = run_script(cell_name, "drc")

    # Check the result for these lines in the summary:
    # Total DRC errors found: 0
    # The count is shown in this format:
    # Cell replica_cell_6t has 3 error tiles.
    # Cell tri_gate_array has 8 error tiles.
    # etc.
    try:
        f = open(outfile, "r")
    except FileNotFoundError:
        debug.error("Unable to load DRC results file from {}. Is magic set up?".format(outfile),1)

    results = f.readlines()
    f.close()
    errors=1
    # those lines should be the last 3
    for line in results:
        if "Total DRC errors found:" in line:
            errors = int(re.split(": ", line)[1])
            break
    else:
        debug.error("Unable to find the total error line in Magic output.",1)


    # always display this summary
    result_str = "DRC Errors {0}\t{1}".format(cell_name, errors)
    if errors > 0:
        for line in results:
            if "error tiles" in line:
                debug.info(1,line.rstrip("\n"))
        debug.warning(result_str)
    else:
        debug.info(1, result_str)

    return errors


def run_lvs(cell_name, gds_name, sp_name, final_verification=False):
    """Run LVS check on a given top-level name which is
    implemented in gds_name and sp_name. Final verification will
    ensure that there are no remaining virtual conections. """

    global num_lvs_runs
    num_lvs_runs += 1

    # Copy file to local dir if it isn't already
    if os.path.dirname(gds_name)!=OPTS.openram_temp.rstrip('/'):
        shutil.copy(gds_name, OPTS.openram_temp)
    if os.path.dirname(sp_name)!=OPTS.openram_temp.rstrip('/'):
        shutil.copy(sp_name, OPTS.openram_temp)

    # Copy .magicrc file into temp dir
    magic_file = OPTS.openram_tech + "tech/.magicrc"
    if os.path.exists(magic_file):
        shutil.copy(magic_file, OPTS.openram_temp)
    else:
        debug.warning("Could not locate .magicrc file: {}".format(magic_file))

    write_netgen_script(cell_name)

    (outfile, errfile, resultsfile) = run_script(cell_name, "lvs")

    total_errors = 0

    # check the result for these lines in the summary:
    try:
        f = open(resultsfile, "r")
    except FileNotFoundError:
        debug.error("Unable to load LVS results from {}".format(resultsfile),1)

    results = f.readlines()
    f.close()
    # Look for the results after the final "Subcircuit summary:"
    # which will be the top-level netlist.
    final_results = []
    for line in reversed(results):
        if "Subcircuit summary:" in line:
            break
        else:
            final_results.insert(0,line)

    # There were property errors in any module.
    test = re.compile("Property errors were found.")
    propertyerrors = list(filter(test.search, results))
    total_errors += len(propertyerrors)

    # Require pins to match?
    # Cell pin lists for pnand2_1.spice and pnand2_1 altered to match.
    # test = re.compile(".*altered to match.")
    # pinerrors = list(filter(test.search, results))
    # if len(pinerrors)>0:
    #     debug.warning("Pins altered to match in {}.".format(cell_name))

    #if len(propertyerrors)>0:
    #    debug.warning("Property errors found, but not checking them.")

    # Netlists do not match.
    test = re.compile("Netlists do not match.")
    incorrect = list(filter(test.search, final_results))
    total_errors += len(incorrect)

    # Netlists match uniquely.
    test = re.compile("match uniquely.")
    correct = list(filter(test.search, final_results))
    # Fail if they don't match. Something went wrong!
    if len(correct) == 0:
        total_errors += 1

    if total_errors>0:
        # Just print out the whole file, it is short.
        for e in results:
            debug.info(1,e.strip("\n"))
        debug.error("{0}\tLVS mismatch (results in {1})".format(cell_name,resultsfile))
    else:
        debug.info(1, "{0}\tLVS matches".format(cell_name))

    return total_errors


def run_pex(name, gds_name, sp_name, output=None, final_verification=False):
    """Run pex on a given top-level name which is
       implemented in gds_name and sp_name. """

    global num_pex_runs
    num_pex_runs += 1
    #debug.warning("PEX using magic not implemented.")
    #return 1
    os.chdir(OPTS.openram_temp)

    from tech import drc
    if output == None:
        output = name + ".pex.netlist"

    # check if lvs report has been done
    # if not run drc and lvs
    if not os.path.isfile(name + ".lvs.report"):
        run_drc(name, gds_name)
        run_lvs(name, gds_name, sp_name)

    # pex_fix did run the pex using a script while dev orignial method
    # use batch mode.
    # the dev old code using batch mode does not run and is split into functions
    #pex_runset = write_batch_pex_rule(gds_name,name,sp_name,output)
    pex_runset = write_script_pex_rule(gds_name,name,output)

    errfile = "{0}{1}.pex.err".format(OPTS.openram_temp, name)
    outfile = "{0}{1}.pex.out".format(OPTS.openram_temp, name)

    # bash mode command from dev branch
    #batch_cmd = "{0} -gui -pex {1}pex_runset -batch 2> {2} 1> {3}".format(OPTS.pex_exe,
    #                                                                OPTS.openram_temp,
    #                                                                errfile,
    #                                                                outfile)
    script_cmd = "{0} 2> {1} 1> {2}".format(pex_runset,
                                            errfile,
                                            outfile)
    cmd = script_cmd
    debug.info(2, cmd)
    os.system(cmd)

    # rename technology models
    pex_nelist = open(output, 'r')
    s = pex_nelist.read()
    pex_nelist.close()
    s = s.replace('pfet','p')
    s = s.replace('nfet','n')
    f = open(output, 'w')
    f.write(s)
    f.close()

    # also check the output file
    f = open(outfile, "r")
    results = f.readlines()
    f.close()
    out_errors = find_error(results)
    debug.check(os.path.isfile(output),"Couldn't find PEX extracted output.")

    correct_port(name,output,sp_name)
    return out_errors

def write_batch_pex_rule(gds_name,name,sp_name,output):
    """
    The dev branch old batch mode runset
    2. magic can perform extraction with the following:
    #!/bin/sh
    rm -f $1.ext
    rm -f $1.spice
    magic -dnull -noconsole << EOF
    tech load sky130 
    #scalegrid 1 2
    gds rescale no
    gds polygon subcell true
    gds warning default
    gds read $1
    extract
    ext2spice scale off
    ext2spice
    quit -noprompt
    EOF
    """
    pex_rules = drc["xrc_rules"]
    pex_runset = {
        'pexRulesFile': pex_rules,
        'pexRunDir': OPTS.openram_temp,
        'pexLayoutPaths': gds_name,
        'pexLayoutPrimary': name,
        #'pexSourcePath' : OPTS.openram_temp+"extracted.sp",
        'pexSourcePath': sp_name,
        'pexSourcePrimary': name,
        'pexReportFile': name + ".lvs.report",
        'pexPexNetlistFile': output,
        'pexPexReportFile': name + ".pex.report",
        'pexMaskDBFile': name + ".maskdb",
        'cmnFDIDEFLayoutPath': name + ".def",
    }

    # write the runset file
    file = OPTS.openram_temp + "pex_runset"
    f = open(file, "w")
    for k in sorted(pex_runset.keys()):
        f.write("*{0}: {1}\n".format(k, pex_runset[k]))
    f.close()
    return file

def write_script_pex_rule(gds_name,cell_name,output):
    global OPTS
    run_file = OPTS.openram_temp + "run_pex.sh"
    f = open(run_file, "w")
    f.write("#!/bin/sh\n")
    f.write("{} -dnull -noconsole << eof\n".format(OPTS.drc_exe[1]))
    f.write("gds polygon subcell true\n")
    f.write("gds warning default\n")
    f.write("gds read {}\n".format(gds_name))
    f.write("load {}\n".format(cell_name))
    f.write("select top cell\n")
    f.write("expand\n")
    f.write("port makeall\n")
    extract = True
    if not extract:
        pre = "#"
    else:
        pre = ""
    f.write(pre+"extract\n".format(cell_name))
    #f.write(pre+"ext2spice hierarchy on\n")
    #f.write(pre+"ext2spice format ngspice\n")
    #f.write(pre+"ext2spice renumber off\n")
    #f.write(pre+"ext2spice scale off\n")
    #f.write(pre+"ext2spice blackbox on\n")
    f.write(pre+"ext2spice subcircuit top on\n")
    #f.write(pre+"ext2spice global off\n")
    f.write(pre+"ext2spice {}\n".format(cell_name))
    f.write("quit -noprompt\n")
    f.write("eof\n")
    f.write("mv {0}.spice {1}\n".format(cell_name,output))

    f.close()
    os.system("chmod u+x {}".format(run_file))
    return run_file

def find_error(results):
    # Errors begin with "ERROR:"
    test = re.compile("ERROR:")
    stdouterrors = list(filter(test.search, results))
    for e in stdouterrors:
        debug.error(e.strip("\n"))
    out_errors = len(stdouterrors)
    return out_errors

def correct_port(name, output_file_name, ref_file_name):
    pex_file = open(output_file_name, "r")
    contents = pex_file.read()
    # locate the start of circuit definition line
    match = re.search(".subckt " + str(name) + ".*", contents)
    match_index_start = match.start()
    pex_file.seek(match_index_start)
    rest_text = pex_file.read()
    # locate the end of circuit definition line
    match = re.search(r'\n', rest_text)
    match_index_end = match.start()
    # store the unchanged part of pex file in memory
    pex_file.seek(0)
    part1 = pex_file.read(match_index_start)
    pex_file.seek(match_index_start + match_index_end)
    part2 = pex_file.read()
    pex_file.close()

    # obtain the correct definition line from the original spice file
    sp_file = open(ref_file_name, "r")
    contents = sp_file.read()
    circuit_title = re.search(".SUBCKT " + str(name) + ".*\n", contents)
    circuit_title = circuit_title.group()
    sp_file.close()

    # write the new pex file with info in the memory
    output_file = open(output_file_name, "w")
    output_file.write(part1)
    output_file.write(circuit_title)
    output_file.write(part2)
    output_file.close()

def print_drc_stats():
    debug.info(1,"DRC runs: {0}".format(num_drc_runs))
def print_lvs_stats():
    debug.info(1,"LVS runs: {0}".format(num_lvs_runs))
def print_pex_stats():
    debug.info(1,"PEX runs: {0}".format(num_pex_runs))
