* NGSPICE file created from 018SRAM_cell1_128x8m81.ext - technology: gf180mcuC

.subckt cell1rw VDD WL GND BL BR nwell pwell
X0 GND a_63_149# a_18_103# pwell nmos_6p0 w=0.95u l=0.6u
X1 a_18_103# WL BL pwell nmos_6p0 w=0.6u l=0.77u
X2 a_63_149# a_18_103# VDD nwell pmos_6p0 w=0.6u l=0.6u
X3 a_63_149# WL BR pwell nmos_6p0 w=0.6u l=0.77u
X4 VDD a_63_149# a_18_103# nwell pmos_6p0 w=0.6u l=0.6u
X5 a_63_149# a_18_103# GND pwell nmos_6p0 w=0.95u l=0.6u
.ends

