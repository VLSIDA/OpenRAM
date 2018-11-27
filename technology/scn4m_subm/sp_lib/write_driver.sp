*********************** Write_Driver ******************************
.SUBCKT write_driver din bl br en vdd gnd

**** Inverter to conver Data_in to data_in_bar ******
M_1 din_bar din gnd gnd n W=0.8u L=0.4u
M_2 din_bar din vdd vdd p W=1.4u L=0.4u

**** 2input nand gate follwed by inverter to drive BL ******
M_3 din_bar_gated en net_7 gnd n W=1.4u L=0.4u
M_4 net_7 din gnd gnd n W=1.4u L=0.4u
M_5 din_bar_gated en vdd vdd p W=1.4u L=0.4u
M_6 din_bar_gated din vdd vdd p W=1.4u L=0.4u


M_7 net_1 din_bar_gated vdd vdd p W=1.4u L=0.4u
M_8 net_1 din_bar_gated gnd gnd n W=0.8u L=0.4u

**** 2input nand gate follwed by inverter to drive BR******

M_9 din_gated en vdd vdd p W=1.4u L=0.4u
M_10 din_gated en net_8 gnd n W=1.4u L=0.4u
M_11 net_8 din_bar gnd gnd n W=1.4u L=0.4u
M_12 din_gated din_bar vdd vdd p W=1.4u L=0.4u

M_13 net_6 din_gated vdd vdd p W=1.4u L=0.4u
M_14 net_6 din_gated gnd gnd n W=0.8u L=0.4u

************************************************

M_15 bl net_6 net_5 gnd n W=2.4u L=0.4u
M_16 br net_1 net_5 gnd n W=2.4u L=0.4u
M_17 net_5 en gnd gnd n W=2.4u L=0.4u



.ENDS   $ write_driver
