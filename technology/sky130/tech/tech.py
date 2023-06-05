#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#


import os
from openram import drc as d

"""
File containing the process technology parameters for Skywater 130nm.
"""

###################################################
# Custom modules
###################################################

# This uses the default classes to instantiate module from
# '$OPENRAM_HOME/compiler/modules'.
# Using tech_modules['cellname'] you can override each class by providing a custom
# implementation in '$OPENRAM_TECHDIR/modules/'
# For example: tech_modules["contact"] = "contact_freepdk45"
tech_modules = d.module_type()

# These modules have been hand designed and provided in this repository.
tech_modules["nand2_dec"] = "nand2_dec"
tech_modules["nand3_dec"] = "nand3_dec"
tech_modules["nand4_dec"] = "nand4_dec"

# Override default OpenRAM modules to sky130 modules
# These are for single port and dual port as a list,
# or for both if there is no list,
# or only applicable to one if there is no list.
tech_modules["bitcell_1port"] = "sky130_bitcell"
tech_modules["replica_bitcell_1port"] = "sky130_replica_bitcell"
tech_modules["dummy_bitcell_1port"] = "sky130_dummy_bitcell"

tech_modules["replica_bitcell_2port"] = "replica_bitcell_2port"
tech_modules["dummy_bitcell_2port"] = "dummy_bitcell_2port"
tech_modules["bitcell_2port"] = "bitcell_2port"

tech_modules["bitcell_array"] = ["sky130_bitcell_array", "bitcell_array"]
tech_modules["replica_bitcell_array"] = ["sky130_replica_bitcell_array", "replica_bitcell_array"]
tech_modules["capped_replica_bitcell_array"] = ["sky130_capped_replica_bitcell_array", "capped_replica_bitcell_array"]
tech_modules["dummy_array"] = ["sky130_dummy_array", "dummy_array"]

tech_modules["replica_column"] = ["sky130_replica_column", "replica_column"]

tech_modules["col_cap_array"] = ["sky130_col_cap_array", "col_cap_array"]
tech_modules["col_cap"] = ["sky130_col_cap", "col_cap_bitcell_2port"]
tech_modules["corner"] = ["sky130_corner", None]
tech_modules["internal"] = ["sky130_internal", None]
tech_modules["row_cap_array"] = ["sky130_row_cap_array", "row_cap_array"]
tech_modules["row_cap"] = ["sky130_row_cap", "row_cap_bitcell_2port"]

# These modules are auto-generated from the nand decoders above and are not
# found in this.
tech_modules["buf_dec"] = "pbuf_dec"
tech_modules["inv_dec"] = "pinv_dec"
tech_modules["and2_dec"] = "and2_dec"
tech_modules["and3_dec"] = "and3_dec"
tech_modules["and4_dec"] = "and4_dec"

###################################################
# Custom cell properties
###################################################
cell_properties = d.cell_properties()

cell_properties.bitcell_power_pin_directions = ("H", "H")

cell_properties.bitcell_1port.mirror.x = True
cell_properties.bitcell_1port.mirror.y = True
cell_properties.bitcell_1port.end_caps = True
cell_properties.bitcell_1port.boundary_layer = "mem"
cell_properties.bitcell_1port.port_order = ['bl', 'br', 'gnd', 'vdd', 'vpb', 'vnb', 'wl']
cell_properties.bitcell_1port.port_types = ["OUTPUT", "OUTPUT", "GROUND", "POWER", "BIAS", "BIAS", "INPUT"]
cell_properties.bitcell_1port.port_map = {'bl': 'BL',
                                          'br': 'BR',
                                          'wl': 'WL',
                                          'vdd': 'VPWR',
                                          'vnb': 'VNB',
                                          'vpb': 'VPB',
                                          'gnd': 'VGND'}

cell_properties.bitcell_1port.wl_layer = "m2"
cell_properties.bitcell_1port.bl_layer = "m1"
cell_properties.bitcell_1port.vdd_layer = "m1"
cell_properties.bitcell_1port.vdd_dir = "V"
cell_properties.bitcell_1port.gnd_layer = "m2"
cell_properties.bitcell_1port.gnd_dir = "H"

cell_properties.bitcell_2port.mirror.x = True
cell_properties.bitcell_2port.mirror.y = True
cell_properties.bitcell_2port.end_caps = True
cell_properties.bitcell_2port.port_order = ['bl0', 'br0', 'bl1', 'br1', 'wl0', 'wl1', 'vdd', 'gnd']
cell_properties.bitcell_2port.port_map = {'bl0': 'BL0',
                                          'br0': 'BR0',
                                          'bl1': 'BL1',
                                          'br1': 'BR1',
                                          'wl0': 'WL0',
                                          'wl1': 'WL1',
                                          'vdd': 'VDD',
                                          'gnd': 'GND'}
