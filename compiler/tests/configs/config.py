# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import OPTS
word_size = 1
num_words = 16

tech_name = OPTS.tech_name

nominal_corner_only = True
check_lvsdrc = True

if tech_name == "ihp_sg13g2":
    analytical_delay = False
    trim_netlist = False
    spice_name = "ngspice"
    use_nix = False  # Tests use the selected IIC-OSIC environment.

#route_supplies = False

output_name = "sram"
rom_data_dir = "tests/configs"
