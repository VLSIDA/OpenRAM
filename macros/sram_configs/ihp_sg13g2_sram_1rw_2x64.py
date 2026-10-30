"""Foundry-cell SG13G2 bring-up; run inside IIC-OSIC with this PDK selected."""

tech_name = "ihp_sg13g2"
word_size = 2
num_words = 64
words_per_row = 4
num_banks = 1
num_rw_ports = 1
num_r_ports = num_w_ports = 0

# Use the installed container tools and actual transistor simulation. The
# imported SRAM topology has no validated trimming or PEX integration yet.
use_nix = False
analytical_delay = False
spice_name = "ngspice"
num_sim_threads = 1
trim_netlist = False
use_pex = False
check_lvsdrc = False  # Use technology/ihp_sg13g2/tests/verify_array.py explicitly.

process_corners = ["TT"]
supply_voltages = [1.2]
temperatures = [27]
use_specified_corners = [("TT", 1.2, 27)]
nominal_corner_only = False
load_scales = [1, 4]
slew_scales = [1, 2]

output_name = "ihp_sg13g2_sram_1rw_2x64"
output_path = "macro/" + output_name
