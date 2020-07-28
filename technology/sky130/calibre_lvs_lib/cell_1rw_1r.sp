
.SUBCKT cell_1rw_1r bl0 br0 bl1 br1 wl0 wl1 vdd gnd
** N=11 EP=8 IP=0 FDC=16
*.SEEDPROM

* Bitcell Core
M0 Q wl1 bl1 gnd npd W=0.21 L=0.15 m=1 mult=1
M1 gnd Q_bar Q gnd npd W=0.21 L=0.15 m=1 mult=1
M2 gnd Q_bar Q gnd npd W=0.21 L=0.15 m=1 mult=1
M3 bl0 wl0 Q gnd npd W=0.21 L=0.15 m=1 mult=1
M4 Q_bar wl1 br1 gnd npd W=0.21 L=0.15 m=1 mult=1
M5 gnd Q Q_bar gnd npd W=0.21 L=0.15 m=1 mult=1
M6 gnd Q Q_bar gnd npd W=0.21 L=0.15 m=1 mult=1
M7 br0 wl0 Q_bar gnd npd W=0.21 L=0.15 m=1 mult=1
M8 vdd Q Q_bar vdd ppu W=0.14 L=0.15 m=1 mult=1
M9 Q Q_bar vdd vdd ppu W=0.14 L=0.15 m=1 mult=1

* drainOnly PMOS
M10 Q_bar wl1 Q_bar vdd ppu W=0.14 L=0.08 m=1 mult=1
M11 Q wl0 Q vdd ppu W=0.14 L=0.08 m=1 mult=1

* drainOnly NMOS
M12 bl1 gnd bl1 gnd npd W=0.21 L=0.08 m=1 mult=1
M14 br1 gnd br1 gnd npd W=0.21 L=0.08 m=1 mult=1

.ENDS
