###############################################################################
BASIC SETUP

-The OpenRAM compiler has very few dependencies:

1) ngspice v20 or later or HSpice I-2013.12-1 or later
2) Python 2.7 and higher (currently excludes Python 3 and up)
3) a setup script for each technology
4) a technology directory for each technology with the base cells

- You must set two environment variables: OPENRAM_HOME should point to
the compiler source directory OPENERAM_TECH should point to a root
technology directory that contains subdirs of all other technologies.

-All setup scripts should be in the setup_scripts directory under the
technology directory.  Please look at the file
setup_openram_freepdk45.py for an example of what is needed for
OpenRAM.  Each setup script should be named as: setup_openram_{tech
folder name}.py.

-Each specific technology (e.g. freepdk45) should be a subdirectory
 and include certain folders and files:

1) gds_lib folder with all the .gds (premade) library cells. At a
minimum this includes:
 ms_flop.gds         
 sense_amp.gds       
 write_driver.gds
 cell_6t.gds         
 replica_cell_6t.gds 
 tri_gate.gds

2) sp_lib folder  with all the .sp (premade) library netlists for the above cells.

3) layers.map 

4) References in tech.py to spice models that correspond to the
transistors in the cells

5) OpenRAM tech file (tech.py) that contains library, DRC/LVS
information, layer information, etc. for the technology

- In order to debug, it is useful to have a GDS viewer. In addition to
normal layout tools, we recommend the following viewers:

LayoutEditor http://www.layouteditor.net/ 
GLADE http://www.peardrop.co.uk/
Magic http://opencircuitdesign.com/magic/

###############################################################################
DIRECTORY STRUCTURE

compiler - openram compiler itself (pointed to by OPENRAM_HOME)
compiler/characterizer - timing characterization code
compiler/gdsMill - gds reader/writer
compiler/tests - unit tests
technology/freepdk45 - example configuration library for freepdk45 technology node
technology/scn3me_subm - example configuration library SCMOS technology node
technology/setup_scripts - setup scripts to customize your PDKs and OpenRAM technologies

###############################################################################
Example to output/input .gds layout files from/to Cadence

1) To create your component layouts, you should stream them to
individual gds files using our provided layermap and flatten
cells. For example,

  strmout -layerMap layers.map -library sram -topCell $i -view layout -flattenVias -flattenPcells -strmFile ../gds_lib/$i.gds

2) To stream a layout back into Cadence, do this:

  strmin -layerMap layers.map -attachTechFileOfLib NCSU_TechLib_FreePDK45 -library sram_4_32 -strmFile sram_4_32.gds

When you import a gds file, make sure to attach the correct tech lib
or you will get incorrect layers in the resulting library.



###############################################################################
UNIT TESTS

Regression testing  performs a number of tests for all modules in OpenRAM.

Steps to run regression testing:
1) First, ensure your setup_scripts is correctly setup.
2) Navigate to the compiler directory (trunk/compiler/tests)
3) Use the command: 
   python regress.py 
4) To run a specific test:
   python {unit test}.py 

The unit tests take the same arguments as openram.py itself. 

To increase the verbosity of the test, add one (or more) -v options:
python tests/00_code_format_check_test.py -v

To specify a particular technology use "-t <techname>" such as
"-t scn3me_subm"

A regression daemon script that can be used with cron is included:
regress_daemon.py
regress_daemon.sh

This updates a git repository, checks out code, and sends an email
report with status information.


