.subckt gf180mcu_3v3__nand2_1_dec A B Z VDD GND
X0 VDD B Z VDD pfet_03v3 w=1.7u l=0.3u
X1 Z A VDD VDD pfet_03v3 w=1.7u l=0.3u
X2 a_28_21# A Z GND nfet_03v3 w=0.85u l=0.3u
X3 GND B a_28_21# GND nfet_03v3 w=0.85u l=0.3u
.ends
