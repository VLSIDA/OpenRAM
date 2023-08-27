#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from openram import debug
from openram.base import design
from openram.tech import cell_properties as props


class sky130_corner(design):

    def __init__(self, location, name=""):

        if location == "ul":
            cell_name = "sky130_fd_bd_sram__sram_sp_corner"
        elif location == "ur":
            cell_name = "sky130_fd_bd_sram__sram_sp_cornerb"
        elif location == "ll":
            cell_name = "sky130_fd_bd_sram__sram_sp_cornera"
        elif location == "lr":
            cell_name = "sky130_fd_bd_sram__sram_sp_cornera"
        else:
            debug.error("Invalid sky130_corner location", -1)
        super().__init__(name=name, cell_name=cell_name, prop=props.col_cap_1port_strap_power)
