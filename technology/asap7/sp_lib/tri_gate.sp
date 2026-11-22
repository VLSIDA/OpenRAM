* ASAP7 (BSIM-CMG) library cell for OpenRAM. Device widths are fin-quantized: w = 27n * nfin.
.SUBCKT tri_gate in out en en_bar vdd gnd
M_1 net_2 in_inv gnd gnd nmos_rvt w=54n l=20n nfin=2
M_2 out en net_2 gnd nmos_rvt w=54n l=20n nfin=2
M_3 net_3 in_inv vdd vdd pmos_rvt w=54n l=20n nfin=2
M_4 out en_bar net_3 vdd pmos_rvt w=54n l=20n nfin=2
M_5 in_inv in vdd vdd pmos_rvt w=27n l=20n nfin=1
M_6 in_inv in gnd gnd nmos_rvt w=27n l=20n nfin=1
.ENDS
