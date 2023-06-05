# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

from enum import Enum

class sram_op(Enum):
    READ_ZERO = 0
    READ_ONE = 1
    WRITE_ZERO = 2
    WRITE_ONE = 3
