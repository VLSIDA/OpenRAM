import os
import gdsMill
import tech
import math
import globals
from vector import vector
from pin_layout import pin_layout

OPTS = globals.OPTS

def ceil(decimal):
    """
    Performs a ceiling function on the decimal place specified by the DRC grid.
    """
    grid = tech.drc["grid"]
    return math.ceil(decimal * 1 / grid) / (1 / grid)

def round_to_grid(number):
    """
    Rounds an arbitrary number to the grid.
    """
    grid = tech.drc["grid"]  
    # this gets the nearest integer value
    number_grid = int(round(round((number / grid), 2), 0))
    number_off = number_grid * grid
    return number_off

def snap_to_grid(offset):
    """
    Changes the coodrinate to match the grid settings
    """
    return [round_to_grid(offset[0]),round_to_grid(offset[1])]

def pin_center(boundary):
    """
    This returns the center of a pin shape in the vlsiLayout border format.
    """
    return [0.5 * (boundary[0] + boundary[2]), 0.5 * (boundary[1] + boundary[3])]

def pin_rect(boundary):
    """
    This returns a LL,UR point pair.
    """
    return [vector(boundary[0],boundary[1]),vector(boundary[2],boundary[3])]

def auto_measure_libcell(pin_list, name, units, layer):
    """
    Open a GDS file and find the pins in pin_list as text on a given layer.
    Return these as a set of properties including the cell width/height too.
    """
    cell_gds = OPTS.openram_tech + "gds_lib/" + str(name) + ".gds"
    cell_vlsi = gdsMill.VlsiLayout(units=units)
    reader = gdsMill.Gds2reader(cell_vlsi)
    reader.loadFromFile(cell_gds)

    cell = {}
    measure_result = cell_vlsi.getLayoutBorder(layer)
    if measure_result == None:
        measure_result = cell_vlsi.measureSize(name)
    [cell["width"], cell["height"]] = measure_result

    for pin in pin_list:
        (name,layer,boundary)=cell_vlsi.getPinShapeByLabel(str(pin))        
        cell[str(pin)] = pin_center(boundary)
    return cell



def get_libcell_size(name, units, layer):
    """
    Open a GDS file and return the library cell size from either the
    bounding box or a border layer.
    """
    cell_gds = OPTS.openram_tech + "gds_lib/" + str(name) + ".gds"
    cell_vlsi = gdsMill.VlsiLayout(units=units)
    reader = gdsMill.Gds2reader(cell_vlsi)
    reader.loadFromFile(cell_gds)

    cell = {}
    measure_result = cell_vlsi.getLayoutBorder(layer)
    if measure_result == None:
        measure_result = cell_vlsi.measureSize(name)
    # returns width,height
    return measure_result


def get_libcell_pins(pin_list, name, units, layer):
    """
    Open a GDS file and find the pins in pin_list as text on a given layer.
    Return these as a rectangle layer pair for each pin.
    """
    cell_gds = OPTS.openram_tech + "gds_lib/" + str(name) + ".gds"
    cell_vlsi = gdsMill.VlsiLayout(units=units)
    reader = gdsMill.Gds2reader(cell_vlsi)
    reader.loadFromFile(cell_gds)

    cell = {}
    for pin in pin_list:
        cell[str(pin)]=[]
        label_list=cell_vlsi.getPinShapeByLabel(str(pin))
        for label in label_list:
            (name,layer,boundary)=label
            rect = pin_rect(boundary)
            # this is a list because other cells/designs may have must-connect pins
            cell[str(pin)].append(pin_layout(pin, rect, layer))
    return cell




