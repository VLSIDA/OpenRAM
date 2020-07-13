word_size = 4
num_words = 64
words_per_row = 2

num_rw_ports = 1
num_r_ports = 0
num_w_ports = 0

tech_name = "scn4m_subm"
nominal_corners_only = False
process_corners = ["TT"]
supply_voltages = [5.0]
temperatures = [25]

# route_supplies = True
check_lvsdrc = True

output_path = "temp"
output_name = "sram_1rw_{0}_{1}_{2}".format(word_size,
                                            num_words,
                                            tech_name)
