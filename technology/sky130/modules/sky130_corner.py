#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California
# All rights reserved.
#

import debug
import design
import utils
from tech import layer, GDS


class sky130_corner(design.design):

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
        design.design.__init__(self, name=self.name)
        (self.width, self.height) = utils.get_libcell_size(self.name,
                                                           GDS["unit"],
                                                           layer["mem"])
        # pin_map = utils.get_libcell_pins(pin_names, self.name, GDS["unit"])
