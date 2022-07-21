#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California
# All rights reserved.
#

import debug
from base import design
from base import get_libcell_size
from tech import layer, GDS


class sky130_internal(design):

    def __init__(self, version, name=""):
        super().__init__(name)

        if version == "wlstrap":
            self.name = "sky130_fd_bd_sram__sram_sp_wlstrap"
        elif version == "wlstrap_p":
            self.name = "sky130_fd_bd_sram__sram_sp_wlstrap_p"
        elif version == "wlstrapa":
            self.name = "sky130_fd_bd_sram__sram_sp_wlstrapa"
        elif version == "wlstrapa_p":
            self.name = "sky130_fd_bd_sram__sram_sp_wlstrapa_p"
        else:
            debug.error("Invalid version", -1)
        design.__init__(self, name=self.name)
        (self.width, self.height) = get_libcell_size(self.name,
                                                     GDS["unit"],
                                                     layer["mem"])
        # pin_map = get_libcell_pins(pin_names, self.name, GDS["unit"])
