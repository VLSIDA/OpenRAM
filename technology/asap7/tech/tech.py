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
File containing the process technology parameters for ASAP7 (predictive 7nm FinFET).
Rule values are from the ASAP7 DRM (asap7PDK_r1p7/docs/asap7_drm.pdf).
This port is netlist-only; see ../__init__.py.
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

cell_properties.bitcell_1port.mirror.y = True
cell_properties.bitcell_1port.mirror.y = False

cell_properties.bitcell_2port.mirror.y = True
cell_properties.bitcell_2port.mirror.y = False

###################################################
# Custom cell properties
###################################################
layer_properties = d.layer_properties()


power_ring_top = True
power_ring_bottom = True
power_ring_left = True
power_ring_right = True
connect_ring_top = []
connect_ring_bottom = []
connect_ring_left = ['vdd','gnd']
connect_ring_right = ['vdd','gnd']
###################################################
# GDS file info
###################################################

GDS = {}
# ASAP7 GDS uses a 0.25 nm database unit (Calibre precision 4000/um)
GDS["unit"] = (0.00025, 2.5e-10)

# LEF database units per micron
lef_units = 4000
# default label zoom
GDS["zoom"] = 0.05

###################################################
# Interconnect stacks
###################################################

# ASAP7 contacts diffusion through LISD and gates through LIG, then V0 to M1.
# OpenRAM's single-contact FEOL stacks are an approximation used for netlist mode.
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

feol_stacks = [poly_stack,
               active_stack]

beol_stacks = [m1_stack,
               m2_stack,
               m3_stack]

layer_stacks = feol_stacks + beol_stacks

# ASAP7: M1 vertical, M2 horizontal, M3 vertical, M4 horizontal
preferred_directions = {"poly": "V",
                        "active": "H",
                        "m1": "V",
                        "m2": "H",
                        "m3": "V",
                        "m4": "H"}

lef_rom_interconnect = ["m1", "m2", "m3", "m4"]

###################################################
# Power grid
###################################################
power_grid = m3_stack

###################################################
# GDS Layer Map (asap7_TechLib.layermap)
###################################################

layer = {}
layer["nwell"]    = (1, 0)
layer["fin"]      = (2, 0)
layer["poly"]     = (7, 0)    # Gate
layer["active"]   = (11, 0)
layer["nimplant"] = (12, 0)   # Nselect
layer["pimplant"] = (13, 0)   # Pselect
layer["lig"]      = (16, 0)
layer["lisd"]     = (17, 0)
layer["contact"]  = (18, 0)   # V0
layer["m1"]       = (19, 0)
layer["via1"]     = (21, 0)
layer["m2"]       = (20, 0)
layer["via2"]     = (25, 0)
layer["m3"]       = (30, 0)
layer["via3"]     = (35, 0)
layer["m4"]       = (40, 0)
layer["via4"]     = (45, 0)
layer["m5"]       = (50, 0)
layer["via5"]     = (55, 0)
layer["m6"]       = (60, 0)
layer["via6"]     = (65, 0)
layer["m7"]       = (70, 0)
layer["via7"]     = (75, 0)
layer["m8"]       = (80, 0)
layer["via8"]     = (85, 0)
layer["m9"]       = (90, 0)
layer["boundary"] = (100, 0)
layer["text"]     = (101, 0)
layer["sramvt"]   = (110, 0)
# No separate pwell, vtg/vth or thick-oxide layers: OpenRAM tests "x in layer"

use_purpose = {}

# Pin shapes and labels use purpose 251 (pin) in ASAP7
pin_purpose = 251
label_purpose = 251

layer_names = {}
for k in layer:
    layer_names[k] = k

###################################################
# DRC/LVS Rules Setup
###################################################

parameter = {}
# FinFET widths are fin-quantized: one fin is 27 nm of effective width
# (spice["fin_width"] below). Minimum logic device is 3 fins as in INVx1_ASAP7.
parameter["min_tx_size"] = 0.081
# NMOS and PMOS fins have similar drive in ASAP7 (INVx1 uses 3/3 fins)
parameter["beta"] = 1

