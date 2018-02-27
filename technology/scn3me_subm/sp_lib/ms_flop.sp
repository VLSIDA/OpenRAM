*master-slave flip-flop with both output and inverted ouput

.subckt dlatch din dout dout_bar clk clk_bar vdd gnd
*clk inverter
mPff1 clk_bar clk vdd vdd p W=1.8u L=0.6u m=1
mNff1 clk_bar clk gnd gnd n W=0.9u L=0.6u m=1

*transmission gate 1
mtmP1 din clk int1 vdd p W=1.8u L=0.6u m=1
mtmN1 din clk_bar int1 gnd n W=0.9u L=0.6u m=1

*foward inverter
mPff3 dout_bar int1 vdd vdd p W=1.8u L=0.6u m=1
mNff3 dout_bar int1 gnd gnd n W=0.9u L=0.6u m=1

*backward inverter
mPff4 dout dout_bar vdd vdd p W=1.8u L=0.6u m=1
mNf4 dout dout_bar gnd gnd n W=0.9u L=0.6u m=1

*transmission gate 2
mtmP2 int1 clk_bar dout vdd p W=1.8u L=0.6u m=1
mtmN2 int1 clk dout gnd n W=0.9u L=0.6u m=1
.ends dlatch

.subckt ms_flop din dout dout_bar clk vdd gnd 
xmaster din mout mout_bar clk clk_bar vdd gnd dlatch
xslave mout_bar dout_bar dout clk_bar clk_nn vdd gnd dlatch
.ends flop

