# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os
from openram import drc as d
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
cell_properties.bitcell_1port.gnd_layer = "m2"
cell_properties.bitcell_1port.gnd_dir = "V"

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

poly_stack = ("poly", "poly_contact", "m1")
active_stack = ("active", "active_contact", "m1")
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
layer["pwell"]          = (41, 0)
layer["nwell"]          = (42, 0)
layer["active"]         = (43, 0)
layer["pimplant"]       = (44, 0)
layer["nimplant"]       = (45, 0)
layer["poly"]           = (46, 0)
layer["poly_contact"]   = (47, 0)
layer["active_contact"] = (48, 0)
layer["m1"]         = (49, 0)
layer["via1"]           = (50, 0)
layer["m2"]         = (51, 0)
layer["via2"]           = (61, 0)
layer["m3"]         = (62, 0)
layer["via3"]           = (30, 0)
layer["m4"]         = (31, 0)
layer["text"]           = (63, 0)
layer["boundary"]       = (63, 0)

use_purpose = {}

# Layer names for external PDKs
layer_names = {}
layer_names["active"]  = "active"
layer_names["pwell"]   = "pwell"
layer_names["nwell"]   = "nwell"
layer_names["nimplant"]= "nimplant"
layer_names["pimplant"]= "pimplant"
layer_names["poly"]    = "poly"
layer_names["poly_contact"] = "poly_contact"
layer_names["active_contact"] = "active_contact"
layer_names["m1"]      = "metal1"
layer_names["via1"]    = "via1"
layer_names["m2"]      = "metal2"
layer_names["via2"]    = "via2"
layer_names["m3"]      = "metal3"
layer_names["via3"]    = "via3"
layer_names["m4"]      = "metal4"
layer_names["text"]    = "text"
layer_names["boundary"]= "boundary"

###################################################
# DRC/LVS Rules Setup
###################################################
_lambda_ = 0.2

#technology parameter
parameter={}
parameter["min_tx_size"] = 4*_lambda_
parameter["beta"] = 2

# These 6T sizes are used in the parameterized bitcell.
parameter["6T_inv_nmos_size"] = 8*_lambda_
parameter["6T_inv_pmos_size"] = 3*_lambda_
parameter["6T_access_size"] = 4*_lambda_

drclvs_home=os.environ.get("DRCLVS_HOME")

drc = d.design_rules("scn4me_sub")

#grid size is 1/2 a lambda
drc["grid"]=0.5*_lambda_

#DRC/LVS test set_up
drc["drc_rules"]=None #drclvs_home+"/calibreDRC_scn3me_subm.rul"
drc["lvs_rules"]=None #drclvs_home+"/calibreLVS_scn3me_subm.rul"
drc["layer_map"]=os.environ.get("OPENRAM_TECH")+"/scn3me_subm/layers.map"

# minwidth_tx with contact (no dog bone transistors)
drc["minwidth_tx"] = 4*_lambda_
drc["minlength_channel"] = 2*_lambda_

# 1.4 Minimum spacing between wells of different type (if both are drawn)
drc["pwell_to_nwell"] = 0
# 1.3 Minimum spacing between wells of same type (if both are drawn)
# 1.1 Minimum width
drc.add_layer("nwell",
              width = 12*_lambda_,
              spacing = 6*_lambda_)
drc.add_layer("pwell",
              width = 12*_lambda_,
              spacing = 6*_lambda_)

# 3.1 Minimum width
# 3.2 Minimum spacing over active
drc.add_layer("poly",
              width = 2*_lambda_,
              spacing = 3*_lambda_)
# 3.3 Minimum gate extension of active
drc["poly_extend_active"] = 2*_lambda_
# 5.5.b Minimum spacing between poly contact and other poly (alternative rules)
drc["poly_to_contact"] = 4*_lambda_
# ??
drc["active_enclose_gate"] = 0.0
# 3.5 Minimum field poly to active
drc["poly_to_active"] = _lambda_
# 3.2.a Minimum spacing over field poly
drc["poly_to_field_poly"] = 3*_lambda_

# 2.1 Minimum width
# 2.2 Minimum spacing
drc.add_layer("active",
              width = 3*_lambda_,
              spacing = 4*_lambda_)

# 2.3 Source/drain active to well edge
drc.add_enclosure("nwell",
                  layer = "active",
                  enclosure = 6*_lambda_)
drc.add_enclosure("pwell",
                  layer = "active",
                  enclosure = 6*_lambda_)

# 4.1 Minimum select spacing to channel of transistor to ensure adequate source/drain width
drc["implant_to_channel"] = 3*_lambda_
# 4.2 Minimum select overlap of active
drc.add_enclosure("implant",
                  layer = "active",
                  enclosure = 2*_lambda_)
# 4.3 Minimum select overlap of contact
drc.add_enclosure("implant",
                  layer = "contact",
                  enclosure = _lambda_)