cell_properties.bitcell_1port.wl_layer = "m2"
cell_properties.bitcell_1port.vdd_layer = "m2"
cell_properties.bitcell_1port.vdd_dir = "H"
cell_properties.bitcell_1port.gnd_layer = "m2"
cell_properties.bitcell_1port.gnd_dir = "H"
cell_properties.bitcell_2port.wl_layer = "m2"
cell_properties.bitcell_2port.vdd_layer = "m1"
cell_properties.bitcell_2port.vdd_dir = "H"
cell_properties.bitcell_2port.gnd_layer = "m2"
cell_properties.bitcell_2port.gnd_dir = "H"

cell_properties.col_cap_1port_bitcell = d.cell(['bl', 'vdd', 'gnd', 'br', 'gate', 'vpb', 'vnb'],
                                             ['INPUT', 'POWER', 'GROUND', 'INPUT', 'INPUT', 'BIAS', 'BIAS'],
                                             {'bl': 'bl',
                                              'br': 'br',
                                              'vdd': 'vdd',
                                              'gnd': 'gnd',
                                              'gate': 'gate',
                                              'vnb': 'vnb',
                                              'vpb': 'vpb'})
cell_properties.col_cap_1port_bitcell.boundary_layer = "mem"

cell_properties.col_cap_1port_strap_power = d.cell(['vdd', 'vpb', 'vnb'],
                                                 ['POWER', 'BIAS', 'BIAS'],
                                                 {'vnb': 'VNB',
                                                  'vpb': 'VPB',
                                                  'vdd': 'VPWR'})
cell_properties.col_cap_1port_strap_power.boundary_layer = "mem"

cell_properties.col_cap_1port_strap_ground = d.cell(['gnd', 'vpb', 'vnb'],
                                                  ['GROUND', 'BIAS', 'BIAS'],
                                                  {'vnb': 'VNB',
                                                   'vpb': 'VPB',
                                                   'gnd': 'VGND'})
cell_properties.col_cap_1port_strap_ground.boundary_layer = "mem"

cell_properties.row_cap_1port_cell = d.cell(['vdd', 'wl'],
                                          ['POWER', 'INPUT'],
                                          {'wl': 'WL',
                                           'vdd': 'VPWR'})
cell_properties.row_cap_1port_cell.boundary_layer = "mem"

cell_properties.col_cap_2port.port_order = ['bl0', 'br0', 'bl1', 'br1', 'vdd']
cell_properties.col_cap_2port.port_map = {'bl0': 'BL0',
                                          'br0': 'BR0',
                                          'bl1': 'BL1',
                                          'br1': 'BR1',
                                          'vdd': 'VDD'}

cell_properties.row_cap_2port.port_order = ['wl0', 'wl1', 'gnd']
cell_properties.row_cap_2port.port_map = {'wl0': 'WL0',
                                          'wl1': 'WL1',
                                          'gnd': 'GND'}


cell_properties.ptx.bin_spice_models = True
cell_properties.ptx.model_is_subckt = True

cell_properties.pgate.add_implants = True

cell_properties.use_strap = True
cell_properties.strap_module = "internal"
cell_properties.strap_version = "wlstrap"

cell_properties.dff.port_order = ['D', 'Q', 'clk', 'vdd', 'gnd']
cell_properties.dff.port_map = {'D': 'D',
                                'Q': 'Q',
                                'clk': 'CLK',
                                'vdd': 'VDD',
                                'gnd': 'GND'}

cell_properties.nand2_dec.port_order = ['A', 'B', 'Z', 'vdd', 'gnd']
cell_properties.nand2_dec.port_map = {'A': 'A',
                                      'B': 'B',
                                      'Z': 'Z',
                                      'vdd': 'VDD',
                                      'gnd': 'GND'}

cell_properties.nand3_dec.port_order = ['A', 'B', 'C', 'Z', 'vdd', 'gnd']
cell_properties.nand3_dec.port_map = {'A': 'A',
                                      'B': 'B',
                                      'C': 'C',
                                      'Z': 'Z',
                                      'vdd': 'VDD',
                                      'gnd': 'GND'}

cell_properties.nand4_dec.port_order = ['A', 'B', 'C', 'D', 'Z', 'vdd', 'gnd']
cell_properties.nand4_dec.port_map = {'A': 'A',
                                      'B': 'B',
                                      'C': 'C',
                                      'D': 'D',
                                      'Z': 'Z',
                                      'vdd': 'VDD',
                                      'gnd': 'GND'}

