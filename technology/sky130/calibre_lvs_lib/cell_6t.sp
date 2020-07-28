
.SUBCKT cell_6t bl br wl vdd gnd
* Inverter 1
Mnpd_bar Qbar Q gnd gnd npd W=0.210 L=0.150 m=1 mult=1
Mppu_bar Qbar Q vdd vdd pp W=0.140 L=0.150 m=1 mult=1

* Inverer 2
Mnpd_tr Q Qbar gnd gnd npd W=0.210 L=0.150 m=1 mult=1
Mppu_tr Q Qbar vdd vdd pp W=0.140 L=0.150 m=1 mult=1

* Access transistors
Mnpass_tr bl wl Q gnd npass W=0.140 L=0.150 m=1 mult=1
Mnpass_bar br wl Qbar gnd npass W=0.140 L=0.150 m=1 mult=1

* Parasitic transistors
Mpdo_tr Q wl Q vdd pp W=0.140 L=0.25 m=1 mult=1
Mpdo_bar Qbar wl Qbar vdd pp W=0.140 L=0.25 m=1 mult=1

.ENDS cell_6t
