# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os
import optparse


class options(optparse.Values):
    """
    Class for holding all of the OpenRAM options. All
    of these options can be over-riden in a configuration file
    that is the sole required command-line positional argument for sram_compiler.py.
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

    # By default, don't use hierarchical wordline
    local_array_size = 0

    # Write mask size, default will be overwritten with word_size if not user specified
    write_size = None

    # These will get initialized by the user or the tech file
    nominal_corner_only = False
    supply_voltages = ""
    temperatures = ""
    process_corners = ""
    load_scales = ""
    slew_scales = ""

    # Size parameters must be specified by user in config file.
    # num_words = 0
    # word_size = 0
    # You can manually specify banks, but it is better to auto-detect it.
    num_banks = 1
    words_per_row = None
    num_spare_rows = 0
    num_spare_cols = 0

    ###################
    # ROM configuration options
    ###################
    rom_endian = "little"
    rom_data = None
    data_type = "bin"
    strap_spacing = 8
    scramble_bits = True

    ###################
    # Optimization options
    ###################
    # Approximate percentage of delay compared to bitlines
    rbl_delay_percentage = 0.5

    # delay chain is automatically sized in delay based control logic
    # this multiplier can be used to add a guard band to the standard timing
    # lowering it can improve performance but may cause sram to fail
    delay_control_scaling_factor = 1.0
    # stages for delay chain in rbl control logic only
    delay_chain_stages = 9
    # fanout per stage for any control logic
    delay_chain_fanout_per_stage = 4

    accuracy_requirement = 0.75

    ###################
    # Debug options.
    ###################
    # This is the temp directory where all intermediate results are stored.
    try:
        # If user defined the temporary location in their environment, use it

        openram_temp = os.path.abspath(os.environ.get("OPENRAM_TMP"))

    except:
        openram_temp = "/tmp"

    # This is the verbosity level to control debug information. 0 is none, 1
    # is minimal, etc.
    verbose_level = 0
    # Drop to pdb on failure?
    debug = False
    # Only use corners in config file. Disables generated corners
    only_use_config_corners = False
    # A list of PVT tuples and be given and only these will be characterized
    use_specified_corners = None
    # Allows specification of model data
    sim_data_path = None
    # A list of load/slew tuples
    use_specified_load_slew = None
    # Spice simulation raw file
    spice_raw_file = None

    ###################
    # Run-time vs accuracy options.
    # Default, sacrifice accuracy/completeness for speed.
    # Must turn on options for verification, final routing, etc.
    ###################
    # When enabled, layout is not generated (and no DRC or LVS are performed)
    netlist_only = False
    # Whether we should do the final power routing
    route_supplies = "tree"
    supply_pin_type = "ring"
    # This determines whether LVS and DRC is checked at all.
    check_lvsdrc = False
    # This determines whether LVS and DRC is checked for every submodule.
    inline_lvsdrc = False
    # Remove noncritical memory cells for characterization speed-up
    trim_netlist = True
    # Run with extracted parasitics
    use_pex = False
    # Output config with all options
    output_extended_config = False
    # Output temporary file used to format HTML page
    output_datasheet_info = True
    # Determines which analytical model to use.
    # Available Models: elmore, linear_regression
    model_name = "elmore"
    # Write graph to a file
    write_graph = False

    ###################
    # Tool options
    ###################
    # Top process that was ran (openram, memchar, memfunc)
    top_process = None
    # Use conda to install the default tools
    # (existing tools will be used if disabled)
    use_conda = True
    # Variable to select the variant of spice
    spice_name = None
    # The spice executable being used which is derived from the user PATH.
    spice_exe = None
    # Variable to select the variant of drc, lvs, pex
    drc_name = None
    lvs_name = None
    pex_name = None
    # The DRC/LVS/PEX executable being used
    # which is derived from the user PATH.
    drc_exe = None
    lvs_exe = None
    pex_exe = None
    # For sky130, we need magic for filtering.
    magic_exe = None

    # Number of threads to use
    num_threads = 1
    # Number of threads to use in ngspice/hspice
    num_sim_threads = 3

    # Some tools (e.g. Xyce) use other separators like ":"
    hier_seperator = "."

    # Should we print out the banner at startup
    print_banner = True

    # Define the output file paths
    output_path = "."
    # Define the output file base name
    output_name = ""
    # Use analytical delay models by default
    # rather than (slow) characterization
    analytical_delay = True
    # Purge the temp directory after a successful
    # run (doesn't purge on errors, anyhow)

    # Bitline, s_en and cell names used in characterizer
    bl_format = "X{name}{hier_sep}xbank0{hier_sep}bl_{row}_{col}"
    br_format = "X{name}{hier_sep}xbank0{hier_sep}br_{row}_{col}"
    sen_format = "X{name}{hier_sep}xbank0{hier_sep}s_en"
    cell_format = "X{name}{hier_sep}xbank0{hier_sep}xbitcell_array{hier_sep}xreplica_bitcell_array{hier_sep}xbitcell_array{hier_sep}xbit_r{row}_c{col}"
    # Route the input/output pins to the perimeter
    perimeter_pins = True

    # Detailed or abstract LEF view
    detailed_lef = False

    keep_temp = False

    # These are the default modules that can be over-riden
    bank_select = "bank_select"
    bitcell_array = "bitcell_array"
    bitcell = "bitcell"
    buf_dec = "pbuf"
    column_decoder = "column_decoder"
    column_mux_array = "column_mux_array"
    control_logic = "control_logic"
    decoder = "hierarchical_decoder"
    delay_chain = "delay_chain"
    dff_array = "dff_array"
    dff = "dff"
    inv_dec = "pinv"
    nand2_dec = "pnand2"
    nand3_dec = "pnand3"
    nand4_dec = "pnand4" # Not available right now
    precharge = "precharge"
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
