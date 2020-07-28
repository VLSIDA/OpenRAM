# OpenRAM

OpenRAM is a compiler based sRAM, that produces layouts, netlists, power models and timing. The compiler has some dependencies:
1.	Configuration of the memories are done using Python, therefore you need Python 3.5+ and Numpy.
2.	To generate spice, you need a spice simulator. Supported simulators:
a.	Ngspice 26 (or later)
b.	Hspice I-2013.12-1 (or later)
c.	CustomSim 2017 (or later)
3.	For DRC tests, you can either use Calibre 2017.3_29.23 or Magic 8.x that can be found in this link http://opencircuitdesign.com/magic/
4.	For LVS tests, you can either use Calibre 2017.3_29.23 or Netgen 1.5 that can be found in this link http://opencircuitdesign.com/netgen/ 

# User tutorial:
## 1.	You need to clone the repository from github using command
```
$ git clone https://github.com/marwaneltoukhy/OpenRAM-SKY130.git
```
## 2.	To set up the environment:
```
$ export OPENRAM_HOME="$HOME/OpenRAM/compiler"
$ export OPENRAM_TECH="$HOME/OpenRAM/technology"
$ export PYTHONPATH="$PYTHONPATH:$OPENRAM_HOME"
```
## 3.	Ubuntu docker image:
Can be pulled from https://hub.docker.com/r/vlsida/openram-ubuntu
Or pull using this command:
```
$ docker pull vlsida/openram-ubuntu
```
If you get a “Permission denied” error you can fix it using this command
```
$ sudo chmod 666 /var/run/docker.sock
```
## 4.	Example of configuration file using python 3.5+:

create a file called myconfig.py

```
# Data word size
word_size = 2
# Number of words in the memory
num_words = 16
# Technology to use in $OPENRAM_TECH
tech_name = "scn4m_subm"
# You can use the technology nominal corner only
nominal_corner_only = True
# Or you can specify particular corners
# Process corners to characterize
# process_corners = ["SS", "TT", "FF"]
# Voltage corners to characterize
# supply_voltages = [ 3.0, 3.3, 3.5 ]
# Temperature corners to characterize
# temperatures = [ 0, 25 100]
# Output directory for the results
output_path = "temp"
# Output file base name
output_name = "sram_{0}_{1}_{2}".format(word_size,num_words,tech_name)
# Disable analytical models for full characterization (WARNING: slow!)
# analytical_delay = False
```

To execute the configuration file:
```
$ python3 $OPENRAM_HOME/openram.py myconfig
```
### Configuration file options:
- Characterization corners                                   
   - supply_voltages = [1.7, 1.8, 1.9]
   - temperatures = [25, 50, 100]
   - process_corners = [“SS”, “TT”, “FF”]
- Do not generate layout
  - netlist_only=True
- Multi-port options
  - num_rw_ports=1
  - num_r_ports=1
  - num_w_ports=0
- Customized module or bit cell
  - bitcell = “bitcell_1rw_1r”
  - replica_bitcell = “replica_bitcell_1rw_1r”
- Enable simulation characterization
  - WARNING! Slow!
  - analytical_delay=False
- Output name and location
  - output_path = "temp"
  - output_name = "sram_32x256"
- Force tool selection (should match the PDK!) 
  - drc_name = "magic"
  - lvs_name = "netgen"
  - pex_name = "magic"
- Include shared configuration options using Python imports
  - from corners_freepdk45 import *

You can find the output files in *output_dir* in configuration file

Names are specified as *output_name* and the suffix

## 5.  For Testing

You can perform regression tests which run tests on all the modules using the command:
```
$ python3 regress.py
```
Or you can run a specific test using the command
```
$ python3 {unit test}.py 
```
You can specify the technology using -t for example "-t freepdk45"

# Debugging

Testing using ngspice version 26 or later.

After compiling the config file, you should find the output files in the file specified in the config file. In the example given it's called "temp"

## The output files:

- GDS (.gds) a file that contains information about the layout, it can be viewed via cascde

