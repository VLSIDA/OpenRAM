* ASAP7 (BSIM-CMG) library cell for OpenRAM. Device widths are fin-quantized: w = 27n * nfin.
* 6T bitcell "122" as in ASAP7 sram_cell_6t_122: pull-up 1 fin, pass-gate 2, pull-down 2.
.SUBCKT cell_1rw bl br wl vdd gnd
MM0 Q_bar Q gnd gnd nmos_sram w=54n l=20n nfin=2
MM4 Q_bar Q vdd vdd pmos_sram w=27n l=20n nfin=1
MM1 Q Q_bar gnd gnd nmos_sram w=54n l=20n nfin=2
MM5 Q Q_bar vdd vdd pmos_sram w=27n l=20n nfin=1
MM3 bl wl Q gnd nmos_sram w=54n l=20n nfin=2
MM2 br wl Q_bar gnd nmos_sram w=54n l=20n nfin=2
.ENDS cell_1rw
