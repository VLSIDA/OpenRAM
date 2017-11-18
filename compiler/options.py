import optparse
import getpass 
import os

class options(optparse.Values):
    """
    Class for holding all of the OpenRAM options.
    """

    # This is the technology directory.
    openram_tech = ""
    # This is the name of the technology.
    tech_name = ""
    # This is the temp directory where all intermediate results are stored.
    openram_temp = "/tmp/openram_{0}_{1}_temp/".format(getpass.getuser(),os.getpid())
    # This is the verbosity level to control debug information. 0 is none, 1
    # is minimal, etc.
    debug_level = 0
    # This determines whether  LVS and DRC is checked for each submodule.
    check_lvsdrc = True
    # Variable to select the variant of spice
    spice_version = ""
    # Should we print out the banner at startup
    print_banner = True
    # The DRC/LVS/PEX executable being used which is derived from the user PATH.
    drc_exe = ""
    lvs_exe = ""
    pex_exe = ""
    # The spice executable being used which is derived from the user PATH.
    spice_exe = ""
    # Run with extracted parasitics
    use_pex = False
    # Remove noncritical memory cells for characterization speed-up
    trim_netlist = True
    # Define the output file paths
    output_path = ""
    # Define the output file base name
    output_name = ""
    # Use analytical delay models by default rather than (slow) characterization
    analytical_delay = True
