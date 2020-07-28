*********************** "sense_amp" ******************************

.SUBCKT sense_amp bl br dout en vdd gnd
M1000 gnd en a_56_432# gnd nshort W=0.65 L=0.15 m=1 mult=1
M1001 a_56_432# dint_bar dint gnd nshort W=0.65 L=0.15 m=1 mult=1
M1002 dint_bar dint a_56_432# gnd nshort W=0.65 L=0.15 m=1 mult=1

M1003 vdd dint_bar dint vdd pshort W=1.26 L=0.15 m=1 mult=1
M1004 dint_bar dint vdd vdd pshort W=1.26 L=0.15 m=1 mult=1

M1005 bl en dint vdd pshort W=2 L=0.15 m=1 mult=1
M1006 dint_bar en br vdd pshort W=2 L=0.15 m=1 mult=1

M1007 vdd dint_bar dout vdd pshort W=1.26 L=0.15 m=1 mult=1
M1008 dout dint_bar gnd gnd nshort W=0.65 L=0.15 m=1 mult=1

.ENDS sense_amp
