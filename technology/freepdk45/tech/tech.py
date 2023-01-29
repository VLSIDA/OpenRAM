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
File containing the process technology parameters for FreePDK 45nm.
"""

###################################################
# Custom modules
###################################################

# This uses the default classes to instantiate module from
# '$OPENRAM_HOME/compiler/modules'.
# Using tech_modules['cellname'] you can override each class by providing a custom
# implementation in '$OPENRAM_TECHDIR/modules/'
# For example: tech_modules['contact'] = 'contact_freepdk45'
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

GDS = {}
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
GDS["unit"] = (0.0005,1e-9)
# default label zoom
GDS["zoom"] = 0.05

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
# GDS Layer Map
###################################################

# Create the GDS layer map using internal names
layer = {}
layer["active"]  = (1, 0)
layer["pwell"]   = (2, 0)
layer["nwell"]   = (3, 0)
layer["nimplant"]= (4, 0)
layer["pimplant"]= (5, 0)
layer["vtg"]     = (6, 0)
layer["vth"]     = (7, 0)
layer["thkox"]   = (8, 0)
layer["poly"]    = (9, 0)
layer["contact"] = (10, 0)
layer["m1"]  = (11, 0)
layer["via1"]    = (12, 0)
layer["m2"]  = (13, 0)
layer["via2"]    = (14, 0)
layer["m3"]  = (15, 0)
layer["via3"]    = (16, 0)
layer["m4"]  = (17, 0)
layer["via4"]    = (18, 0)
layer["m5"]  = (19, 0)
layer["via5"]    = (20, 0)
layer["m6"]  = (21, 0)
layer["via6"]    = (22, 0)
layer["m7"]  = (23, 0)
layer["via7"]    = (24, 0)
layer["m8"]  = (25, 0)
layer["via8"]    = (26, 0)
layer["m9"]  = (27, 0)
layer["via9"]    = (28, 0)
layer["m10"] = (29, 0)
layer["text"]    = (239, 0)
layer["boundary"]= (239, 0)

use_purpose = {}

# Layer names for external PDKs
layer_names = {}
layer_names["active"]  = "active"
layer_names["pwell"]   = "pwell"
layer_names["nwell"]   = "nwell"
layer_names["nimplant"]= "nimplant"
layer_names["pimplant"]= "pimplant"
layer_names["vtg"]     = "vtg"
layer_names["vth"]     = "vth"
layer_names["thkox"]   = "thkox"
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
layer_names["via5"]    = "via5"
layer_names["m6"]      = "metal6"
layer_names["via6"]    = "via6"
layer_names["m7"]      = "metal7"
layer_names["via7"]    = "via7"
layer_names["m8"]      = "metal8"
layer_names["via8"]    = "via8"
layer_names["m9"]      = "metal9"
layer_names["via9"]    = "via9"
layer_names["m10"]     = "metal10"
layer_names["text"]    = "text"
layer_names["boundary"]= "boundary"

###################################################
# DRC/LVS Rules Setup
###################################################

#technology parameter
parameter={}
parameter["min_tx_size"] = 0.09
parameter["beta"] = 3

parameter["6T_inv_nmos_size"] = 0.205
parameter["6T_inv_pmos_size"] = 0.09
parameter["6T_access_size"] = 0.135

drclvs_home=os.environ.get("DRCLVS_HOME")

drc = d.design_rules("freepdk45")

#grid size
drc["grid"] = 0.0025

#DRC/LVS test set_up
drc["drc_rules"]=drclvs_home + "/calibreDRC.rul"
drc["lvs_rules"]=drclvs_home + "/calibreLVS.rul"
drc["xrc_rules"]=drclvs_home + "/calibrexRC.rul"
drc["layer_map"]=os.environ.get("OPENRAM_TECH") + "/freepdk45/layers.map"

# minwidth_tx with contact (no dog bone transistors)
drc["minwidth_tx"] = 0.09
drc["minlength_channel"] = 0.05

# WELL.2 Minimum spacing of nwell/pwell at different potential
drc["pwell_to_nwell"] = 0.225
# WELL.3 Minimum spacing of nwell/pwell at the same potential
# WELL.4 Minimum width of nwell/pwell
drc.add_layer("nwell",
              width=0.2,
              spacing=0.135)
drc.add_layer("pwell",
              width=0.2,
              spacing=0.135)

# POLY.1 Minimum width of poly
# POLY.2 Minimum spacing of poly AND active
drc.add_layer("poly",
              width=0.05,
              spacing=0.14)

# POLY.3 Minimum poly extension beyond active
drc["poly_extend_active"]=0.055
# Not a rule
drc["poly_to_contact"]=0.075
# POLY.4 Minimum enclosure of active around gate
drc["active_enclose_gate"]=0.07
# POLY.5 Minimum spacing of field poly to active
drc["poly_to_active"]=0.05
# POLY.6 Minimum Minimum spacing of field poly
drc["poly_to_field_poly"]=0.075
# Not a rule
drc["minarea_poly"]=0.0

# ACTIVE.1 Minimum width of active
# ACTIVE.2 Minimum spacing of active
drc.add_layer("active",
              width=0.09,
              spacing=0.08)
# ACTIVE.3 Minimum enclosure/spacing of nwell/pwell to active
drc.add_enclosure("nwell",
                  layer="active",
                  enclosure=0.055)
drc.add_enclosure("pwell",
                  layer="active",
                  enclosure=0.055)

# IMPLANT.1 Minimum spacing of nimplant/ pimplant to channel
drc["implant_to_channel"]=0.07
# Not a rule
drc.add_enclosure("implant",
                  layer="active",
                  enclosure=0)
# Not a rule
drc.add_enclosure("implant",
                  layer="contact",
                  enclosure=0)
# IMPLANT.2 Minimum spacing of nimplant/ pimplant to contact
drc["implant_to_contact"]=0.025
# IMPLANT.3 Minimum width/ spacing of nimplant/ pimplant
# IMPLANT.4 Minimum width/ spacing of nimplant/ pimplant
drc.add_layer("implant",
              width=0.045,
              spacing=0.045)

# CONTACT.1 Minimum width of contact
# CONTACT.2 Minimum spacing of contact
drc.add_layer("contact",
              width=0.065,
              spacing=0.075)
# CONTACT.4 Minimum enclosure of active around contact
drc.add_enclosure("active",
                  layer="contact",
                  enclosure=0.005)

# CONTACT.6 Minimum spacing of contact and gate
drc["active_contact_to_gate"]=0.0375
# CONTACT.7 Minimum spacing of contact and poly
drc["poly_contact_to_gate"]=0.090

# CONTACT.1 Minimum width of contact
# CONTACT.2 Minimum spacing of contact
drc.add_layer("contact",
              width=0.065,
              spacing=0.075)
# CONTACT.5 Minimum enclosure of poly around contact
drc.add_enclosure("poly",
                  layer="contact",
                  enclosure=0.005)
# CONTACT.6 Minimum spacing of contact and gate
drc["contact_to_gate"]=0.0375
# CONTACT.7 Minimum spacing of contact and poly
drc["contact_to_poly"]=0.090

# METAL1.1 Minimum width of metal1
# METAL1.2 Minimum spacing of metal1
drc.add_layer("m1",
              width=0.065,
              spacing=0.065)

# METAL1.3 Minimum enclosure around contact on two opposite sides
drc.add_enclosure("m1",
                  layer="contact",
                  enclosure=0,
                  extension=0.035)
# METAL1.4 inimum enclosure around via1 on two opposite sides
drc.add_enclosure("m1",
                  layer="via1",
                  enclosure=0,
                  extension=0.035)

# VIA1.1 Minimum width of via1
# VIA1.2 Minimum spacing of via1
drc.add_layer("via1",
              width=0.065,
              spacing=0.075)


# METALINT.1 Minimum width of intermediate metal
# METALINT.2 Minimum spacing of intermediate metal
drc.add_layer("m2",
              width=0.07,
              spacing=0.07)

# METALINT.3 Minimum enclosure around via1 on two opposite sides
drc.add_enclosure("m2",
                  layer="via1",
                  enclosure=0,
                  extension=0.035)

# METALINT.4 Minimum enclosure around via[2-3] on two opposite sides
drc.add_enclosure("m2",
                  layer="via2",
                  enclosure=0,
                  extension=0.035)

# VIA2-3.1 Minimum width of Via[2-3]
# VIA2-3.2 Minimum spacing of Via[2-3]
drc.add_layer("via2",
              width=0.065,
              spacing=0.085)

# METALINT.1 Minimum width of intermediate metal
# METALINT.2 Minimum spacing of intermediate metal
# Minimum spacing of m3 wider than 0.09 & longer than 0.3=0.09
# Minimum spacing of m3 wider than 0.27 & longer than 0.9=0.27
# Minimum spacing of m3 wider than 0.5 & longer than 1.8=0.5
# Minimum spacing of m3 wider than 0.9 & longer than 2.7=0.9
# Minimum spacing of m3 wider than 1.5 & longer than 4.0=1.5
drc.add_layer("m3",
              width=0.07,
              spacing=d.drc_lut({(0.00, 0.0): 0.07,
                                 (0.09, 0.3): 0.09,
                                 (0.27, 0.9): 0.27,
                                 (0.50, 1.8): 0.5,
                                 (0.90, 2.7): 0.9,
                                 (1.50, 4.0): 1.5}))
# METALINT.3 Minimum enclosure around via1 on two opposite sides
drc.add_enclosure("m3",
                  layer="via2",
                  enclosure=0,
                  extension=0.035)

# METALINT.4 Minimum enclosure around via[2-3] on two opposite sides
drc.add_enclosure("m3",
                  layer="via3",
                  enclosure=0,
                  extension=0.035)

# VIA2-3.1 Minimum width of Via[2-3]
# VIA2-3.2 Minimum spacing of Via[2-3]
drc.add_layer("via3",
              width=0.07,
              spacing=0.085)

# METALSMG.1 Minimum width of semi-global metal
# METALSMG.2 Minimum spacing of semi-global metal
# Minimum spacing of m4 wider than 0.27 & longer than 0.9=0.27
# Minimum spacing of m4 wider than 0.5 & longer than 1.8=0.5
# Minimum spacing of m4 wider than 0.9 & longer than 2.7=0.9
# Minimum spacing of m4 wider than 1.5 & longer than 4.0=1.5
drc.add_layer("m4",
              width=0.14,
              spacing=d.drc_lut({(0.00, 0.0): 0.14,
                                 (0.27, 0.9): 0.27,
                                 (0.50, 1.8): 0.5,
                                 (0.90, 2.7): 0.9,
                                 (1.50, 4.0): 1.5}))
# METALSMG.3 Minimum enclosure around via[3-6] on two opposite sides
drc.add_enclosure("m4",
                  layer="via3",
                  enclosure=0.0025)

# Metal 5-10 are ommitted

###################################################
# Spice Simulation Parameters
###################################################

#spice info
spice = {}
spice["nmos"] = "nmos_vtg"
spice["pmos"] = "pmos_vtg"
# This is a map of corners to model files
SPICE_MODEL_DIR=os.environ.get("SPICE_MODEL_DIR")
spice["fet_models"] = {"TT": [SPICE_MODEL_DIR + "/models_nom/PMOS_VTG.inc", SPICE_MODEL_DIR + "/models_nom/NMOS_VTG.inc"],
                       "FF": [SPICE_MODEL_DIR + "/models_ff/PMOS_VTG.inc", SPICE_MODEL_DIR + "/models_ff/NMOS_VTG.inc"],
                       "SF": [SPICE_MODEL_DIR + "/models_ss/PMOS_VTG.inc", SPICE_MODEL_DIR + "/models_ff/NMOS_VTG.inc"],
                       "FS": [SPICE_MODEL_DIR + "/models_ff/PMOS_VTG.inc", SPICE_MODEL_DIR + "/models_ss/NMOS_VTG.inc"],
                       "SS": [SPICE_MODEL_DIR + "/models_ss/PMOS_VTG.inc", SPICE_MODEL_DIR + "/models_ss/NMOS_VTG.inc"],
                       "ST": [SPICE_MODEL_DIR + "/models_ss/PMOS_VTG.inc", SPICE_MODEL_DIR + "/models_nom/NMOS_VTG.inc"],
                       "TS": [SPICE_MODEL_DIR + "/models_nom/PMOS_VTG.inc", SPICE_MODEL_DIR + "/models_ss/NMOS_VTG.inc"],
                       "FT": [SPICE_MODEL_DIR + "/models_ff/PMOS_VTG.inc", SPICE_MODEL_DIR + "/models_nom/NMOS_VTG.inc"],
                       "TF": [SPICE_MODEL_DIR + "/models_nom/PMOS_VTG.inc", SPICE_MODEL_DIR + "/models_ff/NMOS_VTG.inc"],
                       }

#spice stimulus related variables
spice["feasible_period"] = 5         # estimated feasible period in ns
spice["supply_voltages"] = [0.9, 1.0, 1.1] # Supply voltage corners in [Volts]
spice["nom_supply_voltage"] = 1.0    # Nominal supply voltage in [Volts]
spice["rise_time"] = 0.005           # rise time in [Nano-seconds]
spice["fall_time"] = 0.005           # fall time in [Nano-seconds]
spice["temperatures"] = [0, 25, 100] # Temperature corners (celcius)
spice["nom_temperature"] = 25        # Nominal temperature (celcius)

# analytical delay parameters
spice["nom_threshold"] = 0.4     # Typical Threshold voltage in Volts
spice["wire_unit_r"] = 0.25      # Unit wire resistance in ohms/square
spice["wire_unit_c"] = 2.3e-15   # Unit wire capacitance F/um^2, calculated from PTM
spice["min_tx_drain_c"] = 0.7    # Minimum transistor drain capacitance in ff
spice["min_tx_gate_c"] = 0.2     # Minimum transistor gate capacitance in ff
spice["dff_setup"] = 9        # DFF setup time in ps
spice["dff_hold"] = 1         # DFF hold time in ps
spice["dff_in_cap"] = 0.2091  # Input capacitance (D) [Femto-farad]
spice["dff_out_cap"] = 2       # Output capacitance (Q) [Femto-farad]

# analytical power parameters, many values are temporary
spice["bitcell_leakage"] = 1     # Leakage power of a single bitcell in nW
spice["inv_leakage"] = 1         # Leakage power of inverter in nW
spice["nand2_leakage"] = 1       # Leakage power of 2-input nand in nW
spice["nand3_leakage"] = 1       # Leakage power of 3-input nand in nW
spice["nand4_leakage"] = 1       # Leakage power of 4-input nand in nW
spice["nor2_leakage"] = 1        # Leakage power of 2-input nor in nW
spice["dff_leakage"] = 1      # Leakage power of flop in nW

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

# Spice Values uses to calculate analytical delay based on CACTI equations
spice["i_on_n"] = 0.0004463 # A/um
spice["i_on_p"] = 0.0000771   # A/um
spice["tox"] = 0.00114        # microns
spice["eps_ox"] = 0.00245e-14  # F/um, calculated from CACTI 45nm data
spice["cox"] = spice["eps_ox"]/spice["tox"] # F/um^2
spice["c_g_ideal"] = spice["cox"]*drc["minlength_channel"] # F/um
spice["c_overlap"] = 0.2*spice["c_g_ideal"] # F/um
spice["c_fringe"] = 0 # F/um, not defined in this technology
spice["cpolywire"] = 0 # F/um, replicated from CACTI which is hardcoded to 0
spice["c_junc"] = 5e-16 #F/um^2
spice["c_junc_sw"] = 5e-16 #F/um
spice["wire_c_per_um"] = spice["wire_unit_c"]*drc["minwidth_m2"] # Unit c by m2 width,  F/um units
spice["wire_r_per_um"] = spice["wire_unit_r"]/drc["minwidth_m2"] # Unit r per m2 width, Ohms/um units
spice["mobility_n"] = 0.045e8   # um^2/(V*s)
spice["V_dsat"] = 0.0938        # From CACTI 45nm tech
spice["sa_transconductance"] = (spice["mobility_n"])*spice["cox"]*(parameter["sa_inv_nmos_size"]/parameter["min_tx_size"])*spice["V_dsat"]
###################################################
# Technology Tool Preferences
###################################################

#drc_name = "calibre"
#lvs_name = "calibre"
#pex_name = "calibre"

drc_name = "klayout"
lvs_name = "klayout"
pex_name = "klayout"

blackbox_bitcell = False
