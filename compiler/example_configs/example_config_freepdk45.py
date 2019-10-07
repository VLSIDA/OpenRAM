word_size = 2
num_words = 16

tech_name = "freepdk45"
process_corners = ["TT"]
supply_voltages = [1.0]
temperatures = [25]

route_supplies = True
check_lvsdrc = True

output_path = "temp"
output_name = "sram_{0}_{1}_{2}".format(word_size,
                                        num_words,
                                        tech_name)

