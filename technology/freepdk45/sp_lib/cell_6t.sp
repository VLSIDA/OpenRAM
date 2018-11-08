
.SUBCKT cell_6t bl br wl vdd gnd
* Inverter 1
MM0 Qbar Q gnd gnd NMOS_VTG W=205.00n L=50n
MM4 Qbar Q vdd vdd PMOS_VTG W=90n L=50n

* Inverer 2
MM1 Q Qbar gnd gnd NMOS_VTG W=205.00n L=50n 
MM5 Q Qbar vdd vdd PMOS_VTG W=90n L=50n

* Access transistors
MM3 bl wl Q gnd NMOS_VTG W=135.00n L=50n
MM2 br wl Qbar gnd NMOS_VTG W=135.00n L=50n 
.ENDS cell_6t

