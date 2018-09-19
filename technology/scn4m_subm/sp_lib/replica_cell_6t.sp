
*********************** "cell_6t" ******************************
.SUBCKT replica_cell_6t bl br wl vdd gnd
* SPICE3 file created from replica_cell_6t.ext - technology: scmos

M1000 gnd a_28_32# vdd vdd p w=0.6u l=0.8u
M1001 vdd gnd a_28_32# vdd p w=0.6u l=0.8u
** SOURCE/DRAIN TIED
M1002 gnd a_28_32# gnd gnd n w=1.6u l=0.4u
M1003 gnd gnd a_28_32# gnd n w=1.6u l=0.4u
M1004 gnd wl bl gnd n w=0.8u l=0.4u
M1005 a_28_32# wl br gnd n w=0.8u l=0.4u

.ENDS
