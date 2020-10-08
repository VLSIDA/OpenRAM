# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import design
import debug
import utils
from tech import GDS,layer,drc,parameter,cell_properties
from tech import cell_properties as props
import bitcell_base
from globals import OPTS

class s8_dummy_bitcell(bitcell_base.bitcell_base):
    """
    A single bit cell (6T, 8T, etc.)  This module implements the
    single memory cell used in the design. It is a hand-made cell, so
    the layout and netlist should be available in the technology
    library.
    """
    if props.compare_ports(props.bitcell.split_wl):
        pin_names = ["bl", "br", "wl0", "wl1", "vdd", "gnd"]
        type_list = ["OUTPUT", "OUTPUT", "INPUT", "INPUT" , "POWER", "GROUND"] 
    else:
        pin_names = [props.bitcell.cell_s8_6t.pin.bl,
                    props.bitcell.cell_s8_6t.pin.br,
                    props.bitcell.cell_s8_6t.pin.wl,
                    "vpwr",
                    "vgnd"]



    def __init__(self, version, name=""):
        # Ignore the name argument

        if version == "opt1":
            self.name = "s8sram_cell_opt1"
            self.border_structure = "s8sram_cell"
        elif version == "opt1a":
            self.name = "s8sram_cell_opt1a"
            self.border_structure = "s8sram_cell"
        bitcell_base.bitcell_base.__init__(self, self.name)
        debug.info(2, "Create dummy bitcell")
        (self.width, self.height) = utils.get_libcell_size(self.name,
                                            GDS["unit"],
                                            layer["mem"],
                                            "s8sram_cell\x00")
        self.pin_map = utils.get_libcell_pins(self.pin_names, self.name, GDS["unit"])


