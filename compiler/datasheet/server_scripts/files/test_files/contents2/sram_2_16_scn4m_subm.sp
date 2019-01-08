**************************************************
* OpenRAM generated memory.
* Words: 16
* Data bits: 2
* Banks: 1
* Column mux: 1:1
**************************************************
*********************** "dff" ******************************
* Positive edge-triggered FF
.SUBCKT dff D Q clk vdd gnd

* SPICE3 file created from dff.ext - technology: scmos

M1000 vdd clk a_24_24# vdd p w=8u l=0.4u
M1001 a_84_296# D vdd vdd p w=4u l=0.4u
M1002 a_104_24# clk a_84_296# vdd p w=4u l=0.4u
M1003 a_140_296# a_24_24# a_104_24# vdd p w=4u l=0.4u
M1004 vdd a_152_16# a_140_296# vdd p w=4u l=0.4u
M1005 a_152_16# a_104_24# vdd vdd p w=4u l=0.4u
M1006 a_260_296# a_152_16# vdd vdd p w=4u l=0.4u
M1007 a_280_24# a_24_24# a_260_296# vdd p w=4u l=0.4u
M1008 a_320_336# clk a_280_24# vdd p w=2u l=0.4u
M1009 vdd Q a_320_336# vdd p w=2u l=0.4u
M1010 gnd clk a_24_24# gnd n w=4u l=0.4u
M1011 Q a_280_24# vdd vdd p w=8u l=0.4u
M1012 a_84_24# D gnd gnd n w=2u l=0.4u
M1013 a_104_24# a_24_24# a_84_24# gnd n w=2u l=0.4u
M1014 a_140_24# clk a_104_24# gnd n w=2u l=0.4u
M1015 gnd a_152_16# a_140_24# gnd n w=2u l=0.4u
M1016 a_152_16# a_104_24# gnd gnd n w=2u l=0.4u
M1017 a_260_24# a_152_16# gnd gnd n w=2u l=0.4u
M1018 a_280_24# clk a_260_24# gnd n w=2u l=0.4u
M1019 a_320_24# a_24_24# a_280_24# gnd n w=2u l=0.4u
M1020 gnd Q a_320_24# gnd n w=2u l=0.4u
M1021 Q a_280_24# gnd gnd n w=4u l=0.4u

.ENDS

.SUBCKT row_addr_dff din_0 din_1 din_2 din_3 dout_0 dout_1 dout_2 dout_3 clk vdd gnd
Xdff_r0_c0 din_0 dout_0 clk vdd gnd dff
Xdff_r1_c0 din_1 dout_1 clk vdd gnd dff
Xdff_r2_c0 din_2 dout_2 clk vdd gnd dff
Xdff_r3_c0 din_3 dout_3 clk vdd gnd dff
.ENDS row_addr_dff

.SUBCKT data_dff din_0 din_1 dout_0 dout_1 clk vdd gnd
Xdff_r0_c0 din_0 dout_0 clk vdd gnd dff
Xdff_r0_c1 din_1 dout_1 clk vdd gnd dff
.ENDS data_dff

* ptx M{0} {1} n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p

* ptx M{0} {1} p m=1 w=0.6000000000000001u l=0.4u pd=2.00u ps=2.00u as=0.60p ad=0.60p

* ptx M{0} {1} n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p

* ptx M{0} {1} n m=1 w=1.2000000000000002u l=0.4u pd=3.20u ps=3.20u as=1.20p ad=1.20p

.SUBCKT pbitcell_1RW_0W_0R bl0 br0 wl0 vdd gnd
Minverter_nmos_left Q Q_bar gnd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Minverter_nmos_right gnd Q Q_bar gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Minverter_pmos_left Q Q_bar vdd vdd p m=1 w=0.6000000000000001u l=0.4u pd=2.00u ps=2.00u as=0.60p ad=0.60p
Minverter_pmos_right vdd Q Q_bar vdd p m=1 w=0.6000000000000001u l=0.4u pd=2.00u ps=2.00u as=0.60p ad=0.60p
Mreadwrite_nmos_left0 bl0 wl0 Q gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
Mreadwrite_nmos_right0 Q_bar wl0 br0 gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
.ENDS pbitcell_1RW_0W_0R

