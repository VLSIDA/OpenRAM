word_size = 2
num_words = 16

tech_name = "freepdk45"
process_corners = ["TT"]
supply_voltages = [1.0]
temperatures = [25]

output_path = "temp"
output_name = "sram_{0}_{1}_{2}_{3}".format(word_size,num_words,num_banks,tech_name)

#Below are some additions to test additional ports on sram
#bitcell = "pbitcell"

# These are the configuration parameters
#rw_ports = 2
#r_ports = 2
#w_ports = 2
