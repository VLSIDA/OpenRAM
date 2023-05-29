# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
"""
Utility functions for Hanan router.
"""

def is_probe_blocked(p1, p2, blockages):
    """
    Return if a probe sent from p1 to p2 encounters a blockage.
    The probe must be sent vertically or horizontally.
    This method assumes that blockages are rectangular.
    """

    # Check if any blockage blocks this probe
    for blockage in blockages:
        ll, ur = blockage.rect
        right_x = ur[0]
        upper_y = ur[1]
        left_x = ll[0]
        lower_y = ll[1]
        # Check if blocked vertically
        if is_between(left_x, right_x, p1.x) and (is_between(p1.y, p2.y, upper_y) or is_between(p1.y, p2.y, lower_y)):
            return True
        # Check if blocked horizontally
        if is_between(upper_y, lower_y, p1.y) and (is_between(p1.x, p2.x, left_x) or is_between(p1.x, p2.x, right_x)):
            return True
    return False


def is_in_region(point, region):
    """ Return if a point is in the given region. """

    ll, ur = region.rect
    if is_between(ll.x, ur.x, point.x) and is_between(ll.y, ur.y, point.y):
        return True
    return False


def is_between(a, b, mid):
    """ Return if 'mid' is between 'a' and 'b'. """

    return (a < mid and mid < b) or (b < mid and mid < a)
