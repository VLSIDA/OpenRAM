# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
"""
Utility functions for navigation router.
"""

def is_in_region(point, region):
    """"""

    if is_between(region[0].x, region[1].x, point.x) and is_between(region[0].y, region[1].y, point.y):
        return True
    return False


def is_between(a, b, mid):
    """ Return if 'mid' is between 'a' and 'b'. """

    return (a < mid and mid < b) or (b < mid and mid < a)