# Not a rule
drc["implant_to_contact"] = 0
# Not a rule
drc.add_layer("implant",
              width = 0,
              spacing = 0)

# 6.1 Exact contact size
# 5.3 Minimum contact spacing
drc.add_layer("active_contact",
              width = 2*_lambda_,
              spacing = 3*_lambda_)
# 6.2.b Minimum active overlap
drc.add_enclosure("active",
                  layer = "active_contact",
                  enclosure = _lambda_)
drc.add_enclosure("active",
                  layer = "contact",
                  enclosure = _lambda_)
# Reserved for other technologies
drc["active_contact_to_gate"] = 2*_lambda_
# 5.4 Minimum spacing to gate of transistor
drc["poly_contact_to_gate"] = 2*_lambda_

# 6.1 Exact contact size
# 5.3 Minimum contact spacing
drc.add_layer("poly_contact",
              width = 2*_lambda_,
              spacing = 3*_lambda_)
# 5.2.b Minimum poly overlap
drc.add_enclosure("poly",
                  layer = "poly_contact",
                  enclosure = _lambda_)
# Reserved for other technologies
drc["poly_contact_to_gate"] = 2*_lambda_
# 5.4 Minimum spacing to gate of transistor
drc["poly_contact_to_poly"] = 2*_lambda_

# 7.1 Minimum width
# 7.2 Minimum spacing
drc.add_layer("m1",
              width = 3*_lambda_,
              spacing = 3*_lambda_)
# 7.3 Minimum overlap of any contact
drc.add_enclosure("m1",
                  layer = "poly_contact",
                  enclosure = _lambda_)
drc.add_enclosure("m1",
                  layer = "active_contact",
                  enclosure = _lambda_)
# 8.3 Minimum overlap by m1
drc.add_enclosure("m1",
                  layer = "via1",
                  enclosure = _lambda_)

# 8.1 Exact size
# 8.2 Minimum via1 spacing
drc.add_layer("via1",
              width = 2*_lambda_,
              spacing = 3*_lambda_)

# 9.1 Minimum width
# 9.2 Minimum spacing
drc.add_layer("m2",
              width = 3*_lambda_,
              spacing = 3*_lambda_)
# 9.3 Minimum overlap of via1
drc.add_enclosure("m2",
                  layer = "via1",
                  enclosure = _lambda_)
# 14.3 Minimum overlap by m2
drc.add_enclosure("m2",
                  layer = "via2",
                  enclosure = _lambda_)

# 14.1 Exact size
# 14.2 Minimum spacing
drc.add_layer("via2",
              width = 2*_lambda_,
              spacing = 3*_lambda_)

# 15.1 Minimum width
# 15.2 Minimum spacing to m3
drc.add_layer("m3",
              width = 3*_lambda_,
              spacing = 3*_lambda_)

# 15.3 Minimum overlap of via 2
drc.add_enclosure("m3",
                  layer = "via2",
                  enclosure = _lambda_)

# 21.3 Minimum overlap by m3
drc.add_enclosure("m3",
                  layer = "via3",
                  enclosure = _lambda_)

# 21.1 Exact size
# 21.2 Minimum spacing
drc.add_layer("via3",
              width = 2*_lambda_,
              spacing = 3*_lambda_)

# 22.1 Minimum width
# 22.2 Minimum spacing to m4
drc.add_layer("m4",
              width = 6*_lambda_,
              spacing = 6*_lambda_)

# 22.3 Minimum overlap of via 3
drc.add_enclosure("m4",
                  layer = "via3",
                  enclosure = 2*_lambda_)

###################################################
# Spice Simulation Parameters
###################################################

# spice model info
spice={}
spice["nmos"]="n"
spice["pmos"]="p"
# This is a map of corners to model files
SPICE_MODEL_DIR=os.environ.get("SPICE_MODEL_DIR")
spice["fet_models"] = {"TT": [SPICE_MODEL_DIR + "/nom/pmos.sp", SPICE_MODEL_DIR + "/nom/nmos.sp"],
                       "FF": [SPICE_MODEL_DIR + "/ff/pmos.sp", SPICE_MODEL_DIR + "/ff/nmos.sp"],
                       "FS": [SPICE_MODEL_DIR + "/ff/pmos.sp", SPICE_MODEL_DIR + "/ss/nmos.sp"],
                       "SF": [SPICE_MODEL_DIR + "/ss/pmos.sp", SPICE_MODEL_DIR + "/ff/nmos.sp"],
                       "SS": [SPICE_MODEL_DIR + "/ss/pmos.sp", SPICE_MODEL_DIR + "/ss/nmos.sp"],
                       "ST": [SPICE_MODEL_DIR + "/ss/pmos.sp", SPICE_MODEL_DIR + "/nom/nmos.sp"],
                       "TS": [SPICE_MODEL_DIR + "/nom/pmos.sp", SPICE_MODEL_DIR + "/ss/nmos.sp"],
                       "FT": [SPICE_MODEL_DIR + "/ff/pmos.sp", SPICE_MODEL_DIR + "/nom/nmos.sp"],
                       "TF": [SPICE_MODEL_DIR + "/nom/pmos.sp", SPICE_MODEL_DIR + "/ff/nmos.sp"],
                       }


