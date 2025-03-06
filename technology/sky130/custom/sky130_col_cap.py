#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from openram import debug
from openram.base import design
from openram.tech import cell_properties as props
from openram import OPTS

class sky130_col_cap(design):

    def __init__(self, version, name="",left_rbl=[],right_rbl=[]):
        
        if version == "colend":
            if OPTS.control_logic == "control_logic_delay" or not right_rbl:
                cell_name = "sky130_fd_bd_sram__sram_sp_colend"
            else:
                cell_name = "sky130_fd_bd_sram__openram_sp_colend_replica"
            prop = props.col_cap_1port_bitcell
            
        elif version == "colenda":
            if OPTS.control_logic == "control_logic_delay" or not left_rbl:
                cell_name = "sky130_fd_bd_sram__sram_sp_colenda"
            else:
                cell_name = "sky130_fd_bd_sram__openram_sp_colenda_replica"
            prop = props.col_cap_1port_bitcell
            
        elif version == "colend_p_cent":
            cell_name = "sky130_fd_bd_sram__sram_sp_colend_p_cent"
            prop = props.col_cap_1port_strap_ground
        elif version == "colenda_p_cent":
            cell_name = "sky130_fd_bd_sram__sram_sp_colenda_p_cent"
            prop = props.col_cap_1port_strap_ground
        elif version == "colend_cent":
            cell_name = "sky130_fd_bd_sram__sram_sp_colend_cent"
            prop = props.col_cap_1port_strap_power
        elif version == "colenda_cent":
            cell_name = "sky130_fd_bd_sram__sram_sp_colenda_cent"
            prop = props.col_cap_1port_strap_power
        else:
            debug.error("Invalid type for col_end", -1)
        super().__init__(name=name, cell_name=cell_name, prop=prop)
