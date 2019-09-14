
*********************** "cell_6t" ******************************
.SUBCKT cell_6t bl br wl vdd gnd
M_1 Q Qb vdd vdd p W='0.9u' L=1.2u 
M_2 Qb Q vdd vdd p W='0.9u' L=1.2u 
M_3 br wl Qb gnd n W='1.2u' L=0.6u 
M_4 bl wl Q gnd n W='1.2u' L=0.6u  
M_5 Qb Q gnd gnd n W='2.4u' L=0.6u 
M_6 Q Qb gnd gnd n W='2.4u' L=0.6u  
.ENDS	$ cell_6t