cell_properties.sense_amp.port_order = ['bl', 'br', 'dout', 'en', 'vdd', 'gnd']
cell_properties.sense_amp.port_map = {'bl': 'BL',
                                      'br': 'BR',
                                      'dout': 'DOUT',
                                      'en': 'EN',
                                      'vdd': 'VDD',
                                      'gnd': 'GND'}

cell_properties.write_driver.port_order = ['din', 'bl', 'br', 'en', 'vdd', 'gnd']
cell_properties.write_driver.port_map = {'din': 'DIN',
                                         'bl': 'BL',
                                         'br': 'BR',
                                         'en': 'EN',
                                         'vdd': 'VDD',
                                         'gnd': 'GND'}


# You can override the GDS for custom cell using the following:
# If it is a list, the first is single port and the second is dual port.
# If it is string, it is used for both single and dual port.
cell_properties.names["dff"] = "sky130_fd_bd_sram__openram_dff"
cell_properties.names["nand2_dec"] = ["sky130_fd_bd_sram__openram_sp_nand2_dec", "sky130_fd_bd_sram__openram_dp_nand2_dec"]
cell_properties.names["nand3_dec"] = ["sky130_fd_bd_sram__openram_sp_nand3_dec", "sky130_fd_bd_sram__openram_dp_nand3_dec"]
cell_properties.names["nand4_dec"] = ["sky130_fd_bd_sram__openram_sp_nand4_dec", "sky130_fd_bd_sram__openram_dp_nand4_dec"]

cell_properties.names["bitcell_2port"] = "sky130_fd_bd_sram__openram_dp_cell"
cell_properties.names["dummy_bitcell_2port"] = "sky130_fd_bd_sram__openram_dp_cell_dummy"
cell_properties.names["replica_bitcell_2port"] = "sky130_fd_bd_sram__openram_dp_cell_replica"
cell_properties.names["col_cap_bitcell_2port"] = "sky130_fd_bd_sram__openram_dp_cell_cap_col"
cell_properties.names["row_cap_bitcell_2port"] = "sky130_fd_bd_sram__openram_dp_cell_cap_row"
cell_properties.names["sense_amp"] = "sky130_fd_bd_sram__openram_sense_amp"
cell_properties.names["write_driver"] = "sky130_fd_bd_sram__openram_write_driver"

array_row_multiple = 2
array_col_multiple = 2

###################################################
# Custom layer properties
###################################################
layer_properties = d.layer_properties()
layer_properties.hierarchical_decoder.bus_layer = "m1"
layer_properties.hierarchical_decoder.bus_directions = "nonpref"
layer_properties.hierarchical_decoder.input_layer = "li"
layer_properties.hierarchical_decoder.output_layer = "m2"
layer_properties.hierarchical_decoder.vertical_supply = True

layer_properties.hierarchical_predecode.bus_layer = "m1"
layer_properties.hierarchical_predecode.bus_directions = "nonpref"
# This is added to allow the column decoder connections on m2
layer_properties.hierarchical_predecode.bus_pitch_factor = 1.2
layer_properties.hierarchical_predecode.bus_space_factor = 1.5
layer_properties.hierarchical_predecode.input_layer = "li"
layer_properties.hierarchical_predecode.output_layer = "m2"
layer_properties.hierarchical_predecode.vertical_supply = True
layer_properties.hierarchical_predecode.force_horizontal_input_contact = True

layer_properties.bank.stack = "m2_stack"
layer_properties.bank.pitch = "m3_pitch"

layer_properties.column_mux_array.select_layer = "m3"
layer_properties.column_mux_array.bitline_layer = "m1"

layer_properties.port_address.supply_offset = True

layer_properties.port_data.enable_layer = "m1"
layer_properties.port_data.channel_route_bitlines = False

layer_properties.replica_column.even_rows = True

layer_properties.wordline_driver.vertical_supply = True

layer_properties.global_wordline_layer = "m5"


