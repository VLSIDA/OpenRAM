#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from openram import debug
from openram.base import design
from openram.base import get_libcell_size
from openram.tech import layer, GDS


class sky130_corner(design):

    def __init__(self, location, name=""):
        super().__init__(name)

        if location == "ul":
            self.name = "sky130_fd_bd_sram__sram_sp_corner"
        elif location == "ur":
            self.name = "sky130_fd_bd_sram__sram_sp_cornerb"
        elif location == "ll":
            self.name = "sky130_fd_bd_sram__sram_sp_cornera"
        elif location == "lr":
            self.name = "sky130_fd_bd_sram__sram_sp_cornera"
        else:
            debug.error("Invalid sky130_corner location", -1)
        design.__init__(self, name=self.name)
        (self.width, self.height) = get_libcell_size(self.name,
                                                     GDS["unit"],
                                                     layer["mem"])
        # pin_map = get_libcell_pins(pin_names, self.name, GDS["unit"])
