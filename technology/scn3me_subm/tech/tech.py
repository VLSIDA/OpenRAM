import os
from openram.drc.design_rules import *
from openram.drc.module_type import *
from openram.drc.custom_cell_properties import CellProperties

"""
File containing the process technology parameters for SCMOS 3me, subm, 180nm.
"""
# This uses the default classes to instantiate module from
# '$OPENRAM_HOME/compiler/modules'.
# Using tech_modules['cellname'] you can override each class by providing a custom
# implementation in '$OPENRAM_TECHDIR/modules/'
# For example: tech_modules['contact'] = 'contact_scn3me'
tech_modules = ModuleType()

###################################################
# Custom cell properties
###################################################
cell_properties = CellProperties()
cell_properties.bitcell.mirror.x = True
cell_properties.bitcell.mirror.y = False

#GDS file info
GDS={}
# gds units
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
##GDS Layer Map
###################################################

# create the GDS layer map
layer={}
layer["vtg"]            = (-1, 0)
layer["vth"]            = (-1, 0)
layer["contact"]        = (47, 0)
layer["pwell"]          = (41, 0)
layer["nwell"]          = (42, 0)
layer["active"]         = (43, 0)
layer["pimplant"]       = (44, 0)
layer["nimplant"]       = (45, 0)
layer["poly"]           = (46, 0)
layer["active_contact"] = (48, 0)
layer["metal1"]         = (49, 0)
layer["via1"]           = (50, 0)
layer["metal2"]         = (51, 0)
layer["via2"]           = (61, 0)
layer["metal3"]         = (62, 0)
layer["text"]           = (63, 0)
layer["boundary"]       = (63, 0)
layer["blockage"]       = (83, 0)

use_purpose = {}
###################################################
##END GDS Layer Map
###################################################

###################################################
##DRC/LVS Rules Setup
###################################################
_lambda_ = 0.3

#technology parameter
parameter={}
parameter["min_tx_size"] = 4*_lambda_
parameter["beta"] = 2

parameter["6T_inv_nmos_size"] = 8*_lambda_
parameter["6T_inv_pmos_size"] = 3*_lambda_
parameter["6T_access_size"] = 4*_lambda_

drclvs_home=os.environ.get("DRCLVS_HOME")

drc = design_rules("scn3me_subm")

drc["body_tie_down"] = 0
drc["has_pwell"] = True
drc["has_nwell"] = True


#grid size is 1/2 a lambda
drc["grid"]=0.5*_lambda_
#DRC/LVS test set_up
drc["drc_rules"]=drclvs_home+"/calibreDRC_scn3me_subm.rul"
drc["lvs_rules"]=drclvs_home+"/calibreLVS_scn3me_subm.rul"
drc["layer_map"]=os.environ.get("OPENRAM_TECH")+"/scn3me_subm/layers.map"


# minwidth_tx with contact (no dog bone transistors)
drc["minwidth_tx"] = 4*_lambda_
drc["minlength_channel"] = 2*_lambda_

# 1.3 Minimum spacing between wells of same type (if both are drawn)
drc["well_to_well"] = 6*_lambda_
# 1.4 Minimum spacing between wells of different type (if both are drawn)
drc["pwell_to_nwell"] = 0
# 1.1 Minimum width
drc["minwidth_well"] = 12*_lambda_

# 3.1 Minimum width
drc["minwidth_poly"] = 2*_lambda_
# 3.2 Minimum spacing over active
drc["poly_to_poly"] = 3*_lambda_
# 3.3 Minimum gate extension of active
drc["poly_extend_active"] = 2*_lambda_
# 5.5.b Minimum spacing between poly contact and other poly (alternative rules)
drc["poly_to_polycontact"] = 4*_lambda_
# ??
drc["active_enclosure_gate"] = 0.0
# 3.5 Minimum field poly to active
drc["poly_to_active"] = _lambda_
# 3.2.a Minimum spacing over field poly
drc["poly_to_field_poly"] = 3*_lambda_
# Not a rule
drc["minarea_poly"] = 0.0

# ??
drc["active_to_body_active"] = 4*_lambda_  # Fix me
# 2.1 Minimum width
drc["minwidth_active"] = 3*_lambda_
# 2.2 Minimum spacing
drc["active_to_active"] = 3*_lambda_
# 2.3 Source/drain active to well edge
drc["well_enclosure_active"] = 6*_lambda_
# Reserved for asymmetric enclosures
drc["well_extend_active"] = 6*_lambda_
# Not a rule
drc["minarea_active"] = 0.0

# 4.1 Minimum select spacing to channel of transistor to ensure adequate source/drain width
drc["implant_to_channel"] = 3*_lambda_
# 4.2 Minimum select overlap of active
drc["implant_enclosure_active"] = 2*_lambda_
# 4.3 Minimum select overlap of contact
drc["implant_enclosure_contact"] = _lambda_
# Not a rule
drc["implant_to_contact"] = 0
# Not a rule
drc["implant_to_implant"] = 0
# Not a rule
drc["minwidth_implant"] = 0

# 6.1 Exact contact size
drc["minwidth_contact"] = 2*_lambda_
# 5.3 Minimum contact spacing
drc["contact_to_contact"] = 3*_lambda_
# 6.2.b Minimum active overlap
drc["active_enclosure_contact"] = _lambda_
# Reserved for asymmetric enclosure
drc["active_extend_contact"] = _lambda_
# 5.2.b Minimum poly overlap
drc["poly_enclosure_contact"] = _lambda_
# Reserved for asymmetric enclosures
drc["poly_extend_contact"] = _lambda_
# Reserved for other technologies
drc["contact_to_gate"] = 2*_lambda_
# 5.4 Minimum spacing to gate of transistor
drc["contact_to_poly"] = 2*_lambda_

