    #!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from openram.base import geometry
from openram.sram_factory import factory
from openram.tech import layer
from openram import OPTS
from openram.modules.col_cap_array import col_cap_array  
from .sky130_bitcell_base_array import sky130_bitcell_base_array

class sky130_col_cap_array(col_cap_array, sky130_bitcell_base_array):
    """
    Generate a dummy row/column for the replica array.
    """
    def __init__(self, rows, cols, column_offset=0, mirror=0, location="", name=""):
        super().__init__(rows, cols, column_offset=0, mirror=0, location="", name="")

    def add_modules(self):
        """ Add the modules used in this design """
        if self.location == "top":
            self.colend1 = factory.create(module_type="col_cap", version="colend")
            self.colend2 = factory.create(module_type="col_cap", version="colend_p_cent")
            self.colend3 = factory.create(module_type="col_cap", version="colend_cent")
        elif self.location == "bottom":
            self.colend1 = factory.create(module_type="col_cap", version="colenda")
            self.colend2 = factory.create(module_type="col_cap", version="colenda_p_cent")
            self.colend3 = factory.create(module_type="col_cap", version="colenda_cent")

        self.cell = factory.create(module_type=OPTS.bitcell, version="opt1")

    def create_instances(self):
        