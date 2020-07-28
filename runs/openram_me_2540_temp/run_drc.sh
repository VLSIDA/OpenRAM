#!/bin/sh
/ef/apps/bin/magic -dnull -noconsole << EOF
gds polygon subcell true
gds warning default
gds read sram_2_16_sky130.gds
load sram_2_16_sky130
cellname delete \(UNNAMED\)
writeall force
select top cell
expand
drc check
drc catchup
drc count total
drc count
port makeall
extract style ngspice(si)
extract
ext2spice hierarchy on
ext2spice format ngspice
ext2spice cthresh infinite
ext2spice rthresh infinite
ext2spice renumber off
ext2spice scale off
ext2spice blackbox on
ext2spice subcircuit top auto
ext2spice global off
ext2spice sram_2_16_sky130
quit -noprompt
EOF
