from flask_table import *

class operating_conditions(Table):
    """
    Set up operating conditions columns and title information
    """
    parameter = Col('Parameter')
    min = Col('Min')
    typ = Col('Typ')
    max = Col('Max')
    units = Col('Units')

class operating_conditions_item(object):
    """
    Define operating conditions table row element
    """
    def __init__(self, parameter, min, typ, max, units):
        self.parameter = parameter
        self.min = min
        self.typ = typ
        self.max = max
        self.units = units

