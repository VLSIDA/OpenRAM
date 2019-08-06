# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os
from design_rules import *

"""
File containing the process technology parameters for FreePDK 45nm.
"""

#GDS file info
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
##GDS Layer Map
###################################################

# create the GDS layer map
# FIXME: parse the gds layer map from the cadence map?
layer = {}
layer["active"]  = 1
layer["pwell"]   = 2
layer["nwell"]   = 3
layer["nimplant"]= 4
layer["pimplant"]= 5
layer["vtg"]     = 6
layer["vth"]     = 7
layer["thkox"]   = 8
layer["poly"]    = 9
layer["contact"] = 10
layer["active_contact"] = 10
layer["metal1"]  = 11
layer["via1"]    = 12
layer["metal2"]  = 13
layer["via2"]    = 14
layer["metal3"]  = 15
layer["via3"]    = 16
layer["metal4"]  = 17
layer["via4"]    = 18
layer["metal5"]  = 19
layer["via5"]    = 20
layer["metal6"]  = 21
layer["via6"]    = 22
layer["metal7"]  = 23
layer["via7"]    = 24
layer["metal8"]  = 25
layer["via8"]    = 26
layer["metal9"]  = 27
layer["via9"]    = 28
layer["metal10"] = 29
layer["text"]    = 239
layer["boundary"]= 239
layer["blockage"]= 239

###################################################
##END GDS Layer Map
###################################################

###################################################
##DRC/LVS Rules Setup
###################################################

#technology parameter
parameter={}
parameter["min_tx_size"] = 0.09
parameter["beta"] = 3

parameter["6T_inv_nmos_size"] = 0.205
parameter["6T_inv_pmos_size"] = 0.09
parameter["6T_access_size"] = 0.135

drclvs_home=os.environ.get("DRCLVS_HOME")

drc = design_rules("freepdk45")

drc["body_tie_down"] = 0
drc["has_pwell"] = True
drc["has_nwell"] = True

#grid size
drc["grid"] = 0.0025

#DRC/LVS test set_up
drc["drc_rules"]=drclvs_home+"/calibreDRC.rul"
drc["lvs_rules"]=drclvs_home+"/calibreLVS.rul"
drc["xrc_rules"]=drclvs_home+"/calibrexRC.rul"
drc["layer_map"]=os.environ.get("OPENRAM_TECH")+"/freepdk45/layers.map"

# minwidth_tx with contact (no dog bone transistors)
drc["minwidth_tx"] = 0.09
drc["minlength_channel"] = 0.05

# WELL.2 Minimum spacing of nwell/pwell at different potential
drc["pwell_to_nwell"] = 0.225
# WELL.3 Minimum spacing of nwell/pwell at the same potential
drc["well_to_well"] = 0.135
# WELL.4 Minimum width of nwell/pwell
drc["minwidth_well"] = 0.2

# POLY.1 Minimum width of poly
drc["minwidth_poly"] = 0.05
# POLY.2 Minimum spacing of poly AND active
drc["poly_to_poly"] = 0.14
# POLY.3 Minimum poly extension beyond active
drc["poly_extend_active"] = 0.055
# Not a rule
drc["poly_to_polycontact"] = 0.075
# POLY.4 Minimum enclosure of active around gate
drc["active_enclosure_gate"] = 0.07
# POLY.5 Minimum spacing of field poly to active
drc["poly_to_active"] = 0.05
# POLY.6 Minimum Minimum spacing of field poly
drc["poly_to_field_poly"] = 0.075
# Not a rule
drc["minarea_poly"] = 0.0

# ACTIVE.2 Minimum spacing of active
drc["active_to_body_active"] = 0.08
# ACTIVE.1 Minimum width of active
drc["minwidth_active"] = 0.09
# Not a rule
drc["active_to_active"] = 0
# ACTIVE.3 Minimum enclosure/spacing of nwell/pwell to active
drc["well_enclosure_active"] = 0.055
# Reserved for asymmetric enclosures
drc["well_extend_active"] = 0.055
# Not a rule
drc["minarea_active"] = 0

