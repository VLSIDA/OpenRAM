### [Go Back](./index.md#table-of-contents)

# Introduction
This is a note, which may be helpful for people, who want to contribute to OpenRAM, currently the note concentrates on the SRAM(SKY130) only.
# Detailed usage
In this section, the detailed usage of using OpenRAM framework will be demonstrated.
## Generate 1 sram macro
### General process 

> [!IMPORTANT]
>
>  Before you go through, make sure that environment of Sky130 has been already set up.

1. Activate miniconda

2. Edit the sram configuration file

3. Generate the macro

4. Check the results

#### Activate miniconda

```bash
cd OpenRAM/
source ./miniconda/bin/activate
```

#### Modified the sram configuration
Go to the directory where the sram configurtion exits with the following command:
```bash
cd OpenRAM/macros/sram_configs
```
In the directory you will find 2 kinds of configuration:  
1. sky130_sram_common.py ->  some commmon configration of sram 
2. sky130_sram_*kbyte_1rw_*x*_8.py -> the size of sram, should includes the 1. file
##### Useful parameters
You may want to change the configuration, here some frequently used options / parameters:
- **check_lvsdrc**
  - location: sky130_sram_common.py    
  - function: whether enable the lvs & drc or not
  - value: True / False
- **word_size**
  - location: sky130_sram_*kbyte_1rw_*x*_8.py    
  - function: the word size of sram
  - value: 8, 16, 32, 64...
- **num_words**
  - location: sky130_sram_*kbyte_1rw_*x*_8.py    
  - function: the number of words of sram
  - value: 8, 16, 32, 64, 128..
- **write_size**
  - location: sky130_sram_*kbyte_1rw_*x*_8.py    
  - function: allow byte-write, which known as wmask
  - value: 8 (usually)
- **num_spare_rows**
  - location: sky130_sram_*kbyte_1rw_*x*_8.py    
  - function: the number of spare_rows
  - value: 0,1,2,3,4,5...(odd wenn only 1 port)
- **num_spare_cols**
  - location: sky130_sram_*kbyte_1rw_*x*_8.py    
  - function: tthe number of spare_cols
  - value: 0,1,2,3,4,5....(odd wenn only 1 port)
- **ports_human**
  - location: sky130_sram_*kbyte_1rw_*x*_8.py    
  - function: the port information
  - value: 1rw, 1w1r, 1rwr...
####  Generate macro
Go to directory of macros, where the Makefile exits:
```
cd /OpenRAM/macros
```
And then "make" the corresponding sram configuration (without .py in the end):
```
make my_sram_config
```
#### Check the results
After successfully generating the sram macro, you will find a directory located in /OpenRAM/macros, which has exactly the same name as your sram configuration:
```
--macros/
  |
  --rom_configs/
  |
  --sram_configs/
  |
  --my_sram_config/  <- Your macro
  |
  --Makefile
```
Just go to your macro directory, and check the results: (only important files are listed here)
```
cd my_sram_config/ 

--my_sram_config/
  |
  --my_sram_config.v
  |
  --my_sram_config.lib
  |
  --my_sram_config.gds
  |
  --my_sram_config.lef
```
#### Common problems
##### Lvs_drc process gets stuck and runs into forever ?
- Comments: This is likely to happen when you're trying to generate some " bigger " sram, like 1kb. It will likely to get stuck in the extraction process of magic, you'll find the terminal keep printing like " ...still running(4000s) ".
- Workaround: Just disable the lvs_drc here. Don't worry, you will have to do drc check and lvs when harding it, however there're some problems with it, which will be demonstrated and " solved " later.
##### Failed in generating, complains when "calculating something" ? 
- Comments: This is likely to happen when the spare_wen_row / spare_wen_col has the wrong number, thus failed to generate the correspoding submodule of sram.
- Solution: make sure you set the correct number of spare_wen_row / spare_wen_col in the sram configuration.
## Harden 1 sram macro in Openlane2

Since there's no tutorial of using sram macro in Openlane2 currently, this section is added. The usage in Openlane1 could be found here -> https://openlane.readthedocs.io/en/latest/tutorials/openram.html 

### General process
> [!IMPORTANT]
>
>  Before you go through, make sure that environment of Openlane2 has been already set up.
1. Modified the config.json
2. Modified the OpenRAM lef file 
3. Modified the pdn.tcl
4. Harden

