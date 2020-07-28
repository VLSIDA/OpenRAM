###################
# Configuration options
###################
# This is the technology directory.
# openram_tech = ""
# This is the name of the technology.
tech_name = "sky130"
# tech_name = "scn4m_subm"
# Port configuration (1-2 ports allowed)
num_rw_ports = 1
num_r_ports = 1
num_w_ports = 0
# Write mask size, default will be overwritten with word_size if not user specified
write_size = 8
# These will get initialized by the user or the tech file
nominal_corner_only = True
# Or you can specify particular corners
# Process corners to characterize
# process_corners = ["SS", "TT", "FF"]

# Voltage corners to characterize
# supply_voltages = [ 3.0, 3.3, 3.5 ]

# Temperature corners to characterize
# temperatures = [ 0, 25 100]

# Size parameters must be specified by user in config file.
# Data word size
num_words = 256 
# Number of words in the memory
word_size = 32  
# You can manually specify banks, but it is better to auto-detect it.
num_banks = 1
num_spare_rows = 0
# num_spare_cols = 0
###################
# Optimization options
###################
# Approximate percentage of delay compared to bitlines
rbl_delay_percentage = 0.5
# Allow manual adjustment of the delay chain over automatic
use_tech_delay_chain_size = False
delay_chain_stages = 9
delay_chain_fanout_per_stage = 4
accuracy_requirement = 0.75
###################
# Debug options.
###################
# This is the temp directory where all intermediate results are stored.
# try:
# If user defined the temporary location in their environment, use it
# openram_temp = os.path.abspath(os.environ.get("OPENRAM_TMP"))
#except:
# Else use a unique temporary directory
#    openram_temp = "/tmp/"
# This is the verbosity level to control debug information. 0 is none, 1
# is minimal, etc.
# debug_level = 0
###################
# Run-time vs accuracy options.
# Default, sacrifice accuracy/completeness for speed.
# Must turn on options for verification, final routing, etc.
###################
# When enabled, layout is not generated (and no DRC or LVS are performed)
netlist_only = True
# Whether we should do the final power routing
route_supplies = True
# This determines whether LVS and DRC is checked at all.
check_lvsdrc = False
# This determines whether LVS and DRC is checked for every submodule.
inline_lvsdrc = False
# Remove noncritical memory cells for characterization speed-up
trim_netlist = False
# Run with extracted parasitics
use_pex = False
###################
# Tool options
###################
# Variable to select the variant of spice
spice_name = "ngspice"
# The spice executable being used which is derived from the user PATH.
spice_exe = "ngspice"
# Variable to select the variant of drc, lvs, pex
drc_name = "magic"
lvs_name = "netgen"
pex_name = "magic"
# The DRC/LVS/PEX executable being used
# which is derived from the user PATH.
drc_exe = "magic"
lvs_exe = "netgen"
pex_exe = "magic"
# For sky130, we need magic for filtering.
magic_exe = "magic"
# Should we print out the banner at startup
print_banner = True
# Define the output file paths
output_path = "runs"
# Define the output file base name
output_name = "sram_{0}_{1}_{2}".format(word_size,num_words,tech_name)
# Use analytical delay models by default
# rather than (slow) characterization
analytical_delay = False
# Purge the temp directory after a successful
# run (doesn't purge on errors, anyhow)
# Route the input/output pins to the perimeter
perimeter_pins = True

purge_temp = True
# These are the default modules that can be over-riden
bitcell_suffix = ""
bank_select = "bank_select"
bitcell_array = "bitcell_array"
bitcell = "bitcell"
column_mux_array = "single_level_column_mux_array"
control_logic = "control_logic"
decoder = "hierarchical_decoder"
delay_chain = "delay_chain"
dff_array = "dff_array"
dff = "dff"
inv_dec = "pinv"
nand2_dec = "pnand2"
nand3_dec = "pnand3"
nand4_dec = "pnand4" # Not available right now
precharge_array = "precharge_array"
ptx = "ptx"
replica_bitline = "replica_bitline"
sense_amp_array = "sense_amp_array"
sense_amp = "sense_amp"
tri_gate_array = "tri_gate_array"
tri_gate = "tri_gate"
wordline_driver = "wordline_driver"
write_driver_array = "write_driver_array"
write_driver = "write_driver"
write_mask_and_array = "write_mask_and_array"

use_calibre = False

