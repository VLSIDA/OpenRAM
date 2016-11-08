
.SUBCKT replica_cell_6t bl br wl vdd gnd
MM3 bl wl gnd gnd NMOS_VTG W=135.00n L=50n
MM2 br wl net4 gnd NMOS_VTG W=135.00n L=50n 
MM1 gnd net4 gnd gnd NMOS_VTG W=205.00n L=50n 
MM0 net4 gnd gnd gnd NMOS_VTG W=205.00n L=50n 
MM5 gnd net4 vdd vdd PMOS_VTG W=90n L=50n 
MM4 net4 gnd vdd vdd PMOS_VTG W=90n L=50n 
.ENDS replica_cell_6t

