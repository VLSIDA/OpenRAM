* NGSPICE file created from nand2_dec.ext - technology: EFS8A


* Top level circuit nand2_dec
.subckt nand2_dec A B Z vdd gnd

M1001 Z B vdd vdd pshort W=1.12u L=0.15u m=1
M1002 vdd A Z vdd pshort W=1.12u L=0.15u m=1
M1000 Z A a_n722_276# gnd nshort W=0.74u L=0.15u m=1
M1003 a_n722_276# B gnd gnd nshort W=0.74u L=0.15u m=1
.ends

