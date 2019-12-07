# Debugging

When OpenRAM runs, it puts files in a temporary directory that is
shown in the banner at the top. Like:
```
  /tmp/openram_mrg_18128_temp/
```
This is where simulations and DRC/LVS get run so there is no network
traffic. The directory name is unique for each person and run of
OpenRAM to not clobber any files and allow simultaneous runs. If it
passes, the files are deleted. If it fails, you will see these files:
+ temp.gds is the layout (.mag files too if using SCMOS)
+ temp.sp is the netlist
+ test1.drc.err is the std err output of the DRC command
+ test1.drc.out is the standard output of the DRC command
+ test1.drc.results is the DRC results file
+ test1.lvs.err is the std err output of the LVS command
+ test1.lvs.out is the standard output of the LVS command
+ test1.lvs.results is the DRC results file

Depending on your DRC/LVS tools, there will also be:
+ \_calibreDRC.rul\_ is the DRC rule file (Calibre)
+ dc_runset is the command file (Calibre)
+ extracted.sp (Calibre)
+ run_lvs.sh is a Netgen script for LVS (Netgen)
+ run_drc.sh is a Magic script for DRC (Magic)
+ <topcell>.spice (Magic)

If DRC/LVS fails, the first thing is to check if it ran in the .out and
.err file. This shows the standard output and error output from
running DRC/LVS. If there is a setup problem it will be shown here.

If DRC/LVS runs, but doesn't pass, you then should look at the .results
file. If the DRC fails, it will typically show you the command that was used
to run Calibre or Magic+Netgen. 

To debug, you will need a layout viewer. I prefer to use Glade 
on my Mac, but you can also use Calibre, Magic, etc. 

1. Klayout

   You can view the designs in [Klayout](https://www.klayout.de/) with the configuration
   file provided in the tech directories. For example,
```
  klayout temp.gds -l /home/vagrant/openram/technology/freepdk45/tf/FreePDK45.lyp
```

2. Calibre

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

3. Glade

   You can view errors in [Glade](http://www.peardrop.co.uk/glade/) as well. 

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

   To load the errors, you simply do Verify->Import Calibre Errors select
   the .results file from Calibre.

4. Magic

   Magic is only supported in SCMOS. You will need to install the MOSIS SCMOS rules
   and [Magic](http://opencircuitdesign.com/)

   When running DRC or extraction, OpenRAM will load the GDS file, save
   the .ext/.mag files, and export an extracted netlist (.spice).

5. It is possible to use other viewers as well, such as:
   * [LayoutEditor](http://www.layouteditor.net/)


# Example to output/input .gds layout files from/to Cadence

1. To create your component layouts, you should stream them to
   individual gds files using our provided layermap and flatten
   cells. For example,
```
  strmout -layerMap layers.map -library sram -topCell $i -view layout -flattenVias -flattenPcells -strmFile ../gds_lib/$i.gds
```
2. To stream a layout back into Cadence, do this:
```
  strmin -layerMap layers.map -attachTechFileOfLib NCSU\_TechLib\_FreePDK45 -library sram_4_32 -strmFile sram_4_32.gds
```
   When you import a gds file, make sure to attach the correct tech lib
   or you will get incorrect layers in the resulting library.
