word_size = 32
num_words = 2048
write_size = 8

local_array_size = 32

num_rw_ports = 1
num_r_ports = 1
num_w_ports = 0

tech_name = "freepdk45"
nominal_corner_only = True

route_supplies = False
check_lvsdrc = False
perimeter_pins = False
#netlist_only = True
#analytical_delay = False

output_name = "sram_{0}rw{1}r{2}w_{3}_{4}_{5}".format(num_rw_ports,
                                                      num_r_ports,
                                                      num_w_ports,
                                                      word_size,
                                                      num_words,
                                                      tech_name)
output_path = "macro/{}".format(output_name)
