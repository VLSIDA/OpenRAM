
.SUBCKT cell_6t bl br wl vdd gnd
MM3 bl wl Q gnd NMOS_VTG W=135.00n L=50n
MM2 br wl Qb gnd NMOS_VTG W=135.00n L=50n 
MM1 Q Qb gnd gnd NMOS_VTG W=205.00n L=50n 
MM0 Qb Q gnd gnd NMOS_VTG W=205.00n L=50n 
MM5 Q Qb vdd vdd PMOS_VTG W=90n L=50n 
MM4 Qb Q vdd vdd PMOS_VTG W=90n L=50n 
.ENDS cell_6t

