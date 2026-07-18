#!/usr/bin/env python3
# See LICENSE for licensing information.
#
"""IHP SG13G2 technology definition."""

import os
from openram import drc as d

tech_modules = d.module_type()

cell_properties = d.cell_properties()
cell_properties.ptx.model_is_subckt = True

###################################################
# GDS file info
###################################################
GDS = {}
GDS["unit"] = (0.001, 1e-6)
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
m5_stack = ("m5", "topvia1", "topmetal1")
topmetal1_stack = ("topmetal1", "topvia2", "topmetal2")

lef_rom_interconnect = ["m1", "m2", "m3", "m4", "m5", "topmetal1", "topmetal2"]

layer_indices = {"poly": 0,
                 "active": 0,
                 "nwell": 0,
                 "pwell": 0,
                 "m1": 1,
                 "m2": 2,
                 "m3": 3,
                 "m4": 4,
                 "m5": 5,
                 "topmetal1": 6,
                 "topmetal2": 7}

feol_stacks = [poly_stack, active_stack]
beol_stacks = [m1_stack, m2_stack, m3_stack, m4_stack, m5_stack, topmetal1_stack]
layer_stacks = feol_stacks + beol_stacks

preferred_directions = {"poly": "V",
                        "active": "V",
                        "m1": "H",
                        "m2": "V",
                        "m3": "H",
                        "m4": "V",
                        "m5": "H",
                        "topmetal1": "V",
                        "topmetal2": "H"}

power_grid = topmetal1_stack

###################################################
# GDS Layer Map
###################################################
layer = {}
layer["activ"] = (1, 0)
layer["active"] = layer["activ"]
layer["gatpoly"] = (5, 0)
layer["poly"] = layer["gatpoly"]
layer["cont"] = (6, 0)
layer["contact"] = layer["cont"]
layer["metal1"] = (8, 0)
layer["m1"] = layer["metal1"]
layer["via1"] = (19, 0)
layer["metal2"] = (10, 0)
layer["m2"] = layer["metal2"]
layer["via2"] = (29, 0)
layer["metal3"] = (30, 0)
layer["m3"] = layer["metal3"]
layer["via3"] = (49, 0)
layer["metal4"] = (50, 0)
layer["m4"] = layer["metal4"]
layer["via4"] = (66, 0)
layer["metal5"] = (67, 0)
layer["m5"] = layer["metal5"]
layer["topvia1"] = (125, 0)
layer["topmetal1"] = (126, 0)
layer["topvia2"] = (133, 0)
layer["topmetal2"] = (134, 0)
layer["nwell"] = (31, 0)
layer["pwell"] = (46, 0)
layer["text"] = (63, 0)
layer["boundary"] = (189, 4)
layer["mem"] = (189, 4)

label_purpose = 25

layer_names = {}
for openram_name, pdk_name in [("active", "Activ"),
                               ("poly", "GatPoly"),
                               ("contact", "Cont"),
                               ("m1", "Metal1"),
                               ("via1", "Via1"),
                               ("m2", "Metal2"),
                               ("via2", "Via2"),
                               ("m3", "Metal3"),
                               ("via3", "Via3"),
                               ("m4", "Metal4"),
                               ("via4", "Via4"),
                               ("m5", "Metal5"),
                               ("topvia1", "TopVia1"),
                               ("topmetal1", "TopMetal1"),
                               ("topvia2", "TopVia2"),
                               ("topmetal2", "TopMetal2"),
                               ("nwell", "NWell"),
                               ("pwell", "PWell"),
                               ("text", "TEXT"),
                               ("boundary", "prBoundary"),
                               ("mem", "prBoundary")]:
    layer_names[openram_name] = pdk_name

