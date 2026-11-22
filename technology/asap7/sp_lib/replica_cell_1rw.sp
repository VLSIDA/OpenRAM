* ASAP7 (BSIM-CMG) library cell for OpenRAM. Device widths are fin-quantized: w = 27n * nfin.
.SUBCKT replica_cell_1rw bl br wl vdd gnd
MM0 vdd Q gnd gnd nmos_sram w=54n l=20n nfin=2
MM4 vdd Q vdd vdd pmos_sram w=27n l=20n nfin=1
MM1 Q vdd gnd gnd nmos_sram w=54n l=20n nfin=2
MM5 Q vdd vdd vdd pmos_sram w=27n l=20n nfin=1
MM3 bl wl Q gnd nmos_sram w=54n l=20n nfin=2
MM2 br wl vdd gnd nmos_sram w=54n l=20n nfin=2
.ENDS replica_cell_1rw
