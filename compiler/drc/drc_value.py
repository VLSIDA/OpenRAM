# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

class drc_value():
    """
    A single DRC value.
    """
    def __init__(self, value):
        self.value = value

    def __call__(self, *args):
        """
        Return the value.
        """
        return self.value




