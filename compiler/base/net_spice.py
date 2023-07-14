# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from .pin_spice import pin_spice


class net_spice:
    """
    A class to represent a spice net.
    pins are all the pins connected to this net.
    inst is the instance this net is a part of, if any.
    """

    def __init__(self, name):
        self.name = name
        self.pins = []
        self.inst = None

        # TODO: evaluate if this makes sense... and works
        self._hash = hash(self.name)

    def connect_pin(self, pin):
        debug.check(isinstance(pin, pin_spice), "pin must be a pin_spice object")
        if pin in self.pins:
            debug.warning("pin {} was already connected to net {} ... why was it connected again?".format(pin.name, self.name))
        else:
            self.pins.append(pin)

    def __str__(self):
        """ override print function output """
        return "(pin_name={} type={})".format(self.name, self.type)

    def __repr__(self):
        """ override repr function output """
        return self.name

    def __eq__(self, name):
        return (name == self.name) if isinstance(name, str) else super().__eq__(name)

    def __hash__(self):
        """
        Implement the hash function for sets etc.
        Only hash name since spice does not allow two pins to share a name.
        Provides a speedup if pin_spice is used as a key for dicts.
        """
        return self._hash
