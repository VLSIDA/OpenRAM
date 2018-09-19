*********************** tri_gate ******************************

.SUBCKT tri_gate in out en en_bar vdd gnd

* SPICE3 file created from tri_gate.ext - technology: scmos

M1000 vdd in a_16_108# vdd p w=1.6u l=0.4u
M1001 a_76_212# a_16_108# vdd vdd p w=1.6u l=0.4u
M1002 out en_bar a_76_212# vdd p w=1.6u l=0.4u
M1003 gnd in a_16_108# gnd n w=0.8u l=0.4u
M1004 a_76_108# a_16_108# gnd gnd n w=0.8u l=0.4u
M1005 out en a_76_108# gnd n w=0.8u l=0.4u

.ENDS
