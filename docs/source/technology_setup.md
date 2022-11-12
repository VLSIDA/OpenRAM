### [Go Back](./index.md#table-of-contents)

# Technology Setup
This page of the documentation explains the technology setup of OpenRAM.



## Table of Contents
1. [Technology Directories](#technology-directories)
1. Technology Configuration:
    1. [Layer Map](#technology-configuration-layer-map)
    1. [GDS](#technology-configuration-gds)
    1. [DRC](#technology-configuration-drc)
    1. [SPICE](#technology-configuration-spice)
    1. [Parameters](#technology-configuration-parameters)



## Technology Directories
* Environment variable OPENRAM\_TECH specifies list of technology directories
    * Similar to `*nix $PATH`
* Directory structure:
    ```
    techname/
        __init__.py     -- Sets up PDK environment
        tech/           -- Contains technology configuration
            __init__.py -- Loads all modules
            tech.py     -- SPICE, DRC, GDS, and layer config
        gds_lib/        -- Contains .gds files for each lib cell
        sp_lib/         -- Contains .sp file for each lib cell
        models/         -- Contains SPICE device corner models
        (tf/)           -- May contain some PDK material
        (mag_lib/)      -- May contain other layout formats
    ```



## Technology Configuration: Layer Map
* Layer map contains mapping of layer names to GDS layers
* Layer names are used in OpenRAM code directly
    ```python
    layer={} 
    layer["vtg"]      = -1 
    layer["vth"]      = -1 
    layer["contact"]  = 47 
    layer["pwell"]    = 41 
    ...
    layer["metal4"]   = 31 
    layer["text"]     = 63 
    layer["boundary"] = 63 
    layer["blockage"] = 83
    ```



## Technology Configuration: GDS
* OpenRAM uses the gdsMill library (included and heavily modified)
* Units defined for GDS format
    * First number is DB units per user units
    * Second number is DB unit in meters
        ```python
        # GDS file info
        GDS={}
        # gds units
        GDS["unit"]=(0.001,1e-6)  
        # default label zoom
        GDS["zoom"] = 0.5
        ```
* Zoom defines default zoom for labels
* More info on the GDS format at:
    * http://boolean.klaasholwerda.nl/interface/bnf/gdsformat.html



## Technology Configuration: DRC
* Creates the design\_rule class with several parts:
    * Grid size
    * Location of DRC, LVS, PEX rules and layer map
    * Subset of design rules for FEOL and BEOL
* Design rules have common naming scheme (names used in OpenRAM)
    * `minwidth_<layer>`
    * `<layer>_to_<layer>`
    * `<layer>_extend_<layer>`
    * `minarea_<layer>`
    * Allows rule tables for complex rules
```python
# Minimum spacing of metal3 wider than 0.09 & longer than 0.3 = 0.09
# Minimum spacing of metal3 wider than 0.27 & longer than 0.9 = 0.27
# Minimum spacing of metal3 wider than 0.5 & longer than 1.8 = 0.5
# Minimum spacing of metal3 wider than 0.9 & longer than 2.7 = 0.9
# Minimum spacing of metal3 wider than 1.5 & longer than 4.0 = 1.5
drc["metal3_to_metal3"] = drc_lut({(0.00, 0.0) : 0.07,
                                   (0.09, 0.3) : 0.09,
                                   (0.27, 0.9) : 0.27,
                                   (0.50, 1.8) : 0.5,
                                   (0.90, 2.7) : 0.9,
                                   (1.50, 4.0) : 1.5})
```



## Technology Configuration: SPICE
* Device models (and corners)
* Defaults simulation values
    * Voltage
    * Temperature
    * Feasible period for simulation
    * Rise/fall input slews
* Analytical parameters
    * For example, device capacitance and "on" resistance
    * Used for analytical delay and power estimation



## Technology Configuration: Parameters
* Default design parameters
    * Being cleaned up and standardized...
* Defaults simulation values
    * Voltage
    * Temperature
    * Feasible period for simulation
    * Rise/fall input slews
* Analytical parameters
    * Used for analytical delay and power estimation
    * E.g. device capacitance and "on" resistance