- SPICE (.sp) a file that contains information about the circuit and can be used to plot graphs using the spice simulators

- Verilog (.v) a file that has verilog code that defined the circuit

- P&R Abstract (.lef) a file that contains design rules and abstract information about the cells

- Liberty (.lib) a file that contains the libraries

- Datasheet (.html)

- Log (.log) has the output log file, it is printed once you compile

## Debugging

if the DRC or LVS fail you will see files that ends with .drc.err and/or .lvs.err, from there you can figure out errors.

### files that result from fails:

- temp.gds is the layout (.mag files too if using SCMOS)

- temp.sp is the netlist

- test1.drc.err is the std err output of the DRC command

- test1.drc.out is the standard output of the DRC command

- test1.drc.results is the DRC results file

- test1.lvs.err is the std err output of the LVS command

- test1.lvs.out is the standard output of the LVS command

- test1.lvs.results is the DRC results file

### if calibre is being used you might see

- _calibreDRC.rul_ is the DRC rule file (Calibre)

- dc_runset is the command file (Calibre)

- extracted.sp (Calibre)

### if Netgen is being used:

- run_lvs.sh is a Netgen script for LVS (Netgen)

### if Magic is being used

- run_drc.sh is a Magic script for DRC (Magic)

- .spice (Magic)

# Measurements 

There are several ways that you can look at all the measurements from the output files.

One way is to open the .html file that is produced from the compiler in the output file directory that you specified in the configuration file, this will show you all the measurements and the data you might need to know in a datasheet.

The other way is to look at the Liberty file (.lib), this is the file that has all the readings and measurements that you need, but it might take a while to understand how to find what you're looking for, especially if you are not familiar with the Liberty file format. To get more familiar you can take a look at the [Liberty Reference Manual](https://people.eecs.berkeley.edu/~alanmi/publications/other/liberty07_03.pdf).

# Sample Configuration files

[Sample Config Files](https://github.com/VLSIDA/OpenRAM/tree/master/compiler/example_configs)

will be adding new Config files here.

# Changing Technology

OpenRAM supports the change of technology, the default technology is [SCMOS](https://www.mosis.com/files/scmos/scmos.pdf) SCN4M_SUBM, that would work automatically after pulling the [repo](https://github.com/VLSIDA/OpenRAM) from GitHub. OpenRAM also supports FreePDK45, but for you to run the DRC and LVS you need to download the [technology file](https://www.eda.ncsu.edu/eda_registration.php) by simply registring using your email and an email will be sent immediately with the link for download (NOTE: You can only use the technology on the machine you are working on). 

You then have to point the environment variable to the PDK, for example:

```
$ export FREEPDK45="/bsoe/software/design-kits/FreePDK45"
```

### Changing to a new Technology

In the case that you want to change to another technology that isn't SCN4M_SUBM or FreePDK45, you need to have some files to work with. First of all you need a directory to put all the files in (you can mimic the path of other technologies in "$OPENRAM_TECH/" directory). Moreover, you need a setup file, like the one you can find in ```$OPENRAM_TECH/freepdk45/__init__.py```. Also, you need technology files that include but are not limited to (you can look at the files from the exisiting technologies for better understanding):

- gds_lib folder with all the .gds (premade) library cells:
  - dff.gds
  - sense_amp.gds
  - write_driver.gds
  - cell_6t.gds
  - replica_cell_6t.gds
  - dummy_cell_6t.gds
- sp_lib folder with all the .sp (premade) library netlists for the above cells.
- layers.map
- A valid tech Python module (tech directory with __init__.py and tech.py) with:
  - References in tech.py to spice models
  - DRC/LVS rules needed for dynamic cells and routing
  - Layer information
  - Spice and supply information
  - etc.
  

# References

[OpenRAM](https://github.com/VLSIDA/OpenRAM)

[Documentation for OpenRAM](https://docs.google.com/presentation/d/10InGB33N51I6oBHnqpU7_w9DXlx-qe9zdrlco2Yc5co/edit#slide=id.g4e915a9f17_2_45)
