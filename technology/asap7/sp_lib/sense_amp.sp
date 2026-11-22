* ASAP7 (BSIM-CMG) library cell for OpenRAM. Device widths are fin-quantized: w = 27n * nfin.
* Latch-type sense amplifier (same topology as the FreePDK45 cell).
.SUBCKT sense_amp bl br dout en vdd gnd
M_1 dint net_1 vdd vdd pmos_rvt w=54n l=20n nfin=2
M_3 net_1 dint vdd vdd pmos_rvt w=54n l=20n nfin=2
M_2 dint net_1 net_2 gnd nmos_rvt w=54n l=20n nfin=2
M_8 net_1 dint net_2 gnd nmos_rvt w=54n l=20n nfin=2
M_5 bl en dint vdd pmos_rvt w=81n l=20n nfin=3
M_6 br en net_1 vdd pmos_rvt w=81n l=20n nfin=3
M_7 net_2 en gnd gnd nmos_rvt w=81n l=20n nfin=3
M_9 dout_bar dint vdd vdd pmos_rvt w=27n l=20n nfin=1
M_10 dout_bar dint gnd gnd nmos_rvt w=27n l=20n nfin=1
M_11 dout dout_bar vdd vdd pmos_rvt w=81n l=20n nfin=3
M_12 dout dout_bar gnd gnd nmos_rvt w=81n l=20n nfin=3
.ENDS sense_amp