#### Modified the config.json
Usually, config.json consists of 3 parts:
- Tell the tool about the source files, usually .v files
- Tell the tool about the macro files, .lef, .gds, .v(for simulation), .lib, etc.
- Tell the tool about the flow options, pdn settings, die size, clock frequency, etc.
The following config.json could be used as reference: 
```json
{
	"DESIGN_NAME": "top",
	"VERILOG_FILES": ["dir::src/top.v", "dir::src/SRAMController.v", "dir::src/UARTReceiver.v", "dir::src/UARTTransmitter.v", "dir::src/dpu.v"],
	"EXTRA_VERILOG_MODELS": ["dir::src/myconfig_sky_dual.v"],
  
	"FP_PDN_CHECK_NODES": false,
	"FP_PDN_VOFFSET": 26.32,
	"FP_PDN_VPITCH": 138.87,
	"FP_PDN_CFG": "pdn_cfg.tcl",
	"RUN_MAGIC_WRITE_LEF": true,
	"MAGIC_LEF_WRITE_USE_GDS": false,
	"MAGIC_CAPTURE_ERRORS": false,
	"MAGIC_WRITE_LEF_PINONLY": true,
	"MAGIC_DRC_USE_GDS": true,
	"QUIT_ON_MAGIC_DRC": false,
	"QUIT_ON_KLAYOUT_DRC": false,
	"SYNTH_ABC_BUFFERING": true,
	"RUN_HEURISTIC_DIODE_INSERTION": true,
	"VDD_NETS": "VDPWR",
	"GND_NETS": "VGND",
  "FP_PDN_MACRO_HOOKS": "sram_ins VDPWR VGND vccd1 vssd1",
	"SYNTH_POWER_DEFINE": "USE_POWER_PINS",
	"MACROS": {
		"myconfig_sky_dual": {
		  "instances": {
			"sram_ins": {
			  "location": [100, 16],
			  "orientation": "N"
			}
		  },
		  "gds": ["dir::macro/myconfig_sky_dual.gds"],
		  "lef": ["dir::macro/myconfig_sky_dual.lef"]
		}
	},
  "GRT_ALLOW_CONGESTION": true,
	"FP_SIZING": "absolute",
	"DIE_AREA": [0, 0, 500, 210],
  
	"//": "MAGIC_DEF_LABELS may cause issues with LVS",
	"MAGIC_DEF_LABELS": false,
  
	"//": "use alternative efabless decap cells to solve LI density issue",
	"DECAP_CELL": [
	  "sky130_fd_sc_hd__decap_3",
	  "sky130_fd_sc_hd__decap_4",
	  "sky130_fd_sc_hd__decap_6",
	  "sky130_fd_sc_hd__decap_8",
	  "sky130_ef_sc_hd__decap_12"
	],
  
	"//": "period is in ns, so 20ns == 50mHz",
	"CLOCK_PERIOD": 40,
	"CLOCK_PORT": "clk",

  "//": "Reduce wasted space",
  "TOP_MARGIN_MULT": 1,
  "BOTTOM_MARGIN_MULT": 1,
  "LEFT_MARGIN_MULT": 6,
  "RIGHT_MARGIN_MULT": 6,

	"FP_IO_HLENGTH": 2,
	"FP_IO_VLENGTH": 2,
  
	"//": "don't use power rings or met5",
	"DESIGN_IS_CORE": false,
	"RT_MAX_LAYER": "met4"
}
```
##### Useful parameters
Of course, in the above mentioned reference config.json, not all the parameters are needed to be used or must be used. You may edit it based on your usage / requirments. Here some commonly used parameters are introduced. You could find more in the following 2 links -> https://openlane.readthedocs.io/en/latest/reference/configuration.html & https://openlane2.readthedocs.io/en/latest/reference/step_config_vars.html. It is suggested to use both of them to have a better understanding.
- **DESIGN_NAME**
  - function: Tell the tool the name of your "top level" design
  - value: string -> "top"
- **VERILOG_FILES**
  - function: Tell the tool all your source files
  - value: list -> ["top.v, design_sub.v,..."]
- **EXTRA_VERILOG_MODELS**
  - function: Tell the tool your behavior simulation module of macro
  - attention: " /// sta-blackbox " need to be added in the verilog file
  - value: list -> ["macro.v"]
- **RUN_HEURISTIC_DIODE_INSERTION**
  - function: Solve the antenna error, in case it occurs in the final report
  - value: bool -> true
- **VDD_NETS**
  - function: Define the name of VDD_NETS
  - value: string -> "VDPWR"
