import optparse
import getpass 
import os

class options(optparse.Values):
    """
    Class for holding all of the OpenRAM options. All of these options can be over-riden in a configuration file
    that is the sole required command-line positional argument for openram.py.
    """

    ###################
    # Configuration options
    ###################
    # This is the technology directory.
    openram_tech = ""
    
    # This is the name of the technology.
    tech_name = ""
    
    # Port configuration (1-2 ports allowed)
    num_rw_ports = 1
    num_r_ports = 0
    num_w_ports = 0
    
    # These will get initialized by the user or the tech file
    supply_voltages = ""
    temperatures = ""
    process_corners = ""

    # Size parameters must be specified by user in config file.
    #num_words = 0
    #word_size = 0
    # You can manually specify banks, but it is better to auto-detect it.
    num_banks = 1

    ###################
    # Optimization options
    ###################    
    # Uses the delay chain size in the tech.py file rather automatic sizing.
    use_tech_delay_chain_size = False


    ###################
    # Debug options.
    ###################    
    # This is the temp directory where all intermediate results are stored.
    try:
        # If user defined the temporary location in their environment, use it
        openram_temp = os.path.abspath(os.environ.get("OPENRAM_TMP"))
    except:
        # Else use a unique temporary directory
        openram_temp = "/tmp/openram_{0}_{1}_temp/".format(getpass.getuser(),os.getpid())
    # This is the verbosity level to control debug information. 0 is none, 1
    # is minimal, etc.
    debug_level = 0

    ###################
    # Run-time vs accuracy options.
    ###################
    # When enabled, layout is not generated (and no DRC or LVS are performed)
    netlist_only = False
    # Whether we should do the final power routing
    route_supplies = False
    # This determines whether LVS and DRC is checked at all.
    check_lvsdrc = True
    # This determines whether LVS and DRC is checked for every submodule.
    inline_lvsdrc = False
    # Remove noncritical memory cells for characterization speed-up
    trim_netlist = True
    # Run with extracted parasitics
    use_pex = False

    
    ###################
    # Tool options
    ###################
    # Variable to select the variant of spice
    spice_name = ""
    # The spice executable being used which is derived from the user PATH.
    spice_exe = ""
    # Variable to select the variant of drc, lvs, pex
    drc_name = ""
    lvs_name = ""
    pex_name = ""
    # The DRC/LVS/PEX executable being used which is derived from the user PATH.
    drc_exe = None
    lvs_exe = None
    pex_exe = None
    
    # Should we print out the banner at startup
    print_banner = True
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


    ###################    
    # These are the default modules that can be over-riden
    ###################    
    bank_select = "bank_select"
    bitcell_array = "bitcell_array"
    bitcell = "bitcell"
    column_mux_array = "single_level_column_mux_array"
    control_logic = "control_logic"
    decoder = "hierarchical_decoder"
    delay_chain = "delay_chain"
    dff_array = "dff_array"
    dff = "dff"
    precharge_array = "precharge_array"
    ptx = "ptx"
    replica_bitcell = "replica_bitcell"
    replica_bitline = "replica_bitline"
    sense_amp_array = "sense_amp_array"
    sense_amp = "sense_amp"
    tri_gate_array = "tri_gate_array"
    tri_gate = "tri_gate"
    wordline_driver = "wordline_driver"
    write_driver_array = "write_driver_array"
    write_driver = "write_driver"

