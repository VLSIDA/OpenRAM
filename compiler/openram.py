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

# These depend on arguments, so don't load them until now.
import debug

# required positional args for using openram main exe
if len(args) < 1:
    print globals.USAGE
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

if (OPTS.out_name == ""):
    OPTS.out_name = "sram_{0}_{1}_{2}_{3}".format(word_size,
                                                  num_words,
                                                  num_banks,
                                                  OPTS.tech_name)

debug.info(1, "Output file is " + OPTS.out_name + ".(sp|gds|v|lib|lef)")

print "Technology: %s" % (OPTS.tech_name)
print "Word size: {0}\nWords: {1}\nBanks: {2}".format(word_size,num_words,num_banks)

# only start importing modules after we have the config file
import calibre
import sram

print "Start: ", datetime.datetime.now()

# import SRAM test generation
s = sram.sram(word_size=word_size,
              num_words=num_words,
              num_banks=num_banks,
              name=OPTS.out_name)

# Measure design area
# Not working?
#cell_size = s.gds.measureSize(s.name)
#print "Area:", cell_size[0] * cell_size[1]

# Output the files for the resulting SRAM

spname = OPTS.out_path + s.name + ".sp"
print "SP: Writing to {0}".format(spname)
s.sp_write(spname)

gdsname = OPTS.out_path + s.name + ".gds"
print "GDS: Writing to {0}".format(gdsname)
s.gds_write(gdsname)

# Run Characterizer on the design
sram_file = spname
if OPTS.use_pex:
    sram_file = OPTS.out_path + "temp_pex.sp"
    calibre.run_pex(s.name, gdsname, spname, output=sram_file)


# geenrate verilog
import verilog
vname = OPTS.out_path + s.name + ".v"
print "Verilog: Writing to {0}".format(vname)
verilog.verilog(vname,s)

# generate LEF
import lef
lefname = OPTS.out_path + s.name + ".lef"
print "LEF: Writing to {0}".format(lefname)
lef.lef(gdsname,lefname,s)

# generate lib
import lib
libname = OPTS.out_path + s.name + ".lib"
print "LIB: Writing to {0}".format(libname)
lib.lib(libname,s,sram_file)

globals.end_openram()

print "End: ", datetime.datetime.now()