###################################################
# Discrete tx bins
###################################################
# enforce that tx sizes are within 25% of requested size after fingering.
accuracy_requirement = 0.75
nmos_bins = {
    0.15 : [0.36, 0.39, 0.42, 0.52, 0.54, 0.55, 0.58, 0.6, 0.61, 0.64, 0.65, 0.74, 0.84, 1.0, 1.26, 1.68, 2.0, 3.0, 5.0, 7.0],
    0.18 : [0.42, 0.65, 1.0, 3.0, 5.0, 7.0],
    0.25 : [0.65, 1.0, 3.0, 5.0, 7.0],
    0.5  : [0.42, 0.55, 0.65, 1.0, 3.0, 5.0, 7.0],
    1.0  : [0.42, 0.65, 1.0, 3.0, 5.0, 7.0],
    2.0  : [0.42, 0.65, 1.0, 3.0, 5.0, 7.0],
    4.0  : [0.42, 0.65, 1.0, 3.0, 5.0, 7.0],
    8.0  : [0.42, 0.65, 1.0, 3.0, 5.0, 7.0],
    20.0 : [0.42, 0.65, 1.0, 3.0, 5.0, 7.0]
}

pmos_bins = {
    0.15 : [0.42, 0.55, 0.64, 0.84, 1.0, 1.12, 1.26, 1.65, 1.68, 2.0, 3.0, 5.0, 7.0],
    1.0  : [0.42, 0.55, 1.0, 3.0, 5.0, 7.0],
    2.0  : [0.42, 0.55, 1.0, 3.0, 5.0, 7.0],
    4.0  : [0.42, 0.55, 1.0, 3.0, 5.0, 7.0],
    8.0  : [0.42, 0.55, 1.0, 3.0, 5.0, 7.0],
    0.17 : [0.42, 0.55, 0.64, 0.84, 1.0, 1.12],
    0.18 : [0.42, 0.55, 0.64, 0.84, 1.0, 1.12, 1.26, 1.68, 2.0, 3.0, 5.0, 7.0],
    0.25 : [1.0, 3.0, 5.0, 7.0],
    0.5  : [0.42, 0.55, 1.0, 3.0, 5.0, 7.0],
    20.0   : [0.42]
}
###################################################
# GDS file info
###################################################
GDS = {}
# gds units
# From http://www.cnf.cornell.edu/cnf_spie9.html: "The first
# is the size of a database unit in user units. The second is the size
# of a database unit in meters.  For example, if your library was
# created with the default units (user unit = 1 um and 1000 database
# units per user unit), then the first number would be 0.001 and the
# second number would be 10-9. Typically, the first number is less than
# 1, since you use more than 1 database unit per user unit. To
# calculate the size of a user unit in meters, divide the second number
# by the first."
GDS["unit"] = (0.001, 1e-9)
#GDS["unit"]=(0.001, 1e-6)

###################################################
# Interconnect stacks
###################################################

poly_stack = ("poly", "contact", "li")
active_stack = ("active", "contact", "li")
li_stack = ("li", "mcon", "m1")
m1_stack = ("m1", "via1", "m2")
m2_stack = ("m2", "via2", "m3")
m3_stack = ("m3", "via3", "m4")
m4_stack = ("m4", "via4", "m5")

layer_indices = {"poly": 0,
                 "active": 0,
                 "nwell": 0,
                 "li": 1,
                 "m1": 2,
                 "m2": 3,
                 "m3": 4,
                 "m4": 5,
                 "m5": 6}

# The FEOL stacks get us up to m1
feol_stacks = [poly_stack,
               active_stack,
               li_stack]

# The BEOL stacks are m1 and up
beol_stacks = [m1_stack,
               m2_stack,
               m3_stack,
               m4_stack]

layer_stacks = feol_stacks + beol_stacks

preferred_directions = {"poly": "V",
                        "active": "V",
                        "li": "V",
                        "m1": "H",
                        "m2": "V",
                        "m3": "H",
                        "m4": "V",
                        "m5": "H"}

###################################################
# GDS Layer Map
###################################################


layer = {}
layer["active"]  = (65, 20) # diff
layer["activep"]  = (65, 20) # diff
layer["tap"]  = (65, 44) # tap
layer["pwellp"] = (122,16)
layer["nwell"]   = (64, 20) # nwell
layer["dnwell"]   = (64,18)
layer["nimplant"]= (93, 44) # nsdm
layer["pimplant"]= (94, 20) # psdm
layer["vtl"]     = (125, 44) # lvtn
layer["vth"]     = (78, 44) # hvtp (pmos only)
layer["thkox"]   = (8, 0)
layer["poly"]    = (66, 20)
layer["contact"] = (66, 44) # licon1
layer["npc"]   = (95, 20) # npc (nitride cut)
layer["li"]     = (67, 20) # active li1
layer["mcon"]    = (67, 44) # mcon
layer["m1"]  = (68, 20) # met1
layer["m1p"] = (68, 5) # met1 pin
layer["via1"]    = (68, 44) # via1
layer["m2"]  = (69, 20) # met2
layer["m2p"] = (69, 5) # met2 pin
layer["via2"]    = (69, 44) # via2
layer["m3"]  = (70, 20) # met3
layer["m3p"] = (70, 5) # met3 pin
layer["via3"]    = (70, 44) # via3
layer["m4"]  = (71, 20) # met4
layer["m4p"] = (71, 5) # met4 pin
layer["via4"]    = (71, 44) # via4
layer["m5"]  = (72, 20) # met5
layer["m5p"] = (72, 5) # met5 pin
layer["boundary"]= (235, 4)
# specific boundary type to define standard cell regions for DRC
layer["stdc"] = (81, 4)
layer["mem"] = (81, 2)
# Not an official sky130 layer, but useful for router debug infos
layer["text"]= (234, 5)
# Excpected value according to sky130A tech file
# If calibre is enabled, these will be swapped below
#pin_purpose = 5
label_purpose = 5
#label_purpose = 16
#pin_purpose = 16
#label_purpose = 5

