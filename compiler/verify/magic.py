"""
This is a DRC/LVS/PEX interface file for magic + netgen. 

This assumes you have the SCMOS magic rules installed. Get these from:
ftp://ftp.mosis.edu/pub/sondeen/magic/new/beta/current.tar.gz
and install them in:
cd /opt/local/lib/magic/sys
tar zxvf current.tar.gz
ln -s 2001a current

1. magic can perform drc with the following:
#!/bin/sh
magic -dnull -noconsole << EOF
tech load SCN3ME_SUBM.30
#scalegrid 1 2
gds rescale no
gds polygon subcell true
gds warning default
gds read $1
load $1
writeall force
drc count
drc why
quit -noprompt
EOF

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

3. netgen can perform LVS with:
#!/bin/sh
netgen -noconsole <<EOF
readnet spice $1.spice
readnet spice $1.sp
ignore class c
equate class {$1.spice nfet} {$2.sp n}
equate class {$1.spice pfet} {$2.sp p}
permute default
compare hierarchical $1.spice {$1.sp $1}
run converge
EOF

"""


import os
import re
import time
import debug
from globals import OPTS
import subprocess

def write_magic_script(cell_name, gds_name, extract=False):
    """ Write a magic script to perform DRC and optionally extraction. """

    global OPTS

    run_file = OPTS.openram_temp + "run_drc.sh"
    f = open(run_file, "w")
    f.write("#!/bin/sh\n")
    f.write("{} -dnull -noconsole << EOF\n".format(OPTS.drc_exe[1]))
    f.write("tech load SCN3ME_SUBM.30\n")
    #gf.write("scalegrid 1 8\n")
    #f.write("gds rescale no\n")
    f.write("gds polygon subcell true\n")
    f.write("gds warning default\n")
    f.write("gds read {}\n".format(gds_name))
    f.write("load {}\n".format(cell_name))
    f.write("writeall force\n")
    f.write("drc check\n")
    f.write("drc catchup\n")
    f.write("drc count total\n")
    f.write("drc count\n")
    if extract:
        f.write("extract all\n")
        f.write("ext2spice hierarchy on\n")        
        f.write("ext2spice scale off\n")
        # Can choose hspice, ngspice, or spice3,
        # but they all seem compatible enough.
        #f.write("ext2spice format ngspice\n")
        f.write("ext2spice\n")
    f.write("quit -noprompt\n")
    f.write("EOF\n")
        
    f.close()
    os.system("chmod u+x {}".format(run_file))

def write_netgen_script(cell_name, sp_name):
    """ Write a netgen script to perform LVS. """

    global OPTS
    # This is a hack to prevent netgen from re-initializing the LVS
    # commands. It will be unnecessary after Tim adds the nosetup option.
    setup_file = OPTS.openram_temp + "setup.tcl"
    f = open(setup_file, "w")
    f.close()

    run_file = OPTS.openram_temp + "run_lvs.sh"
    f = open(run_file, "w")
    f.write("#!/bin/sh\n")
    f.write("{} -noconsole << EOF\n".format(OPTS.lvs_exe[1]))
    f.write("readnet spice {0}.spice\n".format(cell_name))
    f.write("readnet spice {0}\n".format(sp_name))
    # Allow some flexibility in W size because magic will snap to a lambda grid
    # This can also cause disconnects unfortunately!
    # f.write("property {{{0}{1}.spice nfet}} tolerance {{w 0.1}}\n".format(OPTS.openram_temp,
    #                                                                     cell_name))
    # f.write("property {{{0}{1}.spice pfet}} tolerance {{w 0.1}}\n".format(OPTS.openram_temp,
    #                                                                     cell_name))
    f.write("lvs {0}.spice {{{1} {0}}} setup.tcl {0}.lvs.report\n".format(cell_name, sp_name))
    f.write("quit\n")
    f.write("EOF\n")
    f.close()
    os.system("chmod u+x {}".format(run_file))

    setup_file = OPTS.openram_temp + "setup.tcl"
    f = open(setup_file, "w")
    f.write("ignore class c\n")
    f.write("equate class {{nfet {0}.spice}} {{n {1}}}\n".format(cell_name, sp_name))
    f.write("equate class {{pfet {0}.spice}} {{p {1}}}\n".format(cell_name, sp_name))
    # This circuit has symmetries and needs to be flattened to resolve them or the banks won't pass
    # Is there a more elegant way to add this when needed?
    f.write("flatten class {{{0}.spice precharge_array}}\n".format(cell_name))
    f.write("property {{nfet {0}.spice}} remove as ad ps pd\n".format(cell_name))
    f.write("property {{pfet {0}.spice}} remove as ad ps pd\n".format(cell_name))
    f.write("property {{n {0}}} remove as ad ps pd\n".format(sp_name))
    f.write("property {{p {0}}} remove as ad ps pd\n".format(sp_name))
    f.write("permute transistors\n")
    f.write("permute pins n source drain\n")
    f.write("permute pins p source drain\n")
    f.close()
    
    
def run_drc(cell_name, gds_name, extract=False):
    """Run DRC check on a cell which is implemented in gds_name."""

    write_magic_script(cell_name, gds_name, extract)
    
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
    except:
        debug.error("Unable to retrieve DRC results file. Is magic set up?",1)
    results = f.readlines()
    f.close()
    # those lines should be the last 3
    for line in results:
        if "Total DRC errors found:" in line:
            errors = int(re.split(":\W+", line)[1])
            break

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

    run_drc(cell_name, gds_name, extract=True)
    write_netgen_script(cell_name, sp_name)
    
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

    # check the result for these lines in the summary:
    f = open(resultsfile, "r")
    results = f.readlines()
    f.close()


    # Netlists do not match.
    test = re.compile("Netlists do not match.")
    incorrect = filter(test.search, results)
    # There were property errors.
    test = re.compile("Property errors were found.")
    propertyerrors = filter(test.search, results)
    # Require pins to match?
    # Cell pin lists for pnand2_1.spice and pnand2_1 altered to match.
    # test = re.compile(".*altered to match.")
    # pinerrors = filter(test.search, results)
    # if len(pinerrors)>0:
    #     debug.warning("Pins altered to match in {}.".format(cell_name))
    
    total_errors = len(propertyerrors) + len(incorrect)
    # If we want to ignore property errors
    #total_errors = len(incorrect)
    #if len(propertyerrors)>0:
    #    debug.warning("Property errors found, but not checking them.")

    # Netlists match uniquely.
    test = re.compile("Netlists match uniquely.")
    correct = filter(test.search, results)
    # Fail if they don't match. Something went wrong!
    if correct == 0:
        total_errors += 1

    if total_errors>0:
        # Just print out the whole file, it is short.
        for e in results:
            debug.info(1,e.strip("\n"))
        debug.error("LVS mismatch (results in {})".format(resultsfile)) 

    return total_errors


def run_pex(name, gds_name, sp_name, output=None):
    """Run pex on a given top-level name which is
       implemented in gds_name and sp_name. """

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
    stdouterrors = filter(test.search, results)
    for e in stdouterrors:
        debug.error(e.strip("\n"))

    out_errors = len(stdouterrors)

    assert(os.path.isfile(output))
    #correct_port(name, output, sp_name)

    return out_errors

