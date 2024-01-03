# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California, Santa Cruz
# All rights reserved.
#

class graph_probe:
    """
    This class represents a probe sent from one point to another on Hanan graph.
    This is used to mimic the pin_layout class to utilize its methods.
    """

    def __init__(self, p1, p2, lpp):

        self.rect = (p1.min(p2), p1.max(p2))
        self.lpp = lpp
