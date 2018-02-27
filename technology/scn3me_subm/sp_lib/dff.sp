* Positive edge-triggered FF
.subckt dff d q clk vdd gnd
M0 vdd clk a_2_6# vdd p w=12u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M1 a_17_74# d vdd vdd p w=6u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M2 a_22_6# clk a_17_74# vdd p w=6u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M3 a_31_74# a_2_6# a_22_6# vdd p w=6u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M4 vdd a_34_4# a_31_74# vdd p w=6u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M5 a_34_4# a_22_6# vdd vdd p w=6u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M6 a_61_74# a_34_4# vdd vdd p w=6u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M7 a_66_6# a_2_6# a_61_74# vdd p w=6u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M8 a_76_84# clk a_66_6# vdd p w=3u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M9 vdd q a_76_84# vdd p w=3u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M10 gnd clk a_2_6# gnd n w=6u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M11 q a_66_6# vdd vdd p w=12u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M12 a_17_6# d gnd gnd n w=3u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M13 a_22_6# a_2_6# a_17_6# gnd n w=3u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M14 a_31_6# clk a_22_6# gnd n w=3u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M15 gnd a_34_4# a_31_6# gnd n w=3u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M16 a_34_4# a_22_6# gnd gnd n w=3u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M17 a_61_6# a_34_4# gnd gnd n w=3u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M18 a_66_6# clk a_61_6# gnd n w=3u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M19 a_76_6# a_2_6# a_66_6# gnd n w=3u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M20 gnd q a_76_6# gnd n w=3u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
M21 q a_66_6# gnd gnd n w=6u l=0.6u
+ ad=0p pd=0u as=0p ps=0u 
.ends dff
