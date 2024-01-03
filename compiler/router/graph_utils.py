# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California, Santa Cruz
# All rights reserved.
#
"""
Utility functions for graph router.
"""
from openram.base import vector
from openram.tech import drc


def snap(a):
    """ Use custom `snap` since `vector.snap_to_grid` isn't working. """

    if isinstance(a, vector):
        return vector(snap(a.x), snap(a.y))
    return round(a, len(str(drc["grid"]).split('.')[1]))
