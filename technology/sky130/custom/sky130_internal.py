#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from copy import deepcopy
from openram.modules import internal_base
from openram.tech import cell_properties as props

class sky130_internal(internal_base):

    def __init__(self, version, name=""):
        prop = deepcopy(props.internal)
        prop.boundary_layer = "mem"
        if version == "wlstrap":
            self.name = "sky130_fd_bd_sram__sram_sp_wlstrap"
            prop.port_order = ["vdd"]
            prop.port_types = ["POWER"]
            prop.port_map = {'vdd': 'VPWR'}
        elif version == "wlstrap_p":
            self.name = "sky130_fd_bd_sram__sram_sp_wlstrap_p"
            prop.port_order = ["gnd"]
            prop.port_types = ["GROUND"]
            prop.port_map = {'gnd': 'VGND'}
        elif version == "wlstrapa":
            self.name = "sky130_fd_bd_sram__sram_sp_wlstrapa"
            prop.port_order = ["vdd"]
            prop.port_types = ["POWER"]
            prop.port_map = {'vdd': 'VPWR'}
        elif version == "wlstrapa_p":
            self.name = "sky130_fd_bd_sram__sram_sp_wlstrapa_p"
            prop.port_order = ["gnd"]
            prop.port_types = ["GROUND"]
            prop.port_map = {'gnd': 'VGND'}
        else:
            debug.error("Invalid version", -1)
            
        super().__init__(name, cell_name=self.name, prop=prop)
