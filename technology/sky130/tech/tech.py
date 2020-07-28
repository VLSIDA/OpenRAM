# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os
from design_rules import *
from module_type import *
from custom_cell_properties import cell_properties
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
tech_modules = module_type()

# These modules have been hand designed and provided in this repository. 
tech_modules["nand2_dec"] = "nand2_dec"
tech_modules["nand3_dec"] = "nand3_dec"
tech_modules["nand4_dec"] = "nand4_dec"

# These modules are auto-generated from the nand decoders above and are not
# found in this.
tech_modules["inv_dec"] = "pinv_dec"
tech_modules["and2_dec"] = "and2_dec"
tech_modules["and3_dec"] = "and3_dec"
tech_modules["and4_dec"] = "and4_dec"

###################################################
# Custom cell properties
###################################################
cell_properties = cell_properties()
cell_properties.bitcell.mirror.x = True
cell_properties.bitcell.mirror.y = True
cell_properties.bitcell.split_wl = False
cell_properties.bitcell_power_pin_directions = ("H", "H")
cell_properties.bitcell.end_caps = True

cell_properties.dff.use_custom_ports = True
cell_properties.dff.custom_port_list = ['D', 'Q', 'clk', 'vdd', 'gnd']
cell_properties.dff.custom_typ_list = ["INPUT", "OUTPUT", "INPUT", "POWER", "GROUND"]
cell_properties.dff.clk_pin = "clk"

cell_properties.dff_buff.use_custom_ports = False
cell_properties.dff_buff.buf_ports = ['CLK', 'D', 'Q', 'gnd', 'vdd']
cell_properties.dff_buff.add_body_contacts = False

cell_properties.dff_buff_array.use_custom_ports = False
cell_properties.dff_buff_array.add_body_contacts = False
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
# default label zoom
GDS["zoom"] = 0.05


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
layer["tap"]  = (65, 44) # tap
layer["nwell"]   = (64, 20) # nwell
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
layer["via1"]    = (68, 44) # via1
layer["m2"]  = (69, 20) # met2
layer["via2"]    = (69, 44) # via2
layer["m3"]  = (70, 20) # met3
layer["via3"]    = (70, 44) # via3
layer["m4"]  = (71, 20) # met4
layer["via4"]    = (71, 44) # via4
layer["m5"]  = (72, 20) # met5
layer["boundary"]= (235, 4)
# specific boundary type to define standard cell regions for DRC
layer["stdc"] = (81, 4)
layer["mem"] = (81, 2)

# Hack for sky130
# pin_purpose = 5
label_purpose = 16

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

# bitcell
parameter["bitcell_split_wl"] = False

drc = design_rules("sky130")

# grid size
drc["grid"] = 0.005

pdk_home = os.environ.get("PDK_HOME")

#DRC/LVS test set_up
# Switching between calibre and magic can be useful for development,
# it eventually should be deleted.
use_calibre = False
if use_calibre:
    # drc["drc_rules"]=pdk_home + "/DRC/Calibre/s8_drcRules"
    tech_dir = os.path.dirname(os.path.realpath(__file__))
    drc["drc_rules"]=tech_dir + "/s8_drcRules"
    # drc["lvs_rules"]=pdk_home + "/LVS/Calibre/lvsRules_s8"
    drc["lvs_rules"]=tech_dir + "/lvs_s8_opts"
    drc["xrc_rules"]=pdk_home + "/PEX/xRC/extLvsRules_s8_5lm"
    drc["layer_map"]=pdk_home + "/VirtuosoOA/libs/technology_library/s8phirs_10r.layermap"

# minwidth_tx with contact (no dog bone transistors)
# difftap.2b
drc["minwidth_tx"] = 0.360
drc["minlength_channel"] = 0.150

drc["pwell_to_nwell"] = 0
# nwell.1 Minimum width of nwell/pwell
drc.add_layer("nwell",
              width=0.840,
              spacing=0)

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
spice["nmos"] = "nshort"
spice["pmos"] = "pshort"
# This is a map of corners to model files
SPICE_MODEL_DIR = os.environ.get("SPICE_MODEL_DIR")

spice["fet_libraries"] = {"TT" : [[SPICE_MODEL_DIR+"/s8.lib", "tt"]]}
spice["fet_models"] = { "TT" :  [SPICE_MODEL_DIR+"/ppu.pm3",SPICE_MODEL_DIR+"/npd.pm3", SPICE_MODEL_DIR+"/npass.pm3",
                                SPICE_MODEL_DIR+"/tt_discrete.cor",SPICE_MODEL_DIR+"/leakcell.cor"]
                        }

# spice stimulus related variables
spice["feasible_period"] = 10        # estimated feasible period in ns
spice["supply_voltages"] = [1.7, 1.8, 1.9] # Supply voltage corners in [Volts]
spice["nom_supply_voltage"] = 1.8    # Nominal supply voltage in [Volts]
spice["rise_time"] = 0.005           # rise time in [Nano-seconds]
spice["fall_time"] = 0.005           # fall time in [Nano-seconds]
spice["temperatures"] = [0, 25, 100] # Temperature corners (celcius)
spice["nom_temperature"] = 25        # Nominal temperature (celcius)

# analytical delay parameters
spice["nom_threshold"] = 0.4     # Typical Threshold voltage in Volts
spice["wire_unit_r"] = 0.075     # Unit wire resistance in ohms/square
spice["wire_unit_c"] = 0.64      # Unit wire capacitance ff/um^2
spice["min_tx_drain_c"] = 0.7    # Minimum transistor drain capacitance in ff
spice["min_tx_gate_c"] = 0.2     # Minimum transistor gate capacitance in ff
spice["dff_setup"] = 165         # DFF setup time in ps
spice["dff_hold"] = -52          # DFF hold time in ps
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
parameter["le_tau"] = 2.25                  #In pico-seconds.
parameter["cap_relative_per_ff"] = 7.5      #Units of Relative Capacitance/ Femto-Farad
parameter["dff_clk_cin"] = 30.6             #relative capacitance
parameter["6tcell_wl_cin"] = 3              #relative capacitance
parameter["min_inv_para_delay"] = 2.4        #Tau delay units
parameter["sa_en_pmos_size"] = 0.72          #micro-meters
parameter["sa_en_nmos_size"] = 0.27          #micro-meters
parameter["sa_inv_pmos_size"] = 0.54          #micro-meters
parameter["sa_inv_nmos_size"] = 0.27          #micro-meters
parameter["bitcell_drain_cap"] = 0.1        #In Femto-Farad, approximation of drain capacitance

###################################################
# Technology Tool Preferences
###################################################

if use_calibre:
    drc_name = "calibre"
    lvs_name = "calibre"
    pex_name = "calibre"
    # Calibre automatically scales from micron to SI units
    lvs_lib = "calibre_lvs_lib"
else:
    drc_name = "magic"
    lvs_name = "netgen"
    pex_name = "magic"

# List of cells to skip running DRC/LVS on directly
blackbox_cells = ["cell_6t",
                  "dummy_cell_6t",
                  "replica_cell_6t",
                  "cell_1rw_1r",
                  "dummy_cell_1rw_1r",
                  "replica_cell_1rw_1r",
                  "cell_1w_1r",
                  "dummy_cell_1w_1r",
                  "replica_cell_1w_1r",
                  "row_cap_cell_1rw_1r",
                  "col_cap_cell_1rw_1r",
                  "nand4_dec"]