.SUBCKT bitcell_array_16x2_1 bl0_0 br0_0 bl0_1 br0_1 wl0_0 wl0_1 wl0_2 wl0_3 wl0_4 wl0_5 wl0_6 wl0_7 wl0_8 wl0_9 wl0_10 wl0_11 wl0_12 wl0_13 wl0_14 wl0_15 vdd gnd
Xbit_r0_c0 bl0_0 br0_0 wl0_0 vdd gnd pbitcell_1RW_0W_0R
Xbit_r1_c0 bl0_0 br0_0 wl0_1 vdd gnd pbitcell_1RW_0W_0R
Xbit_r2_c0 bl0_0 br0_0 wl0_2 vdd gnd pbitcell_1RW_0W_0R
Xbit_r3_c0 bl0_0 br0_0 wl0_3 vdd gnd pbitcell_1RW_0W_0R
Xbit_r4_c0 bl0_0 br0_0 wl0_4 vdd gnd pbitcell_1RW_0W_0R
Xbit_r5_c0 bl0_0 br0_0 wl0_5 vdd gnd pbitcell_1RW_0W_0R
Xbit_r6_c0 bl0_0 br0_0 wl0_6 vdd gnd pbitcell_1RW_0W_0R
Xbit_r7_c0 bl0_0 br0_0 wl0_7 vdd gnd pbitcell_1RW_0W_0R
Xbit_r8_c0 bl0_0 br0_0 wl0_8 vdd gnd pbitcell_1RW_0W_0R
Xbit_r9_c0 bl0_0 br0_0 wl0_9 vdd gnd pbitcell_1RW_0W_0R
Xbit_r10_c0 bl0_0 br0_0 wl0_10 vdd gnd pbitcell_1RW_0W_0R
Xbit_r11_c0 bl0_0 br0_0 wl0_11 vdd gnd pbitcell_1RW_0W_0R
Xbit_r12_c0 bl0_0 br0_0 wl0_12 vdd gnd pbitcell_1RW_0W_0R
Xbit_r13_c0 bl0_0 br0_0 wl0_13 vdd gnd pbitcell_1RW_0W_0R
Xbit_r14_c0 bl0_0 br0_0 wl0_14 vdd gnd pbitcell_1RW_0W_0R
Xbit_r15_c0 bl0_0 br0_0 wl0_15 vdd gnd pbitcell_1RW_0W_0R
Xbit_r0_c1 bl0_1 br0_1 wl0_0 vdd gnd pbitcell_1RW_0W_0R
Xbit_r1_c1 bl0_1 br0_1 wl0_1 vdd gnd pbitcell_1RW_0W_0R
Xbit_r2_c1 bl0_1 br0_1 wl0_2 vdd gnd pbitcell_1RW_0W_0R
Xbit_r3_c1 bl0_1 br0_1 wl0_3 vdd gnd pbitcell_1RW_0W_0R
Xbit_r4_c1 bl0_1 br0_1 wl0_4 vdd gnd pbitcell_1RW_0W_0R
Xbit_r5_c1 bl0_1 br0_1 wl0_5 vdd gnd pbitcell_1RW_0W_0R
Xbit_r6_c1 bl0_1 br0_1 wl0_6 vdd gnd pbitcell_1RW_0W_0R
Xbit_r7_c1 bl0_1 br0_1 wl0_7 vdd gnd pbitcell_1RW_0W_0R
Xbit_r8_c1 bl0_1 br0_1 wl0_8 vdd gnd pbitcell_1RW_0W_0R
Xbit_r9_c1 bl0_1 br0_1 wl0_9 vdd gnd pbitcell_1RW_0W_0R
Xbit_r10_c1 bl0_1 br0_1 wl0_10 vdd gnd pbitcell_1RW_0W_0R
Xbit_r11_c1 bl0_1 br0_1 wl0_11 vdd gnd pbitcell_1RW_0W_0R
Xbit_r12_c1 bl0_1 br0_1 wl0_12 vdd gnd pbitcell_1RW_0W_0R
Xbit_r13_c1 bl0_1 br0_1 wl0_13 vdd gnd pbitcell_1RW_0W_0R
Xbit_r14_c1 bl0_1 br0_1 wl0_14 vdd gnd pbitcell_1RW_0W_0R
Xbit_r15_c1 bl0_1 br0_1 wl0_15 vdd gnd pbitcell_1RW_0W_0R
.ENDS bitcell_array_16x2_1

* ptx M{0} {1} p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p

.SUBCKT precharge_1 bl br en_bar vdd
Mlower_pmos bl en_bar br vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mupper_pmos1 bl en_bar vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mupper_pmos2 br en_bar vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
.ENDS precharge_1

.SUBCKT precharge_array_1 bl_0 br_0 bl_1 br_1 en_bar vdd
Xpre_column_0 bl_0 br_0 en_bar vdd precharge_1
Xpre_column_1 bl_1 br_1 en_bar vdd precharge_1
.ENDS precharge_array_1
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

