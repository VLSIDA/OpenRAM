# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

class delay_data():
    """
    This is the delay class to represent the delay information
    Time is 50% of the signal to 50% of reference signal delay.
    Slew is the 10% of the signal to 90% of signal
    """
    def __init__(self, delay=0.0, slew=0.0):
        """ init function support two init method"""
        # will take single input as a coordinate
        self.delay = delay
        self.slew = slew

    def __str__(self):
        """ override print function output """
        return "Delta Data: Delay {} Slew {}".format(self.delay, self.slew)

    def __add__(self, other):
        """
        Override - function (left), for delay_data: a+b != b+a
        """
        assert isinstance(other, delay_data)
        return delay_data(other.delay + self.delay,
                          other.slew)

    def __radd__(self, other):
        """
        Override - function (right), for delay_data: a+b != b+a
        """
        assert isinstance(other, delay_data)
        return delay_data(other.delay + self.delay,
                          self.slew)
