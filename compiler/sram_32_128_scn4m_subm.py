word_size = 32
num_words = 128

tech_name = "scn4m_subm"
process_corners = ["TT"]
supply_voltages = [5.0]
temperatures = [25]

route_supplies = True
check_lvsdrc = True
netlist_only = True
output_name = "sram_{0}_{1}_{2}".format(word_size,
                                        num_words,
                                        tech_name)

drc_name = "magic"
lvs_name = "netgen"
pex_name = "magic"
