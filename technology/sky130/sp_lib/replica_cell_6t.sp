
.SUBCKT replica_cell_6t bl br wl vdd gnd
* Inverter 1
Mnpd_bar vdd Q gnd gnd npd W=0.210 L=0.150
Mppu_bar vdd Q vdd vdd ppu W=0.140 L=0.150

* Inverer 2
Mnpd_tru Q vdd gnd gnd npd W=0.210 L=0.150 
Mppu_tru Q vdd vdd vdd ppu W=0.140 L=0.150

* Access transistors
Mnpass_tru bl wl Q gnd npass W=0.140 L=0.150
Mnpass_bar br wl vdd gnd npass W=0.140 L=0.150

* Parasitic transistors
Mpdo_tru Q wl Q vdd ppu W=0.140 L=0.025
Mpdo_bar vdd wl vdd vdd ppu W=0.140 L=0.025

.ENDS replica_cell_6t