# pin_read purposes
special_purposes = {layer["nwell"][0]: [layer["nwell"][1], 5, 59, 16]}
#layer_override = {"VNB\x00": ["pwell",122]}
layer_override = {"VNB": layer["pwellp"]}
layer_override_name = {"VNB": "pwellp"}
layer_override_purpose = {122: (64, 59)}
# Layer names for external PDKs
layer_names = {}
layer_names["active"]  = "diff"
layer_names["activep"]  = "diff"
layer_names["tap"]     = "tap"
layer_names["pwellp"] = "pwellp"
layer_names["nwell"]   = "nwell"
layer_names["dnwell"]   = "dnwell"
layer_names["nimplant"]= "nsdm"
layer_names["pimplant"]= "psdm"
layer_names["vtl"]     = "lvtn"
layer_names["vth"]     = "hvtp"
layer_names["thkox"]   = "thkox"
layer_names["poly"]    = "poly"
layer_names["contact"] = "licon1"
layer_names["li"]      = "li1"
layer_names["mcon"]    = "mcon"
layer_names["m1"]      = "met1"
layer_names["m1p"]      = "met1"
layer_names["via1"]    = "via"
layer_names["m2"]      = "met2"
layer_names["m2p"]      = "met2"
layer_names["via2"]    = "via2"
layer_names["m3"]      = "met3"
layer_names["m3p"]      = "met3"
layer_names["via3"]    = "via3"
layer_names["m4"]      = "met4"
layer_names["m4p"]      = "met4"
layer_names["via4"]    = "via4"
layer_names["m5p"]      = "met5"
layer_names["boundary"]= "boundary"
layer_names["stdc"]    = "areaid.standardc"
layer_names["mem"]     = "areaid.core"
layer_names["text"]    = "text"


###################################################
# DRC/LVS Rules Setup
###################################################

# technology parameter
parameter={}
# difftap.2b
parameter["min_tx_size"] = 0.150
parameter["beta"] = 3

parameter["6T_inv_nmos_size"] = 0.205
parameter["6T_inv_pmos_size"] = 0.09
parameter["6T_access_size"] = 0.135

drc = d.design_rules("sky130")

# grid size
drc["grid"] = 0.005

#DRC/LVS test set_up
# Switching between calibre and magic can be useful for development,
# it eventually should be deleted.
NDA_PDK_ROOT = os.environ.get("NDA_PDK_ROOT", False)
use_calibre = bool(NDA_PDK_ROOT)
use_calibre = False
use_klayout = False
if use_calibre:
    # Correct order according to s8
    pin_purpose = 16
    label_purpose = 5

    drc["drc_rules"] = NDA_PDK_ROOT + "/DRC/Calibre/s8_drcRules"
    drc["lvs_rules"] = NDA_PDK_ROOT + "/LVS/Calibre/lvs_s8_opts"
    drc["xrc_rules"] = NDA_PDK_ROOT + "/PEX/xRC/extLvsRules_s8_5lm"
    drc["layer_map"] = NDA_PDK_ROOT + "/VirtuosoOA/libs/technology_library/s8phirs_10r.layermap"

# minwidth_tx with contact (no dog bone transistors)
# difftap.2b
drc["minwidth_tx"] = 0.360
drc["minlength_channel"] = 0.150

drc["pwell_to_nwell"] = 0
# nwell.1 Minimum width of nwell/pwell
drc.add_layer("nwell",
              width=0.840,
              spacing=1.270)

# poly.1a Minimum width of poly
# poly.2 Minimum spacing of poly AND active
drc.add_layer("poly",
              width=0.150,
              spacing=0.210)
