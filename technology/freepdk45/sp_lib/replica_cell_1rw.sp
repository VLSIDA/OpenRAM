
.SUBCKT replica_cell_1rw bl br wl vdd gnd
* Inverter 1
MM0 vdd Q gnd gnd NMOS_VTG W=205.00n L=50n
MM4 vdd Q vdd vdd PMOS_VTG W=90n L=50n

* Inverer 2
MM1 Q vdd gnd gnd NMOS_VTG W=205.00n L=50n 
MM5 Q vdd vdd vdd PMOS_VTG W=90n L=50n

* Access transistors
MM3 bl wl Q gnd NMOS_VTG W=135.00n L=50n
MM2 br wl vdd gnd NMOS_VTG W=135.00n L=50n 
.ENDS cell_1rw

