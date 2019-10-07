word_size = 2
num_words = 16

num_rw_ports = 1
num_r_ports = 1
num_w_ports = 0

tech_name = "scn4m_subm"
process_corners = ["TT"]
supply_voltages = [5.0]
temperatures = [25]

route_supplies = True
check_lvsdrc = True

output_path = "temp"
output_name = "sram_1w_1r_{0}_{1}_{2}".format(word_size,
                                              num_words,
                                              tech_name)

drc_name = "magic"
lvs_name = "netgen"
pex_name = "magic"