# poly.8
drc["poly_extend_active"] = 0.13
# Not a rule
drc["poly_to_contact"] = 0
# poly.7 Minimum enclosure of active around gate
drc["active_enclose_gate"] = 0.075
# poly.4 Minimum spacing of field poly to active
drc["poly_to_active"] = 0.075
# poly.2 Minimum spacing of field poly
drc["poly_to_field_poly"] = 0.210

# difftap.1 Minimum width of active
# difftap.3 Minimum spacing of active
drc.add_layer("active",
              width=0.150,
              spacing=0.270)
# difftap.8
drc.add_enclosure("nwell",
                  layer="active",
                  enclosure=0.18,
                  extension=0.18)

# nsd/psd.5a
drc.add_enclosure("implant",
                  layer="active",
                  enclosure=0.125)

# Same as active enclosure?
drc["implant_to_contact"] = 0.070
# nsd/psd.1 nsd/psd.2
drc.add_layer("implant",
              width=0.380,
              spacing=0.380,
              area=0.265)

# licon.1, licon.2
drc.add_layer("contact",
              width=0.170,
              spacing=0.170)
# licon.5c (0.06 extension), (licon.7 for extension)
drc.add_enclosure("active",
                  layer="contact",
                  enclosure=0.040,
                  extension=0.060)
# licon.7
drc["tap_extend_contact"] = 0.120

# licon.8 Minimum enclosure of poly around contact
drc.add_enclosure("poly",
                  layer="contact",
                  enclosure=0.08,
                  extension=0.08)
# licon.11a
drc["active_contact_to_gate"] = 0.050
# npc.4 > licon.14 0.19 > licon.11a
drc["poly_contact_to_gate"] = 0.270
# licon.15
drc["npc_enclose_poly"] = 0.1

# li.1, li.3
drc.add_layer("li",
              width=0.170,
              spacing=0.170)

# licon.5
drc.add_enclosure("li",
                  layer="contact",
                  enclosure=0,
                  extension=0.080)

drc.add_enclosure("li",
                  layer="mcon",
                  enclosure=0,
                  extension=0.080)
# mcon.1, mcon.2
drc.add_layer("mcon",
              width=0.170,
              spacing=0.210)

# m1.1 Minimum width of metal1
# m1.2 Minimum spacing of metal1
# m1.6 Minimum area of metal1
drc.add_layer("m1",
              width=0.140,
              spacing=0.140,
              area=0.083)
# m1.4 Minimum enclosure of metal1
# m1.5 Minimum enclosure around contact on two opposite sides
drc.add_enclosure("m1",
                  layer="mcon",
                  enclosure=0.030,
                  extension=0.060)
# via.4a Minimum enclosure around via1
# via.5a Minimum enclosure around via1 on two opposite sides
drc.add_enclosure("m1",
                  layer="via1",
                  enclosure=0.055,
                  extension=0.085)

# via.1a Minimum width of via1
# via.2 Minimum spacing of via1
drc.add_layer("via1",
              width=0.150,
              spacing=0.170)

# m2.1 Minimum width of intermediate metal
# m2.2 Minimum spacing of intermediate metal
# m2.6 Minimum area of metal2
drc.add_layer("m2",
              width=0.140,
              spacing=0.140,
              area=0.0676)
# m2.4 Minimum enclosure around via1
# m2.5 Minimum enclosure around via1 on two opposite sides
drc.add_enclosure("m2",
                  layer="via1",
                  enclosure=0.055,
                  extension=0.085)
# via2.4 Minimum enclosure around via2
# via2.5 Minimum enclosure around via2 on two opposite sides
drc.add_enclosure("m2",
                  layer="via2",
                  enclosure=0.040,
                  extension=0.085)

# via2.1a Minimum width of Via2
# via2.2  Minimum spacing of Via2
drc.add_layer("via2",
              width=0.200,
              spacing=0.200)

# m3.1 Minimum width of metal3
# m3.2 Minimum spacing of metal3
# m3.6 Minimum area of metal3
drc.add_layer("m3",
              width=0.300,
              spacing=0.300,
              area=0.240)
# m3.4 Minimum enclosure around via2
drc.add_enclosure("m3",
                  layer="via2",
                  enclosure=0.065)
# via3.4 Minimum enclosure around via3
# via3.5 Minimum enclosure around via3 on two opposite sides
drc.add_enclosure("m3",
                  layer="via3",
                  enclosure=0.060,
                  extension=0.090)

# via3.1 Minimum width of Via3
# via3.2 Minimum spacing of Via3
drc.add_layer("via3",
              width=0.200,
              spacing=0.200)

