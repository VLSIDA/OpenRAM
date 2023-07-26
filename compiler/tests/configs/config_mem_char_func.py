# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import OPTS
word_size = 2
num_words = 16

tech_name = OPTS.tech_name
if tech_name == "sky130":
    num_spare_cols = 1
    num_spare_rows = 1

output_name = "sram"

analytical_delay = False
nominal_corner_only = True
spice_name = "Xyce"
