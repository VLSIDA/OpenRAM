word_size = 2
num_words = 16

num_rw_ports = 2
num_r_ports = 0
num_w_ports = 0

tech_name = "scn4m_subm"
nominal_corner_only = False
process_corners = ["TT"]
supply_voltages = [5.0]
temperatures = [25]

route_supplies = False
check_lvsdrc = True

output_name = "sram_{0}rw{1}r{2}w_{3}_{4}_{5}".format(num_rw_ports,
                                                      num_r_ports,
                                                      num_w_ports,
                                                      word_size,
                                                      num_words,
                                                      tech_name)
output_path = "macro/{}".format(output_name)

