### [Go Back](./index.md#table-of-contents)

# Base Data Structures
This page of the documentation explains the base data structures of OpenRAM.



## Table of Contents
1. [Design Classes](#design-classes)
1. [Base Class Inheritance](#base-class-inheritance)
1. [Parameterized Transistor](#parameterized-transistor-ptx-or-pfinfet)
1. [Parameterized Cells](#parameterized-cells)



## Design Classes
<img align="right" height="100" src="../assets/images/base_data_structures/layout_1.png">

* SPICE and GDS2 Interfaces
    * Custom cells (read GDS and SPICE)
    * Generated cells (creates GDS and SPICE "on the fly")
* Netlist functions
    * Add (directional) pins
    * Add and connect instances
    <img align="right" height="100" src="../assets/images/base_data_structures/layout_2.png">
* Layout functions 
    * Place instances
    * Add wires, routes, vias
    * Channel and Power router
* Verification functions (wrap around DRC and LVS tools)



## Base Class Inheritance
```mermaid
flowchart TD
    A[design.py \n\n General design and helper DRC constants] --> B[hierarchy_design.py \n\n DRC/LVS functions]
    B --> C["hierarchy_spice.py \n\n Netlist related functionality"]
    B --> D["hierarchy_layout.py \n\n Layout related functionality"]
    C --> E["Functions: \n add_pins \n add_inst"]
    C --> F["sp_read \n sp_write \n Power data \n Delay data"]
    D --> G["Functions: \n add_{layout_pin,rect,...} \n place_inst \n create_channel_route \n etc."]
    D --> H["gds_read \n gds_write \n get_blockages \n etc."]
```



## Parameterized Transistor (ptx or pfinfet)
<img align="right" height="100" src="../assets/images/base_data_structures/transistor.png">

* Creates variable size/finger nmos or pmos transistor
    * Optional gate and source/drain contacts in naive way
    * Not optimal layout, but "good enough"
    * Offset (0,0) is lower-left corner of active area
* Size/fingers effect on size must be estimated elsewhere perhaps by trying configurations



## Parameterized Cells
<img align="right" height="230" src="../assets/images/base_data_structures/parameterized_cell.png">

Dynamically generated cells (in `$OPENRAM_HOME/pgates`)
* Not the most efficient layouts but "ok"
* Try to use restrictive design rules to keep them portable
* Transistors
    * `ptx`, `pfinfet`
* Logic gates
    *  `pinv`, `pnand2`, `pnand3`, `pnor2`
* Buffer/drivers
    * `pbuf`, `pinvbuf`, `pdriver`
* SRAM Logic
    * `precharge`, `single_level_column_mux`
