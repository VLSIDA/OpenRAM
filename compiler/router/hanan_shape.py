# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram.base.pin_layout import pin_layout


class hanan_shape(pin_layout):
    """
    This class inherits the pin_layout class to change some of its behavior for
    the Hanan router.
    """

    def __init__(self, name, rect, layer_name_pp):

        pin_layout.__init__(self, name, rect, layer_name_pp)


    def inflated_pin(self, spacing=None, multiple=0.5):
        """ Override the default inflated_pin behavior. """

        inflated_area = self.inflate(spacing, multiple)
        return hanan_shape(self.name, inflated_area, self.layer)


    def aligns(self, other):
        """ Return if the other shape aligns with this shape. """

        # Shapes must overlap to be able to align
        if not self.overlaps(other):
            return False
        ll, ur = self.rect
        oll, our = other.rect
        if ll.x == oll.x and ur.x == our.x:
            return True
        if ll.y == oll.y and ur.y == our.y:
            return True
        return False
