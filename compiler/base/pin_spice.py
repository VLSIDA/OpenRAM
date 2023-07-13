# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug


class pin_spice:
    """
    A class to represent a spice netlist pin.
    """

    valid_pin_types = ["INOUT", "INPUT", "OUTPUT", "POWER", "GROUND"]

    def __init__(self, name, type):
        self.name = name
        self.set_type(type)

        self._hash = hash(self.name)

    def set_type(self, type):
        debug.check(type in pin_spice.valid_pin_types,
                    "Invalid pin type for {0}: {1}".format(self.name, type))
        self.type = type

    def __str__(self):
        """ override print function output """
        return "(pin_name={} type={})".format(self.name, self.type)

    def __repr__(self):
        """ override repr function output """
        return self.name

    def __hash__(self):
        """
        Implement the hash function for sets etc.
        Only hash name since spice does not allow two pins to share a name.
        Provides a speedup if pin_spice is used as a key for dicts.
        """
        return self._hash
