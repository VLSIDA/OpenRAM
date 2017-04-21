"""
This is a DRC/LVS interface for calibre. It implements completely
independently two functions: run_drc and run_lvs, that perform these
functions in batch mode and will return true/false if the result
passes. All of the setup (the rules, temp dirs, etc.) should be
contained in this file.  Replacing with another DRC/LVS tool involves
rewriting this code to work properly. Porting to a new technology in
Calibre means pointing the code to the proper DRC and LVS rule files.

A calibre DRC runset file contains, at the minimum, the following information:

*drcRulesFile: /mada/software/techfiles/FreePDK45/ncsu_basekit/techfile/calibre/calibreDRC.rul
*drcRunDir: .
*drcLayoutPaths: ./cell_6t.gds
*drcLayoutPrimary: cell_6t
*drcLayoutSystem: GDSII
*drcResultsformat: ASCII
*drcResultsFile: cell_6t.drc.db
*drcSummaryFile: cell_6t.drc.summary
*cmnFDILayerMapFile: ./layer.map
*cmnFDIUseLayerMap: 1

This can be executed in "batch" mode with the following command:

calibre -gui -drc example_drc_runset  -batch

To open the results, you can do this:

calibredrv cell_6t.gds
Select Verification->Start RVE.
Select the cell_6t.drc.db file.
Click on the errors and they will highlight in the design layout viewer.

For LVS:

*lvsRulesFile: /mada/software/techfiles/FreePDK45/ncsu_basekit/techfile/calibre/calibreLVS.rul
*lvsRunDir: .
*lvsLayoutPaths: ./cell_6t.gds
*lvsLayoutPrimary: cell_6t
*lvsSourcePath: ./cell_6t.sp
*lvsSourcePrimary: cell_6t
*lvsSourceSystem: SPICE
*lvsSpiceFile: extracted.sp
*lvsPowerNames: vdd 
*lvsGroundNames: vss
*lvsIgnorePorts: 1
*lvsERCDatabase: cell_6t.erc.db
*lvsERCSummaryFile: cell_6t.erc.summary
*lvsReportFile: cell_6t.lvs.report
*lvsMaskDBFile: cell_6t.maskdb
*cmnFDILayerMapFile: ./layer.map
*cmnFDIUseLayerMap: 1

To run and see results:

calibre -gui -lvs example_lvs_runset -batch
more cell_6t.lvs.report
"""


import os
import re
import time
import debug
import globals
import subprocess


def run_drc(name, gds_name):
    """Run DRC check on a given top-level name which is
       implemented in gds_name."""
    OPTS = globals.get_opts()

    # the runset file contains all the options to run calibre
    from tech import drc
    drc_rules = drc["drc_rules"]

    drc_runset = {
        'drcRulesFile': drc_rules,
        'drcRunDir': OPTS.openram_temp,
        'drcLayoutPaths': gds_name,
        'drcLayoutPrimary': name,
        'drcLayoutSystem': 'GDSII',
        'drcResultsformat': 'ASCII',
        'drcResultsFile': OPTS.openram_temp + name + ".drc.db",
        'drcSummaryFile': OPTS.openram_temp + name + ".drc.summary",
        'cmnFDILayerMapFile': drc["layer_map"],
        'cmnFDIUseLayerMap': 1
    }

    # write the runset file
    f = open(OPTS.openram_temp + "drc_runset", "w")
    for k in sorted(drc_runset.iterkeys()):
        f.write("*%s: %s\n" % (k, drc_runset[k]))
    f.close()

    # run drc
    cwd = os.getcwd()
    os.chdir(OPTS.openram_temp)
    errfile = "%s%s.drc.err" % (OPTS.openram_temp, name)
    outfile = "%s%s.drc.out" % (OPTS.openram_temp, name)

    cmd = "{0} -gui -drc {1}drc_runset -batch 2> {2} 1> {3}".format(
        OPTS.calibre_exe, OPTS.openram_temp, errfile, outfile)
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
        debug.error("Unable to retrieve DRC results file. Is calibre set up?",1)
    results = f.readlines()
    f.close()
    # those lines should be the last 3
    results = results[-3:]
    geometries = int(re.split("\W+", results[0])[5])
    rulechecks = int(re.split("\W+", results[1])[4])
    errors = int(re.split("\W+", results[2])[5])

    # always display this summary
    if errors > 0:
        debug.error("%-25s\tGeometries: %d\tChecks: %d\tErrors: %d" %
                    (name, geometries, rulechecks, errors))
    else:
        debug.info(1, "%-25s\tGeometries: %d\tChecks: %d\tErrors: %d" %
                   (name, geometries, rulechecks, errors))

    return errors


def run_lvs(name, gds_name, sp_name):
    """Run LVS check on a given top-level name which is
       implemented in gds_name and sp_name. """
    OPTS = globals.get_opts()
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
        'lvsERCDatabase': OPTS.openram_temp + name + ".erc.db",
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
    errfile = "%s%s.lvs.err" % (OPTS.openram_temp, name)
    outfile = "%s%s.lvs.out" % (OPTS.openram_temp, name)

    cmd = "calibre -gui -lvs %slvs_runset -batch 2> %s 1> %s" % (
        OPTS.openram_temp, errfile, outfile)
    debug.info(2, cmd)
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
        debug.error(e.strip("\n"))

    ext_errors = len(exterrors) + len(extwarnings)

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

    return summary_errors + out_errors + ext_errors


def run_pex(name, gds_name, sp_name, output=None):
    """Run pex on a given top-level name which is
       implemented in gds_name and sp_name. """
    OPTS = globals.get_opts()
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

    cmd = "{0} -gui -pex {1}pex_runset -batch 2> {2} 1> {3}".format(OPTS.calibre_exe,
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
    correct_port(name, output, sp_name)

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
    match = re.search("\* \n", rest_text)
    match_index_end = match.start()
    # store the unchanged part of pex file in memory
    pex_file.seek(0)
    part1 = pex_file.read(match_index_start)
    pex_file.seek(match_index_start + match_index_end)
    part2 = pex_file.read()
    pex_file.close()

    # obatin the correct definition line from the original spice file
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