- **GND_NETS**
  - function: Define the name of GND_NETS
  - value: string -> "VGND"
- **FP_PDN_MACRO_HOOKS**
  - function: Tell the tool which pdn should connect which power pin of macro
  - attention: this parameter is named as "PDN_MACRO_CONNECTIONS" in Openlane2, however the old one still works
  - value: string -> "sram_ins VDPWR VGND vccd1 vssd1", sram_ins must be the instance name of the macro, the following is "PDN_VDD_NETS PDN_GND_NETS macro_power_pin macro_gnd_pin"
- **GRT_ALLOW_CONGESTION**
  - function: Tell the tool to allow congestion during global routing, this option is useful especially the area of design is strictly limited and you've got error message compaining about "routing failed" before
  - value: bool -> true
- **FP_SIZING**
  - function: Tell the tool that the size of design is adjustable or not
  - value: string -> "absolute" or just ignore this option, which you may find the design size can change to ease routing
- **FP_PDN_VOFFSET**
  - function: Change the defaut x-position of the first vertical PDN stripe 
  - value: int/float -> 26.32
- **FP_PDN_VPITCH**
  - function: Change the defaut distance between 2 vertical power stripe
  - value: int/float -> 138.87
- **MACROS**
  - function: Tell the tool all the information of the macro
  - value: 
  ```json
	"MACROS": {
		"myconfig_sky_dual": {
		  "instances": {
			"sram_ins": {
			  "location": [100, 16],
			  "orientation": "N"
			}
		  },
		  "gds": ["dir::macro/myconfig_sky_dual.gds"],
		  "lef": ["dir::macro/myconfig_sky_dual.lef"]
		}
	},
  ```
> [!IMPORTANT]
>
>  The following parameters are used to make sure the harden process could go through with OpenRAM macros.

- **FP_PDN_CHECK_NODES**
  - function: Enables checking for unconnected nodes in the power grid.
  - value: bool -> false
  - comments: This option need to be turned off, since current version of openlane2 still lacks of the ability to check the connection on the sram macro. If not turned off, it is likely to see a lot of "unconnected nodes" in the terminal, and then fails at stage 20 PDN.
- **FP_PDN_CFG**
  - function: Tell the tool the position of pdn.tcl script, where the exact behavir of PDN generation will be defined.
  - value: string -> "pdn_cfg.tcl"
  - comments: A modified pdn script is a must for using OpenRAM sram macro. If not use, you'll be likely to fail at stage 20 PDN.
- **MAGIC_DRC_USE_GDS**
  - function: run magic drc at lef level or gds level
  - value: bool ->  false
  - comments: the openram_cells (either sp/dp) have special rules and current magic drc script in the PDK cannot check. If run under gds level, there will be plenty of errors, but in fact they're fine
- **MAGIC_CAPTURE_ERRORS**
  - function: control the magic will throw error or not
  - value: bool -> false
  - comments: same reason. Otherwise it will complain about "unknown layer", "unknown cell", and "cell put on itself, ignoring the other", which will stop the whole flow.
- **QUIT_ON_MAGIC_DRC**
  - function: quit the flow wenn there're magic drc
  - value: bool -> false
  - comments: same reason. Just do not stop the flow
  - attention: actually, if run magic drc at lef level, you'll get this "All nwells must contain metal-connected N+ taps (nwell.4)", but in fact in you check the odb file, it can be found the tap is inserted.