.SUBCKT sense_amp_array data_0 bl_0 br_0 data_1 bl_1 br_1 en vdd gnd
Xsa_d0 bl_0 br_0 data_0 en vdd gnd sense_amp
Xsa_d1 bl_1 br_1 data_1 en vdd gnd sense_amp
.ENDS sense_amp_array
*********************** Write_Driver ******************************
.SUBCKT write_driver din bl br en vdd gnd

**** Inverter to conver Data_in to data_in_bar ******
* din_bar = inv(din)
M_1 din_bar din gnd gnd n W=0.8u L=0.4u
M_2 din_bar din vdd vdd p W=1.4u L=0.4u

**** 2input nand gate follwed by inverter to drive BL ******
* din_bar_gated = nand(en, din)
M_3 din_bar_gated en net_7 gnd n W=1.4u L=0.4u
M_4 net_7 din gnd gnd n W=1.4u L=0.4u
M_5 din_bar_gated en vdd vdd p W=1.4u L=0.4u
M_6 din_bar_gated din vdd vdd p W=1.4u L=0.4u
* din_bar_gated_bar = inv(din_bar_gated)
M_7 din_bar_gated_bar din_bar_gated vdd vdd p W=1.4u L=0.4u
M_8 din_bar_gated_bar din_bar_gated gnd gnd n W=0.8u L=0.4u

**** 2input nand gate follwed by inverter to drive BR******
* din_gated = nand(en, din_bar)
M_9 din_gated en vdd vdd p W=1.4u L=0.4u
M_10 din_gated en net_8 gnd n W=1.4u L=0.4u
M_11 net_8 din_bar gnd gnd n W=1.4u L=0.4u
M_12 din_gated din_bar vdd vdd p W=1.4u L=0.4u
* din_gated_bar = inv(din_gated)
M_13 din_gated_bar din_gated vdd vdd p W=1.4u L=0.4u
M_14 din_gated_bar din_gated gnd gnd n W=0.8u L=0.4u

************************************************
* pull down with en enable
M_15 bl din_gated_bar net_5 gnd n W=2.4u L=0.4u
M_16 br din_bar_gated_bar net_5 gnd n W=2.4u L=0.4u
M_17 net_5 en gnd gnd n W=2.4u L=0.4u



.ENDS   $ write_driver

.SUBCKT write_driver_array data_0 data_1 bl_0 br_0 bl_1 br_1 en vdd gnd
Xwrite_driver0 data_0 bl_0 br_0 en vdd gnd write_driver
Xwrite_driver1 data_1 bl_1 br_1 en vdd gnd write_driver
.ENDS write_driver_array

* ptx M{0} {1} n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p

* ptx M{0} {1} p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p

.SUBCKT pinv_1 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
.ENDS pinv_1

* ptx M{0} {1} n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p

.SUBCKT pnand2_1 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
.ENDS pnand2_1

.SUBCKT pnand3_1 A B C Z vdd gnd
Mpnand3_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand3_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand3_pmos3 Z C vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand3_nmos1 Z C net1 gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand3_nmos2 net1 B net2 gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand3_nmos3 net2 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
.ENDS pnand3_1

.SUBCKT pinv_2 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
.ENDS pinv_2

.SUBCKT pnand2_2 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
.ENDS pnand2_2

.SUBCKT pre2x4_1 in_0 in_1 out_0 out_1 out_2 out_3 vdd gnd
Xpre_inv_0 in_0 inbar_0 vdd gnd pinv_2
Xpre_inv_1 in_1 inbar_1 vdd gnd pinv_2
Xpre_nand_inv_0 Z_0 out_0 vdd gnd pinv_2
Xpre_nand_inv_1 Z_1 out_1 vdd gnd pinv_2
Xpre_nand_inv_2 Z_2 out_2 vdd gnd pinv_2
Xpre_nand_inv_3 Z_3 out_3 vdd gnd pinv_2
XXpre2x4_nand_0 inbar_0 inbar_1 Z_0 vdd gnd pnand2_2
XXpre2x4_nand_1 in_0 inbar_1 Z_1 vdd gnd pnand2_2
XXpre2x4_nand_2 inbar_0 in_1 Z_2 vdd gnd pnand2_2
XXpre2x4_nand_3 in_0 in_1 Z_3 vdd gnd pnand2_2
.ENDS pre2x4_1

.SUBCKT pinv_3 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
.ENDS pinv_3

.SUBCKT pnand3_2 A B C Z vdd gnd
Mpnand3_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand3_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand3_pmos3 Z C vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand3_nmos1 Z C net1 gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand3_nmos2 net1 B net2 gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand3_nmos3 net2 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
.ENDS pnand3_2

