import optparse
import getpass 
import os

class options(optparse.Values):
    """
    Class for holding all of the OpenRAM options. All of these options can be over-riden in a configuration file
    that is the sole required command-line positional argument for openram.py.
    """

    # This is the technology directory.
    openram_tech = ""
    # This is the name of the technology.
    tech_name = ""
    # This is the temp directory where all intermediate results are stored.
    openram_temp = "/tmp/openram_{0}_{1}_temp/".format(getpass.getuser(),os.getpid())
    #openram_temp = "/Users/{}/openram_temp/".format(getpass.getuser())
    # This is the verbosity level to control debug information. 0 is none, 1
    # is minimal, etc.
    debug_level = 0
    # This determines whether  LVS and DRC is checked for each submodule.
    check_lvsdrc = True
    # Variable to select the variant of spice
    spice_name = ""
    # Should we print out the banner at startup
    print_banner = True
    # The DRC/LVS/PEX executable being used which is derived from the user PATH.
    drc_exe = None
    lvs_exe = None
    pex_exe = None
    # The spice executable being used which is derived from the user PATH.
    spice_exe = ""
    # Run with extracted parasitics
    use_pex = False
    # Remove noncritical memory cells for characterization speed-up
    trim_netlist = True
    # Use detailed LEF blockages
    detailed_blockages = True
    # Define the output file paths
    output_path = "."
    # Define the output file base name
    output_name = ""
    # Use analytical delay models by default rather than (slow) characterization
    analytical_delay = True
    # Purge the temp directory after a successful run (doesn't purge on errors, anyhow)
    purge_temp = True

    # These are the configuration parameters
    rw_ports = 1
    r_ports = 0
    # These will get initialized by the the file
    supply_voltages = ""
    temperatures = ""
    process_corners = ""
    

    # These are the default modules that can be over-riden
    decoder = "hierarchical_decoder"
    ms_flop = "ms_flop"
    ms_flop_array = "ms_flop_array"
    dff = "dff"
    dff_array = "dff_array"
    control_logic = "control_logic"
    bitcell_array = "bitcell_array"
    sense_amp = "sense_amp"
    sense_amp_array = "sense_amp_array"
    precharge_array = "precharge_array"
    column_mux_array = "single_level_column_mux_array"
    write_driver = "write_driver"
    write_driver_array = "write_driver_array"
    tri_gate = "tri_gate"
    tri_gate_array = "tri_gate_array"
    wordline_driver = "wordline_driver"
    replica_bitline = "replica_bitline"
    replica_bitcell = "replica_bitcell"
    bitcell = "bitcell"
    delay_chain = "delay_chain"

