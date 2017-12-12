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
gds rescale false
gds polygon subcell true
gds warning default
gds read $1
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
gds rescale false
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
readnet $1.spice
readnet $1.sp
ignore class c
permute transistors
compare hierarchical $1.spice {$1.sp $1}
permute
run converge
EOF

"""


import os
import re
import time
import debug
from globals import OPTS
import subprocess


def run_drc(name, gds_name):
    """Run DRC check on a given top-level name which is
       implemented in gds_name."""

    debug.warning("DRC using magic not implemented.")
    return 1

    # the runset file contains all the options to run drc
    from tech import drc
    drc_rules = drc["drc_rules"]
    drc_runset = {
        'drcRulesFile': drc_rules,
        'drcRunDir': OPTS.openram_temp,
        'drcLayoutPaths': gds_name,
        'drcLayoutPrimary': name,
        'drcLayoutSystem': 'GDSII',
        'drcResultsformat': 'ASCII',
        'drcResultsFile': OPTS.openram_temp + name + ".drc.results",
        'drcSummaryFile': OPTS.openram_temp + name + ".drc.summary",
        'cmnFDILayerMapFile': drc["layer_map"],
        'cmnFDIUseLayerMap': 1
    }

    # write the runset file
    f = open(OPTS.openram_temp + "drc_runset", "w")
    for k in sorted(drc_runset.iterkeys()):
        f.write("*{0}: {1}\n".format(k, drc_runset[k]))
    f.close()

    # run drc
    cwd = os.getcwd()
    os.chdir(OPTS.openram_temp)
    errfile = "{0}{1}.drc.err".format(OPTS.openram_temp, name)
    outfile = "{0}{1}.drc.out".format(OPTS.openram_temp, name)

    cmd = "{0} -gui -drc {1}drc_runset -batch 2> {2} 1> {3}".format(OPTS.drc_exe,
                                                                    OPTS.openram_temp,
                                                                    errfile,
                                                                    outfile)
    debug.info(1, cmd)
    os.system(cmd)
    os.chdir(cwd)

    # check the result for these lines in the summary:
    # TOTAL Original Layer Geometries: 106 (157)
    # TOTAL DRC RuleChecks Executed:   156
    # TOTAL DRC Results Generated:     0 (0)
    try:
        f = open(drc_runset['drcSummaryFile'], "r")
    except:
        debug.error("Unable to retrieve DRC results file. Is magic set up?",1)
    results = f.readlines()
    f.close()
    # those lines should be the last 3
    results = results[-3:]
    geometries = int(re.split("\W+", results[0])[5])
    rulechecks = int(re.split("\W+", results[1])[4])
    errors = int(re.split("\W+", results[2])[5])

    # always display this summary
    if errors > 0:
        debug.error("{0}\tGeometries: {1}\tChecks: {2}\tErrors: {3}".format(name, 
                                                                            geometries,
                                                                            rulechecks,
                                                                            errors))
    else:
        debug.info(1, "{0}\tGeometries: {1}\tChecks: {2}\tErrors: {3}".format(name, 
                                                                              geometries,
                                                                              rulechecks,
                                                                              errors))

    return errors


def run_lvs(name, gds_name, sp_name):
    """Run LVS check on a given top-level name which is
       implemented in gds_name and sp_name. """

    debug.warning("LVS using magic+netgen not implemented.")
    return 1
    
    from tech import drc
    lvs_rules = drc["lvs_rules"]
    lvs_runset = {
        'lvsRulesFile': lvs_rules,
        'lvsRunDir': OPTS.openram_temp,
        'lvsLayoutPaths': gds_name,
        'lvsLayoutPrimary': name,
        'lvsSourcePath': sp_name,
        'lvsSourcePrimary': name,
        'lvsSourceSystem': 'SPICE',
        'lvsSpiceFile': OPTS.openram_temp + "extracted.sp",
        'lvsPowerNames': 'vdd',
        'lvsGroundNames': 'gnd',
        'lvsIncludeSVRFCmds': 1,
        'lvsSVRFCmds': '{VIRTUAL CONNECT NAME VDD? GND? ?}',
        'lvsIgnorePorts': 1,
        'lvsERCDatabase': OPTS.openram_temp + name + ".erc.results",
        'lvsERCSummaryFile': OPTS.openram_temp + name + ".erc.summary",
        'lvsReportFile': OPTS.openram_temp + name + ".lvs.report",
        'lvsMaskDBFile': OPTS.openram_temp + name + ".maskdb",
        'cmnFDILayerMapFile': drc["layer_map"],
        'cmnFDIUseLayerMap': 1,
        'cmnVConnectNames': 'vdd, gnd',
        #'cmnVConnectNamesState' : 'ALL', #connects all nets with the same name
    }

    # write the runset file
    f = open(OPTS.openram_temp + "lvs_runset", "w")
    for k in sorted(lvs_runset.iterkeys()):
        f.write("*%s: %s\n" % (k, lvs_runset[k]))
    f.close()

    # run LVS
    cwd = os.getcwd()
    os.chdir(OPTS.openram_temp)
    errfile = "{0}{1}.lvs.err".format(OPTS.openram_temp, name)
    outfile = "{0}{1}.lvs.out".format(OPTS.openram_temp, name)

    cmd = "{0} -gui -lvs {1}lvs_runset -batch 2> {2} 1> {3}".format(OPTS.lvs_exe,
                                                                    OPTS.openram_temp,
                                                                    errfile,
                                                                    outfile)
    debug.info(1, cmd)
    os.system(cmd)
    os.chdir(cwd)

    # check the result for these lines in the summary:
    f = open(lvs_runset['lvsReportFile'], "r")
    results = f.readlines()
    f.close()

    # NOT COMPARED
    # CORRECT
    # INCORRECT
    test = re.compile("#     CORRECT     #")
    correct = filter(test.search, results)
    test = re.compile("NOT COMPARED")
    notcompared = filter(test.search, results)
    test = re.compile("#     INCORRECT     #")
    incorrect = filter(test.search, results)

    # Errors begin with "Error:"
    test = re.compile("\s+Error:")
    errors = filter(test.search, results)
    for e in errors:
        debug.error(e.strip("\n"))

    summary_errors = len(notcompared) + len(incorrect) + len(errors)

    # also check the extraction summary file
    f = open(lvs_runset['lvsReportFile'] + ".ext", "r")
    results = f.readlines()
    f.close()

    test = re.compile("ERROR:")
    exterrors = filter(test.search, results)
    for e in exterrors:
        debug.error(e.strip("\n"))

    test = re.compile("WARNING:")
    extwarnings = filter(test.search, results)
    for e in extwarnings:
        debug.warning(e.strip("\n"))

    # MRG - 9/26/17 - Change this to exclude warnings because of
    # multiple labels on different pins in column mux.
    ext_errors = len(exterrors)
    ext_warnings = len(extwarnings) 

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

    total_errors = summary_errors + out_errors + ext_errors
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

