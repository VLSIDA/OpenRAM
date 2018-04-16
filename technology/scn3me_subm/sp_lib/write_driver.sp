*********************** Write_Driver ******************************
.SUBCKT write_driver din bl br en vdd gnd

*Inverters for enable and data input
M_1 bl_bar din vdd vdd p W='2.1*1u' L=0.6u
M_2 bl_bar din gnd gnd n W='1.2*1u' L=0.6u
M_3 en_bar en vdd vdd p W='2.1*1u' L=0.6u
M_4 en_bar en gnd gnd n W='1.2*1u' L=0.6u

*tristate for BL
M_5 int1 bl_bar vdd vdd p W='3.6*1u' L=0.6u
M_6 bl en_bar int1 vdd p W='3.6*1u' L=0.6u
M_7 bl en int2 gnd n W='1.8*1u' L = 0.6u
M_8 int2 bl_bar gnd gnd n W='1.8*1u' L=0.6u

*tristate for BR
M_9 int3 din vdd vdd p W='3.6*1u' L=0.6u
M_10 br en_bar int3 vdd p W='3.6*1u' L=0.6u
M_11 br en int4 gnd n W='1.8*1u' L=0.6u
M_12 int4 din gnd gnd n W='1.8*1u' L=0.6u


.ENDS	$ write_driver