# m4.1 Minimum width of metal4
# m4.2 Minimum spacing of metal4
# m4.7 Minimum area of metal4
drc.add_layer("m4",
              width=0.300,
              spacing=0.300,
              area=0.240)
# m4.3 Minimum enclosure around via3
drc.add_enclosure("m4",
                  layer="via3",
                  enclosure=0.065)
# FIXME: Wrong rule m4.3 Minimum enclosure around via3
drc.add_enclosure("m4",
                  layer="via4",
                  enclosure=0.060)


# via4.1 Minimum width of Via4
# via4.2 Minimum spacing of Via4
drc.add_layer("via4",
              width=0.800,
              spacing=0.800)

# FIXME: Wrong rules
# m5.1 Minimum width of metal5
# m5.2 Minimum spacing of metal5
# m5.7 Minimum area of metal5
drc.add_layer("m5",
              width=1.600,
              spacing=1.600,
              area=4.000)
# m5.3 Minimum enclosure around via4
drc.add_enclosure("m5",
                  layer="via4",
                  enclosure=0.310)



# Metal 5-10 are ommitted

###################################################
# Spice Simulation Parameters
###################################################

# spice info
spice = {}
spice["nmos"] = "sky130_fd_pr__nfet_01v8"
spice["pmos"] = "sky130_fd_pr__pfet_01v8"
spice["power"]="vccd1"
spice["ground"]="vssd1"

# whether or not the device model is actually a subckt
spice["device_prefix"] = "X"

spice["fet_libraries"] = { "TT": [[os.environ.get("SPICE_MODEL_DIR") + "/sky130.lib.spice", "tt"]],
                           "SS": [[os.environ.get("SPICE_MODEL_DIR") + "/sky130.lib.spice", "ss"]],
                           "FF": [[os.environ.get("SPICE_MODEL_DIR") + "/sky130.lib.spice", "ff"]],
                           "SF": [[os.environ.get("SPICE_MODEL_DIR") + "/sky130.lib.spice", "sf"]],
                           "FS": [[os.environ.get("SPICE_MODEL_DIR") + "/sky130.lib.spice", "fs"]] }

# spice stimulus related variables
spice["feasible_period"] = 10        # estimated feasible period in ns
spice["supply_voltages"] = [1.7, 1.8, 1.9] # Supply voltage corners in [Volts]
spice["nom_supply_voltage"] = 1.8    # Nominal supply voltage in [Volts]
spice["rise_time"] = 0.005           # rise time in [Nano-seconds]
spice["fall_time"] = 0.005           # fall time in [Nano-seconds]
spice["temperatures"] = [0, 25, 100] # Temperature corners (celcius)
spice["nom_temperature"] = 25        # Nominal temperature (celcius)

# analytical delay parameters
spice["nom_threshold"] = 0.49     # Typical Threshold voltage in Volts
spice["wire_unit_r"] = 0.125     # Unit wire resistance in ohms/square
spice["wire_unit_c"] = 0.134     # Unit wire capacitance ff/um^2
spice["min_tx_drain_c"] = 0.7    # Minimum transistor drain capacitance in ff
spice["min_tx_gate_c"] = 0.2     # Minimum transistor gate capacitance in ff
spice["dff_setup"] = 102.5391    # DFF setup time in ps
spice["dff_hold"] = -56          # DFF hold time in ps
spice["dff_in_cap"] = 6.89       # Input capacitance (D) [Femto-farad]
spice["dff_out_cap"] = 6.89      # Output capacitance (Q) [Femto-farad]

# analytical power parameters, many values are temporary
spice["bitcell_leakage"] = 1     # Leakage power of a single bitcell in nW
spice["inv_leakage"] = 1         # Leakage power of inverter in nW
spice["nand2_leakage"] = 1       # Leakage power of 2-input nand in nW
spice["nand3_leakage"] = 1       # Leakage power of 3-input nand in nW
spice["nor2_leakage"] = 1        # Leakage power of 2-input nor in nW
spice["dff_leakage"] = 1         # Leakage power of flop in nW

spice["default_event_frequency"] = 100     # Default event activity of every gate. MHz

