* ASAP7 (BSIM-CMG) library cell for OpenRAM: DFFHQx4_ASAP7_75t_R from asap7sc7p5t (BSD-3-Clause),
* ports renamed CLK->clk, VDD->vdd, VSS->gnd and reordered for OpenRAM.
.SUBCKT dff D Q clk vdd gnd
MM38 Q net049 gnd gnd nmos_rvt w=324.00n l=20n nfin=12
MM24 net049 SH gnd gnd nmos_rvt w=162.00n l=20n nfin=6
MM23 clkb clkn gnd gnd nmos_rvt w=54.0n l=20n nfin=2
MM20 clkn clk gnd gnd nmos_rvt w=54.0n l=20n nfin=2
MM17 SH clkn pd5 gnd nmos_rvt w=27.0n l=20n nfin=1
MM16 pd5 SS gnd gnd nmos_rvt w=27.0n l=20n nfin=1
MM14 SS SH gnd gnd nmos_rvt w=27.0n l=20n nfin=1
MM12 MS clkb SH gnd nmos_rvt w=27.0n l=20n nfin=1
MM9 MH clkb pd3 gnd nmos_rvt w=27.0n l=20n nfin=1
MM8 pd3 MS gnd gnd nmos_rvt w=27.0n l=20n nfin=1
MM6 MS MH gnd gnd nmos_rvt w=27.0n l=20n nfin=1
MM5 pd1 D gnd gnd nmos_rvt w=81.0n l=20n nfin=3
MM4 MH clkn pd1 gnd nmos_rvt w=81.0n l=20n nfin=3
MM25 net049 SH vdd vdd pmos_rvt w=162.00n l=20n nfin=6
MM22 clkb clkn vdd vdd pmos_rvt w=54.0n l=20n nfin=2
MM21 clkn clk vdd vdd pmos_rvt w=54.0n l=20n nfin=2
MM19 pd4 SS vdd vdd pmos_rvt w=27n l=20n nfin=1
MM18 SH clkb pd4 vdd pmos_rvt w=27n l=20n nfin=1
MM15 SS SH vdd vdd pmos_rvt w=27n l=20n nfin=1
MM13 MS clkn SH vdd pmos_rvt w=27.0n l=20n nfin=1
MM11 pd2 MS vdd vdd pmos_rvt w=27n l=20n nfin=1
MM10 MH clkn pd2 vdd pmos_rvt w=27n l=20n nfin=1
MM7 MS MH vdd vdd pmos_rvt w=27n l=20n nfin=1
MM1 MH clkb pu1 vdd pmos_rvt w=81.0n l=20n nfin=3
MM37 Q net049 vdd vdd pmos_rvt w=324.00n l=20n nfin=12
MM3 pu1 D vdd vdd pmos_rvt w=81.0n l=20n nfin=3
.ENDS