###################################################
# DRC/LVS rules setup
###################################################
parameter = {}
parameter["min_tx_size"] = 0.13
parameter["beta"] = 2
parameter["6T_inv_nmos_size"] = 0.26
parameter["6T_inv_pmos_size"] = 0.26
parameter["6T_access_size"] = 0.26
parameter["le_tau"] = 2.25
parameter["cap_relative_per_ff"] = 7.5
parameter["dff_clk_cin"] = 30.6
parameter["6tcell_wl_cin"] = 3
parameter["min_inv_para_delay"] = 2.4
parameter["sa_en_pmos_size"] = 0.72
parameter["sa_en_nmos_size"] = 0.27
parameter["sa_inv_pmos_size"] = 0.54
parameter["sa_inv_nmos_size"] = 0.27
parameter["bitcell_drain_cap"] = 0.1

drc = d.design_rules("ihp_sg13g2")
drc["grid"] = 0.005
drc["minwidth_tx"] = 0.13
drc["minlength_channel"] = 0.13
drc["pwell_to_nwell"] = 1.8

drc.add_layer("active", width=0.15, spacing=0.21)
drc.add_layer("poly", width=0.13, spacing=0.18)
drc.add_layer("contact", width=0.16, spacing=0.18)
drc.add_layer("m1", width=0.16, spacing=0.18)
drc.add_layer("m2", width=0.20, spacing=0.21)
drc.add_layer("m3", width=0.20, spacing=0.21)
drc.add_layer("m4", width=0.20, spacing=0.21)
drc.add_layer("m5", width=0.20, spacing=0.21)
drc.add_layer("topmetal1", width=1.64, spacing=1.64)
drc.add_layer("topmetal2", width=2.0, spacing=2.0)

drc["minwidth_contact"] = 0.16
drc["contact_to_contact"] = 0.18
drc["minwidth_via1"] = 0.19
drc["via1_to_via1"] = 0.22
drc["minwidth_via2"] = 0.19
drc["via2_to_via2"] = 0.22
drc["minwidth_via3"] = 0.19
drc["via3_to_via3"] = 0.22
drc["minwidth_via4"] = 0.19
drc["via4_to_via4"] = 0.22

###################################################
# Spice parameters
###################################################
spice = {}
spice["power"] = "VDD"
spice["ground"] = "VSS"
spice["nmos"] = "sg13_lv_nmos"
spice["pmos"] = "sg13_lv_pmos"
spice["fet_models"] = {"TT": "mos_tt", "SS": "mos_ss", "FF": "mos_ff"}
spice["fet_libraries"] = {
    "TT": [[os.path.join(os.environ.get("SPICE_MODEL_DIR", ""), "cornerMOSlv.lib"), "mos_tt"]],
    "SS": [[os.path.join(os.environ.get("SPICE_MODEL_DIR", ""), "cornerMOSlv.lib"), "mos_ss"]],
    "FF": [[os.path.join(os.environ.get("SPICE_MODEL_DIR", ""), "cornerMOSlv.lib"), "mos_ff"]],
}
spice["supply_voltages"] = [1.08, 1.20, 1.32]
spice["temperatures"] = [125, 25, -55]
spice["nom_supply_voltage"] = 1.20
spice["nom_temperature"] = 25
spice["dff_in_cap"] = 0.001
spice["rise_time"] = 0.05
spice["fall_time"] = 0.05
spice["feasible_period"] = 10
spice["c_g_ideal"] = 0
spice["c_overlap"] = 0
spice["c_fringe"] = 0
spice["wire_unit_r"] = 0
spice["wire_unit_c"] = 0
spice["wire_r_per_um"] = 0
spice["wire_c_per_um"] = 0
spice["min_tx_gate_c"] = 0.1
spice["min_tx_drain_c"] = 0.1
spice["dff_out_cap"] = 0.1
spice["nom_threshold"] = 0.4
spice["default_event_frequency"] = 100
spice["inv_leakage"] = 0
spice["nand2_leakage"] = 0
spice["nand3_leakage"] = 0
spice["nand4_leakage"] = 0
spice["nor2_leakage"] = 0
spice["dff_leakage"] = 0
spice["bitcell_leakage"] = 0
spice["sa_transconductance"] = 1
spice["dff_setup"] = 0
spice["dff_hold"] = 0

drc_name = "klayout"
lvs_name = "klayout"
pex_name = "magic"

layer_properties = d.layer_properties()
