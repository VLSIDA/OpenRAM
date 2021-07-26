# Include with
#   import os
#   exec(open(os.path.join(os.path.dirname(__file__), 'sky130_sram_common.py')).read())


tech_name = "sky130"
nominal_corner_only = True

# Local wordlines have issues with met3 power routing for now
#local_array_size = 16

route_supplies = "ring"
#route_supplies = "left"
check_lvsdrc = True
uniquify = True
#perimeter_pins = False
#netlist_only = True
#analytical_delay = False

output_name = "{tech_name}_sram_{human_byte_size}_{ports_human}_{word_size}x{num_words}_{write_size}".format(**locals())
output_path = "macro/{output_name}".format(**locals())
