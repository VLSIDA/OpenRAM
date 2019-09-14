
.SUBCKT cell_1rw_1r bl0 br0 bl1 br1 wl0 wl1 vdd gnd
MM9 RA_to_R_right wl1 br1 gnd n w=1.8u l=0.6u
MM8 RA_to_R_right Q gnd gnd n w=1.8u l=0.6u
MM7 RA_to_R_left Q_bar gnd gnd n w=1.8u l=0.6u
MM6 RA_to_R_left wl1 bl1 gnd n w=1.8u l=0.6u
MM5 Q wl0 bl0 gnd n w=1.2u l=0.6u
MM4 Q_bar wl0 br0 gnd n w=1.2u l=0.6u
MM1 Q Q_bar gnd gnd n w=2.4u l=0.6u
MM0 Q_bar Q gnd gnd n w=2.4u l=0.6u
MM3 Q Q_bar vdd vdd p w=1.2u l=0.6u
MM2 Q_bar Q vdd vdd p w=1.2u l=0.6u
.ENDS