# 7.1 Minimum width
drc["minwidth_metal1"] = 3*_lambda_
# 7.2 Minimum spacing
drc["metal1_to_metal1"] = 3*_lambda_
# 7.3 Minimum overlap of any contact
drc["metal1_enclosure_contact"] = _lambda_
# Reserved for asymmetric enclosure
drc["metal1_extend_contact"] = _lambda_
# 8.3 Minimum overlap by metal1
drc["metal1_enclosure_via1"] = _lambda_
# Reserve for asymmetric enclosures
drc["metal1_extend_via1"] = _lambda_
# Not a rule
drc["minarea_metal1"] = 0

# 8.1 Exact size
drc["minwidth_via1"] = 2*_lambda_
# 8.2 Minimum via1 spacing
drc["via1_to_via1"] = 3*_lambda_

# 9.1 Minimum width
drc["minwidth_metal2"] = 3*_lambda_
# 9.2 Minimum spacing
drc["metal2_to_metal2"] = 3*_lambda_
# 9.3 Minimum overlap of via1
drc["metal2_extend_via1"] = _lambda_
# Reserved for asymmetric enclosures
drc["metal2_enclosure_via1"] = _lambda_
# 14.3 Minimum overlap by metal2
drc["metal2_extend_via2"] = _lambda_
# Reserved for asymmetric enclosures
drc["metal2_enclosure_via2"] = _lambda_
# Not a rule
drc["minarea_metal2"] = 0

# 14.1 Exact size
drc["minwidth_via2"] = 2*_lambda_
# 14.2 Minimum spacing
drc["via2_to_via2"] = 3*_lambda_

# 15.1 Minimum width
drc["minwidth_metal3"] = 5*_lambda_
# 15.2 Minimum spacing to metal3
drc["metal3_to_metal3"] = 3*_lambda_
# 15.3 Minimum overlap of via 2
drc["metal3_extend_via2"] = 2*_lambda_
# Reserved for asymmetric enclosures
drc["metal3_enclosure_via2"] = 2*_lambda_
# Not a rule
drc["minarea_metal3"] = 0

###################################################
##END DRC/LVS Rules
###################################################

###################################################
##Spice Simulation Parameters
###################################################

# spice model info
spice={}
spice["nmos"]="n"
spice["pmos"]="p"
# This is a map of corners to model files
SPICE_MODEL_DIR=os.environ.get("SPICE_MODEL_DIR")
spice["fet_models"] = { "TT" : [SPICE_MODEL_DIR+"/nom/pmos.sp",SPICE_MODEL_DIR+"/nom/nmos.sp"],
                        "FF" : [SPICE_MODEL_DIR+"/ff/pmos.sp",SPICE_MODEL_DIR+"/ff/nmos.sp"],
                        "FS" : [SPICE_MODEL_DIR+"/ff/pmos.sp",SPICE_MODEL_DIR+"/ss/nmos.sp"],
                        "SF" : [SPICE_MODEL_DIR+"/ss/pmos.sp",SPICE_MODEL_DIR+"/ff/nmos.sp"],
                        "SS" : [SPICE_MODEL_DIR+"/ss/pmos.sp",SPICE_MODEL_DIR+"/ss/nmos.sp"],
                        "ST" : [SPICE_MODEL_DIR+"/ss/pmos.sp",SPICE_MODEL_DIR+"/nom/nmos.sp"],
                        "TS" : [SPICE_MODEL_DIR+"/nom/pmos.sp",SPICE_MODEL_DIR+"/ss/nmos.sp"],
                        "FT" : [SPICE_MODEL_DIR+"/ff/pmos.sp",SPICE_MODEL_DIR+"/nom/nmos.sp"],
                        "TF" : [SPICE_MODEL_DIR+"/nom/pmos.sp",SPICE_MODEL_DIR+"/ff/nmos.sp"],
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
spice["nom_threshold"] = 1.3   # Typical Threshold voltage in Volts
# FIXME: These need to be updated for SCMOS, they are copied from FreePDK45.
spice["wire_unit_r"] = 0.075    # Unit wire resistance in ohms/square
spice["wire_unit_c"] = 0.64     # Unit wire capacitance ff/um^2
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
spice["nor2_leakage"] = 1        # Leakage power of 2-input nor in nW
spice["dff_leakage"] = 1      # Leakage power of flop in nW

spice["default_event_frequency"] = 100         # Default event activity of every gate. MHz

#Logical Effort relative values for the Handmade cells
parameter["le_tau"] = 23                     #In pico-seconds.
parameter["min_inv_para_delay"] = 0.73        #In relative delay units
parameter["cap_relative_per_ff"] = 0.91       #Units of Relative Capacitance/ Femto-Farad
parameter["dff_clk_cin"] = 27.5              #In relative capacitance units
parameter["6tcell_wl_cin"] = 2               #In relative capacitance units
parameter["sa_en_pmos_size"] = 24*_lambda_
parameter["sa_en_nmos_size"] = 9*_lambda_
parameter["sa_inv_pmos_size"] = 18*_lambda_
parameter["sa_inv_nmos_size"] = 9*_lambda_
parameter["bitcell_drain_cap"] = 0.2        #In Femto-Farad, approximation of drain capacitance

###################################################
##END Spice Simulation Parameters
###################################################

###################################################
##BEGIN Technology Tool Preferences
###################################################

drc_name = "magic"
lvs_name = "netgen"
pex_name = "magic"

###################################################
##END Technology Tool Preferences
###################################################
array_row_multiple = 1
array_col_multiple = 1
