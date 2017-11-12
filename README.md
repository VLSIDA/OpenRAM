# BASIC SETUP

Please look at the OpenRAM ICCAD paper and presentation in the repository:
https://github.com/mguthaus/OpenRAM/blob/master/OpenRAM_ICCAD_2016_paper.pdf
https://github.com/mguthaus/OpenRAM/blob/master/OpenRAM_ICCAD_2016_presentation.pdf

The OpenRAM compiler has very few dependencies:
* ngspice-26 (or later) or HSpice I-2013.12-1 (or later) or CustomSim 2017 (or later)
* Python 2.7 and higher (currently excludes Python 3 and up)
* a setup script for each technology
* a technology directory for each technology with the base cells

You must set two environment variables: OPENRAM_HOME should point to
the compiler source directory. OPENERAM_TECH should point to a root
technology directory that contains subdirs of all other technologies.
For example, in bash, add to your .bashrc:
```
  export OPENRAM_HOME="$HOME/OpenRAM/compiler"
  export OPENRAM_TECH="$HOME/OpenRAM/technology"
```
For example, in csh/tcsh, add to your .cshrc/.tcshrc:
```
  setenv OPENRAM_HOME "$HOME/OpenRAM/compiler"
  setenv OPENRAM_TECH "$HOME/OpenRAM/technology"
```
If you are using FreePDK, you should also have that set up and have the
environment variable point to the PDK. 
For example, in bash, add to your .bashrc:
```
  export FREEPDK45="/bsoe/software/design-kits/FreePDK45"
```
For example, in csh/tcsh, add to your .tcshrc:
```
  setenv FREEPDK45 "/bsoe/software/design-kits/FreePDK45"
```
We do not distribute the PDK, but you may get it from:
    https://www.eda.ncsu.edu/wiki/FreePDK45:Contents


# DIRECTORY STRUCTURE

* compiler - openram compiler itself (pointed to by OPENRAM_HOME)
  * compiler/characterizer - timing characterization code
  * compiler/gdsMill - GDSII reader/writer
  * compiler/router - detailed router
  * compiler/tests - unit tests
* technology - openram technology directory (pointed to by OPENRAM_TECH)
  * technology/freepdk45 - example configuration library for freepdk45 technology node
  * technology/scn3me_subm - example configuration library SCMOS technology node
  * technology/setup_scripts - setup scripts to customize your PDKs and OpenRAM technologies


# UNIT TESTS

Regression testing  performs a number of tests for all modules in OpenRAM.

Use the command:
```
   python regress.py
```
To run a specific test:
```
   python {unit test}.py 
```
The unit tests take the same arguments as openram.py itself. 

To increase the verbosity of the test, add one (or more) -v options:
```
   python tests/00_code_format_check_test.py -v -t freepdk45
```
To specify a particular technology use "-t <techname>" such as
"-t scn3me_subm". The default for a unit test is freepdk45 whereas
the default for openram.py is specified in the configuration file.

A regression daemon script that can be used with cron is included in
a separate repository at https://github.com/mguthaus/openram-daemons
```
   regress_daemon.py
   regress_daemon.sh
```
This updates a git repository, checks out code, and sends an email
report with status information.

# CREATING CUSTOM TECHNOLOGIES

All setup scripts should be in the setup_scripts directory under the
$OPENRAM_TECH directory.  Please look at the following file for an
example of what is needed for OpenRAM:
```
  $OPENRAM_TECH/setup_scripts/setup_openram_freepdk45.py
```
Each setup script should be named as: setup_openram_{tech name}.py.

Each specific technology (e.g., freepdk45) should be a subdirectory
(e.g., $OPENRAM_TECH/freepdk45) and include certain folders and files:
  1. gds_lib folder with all the .gds (premade) library cells. At a
     minimum this includes:
     * ms_flop.gds
     * sense_amp.gds
     * write_driver.gds
     * cell_6t.gds
     * replica_cell_6t.gds 
     * tri_gate.gds
  2. sp_lib folder with all the .sp (premade) library netlists for the above cells.
  3. layers.map 
  4. A valid tech Python module (tech directory with __init__.py and tech.py) with:
     * References in tech.py to spice models
     * DRC/LVS rules needed for dynamic cells and routing
     * Layer information
     * etc.

