#!/bin/sh
/ef/apps/bin/netgen -noconsole << EOF
readnet spice sram_2_16_sky130.spice
readnet spice sram_2_16_sky130.sp
log sram_2_16_sky130.lvs.report
lvs {sram_2_16_sky130.spice sram_2_16_sky130} {sram_2_16_sky130.sp sram_2_16_sky130} setup.tcl sram_2_16_sky130.lvs.report
quit
EOF
