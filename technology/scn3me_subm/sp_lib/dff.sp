*********************** "dff" ******************************
* Positive edge-triggered FF
.SUBCKT dff D Q clk vdd gnd
M0 vdd clk a_2_6# vdd p w=12u l=0.6u
M1 a_17_74# D vdd vdd p w=6u l=0.6u
M2 a_22_6# clk a_17_74# vdd p w=6u l=0.6u
M3 a_31_74# a_2_6# a_22_6# vdd p w=6u l=0.6u
M4 vdd a_34_4# a_31_74# vdd p w=6u l=0.6u
M5 a_34_4# a_22_6# vdd vdd p w=6u l=0.6u
M6 a_61_74# a_34_4# vdd vdd p w=6u l=0.6u
M7 a_66_6# a_2_6# a_61_74# vdd p w=6u l=0.6u
M8 a_76_84# clk a_66_6# vdd p w=3u l=0.6u
M9 vdd Q a_76_84# vdd p w=3u l=0.6u
M10 gnd clk a_2_6# gnd n w=6u l=0.6u
M11 Q a_66_6# vdd vdd p w=12u l=0.6u
M12 a_17_6# D gnd gnd n w=3u l=0.6u
M13 a_22_6# a_2_6# a_17_6# gnd n w=3u l=0.6u
M14 a_31_6# clk a_22_6# gnd n w=3u l=0.6u
M15 gnd a_34_4# a_31_6# gnd n w=3u l=0.6u
M16 a_34_4# a_22_6# gnd gnd n w=3u l=0.6u
M17 a_61_6# a_34_4# gnd gnd n w=3u l=0.6u
M18 a_66_6# clk a_61_6# gnd n w=3u l=0.6u
M19 a_76_6# a_2_6# a_66_6# gnd n w=3u l=0.6u
M20 gnd Q a_76_6# gnd n w=3u l=0.6u
M21 Q a_66_6# gnd gnd n w=6u l=0.6u

.ENDS dff
