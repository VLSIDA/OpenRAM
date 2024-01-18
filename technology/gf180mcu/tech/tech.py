# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os
from openram import drc as d

"""
File containing the process technology parameters for Global Foundaries 180nm
"""

###################################################
# Custom modules
###################################################

# This uses the default classes to instantiate module from
# '$OPENRAM_HOME/compiler/modules'.
# Using tech_modules['cellname'] you can override each class by providing a custom
# implementation in '$OPENRAM_TECHDIR/modules/'
# For example: tech_modules['contact'] = 'contact_scn4m'
tech_modules = d.module_type()

tech_modules["bitcell_1port"] = "gf180_bitcell"
tech_modules["nand2_dec"] = "nand2_dec"

###################################################
# Custom cell properties
###################################################
cell_properties = d.cell_properties()

# is there a better way to tell if the user overrode the port order than this?
# this is needed to correctly create the bitcell_pins list in the bitcell_base_array
cell_properties.override_bitcell_1port_order = True
cell_properties.bitcell_1port.port_order = ['bl', 'br', 'gnd', 'vdd', 'vpb', 'vnb', 'wl']
cell_properties.bitcell_1port.port_types = ["OUTPUT", "OUTPUT", "GROUND", "POWER", "BIAS", "BIAS", "INPUT"]
cell_properties.bitcell_1port.port_map = {'bl': 'BL',
                                          'br': 'BR',
                                          'wl': 'WL',
                                          'vdd': 'VDD',
                                          'vnb': 'pwell',
                                          'vpb': 'nwell',
                                          'gnd': 'GND'}

cell_properties.bitcell_1port.wl_layer = "m3"
cell_properties.bitcell_1port.bl_layer = "m2"
cell_properties.bitcell_1port.vdd_layer = "m1"
cell_properties.bitcell_1port.gnd_layer = "m1"

cell_properties.nand2_dec.port_order = ['A', 'B', 'Z', 'vdd', 'gnd']
cell_properties.nand2_dec.port_map = {'A': 'A',
                                      'B': 'B',
                                      'Z': 'Z',
                                      'vdd': 'VDD',
                                      'gnd': 'GND'}


cell_properties.ptx.model_is_subckt = True

cell_properties.strap_placement = 8     # this means strap cell gets placed after every 8 bitcells

cell_properties.names["nand2_dec"] = ["gf180mcu_3v3__nand2_1_dec"]

###################################################
# Custom layer properties
###################################################
layer_properties = d.layer_properties()

###################################################
# GDS file info
###################################################
GDS={}
# gds units
# From http://www.cnf.cornell.edu/cnf_spie9.html: "The first
#is the size of a database unit in user units. The second is the size
#of a database unit in meters.  For example, if your library was
#created with the default units (user unit = 1 m and 1000 database
#units per user unit), then the first number would be 0.001 and the
#second number would be 10-9. Typically, the first number is less than
#1, since you use more than 1 database unit per user unit. To
#calculate the size of a user unit in meters, divide the second number
#by the first."
GDS["unit"]=(0.001,1e-6)
# default label zoom
GDS["zoom"] = 0.5

###################################################
# Interconnect stacks
###################################################

poly_stack = ("poly", "contact", "m1")
active_stack = ("active", "contact", "m1")
m1_stack = ("m1", "via1", "m2")
m2_stack = ("m2", "via2", "m3")
m3_stack = ("m3", "via3", "m4")
m4_stack = ("m4", "via4", "m5")

lef_rom_interconnect = ["m1", "m2", "m3", "m4", "m5"]

layer_indices = {"poly": 0,
                 "active": 0,
                 "nwell": 0,
                 "pwell": 0,
                 "m1": 1,
                 "m2": 2,
                 "m3": 3,
                 "m4": 4,
                 "m5": 5}

# The FEOL stacks get us up to m1
feol_stacks = [poly_stack,
               active_stack]

# The BEOL stacks are m1 and up
beol_stacks = [m1_stack,
               m2_stack,
               m3_stack,
               m4_stack]

layer_stacks = feol_stacks + beol_stacks

