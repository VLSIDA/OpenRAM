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
        return self.rules[name](args)

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
        if callable(rule):
            return rule()
        else:
            return rule
        
        
    
