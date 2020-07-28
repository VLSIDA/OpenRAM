word_size = 32
num_words = 32
num_rw_ports = 1
num_r_ports = 1
num_w_ports = 0
tech_name = "sky130"
nominal_corners_only = True
route_supplies = True
check_lvsdrc = True
perimeter_pins = True
netlist_only = False
# analytical_delay = False
output_path = "riscv-{}".format(tech_name)
output_name = "sram_1rw1r_{0}_{1}_{2}".format(word_size,
                                                  num_words,
                                                  tech_name)
