# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
from drc_value import *
from drc_lut import *

class design_rules():
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

    def __getitem__(self, b):
        """
        For backward compatibility with existing rules.
        """
        rule = self.rules[b]
        if not callable(rule):
            return rule
        else:
            debug.error("Must call complex DRC rule {} with arguments.".format(b),-1)

        
        
    