#### Modified the OpenRAM lef file
The lef need to be adjusted, in order to use the sram macro.
##### Change the units
```
UNITS
  DATABASE MICRONS 1000 ; -> origin is 2000
```
##### Check the blockage
This step is in order to make sure the PDN step can be gone through. Make sure there's no blockage at power pins of macro or full macro in your pdn stripe layer, in which you want to connect the power pins of maco. 
#### Modified the pdn.tcl
Here a reference pdn script is attached. It is suggested that to modify it to adjust your own requirements. The script is modified based on the official one, it may be confusing at first. Here a short introduction to it is attached. For more details of usage of the tcl command, it is suggested to refer to the OpenRoad documentation of power gird step - > https://openroad.readthedocs.io/en/latest/main/src/pdn/README.html#add-pdn-connect.
```tcl
# Copyright 2020-2022 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

source $::env(SCRIPTS_DIR)/openroad/common/set_global_connections.tcl
set_global_connections

define_pdn_grid \
    -name stdcell_grid \
    -starts_with POWER \
    -voltage_domain CORE \
    -pins $::env(FP_PDN_VERTICAL_LAYER)

add_pdn_stripe \
    -grid stdcell_grid \
    -layer $::env(FP_PDN_VERTICAL_LAYER) \
    -width $::env(FP_PDN_VWIDTH) \
    -pitch $::env(FP_PDN_VPITCH) \
	-spacing 2\
	-number_of_straps 1\
    -offset $::env(FP_PDN_VOFFSET) \
    -starts_with POWER

add_pdn_stripe \
    -grid stdcell_grid \
    -layer $::env(FP_PDN_VERTICAL_LAYER) \
    -width $::env(FP_PDN_VWIDTH) \
    -pitch $::env(FP_PDN_VPITCH) \
	-spacing 2\
	-number_of_straps 1\
    -offset 143 \
    -starts_with POWER\

add_pdn_stripe \
    -grid stdcell_grid \
    -layer $::env(FP_PDN_VERTICAL_LAYER) \
    -width $::env(FP_PDN_VWIDTH) \
    -pitch $::env(FP_PDN_VPITCH) \
	-spacing 2\
	-number_of_straps 1\
    -offset 470 \
    -starts_with POWER
# this is not used, since fp pdn is m5
add_pdn_stripe \
    -grid stdcell_grid \
    -layer $::env(FP_PDN_HORIZONTAL_LAYER) \
    -width $::env(FP_PDN_HWIDTH) \
    -pitch $::env(FP_PDN_HPITCH) \
    -offset $::env(FP_PDN_HOFFSET) \
    -spacing $::env(FP_PDN_HSPACING) \
    -starts_with POWER 

# Adds the standard cell rails if enabled.
if { $::env(FP_PDN_ENABLE_RAILS) == 1 } {
    add_pdn_stripe \
        -grid stdcell_grid \
        -layer $::env(FP_PDN_RAIL_LAYER) \
        -width $::env(FP_PDN_RAIL_WIDTH) \
        -followpins \
        -starts_with POWER

    add_pdn_connect \
        -grid stdcell_grid \
        -layers "$::env(FP_PDN_RAIL_LAYER) $::env(FP_PDN_VERTICAL_LAYER)"
}

# this will tell the tool the power ring of the macro
define_pdn_grid \
    -macro \
    -default \
    -name macro \
    -starts_with POWER \
    -halo "$::env(FP_PDN_HORIZONTAL_HALO) $::env(FP_PDN_VERTICAL_HALO)"

# this will add vias at the power ring, make sure power line is connected to the macro power ring
add_pdn_connect \
    -grid macro \
    -layers "met3 met4"


add_pdn_connect \
    -grid stdcell_grid \
    -layers "met3 met4"
```
##### Basic principle of PDN
- There must be min. 1 PDN pair, which means min. 1 VDD_NET stripe & min. 1 GND_NET stripe connected to the macro
- The other area of your design should have power grid, making sure everywhere could get the power
##### Reference realization
The above reference pdn script describe a way to generate the power grid. 
1. Horizontal trails are added and connect with vertical power / groud sripe
2. 1 vertical stripe pair located at left side of the macro
3. 1 vertical stripe pair across the macro, and connected with power ring of macro
4. 1 vertical stripe pair located right side of the maco
- **Useful tcl commands**
  - **define_pdn_grid**
    - function: define 1 pdn grid with the settings given
    - comments: usually 1 grid for std_cell, 1 grid for macro
  - **add_pdn_stripe**
    - function: add the pdn stripe to the grid you defined
    - comments: here the number / offset / spacing of the stripe could be manually controlled
  - **add_pdn_connect**
    - function: connect all the pdn at the given layer
    - comments: "think at the tool side", the tool only knows the command. So make sure the stripe is clearly defined and added, make sure you know which stripe should be connected to which stripe
