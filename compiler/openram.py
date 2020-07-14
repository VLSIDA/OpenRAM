#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
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
import datetime
import globals as g

(OPTS, args) = g.parse_args()

# Check that we are left with a single configuration file as argument.
if len(args) != 1:
    print(g.USAGE)
    sys.exit(2)


# These depend on arguments, so don't load them until now.
import debug

# Parse config file and set up all the options
g.init_openram(config_file=args[0], is_unit_test=False)

# Ensure that the right bitcell exists or use the parameterised one
g.setup_bitcell()

# Only print banner here so it's not in unit tests
g.print_banner()

# Keep track of running stats
start_time = datetime.datetime.now()
g.print_time("Start", start_time)

# Output info about this run
g.report_status()

from sram_config import sram_config


# Configure the SRAM organization
c = sram_config(word_size=OPTS.word_size,
                num_words=OPTS.num_words,
                write_size=OPTS.write_size,
                num_banks=OPTS.num_banks,
                words_per_row=OPTS.words_per_row,
                num_spare_rows=OPTS.num_spare_rows,
                num_spare_cols=OPTS.num_spare_cols)
debug.print_raw("Words per row: {}".format(c.words_per_row))

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


from sram import sram
s = sram(sram_config=c,
         name=OPTS.output_name)

# Output the files for the resulting SRAM
s.save()

# Delete temp files etc.
g.end_openram()
g.print_time("End", datetime.datetime.now(), start_time)


