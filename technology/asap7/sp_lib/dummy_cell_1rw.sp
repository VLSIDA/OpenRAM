* ASAP7 (BSIM-CMG) library cell for OpenRAM. Device widths are fin-quantized: w = 27n * nfin.
.SUBCKT dummy_cell_1rw bl br wl vdd gnd
MM0 Q_bar Q gnd gnd nmos_sram w=54n l=20n nfin=2
MM4 Q_bar Q vdd vdd pmos_sram w=27n l=20n nfin=1
MM1 Q Q_bar gnd gnd nmos_sram w=54n l=20n nfin=2
MM5 Q Q_bar vdd vdd pmos_sram w=27n l=20n nfin=1
MM3 bl_noconn wl Q gnd nmos_sram w=54n l=20n nfin=2
MM2 br_noconn wl Q_bar gnd nmos_sram w=54n l=20n nfin=2
.ENDS dummy_cell_1rw