# 6T bitcell "122" (pull-up 1 fin, pass-gate 2, pull-down 2), for analytical models
parameter["6T_inv_nmos_size"] = 0.054
parameter["6T_inv_pmos_size"] = 0.027
parameter["6T_access_size"] = 0.054

drclvs_home = os.environ.get("DRCLVS_HOME")

drc = d.design_rules("asap7")

drc["grid"] = 0.001

drc["drc_rules"] = drclvs_home + "/ruledirs/drc/drcRules_calibre_asap7.rul"
drc["lvs_rules"] = drclvs_home + "/ruledirs/lvs/lvsRules_calibre_asap7.rul"
drc["xrc_rules"] = drclvs_home + "/ruledirs/rcx/calibre.rcx"
drc["layer_map"] = os.environ.get("OPENRAM_TECH") + "/asap7/layers.map"

# ACTIVE.W.1: one fin; GATE.W.1: 20 nm gate
drc["minwidth_tx"] = 0.027
drc["minlength_channel"] = 0.020

# WELL.W.1 / WELL.S.1
drc["pwell_to_nwell"] = 0.0
drc.add_layer("nwell",
              width=0.108,
              spacing=0.108)
drc.add_layer("pwell",
              width=0.108,
              spacing=0.108)

# GATE.W.1 (20 nm), GATE.S.1 (54 nm pitch, so 34 nm space)
drc.add_layer("poly",
              width=0.020,
              spacing=0.034)
# GATE.W.2 and GCUT end rules, approximated
drc["poly_extend_active"] = 0.020
drc["poly_to_contact"] = 0.010
drc["active_enclose_gate"] = 0.017
drc["poly_to_active"] = 0.010
drc["poly_to_field_poly"] = 0.034
drc["minarea_poly"] = 0.0

# ACTIVE.W.1 / ACTIVE.S.1
drc.add_layer("active",
              width=0.027,
              spacing=0.027)
# ACTIVE.WELL.EN.1, approximated
drc.add_enclosure("nwell",
                  layer="active",
                  enclosure=0.0135)
drc.add_enclosure("pwell",
                  layer="active",
                  enclosure=0.0135)

drc["implant_to_channel"] = 0.0
drc.add_enclosure("implant",
                  layer="active",
                  enclosure=0)
drc.add_enclosure("implant",
                  layer="contact",
                  enclosure=0)
drc["implant_to_contact"] = 0.0
drc.add_layer("implant",
              width=0.054,
              spacing=0.054)

# V0.W.1 / V0.S.2
drc.add_layer("contact",
              width=0.018,
              spacing=0.023)
drc.add_enclosure("active",
                  layer="contact",
                  enclosure=0.0)
drc.add_enclosure("poly",
                  layer="contact",
                  enclosure=0.0)
drc["active_contact_to_gate"] = 0.008
drc["poly_contact_to_gate"] = 0.017
drc["contact_to_gate"] = 0.008
drc["contact_to_poly"] = 0.017

# M1.W.1 / M1.S.1, V1.M1.EN.1
drc.add_layer("m1",
              width=0.018,
              spacing=0.018)
drc.add_enclosure("m1",
                  layer="contact",
                  enclosure=0,
                  extension=0.005)
drc.add_enclosure("m1",
                  layer="via1",
                  enclosure=0,
                  extension=0.005)

# V1.W.1 / V1.S.4
drc.add_layer("via1",
              width=0.018,
              spacing=0.027)

# M2 and M3 follow the M1 width/spacing rules
drc.add_layer("m2",
              width=0.018,
              spacing=0.018)
drc.add_enclosure("m2",
                  layer="via1",
                  enclosure=0,
                  extension=0.005)
drc.add_enclosure("m2",
                  layer="via2",
                  enclosure=0,
                  extension=0.005)

drc.add_layer("via2",
              width=0.018,
              spacing=0.027)

drc.add_layer("m3",
              width=0.018,
              spacing=0.018)
drc.add_enclosure("m3",
                  layer="via2",
                  enclosure=0,
                  extension=0.005)
drc.add_enclosure("m3",
                  layer="via3",
                  enclosure=0,
                  extension=0.005)

