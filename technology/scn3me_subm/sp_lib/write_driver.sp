*********************** Write_Driver ******************************
.SUBCKT write_driver din bl br en vdd gnd

**** Inverter to conver Data_in to data_in_bar ******
* din_bar = inv(din)
M_1 din_bar din gnd gnd n W=1.2u L=0.6u
M_2 din_bar din vdd vdd p W=2.1u L=0.6u

**** 2input nand gate follwed by inverter to drive BL ******
* din_bar_gated = nand(en, din)
M_3 din_bar_gated en net_7 gnd n W=2.1u L=0.6u 
M_4 net_7 din gnd gnd n W=2.1u L=0.6u 
M_5 din_bar_gated en vdd vdd p W=2.1u L=0.6u 
M_6 din_bar_gated din vdd vdd p W=2.1u L=0.6u 
* din_bar_gated_bar = inv(din_bar_gated)
M_7 din_bar_gated_bar din_bar_gated vdd vdd p W=2.1u L=0.6u 
M_8 din_bar_gated_bar din_bar_gated gnd gnd n W=1.2u L=0.6u 

**** 2input nand gate follwed by inverter to drive BR******
* din_gated = nand(en, din_bar)
M_9 din_gated en vdd vdd p W=2.1u L=0.6u
M_10 din_gated en net_8 gnd n W=2.1u L=0.6u  
M_11 net_8 din_bar gnd gnd n W=2.1u L=0.6u
M_12 din_gated din_bar vdd vdd p W=2.1u L=0.6u 
* din_gated_bar = inv(din_gated)
M_13 din_gated_bar din_gated vdd vdd p W=2.1u L=0.6u 
M_14 din_gated_bar din_gated gnd gnd n W=1.2u L=0.6u

************************************************
* pull down with en enable
M_15 bl din_gated_bar net_5 gnd n W=3.6u L=0.6u 
M_16 br din_bar_gated_bar net_5 gnd n W=3.6u L=0.6u 
M_17 net_5 en gnd gnd n W=3.6u L=0.6u 



.ENDS	$ write_driver

