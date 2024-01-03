#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
This script will generate a stimulus file for a given period, load, and slew input
for the given dimension SRAM. It is useful for debugging after an SRAM has been
created without re-running the entire process. Right now, it assumes the nominal
corner, but should probably be extended.
"""

import sys
from globals import *
from importlib import reload

(OPTS, args) = parse_args()

# Override the usage
USAGE = "Usage: {} [options] <config file> <period in ns> <load in fF> <slew in ns>\nUse -h for help.\n".format(__file__)

# Check that we are left with a single configuration file as argument.
if len(args) != 4:
    print(USAGE)
    sys.exit(2)


# We need to get the:
# config file
config_file = args[0]
# period
period = float(args[1])
# load
load = float(args[2])
# slew
slew = float(args[3])

# These depend on arguments, so don't load them until now.
import debug

init_openram(config_file=config_file, is_unit_test=False)

from sram_config import sram_config
c = sram_config(word_size=OPTS.word_size,
                num_words=OPTS.num_words,
                write_size=OPTS.write_size,
                num_banks=OPTS.num_banks,
                words_per_row=OPTS.words_per_row,
                num_spare_rows=OPTS.num_spare_rows,
                num_spare_cols=OPTS.num_spare_cols)

OPTS.netlist_only = True
OPTS.check_lvsdrc = False
# Put the temp output in the output path since it is what we want to generate!
old_openram_temp = OPTS.openram_temp
OPTS.openram_temp = OPTS.output_path

from sram import sram
s = sram(name=OPTS.output_name, sram_config=c)

from characterizer import delay
import tech
# Set up the delay and set to the nominal corner
d = delay(s, s.get_sp_name(), ("TT", tech.spice["nom_supply_voltage"], tech.spice["nom_temperature"]))
# Set the period
d.period = period
# Set the load of outputs and slew of inputs
d.set_load_slew(load,slew)
# Set the probe address/bit
if (self.num_spare_rows == 0):
    probe_address = "1" * sram.addr_size
else:
    probe_address = "0" + ("1" * sram.addr_size - 1)
probe_data = sram.word_size - 1
d.set_probe(probe_address, probe_data)

d.write_delay_stimulus()

# Output info about this run
report_status()
print("Output files are:\n{0}stim.sp\n{0}sram.sp\n{0}reduced.sp".format(OPTS.output_path))
OPTS.openram_temp = old_openram_temp
# Delete temp files, remove the dir, etc.
end_openram()