drc.add_layer("via3",
              width=0.018,
              spacing=0.027)

# M4.W.1 / M4.S.1, V3.M4.EN.2
drc.add_layer("m4",
              width=0.024,
              spacing=0.024)
drc.add_enclosure("m4",
                  layer="via3",
                  enclosure=0.011)

###################################################
# Spice Simulation Parameters
###################################################

spice = {}
spice["nmos"] = "nmos_rvt"
spice["pmos"] = "pmos_rvt"
# BSIM-CMG FinFET: widths are emitted as an integer number of fins
# (nfin), each fin 27 nm of effective width.
spice["fin_width"] = 0.027

SPICE_MODEL_DIR = os.environ.get("SPICE_MODEL_DIR")
spice["fet_models"] = {"TT": [SPICE_MODEL_DIR + "/7nm_TT.pm"],
                       "FF": [SPICE_MODEL_DIR + "/7nm_FF.pm"],
                       "SS": [SPICE_MODEL_DIR + "/7nm_SS.pm"],
                       }

spice["feasible_period"] = 1          # estimated feasible period in ns
spice["supply_voltages"] = [0.63, 0.7, 0.77]  # Supply voltage corners in [Volts]
spice["nom_supply_voltage"] = 0.7     # Nominal supply voltage in [Volts]
spice["rise_time"] = 0.005            # rise time in [Nano-seconds]
spice["fall_time"] = 0.005            # fall time in [Nano-seconds]
spice["temperatures"] = [0, 25, 100]  # Temperature corners (celcius)
spice["nom_temperature"] = 25         # Nominal temperature (celcius)

# analytical delay parameters (rough 7nm estimates, used only with analytical_delay)
spice["nom_threshold"] = 0.25
spice["wire_unit_r"] = 2.0
spice["wire_unit_c"] = 1.0e-15
spice["min_tx_drain_c"] = 0.05
spice["min_tx_gate_c"] = 0.05
spice["dff_setup"] = 10
spice["dff_hold"] = 5
spice["dff_in_cap"] = 0.6
spice["dff_out_cap"] = 1

spice["bitcell_leakage"] = 1
spice["inv_leakage"] = 1
spice["nand2_leakage"] = 1
spice["nand3_leakage"] = 1
spice["nand4_leakage"] = 1
spice["nor2_leakage"] = 1
spice["dff_leakage"] = 1

spice["default_event_frequency"] = 100

parameter["le_tau"] = 1.0
parameter["cap_relative_per_ff"] = 7.5
parameter["dff_clk_cin"] = 30.6
parameter["6tcell_wl_cin"] = 3
parameter["min_inv_para_delay"] = 2.4
parameter["sa_en_pmos_size"] = 0.108
parameter["sa_en_nmos_size"] = 0.081
parameter["sa_inv_pmos_size"] = 0.081
parameter["sa_inv_nmos_size"] = 0.081
parameter["bitcell_drain_cap"] = 0.02

spice["i_on_n"] = 0.0012
spice["i_on_p"] = 0.0010
spice["tox"] = 0.001
spice["eps_ox"] = 0.00245e-14
spice["cox"] = spice["eps_ox"]/spice["tox"]
spice["c_g_ideal"] = spice["cox"]*drc["minlength_channel"]
spice["c_overlap"] = 0.2*spice["c_g_ideal"]
spice["c_fringe"] = 0
spice["cpolywire"] = 0
spice["c_junc"] = 5e-16
spice["c_junc_sw"] = 5e-16
spice["wire_c_per_um"] = spice["wire_unit_c"]*drc["minwidth_m2"]
spice["wire_r_per_um"] = spice["wire_unit_r"]/drc["minwidth_m2"]
spice["mobility_n"] = 0.045e8
spice["V_dsat"] = 0.05
spice["sa_transconductance"] = (spice["mobility_n"])*spice["cox"]*(parameter["sa_inv_nmos_size"]/parameter["min_tx_size"])*spice["V_dsat"]

###################################################
# Technology Tool Preferences
###################################################

drc_name = "calibre"
lvs_name = "calibre"
pex_name = "calibre"

blackbox_bitcell = False
