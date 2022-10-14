# OpenRAM Documentation
![OpenRAM Logo](../../images/OpenRAM_logo_yellow_transparent.svg)

These pages provide the documentation of OpenRAM. You can use the links below to navigate through the documentation.



## Directory
1.  [Contributors/Collaborators](#contributorscollaborators)
2.  [OpenRAM Dependencies](#openram-dependencies)
3.  [Supported Technologies](#supported-technologies)
4.  [Bitcells](./bitcells.md#go-back)
5.  [Architecture](./architecture.md#go-back)
6.  [Implementation](#implementation)
7.  [Technology and Tool Portability](#technology-and-tool-portability)
8.  [Basic Usage](./basic_usage.md#go-back)
9.  [Tutorials](./tutorials.md#go-back)
10. [Debugging and Unit Testing](./debug.md#go-back)
11. [Technology Setup](./technology_setup.md#go-back)
12. [Library Cells](./library_cells.md#go-back)
13. [Base Data Structures](./base_data_structures.md#go-back)
14. [Hierarchical Design Modules](./design_modules.md#go-back)
15. [Control Logic and Timing](./control_logic.md#go-back)
16. [Routing](./routing.md#go-back)
17. [Characterization](./characterization.md#go-back)
18. [Results](./results.md#go-back)
19. [FAQ](./FAQ.md#go-back)



## Contributors/Collaborators
<img align="right" height="120" src="../assets/images/logos/okstate.png">

* Prof. Matthew Guthaus (UCSC)
* Prof. James Stine & Dr. Samira Ataei (Oklahoma State University)
* UCSC students:
    * Bin Wu
    * Hunter Nichols
    * Michael Grimes
    * Jennifer Sowash
    * Jesse Cirimelli-Low
    <img align="right" height="100" src="../assets/images/logos/vlsida.png">
* Many other past students:
    * Jeff Butera
    * Tom Golubev
    * Marcelo Sero
    * Seokjoong Kim



## OpenRAM Dependencies

Please see the Dockerfile for the required versions of tools.

In general, the OpenRAM compiler has very few dependencies:
+ Docker
+ Make
+ Python 3.6 or higher
+ Various Python packages (pip install -r requirements.txt)
+ [Git]

Commercial tools (optional):
* Spice Simulator
    * Hspice  I-2013.12-1 (or later)
    * CustomSim 2017 (or later)
* DRC
    * Calibre 2017.3_29.23
* LVS
    * Calibre 2017.3_29.23



## Supported Technologies
* NCSU FreePDK 45nm
    * Non-fabricable but contains DSM rules
    * Calibre or klayout for DRC/LVS
* MOSIS 0.35um (SCN4M_SUBM)
    * Fabricable technology
    * Magic/Netgen or Calibre for DRC/LVS
* Skywater 130nm (sky130)
    * Fabricable technology
    * Magic/Netgen or klayout



## Implementation
* Front-end mode
    * Generates SPICE, layout views, timing models
        * Netlist-only mode can skip the physical design too
    * Doesn't perform DRC/LVS
    * Estimates power/delay analytically
* Back-end mode
    * Generates SPICE, layout views, timing models
    * Performs DRC/LVS
        * Can perform at each level of hierarchy or at the end
    * Simulates power/delay
        * Can be back-annotated or not



## Technology and Tool Portability
* OpenRAM is technology independent by using a technology directory that includes:
    * Technology's specific information
    * Technology's rules such as DRC rules and the GDS layer map
    * Custom designed library cells (6T, sense amp, DFF) to improve the SRAM density.
* For technologies that have specific design requirements, such as specialized well contacts, the user can include helper functions in the technology directory.
* Verification wrapper scripts
    * Uses a wrapper interface with DRC and LVS tools that allow flexibility
    * DRC and LVS can be performed at all levels of the design hierarchy to enhance bug tracking.
    * DRC and LVS can be disabled completely for improved run-time or if licenses are not available.
