from flask_table import *

class timing_and_current_data(Table):
    """
    Set up timing and current table columns and title information
    """
    parameter = Col('Parameter')
    min = Col('Min')
    max = Col('Max')
    units = Col('Units')

class timing_and_current_data_item(object):
    """
    Define timing and current data row element
    """
    def __init__(self, parameter, min, max, units):
        self.parameter = parameter
        self.min = min
        self.max = max
        self.units = units


