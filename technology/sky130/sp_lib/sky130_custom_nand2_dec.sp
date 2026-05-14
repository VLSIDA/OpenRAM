* NGSPICE file created from sky130_fd_bd_sram__openram_sp_custom_nand2_dec.ext - technology: sky130A

.subckt sky130_custom_nand2_dec A B Z VDD GND
X0 Z A VDD VDD sky130_fd_pr__pfet_01v8 w=1.12 l=0.15
X1 VDD B Z VDD sky130_fd_pr__pfet_01v8 w=1.12 l=0.15
X2 a_196_224# B GND GND sky130_fd_pr__nfet_01v8 w=0.74 l=0.15
X3 Z A a_196_224# GND sky130_fd_pr__nfet_01v8 w=0.74 l=0.15
.ends
