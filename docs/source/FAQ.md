### [Go Back](./index.md#table-of-contents)

# Frequently Asked Questions

## What to do if OpenRAM encounters an error?

When OpenRAM runs, it puts files in a temporary directory that is
shown in the banner at the top. Like:
```
  /tmp/openram_mrg_18128_temp/
```
This is where simulations and DRC/LVS get run so there is no network
traffic. The directory name is unique for each person and run of
OpenRAM to not clobber any files and allow simultaneous runs. If it
passes, the files are deleted. If it fails, you will see these files:
+ `temp.gds` is the layout (.mag files too if using SCMOS)
+ `temp.sp` is the netlist
+ `test1.drc.err` is the std err output of the DRC command
+ `test1.drc.out` is the standard output of the DRC command
+ `test1.drc.results` is the DRC results file
+ `test1.lvs.err` is the std err output of the LVS command
+ `test1.lvs.out` is the standard output of the LVS command
+ `test1.lvs.results` is the DRC results file

Depending on your DRC/LVS tools, there will also be:
+ `run\_drc.sh` is a script to run DRC
+ `run\_ext.sh` is a script to run extraction
+ `run\_lvs.sh` is a script to run LVS

If DRC/LVS fails, the first thing is to check if it ran in the `.out` and
`.err` file. This shows the standard output and error output from
running DRC/LVS. If there is a setup problem it will be shown here.

If DRC/LVS runs, but doesn't pass, you then should look at the `.results`
file. If the DRC fails, it will typically show you the command that was used
to run Calibre or Magic+Netgen. 