#spice stimulus related variables
spice["feasible_period"] = 10         # estimated feasible period in ns
spice["supply_voltages"] = [4.5, 5.0, 5.5]  # Supply voltage corners in [Volts]
spice["nom_supply_voltage"] = 5.0    # Nominal supply voltage in [Volts]
spice["rise_time"] = 0.05            # rise time in [Nano-seconds]
spice["fall_time"] = 0.05            # fall time in [Nano-seconds]
spice["temperatures"] = [0, 25, 100]  # Temperature corners (celcius)
spice["nom_temperature"] = 25        # Nominal temperature (celcius)

# analytical delay parameters
spice["nom_threshold"] = 1.3   # Nominal Threshold voltage in Volts
spice["wire_unit_r"] = 0.07     # Unit wire resistance in ohms/square
spice["wire_unit_c"] = 1.7e-17  # Unit wire capacitance F/um^2
spice["min_tx_drain_c"] = 0.7   # Minimum transistor drain capacitance in ff
spice["min_tx_gate_c"] = 0.1    # Minimum transistor gate capacitance in ff
spice["dff_setup"] = 9        # DFF setup time in ps
spice["dff_hold"] = 1         # DFF hold time in ps
spice["dff_in_cap"] = 9.8242  # Input capacitance (D) [Femto-farad]
spice["dff_out_cap"] = 2       # Output capacitance (Q) [Femto-farad]

# analytical power parameters, many values are temporary
spice["bitcell_leakage"] = 1     # Leakage power of a single bitcell in nW
spice["inv_leakage"] = 1         # Leakage power of inverter in nW
spice["nand2_leakage"] = 1       # Leakage power of 2-input nand in nW
spice["nand3_leakage"] = 1       # Leakage power of 3-input nand in nW
spice["nand4_leakage"] = 1       # Leakage power of 4-input nand in nW
spice["nor2_leakage"] = 1        # Leakage power of 2-input nor in nW
spice["dff_leakage"] = 1      # Leakage power of flop in nW

spice["default_event_frequency"] = 100         # Default event activity of every gate. MHz

# Logical Effort relative values for the Handmade cells
parameter["le_tau"] = 18.17                  # In pico-seconds.
parameter["min_inv_para_delay"] = 2.07       # In relative delay units
parameter["cap_relative_per_ff"] = .91       # Units of Relative Capacitance/ Femto-Farad
parameter["dff_clk_cin"] = 27.5              # In relative capacitance units
parameter["6tcell_wl_cin"] = 2               # In relative capacitance units
parameter["sa_en_pmos_size"] = 24 * _lambda_
parameter["sa_en_nmos_size"] = 9 * _lambda_
parameter["sa_inv_pmos_size"] = 18 * _lambda_
parameter["sa_inv_nmos_size"] = 9 * _lambda_
parameter["bitcell_drain_cap"] = 0.2        # In Femto-Farad, approximation of drain capacitance

# Spice Values uses to calculate analytical delay based on CACTI equations
spice["i_on_n"] = 0.00060199 # A/um 
spice["i_on_p"] = 0.000108   # A/um
spice["tox"] = 0.0076          # microns
spice["eps_ox"] = 0.00859e-14  # F/um, calculated from CACTI 180nm data 
spice["cox"] = spice["eps_ox"]/spice["tox"] # F/um^2
spice["c_g_ideal"] = spice["cox"]*drc["minlength_channel"] # F/um
spice["c_overlap"] = 0.2*spice["c_g_ideal"] # F/um
spice["c_fringe"] = 0 # F/um, not defined in this technology
spice["cpolywire"] = 0 # F/um, replicated from CACTI which is hardcoded to 0
spice["c_junc"] = 9.276962e-16 #F/um^2
spice["c_junc_sw"] = 3.181055e-16 #F/um
spice["wire_c_per_um"] = spice["wire_unit_c"]*drc["minwidth_m2"] # Unit c by m2 width,  F/um units
spice["wire_r_per_um"] = spice["wire_unit_r"]/drc["minwidth_m2"] # Unit r per m2 width, Ohms/um units
spice["mobility_n"] = 444.94e8 # um^2/(V*s)
spice["V_dsat"] = 0.256        # From CACTI 180nm tech
spice["sa_transconductance"] = (spice["mobility_n"])*spice["cox"]*(parameter["sa_inv_nmos_size"]/parameter["min_tx_size"])*spice["V_dsat"]


###################################################
# Technology Tool Preferences
###################################################

drc_name = "magic"
lvs_name = "netgen"
pex_name = "magic"

blackbox_bitcell = False
