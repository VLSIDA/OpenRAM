# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from globals import OPTS
word_size = 1
num_words = 16

tech_name = OPTS.tech_name
process_corners = ["TT"]
supply_voltages = [5.0]
temperatures = [25]

if tech_name == "freepdk45":
    supply_voltages = [1.0]
    drc_name = "calibre"
    lvs_name = "calibre"
    pex_name = "calibre"
else:
    drc_name = "magic"
    lvs_name = "netgen"
    pex_name = "magic"