.SUBCKT pre3x8_2 in_0 in_1 in_2 out_0 out_1 out_2 out_3 out_4 out_5 out_6 out_7 vdd gnd
Xpre_inv_0 in_0 inbar_0 vdd gnd pinv_3
Xpre_inv_1 in_1 inbar_1 vdd gnd pinv_3
Xpre_inv_2 in_2 inbar_2 vdd gnd pinv_3
Xpre_nand_inv_0 Z_0 out_0 vdd gnd pinv_3
Xpre_nand_inv_1 Z_1 out_1 vdd gnd pinv_3
Xpre_nand_inv_2 Z_2 out_2 vdd gnd pinv_3
Xpre_nand_inv_3 Z_3 out_3 vdd gnd pinv_3
Xpre_nand_inv_4 Z_4 out_4 vdd gnd pinv_3
Xpre_nand_inv_5 Z_5 out_5 vdd gnd pinv_3
Xpre_nand_inv_6 Z_6 out_6 vdd gnd pinv_3
Xpre_nand_inv_7 Z_7 out_7 vdd gnd pinv_3
XXpre3x8_nand_0 inbar_0 inbar_1 inbar_2 Z_0 vdd gnd pnand3_2
XXpre3x8_nand_1 in_0 inbar_1 inbar_2 Z_1 vdd gnd pnand3_2
XXpre3x8_nand_2 inbar_0 in_1 inbar_2 Z_2 vdd gnd pnand3_2
XXpre3x8_nand_3 in_0 in_1 inbar_2 Z_3 vdd gnd pnand3_2
XXpre3x8_nand_4 inbar_0 inbar_1 in_2 Z_4 vdd gnd pnand3_2
XXpre3x8_nand_5 in_0 inbar_1 in_2 Z_5 vdd gnd pnand3_2
XXpre3x8_nand_6 inbar_0 in_1 in_2 Z_6 vdd gnd pnand3_2
XXpre3x8_nand_7 in_0 in_1 in_2 Z_7 vdd gnd pnand3_2
.ENDS pre3x8_2

.SUBCKT hierarchical_decoder_16rows_1 addr_0 addr_1 addr_2 addr_3 decode_0 decode_1 decode_2 decode_3 decode_4 decode_5 decode_6 decode_7 decode_8 decode_9 decode_10 decode_11 decode_12 decode_13 decode_14 decode_15 vdd gnd
Xpre_0 addr_0 addr_1 out_0 out_1 out_2 out_3 vdd gnd pre2x4_1
Xpre_1 addr_2 addr_3 out_4 out_5 out_6 out_7 vdd gnd pre2x4_1
XDEC_NAND_0 out_0 out_4 Z_0 vdd gnd pnand2_1
XDEC_NAND_4 out_0 out_5 Z_4 vdd gnd pnand2_1
XDEC_NAND_8 out_0 out_6 Z_8 vdd gnd pnand2_1
XDEC_NAND_12 out_0 out_7 Z_12 vdd gnd pnand2_1
XDEC_NAND_1 out_1 out_4 Z_1 vdd gnd pnand2_1
XDEC_NAND_5 out_1 out_5 Z_5 vdd gnd pnand2_1
XDEC_NAND_9 out_1 out_6 Z_9 vdd gnd pnand2_1
XDEC_NAND_13 out_1 out_7 Z_13 vdd gnd pnand2_1
XDEC_NAND_2 out_2 out_4 Z_2 vdd gnd pnand2_1
XDEC_NAND_6 out_2 out_5 Z_6 vdd gnd pnand2_1
XDEC_NAND_10 out_2 out_6 Z_10 vdd gnd pnand2_1
XDEC_NAND_14 out_2 out_7 Z_14 vdd gnd pnand2_1
XDEC_NAND_3 out_3 out_4 Z_3 vdd gnd pnand2_1
XDEC_NAND_7 out_3 out_5 Z_7 vdd gnd pnand2_1
XDEC_NAND_11 out_3 out_6 Z_11 vdd gnd pnand2_1
XDEC_NAND_15 out_3 out_7 Z_15 vdd gnd pnand2_1
XDEC_INV_0 Z_0 decode_0 vdd gnd pinv_1
XDEC_INV_1 Z_1 decode_1 vdd gnd pinv_1
XDEC_INV_2 Z_2 decode_2 vdd gnd pinv_1
XDEC_INV_3 Z_3 decode_3 vdd gnd pinv_1
XDEC_INV_4 Z_4 decode_4 vdd gnd pinv_1
XDEC_INV_5 Z_5 decode_5 vdd gnd pinv_1
XDEC_INV_6 Z_6 decode_6 vdd gnd pinv_1
XDEC_INV_7 Z_7 decode_7 vdd gnd pinv_1
XDEC_INV_8 Z_8 decode_8 vdd gnd pinv_1
XDEC_INV_9 Z_9 decode_9 vdd gnd pinv_1
XDEC_INV_10 Z_10 decode_10 vdd gnd pinv_1
XDEC_INV_11 Z_11 decode_11 vdd gnd pinv_1
XDEC_INV_12 Z_12 decode_12 vdd gnd pinv_1
XDEC_INV_13 Z_13 decode_13 vdd gnd pinv_1
XDEC_INV_14 Z_14 decode_14 vdd gnd pinv_1
XDEC_INV_15 Z_15 decode_15 vdd gnd pinv_1
.ENDS hierarchical_decoder_16rows_1

