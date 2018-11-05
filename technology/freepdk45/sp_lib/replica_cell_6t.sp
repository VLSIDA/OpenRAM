
.SUBCKT replica_cell_6t bl br wl vdd gnd

* Inverter 1
MM4 Qbar gnd vdd vdd PMOS_VTG W=90n L=50n
MM0 Qbar gnd gnd gnd NMOS_VTG W=205.00n L=50n 

* Inverter 2
MM5 gnd Qbar vdd vdd PMOS_VTG W=90n L=50n
MM1 gnd Qbar gnd gnd NMOS_VTG W=205.00n L=50n

* Access transistors
MM3 bl wl gnd gnd NMOS_VTG W=135.00n L=50n
MM2 br wl Qbar gnd NMOS_VTG W=135.00n L=50n 
.ENDS replica_cell_6t

