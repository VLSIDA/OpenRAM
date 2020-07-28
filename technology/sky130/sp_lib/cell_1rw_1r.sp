
.SUBCKT cell_1rw_1r bl0 br0 bl1 br1 wl0 wl1 vdd gnd
** N=11 EP=8 IP=0 FDC=16
*.SEEDPROM

* Bitcell Core
M0 Q wl1 bl1 gnd npd W=0.21 L=0.15
M1 gnd Q_bar Q gnd npd W=0.21 L=0.15
M2 gnd Q_bar Q gnd npd W=0.21 L=0.15
M3 bl0 wl0 Q gnd npd W=0.21 L=0.15
M4 Q_bar wl1 br1 gnd npd W=0.21 L=0.15
M5 gnd Q Q_bar gnd npd W=0.21 L=0.15
M6 gnd Q Q_bar gnd npd W=0.21 L=0.15
M7 br0 wl0 Q_bar gnd npd W=0.21 L=0.15
M8 vdd Q Q_bar vdd ppu W=0.14 L=0.15
M9 Q Q_bar vdd vdd ppu W=0.14 L=0.15

* drainOnly PMOS
* M10 Q_bar wl1 Q_bar vdd ppu L=0.08 W=0.14
* M11 Q wl0 Q vdd ppu L=0.08 W=0.14

* drainOnly NMOS
M12 bl1 gnd bl1 gnd npd W=0.21 L=0.08
M14 br1 gnd br1 gnd npd W=0.21 L=0.08

.ENDS
