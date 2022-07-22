# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
from tech import cell_properties as props
from .bitcell_base import bitcell_base


class col_cap_bitcell_1port(bitcell_base):
    """
    Column end cap cell. 
    """

    def __init__(self, name="col_cap_bitcell_1port"):
        bitcell_base.__init__(self, name, prop=props.col_cap_1port)
        debug.info(2, "Create col_cap bitcell 1 port object")

        self.no_instances = True
