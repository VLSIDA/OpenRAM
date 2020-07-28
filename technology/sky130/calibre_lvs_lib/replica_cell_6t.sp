
.SUBCKT replica_cell_6t bl br wl vdd gnd
* Inverter 1
Mnpd_bar vdd Q gnd gnd npd W=0.210 L=0.150 m=1 mult=1
Mppu_bar vdd Q vdd vdd pp W=0.140 L=0.150 m=1 mult=1

* Inverer 2
Mnpd_tr Q vdd gnd gnd npd W=0.210 L=0.150 m=1 mult=1
Mppu_tr Q vdd vdd vdd pp W=0.140 L=0.150 m=1 mult=1

* Access transistors
Mnpass_tr bl wl Q gnd npass W=0.140 L=0.150 m=1 mult=1
Mnpass_bar br wl vdd gnd npass W=0.140 L=0.150 m=1 mult=1

* Parasitic transistors
Mpdo_tr Q wl Q vdd pp W=0.140 L=0.25 m=1 mult=1

Mpdo_bar vdd wl vdd vdd pp W=0.140 L=0.25 m=1 mult=1

.ENDS replica_cell_6t
