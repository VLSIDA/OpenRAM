# See LICENSE for licensing information.
#
#Copyright (c) 2019 Regents of the University of California and The Board
#of Regents for the Oklahoma Agricultural and Mechanical College
#(acting for and on behalf of Oklahoma State University)
#All rights reserved.
#
"""
This is a DRC/LVS/PEX interface file for magic + netgen. 

We include the tech file for SCN3ME_SUBM in the tech directory,
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
import time
import shutil
import debug
from globals import OPTS
import subprocess

# Keep track of statistics
num_drc_runs = 0
num_lvs_runs = 0
num_pex_runs = 0

def write_magic_script(cell_name, extract=False, final_verification=False):
    """ Write a magic script to perform DRC and optionally extraction. """

    global OPTS

    run_file = OPTS.openram_temp + "run_drc.sh"
    f = open(run_file, "w")
    f.write("#!/bin/sh\n")
    f.write("{} -dnull -noconsole << EOF\n".format(OPTS.drc_exe[1]))
    f.write("gds polygon subcell true\n")
    f.write("gds warning default\n")
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
        f.write(pre+"extract unique all\n".format(cell_name))
    f.write(pre+"extract\n".format(cell_name))
    #f.write(pre+"ext2spice hierarchy on\n")        
    #f.write(pre+"ext2spice scale off\n")
    # lvs exists in 8.2.79, but be backword compatible for now
    #f.write(pre+"ext2spice lvs\n")
    f.write(pre+"ext2spice hierarchy on\n")
    f.write(pre+"ext2spice format ngspice\n")
    f.write(pre+"ext2spice cthresh infinite\n")
    f.write(pre+"ext2spice rthresh infinite\n")
    f.write(pre+"ext2spice renumber off\n")
    f.write(pre+"ext2spice scale off\n")
    f.write(pre+"ext2spice blackbox on\n")
    f.write(pre+"ext2spice subcircuit top auto\n")
    f.write(pre+"ext2spice global off\n")
    
    # Can choose hspice, ngspice, or spice3,
    # but they all seem compatible enough.
    #f.write(pre+"ext2spice format ngspice\n")
    f.write(pre+"ext2spice {}\n".format(cell_name))
    f.write("quit -noprompt\n")
    f.write("EOF\n")
        
    f.close()
    os.system("chmod u+x {}".format(run_file))

def write_netgen_script(cell_name):
    """ Write a netgen script to perform LVS. """

    global OPTS

    setup_file = "setup.tcl"
    full_setup_file = OPTS.openram_tech + "mag_lib/" + setup_file
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
    magic_file = OPTS.openram_tech + "mag_lib/.magicrc"
    if os.path.exists(magic_file):
        shutil.copy(magic_file, OPTS.openram_temp)
    else:
        debug.warning("Could not locate .magicrc file: {}".format(magic_file))

    write_magic_script(cell_name, extract, final_verification)
    
    # run drc
    cwd = os.getcwd()
    os.chdir(OPTS.openram_temp)
    errfile = "{0}{1}.drc.err".format(OPTS.openram_temp, cell_name)
    outfile = "{0}{1}.drc.summary".format(OPTS.openram_temp, cell_name)

    cmd = "{0}run_drc.sh 2> {1} 1> {2}".format(OPTS.openram_temp,
                                               errfile,
                                               outfile)
    debug.info(2, cmd)
    os.system(cmd)
    os.chdir(cwd)

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
    if errors > 0:
        for line in results:
            if "error tiles" in line:
                debug.info(1,line.rstrip("\n"))
        debug.error("DRC Errors {0}\t{1}".format(cell_name, errors))
    else:
        debug.info(1, "DRC Errors {0}\t{1}".format(cell_name, errors))

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
    
    write_netgen_script(cell_name)
    
    # run LVS
    cwd = os.getcwd()
    os.chdir(OPTS.openram_temp)
    errfile = "{0}{1}.lvs.err".format(OPTS.openram_temp, cell_name)
    outfile = "{0}{1}.lvs.out".format(OPTS.openram_temp, cell_name)
    resultsfile = "{0}{1}.lvs.report".format(OPTS.openram_temp, cell_name)    

    cmd = "{0}run_lvs.sh lvs 2> {1} 1> {2}".format(OPTS.openram_temp,
                                                   errfile,
                                                   outfile)
    debug.info(2, cmd)
    os.system(cmd)
    os.chdir(cwd)

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
    
    debug.warning("PEX using magic not implemented.")
    return 1

    from tech import drc
    if output == None:
        output = name + ".pex.netlist"

    # check if lvs report has been done
    # if not run drc and lvs
    if not os.path.isfile(name + ".lvs.report"):
        run_drc(name, gds_name)
        run_lvs(name, gds_name, sp_name)

        """
        2. magic can perform extraction with the following:
        #!/bin/sh
        rm -f $1.ext
        rm -f $1.spice
        magic -dnull -noconsole << EOF
        tech load SCN3ME_SUBM.30
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
    f = open(OPTS.openram_temp + "pex_runset", "w")
    for k in sorted(pex_runset.iterkeys()):
        f.write("*{0}: {1}\n".format(k, pex_runset[k]))
    f.close()

    # run pex
    cwd = os.getcwd()
    os.chdir(OPTS.openram_temp)
    errfile = "{0}{1}.pex.err".format(OPTS.openram_temp, name)
    outfile = "{0}{1}.pex.out".format(OPTS.openram_temp, name)

    cmd = "{0} -gui -pex {1}pex_runset -batch 2> {2} 1> {3}".format(OPTS.pex_exe,
                                                                    OPTS.openram_temp,
                                                                    errfile,
                                                                    outfile)
    debug.info(2, cmd)
    os.system(cmd)
    os.chdir(cwd)

    # also check the output file
    f = open(outfile, "r")
    results = f.readlines()
    f.close()

    # Errors begin with "ERROR:"
    test = re.compile("ERROR:")
    stdouterrors = list(filter(test.search, results))
    for e in stdouterrors:
        debug.error(e.strip("\n"))

    out_errors = len(stdouterrors)

    debug.check(os.path.isfile(output),"Couldn't find PEX extracted output.")

    return out_errors

def print_drc_stats():
    debug.info(1,"DRC runs: {0}".format(num_drc_runs))
def print_lvs_stats():
    debug.info(1,"LVS runs: {0}".format(num_lvs_runs))
def print_pex_stats():
    debug.info(1,"PEX runs: {0}".format(num_pex_runs))
