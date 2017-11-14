#!/usr/bin/env python2.7
"""
SRAM Compiler

The output files append the given suffixes to the output name:
a spice (.sp) file for circuit simulation
a GDS2 (.gds) file containing the layout
a LEF (.lef) file for preliminary P&R (real one should be from layout)
a Liberty (.lib) file for timing analysis/optimization

"""

__author__ = "Matthew Guthaus (mrg@ucsc.edu) and numerous others"
__version__ = "$Revision: 0.9 $"
__copyright__ = "Copyright (c) 2015 UCSC and OSU"
__license__ = "This is not currently licensed for use outside of UCSC's VLSI-DA and OSU's VLSI group."


import sys,os
import datetime
import re
import importlib
import globals

global OPTS

(OPTS, args) = globals.parse_args()

def print_time(name, now_time, last_time=None):
    if last_time:
        time = round((now_time-last_time).total_seconds(),1)
    else:
        time = now_time
    print("** {0}: {1} seconds".format(name,time))
    return now_time

# These depend on arguments, so don't load them until now.
import debug

# required positional args for using openram main exe
if len(args) < 1:
    print(globals.USAGE)
    sys.exit(2)

globals.print_banner()        

globals.init_openram(args[0])

# Check if all arguments are integers for bits, size, banks
if type(OPTS.config.word_size)!=int:
    debug.error("{0} is not an integer in config file.".format(OPTS.config.word_size))
if type(OPTS.config.num_words)!=int:
    debug.error("{0} is not an integer in config file.".format(OPTS.config.sram_size))
if type(OPTS.config.num_banks)!=int:
    debug.error("{0} is not an integer in config file.".format(OPTS.config.num_banks))

if not OPTS.config.tech_name:
    debug.error("Tech name must be specified in config file.")

word_size = OPTS.config.word_size
num_words = OPTS.config.num_words
num_banks = OPTS.config.num_banks

if (OPTS.output_name == ""):
    OPTS.output_name = "sram_{0}_{1}_{2}_{3}".format(word_size,
                                                  num_words,
                                                  num_banks,
                                                  OPTS.tech_name)

print("Output files are " + OPTS.output_name + ".(sp|gds|v|lib|lef)")

print("Technology: {0}".format(OPTS.tech_name))
print("Word size: {0}\nWords: {1}\nBanks: {2}".format(word_size,num_words,num_banks))


if OPTS.analytical_delay:
    print("Using analytical delay models (no characterization)")
else:
    print("Performing simulation-based characterization with {}".format(OPTS.spice_version))

if OPTS.trim_netlist:
    print("Trimming netlist to speed up characterization (sacrificing some accuracy).")

# only start importing modules after we have the config file
import calibre
import sram

start_time = datetime.datetime.now()
last_time = start_time
print_time("Start",datetime.datetime.now())

# import SRAM test generation
s = sram.sram(word_size=word_size,
              num_words=num_words,
              num_banks=num_banks,
              name=OPTS.output_name)
last_time=print_time("SRAM creation", datetime.datetime.now(), last_time)
# Measure design area
# Not working?
#cell_size = s.gds.measureSize(s.name)
#print("Area:", cell_size[0] * cell_size[1])

# Output the files for the resulting SRAM

spname = OPTS.output_path + s.name + ".sp"
print("SP: Writing to {0}".format(spname))
s.sp_write(spname)
last_time=print_time("Spice writing", datetime.datetime.now(), last_time)

# Output the extracted design
sram_file = spname
if OPTS.use_pex:
    sram_file = OPTS.output_path + "temp_pex.sp"
    calibre.run_pex(s.name, gdsname, spname, output=sram_file)

# Characterize the design
import lib
libname = OPTS.output_path + s.name + ".lib"
print("LIB: Writing to {0}".format(libname))
lib.lib(libname,s,sram_file)
last_time=print_time("Characterization", datetime.datetime.now(), last_time)

# Write the layout
gdsname = OPTS.output_path + s.name + ".gds"
print("GDS: Writing to {0}".format(gdsname))
s.gds_write(gdsname)
last_time=print_time("GDS", datetime.datetime.now(), last_time)

# Create a LEF physical model
import lef
lefname = OPTS.output_path + s.name + ".lef"
print("LEF: Writing to {0}".format(lefname))
lef.lef(gdsname,lefname,s)
last_time=print_time("LEF writing", datetime.datetime.now(), last_time)

# Write a verilog model
import verilog
vname = OPTS.output_path + s.name + ".v"
print("Verilog: Writing to {0}".format(vname))
verilog.verilog(vname,s)
last_time=print_time("Verilog writing", datetime.datetime.now(), last_time)

globals.end_openram()
print_time("End",datetime.datetime.now(), start_time)
