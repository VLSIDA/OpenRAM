# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from .drc_value import *
from .drc_lut import *


class design_rules(dict):
    """
    This is a class that implements the design rules structures.
    """
    def __init__(self, name):
        self.tech_name = name
        self.rules = {}

    def add(self, name, value):
        self.rules[name] = value

    def __call__(self, name, *args):
        rule = self.rules[name]
        if callable(rule):
            return rule(*args)
        else:
            return rule

    def __setitem__(self, b, c):
        """
        For backward compatibility with existing rules.
        """
        self.rules[b] = c

    def __contains__(self, b):
        """
        Allows checking existence of rules
        """
        return b in self.rules

    def __getitem__(self, b):
        """
        For backward compatibility with existing rules.
        """
        rule = self.rules[b]
        if not callable(rule):
            return rule
        else:
            debug.error("Must call complex DRC rule {} with arguments.".format(b),-1)

    def keys(self):
        return self.rules.keys()

    def add_layer(self, name, width, spacing, area=0):
        # Minimum width
        self.add("minwidth_{}".format(name), width)
        # Minimum spacing (could be a table too)
        self.add("{0}_to_{0}".format(name), spacing)
        # Minimum area
        self.add("minarea_{}".format(name), area)

    def add_enclosure(self, name, layer, enclosure, extension=None):
        self.add("{0}_enclose_{1}".format(name, layer), enclosure)
        # Reserved for asymmetric enclosures
        if extension:
            self.add("{0}_extend_{1}".format(name, layer), extension)
        else:
            self.add("{0}_extend_{1}".format(name, layer), enclosure)

