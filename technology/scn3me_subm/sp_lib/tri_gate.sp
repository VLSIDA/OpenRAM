*********************** tri_gate ******************************

.SUBCKT tri_gate in out en en_bar vdd gnd

M_1 net_2 in_inv gnd gnd n W='1.2*1u' L=0.6u
M_2 net_3 in_inv vdd vdd p W='2.4*1u' L=0.6u
M_3 out en_bar net_3 vdd p W='2.4*1u' L=0.6u 
M_4 out en net_2 gnd n W='1.2*1u' L=0.6u 
M_5 in_inv in vdd vdd p W='2.4*1u' L=0.6u 
M_6 in_inv in gnd gnd n W='1.2*1u' L=0.6u


.ENDS	
