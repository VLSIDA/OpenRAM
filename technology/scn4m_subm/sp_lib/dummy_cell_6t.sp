
*********************** "dummy_cell_6t" ******************************
.SUBCKT dummy_cell_6t bl br wl vdd gnd

* Inverter 1
M1000 Q Qbar vdd vdd p w=0.6u l=0.8u
M1002 Q Qbar gnd gnd n w=1.6u l=0.4u

* Inverter 2
M1001 vdd Q Qbar vdd p w=0.6u l=0.8u
M1003 gnd Q Qbar gnd n w=1.6u l=0.4u

* Access transistors
M1004 Q wl bl_noconn gnd n w=0.8u l=0.4u
M1005 Qbar wl br_noconn gnd n w=0.8u l=0.4u

.ENDS
