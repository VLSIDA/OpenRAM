* NGSPICE file created from nand3_dec.ext - technology: EFS8A


* Top level circuit nand3_dec
.subckt nand3_dec A B C Z vdd gnd

M1001 Z A a_n346_328# gnd nshort W=0.74 L=0.15
M1002 a_n346_256# C gnd gnd nshort W=0.74 L=0.15
M1003 a_n346_328# B a_n346_256# gnd nshort W=0.74 L=0.15
M1000 Z B vdd vdd pshort W=1.12 L=0.15
M1004 Z A vdd vdd pshort W=1.12 L=0.15
M1005 Z C vdd vdd pshort W=1.12 L=0.15
.ends

