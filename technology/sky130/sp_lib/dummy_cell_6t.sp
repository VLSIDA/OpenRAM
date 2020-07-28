
.SUBCKT dummy_cell_6t bl br wl vdd gnd
* Inverter 1
Mnpd_bar Qbar Q gnd gnd npd W=0.210 L=0.150
Mppu_bar Qbar Q vdd vdd ppu W=0.140 L=0.150

* Inverer 2
Mnpd_tru Q Qbar gnd gnd npd W=0.210 L=0.150 
Mppu_tru Q Qbar vdd vdd ppu W=0.140 L=0.150

* Access transistors
Mnpass_tru bl_noconn wl Q gnd npass W=0.140 L=0.150
Mnpass_bar br_noconn wl Qbar gnd npass W=0.140 L=0.150

* Parasitic transistors
Mpdo_tru Q wl Q vdd ppu W=0.140 L=0.025
Mpdo_bar Qbar wl Qbar vdd ppu W=0.140 L=0.025

.ENDS dummy_cell_6t
