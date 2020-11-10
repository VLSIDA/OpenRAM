word_size = 32
num_words = 512
write_size = 8

local_array_size = 16

num_rw_ports = 1
num_r_ports = 0
num_w_ports = 0

tech_name = "sky130"
nominal_corner_only = True

route_supplies = False
check_lvsdrc = True
perimeter_pins = False
#netlist_only = True
#analytical_delay = False
output_path = "macros/sram_1rw_{0}_{1}_{2}_{3}".format(word_size,
                                                       num_words,
                                                       write_size,
                                                       tech_name)
output_name = "sram_1rw_{0}_{1}_{2}_{3}".format(word_size,
                                                num_words,
                                                write_size,
                                                tech_name)
