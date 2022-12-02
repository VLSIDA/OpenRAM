#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2022 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
SRAM Compiler

The output files append the given suffixes to the output name:
a spice (.sp) file for circuit simulation
a GDS2 (.gds) file containing the layout
a LEF (.lef) file for preliminary P&R (real one should be from layout)
a Liberty (.lib) file for timing analysis/optimization
"""

import sys
import os
import datetime
try:
    import openram
except:
    # If openram library isn't found as a python package,
    # import it from the $OPENRAM_HOME path.
    import importlib.util
    OPENRAM_HOME = os.getenv("OPENRAM_HOME")
    # Import using spec since the directory can be named something
    # other than "openram".
    spec = importlib.util.spec_from_file_location("openram", "{}/../__init__.py".format(OPENRAM_HOME))
    module = importlib.util.module_from_spec(spec)
    sys.modules["openram"] = module
    spec.loader.exec_module(module)
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

# Ensure that the right bitcell exists or use the parameterised one
openram.setup_bitcell()

# Only print banner here so it's not in unit tests
openram.print_banner()

# Keep track of running stats
start_time = datetime.datetime.now()
openram.print_time("Start", start_time)

# Output info about this run
openram.report_status()

debug.print_raw("Words per row: {}".format(OPTS.words_per_row))

output_extensions = ["lvs", "sp", "v", "lib", "py", "html", "log"]
# Only output lef/gds if back-end
if not OPTS.netlist_only:
    output_extensions.extend(["lef", "gds"])

output_files = ["{0}{1}.{2}".format(OPTS.output_path,
                                    OPTS.output_name, x)
                for x in output_extensions]
debug.print_raw("Output files are: ")
for path in output_files:
    debug.print_raw(path)

# Create an SRAM (we can also pass sram_config, see documentation/tutorials for details)
from openram import sram
s = sram()

# Output the files for the resulting SRAM
s.save()

# Delete temp files etc.
openram.end_openram()
openram.print_time("End", datetime.datetime.now(), start_time)

