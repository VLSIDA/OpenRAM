*********************** Write_Driver ******************************
.SUBCKT write_driver din bl br wen vdd gnd

**** Inverter to conver Data_in to data_in_bar ******
M_1 net_3 din gnd gnd n W='1.2*1u' L=0.6u
M_2 net_3 din vdd vdd p W='2.1*1u' L=0.6u

**** 2input nand gate follwed by inverter to drive BL ******
M_3 net_2 wen net_7 gnd n W='2.1*1u' L=0.6u 
M_4 net_7 din gnd gnd n W='2.1*1u' L=0.6u 
M_5 net_2 wen vdd vdd p W='2.1*1u' L=0.6u 
M_6 net_2 din vdd vdd p W='2.1*1u' L=0.6u 

 
M_7 net_1 net_2 vdd vdd p W='2.1*1u' L=0.6u 
M_8 net_1 net_2 gnd gnd n W='1.2*1u' L=0.6u 

**** 2input nand gate follwed by inverter to drive BR******
 
M_9 net_4 wen vdd vdd p W='2.1*1u' L=0.6u
M_10 net_4 wen net_8 gnd n W='2.1*1u' L=0.6u  
M_11 net_8 net_3 gnd gnd n W='2.1*1u' L=0.6u
M_12 net_4 net_3 vdd vdd p W='2.1*1u' L=0.6u 

M_13 net_6 net_4 vdd vdd p W='2.1*1u' L=0.6u 
M_14 net_6 net_4 gnd gnd n W='1.2*1u' L=0.6u

************************************************

M_15 bl net_6 net_5 gnd n W='3.6*1u' L=0.6u 
M_16 br net_1 net_5 gnd n W='3.6*1u' L=0.6u 
M_17 net_5 wen gnd gnd n W='3.6*1u' L=0.6u 



.ENDS	$ write_driver

