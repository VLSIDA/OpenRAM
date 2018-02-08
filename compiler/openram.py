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

(OPTS, args) = parse_args(is_unit_test=False)

# These depend on arguments, so don't load them until now.
import debug

# Only print banner here so it's not in unit tests
print_banner()

init_openram(args[0])

# Start importing design modules after we have the config file
import verify
import sram

# Keep track of running stats
start_time = datetime.datetime.now()
last_time = start_time
print_time("Start",last_time)

# import SRAM test generation
s = sram.sram(word_size=OPTS.word_size,
              num_words=OPTS.num_words,
              num_banks=OPTS.num_banks,
              name=OPTS.output_name)
last_time=print_time("SRAM creation", datetime.datetime.now(), last_time)

# Output the files for the resulting SRAM
s.save_output(last_time)

# Delete temp files etc.
end_openram()
print_time("End",datetime.datetime.now(), start_time)


