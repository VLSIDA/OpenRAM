import os

"""
Class containing the process technology parameters.
"""
info={}
info["name"]="scn3me_subm"
info["body_tie_down"] = 0
info["has_pwell"] = True
info["has_nwell"] = True

#GDS file info
GDS={}
# gds units
GDS["unit"]=(0.001,1e-6)  
# default label zoom
GDS["zoom"] = 0.5

#####################################################################################################
##GDS Layer Map######################################################################################
#####################################################################################################

# create the GDS layer map
layer={} 
layer["vtg"]            = -1 
layer["vth"]            = -1 
layer["contact"]        = 25 
layer["pwell"]          = 41 
layer["nwell"]          = 42 
layer["active"]         = 43 
layer["pimplant"]       = 44
layer["nimplant"]       = 45
layer["poly"]           = 46 
layer["poly_contact"]   = 47
layer["active_contact"] = 48
layer["metal1"]         = 49 
layer["via1"]           = 50 
layer["metal2"]         = 51 
layer["via2"]           = 61 
layer["metal3"]         = 62 
layer["text"]           = 83 
layer["boundary"]       = 83 

#####################################################################################################
##END GDS Layer Map##################################################################################
#####################################################################################################

#####################################################################################################
##DRC/LVS Rules Setup################################################################################
#####################################################################################################

#technology parameter
parameter={}
parameter["min_tx_size"] = 1.2
parameter["pinv_beta"] = 2 #for use in pinv

drclvs_home=os.environ.get("DRCLVS_HOME")

drc={}
#grid size
drc["grid"]=0.15
#DRC/LVS test set_up
drc["drc_rules"]=drclvs_home+"/calibreDRC_scn3me_subm.rul"
drc["lvs_rules"]=drclvs_home+"/calibreLVS_scn3me_subm.rul"
drc["layer_map"]=os.environ.get("OPENRAM_TECH")+"/scn3me_subm/layers.map"

        	      					
# minwidth_tx withcontact
drc["minwidth_tx"] = 1.2                       
drc["minlength_channel"] = 0.6 

#well rules
drc["pwell_enclose_nwell"] = 0                                     
drc["minwidth_well"] = 3.6                                                                      

#poly rules
drc["minwidth_poly"] = 0.6          
drc["minheight_poly"] = 0.0
drc["poly_to_poly"] = 0.9          
drc["poly_extend_active"] = 0.6   
drc["poly_to_polycontact"] = 1.2                
drc["active_enclosure_gate"] = 0.0             
drc["poly_to_active"] = 0.3         
drc["minarea_poly"] = 0.0

#active
drc["active_extend_gate"] = 0                    
drc["active_to_body_active"] = 1.2  # Fix me              
drc["minwidth_active"] = 0.9   
drc["minheight_active"] = 0.9  
drc["minarea_active"] = 0.0
drc["active_to_active"] = 0.9                   
drc["well_enclosure_active"] = 1.8
drc["well_extend_active"] = 1.8

#Implant (None in IBM)
drc["implant_to_gate"] = 0                       
drc["implant_to_channel"] = 0                    
drc["implant_to_contact"] = 0
drc["implant_to_implant"] = 0
drc["minwidth_implant"] = 0

#Contact
drc["minwidth_contact"] = 0.6
drc["minwidth_active_contact"] = 0.6              
drc["minwidth_poly_contact"] = 0.6 

drc["active_enclosure_contact"] = 0.3   
drc["active_extend_contact"] = 0.3
drc["poly_enclosure_contact"] = 0.3              
drc["poly_extend_contact"] = 0.3        
drc["contact_to_poly"] = 0.6

drc["contact_to_contact"] = 0.9                    
drc["active_contact_to_active_contact"] = 0.9     
drc["poly_contact_to_poly_contact"] = 0.9

        
drc["active_extend_active_contact"] = 0.3         
drc["poly_extend_poly_contact"] = 0.3             
drc["active_enclosure_active_contact"] = 0.3      
drc["poly_enclosure_poly_contact"] = 0.3          

#Metal1
drc["minwidth_metal1"] = 0.9    
drc["minheight_metal1"] = 0   
drc["metal1_to_metal1"] = 0.9                       
drc["metal1_to_contact"] = 0.9                    
drc["metal1_enclosure_contact"] = 0.3             
drc["metal1_extend_contact"] = 0.3               
drc["metal1_extend_via1"] = 0.3                   
drc["metal1_enclosure_via1"] = 0.3                
drc["minarea_metal1"] = 0
drc["metal1_enclosure_active_contact"] = 0.3      
drc["metal1_enclosure_poly_contact"] = 0.3       
drc["metal1_extend_active_contact"] = 0.3        
drc["metal1_extend_poly_contact"] = 0.3           

#via1
drc["minwidth_via1"] = 0.6 
drc["via1_to_via1"] = 0.6               
drc["minselect_overlap_via1"] = 0.3    # Fix me           

#Metal2
drc["minwidth_metal2"] = 0.9  
drc["minheight_metal2"] = 0
drc["metal2_to_metal2"] = 0.9 
drc["metal2_extend_via1"] = 0.3   
drc["metal2_enclosure_via1"] = 0.3
drc["metal2_extend_via2"] = 0.3
drc["metal2_enclosure_via2"] = 0.3
drc["minarea_metal2"] = 0

#Via2
drc["minwidth_via2"] = 0.6  
drc["via2_to_via2"] = 0.9    

#Metal3
drc["minwidth_metal3"] = 1.5                     
drc["minheight_metal3"] = 0.0
drc["metal3_to_metal3"] = 0.9                     
drc["metal3_extend_via2"] = 0.6  
drc["metal3_enclosure_via2"] = 0.6 
drc["minarea_metal3"] = 0

#####################################################################################################
##END DRC/LVS Rules##################################################################################
#####################################################################################################

#####################################################################################################
##Spice Simulation Parameters########################################################################
#####################################################################################################

# spice model info
spice={}
spice["nmos"]="n"
spice["pmos"]="p"
spice["fet_models"] = [os.environ.get("SPICE_MODEL_DIR")+"/on_c5n.sp"]

#spice stimulus related variables
spice["clock_period"] = 10.0
spice["supply_voltage"] = 5.0        #vdd in [Volts]
spice["gnd_voltage"] = 0.0           #gnd in [Volts]
spice["rise_time"] = 0.001           #rise time in [Nano-seconds]
spice["fall_time"] = 0.001           #fall time in [Nano-seconds]
spice["temp"] = 25                   #temperature in [Celsius]

#parasitics of metal for bit/word lines
spice["bitline_res"] = 0.1           #bitline resistance in [Ohms/micro-meter]
spice["bitline_cap"] = 0.2           #bitline capacitance in [Femto-farad/micro-meter]
spice["wordline_res"] = 0.1          #wordline resistance in [Ohms/micro-meter]
spice["wordline_cap"] = 0.2          #wordline capacitance in [Femto-farad/micro-meter]
spice["FF_in_cap"] = 9.8242         #Input capacitance of ms_flop (Din) [Femto-farad]
spice["tri_gate_out_cap"] = 1.4980         #Output capacitance of tri_gate (tri_out) [Femto-farad]


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
# these numbers are copied from freepdk
# need to measure them in scn cmos
spice["wire_unit_r"] = 0.075 #ohm 
spice["wire_unit_c"] = 0.64 #ff/um^2
spice["min_tx_r"] = 9250.0
spice["min_tx_c_para"] = 0.7 #ff
spice["min_tx_gate_c"] = 0.1
spice["msflop_delay"] = 20.5171565446#ps
spice["msflop_slope"] = 13.0801872972#ps
