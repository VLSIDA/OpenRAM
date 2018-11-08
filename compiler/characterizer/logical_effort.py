import debug
from tech import drc, parameter, spice

class logical_effort():
    """
    Class to support the values behind logical effort. Useful for storing the different components
    such as logical effort, electrical effort, and parasitic delay.
    """
    beta = parameter["beta"]
    min_inv_cin = 1+beta
    def __init__(self, size, cin, cout, parasitic):
        self.cin = cin
        self.cout = cout
        self.logical_effort = (self.cin/size)/logical_effort.min_inv_cin
        self.eletrical_effort = self.cout/self.cin
        self.parasitic = parasitic