*********************** "sense_amp" ******************************

.SUBCKT sense_amp bl br dout en vdd gnd
M_1 dout net_1 vdd vdd p W='5.4*1u' L=0.6u 
M_2 dout net_1 net_2 gnd n W='2.7*1u' L=0.6u  
M_3 net_1 dout vdd vdd p W='5.4*1u' L=0.6u  
M_4 net_1 dout net_2 gnd n W='2.7*1u' L=0.6u  
M_5 bl en dout vdd p W='7.2*1u' L=0.6u  
M_6 br en net_1 vdd p W='7.2*1u' L=0.6u  
M_7 net_2 en gnd gnd n W='2.7*1u' L=0.6u  
.ENDS	 sense_amp

