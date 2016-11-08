*master-slave flip-flop with both output and inverted ouput

.SUBCKT ms_flop din dout dout_bar clk vdd gnd 
xmaster din mout mout_bar clk clk_bar vdd gnd dlatch
xslave mout_bar dout_bar dout clk_bar clk_nn vdd gnd dlatch
.ENDS flop

.SUBCKT dlatch din dout dout_bar clk clk_bar vdd gnd
*clk inverter
mPff1 clk_bar clk vdd vdd PMOS_VTG W=180.0n L=50n m=1
mNff1 clk_bar clk gnd gnd NMOS_VTG W=90n L=50n m=1

*transmission gate 1
mtmP1 din clk int1 vdd PMOS_VTG W=180.0n L=50n m=1
mtmN1 din clk_bar int1 gnd NMOS_VTG W=90n L=50n m=1

*foward inverter
mPff3 dout_bar int1 vdd vdd PMOS_VTG W=180.0n L=50n m=1
mNff3 dout_bar int1 gnd gnd NMOS_VTG W=90n L=50n m=1

*backward inverter
mPff4 dout dout_bar vdd vdd PMOS_VTG W=180.0n L=50n m=1
mNf4 dout dout_bar gnd gnd NMOS_VTG W=90n L=50n m=1

*transmission gate 2
mtmP2 int1 clk_bar dout vdd PMOS_VTG W=180.0n L=50n m=1
mtmN2 int1 clk dout gnd NMOS_VTG W=90n L=50n m=1
.ENDS dlatch

