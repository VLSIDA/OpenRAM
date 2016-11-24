import os
import gdsMill
import tech 
import globals

OPTS = globals.OPTS

def gdsPinToOffset(gdsPin):
    boundary = gdsPin[2]
    return [0.5 * (boundary[0] + boundary[2]), 0.5 * (boundary[1] + boundary[3])]

def auto_measure_libcell(pin_list, name, units, layer):
    cell_gds = OPTS.openram_tech + "gds_lib/" + str(name) + ".gds"
    cell_vlsi = gdsMill.VlsiLayout(units=units)
    reader = gdsMill.Gds2reader(cell_vlsi)
    reader.loadFromFile(cell_gds)

    cell = {}
    measure_result = cell_vlsi.readLayoutBorder(layer)
    if measure_result == None:
        measure_result = cell_vlsi.measureSize(name)
    [cell["width"], cell["height"]] = measure_result

    for pin in pin_list:
        cell[str(pin)] = gdsPinToOffset(cell_vlsi.readPin(str(pin)))
    return cell




