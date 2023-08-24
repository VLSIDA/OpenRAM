#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from math import sqrt
from openram import debug
from openram.base import vector
from openram.base import round_to_grid
from openram.tech import drc
from openram.tech import array_row_multiple
from openram.tech import array_col_multiple
from openram import OPTS
from openram.modules import replica_bitcell_array
from .sky130_bitcell_base_array import sky130_bitcell_base_array


class sky130_replica_bitcell_array(replica_bitcell_array, sky130_bitcell_base_array):
    """
    Creates a bitcell arrow of cols x rows and then adds the replica
    and dummy columns and rows.  Replica columns are on the left and
    right, respectively and connected to the given bitcell ports.
    Dummy are the outside columns/rows with WL and BL tied to gnd.
    Requires a regular bitcell array, replica bitcell, and dummy
    bitcell (Bl/BR disconnected).
    """
    def __init__(self, rows, cols, rbl=None, left_rbl=None, right_rbl=None, name=""):
    
        super().__init__(rows, cols, rbl, left_rbl, right_rbl, name)
        # total_ports = OPTS.num_rw_ports + OPTS.num_w_ports + OPTS.num_r_ports
        # self.all_ports = list(range(total_ports))
        #
        # self.column_size = cols
        # self.row_size = rows
        #
        # # This is how many RBLs are in all the arrays
        # if rbl:
        #     self.rbl = rbl
        # else:
        #     self.rbl=[1, 1 if len(self.all_ports)>1 else 0]
        # # This specifies which RBL to put on the left or right
        # # by port number
        # # This could be an empty list
        # if left_rbl != None:
        #     self.left_rbl = left_rbl
        # else:
        #     self.left_rbl = [0]
        # # This could be an empty list
        # if right_rbl != None:
        #     self.right_rbl = right_rbl
        # else:
        #     self.right_rbl=[1] if len(self.all_ports) > 1 else []
        # self.rbls = self.left_rbl + self.right_rbl
        #
        # if ((self.column_size + self.rbl[0] + self.rbl[1]) % array_col_multiple != 0):
        #     debug.error("Invalid number of cols including rbl(s): {}. Total cols must be divisible by {}".format(self.column_size + self.rbl[0] + self.rbl[1], array_col_multiple), -1)
        #
        # if ((self.row_size + self.rbl[0] + self.rbl[1]) % array_row_multiple != 0):
        #     debug.error("invalid number of rows including dummy row(s): {}. Total cols must be divisible by {}".format(self.row_size + self.rbl[0] + self.rbl[1], array_row_multiple), -15)
        #


