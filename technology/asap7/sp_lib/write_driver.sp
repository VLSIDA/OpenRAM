* ASAP7 (BSIM-CMG) library cell for OpenRAM. Device widths are fin-quantized: w = 27n * nfin.
* Write driver (same topology as the FreePDK45 cell).
.SUBCKT write_driver din bl br en vdd gnd
minP bl_bar din vdd vdd pmos_rvt w=54n l=20n nfin=2
minN bl_bar din gnd gnd nmos_rvt w=54n l=20n nfin=2
moutP en_bar en vdd vdd pmos_rvt w=54n l=20n nfin=2
moutN en_bar en gnd gnd nmos_rvt w=54n l=20n nfin=2
mout0P int1 bl_bar vdd vdd pmos_rvt w=81n l=20n nfin=3
mout0P2 bl en_bar int1 vdd pmos_rvt w=81n l=20n nfin=3
mout0N bl en int2 gnd nmos_rvt w=81n l=20n nfin=3
mout0N2 int2 bl_bar gnd gnd nmos_rvt w=81n l=20n nfin=3
mout1P int3 din vdd vdd pmos_rvt w=81n l=20n nfin=3
mout1P2 br en_bar int3 vdd pmos_rvt w=81n l=20n nfin=3
mout1N br en int4 gnd nmos_rvt w=81n l=20n nfin=3
mout1N2 int4 din gnd gnd nmos_rvt w=81n l=20n nfin=3
.ENDS write_driver
