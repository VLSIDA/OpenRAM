* NGSPICE file created from nand4_dec.ext - technology: EFS8A

.subckt nand4_dec A B C D Z vdd gnd
M1000 Z A a_406_334# gnd nshort W=0.74 L=0.15
M1004 a_406_190# D gnd gnd nshort W=0.74 L=0.15
M1005 a_406_262# C a_406_190# gnd nshort W=0.74 L=0.15
M1007 a_406_334# B a_406_262# gnd nshort W=0.74 L=0.15
M1001 Z A vdd vdd pshort W=1.12 L=0.15
M1002 vdd C Z vdd pshort W=1.12 L=0.15
M1003 vdd D Z vdd pshort W=1.12 L=0.15
M1006 Z B vdd vdd pshort W=1.12 L=0.15
.ends

