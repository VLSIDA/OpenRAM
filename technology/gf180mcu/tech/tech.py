# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os
import drc as d
#from drc.design_rules import design_rules
#from drc.module_type import module_type
#from drc.custom_cell_properties import cell_properties
#from drc.custom_layer_properties import layer_properties

"""
File containing the process technology parameters for SCMOS 4m, 0.35um
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

###################################################
# Custom cell properties
###################################################
cell_properties = d.cell_properties()

###################################################
# Custom cell properties
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

layer_indices = {"poly": 0,
                 "active": 0,
                 "m1": 1,
                 "m2": 2,
                 "m3": 3,
                 "m4": 4}

# The FEOL stacks get us up to m1
feol_stacks = [poly_stack,
               active_stack]

# The BEOL stacks are m1 and up
beol_stacks = [m1_stack,
               m2_stack,
               m3_stack]

layer_stacks = feol_stacks + beol_stacks

preferred_directions = {"poly": "V",
                        "active": "V",
                        "m1": "H",
                        "m2": "V",
                        "m3": "H",
                        "m4": "V"}

###################################################
# Power grid
###################################################
# Use M3/M4
power_grid = m3_stack

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

drc["minwidth_tx"] = 0.28
#drc["minlength_channel"] = 0.150

drc["pwell_to_nwell"] = 0 # assuming same potential

drc.add_layer("nwell",
              width=0.86,
              spacing=0.6)

drc.add_layer("pwell",
              width=0.74, # 0.6 for 1.5v
              spacing=0.86) # equal potential 1.7 otherwise

drc.add_layer("poly",
              width=0.18,
              spacing=0.24)
# poly.8
#drc["poly_extend_active"] = 0.13
# Not a rule
#drc["poly_to_contact"] = 0
# poly.7 Minimum enclosure of active around gate
#drc["active_enclose_gate"] = 0.075
# poly.4 Minimum spacing of field poly to active
#drc["poly_to_active"] = 0.075
# poly.2 Minimum spacing of field poly
#drc["poly_to_field_poly"] = 0.210

drc.add_layer("active",
              width=0.22,
              spacing=0.280)

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
# nsd/psd.5a
#drc.add_enclosure("implant",
#                  layer="active",
#                  enclosure=0.125)

# Same as active enclosure?
#drc["implant_to_contact"] = 0.070
# nsd/psd.1 nsd/psd.2
#drc.add_layer("implant",
#              width=0.380,
#              spacing=0.380,
#              area=0.265)

# licon.1, licon.2
#drc.add_layer("contact",
#              width=0.170,
#              spacing=0.170)
# licon.5c (0.06 extension), (licon.7 for extension)
#drc.add_enclosure("active",
#                  layer="contact",
#                  enclosure=0.040,
#                  extension=0.060)
# licon.7
#drc["tap_extend_contact"] = 0.120

# licon.8 Minimum enclosure of poly around contact
#drc.add_enclosure("poly",
#                  layer="contact",
#                  enclosure=0.08,
#                  extension=0.08)
# licon.11a
#drc["active_contact_to_gate"] = 0.050
# npc.4 > licon.14 0.19 > licon.11a
#drc["poly_contact_to_gate"] = 0.270
# licon.15
#drc["npc_enclose_poly"] = 0.1

# li.1, li.3
#drc.add_layer("li",
#              width=0.170,
#              spacing=0.170)

# licon.5
#drc.add_enclosure("li",
#                  layer="contact",
#                  enclosure=0,
#                  extension=0.080)

#drc.add_enclosure("li",
#                  layer="mcon",
#                  enclosure=0,
#                  extension=0.080)
# mcon.1, mcon.2
#drc.add_layer("mcon",
#              width=0.170,
#              spacing=0.210)

drc.add_layer("m1",
              width=0.23,
              spacing=0.23,
              area=0.1444)
# m1.4 Minimum enclosure of metal1
# m1.5 Minimum enclosure around contact on two opposite sides
#drc.add_enclosure("m1",
#                  layer="mcon",
#                  enclosure=0.030,
#                  extension=0.060)
# via.4a Minimum enclosure around via1
# via.5a Minimum enclosure around via1 on two opposite sides
#drc.add_enclosure("m1",
#                  layer="via1",
#                  enclosure=0.055,
#                  extension=0.085)

# via.1a Minimum width of via1
# via.2 Minimum spacing of via1
#drc.add_layer("via1",
#              width=0.150,
#              spacing=0.170)

drc.add_layer("m2",
              width=0.28,
              spacing=0.28,
              area=0.1444)
# m2.4 Minimum enclosure around via1
# m2.5 Minimum enclosure around via1 on two opposite sides
#drc.add_enclosure("m2",
#                  layer="via1",
#                  enclosure=0.055,
#                  extension=0.085)
# via2.4 Minimum enclosure around via2
# via2.5 Minimum enclosure around via2 on two opposite sides
#drc.add_enclosure("m2",
#                  layer="via2",
#                  enclosure=0.040,
#                  extension=0.085)

# via2.1a Minimum width of Via2
# via2.2  Minimum spacing of Via2
#drc.add_layer("via2",
#              width=0.200,
#              spacing=0.200)

drc.add_layer("m3",
              width=0.28,
              spacing=0.28,
              area=0.1444)
# m3.4 Minimum enclosure around via2
#drc.add_enclosure("m3",
#                  layer="via2",
#                  enclosure=0.065)
# via3.4 Minimum enclosure around via3
# via3.5 Minimum enclosure around via3 on two opposite sides
#drc.add_enclosure("m3",
#                  layer="via3",
#                  enclosure=0.060,
#                  extension=0.090)

# via3.1 Minimum width of Via3
# via3.2 Minimum spacing of Via3
#drc.add_layer("via3",
#              width=0.200,
#              spacing=0.200)

drc.add_layer("m4",
              width=0.28,
              spacing=0.28,
              area=0.1444)
# m4.3 Minimum enclosure around via3
#drc.add_enclosure("m4",
#                  layer="via3",
#                  enclosure=0.065)

#drc.add_enclosure("m4",
#                  layer="via4",
#                  enclosure=0.060)


# via4.1 Minimum width of Via4
# via4.2 Minimum spacing of Via4
#drc.add_layer("via4",
#              width=0.800,
#              spacing=0.800)

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
spice["nmos"] = "sky130_fd_pr__nfet_01v8"
spice["pmos"] = "sky130_fd_pr__pfet_01v8"
spice["power"]="vccd1"
spice["ground"]="vssd1"

# whether or not the device model is actually a subckt
spice["device_prefix"] = "X"

spice["fet_libraries"] = {"TT": [[os.environ.get("SPICE_MODEL_DIR") + "/sky130.lib.spice", "tt"]]}

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

