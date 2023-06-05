#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from openram import debug
from openram.base import design
from openram.tech import cell_properties as props


class sky130_row_cap(design):

    def __init__(self, version, name=""):

        if version == "rowend":
            cell_name = "sky130_fd_bd_sram__sram_sp_rowend"
        elif version == "rowenda":
            cell_name = "sky130_fd_bd_sram__sram_sp_rowenda"
        elif version == "rowend_replica":
            cell_name = "sky130_fd_bd_sram__openram_sp_rowend_replica"
        elif version == "rowenda_replica":
            cell_name = "sky130_fd_bd_sram__openram_sp_rowenda_replica"
        else:
            debug.error("Invalid type for row_end", -1)
        super().__init__(name=name, cell_name=cell_name, prop=props.row_cap_1port_cell)