# IMPLANT.1 Minimum spacing of nimplant/ pimplant to channel
drc["implant_to_channel"] = 0.07
# Not a rule
drc["implant_enclosure_active"] = 0
# Not a rule
drc["implant_enclosure_contact"] = 0
# IMPLANT.2 Minimum spacing of nimplant/ pimplant to contact
drc["implant_to_contact"] = 0.025
# IMPLANT.3 Minimum width/ spacing of nimplant/ pimplant
drc["implant_to_implant"] = 0.045
# IMPLANT.4 Minimum width/ spacing of nimplant/ pimplant
drc["minwidth_implant"] = 0.045

# CONTACT.1 Minimum width of contact
drc["minwidth_contact"] = 0.065
# CONTACT.2 Minimum spacing of contact
drc["contact_to_contact"] = 0.075
# CONTACT.4 Minimum enclosure of active around contact
drc["active_enclosure_contact"] = 0.005
# Reserved for asymmetric enclosures
drc["active_extend_contact"] = 0.005
# CONTACT.5 Minimum enclosure of poly around contact
drc["poly_enclosure_contact"] = 0.005
# Reserved for asymmetric enclosures
drc["poly_extend_contact"] = 0.005
# CONTACT.6 Minimum spacing of contact and gate
drc["contact_to_gate"] = 0.0375 #changed from 0.035
# CONTACT.7 Minimum spacing of contact and poly
drc["contact_to_poly"] = 0.090

# METAL1.1 Minimum width of metal1
drc["minwidth_metal1"] = 0.065
# METAL1.2 Minimum spacing of metal1
drc["metal1_to_metal1"] = 0.065
# METAL1.3 Minimum enclosure around contact on two opposite sides
drc["metal1_enclosure_contact"] = 0
# Reserved for asymmetric enclosures
drc["metal1_extend_contact"] = 0.035
# METAL1.4 inimum enclosure around via1 on two opposite sides
drc["metal1_extend_via1"] = 0.035
# Reserved for asymmetric enclosures
drc["metal1_enclosure_via1"] = 0
# Not a rule
drc["minarea_metal1"] = 0

# VIA1.1 Minimum width of via1
drc["minwidth_via1"] = 0.065
# VIA1.2 Minimum spacing of via1
drc["via1_to_via1"] = 0.075

# METALINT.1 Minimum width of intermediate metal
drc["minwidth_metal2"] = 0.07
# METALINT.2 Minimum spacing of intermediate metal
drc["metal2_to_metal2"] = 0.07
# METALINT.3 Minimum enclosure around via1 on two opposite sides
drc["metal2_extend_via1"] = 0.035
# Reserved for asymmetric enclosures
drc["metal2_enclosure_via1"] = 0
# METALINT.4 Minimum enclosure around via[2-3] on two opposite sides
drc["metal2_extend_via2"] = 0.035
# Reserved for asymmetric enclosures
drc["metal2_enclosure_via2"] = 0
# Not a rule
drc["minarea_metal2"] = 0

# VIA2-3.1 Minimum width of Via[2-3]
drc["minwidth_via2"] = 0.065
# VIA2-3.2 Minimum spacing of Via[2-3]
drc["via2_to_via2"] = 0.075

# METALINT.1 Minimum width of intermediate metal
drc["minwidth_metal3"] = 0.07
# METALINT.2 Minimum spacing of intermediate metal
#drc["metal3_to_metal3"] = 0.07
# Minimum spacing of metal3 wider than 0.09 & longer than 0.3 = 0.09
# Minimum spacing of metal3 wider than 0.27 & longer than 0.9 = 0.27
# Minimum spacing of metal3 wider than 0.5 & longer than 1.8 = 0.5
# Minimum spacing of metal3 wider than 0.9 & longer than 2.7 = 0.9
# Minimum spacing of metal3 wider than 1.5 & longer than 4.0 = 1.5
drc["metal3_to_metal3"] = drc_lut({(0.00, 0.0) : 0.07,
                                   (0.09, 0.3) : 0.09,
                                   (0.27, 0.9) : 0.27,
                                   (0.50, 1.8) : 0.5,
                                   (0.90, 2.7) : 0.9,
                                   (1.50, 4.0) : 1.5})
