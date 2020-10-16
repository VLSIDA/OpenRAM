word_size = 2
num_words = 16

tech_name = "freepdk45"
nominal_corners_only = False
process_corners = ["TT"]
supply_voltages = [1.0]
temperatures = [25]

route_supplies = False
check_lvsdrc = True
# nominal_corners_only = True
load_scales = [0.5, 1, 4]
slew_scales = [0.5, 1]

output_path = "temp"
output_name = "sram_{0}_{1}_{2}".format(word_size,
                                        num_words,
                                        tech_name)

