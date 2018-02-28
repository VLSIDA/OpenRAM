#!/usr/bin/env python2.7
"""
SRAM Compiler

The output files append the given suffixes to the output name:
a spice (.sp) file for circuit simulation
a GDS2 (.gds) file containing the layout
a LEF (.lef) file for preliminary P&R (real one should be from layout)
a Liberty (.lib) file for timing analysis/optimization

"""

import sys,os
import datetime
import re
import importlib
from globals import *

(OPTS, args) = parse_args()

# Check that we are left with a single configuration file as argument.
if len(args) != 1:
    print(USAGE)
    sys.exit(2)


# These depend on arguments, so don't load them until now.
import debug


init_openram(config_file=args[0], is_unit_test=False)

# Only print banner here so it's not in unit tests
print_banner()

# Output info about this run
report_status()

# Start importing design modules after we have the config file
import verify
import sram

print("Output files are " + OPTS.output_name + ".(sp|gds|v|lib|lef)")

# Keep track of running stats
start_time = datetime.datetime.now()
print_time("Start",start_time)

# import SRAM test generation
s = sram.sram(word_size=OPTS.word_size,
              num_words=OPTS.num_words,
              num_banks=OPTS.num_banks,
              name=OPTS.output_name)

# Output the files for the resulting SRAM
s.save_output()

# Delete temp files etc.
end_openram()
print_time("End",datetime.datetime.now(), start_time)


