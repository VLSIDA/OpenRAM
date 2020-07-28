# Data word size
word_size = 32
# Number of words in the memory
num_words = 256

# Technology to use in $OPENRAM_TECH
# tech_name = "scn4m_subm"
tech_name = "sky130"

# You can use the technology nominal corner only
nominal_corner_only = True
# Or you can specify particular corners
# Process corners to characterize
# process_corners = ["SS", "TT", "FF"]
# Voltage corners to characterize
# supply_voltages = [ 3.0, 3.3, 3.5 ]
# Temperature corners to characterize
# temperatures = [ 0, 25 100]

# Output directory for the results
output_path = "temp"
# Output file base name
output_name = "sram_{0}_{1}_{2}".format(word_size,num_words,tech_name)

# Disable analytical models for full characterization (WARNING: slow!)
# analytical_delay = False

write_size = 8
num_rw_ports = 1
num_r_ports = 1
num_w_ports = 0


# route_supplies = True
check_lvsdrc = True
# perimeter_pins = True
#netlist_only = True

drc_name = "magic"
