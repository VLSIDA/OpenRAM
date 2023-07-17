# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from .net_spice import net_spice


class pin_spice:
    """
    A class to represent a spice netlist pin.
    mod is the parent module that created this pin.
    mod_net is the net object of this pin's parent module. It must have the same name as the pin.
    inst is the instance this pin is a part of, if any.
    inst_net is the net object from mod's nets which connects to this pin.
    """

    valid_pin_types = ["INOUT", "INPUT", "OUTPUT", "POWER", "GROUND"]

    def __init__(self, name, type, mod):
        self.name = name
        self.set_type(type)
        self.mod = mod
        self.mod_net = None
        self.inst = None
        self.inst_net = None

        # TODO: evaluate if this makes sense... and works
        self._hash = hash(self.name)

    def set_type(self, type):
        debug.check(type in pin_spice.valid_pin_types,
                    "Invalid pin type for {0}: {1}".format(self.name, type))
        self.type = type

    def set_mod_net(self, net):
        debug.check(isinstance(net, net_spice), "net must be a net_spice object")
        debug.check(net.name == self.name, "module spice net must have same name as spice pin")
        self.mod_net = net

    def set_inst(self, inst):
        self.inst = inst

    def set_inst_net(self, net):
        debug.check(self.inst_net is None,
                "pin {} is already connected to net {} so it cannot also be connected to net {}\
                ".format(self.name, self.inst_net.name, net.name))
        debug.check(isinstance(net, net_spice), "net must be a net_spice object")
        self.inst_net = net

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
