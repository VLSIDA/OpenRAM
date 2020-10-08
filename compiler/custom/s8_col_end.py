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

class s8_col_end(design.design):


    def __init__(self, version, name=""):
        super().__init__(name)
        pin_names = []
        type_list = []

        if version == "colend":
            self.name = "s8sram16x16_colend"
        elif version == "colend_p_cent":
            self.name = "s8sram16x16_colend_p_cent"
        elif version == "colenda":
            self.name = "s8sram16x16_colenda"
        elif version == "colenda_p_cent":
            self.name = "s8sram16x16_colenda_p_cent"
        else:
            debug.error("Invalid type for col_end", -1)
        design.design.__init__(self, name=self.name)
        (self.width, self.height) = utils.get_libcell_size(self.name,
                                        GDS["unit"],
                                        layer["mem"],
                                        structure)
        pin_map = utils.get_libcell_pins(pin_names, self.name, GDS["unit"])


    