##### Common problems with PDN
###### No vias and no shape of instance ? 
- Comments: This error message is one of the most common errors which occur in the PDN stage. Usually it is just because the tool could find your power pins of macros, however according to the lef file "OBS" part, they're partly or full in the blockage, so the tool just has no way to reach it, and find there're no power pins at that layer.
- Solution: check the lef file of your macro, make sure your power pins are not blocked in the layers where you want to have your power pins connected to the power grid. If there are, remove them in the OBS, for example, deleting all the blockage at met4 and add the stripe with proper offset manually in order not to disturb the other metal wires inside macro.
###### Unconnected power pins ?
- Comments: This depends on which stage you fail. If it fails at around stage 20, you just need to make sure you've truned off "FP_PDN_CHECK_NODE"; If it fails at around stage 46, you could open the latest .odb file with command"openroad -gui", and it could be found that there's just really no vias added at the stripe across the macro. This because the tool doesn't know there's power ring around the macro and thus never even try to connect them; Or the tool know the power ring, but the pdn_connect doesn't ask the tool to connect to the power ring. In this case, just double check pdn.tcl, make sure the tcl command is correct.
- Solution: Check config.json or pdn.tcl
###### Duplicated vias are added on the power ring 
- Comments: This is because the "add_pdn_connect" command will only tell the tool which layers should be connected with each other. The tool has no idea, whether the power ring is already conneted or not, the tool will just add vias if the power ring happens to be located at the layers that you proviede in the command.
- Solution: Edit the lef file of macro, make the 4 cornors of the power ring "empty". This will make the tool "see" no overlap of the power ring, and give up adding vias at the power ring again.
#### Harden
Go to the directory, and type the following command:
```
openlane config.json
```
Then hopes everything go right! （≧∇≦）
#### Common problems
##### PDN Issue ?
- Comments: very likely to happen, just check the pdn note above.
- Solution: see above
##### Klayout drc errors ? 
- Comments: likely to happen, the framework generated one may not fulfill all the rules. Luckily, there're only very few of it, which could fix by hand.
- Solution: open the klayout with edit mod, load the drc.xml file, fix by hand one by one.
##### Failed in some stage, which are not mentioned here?
- Comments: more likely it is related to config.json or in other words, wrong use of some options of openlane 2.
- Solution: check the options, or find answers in issues related to Openlane 2.
# Code structure
From now on, the detail of the OpenRAM framework will be introduced, which may be helpful for developer.
## In general 
In order to generate 1 sram macro, the file in the main directory "./OpenRAM/sram_compiler" will be called. Go to this file, and the following could be found:
```python
# Create an SRAM (we can also pass sram_config, see documentation/tutorials for details)
from openram import sram
s = sram()

# Output the files for the resulting SRAM
s.save()
```
Here the file "./OpenRAM/compiler/sram.py" will be called, where the define the generated files -> .v, .lef, .gds, etc. In the constructor part, the following could be found:
```python
from openram.modules.sram_1bank import sram_1bank as sram

self.s = sram(name, sram_config)

self.s.create_netlist()
if not OPTS.netlist_only:
    self.s.create_layout()

if not OPTS.is_unit_test:
    print_time("SRAM creation", datetime.datetime.now(), start_time)
```
Here the file "./OpenRAM/compiler/modules/sram_1bank.py" will be called, where the detailed structure of sram will be defined, including the position of submodules in the sram, how they're routed with each other, the PINs of sram macro and how they're routed with the the internal world, etc.
## /compiler/base/
In this directory, some fundamental classes are defined, in which some basic operations are defined, like coordinate(x,.y,.top center, etc.), shapes in gds(metal wire, rectangle, add a pin, etc.), operation(snap to grid, add, sub, etc.). Some commly used files / classes are introduced here:

- **/compiler/base/channel_route.py**
  - function: describe a channel router, using left-edge algorithms
  - comments: used in sram module, connecting the dffs and bank
- **/compiler/base/hierarchy_layout.py**
  - function: class consists of a set of objs and instances for a module. This provides a set of useful generic types for hierarchy management.
  - comments: if you want to add something in the sram gds, you could search the methods in this class
- **compiler/base/pin_layout.py**
  - function: describe a pin in gds
  - comments: in this file some basic properties of a pin could be found, like the coordinate of the lower left point of the pin.
- **compiler/base/vector.py, vector3d.py**
  - function: describe / override operation of vector
  - comments: make sure when doing operation with coordinate of pin / rect, everything is alright
- **compiler/base/route.py, wire.py, wire.py**
  - function: methods of connecting pins
  - comments: these 3 files are actually talking about similar things, could be used when conneting pins / routing
## /compiler/module/
This directory contains the submodules of a sram. Here the top file of sram -> "compiler/modules/sram_1bank.py" will be introduced.
### General structure / steps of sram_1bank
The following things need to be done in order to make a module (not ordered):
1. Define the IO pins of the module (including power/gnd pins) -> .add_pins()
2. Generate spice (it is called netlist in the file)  -> .create_netlists()
3. Generate layout (gds file) -> .create_layout()
4. Connect the submodule / IO pins -> .route_layout() & other methods  

