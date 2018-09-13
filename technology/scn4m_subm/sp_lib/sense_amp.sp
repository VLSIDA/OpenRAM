*********************** "sense_amp" ******************************

.SUBCKT sense_amp bl br dout en vdd gnd

* SPICE3 file created from sense_amp.ext - technology: scmos

M1000 gnd en a_56_432# gnd n w=1.8u l=0.4u
M1001 a_56_432# a_48_304# dout gnd n w=1.8u l=0.4u
M1002 a_48_304# dout a_56_432# gnd n w=1.8u l=0.4u
M1003 vdd a_48_304# dout vdd p w=3.6u l=0.4u
M1004 a_48_304# dout vdd vdd p w=3.6u l=0.4u
M1005 bl en dout vdd p w=4.8u l=0.4u
M1006 a_48_304# en br vdd p w=4.8u l=0.4u

.ENDS