preferred_directions = {"poly": "V",
                        "active": "V",
                        "m1": "V",
                        "m2": "H",
                        "m3": "V",
                        "m4": "H",
                        "m5": "V"}

###################################################
# Power grid
###################################################
# Use M3/M4
power_grid = m4_stack

###################################################
##GDS Layer Map
###################################################

# create the GDS layer map
layer={}
layer["pwell"]          = (204, 0)
layer["nwell"]          = (21, 0)
layer["dnwell"]         = (12, 0)
layer["active"]         = (22, 0)
layer["pimplant"]       = (31, 0)
layer["nimplant"]       = (32, 0)
layer["poly"]           = (30, 0)
layer["contact"]        = (33, 0)
layer["m1"]             = (34, 0)
layer["via1"]           = (35, 0)
layer["m2"]             = (36, 0)
layer["via2"]           = (38, 0)
layer["m3"]             = (42, 0)
layer["via3"]           = (40, 0)
layer["m4"]             = (46, 0)
layer["via4"]           = (41, 0)
layer["m5"]             = (81, 0)
# Not an official layer
layer["text"]           = (234, 5)
layer["mem"]            = (108, 5)
layer["boundary"]       = (0, 0)

label_purpose = 10
#use_purpose = {}

# Layer names for external PDKs
layer_names = {}
layer_names["active"]  = "active"
layer_names["pwell"]   = "pwell"
layer_names["nwell"]   = "nwell"
layer_names["dnwell"]   = "dnwell"
layer_names["nimplant"]= "nimplant"
layer_names["pimplant"]= "pimplant"
layer_names["poly"]    = "poly"
layer_names["contact"] = "contact"
layer_names["m1"]      = "metal1"
layer_names["via1"]    = "via1"
layer_names["m2"]      = "metal2"
layer_names["via2"]    = "via2"
layer_names["m3"]      = "metal3"
layer_names["via3"]    = "via3"
layer_names["m4"]      = "metal4"
layer_names["via4"]    = "via4"
layer_names["m5"]      = "metal5"
layer_names["text"]    = "text"
layer_names["mem"]     = "SramCore"
layer_names["boundary"]= "boundary"

###################################################
# DRC/LVS Rules Setup
###################################################

# technology parameter
parameter={}

parameter["min_tx_size"] = 0.250
parameter["beta"] = 3

parameter["6T_inv_nmos_size"] = 0.6
parameter["6T_inv_pmos_size"] = 0.95
parameter["6T_access_size"] = 0.6
drc = d.design_rules("gf180")

# grid size
drc["grid"] = 0.005

# minwidth_tx with contact (no dog bone transistors)
drc["minwidth_tx"] = 0.57
# PL.2 Min gate width/channel length for 3V3 pmos
drc["minlength_channel"] = 0.28

drc["minlength_channel_pmos"] = 0.55
drc["minlength_channel_nmos"] = 0.7

drc["pwell_to_nwell"] = 0 # assuming same potential

drc.add_layer("nwell",
              width=0.86,
              spacing=0.6)

drc.add_layer("pwell",
              width=0.74, # 0.6 for 3.3v
              spacing=0.86) # equal potential

# PL.1 minwidth of interconnect poly 3v3
# PL.3a poly spacing 3v3
drc.add_layer("poly",
              width=0.28,
              spacing=0.24)

drc["poly_extend_active"] = 0.22

drc["poly_to_contact"] = 0

#drc["active_enclose_gate"] = 0.075

drc["poly_to_active"] = 0.1

#drc["poly_to_field_poly"] = 0.210

#
# DF.1a - minwidth of active (3v3)
# min space of tap to diff across butted junction
# DF.9 - minarea of active area=0.2025
drc.add_layer("active",
              width=0.22,
              spacing=0.33)

drc.add_enclosure("dnwell",
                layer="pwell",
                enclosure=2.5,
                extension=2.5)

drc.add_enclosure("nwell",
                  layer="active",
                  enclosure=0.43,
                  extension=0.6)

drc.add_enclosure("pwell",
                  layer="active",
                  enclosure=0.43,
                  extension=0.6)