# METALINT.3 Minimum enclosure around via1 on two opposite sides
drc["metal3_extend_via2"] = 0.035
# Reserved for asymmetric enclosures
drc["metal3_enclosure_via2"] = 0
# METALINT.4 Minimum enclosure around via[2-3] on two opposite sides
drc["metal3_extend_via3"]=0.035
# Reserved for asymmetric enclosures
drc["metal3_enclosure_via3"] = 0
# Not a rule
drc["minarea_metal3"] = 0

# VIA2-3.1 Minimum width of Via[2-3]
drc["minwidth_via3"] = 0.07
# VIA2-3.2 Minimum spacing of Via[2-3]
drc["via3_to_via3"] = 0.085

# METALSMG.1 Minimum width of semi-global metal
drc["minwidth_metal4"] = 0.14
# METALSMG.2 Minimum spacing of semi-global metal
#drc["metal4_to_metal4"] = 0.14
# Minimum spacing of metal4 wider than 0.27 & longer than 0.9 = 0.27
# Minimum spacing of metal4 wider than 0.5 & longer than 1.8 = 0.5
# Minimum spacing of metal4 wider than 0.9 & longer than 2.7 = 0.9
# Minimum spacing of metal4 wider than 1.5 & longer than 4.0 = 1.5
drc["metal4_to_metal4"] = drc_lut({(0.00, 0.0) : 0.14,
                                   (0.27, 0.9) : 0.27,
                                   (0.50, 1.8) : 0.5,
                                   (0.90, 2.7) : 0.9,
                                   (1.50, 4.0) : 1.5})
# METALSMG.3 Minimum enclosure around via[3-6] on two opposite sides
drc["metal4_extend_via3"] = 0.0025
# Reserved for asymmetric enclosure
drc["metal4_enclosure_via3"] = 0.0025
# Not a rule
drc["minarea_metal4"] = 0

# Metal 5-10 are ommitted



###################################################
##END DRC/LVS Rules
###################################################

###################################################
##Spice Simulation Parameters
###################################################

#spice info
spice = {}
spice["nmos"] = "nmos_vtg"
spice["pmos"] = "pmos_vtg"
# This is a map of corners to model files
SPICE_MODEL_DIR=os.environ.get("SPICE_MODEL_DIR")
spice["fet_models"] = { "TT" : [SPICE_MODEL_DIR+"/models_nom/PMOS_VTG.inc",SPICE_MODEL_DIR+"/models_nom/NMOS_VTG.inc"],
                        "FF" : [SPICE_MODEL_DIR+"/models_ff/PMOS_VTG.inc",SPICE_MODEL_DIR+"/models_ff/NMOS_VTG.inc"],
                        "SF" : [SPICE_MODEL_DIR+"/models_ss/PMOS_VTG.inc",SPICE_MODEL_DIR+"/models_ff/NMOS_VTG.inc"],
                        "FS" : [SPICE_MODEL_DIR+"/models_ff/PMOS_VTG.inc",SPICE_MODEL_DIR+"/models_ss/NMOS_VTG.inc"],
                        "SS" : [SPICE_MODEL_DIR+"/models_ss/PMOS_VTG.inc",SPICE_MODEL_DIR+"/models_ss/NMOS_VTG.inc"],
                        "ST" : [SPICE_MODEL_DIR+"/models_ss/PMOS_VTG.inc",SPICE_MODEL_DIR+"/models_nom/NMOS_VTG.inc"],
                        "TS" : [SPICE_MODEL_DIR+"/models_nom/PMOS_VTG.inc",SPICE_MODEL_DIR+"/models_ss/NMOS_VTG.inc"],
                        "FT" : [SPICE_MODEL_DIR+"/models_ff/PMOS_VTG.inc",SPICE_MODEL_DIR+"/models_nom/NMOS_VTG.inc"],
                        "TF" : [SPICE_MODEL_DIR+"/models_nom/PMOS_VTG.inc",SPICE_MODEL_DIR+"/models_ff/NMOS_VTG.inc"],
                        }

#spice stimulus related variables
spice["feasible_period"] = 5         # estimated feasible period in ns
spice["supply_voltages"] = [0.9, 1.0, 1.1] # Supply voltage corners in [Volts]
spice["nom_supply_voltage"] = 1.0    # Nominal supply voltage in [Volts]
spice["rise_time"] = 0.005           # rise time in [Nano-seconds]
spice["fall_time"] = 0.005           # fall time in [Nano-seconds]
spice["temperatures"] = [0, 25, 100] # Temperature corners (celcius)
spice["nom_temperature"] = 25        # Nominal temperature (celcius)