# DEBUGGING

When OpenRAM runs, it puts files in a temporary directory that is
shown in the banner at the top. Like:
```
  /tmp/openram_mrg_18128_temp/
```
This is where simulations and DRC/LVS get run so there is no network
traffic. The directory name is unique for each person and run of
OpenRAM to not clobber any files and allow simultaneous runs. If it
passes, the files are deleted. If it fails, you will see these files:
* _calibreDRC.rul_ is the DRC rule file.
* dc_runset is the command file for caliber.
* temp.gds is the layout
* test1.drc.err is the std err output of the command
* test1.drc.out is the standard output of the command
* test1.drc.db is the DRC results file

If DRC/LVS fails, the first thing is to check if it ran in the .out and
.err file. This shows the standard output and error output from
running DRC/LVS. If there is a setup problem it will be shown here.

If DRC/LVS runs, but doesn't pass, you then should look at the .db
file. If the DRC fails, it will typically show you the command that was used
to run caliber. It is something like this:
```
  calibre -gui -drc /tmp/openram_mrg_28781_temp/drc_runset -batch 2>
  /tmp/openram_mrg_28781_temp/test1.drc.err 1>
  /tmp/openram_mrg_28781_temp/test1.drc.out
```
To debug, you will need a layout viewer. I prefer to use glade on my
Mac, but you can also use Calibre, Magic, etc. 

1. Calibre

   Start the Calibre DESIGNrev viewer in the temp directory and load your GDS file:
```
  calibredrv temp.gds
```
   Select Verification->Start RVE and select the results database file in
   the new form (e.g., test1.drc.db). This will start the RVE (results
   viewer). Scroll through the check pane and find the DRC check with an
   error.  Select it and it will open some numbers to the right.  Double
   click on any of the errors in the result browser. These will be
   labelled as numbers "1 2 3 4" for example will be 4 DRC errors.

   In the viewer ">" opens the layout down a level.

2. Glade

   You can view errors in Glade as well. I like this because it is on my laptop.
   You can get it from:  http://www.peardrop.co.uk/glade/

   To remote display over X windows, you need to disable OpenGL acceleration or use vnc
   or something. You can disable by adding this to your .bashrc in bash:
```
  export GLADE_USE_OPENGL=no
```
   or in .cshrc/.tcshrc in csh/tcsh:
```
  setenv GLADE_USE_OPENGAL no
```
   To use this with the FreePDK45 or SCMOS layer views you should use the
   tech files. Then create a .glade.py file in your user directory with
   these commands to load the technology layers:
```
ui().importCds("default",
"/Users/mrg/techfiles/freepdk45/display.drf",
"/Users/mrg/techfiles/freepdk45/FreePDK45.tf", 1000, 1,
"/Users/mrg/techfiles/freepdk45/layers.map")
```
   Obviously, edit the paths to point to your directory. To switch
   between processes, you have to change the importCds command (or you
   can manually run the command each time you start glade).

   To load the errors, you simply do Verify->Import Caliber Errors select
   the .db file from calibre.

3. It is possible to use other viewers as well, such as:
   * LayoutEditor http://www.layouteditor.net/ 
   * Magic http://opencircuitdesign.com/magic/


# Example to output/input .gds layout files from/to Cadence

1. To create your component layouts, you should stream them to
   individual gds files using our provided layermap and flatten
   cells. For example,
```
  strmout -layerMap layers.map -library sram -topCell $i -view layout -flattenVias -flattenPcells -strmFile ../gds_lib/$i.gds
```
2. To stream a layout back into Cadence, do this:
```
  strmin -layerMap layers.map -attachTechFileOfLib NCSU_TechLib_FreePDK45 -library sram_4_32 -strmFile sram_4_32.gds
```
   When you import a gds file, make sure to attach the correct tech lib
   or you will get incorrect layers in the resulting library.