drc.add_enclosure("implant",
                  layer="active",
                  enclosure=0.125)

# Same as active enclosure?
#drc["implant_to_contact"] = 0.070

drc.add_layer("implant",
              width=0.4,
              spacing=0.4,
              area=0.35)

drc.add_layer("contact",
              width=0.22,
              spacing=0.25)
# CO.4 - active enclosure of contact
# extension is not a true drc rule, used to extend active to reach active min area
drc.add_enclosure("active",
                  layer="contact",
                  enclosure=0.07,
                  extension=0.175)

drc.add_enclosure("poly",
                  layer="contact",
                  enclosure=0.07,
                  extension=0.07)

drc["active_contact_to_gate"] = 0.15

drc["poly_contact_to_gate"] = 0.165

#drc["npc_enclose_poly"] = 0.1

# M1.1 - width
# M1.2a - space
# M1.3 - area
drc.add_layer("m1",
              width=0.26,
              spacing=0.23)

drc.add_enclosure("m1",
                  layer="contact",
                  enclosure=0,
                  extension=0.205)

drc.add_enclosure("m1",
                  layer="via1",
                  enclosure=0,
                  extension=0.15)

drc.add_layer("via1",
              width=0.26,
              spacing=0.26)

drc.add_layer("m2",
              width=0.28,
              spacing=0.28,
              area=0.1444)

drc.add_enclosure("m2",
                  layer="via1",
                  enclosure=0.06,
                  extension=0.06)

drc.add_enclosure("m2",
                  layer="via2",
                  enclosure=0.06,
                  extension=0.06)

drc.add_layer("via2",
              width=0.26,
              spacing=0.26)

drc.add_layer("m3",
              width=0.28,
              spacing=0.28,
              area=0.1444)

drc.add_enclosure("m3",
                  layer="via2",
                  enclosure=0.06)


drc.add_enclosure("m3",
                  layer="via3",
                  enclosure=0.06,
                  extension=0.06)

drc.add_layer("via3",
              width=0.26,
              spacing=0.26)

drc.add_layer("m4",
              width=0.28,
              spacing=0.28,
              area=0.1444)

drc.add_enclosure("m4",
                  layer="via3",
                  enclosure=0.06)

drc.add_enclosure("m4",
                  layer="via4",
                  enclosure=0.06)

drc.add_layer("via4",
              width=0.26,
              spacing=0.26)

# Magic wants 0.36um width but PDK says 0.28
drc.add_layer("m5",
              width=0.36,
              spacing=0.28,
              area=0.1444)

drc.add_enclosure("m5",
                  layer="via4",
                  enclosure=0.06)

drc.add_enclosure("m5",
                  layer="via5",
                  enclosure=0.06)

drc.add_layer("via5",
              width=0.26,
              spacing=0.26)

# m5.1 Minimum width of metal5
# m5.2 Minimum spacing of metal5
# m5.7 Minimum area of metal5
#drc.add_layer("m5",
#              width=1.600,
#              spacing=1.600,
#              area=4.000)
# m5.3 Minimum enclosure around via4
#drc.add_enclosure("m5",
#                  layer="via4",
#                  enclosure=0.310)



# Metal 5-10 are ommitted

###################################################
# Spice Simulation Parameters
###################################################

# spice info
spice = {}
spice["nmos"] = "nfet_03v3"
spice["pmos"] = "pfet_03v3"
spice["power"]="vccd1"
spice["ground"]="vssd1"

spice["fet_libraries"] = {"TT": [[os.environ.get("SPICE_MODEL_DIR") + "/sm141064.ngspice", "typical"]]}

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

#if use_calibre:
#    drc_name = "calibre"
#    lvs_name = "calibre"
#    pex_name = "calibre"
#if use_klayout:
#    drc_name = "klayout"
#    lvs_name = "klayout"
#    pex_name = "klayout"
#else:
drc_name = "magic"
lvs_name = "netgen"
pex_name = "magic"


flatglob = ["*_?mos_m*"]

ignore_drc_lvs_on = ["wl_strap"]
