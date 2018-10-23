from flask_table import *

class characterization_corners(Table):
    corner_name = Col('Corner Name')
    process = Col('Process')
    power_supply = Col('Power Supply')
    temperature = Col('Temperature')
    library_name_suffix = Col('Library Name Suffix')

class characterization_corners_item(object):
    def __init__(self, corner_name, process, power_supply, temperature, library_name_suffix):
        self.corner_name = corner_name
        self.process = process
        self.power_supply = power_supply
        self.temperature = temperature
        self.library_name_suffix = library_name_suffix