.SUBCKT pinv_4 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
.ENDS pinv_4

.SUBCKT pinv_5 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
.ENDS pinv_5

.SUBCKT pnand2_3 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
.ENDS pnand2_3

.SUBCKT wordline_driver in_0 in_1 in_2 in_3 in_4 in_5 in_6 in_7 in_8 in_9 in_10 in_11 in_12 in_13 in_14 in_15 wl_0 wl_1 wl_2 wl_3 wl_4 wl_5 wl_6 wl_7 wl_8 wl_9 wl_10 wl_11 wl_12 wl_13 wl_14 wl_15 en_bar vdd gnd
Xwl_driver_nand0 en_bar in_0 wl_bar_0 vdd gnd pnand2_3
Xwl_driver_inv0 wl_bar_0 wl_0 vdd gnd pinv_4
Xwl_driver_nand1 en_bar in_1 wl_bar_1 vdd gnd pnand2_3
Xwl_driver_inv1 wl_bar_1 wl_1 vdd gnd pinv_4
Xwl_driver_nand2 en_bar in_2 wl_bar_2 vdd gnd pnand2_3
Xwl_driver_inv2 wl_bar_2 wl_2 vdd gnd pinv_4
Xwl_driver_nand3 en_bar in_3 wl_bar_3 vdd gnd pnand2_3
Xwl_driver_inv3 wl_bar_3 wl_3 vdd gnd pinv_4
Xwl_driver_nand4 en_bar in_4 wl_bar_4 vdd gnd pnand2_3
Xwl_driver_inv4 wl_bar_4 wl_4 vdd gnd pinv_4
Xwl_driver_nand5 en_bar in_5 wl_bar_5 vdd gnd pnand2_3
Xwl_driver_inv5 wl_bar_5 wl_5 vdd gnd pinv_4
Xwl_driver_nand6 en_bar in_6 wl_bar_6 vdd gnd pnand2_3
Xwl_driver_inv6 wl_bar_6 wl_6 vdd gnd pinv_4
Xwl_driver_nand7 en_bar in_7 wl_bar_7 vdd gnd pnand2_3
Xwl_driver_inv7 wl_bar_7 wl_7 vdd gnd pinv_4
Xwl_driver_nand8 en_bar in_8 wl_bar_8 vdd gnd pnand2_3
Xwl_driver_inv8 wl_bar_8 wl_8 vdd gnd pinv_4
Xwl_driver_nand9 en_bar in_9 wl_bar_9 vdd gnd pnand2_3
Xwl_driver_inv9 wl_bar_9 wl_9 vdd gnd pinv_4
Xwl_driver_nand10 en_bar in_10 wl_bar_10 vdd gnd pnand2_3
Xwl_driver_inv10 wl_bar_10 wl_10 vdd gnd pinv_4
Xwl_driver_nand11 en_bar in_11 wl_bar_11 vdd gnd pnand2_3
Xwl_driver_inv11 wl_bar_11 wl_11 vdd gnd pinv_4
Xwl_driver_nand12 en_bar in_12 wl_bar_12 vdd gnd pnand2_3
Xwl_driver_inv12 wl_bar_12 wl_12 vdd gnd pinv_4
Xwl_driver_nand13 en_bar in_13 wl_bar_13 vdd gnd pnand2_3
Xwl_driver_inv13 wl_bar_13 wl_13 vdd gnd pinv_4
Xwl_driver_nand14 en_bar in_14 wl_bar_14 vdd gnd pnand2_3
Xwl_driver_inv14 wl_bar_14 wl_14 vdd gnd pinv_4
Xwl_driver_nand15 en_bar in_15 wl_bar_15 vdd gnd pnand2_3
Xwl_driver_inv15 wl_bar_15 wl_15 vdd gnd pinv_4
.ENDS wordline_driver

.SUBCKT pinv_6 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
.ENDS pinv_6

