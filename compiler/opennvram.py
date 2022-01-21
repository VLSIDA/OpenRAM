#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
NVRAM Compiler

Based on the SRAM compiler

The output files append the given suffixes to the output name:
a spice (.sp) file for circuit simulation
a GDS2 (.gds) file containing the layout
a LEF (.lef) file for preliminary P&R (real one should be from layout)
"""

import sys
import datetime
import globals as g

(OPTS, args) = g.parse_args()

# Check that we are left with a single configuration file as argument.
if len(args) != 1:
    print(g.USAGE)
    sys.exit(2)



