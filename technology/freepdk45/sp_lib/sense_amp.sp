
.SUBCKT sense_amp bl br dout sclk vdd gnd
M_1 dout net_1 vdd vdd pmos_vtg w=540.0n l=50.0n
M_3 net_1 dout vdd vdd pmos_vtg w=540.0n l=50.0n
M_2 dout net_1 net_2 gnd nmos_vtg w=270.0n l=50.0n
M_8 net_1 dout net_2 gnd nmos_vtg w=270.0n l=50.0n
M_5 bl sclk dout vdd pmos_vtg w=720.0n l=50.0n
M_6 br sclk net_1 vdd pmos_vtg w=720.0n l=50.0n
M_7 net_2 sclk gnd gnd nmos_vtg w=270.0n l=50.0n
.ENDS sense_amp

