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
from openram.modules.replica_bitcell_array import replica_bitcell_array
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

