word_size = 64
num_words = 64

num_rw_ports = 1
num_r_ports = 0
num_w_ports = 0
num_banks = 1
words_per_row = 1
spice_name = "hspice"


tech_name = "freepdk45"
process_corners = ["TT"]
supply_voltages = [1.0]
temperatures = [25]

route_supplies = True
perimeter_pins = False
check_lvsdrc = True
nominal_corner_only = True
load_scales = [0.5]
slew_scales = [0.5]
use_pex = False
analytical_delay = False

output_name = "sram_w_{0}_{1}_{2}".format(word_size, num_words, tech_name)
output_path = "macro/{}".format(output_name)