#sram signal names
#FIXME: We don't use these everywhere...
spice["vdd_name"] = "vdd"
spice["gnd_name"] = "gnd"
spice["control_signals"] = ["CSB", "WEB"]
spice["data_name"] = "DATA"
spice["addr_name"] = "ADDR"
spice["minwidth_tx"] = drc["minwidth_tx"]
spice["channel"] = drc["minlength_channel"]
spice["clk"] = "clk"

# analytical delay parameters
spice["vdd_nominal"] = 1.0    # Typical Threshold voltage in Volts
spice["temp_nominal"] = 25.0   # Typical Threshold voltage in Volts
spice["v_threshold_typical"] = 0.4    # Typical Threshold voltage in Volts
spice["wire_unit_r"] = 0.075     # Unit wire resistance in ohms/square
spice["wire_unit_c"] = 0.64      # Unit wire capacitance ff/um^2
spice["min_tx_r"] = 9250.0       # Minimum transistor on resistance in ohms
spice["min_tx_drain_c"] = 0.7    # Minimum transistor drain capacitance in ff
spice["min_tx_gate_c"] = 0.2     # Minimum transistor gate capacitance in ff
spice["msflop_setup"] = 9        # DFF setup time in ps
spice["msflop_hold"] = 1         # DFF hold time in ps
spice["msflop_delay"] = 20.5     # DFF Clk-to-q delay in ps
spice["msflop_slew"] = 13.1      # DFF output slew in ps w/ no load
spice["msflop_in_cap"] = 0.2091  # Input capacitance of ms_flop (Din) [Femto-farad]
spice["dff_setup"] = 9        # DFF setup time in ps
spice["dff_hold"] = 1         # DFF hold time in ps
spice["dff_delay"] = 20.5     # DFF Clk-to-q delay in ps
spice["dff_slew"] = 13.1      # DFF output slew in ps w/ no load
spice["dff_in_cap"] = 0.2091  # Input capacitance of ms_flop (Din) [Femto-farad]

# analytical power parameters, many values are temporary
spice["bitcell_leakage"] = 1     # Leakage power of a single bitcell in nW
spice["inv_leakage"] = 1         # Leakage power of inverter in nW
spice["nand2_leakage"] = 1       # Leakage power of 2-input nand in nW
spice["nand3_leakage"] = 1       # Leakage power of 3-input nand in nW
spice["nor2_leakage"] = 1        # Leakage power of 2-input nor in nW
spice["msflop_leakage"] = 1      # Leakage power of flop in nW
spice["flop_para_cap"] = 2       # Parasitic Output capacitance in fF

spice["default_event_rate"] = 100           # Default event activity of every gate. MHz
spice["flop_transition_prob"] = 0.5        # Transition probability of inverter.
spice["inv_transition_prob"] = 0.5         # Transition probability of inverter.
spice["nand2_transition_prob"] = 0.1875    # Transition probability of 2-input nand.
spice["nand3_transition_prob"] = 0.1094    # Transition probability of 3-input nand.
spice["nor2_transition_prob"] = 0.1875     # Transition probability of 2-input nor.

#Parameters related to sense amp enable timing and delay chain/RBL sizing
parameter['le_tau'] = 2.25                  #In pico-seconds.
parameter['cap_relative_per_ff'] = 7.5      #Units of Relative Capacitance/ Femto-Farad
parameter["dff_clk_cin"] = 30.6             #relative capacitance
parameter["6tcell_wl_cin"] = 3              #relative capacitance
parameter["min_inv_para_delay"] = 2.4        #Tau delay units
parameter["sa_en_pmos_size"] = 0.72          #micro-meters
parameter["sa_en_nmos_size"] = 0.27          #micro-meters
parameter["sa_inv_pmos_size"] = 0.54          #micro-meters
parameter["sa_inv_nmos_size"] = 0.27          #micro-meters
parameter['bitcell_drain_cap'] = 0.1        #In Femto-Farad, approximation of drain capacitance

###################################################
##END Spice Simulation Parameters
###################################################

