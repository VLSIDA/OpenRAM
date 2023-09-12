.subckt gf180mcu_3v3__nand2_1_dec A B Y VDD GND
X0 VDD B Y VDD pfet_03p3 w=1.7u l=0.3u
X1 Y A VDD VDD pfet_03p3 w=1.7u l=0.3u
X2 a_28_21# A Y GND nfet_03p3 w=0.85u l=0.3u
X3 VSS B a_28_21# GND nfet_03p3 w=0.85u l=0.3u
.ends