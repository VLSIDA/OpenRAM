
.SUBCKT cell_6t bl br wl vdd gnd
MM3 bl wl net10 gnd NMOS_VTG W=135.00n L=50n
MM2 br wl net4 gnd NMOS_VTG W=135.00n L=50n 
MM1 net10 net4 gnd gnd NMOS_VTG W=205.00n L=50n 
MM0 net4 net10 gnd gnd NMOS_VTG W=205.00n L=50n 
MM5 net10 net4 vdd vdd PMOS_VTG W=90n L=50n 
MM4 net4 net10 vdd vdd PMOS_VTG W=90n L=50n 
.ENDS cell_6t

