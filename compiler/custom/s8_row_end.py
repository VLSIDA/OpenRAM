# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

import debug
import design
import utils
from tech import layer, GDS


class s8_row_end(design.design):

    def __init__(self, version, name=""):
        super().__init__(name)
        pin_names = ["wl", "vpwr"]

        if version == "rowend":
            self.name = "s8sram16x16_rowend"
        elif version == "rowenda":
            self.name = "s8sram16x16_rowenda"
        else:
            debug.error("Invalid type for row_end", -1)
        design.design.__init__(self, name=self.name)
        (self.width, self.height) = utils.get_libcell_size(self.name,
                                                           GDS["unit"],
                                                           layer["mem"])
        self.pin_map = utils.get_libcell_pins(pin_names, self.name, GDS["unit"])

        self.add_pin("wl", "OUTPUT")
        self.add_pin("vpwr", "POWER")