For sram_1bank, the logic is as follows:
1. Define the IO pins
2. Create spice, create the submodules
3. Place the submodules (layout, which means gds)
4. Connect the submodule inside the sram
5. Connect the submodule to the IO pins of the sram
6. Route the supply
#### Useful methods
- **add_pins(self)**
  - function: add top_level IO pins of sram 
  - comments: this method will add IO pins of sram. However, they're **NOT** physical pins that you see in the final layout(gds)! The physical IO pins are defined in another method called "**add_layout_pins(self, add_vias=True)**", and you should keep them have the same pin name.
  - attention: actually the original process of routing IO pins is a little bit confusing, the pin names will be used to replace the "fake pin" at the end of escape signal routing, more details will be introduced in router section later
- **create_layout(self)**
  - function: generate the layout(gds), it consits other methods like placement
  - comments: this method os used in generating the gds of sram
- **route_supplies(self, bbox=None)**
  - function: route the supply grid and connect the pins to them
  - comments: for sram macro, usually use "power ring", more details are in router section
- **route_escape_pins(self, bbox=None)**
  - function: route the internal pins to the perimeter(IO pins) 
  - comments: more details are in router section
- **add_layout_pins(self, add_vias=True)**
  - function: add the top_level IO pins of sram, which will be seen in the final gds
  - comments: actually, what this function does is just "pull" all the **internal** pins of submodules up to m3 layer, which need to be connected with the outerworld, and change their name that are exactly same as defined in "**add_pins(self)**". But since the escape router will use the same name as IO pins in the end, they would be seen in the final gds
- **place_instances(self)** 
  - function: place all the modules inside the sram in certain position
  - comments: in this method other methods which have name of " **place_* **" are been called, in which the detailed process / position of  submodules are defined
- **route_layout(self)**
  - function: route the submodules with each other, and do supply routing / escape signal routing according to the settings / options
  - comments: the internal signals / submodules -> clk, control logic, dffs, they're routed by "hand" or channel router. Only escape signal and supply router will call router to do the routing
## /compiler/router/
In this directory the files of routers are contained. Currently the router is only used in supply routing / escape signal routing.
### Supply router (original)
Build the graph by Hanan grid graph method, combined with a maze router using A* algorithms to search the shortest path to connect with.
### Escape signal router (original)
Similar to the supply router, actually the "**route(self, pin_names)**" method is almost the same as that in supply router. However the target pin (IO pins) definitioin is different.
#### General process
The basic idea is as follows: 
1. Load the source pins, which are the internal pins that need to connect to the outer world
2. Calculate the nearst edge of the sram(left, right, top, bottom) to each source pin, create a "fake pin" on that edge. Depends on the edge, those fake pins should have either same y_position or x_postion(if not overlape the fake pin added before). 
3. Connecting the target pin (fake pin) with the corresponding source pin (internal pin)
4. Change the name of target pin (fake pin), making it have the same name of internal pin
# Useful methods
Here some commonly used methods are introduced. The parameters are hidden since some of them have many parameters.
- **replace_layout_pin()**
  - function: remove the old pin and replace with a new one
  - file: /OpenRAM/compiler/base/hierarchy_layout.py
  - comments: usually used as self.design.replace_layout_pin(), and this method is used commonly when want to change a name of pin in gds
- **remove_layout_pin()**
  - function: delete a pin with the given pin name
  - file: /OpenRAM/compiler/base/hierarchy_layout.py
  - comments: usually used as self.design.remove_layout_pin()
- **add_via_stack_center()**
  - function: add via at a certain position, from start_layer to target_layer, the vias of the layers between them will also be added
  - file: /OpenRAM/compiler/base/hierarchy_layout.py
  - comments: usually used as self.design.add_via_stack_center(), useful when want to add vias
- **add_rect()**
  - function: add a rectangle on a given layer,offset with width and height
  - file: /OpenRAM/compiler/base/hierarchy_layout.py 
  - comments: usually used as self.design.add_rect(), useful when want to draw metal wires in gds, easier than using wire.py class
- **.x**
  - function: return the x-coordinate of a vector
  - comments: commonly used 
- **.center()**
  - function: return the coordinate(vector(x,y)) of the object (could be a pin, a rectangle)
  - comments: commonly used, like target_pin.center().x