.SUBCKT bank dout0_0 dout0_1 din0_0 din0_1 addr0_0 addr0_1 addr0_2 addr0_3 s_en0 p_en_bar0 w_en0 wl_en0 vdd gnd
Xbitcell_array bl0_0 br0_0 bl0_1 br0_1 wl0_0 wl0_1 wl0_2 wl0_3 wl0_4 wl0_5 wl0_6 wl0_7 wl0_8 wl0_9 wl0_10 wl0_11 wl0_12 wl0_13 wl0_14 wl0_15 vdd gnd bitcell_array_16x2_1
Xprecharge_array0 bl0_0 br0_0 bl0_1 br0_1 p_en_bar0 vdd precharge_array_1
Xsense_amp_array0 dout0_0 bl0_0 br0_0 dout0_1 bl0_1 br0_1 s_en0 vdd gnd sense_amp_array
Xwrite_driver_array0 din0_0 din0_1 bl0_0 br0_0 bl0_1 br0_1 w_en0 vdd gnd write_driver_array
Xrow_decoder0 addr0_0 addr0_1 addr0_2 addr0_3 dec_out0_0 dec_out0_1 dec_out0_2 dec_out0_3 dec_out0_4 dec_out0_5 dec_out0_6 dec_out0_7 dec_out0_8 dec_out0_9 dec_out0_10 dec_out0_11 dec_out0_12 dec_out0_13 dec_out0_14 dec_out0_15 vdd gnd hierarchical_decoder_16rows_1
Xwordline_driver0 dec_out0_0 dec_out0_1 dec_out0_2 dec_out0_3 dec_out0_4 dec_out0_5 dec_out0_6 dec_out0_7 dec_out0_8 dec_out0_9 dec_out0_10 dec_out0_11 dec_out0_12 dec_out0_13 dec_out0_14 dec_out0_15 wl0_0 wl0_1 wl0_2 wl0_3 wl0_4 wl0_5 wl0_6 wl0_7 wl0_8 wl0_9 wl0_10 wl0_11 wl0_12 wl0_13 wl0_14 wl0_15 wl_en0 vdd gnd wordline_driver
.ENDS bank

* ptx M{0} {1} p m=1 w=3.2u l=0.4u pd=7.20u ps=7.20u as=3.20p ad=3.20p

.SUBCKT pinv_9 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=3.2u l=0.4u pd=7.20u ps=7.20u as=3.20p ad=3.20p
Mpinv_nmos Z A gnd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
.ENDS pinv_9

* ptx M{0} {1} n m=1 w=3.2u l=0.4u pd=7.20u ps=7.20u as=3.20p ad=3.20p

* ptx M{0} {1} p m=1 w=6.4u l=0.4u pd=13.60u ps=13.60u as=6.40p ad=6.40p

.SUBCKT pinv_10 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=6.4u l=0.4u pd=13.60u ps=13.60u as=6.40p ad=6.40p
Mpinv_nmos Z A gnd gnd n m=1 w=3.2u l=0.4u pd=7.20u ps=7.20u as=3.20p ad=3.20p
.ENDS pinv_10

.SUBCKT dff_buf_2 D Q Qb clk vdd gnd
Xdff_buf_dff D qint clk vdd gnd dff
Xdff_buf_inv1 qint Qb vdd gnd pinv_9
Xdff_buf_inv2 Qb Q vdd gnd pinv_10
.ENDS dff_buf_2

.SUBCKT dff_buf_array_2x1_1 din_0 din_1 dout_0 dout_bar_0 dout_1 dout_bar_1 clk vdd gnd
Xdff_r0_c0 din_0 dout_0 dout_bar_0 clk vdd gnd dff_buf_2
Xdff_r1_c0 din_1 dout_1 dout_bar_1 clk vdd gnd dff_buf_2
.ENDS dff_buf_array_2x1_1

.SUBCKT pnand2_4 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
.ENDS pnand2_4

.SUBCKT pinv_11 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=6.4u l=0.4u pd=13.60u ps=13.60u as=6.40p ad=6.40p
Mpinv_nmos Z A gnd gnd n m=1 w=3.2u l=0.4u pd=7.20u ps=7.20u as=3.20p ad=3.20p
.ENDS pinv_11

.SUBCKT pand2_4_1 A B Z vdd gnd
Xpand2_nand A B zb_int vdd gnd pnand2_4
Xpand2_inv zb_int Z vdd gnd pinv_11
.ENDS pand2_4_1

.SUBCKT pinv_12 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
.ENDS pinv_12

.SUBCKT pinv_13 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=6.4u l=0.4u pd=13.60u ps=13.60u as=6.40p ad=6.40p
Mpinv_nmos Z A gnd gnd n m=1 w=3.2u l=0.4u pd=7.20u ps=7.20u as=3.20p ad=3.20p
.ENDS pinv_13

