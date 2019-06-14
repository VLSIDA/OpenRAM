# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
Some baseline functions to run scripts.
"""

import os
import debug
from globals import OPTS

def run_script(cell_name, script="lvs"):
    """ Run script and create output files. """

    cwd = os.getcwd()
    os.chdir(OPTS.openram_temp)
    errfile = "{0}{1}.{2}.err".format(OPTS.openram_temp, cell_name, script)
    outfile = "{0}{1}.{2}.out".format(OPTS.openram_temp, cell_name, script)
    resultsfile = "{0}{1}.{2}.report".format(OPTS.openram_temp, cell_name, script)

    cmd = "{0}run_{1}.sh 2> {2} 1> {3}".format(OPTS.openram_temp,
                                               script,
                                               errfile,
                                               outfile)
    debug.info(2, cmd)
    os.system(cmd)
    os.chdir(cwd)

    return (outfile,errfile,resultsfile)

