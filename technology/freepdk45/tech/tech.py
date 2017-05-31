import os

"""
File containing the process technology parameters.
"""

info = {}
info["name"] = "freepdk45"
info["body_tie_down"] = 0
info["has_pwell"] = True
info["has_nwell"] = True

#GDS file info
GDS = {}
# gds units
GDS["unit"] = (0.0005,1e-9)
# default label zoom
GDS["zoom"] = 0.05

#####################################################################################################
##GDS Layer Map######################################################################################
#####################################################################################################

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

#####################################################################################################
##END GDS Layer Map##################################################################################
#####################################################################################################

#####################################################################################################
##DRC/LVS Rules Setup################################################################################
#####################################################################################################

#technology parameter
parameter={}
parameter["min_tx_size"] = 0.09
parameter["pinv_beta"] = 3

drclvs_home=os.environ.get("DRCLVS_HOME")
drc={}
#grid size
drc["grid"] = 0.0025

#DRC/LVS test set_up
drc["drc_rules"]=drclvs_home+"/calibreDRC.rul"
drc["lvs_rules"]=drclvs_home+"/calibreLVS.rul"
drc["xrc_rules"]=drclvs_home+"/calibrexRC.rul"
drc["layer_map"]=os.environ.get("OPENRAM_TECH")+"/freepdk45/layers.map"

# minwidth_tx withcontact
drc["minwidth_tx"]=0.09
drc["minlength_channel"] = 0.05

#well rules
drc["pwell_enclose_nwell"] = 0.225
drc["minwidth_well"] = 0.2

#poly rules
drc["minwidth_poly"] = 0.05
drc["minheight_poly"] = 0.0
drc["poly_to_poly"] = 0.14
drc["poly_extend_active"] = 0.055
drc["active_enclosure_gate"] = 0.07
drc["poly_to_active"] = 0.05
drc["poly_to_field_poly"] = 0.075
drc["minarea_poly"] = 0.0

#active
drc["active_extend_gate"] = 0
drc["active_to_body_active"] = 0.08
drc["minwidth_active"] = 0.09
drc["minheight_active"] = 0.09
drc["minarea_active"] = 0
drc["well_enclosure_active"] = 0.055
drc["well_extend_active"] = 0.055


#Implant
drc["implant_to_gate"] = 0.07
drc["implant_to_channel"] = 0.07
drc["implant_to_contact"] = 0.025
drc["implant_to_implant"] = 0.045
drc["minwidth_implant"] = 0.045

#Contact
drc["minwidth_contact"] = 0.065
drc["contact_to_contact"] = 0.075
drc["active_enclosure_contact"] = 0.005
drc["active_extend_contact"] = 0.005
drc["poly_enclosure_contact"] = 0.005
drc["poly_extend_contact"] = 0.005
drc["contact_to_poly"] = 0.0375 #changed from 0.035

#Metal1
drc["minwidth_metal1"] = 0.065
drc["minheight_metal1"] = 0.0
drc["metal1_to_metal1"] = 0.065
drc["metal1_enclosure_contact"] = 0
drc["metal1_extend_contact"] = 0.035
drc["metal1_extend_via1"] = 0.035
drc["metal1_enclosure_via1"] = 0
drc["minarea_metal1"] = 0

#via1
drc["minwidth_via1"] = 0.065
drc["via1_to_via1"] = 0.075

#Metal2
drc["minwidth_metal2"] = 0.07
drc["minheight_metal2"] = 0.0
drc["metal2_to_metal2"] = 0.07
drc["metal2_extend_via1"] = 0.035
drc["metal2_enclosure_via1"] = 0
drc["metal2_extend_via2"] = 0.035
drc["metal2_enclosure_via2"] = 0
drc["minarea_metal2"] = 0

#Via2
drc["minwidth_via2"] = 0.065
drc["via2_to_via2"] = 0.075

#Metal3
drc["minwidth_metal3"] = 0.07
drc["minheight_metal3"] = 0.0
drc["metal3_to_metal3"] = 0.07
drc["metal3_extend_via2"] = 0.035
drc["metal3_enclosure_via2"] = 0 
drc["metal3_extend_via3"]=0.035
drc["metal3_enclosure_via3"] = 0 
drc["minarea_metal3"] = 0

#Via3
drc["minwidth_via3"] = 0.065
drc["via3_to_via3"] = 0.07

#Metal4
drc["minwidth_metal4"] = 0.14
drc["minheight_metal4"] = 0.0
drc["metal4_enclosure_via3"] = 0 
drc["metal4_extend_via3"] = 0.07
drc["metal4_to_metal4"] = 0.14
drc["metal4_extend_via4"] = 0.07
drc["metal4_enclosure_via4"] = 0.07
drc["minarea_metal4"] = 0

