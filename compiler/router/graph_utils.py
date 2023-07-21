# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
"""
Utility functions for graph router.
"""
from openram.base import vector
from openram.tech import drc


def snap_to_grid(v):
    """ Use custom `snap_to_grid` since `vector.snap_to_grid` isn't working. """

    return vector(snap_offset_to_grid(v.x), snap_offset_to_grid(v.y))


def snap_offset_to_grid(offset):
    """
    Use custom `snap_offset_to_grid` since `vector.snap_offset_to_grid` isn't
    working.
    """

    return round(offset, len(str(drc["grid"]).split('.')[1]))