.SUBCKT pbuf_4_1 A Z vdd gnd
Xbuf_inv1 A zb_int vdd gnd pinv_12
Xbuf_inv2 zb_int Z vdd gnd pinv_13
.ENDS pbuf_4_1

.SUBCKT pinv_14 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=6.4u l=0.4u pd=13.60u ps=13.60u as=6.40p ad=6.40p
Mpinv_nmos Z A gnd gnd n m=1 w=3.2u l=0.4u pd=7.20u ps=7.20u as=3.20p ad=3.20p
.ENDS pinv_14

* ptx M{0} {1} n m=1 w=12.8u l=0.4u pd=26.40u ps=26.40u as=12.80p ad=12.80p

* ptx M{0} {1} p m=1 w=25.6u l=0.4u pd=52.00u ps=52.00u as=25.60p ad=25.60p

.SUBCKT pinv_15 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=25.6u l=0.4u pd=52.00u ps=52.00u as=25.60p ad=25.60p
Mpinv_nmos Z A gnd gnd n m=1 w=12.8u l=0.4u pd=26.40u ps=26.40u as=12.80p ad=12.80p
.ENDS pinv_15

.SUBCKT pbuf_16_2 A Z vdd gnd
Xbuf_inv1 A zb_int vdd gnd pinv_14
Xbuf_inv2 zb_int Z vdd gnd pinv_15
.ENDS pbuf_16_2

.SUBCKT pinv_16 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=3.2u l=0.4u pd=7.20u ps=7.20u as=3.20p ad=3.20p
Mpinv_nmos Z A gnd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
.ENDS pinv_16

* ptx M{0} {1} n m=1 w=6.4u l=0.4u pd=13.60u ps=13.60u as=6.40p ad=6.40p

* ptx M{0} {1} p m=1 w=12.8u l=0.4u pd=26.40u ps=26.40u as=12.80p ad=12.80p

.SUBCKT pinv_17 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=12.8u l=0.4u pd=26.40u ps=26.40u as=12.80p ad=12.80p
Mpinv_nmos Z A gnd gnd n m=1 w=6.4u l=0.4u pd=13.60u ps=13.60u as=6.40p ad=6.40p
.ENDS pinv_17

.SUBCKT pbuf_8_3 A Z vdd gnd
Xbuf_inv1 A zb_int vdd gnd pinv_16
Xbuf_inv2 zb_int Z vdd gnd pinv_17
.ENDS pbuf_8_3

.SUBCKT pinv_18 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
.ENDS pinv_18

.SUBCKT pinv_19 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=12.8u l=0.4u pd=26.40u ps=26.40u as=12.80p ad=12.80p
Mpinv_nmos Z A gnd gnd n m=1 w=6.4u l=0.4u pd=13.60u ps=13.60u as=6.40p ad=6.40p
.ENDS pinv_19

.SUBCKT replica_pbitcell_1RW_0W_0R bl0 br0 wl0 vdd gnd
Minverter_nmos_left Q vdd gnd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Minverter_nmos_right gnd Q vdd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Minverter_pmos_left Q vdd vdd vdd p m=1 w=0.6000000000000001u l=0.4u pd=2.00u ps=2.00u as=0.60p ad=0.60p
Minverter_pmos_right vdd Q vdd vdd p m=1 w=0.6000000000000001u l=0.4u pd=2.00u ps=2.00u as=0.60p ad=0.60p
Mreadwrite_nmos_left0 bl0 wl0 Q gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
Mreadwrite_nmos_right0 vdd wl0 br0 gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
.ENDS replica_pbitcell_1RW_0W_0R

.SUBCKT replica_pbitcell bl0 br0 wl0 vdd gnd
Xpbitcell bl0 br0 wl0 vdd gnd replica_pbitcell_1RW_0W_0R
.ENDS replica_pbitcell

.SUBCKT bitcell_array_8x1_2 bl0_0 br0_0 wl0_0 wl0_1 wl0_2 wl0_3 wl0_4 wl0_5 wl0_6 wl0_7 vdd gnd
Xbit_r0_c0 bl0_0 br0_0 wl0_0 vdd gnd pbitcell_1RW_0W_0R
Xbit_r1_c0 bl0_0 br0_0 wl0_1 vdd gnd pbitcell_1RW_0W_0R
Xbit_r2_c0 bl0_0 br0_0 wl0_2 vdd gnd pbitcell_1RW_0W_0R
Xbit_r3_c0 bl0_0 br0_0 wl0_3 vdd gnd pbitcell_1RW_0W_0R
Xbit_r4_c0 bl0_0 br0_0 wl0_4 vdd gnd pbitcell_1RW_0W_0R
Xbit_r5_c0 bl0_0 br0_0 wl0_5 vdd gnd pbitcell_1RW_0W_0R
Xbit_r6_c0 bl0_0 br0_0 wl0_6 vdd gnd pbitcell_1RW_0W_0R
Xbit_r7_c0 bl0_0 br0_0 wl0_7 vdd gnd pbitcell_1RW_0W_0R
.ENDS bitcell_array_8x1_2

