#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

"""
ROM Compiler

The output files append the given suffixes to the output name:
a spice (.sp) file for circuit simulation
a GDS2 (.gds) file containing the layout
"""


import sys
import os
import datetime

# You don't need the next two lines if you're sure that openram package is installed
from common import *
make_openram_package()
import openram


(OPTS, args) = openram.parse_args()


# Check that we are left with a single configuration file as argument.
if len(args) != 1:
    print(openram.USAGE)
    sys.exit(2)

# These depend on arguments, so don't load them until now.
from openram import debug

# Parse config file and set up all the options
openram.init_openram(config_file=args[0])

# Only print banner here so it's not in unit tests
openram.print_banner()

# Keep track of running stats
start_time = datetime.datetime.now()
openram.print_time("Start", start_time)


output_extensions = [ "sp", "v"]
# Only output lef/gds if back-end
if not OPTS.netlist_only:
    output_extensions.extend(["gds"])

output_files = ["{0}{1}.{2}".format(OPTS.output_path,
                                    OPTS.output_name, x)
                for x in output_extensions]
debug.print_raw("Output files are: ")
for path in output_files:
    debug.print_raw(path)

from openram import rom

r = rom()

# Output the files for the resulting ROM
r.save()

# Delete temp files etc.
openram.end_openram()
openram.print_time("End", datetime.datetime.now(), start_time)