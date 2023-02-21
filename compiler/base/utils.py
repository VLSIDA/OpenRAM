# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os
import math
from openram import debug
from openram import tech
from openram.gdsMill import gdsMill
from openram import OPTS
from .vector import vector
from .pin_layout import pin_layout
try:
    from openram.tech import special_purposes
except ImportError:
    special_purposes = {}


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
    return [round_to_grid(offset[0]),
            round_to_grid(offset[1])]


def pin_center(boundary):
    """
    This returns the center of a pin shape in the vlsiLayout border format.
    """
    return [0.5 * (boundary[0] + boundary[2]),
            0.5 * (boundary[1] + boundary[3])]


def auto_measure_libcell(pin_list, name, units, lpp):
    """
    Open a GDS file and find the pins in pin_list as text on a given layer.
    Return these as a set of properties including the cell width/height too.
    """
    cell_gds = OPTS.openram_tech + "gds_lib/" + str(name) + ".gds"

    cell_vlsi = _get_gds_reader(units, cell_gds)

    # FIXME: This duplicates a lot of functionality of get_gds_size and
    # get_gds_pins, it should probably just call those functions?
    cell = {}
    measure_result = cell_vlsi.getLayoutBorder(lpp[0])
    if measure_result:
        measure_result = cell_vlsi.measureSize(name)
    [cell["width"], cell["height"]] = measure_result

    for pin in pin_list:
        (name, lpp, boundary) = cell_vlsi.getPinShapeByLabel(str(pin))
        cell[str(pin)] = pin_center(boundary)
    return cell


_GDS_READER_CACHE = {}


def _get_gds_reader(units, gds_filename):
    gds_absname = os.path.realpath(gds_filename)
    k = (units, gds_absname)
    try:
        return _GDS_READER_CACHE[k]
    except KeyError:
        debug.info(4, "Creating VLSI layout from {}".format(gds_absname))
        cell_vlsi = gdsMill.VlsiLayout(units=units)
        reader = gdsMill.Gds2reader(cell_vlsi)
        reader.loadFromFile(gds_absname, special_purposes)

        _GDS_READER_CACHE[k] = cell_vlsi
        return cell_vlsi


_GDS_SIZE_CACHE = {}


def get_gds_size(name, gds_filename, units, lpp):
    """
    Open a GDS file and return the size from either the
    bounding box or a border layer.
    """
    k = (name, os.path.realpath(gds_filename), units, lpp)
    try:
        return _GDS_SIZE_CACHE[k]
    except KeyError:
        cell_vlsi = _get_gds_reader(units, gds_filename)

        measure_result = cell_vlsi.getLayoutBorder(lpp)
        if not measure_result:
            debug.info(2, "Layout border failed. Trying to measure size for {}".format(name))
            measure_result = cell_vlsi.measureSize(name)

        _GDS_SIZE_CACHE[k] = measure_result

        # returns width,height
        return measure_result


def get_libcell_size(name, units, lpp):
    """
    Open a GDS file and return the library cell size from either the
    bounding box or a border layer.
    """

    cell_gds = OPTS.openram_tech + "gds_lib/" + str(name) + ".gds"
    return(get_gds_size(name, cell_gds, units, lpp))


_GDS_PINS_CACHE = {}


def get_gds_pins(pin_names, name, gds_filename, units):
    """
    Open a GDS file and find the pins in pin_names as text on a given layer.
    Return these as a rectangle layer pair for each pin.
    """
    k = (tuple(pin_names), name, os.path.realpath(gds_filename), units)
    try:
        return dict(_GDS_PINS_CACHE[k])
    except KeyError:
        cell_vlsi = _get_gds_reader(units, gds_filename)

        cell = {}
        for pin_name in pin_names:
            cell[str(pin_name)] = []
            pin_list = cell_vlsi.getPinShape(str(pin_name))
            for pin_shape in pin_list:
                if pin_shape != None:
                    (lpp, boundary) = pin_shape
                    rect = [vector(boundary[0], boundary[1]),
                            vector(boundary[2], boundary[3])]
                    # this is a list because other cells/designs
                    # may have must-connect pins
                    if isinstance(lpp[1], list):
                        try:
                            from openram.tech import layer_override
                            if layer_override[pin_name]:
                                lpp = layer_override[pin_name.textString]
                        except:
                            pass
                        lpp = (lpp[0], None)
                    cell[str(pin_name)].append(pin_layout(pin_name, rect, lpp))

        _GDS_PINS_CACHE[k] = cell
        return dict(cell)


def get_libcell_pins(pin_list, name, units):
    """
    Open a GDS file and find the pins in pin_list as text on a given layer.
    Return these as a rectangle layer pair for each pin.
    """

    cell_gds = OPTS.openram_tech + "gds_lib/" + str(name) + ".gds"
    return(get_gds_pins(pin_list, name, cell_gds, units))
