word_size = 2
num_words = 16

bitcell = "bitcell_1rw_1r"
replica_bitcell = "replica_bitcell_1rw_1r"
num_rw_ports = 1
num_r_ports = 1
num_w_ports = 0

tech_name = "scn4m_subm"
process_corners = ["TT"]
supply_voltages = [5.0]
temperatures = [25,50]

output_path = "temp"
output_name = "sram_1rw_1r_{0}_{1}_{2}".format(word_size,num_words,tech_name)

drc_name = "magic"
lvs_name = "netgen"
pex_name = "magic"
