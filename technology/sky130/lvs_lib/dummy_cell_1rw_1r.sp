
.SUBCKT dummy_cell_1rw_1r bl0 br0 bl1 br1 wl0 wl1 vdd gnd
** N=14 EP=6 IP=0 FDC=16
*.SEEDPROM

* Bitcell Core
M1 1 gnd gnd gnd npd W=0.21u L=0.15u m=1
M2 1 wl1 bl1 gnd npd W=0.21u L=0.15u m=1
M3 2 gnd gnd gnd npd W=0.21u L=0.15u m=1
M4 2 wl1 br1 gnd npd W=0.21u L=0.15u m=1
M5 3 gnd gnd gnd npd W=0.21u L=0.15u m=1
M6 3 wl0 bl0 gnd npd W=0.21u L=0.15u m=1
M7 4 gnd gnd gnd npd W=0.21u L=0.15u m=1
M8 4 wl0 br0 gnd npd W=0.21u L=0.15u m=1

* drainOnly NMOS
M9 bl1 gnd bl1 gnd npd W=0.21u L=0.08u m=1
M10 br1 gnd br1 gnd npd W=0.21u L=0.08u m=1

.ENDS
