# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
"""
Utility functions for Hanan router.
"""

def is_in_region(point, region):
    """ Return if a point is in the given region. """

    ll, ur = region.rect
    if is_between(ll.x, ur.x, point.x) and is_between(ll.y, ur.y, point.y):
        return True
    return False


def is_between(a, b, mid):
    """ Return if 'mid' is between 'a' and 'b'. """

    return (a < mid and mid < b) or (b < mid and mid < a)
