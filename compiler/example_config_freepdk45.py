word_size = 2
num_words = 16

tech_name = "freepdk45"
process_corners = ["TT"]
supply_voltages = [1.0]
temperatures = [25]

output_path = "temp"
output_name = "sram_{0}_{1}_{2}".format(word_size,num_words,tech_name)

#Setting for multiport
# netlist_only = True
# num_rw_ports = 1
# num_r_ports = 1
# num_w_ports = 0

#Pbitcell modules for multiport
#bitcell = "pbitcell"
#replica_bitcell="replica_pbitcell"

#Custom 1rw+1r multiport cell. Set the above port numbers to rw = 1, r = 1, w = 0
# bitcell = "bitcell_1rw_1r"
# replica_bitcell = "replica_bitcell_1rw_1r"
