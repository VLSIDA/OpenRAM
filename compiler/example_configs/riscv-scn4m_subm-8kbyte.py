word_size = 32
num_words = 2048
write_size = 8

local_array_size = 32

num_rw_ports = 1
num_r_ports = 1
num_w_ports = 0

tech_name = "scn4m_subm"
nominal_corners_only = True

route_supplies = False
check_lvsdrc = False
perimeter_pins = False
#netlist_only = True
#analytical_delay = False
output_path = "macros/sram_1rw1r_{0}_{1}_{2}_{3}".format(word_size,
                                                         num_words,
                                                         write_size,
                                                         tech_name)
output_name = "sram_1rw1r_{0}_{1}_{2}_{3}".format(word_size,
                                                  num_words,
                                                  write_size,
                                                  tech_name)
