### [Go Back](./index.md#directory)

# Basic Usage
This page of the documentation explains the basic usage of OpenRAM.



## Table of Contents
1. [Environment Variable Setup](#environment-variable-setup-assuming-bash)
2. [Command Line Usage](#command-line-usage)
3. [Configuration Files](#configuration-files)
4. [Common Configuration File Options](#common-configuration-file-options)
5. [Output Files](#output-files)
6. [Data Sheets](#data-sheets)



## Environment Variable Setup (assuming bash)
* OPENRAM_HOME defines where the compiler directory is
    * ```export OPENRAM_HOME="$HOME/openram/compiler"```
* OPENRAM_TECH defines list of paths where the technologies exist
    * `export OPENRAM_TECH="$HOME/openram/technology"`
    * Colon separated list so you can have private technology directories
* Must also have any PDK related variables set up
* Add compiler to `PYTHONPATH`
    * `export PYTHONPATH="$PYTHONPATH:$OPENRAM_HOME"`



## Command Line Usage
* Basic command line (with or without py suffix):
    * `openram.py config`
    * `openram.py config.py`
* Common arguments:
    * `-t` specify technology (scn4m_subm or scmos or freepdk45)
    * `-v` increase verbosity of output
    * `-n` don't run DRC/LVS
    * `-c` perform simulation-based characterization
    * `-d` don't purge /tmp directory contents



## Configuration Files
* Memories are created using a Python configuration file to replicate results
    * No YAML, JSON, etc.
* Complete configuration options are in `$OPENRAM_HOME/options.py`
* Some options can be specified on the command line as well
    * Not recommended for replicating results
* Example configuration file:
    ```python
    # Data word size
    word_size = 2
    # Number of words in the memory
    num_words = 16

    # Technology to use in $OPENRAM_TECH
    tech_name = "scn4m_subm"
    # Process corners to characterize
    process_corners = [ "TT" ]
    # Voltage corners to characterize
    supply_voltages = [ 3.3 ]
    # Temperature corners to characterize
    temperatures = [ 25 ]

    # Output directory for the results
    output_path = "temp"
    # Output file base name
    output_name = "sram_16x2"

    # Disable analytical models for full characterization (WARNING: slow!)
    # analytical_delay = False

    # To force this to use magic and netgen for DRC/LVS/PEX
    # Could be calibre for FreePDK45
    drc_name = "magic"
    lvs_name = "netgen"
    pex_name = "magic"  
    ```



## Common Configuration File Options
* Characterization corners
    * `supply_voltages = [1.7, 1.8, 1.9]`
    * `temperatures = [25, 50, 100]`
    * `process_corners = ["SS", "TT", "FF"]`
* Do not generate layout
    * `netlist_only = True`
* Multi-port options
    * `num_rw_ports = 1`
    * `num_r_ports = 1`
    * `num_w_ports = 0`
* Customized module or bit cell
    * `bitcell = "bitcell_1rw_1r"`
    * `replica_bitcell = "replica_bitcell_1rw_1r"`
* Enable simulation characterization
    > **Warning**: Slow!
    * `analytical_delay = False`
* Output name and location
    * `output_path = "temp"`
    * `output_name = "sram_32x256"`
* Force tool selection (should match the PDK!)
    * `drc_name = "magic"`
    * `lvs_name = "netgen"`
    * `pex_name = "magic"`
* Include shared configuration options using Python imports
    * `from corners_freepdk45 import *`



## Output Files
The output files are placed in the `output_dir` defined in the configuration file.

The base name is specified by `output_name` and suffixes are added.

The final results files are:
* GDS (.gds)
* SPICE (.sp)
* Verilog (.v)
* P&R Abstract (.lef)
* Liberty (multiple corners .lib)
* Datasheet (.html)
* Log (.log)
* Configuration (.py) for replication of creation



## Data Sheets
![Datasheet 1](../assets/images/basic_usage/datasheet_1.png)
![Datasheet 2](../assets/images/basic_usage/datasheet_2.png)
![Datasheet 3](../assets/images/basic_usage/datasheet_3.png)