.SUBCKT pinv_20 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
.ENDS pinv_20

.SUBCKT delay_chain_1 in out vdd gnd
Xdinv0 in dout_1 vdd gnd pinv_20
Xdload_0_0 dout_1 n_0_0 vdd gnd pinv_20
Xdload_0_1 dout_1 n_0_1 vdd gnd pinv_20
Xdload_0_2 dout_1 n_0_2 vdd gnd pinv_20
Xdinv1 dout_1 dout_2 vdd gnd pinv_20
Xdload_1_0 dout_2 n_1_0 vdd gnd pinv_20
Xdload_1_1 dout_2 n_1_1 vdd gnd pinv_20
Xdload_1_2 dout_2 n_1_2 vdd gnd pinv_20
Xdinv2 dout_2 dout_3 vdd gnd pinv_20
Xdload_2_0 dout_3 n_2_0 vdd gnd pinv_20
Xdload_2_1 dout_3 n_2_1 vdd gnd pinv_20
Xdload_2_2 dout_3 n_2_2 vdd gnd pinv_20
Xdinv3 dout_3 out vdd gnd pinv_20
Xdload_3_0 out n_3_0 vdd gnd pinv_20
Xdload_3_1 out n_3_1 vdd gnd pinv_20
Xdload_3_2 out n_3_2 vdd gnd pinv_20
.ENDS delay_chain_1

.SUBCKT pinv_21 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
.ENDS pinv_21

* ptx M{0} {1} p m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p

.SUBCKT replica_bitline_rw en out vdd gnd
Xrbl_inv bl0_0 out vdd gnd pinv_21
Mrbl_access_tx vdd delayed_en bl0_0 vdd p m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
Xdelay_chain en delayed_en vdd gnd delay_chain_1
Xbitcell bl0_0 br0_0 delayed_en vdd gnd replica_pbitcell
Xload bl0_0 br0_0 gnd gnd gnd gnd gnd gnd gnd gnd vdd gnd bitcell_array_8x1_2
.ENDS replica_bitline_rw

.SUBCKT control_logic_rw csb web clk s_en w_en p_en_bar wl_en clk_buf vdd gnd
Xctrl_dffs csb web cs_bar cs we_bar we clk_buf vdd gnd dff_buf_array_2x1_1
Xclkbuf clk clk_buf vdd gnd pbuf_4_1
Xinv_clk_bar clk_buf clk_bar vdd gnd pinv_18
Xand2_gated_clk_bar cs clk_bar gated_clk_bar vdd gnd pand2_4_1
Xand2_gated_clk_buf clk_buf cs gated_clk_buf vdd gnd pand2_4_1
Xbuf_wl_en gated_clk_bar wl_en vdd gnd pbuf_16_2
Xbuf_w_en_buf we w_en vdd gnd pbuf_8_3
Xand2_rbl_in gated_clk_bar we_bar rbl_in vdd gnd pand2_4_1
Xand2_pre_p_en gated_clk_buf we_bar pre_p_en vdd gnd pand2_4_1
Xinv_p_en_bar pre_p_en p_en_bar vdd gnd pinv_19
Xbuf_s_en pre_s_en s_en vdd gnd pbuf_8_3
Xreplica_bitline rbl_in pre_s_en vdd gnd replica_bitline_rw
.ENDS control_logic_rw

.SUBCKT sram_2_16_scn4m_subm DIN0[0] DIN0[1] ADDR0[0] ADDR0[1] ADDR0[2] ADDR0[3] csb0 web0 clk0 DOUT0[0] DOUT0[1] vdd gnd
Xbank0 DOUT0[0] DOUT0[1] BANK_DIN0[0] BANK_DIN0[1] A0[0] A0[1] A0[2] A0[3] s_en0 p_en_bar0 w_en0 wl_en0 vdd gnd bank
Xcontrol0 csb0 web0 clk0 s_en0 w_en0 p_en_bar0 wl_en0 clk_buf0 vdd gnd control_logic_rw
Xrow_address0 ADDR0[0] ADDR0[1] ADDR0[2] ADDR0[3] A0[0] A0[1] A0[2] A0[3] clk_buf0 vdd gnd row_addr_dff
Xdata_dff0 DIN0[0] DIN0[1] BANK_DIN0[0] BANK_DIN0[1] clk_buf0 vdd gnd data_dff
.ENDS sram_2_16_scn4m_subm
