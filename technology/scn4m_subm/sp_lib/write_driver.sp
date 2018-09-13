*********************** Write_Driver ******************************
.SUBCKT write_driver din bl br en vdd gnd
* SPICE3 file created from write_driver.ext - technology: scmos

M1000 a_44_708# a_36_700# bl gnd n w=2.4u l=0.4u
M1001 br a_16_500# a_44_708# gnd n w=2.4u l=0.4u
M1002 a_44_708# en gnd gnd n w=2.4u l=0.4u
M1003 gnd a_8_284# a_16_500# gnd n w=0.8u l=0.4u
M1004 a_36_700# a_20_328# gnd gnd n w=0.8u l=0.4u
M1005 vdd a_8_284# a_16_500# vdd p w=1.4u l=0.4u
M1006 a_36_700# a_20_328# vdd vdd p w=1.4u l=0.4u
M1007 vdd en a_20_328# vdd p w=1.4u l=0.4u
M1008 a_20_328# a_64_360# vdd vdd p w=1.4u l=0.4u
M1009 a_48_328# en a_20_328# gnd n w=1.4u l=0.4u
M1010 gnd a_64_360# a_48_328# gnd n w=1.4u l=0.4u
M1011 a_40_228# en a_8_284# gnd n w=1.4u l=0.4u
M1012 gnd din a_40_228# gnd n w=1.4u l=0.4u
M1013 a_64_360# din gnd gnd n w=0.8u l=0.4u
M1014 a_8_284# en vdd vdd p w=1.4u l=0.4u
M1015 vdd din a_8_284# vdd p w=1.4u l=0.4u
M1016 a_64_360# din vdd vdd p w=1.4u l=0.4u

.ENDS
