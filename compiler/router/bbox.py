# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram.base.vector import vector
from .graph_utils import snap


class bbox:
    """
    This class represents a bounding box object that is used in `bbox_node`
    class. We are using bbox objects to group shapes in the router graphs.
    """

    def __init__(self, shape=None):

        self.shape = shape
        self.rect = None
        if self.shape:
            self.rect = self.shape.rect


    def area(self):
        """ Return the area of this bbox. """

        ll, ur = self.rect
        width = ur.x - ll.x
        height = ur.y - ll.y
        return snap(width * height)


    def merge(self, other):
        """ Return the bbox created by merging two bbox objects. """

        ll, ur = self.rect
        oll, our = other.rect
        min_x = min(ll.x, oll.x)
        max_x = max(ur.x, our.x)
        min_y = min(ll.y, oll.y)
        max_y = max(ur.y, our.y)
        rect = [vector(min_x, min_y), vector(max_x, max_y)]
        merged = bbox()
        merged.rect = rect
        return merged


    def overlap(self, other):
        """ Return the bbox created by overlapping two bbox objects. """

        ll, ur = self.rect
        oll, our = other.rect
        min_x = max(ll.x, oll.x)
        max_x = min(ur.x, our.x)
        min_y = max(ll.y, oll.y)
        max_y = min(ur.y, our.y)
        if max_x >= min_x and max_y >= min_y:
            rect = [vector(min_x, min_y), vector(max_x, max_y)]
        else:
            return None
        overlapped = bbox()
        overlapped.rect = rect
        return overlapped
