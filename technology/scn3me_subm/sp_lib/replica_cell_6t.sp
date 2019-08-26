
*********************** "cell_6t" ******************************
.SUBCKT replica_cell_6t bl br wl vdd gnd
M_1 gnd net_2 vdd vdd p W='0.9u' L=1.2u 
M_2 net_2 gnd vdd vdd p W='0.9u' L=1.2u 
M_3 br wl net_2 gnd n W='1.2u' L=0.6u 
M_4 bl wl gnd gnd n W='1.2u' L=0.6u  
M_5 net_2 gnd gnd gnd n W='2.4u' L=0.6u 
M_6 gnd net_2 gnd gnd n W='2.4u' L=0.6u  
.ENDS	$ replica_cell_6t
