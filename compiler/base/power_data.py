# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

class power_data():
    """
    This is the power class to represent the power information
    Dynamic and leakage power are stored as a single object with this class.
    """
    def __init__(self, dynamic=0.0, leakage=0.0):
        """ init function support two init method"""
        # will take single input as a coordinate
        self.dynamic = dynamic
        self.leakage = leakage

    def __str__(self):
        """ override print function output """
        return "Power Data: Dynamic "+str(self.dynamic)+", Leakage "+str(self.leakage)+" in nW"

    def __add__(self, other):
        """
        Override - function (left), for power_data: a+b != b+a
        """
        assert isinstance(other,power_data)
        return power_data(other.dynamic + self.dynamic,
                          other.leakage + self.leakage)

    def __radd__(self, other):
        """
        Override - function (left), for power_data: a+b != b+a
        """
        assert isinstance(other,power_data)
        return power_data(other.dynamic + self.dynamic,
                          other.leakage + self.leakage)
