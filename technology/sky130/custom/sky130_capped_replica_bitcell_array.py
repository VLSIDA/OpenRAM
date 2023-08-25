# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#

from openram import debug
from openram.base import vector
from openram.base import contact
from openram.sram_factory import factory
from openram.tech import drc, spice
from openram.tech import cell_properties as props
from openram import OPTS
from openram.modules.capped_replica_bitcell_array import capped_replica_bitcell_array
from .sky130_bitcell_base_array import sky130_bitcell_base_array


class sky130_capped_replica_bitcell_array(capped_replica_bitcell_array, sky130_bitcell_base_array):
    """
    Creates a replica bitcell array then adds the row and column caps to all
    sides of a bitcell array.
    """
    def __init__(self, rows, cols, rbl=None, left_rbl=None, right_rbl=None, name=""):
        super().__init__(rows, cols, rbl, left_rbl, right_rbl, name)
 
