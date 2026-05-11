* SPICE3 file created from sky130_custom_cell.ext - technology: sky130A

.subckt sky130_custom_cell BL BR WL VPWR VGND
X1 VGND Q Qbar VGND sky130_fd_pr__nfet_01v8 ad=0.09795 pd=0.915 as=0.0777 ps=0.79 w=0.42 l=0.15
X3 VPWR Q Qbar VPWR sky130_fd_pr__pfet_01v8 ad=0.0882 pd=0.84 as=0.1197 ps=1.41 w=0.42 l=0.15
X4 Q Qbar VPWR VPWR sky130_fd_pr__pfet_01v8 ad=0.1218 pd=1.42 as=0.0882 ps=0.84 w=0.42 l=0.15
X5 Q Qbar VGND VGND sky130_fd_pr__nfet_01v8 ad=0.0756 pd=0.78 as=0.09795 ps=0.915 w=0.42 l=0.15

X0 BL WL Q VGND sky130_fd_pr__nfet_01v8 ad=0.1428 pd=1.52 as=0.0756 ps=0.78 w=0.42 l=0.15
X2 Qbar WL BR VGND sky130_fd_pr__nfet_01v8 ad=0.0777 pd=0.79 as=0.1218 ps=1.42 w=0.42 l=0.15

.ends