# Parameters related to sense amp enable timing and delay chain/RBL sizing
parameter["le_tau"] = 2.25                  # In pico-seconds.
parameter["cap_relative_per_ff"] = 7.5      # Units of Relative Capacitance/ Femto-Farad
parameter["dff_clk_cin"] = 30.6             # relative capacitance
parameter["6tcell_wl_cin"] = 3              # relative capacitance
parameter["min_inv_para_delay"] = 2.4       # Tau delay units
parameter["sa_en_pmos_size"] = 0.72         # micro-meters
parameter["sa_en_nmos_size"] = 0.27         # micro-meters
parameter["sa_inv_pmos_size"] = 0.54        # micro-meters
parameter["sa_inv_nmos_size"] = 0.27        # micro-meters
parameter["bitcell_drain_cap"] = 0.1        # In Femto-Farad, approximation of drain capacitance

###################################################
# Technology Tool Preferences
###################################################

if use_calibre:
    drc_name = "calibre"
    lvs_name = "calibre"
    pex_name = "calibre"
elif use_klayout:
    drc_name = "klayout"
    lvs_name = "klayout"
    pex_name = "klayout"
else:
    drc_name = "magic"
    lvs_name = "netgen"
    pex_name = "magic"


# This is used by uniqify to not rename the library cells
library_prefix_name = "sky130_fd_bd_sram__"
# List of cells to skip running DRC/LVS on directly
# This will look for a maglef file and copy it over the mag file
# before DRC after extraction

# gds flatglob sky130_fd_bd_sram__openram_sp_cell_opt1a_cell
# gds flatglob sky130_fd_bd_sram__openram_sp_cell_opt1a_replica_ce
# gds flatglob sky130_fd_bd_sram__openram_sp_cell_opt1_replica_cell
# gds flatglob sky130_fd_bd_sram__openram_sp_cell_opt1_replica_ce
# gds flatglob sky130_fd_bd_sram__openram_sp_cell_opt1_replica_cell
# gds flatglob sky130_fd_bd_sram__openram_sp_cell_opt1a_cell
# gds flatglob sky130_fd_bd_sram__sram_sp_cell_fom_serifs

flatglob = ["*_?mos_m*",
            "sky130_fd_bd_sram__sram_sp_cell_fom_serifs",

            "sky130_fd_bd_sram__sram_sp_cell",
            "sky130_fd_bd_sram__openram_sp_cell_opt1_replica_cell",
            "sky130_fd_bd_sram__openram_sp_cell_opt1a_replica_cell",

            "sky130_fd_bd_sram__sram_sp_cell_opt1_ce",
            "sky130_fd_bd_sram__openram_sp_cell_opt1_replica_ce",
            "sky130_fd_bd_sram__openram_sp_cell_opt1a_replica_ce",
            "sky130_fd_bd_sram__sram_sp_wlstrap_ce",
            "sky130_fd_bd_sram__sram_sp_wlstrap_p_ce"]

blackbox_cells = ["sky130_fd_bd_sram__openram_dp_cell",
                  "sky130_fd_bd_sram__openram_dp_cell_dummy",
                  "sky130_fd_bd_sram__openram_dp_cell_replica",

                  "sky130_fd_bd_sram__sram_sp_cell_opt1a",
                  "sky130_fd_bd_sram__openram_sp_cell_opt1a_dummy",
                  "sky130_fd_bd_sram__sram_sp_cell_opt1_ce",
                  "sky130_fd_bd_sram__sram_sp_cell_opt1",
                  "sky130_fd_bd_sram__openram_sp_cell_opt1_replica",
                  "sky130_fd_bd_sram__openram_sp_cell_opt1a_replica",
                  "sky130_fd_bd_sram__sram_sp_colend",
                  "sky130_fd_bd_sram__sram_sp_colend_cent",
                  "sky130_fd_bd_sram__sram_sp_colend_p_cent",
                  "sky130_fd_bd_sram__sram_sp_colenda",
                  "sky130_fd_bd_sram__sram_sp_colenda_cent",
                  "sky130_fd_bd_sram__sram_sp_colenda_p_cent",
                  "sky130_fd_bd_sram__sram_sp_rowend",
                  "sky130_fd_bd_sram__sram_sp_rowenda",
                  "sky130_fd_bd_sram__openram_sp_rowend_replica",
                  "sky130_fd_bd_sram__openram_sp_rowenda_replica",
                  "sky130_fd_bd_sram__sram_sp_corner",
                  "sky130_fd_bd_sram__sram_sp_cornera",
                  "sky130_fd_bd_sram__sram_sp_cornerb",
                  "sky130_fd_bd_sram__sram_sp_wlstrapa",
                  "sky130_fd_bd_sram__sram_sp_wlstrap_ce",
                  "sky130_fd_bd_sram__sram_sp_wlstrap",
                  "sky130_fd_bd_sram__sram_sp_wlstrap_p_ce",
                  "sky130_fd_bd_sram__sram_sp_wlstrap_p"]
