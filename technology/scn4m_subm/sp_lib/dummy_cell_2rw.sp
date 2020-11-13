
.SUBCKT dummy_cell_2rw bl0 br0 bl1 br1 wl0 wl1 vdd gnd
MM9 RA_to_R_right wl1 br1_noconn gnd n w=1.2u l=0.4u
MM8 RA_to_R_right Q gnd gnd n w=1.2u l=0.4u
MM7 RA_to_R_left Q_bar gnd gnd n w=1.2u l=0.4u
MM6 RA_to_R_left wl1 bl1_noconn gnd n w=1.2u l=0.4u
MM5 Q wl0 bl0_noconn gnd n w=0.8u l=0.4u
MM4 Q_bar wl0 br0_noconn gnd n w=0.8u l=0.4u
MM1 Q Q_bar gnd gnd n w=1.6u l=0.4u
MM0 Q_bar Q gnd gnd n w=1.6u l=0.4u
MM3 Q Q_bar vdd vdd p w=0.6u l=0.4u
MM2 Q_bar Q vdd vdd p w=0.6u l=0.4u
.ENDS

