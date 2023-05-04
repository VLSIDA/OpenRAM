
### [Go Back](./index.md#table-of-contents)

# Basic Usage
This page of the documentation explains the basic usage of OpenRAM's ROM compiler (OpenROM). For usage of the RAM compiler see [here](./basic_usage.md#go-back)



## Table of Contents
1. [Environment Variable Setup](#environment-variable-setup-assuming-bash)
1. [Command Line Usage](#command-line-usage)
1. [Script Usage](#script-usage)
1. [Configuration Files](#configuration-files)
1. [Common Configuration File Options](#common-configuration-file-options)
1. [Output Files](#output-files)



## Environment Variable Setup (assuming bash)
Environment configuration is the same as described in [basic SRAM usage](./basic_usage#environment-variable-setup-assuming-bash)


## Accepted Data formats
OpenROM currently supports input data formatted as a binary file or a text file
of hexadecimal-encoded data. For hexadecimal data, the input file must contain
a single line of hexadecimal text. The data in any input file will be written
the ROM in the order it appears in the input file, ie. the first bit in the input
will be written to address 0.

## Command Line Usage
Once you have defined the environment, you can run OpenROM from the command line
using a single configuration file written in Python. You can then run OpenROM by
executing:
```
python3 $OPENRAM_HOME/../rom_compiler.py myconfig
```
You can see all of the options for the configuration file in
$OPENRAM\_HOME/options.py

To run macros, it is suggested to use, for example:
```
cd OpenRAM/macros/rom_configs
make sky130_rom_1kbyte
```

* Common arguments:
    * `-h` print all arguments
    * `-t` specify technology (currently only sky130 is supported)
    * `-v` increase verbosity of output
    * `-n` don't run DRC/LVS
    * `-d` don't purge /tmp directory contents


## Configuration Files
* Shares some configuration options with SRAM compiler.
* Complete configuration options are in `$OPENRAM_HOME/options.py`
* Some options can be specified on the command line as well
    * Not recommended for replicating results
* Example configuration file:
    ```python

    # Data word size
    word_size = 2

    # Enable LVS/DRC checking
    check_lvsdrc = True

    # Path to input data. Either binary file or hex.
    rom_data = "data_1kbyte.bin"
    # Format type of input data
    data_type = "bin"

    # Technology to use in $OPENRAM_TECH, currently only sky130 is supported
    tech_name = "sky130"

    # Output directory for the results
    output_path = "temp"
    # Output file base name
    output_name = "rom_1kbyte"

    # Only nominal process corner generation is currently supported
    nominal_corner_only = True

    # Add a supply ring to the generated layout
    route_supplies = "ring"
    ```


## Output Files
The output files are placed in the `output_dir` defined in the configuration
file.

The base name is specified by `output_name` and suffixes are added. Currently only layout and schematic files are generated.

The final results files are:
* GDS (.gds)
* SPICE (.sp)
* Log (.log)
* Configuration (.py) for replication of creation
