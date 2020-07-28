*********************** "write_driver" ******************************

.SUBCKT write_driver din bl br en vdd gnd

**** Inverter to conver Data_in to data_in_bar ******
* din_bar = inv(din)
M_1 din_bar din gnd gnd nshort W=0.36u L=0.15u m=1
M_2 din_bar din vdd vdd pshort W=0.55u L=0.15u m=1

**** 2input nand gate follwed by inverter to drive BL ******
* din_bar_gated = nand(en, din)
M_3 din_bar_gated en net_7 gnd nshort W=0.55u L=0.15u m=1
M_4 net_7 din gnd gnd nshort W=0.55u L=0.15u m=1
M_5 din_bar_gated en vdd vdd pshort W=0.55u L=0.15u m=1
M_6 din_bar_gated din vdd vdd pshort W=0.55u L=0.15u m=1
* din_bar_gated_bar = inv(din_bar_gated)
M_7 din_bar_gated_bar din_bar_gated vdd vdd pshort W=0.55u L=0.15u m=1
M_8 din_bar_gated_bar din_bar_gated gnd gnd nshort W=0.36u L=0.15u m=1

**** 2input nand gate follwed by inverter to drive BR******
* din_gated = nand(en, din_bar)
M_9 din_gated en vdd vdd pshort W=0.55u L=0.15u m=1
M_10 din_gated en net_8 gnd nshort W=0.55u L=0.15u m=1
M_11 net_8 din_bar gnd gnd nshort W=0.55u L=0.15u m=1
M_12 din_gated din_bar vdd vdd pshort W=0.55u L=0.15u m=1
* din_gated_bar = inv(din_gated)
M_13 din_gated_bar din_gated vdd vdd pshort W=0.55u L=0.15u m=1
M_14 din_gated_bar din_gated gnd gnd nshort W=0.36u L=0.15u m=1

************************************************
* pull down with en enable
M_15 bl din_gated_bar gnd gnd nshort W=1u L=0.15u m=1
M_16 br din_bar_gated_bar gnd gnd nshort W=1u L=0.15u m=1

.ENDS write_driver