#Via4
drc["minwidth_via4"] = 0.14
drc["via4_to_via4"] = 0.14

#Metal5
drc["minwidth_metal5"] = 0.14
drc["minheight_metal5"] = 0.0
drc["metal5_to_metal5"] = 0.14
drc["metal5_extend_via4"] = 0.07
drc["metal5_enclosure_via4"] = 0.07
drc["minarea_metal5"] = 0

#Via 5
drc["minwidth_via5"] = 0.14
drc["via5_to_via5"] = 0.14

#Metal6
drc["minwidth_metal6"] = 0.14
drc["minheight_metal6"] = 0.0
drc["metal6_to_metal6"] = 0.14
drc["metal6_extend_via5"] = 0
drc["metal6_enclosure_via5"] = 0

#Via 6
drc["minwidth_via6"] = 0.14
drc["via6_to_via6"] = 0.14

#Metal7
drc["minwidth_metal7"] = 0.14
drc["minheight_metal7"] = 0.0
drc["metal7_to_metal7"] = 0.14
drc["metal7_extend_via6"] = 0
drc["metal7_enclosure_via6"] = 0

#Via7
drc["minwidth_via7"] = 0.14
drc["via7_to_via7"] = 0.14

#Metal8
drc["minwidth_metal8"] = 0.14
drc["minheight_metal8"] = 0.0
drc["metal8_to_metal8"] = 0.14
drc["metal8_extend_via7"] = 0
drc["metal8_enclosure_via7"] = 0

#Via8
drc["minwidth_via8"] = 0.14
drc["via8_to_via8"] = 0.14

#Metal9
drc["minwidth_metal9"] = 0.14
drc["minheight_metal9"] = 0.0
drc["metal9_to_metal9"] = 0.14
drc["metal9_extend_via8"] = 0
drc["metal9_enclosure_via8"] = 0

#Via 9
drc["minwidth_via9"] = 0.14
drc["via9_to_via9"] = 0.14

#Metal 10
drc["minwidth_metal10"] = 0.14
drc["minheight_metal10"] = 0.0
drc["metal10_to_metal10"] = 0.14
drc["metal10_extend_via9"] = 0
drc["metal10_enclosure_via9"] = 0

#####################################################################################################
##END DRC/LVS Rules##################################################################################
#####################################################################################################

#####################################################################################################
##Spice Simulation Parameters########################################################################
#####################################################################################################

#spice info
spice = {}
spice["nmos"] = "nmos_vtg"
spice["pmos"] = "pmos_vtg"
SPICE_MODEL_DIR=os.environ.get("SPICE_MODEL_DIR")
spice["fet_models"] = [SPICE_MODEL_DIR+"/NMOS_VTG.inc",
                       SPICE_MODEL_DIR+"/PMOS_VTG.inc"]

#spice stimulus related variables
spice["clock_period"] = 2.0
spice["supply_voltage"] = 1.0        #vdd in [Volts]
spice["gnd_voltage"] = 0.0           #gnd in [Volts]
spice["rise_time"] = 0.001           #rise time in [Nano-seconds]
spice["fall_time"] = 0.001           #fall time in [Nano-seconds]
spice["temp"] = 25                   #temperature in [Celsius]

#parasitics of metal for bit/word lines
spice["bitline_res"] = 0.1           #bitline resistance in [Ohms/micro-meter]
spice["bitline_cap"] = 0.2           #bitline capacitance in [Femto-farad/micro-meter]
spice["wordline_res"] = 0.1          #wordline resistance in [Ohms/micro-meter]
spice["wordline_cap"] = 0.2          #wordline capacitance in [Femto-farad/micro-meter]
spice["FF_in_cap"] = 0.2091        #Input capacitance of ms_flop (Din) [Femto-farad]
spice["tri_gate_out_cap"] = 0.41256         #Output capacitance of tri_gate (tri_out) [Femto-farad]


#sram signal names
spice["vdd_name"] = "vdd"
spice["gnd_name"] = "gnd"
spice["control_signals"] = ["CSb", "WEb", "OEb"]
spice["data_name"] = "DATA"
spice["addr_name"] = "ADDR"
spice["pmos_name"] = spice["pmos"]
spice["nmos_name"] = spice["nmos"]
spice["minwidth_tx"] = drc["minwidth_tx"]
spice["channel"] = drc["minlength_channel"]
spice["clk"] = "clk"

# estimated feasible period in ns
spice["feasible_period"] = 5

# analytical delay parameter
spice["wire_unit_r"] = 0.075 #ohm 
spice["wire_unit_c"] = 0.64 #ff/um^2
spice["min_tx_r"] = 9250.0
spice["min_tx_c_para"] = 0.7 #ff
spice["min_tx_gate_c"] = 0.2
spice["msflop_delay"] = 20.5171565446#ps
spice["msflop_slope"] = 13.0801872972#ps
