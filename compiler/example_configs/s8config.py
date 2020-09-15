word_size = 16
num_words = 16

num_rw_ports = 1
num_r_ports = 0
num_w_ports = 0

tech_name = "sky130"



accuracy_requirement = 0.05
magic_exe = ("magic", "magic")
nominal_corners_only = False
process_corners = ["TT"]
supply_voltages = [5.0]
temperatures = [25]

netlist_only = False
route_supplies = "grid"
check_lvsdrc = False

#replica_bitcell_array = "/home/jesse/openram/technology/sky130/modules/replica_bitcell_array.py"

output_path = "sram_" + str(accuracy_requirement)
output_name = "sram_{0}_{1}_{2}_{3}".format(word_size,
                                        num_words,
                                        tech_name,
                                        accuracy_requirement
                                        )
write_size=8
