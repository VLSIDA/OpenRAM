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
from globals import OPTS
from tech import parameter, drc, layer, GDS

class s8_internal(design.design):


    def __init__(self, version, name=""):
        super().__init__(name)
        pin_names = []
        type_list = []
        
        if version == "wlstrap":
            self.name = "s8sram_wlstrap"
            self.structure = "s8sram_wlstrap_ce\x00"
        elif version == "wlstrap_p":
            self.name = "s8sram16x16_wlstrap_p"
            self.structure = "s8sram16x16_wlstrap_p_ce"
        else:
            debug.error("Invalid version", -1)
        design.design.__init__(self, name=self.name)
        (self.width, self.height) = utils.get_libcell_size(self.name,
                                        GDS["unit"],
                                        layer["mem"],
                                        self.structure)
        pin_map = utils.get_libcell_pins(pin_names, self.name, GDS["unit"])