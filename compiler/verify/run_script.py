# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
Some baseline functions to run scripts.
"""

import os
import debug
import subprocess
import time
from globals import OPTS


def run_script(cell_name, script="lvs"):
    """ Run script and create output files. """

    echo_cmd_output = OPTS.verbose_level > 1

    cwd = os.getcwd()
    os.chdir(OPTS.openram_temp)
    errfile = "{0}{1}.{2}.err".format(OPTS.openram_temp, cell_name, script)
    outfile = "{0}{1}.{2}.out".format(OPTS.openram_temp, cell_name, script)
    resultsfile = "{0}{1}.{2}.report".format(OPTS.openram_temp, cell_name, script)

    scriptpath = '{0}run_{1}.sh'.format(OPTS.openram_temp, script)

    debug.info(2, "Starting {}".format(scriptpath))
    start = time.time()
    with open(outfile, 'wb') as fo, open(errfile, 'wb') as fe:
        p = subprocess.Popen(
                [scriptpath], stdout=fo, stderr=fe, cwd=OPTS.openram_temp)

        if echo_cmd_output:
            tailo = subprocess.Popen([
                'tail',
                '-f',                # Follow the output
                '--pid', str(p.pid), # Close when this pid exits
                outfile,
            ])
            taile = subprocess.Popen([
                'tail',
                '-f',                # Follow the output
                '--pid', str(p.pid), # Close when this pid exits
                errfile,
            ])

    lastoutput = start
    while p.poll() == None:
        runningfor = time.time() - start
        outputdelta = time.time() - lastoutput
        if outputdelta > 30:
            lastoutput = time.time()
            debug.info(1, "Still running {} ({:.0f} seconds)".format(scriptpath, runningfor))
        time.sleep(1)
    assert p.poll() != None, (p.poll(), p)
    p.wait()

    # Kill the tail commands if they haven't finished.
    if echo_cmd_output:
        if tailo.poll() != None:
            tailo.kill()
        tailo.wait()
        if taile.poll() != None:
            taile.kill()
        taile.wait()

    debug.info(2, "Finished {} with {}".format(scriptpath, p.returncode))

    os.chdir(cwd)

    return (outfile, errfile, resultsfile)

