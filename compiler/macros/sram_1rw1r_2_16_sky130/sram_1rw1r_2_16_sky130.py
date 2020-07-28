word_size = 2
num_words = 16
#write_size = 2

num_rw_ports = 1
num_r_ports = 1
num_w_ports = 0

tech_name = "sky130"
nominal_corners_only = True

route_supplies = True
check_lvsdrc = True
perimeter_pins = True
#netlist_only = True
#analytical_delay = False
purge_temp = False
spice_name = "ngspice"
# The spice executable being used which is derived from the user PATH.
spice_exe = "ngspice"
# Variable to select the variant of drc, lvs, pex
drc_name = "magic"
lvs_name = "netgen"
pex_name = "magic"
# The DRC/LVS/PEX executable being used
# which is derived from the user PATH.
drc_exe = "magic"
lvs_exe = "netgen"
pex_exe = "magic"
output_path = "macros/sram_1rw1r_{0}_{1}_{2}".format(word_size,
	                                                 num_words,
 #                                                        write_size,
                                                         tech_name)
output_name = "sram_1rw1r_{0}_{1}_{2}".format(word_size,
                                                  num_words,
  #                                                write_size,
                                                  tech_name)

