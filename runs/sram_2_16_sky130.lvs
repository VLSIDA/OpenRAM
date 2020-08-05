**************************************************
* OpenRAM generated memory.
* Words: 16
* Data bits: 2
* Banks: 1
* Column mux: 1:1
**************************************************
* SPICE3 file created from dff.ext - technology: EFS8A

.subckt dff D Q clk vdd gnd
M1000 a_511_725# a_n8_115# vdd vdd pshort W=3u L=0.15u m=1
M1001 a_353_115# clk a_11_624# gnd nshort W=1u L=0.15u m=1
M1002 a_353_725# a_203_89# a_11_624# vdd pshort W=3u L=0.15u m=1
M1003 a_11_624# a_203_89# a_161_115# gnd nshort W=1u L=0.15u m=1
M1004 a_11_624# clk a_161_725# vdd pshort W=3u L=0.15u m=1
M1005 gnd Q a_703_115# gnd nshort W=1u L=0.15u m=1
M1006 vdd Q a_703_725# vdd pshort W=3u L=0.15u m=1
M1007 a_203_89# clk gnd gnd nshort W=1u L=0.15u m=1
M1008 a_203_89# clk vdd vdd pshort W=3u L=0.15u m=1
M1009 a_161_115# D gnd gnd nshort W=1u L=0.15u m=1
M1010 a_161_725# D vdd vdd pshort W=3u L=0.15u m=1
M1011 gnd a_11_624# a_n8_115# gnd nshort W=1u L=0.15u m=1
M1012 a_703_115# a_203_89# ON gnd nshort W=1u L=0.15u m=1
M1013 vdd a_11_624# a_n8_115# vdd pshort W=3u L=0.15u m=1
M1014 a_703_725# clk ON vdd pshort W=3u L=0.15u m=1
M1015 Q ON vdd vdd pshort W=3u L=0.15u m=1
M1016 Q ON gnd gnd nshort W=1u L=0.15u m=1
M1017 ON a_203_89# a_511_725# vdd pshort W=3u L=0.15u m=1
M1018 ON clk a_511_115# gnd nshort W=1u L=0.15u m=1
M1019 gnd a_n8_115# a_353_115# gnd nshort W=1u L=0.15u m=1
M1020 vdd a_n8_115# a_353_725# vdd pshort W=3u L=0.15u m=1
M1021 a_511_115# a_n8_115# gnd gnd nshort W=1u L=0.15u m=1
.ends

.SUBCKT row_addr_dff din_0 din_1 din_2 din_3 dout_0 dout_1 dout_2 dout_3 clk vdd gnd
* INPUT : din_0 
* INPUT : din_1 
* INPUT : din_2 
* INPUT : din_3 
* OUTPUT: dout_0 
* OUTPUT: dout_1 
* OUTPUT: dout_2 
* OUTPUT: dout_3 
* INPUT : clk 
* POWER : vdd 
* GROUND: gnd 
* rows: 4 cols: 1
Xdff_r0_c0 din_0 dout_0 clk vdd gnd dff
Xdff_r1_c0 din_1 dout_1 clk vdd gnd dff
Xdff_r2_c0 din_2 dout_2 clk vdd gnd dff
Xdff_r3_c0 din_3 dout_3 clk vdd gnd dff
.ENDS row_addr_dff

.SUBCKT data_dff din_0 din_1 dout_0 dout_1 clk vdd gnd
* INPUT : din_0 
* INPUT : din_1 
* OUTPUT: dout_0 
* OUTPUT: dout_1 
* INPUT : clk 
* POWER : vdd 
* GROUND: gnd 
* rows: 1 cols: 2
Xdff_r0_c0 din_0 dout_0 clk vdd gnd dff
Xdff_r0_c1 din_1 dout_1 clk vdd gnd dff
.ENDS data_dff

* ptx M{0} {1} pshort m=1 w=0.55u l=0.15u pd=1.40u ps=1.40u as=0.21p ad=0.21p

.SUBCKT precharge_0 bl br en_bar vdd
* OUTPUT: bl 
* OUTPUT: br 
* INPUT : en_bar 
* POWER : vdd 
Mlower_pmos bl en_bar br vdd pshort m=1 w=0.55u l=0.15u 
Mupper_pmos1 bl en_bar vdd vdd pshort m=1 w=0.55u l=0.15u 
Mupper_pmos2 br en_bar vdd vdd pshort m=1 w=0.55u l=0.15u 
.ENDS precharge_0

.SUBCKT precharge_array bl_0 br_0 bl_1 br_1 bl_2 br_2 en_bar vdd
* OUTPUT: bl_0 
* OUTPUT: br_0 
* OUTPUT: bl_1 
* OUTPUT: br_1 
* OUTPUT: bl_2 
* OUTPUT: br_2 
* INPUT : en_bar 
* POWER : vdd 
* cols: 3 size: 1 bl: bl0 br: br0
Xpre_column_0 bl_0 br_0 en_bar vdd precharge_0
Xpre_column_1 bl_1 br_1 en_bar vdd precharge_0
Xpre_column_2 bl_2 br_2 en_bar vdd precharge_0
.ENDS precharge_array
*********************** "sense_amp" ******************************

.SUBCKT sense_amp bl br dout en vdd gnd
M1000 gnd en a_56_432# gnd nshort W=0.65u L=0.15u m=1
M1001 a_56_432# dint_bar dint gnd nshort W=0.65u L=0.15u m=1
M1002 dint_bar dint a_56_432# gnd nshort W=0.65u L=0.15u m=1

M1003 vdd dint_bar dint vdd pshort W=1.26u L=0.15u m=1
M1004 dint_bar dint vdd vdd pshort W=1.26u L=0.15u m=1

M1005 bl en dint vdd pshort W=2u L=0.15u m=1
M1006 dint_bar en br vdd pshort W=2u L=0.15u m=1

M1007 vdd dint_bar dout vdd pshort W=1.26u L=0.15u m=1
M1008 dout dint_bar gnd gnd nshort W=0.65u L=0.15u m=1

.ENDS sense_amp

.SUBCKT sense_amp_array data_0 bl_0 br_0 data_1 bl_1 br_1 en vdd gnd
* OUTPUT: data_0 
* INPUT : bl_0 
* INPUT : br_0 
* OUTPUT: data_1 
* INPUT : bl_1 
* INPUT : br_1 
* INPUT : en 
* POWER : vdd 
* GROUND: gnd 
* words_per_row: 1
Xsa_d0 bl_0 br_0 data_0 en vdd gnd sense_amp
Xsa_d1 bl_1 br_1 data_1 en vdd gnd sense_amp
.ENDS sense_amp_array
*********************** "write_driver" ******************************

.SUBCKT write_driver din bl br en vdd gnd

**** Inverter to conver Data_in to data_in_bar ******
* din_bar = inv(din)
M_1 din_bar din gnd gnd nshort W=0.36u L=0.15u m=1
M_2 din_bar din vdd vdd pshort W=0.55u L=0.15u m=1

**** 2input nand gate follwed by inverter to drive BL ******
* din_bar_gated = nand(en, din)
M_3 din_bar_gated en net_7 gnd nshort W=0.55u L=0.15u m=1
M_4 net_7 din gnd gnd nshort W=0.55u L=0.15u m=1
M_5 din_bar_gated en vdd vdd pshort W=0.55u L=0.15u m=1
M_6 din_bar_gated din vdd vdd pshort W=0.55u L=0.15u m=1
* din_bar_gated_bar = inv(din_bar_gated)
M_7 din_bar_gated_bar din_bar_gated vdd vdd pshort W=0.55u L=0.15u m=1
M_8 din_bar_gated_bar din_bar_gated gnd gnd nshort W=0.36u L=0.15u m=1

**** 2input nand gate follwed by inverter to drive BR******
* din_gated = nand(en, din_bar)
M_9 din_gated en vdd vdd pshort W=0.55u L=0.15u m=1
M_10 din_gated en net_8 gnd nshort W=0.55u L=0.15u m=1
M_11 net_8 din_bar gnd gnd nshort W=0.55u L=0.15u m=1
M_12 din_gated din_bar vdd vdd pshort W=0.55u L=0.15u m=1
* din_gated_bar = inv(din_gated)
M_13 din_gated_bar din_gated vdd vdd pshort W=0.55u L=0.15u m=1
M_14 din_gated_bar din_gated gnd gnd nshort W=0.36u L=0.15u m=1

************************************************
* pull down with en enable
M_15 bl din_gated_bar gnd gnd nshort W=1u L=0.15u m=1
M_16 br din_bar_gated_bar gnd gnd nshort W=1u L=0.15u m=1

.ENDS write_driver

.SUBCKT write_driver_array data_0 data_1 bl_0 br_0 bl_1 br_1 en vdd gnd
* INPUT : data_0 
* INPUT : data_1 
* OUTPUT: bl_0 
* OUTPUT: br_0 
* OUTPUT: bl_1 
* OUTPUT: br_1 
* INPUT : en 
* POWER : vdd 
* GROUND: gnd 
* word_size 2
Xwrite_driver0 data_0 bl_0 br_0 en vdd gnd write_driver
Xwrite_driver1 data_1 bl_1 br_1 en vdd gnd write_driver
.ENDS write_driver_array

.SUBCKT port_data rbl_bl rbl_br bl0_0 br0_0 bl0_1 br0_1 dout_0 dout_1 din_0 din_1 s_en p_en_bar w_en vdd gnd
* INOUT : rbl_bl 
* INOUT : rbl_br 
* INOUT : bl0_0 
* INOUT : br0_0 
* INOUT : bl0_1 
* INOUT : br0_1 
* OUTPUT: dout_0 
* OUTPUT: dout_1 
* INPUT : din_0 
* INPUT : din_1 
* INPUT : s_en 
* INPUT : p_en_bar 
* INPUT : w_en 
* POWER : vdd 
* GROUND: gnd 
Xprecharge_array0 rbl_bl rbl_br bl0_0 br0_0 bl0_1 br0_1 p_en_bar vdd precharge_array
Xsense_amp_array0 dout_0 bl0_0 br0_0 dout_1 bl0_1 br0_1 s_en vdd gnd sense_amp_array
Xwrite_driver_array0 din_0 din_1 bl0_0 br0_0 bl0_1 br0_1 w_en vdd gnd write_driver_array
.ENDS port_data

.SUBCKT precharge_1 bl br en_bar vdd
* OUTPUT: bl 
* OUTPUT: br 
* INPUT : en_bar 
* POWER : vdd 
Mlower_pmos bl en_bar br vdd pshort m=1 w=0.55u l=0.15u 
Mupper_pmos1 bl en_bar vdd vdd pshort m=1 w=0.55u l=0.15u 
Mupper_pmos2 br en_bar vdd vdd pshort m=1 w=0.55u l=0.15u 
.ENDS precharge_1

.SUBCKT precharge_array_0 bl_0 br_0 bl_1 br_1 bl_2 br_2 en_bar vdd
* OUTPUT: bl_0 
* OUTPUT: br_0 
* OUTPUT: bl_1 
* OUTPUT: br_1 
* OUTPUT: bl_2 
* OUTPUT: br_2 
* INPUT : en_bar 
* POWER : vdd 
* cols: 3 size: 1 bl: bl1 br: br1
Xpre_column_0 bl_0 br_0 en_bar vdd precharge_1
Xpre_column_1 bl_1 br_1 en_bar vdd precharge_1
Xpre_column_2 bl_2 br_2 en_bar vdd precharge_1
.ENDS precharge_array_0

.SUBCKT port_data_0 rbl_bl rbl_br bl1_0 br1_0 bl1_1 br1_1 dout_0 dout_1 s_en p_en_bar vdd gnd
* INOUT : rbl_bl 
* INOUT : rbl_br 
* INOUT : bl1_0 
* INOUT : br1_0 
* INOUT : bl1_1 
* INOUT : br1_1 
* OUTPUT: dout_0 
* OUTPUT: dout_1 
* INPUT : s_en 
* INPUT : p_en_bar 
* POWER : vdd 
* GROUND: gnd 
Xprecharge_array1 bl1_0 br1_0 bl1_1 br1_1 rbl_bl rbl_br p_en_bar vdd precharge_array_0
Xsense_amp_array1 dout_0 bl1_0 br1_0 dout_1 bl1_1 br1_1 s_en vdd gnd sense_amp_array
.ENDS port_data_0
* NGSPICE file created from nand2_dec.ext - technology: EFS8A


* Top level circuit nand2_dec
.subckt nand2_dec A B Z vdd gnd

M1001 Z B vdd vdd pshort W=1.12u L=0.15u m=1
M1002 vdd A Z vdd pshort W=1.12u L=0.15u m=1
M1000 Z A a_n722_276# gnd nshort W=0.74u L=0.15u m=1
M1003 a_n722_276# B gnd gnd nshort W=0.74u L=0.15u m=1
.ends


* ptx M{0} {1} nshort m=1 w=0.36u l=0.15u pd=1.02u ps=1.02u as=0.14p ad=0.14p

* ptx M{0} {1} pshort m=1 w=1.12u l=0.15u pd=2.54u ps=2.54u as=0.42p ad=0.42p

.SUBCKT pinv_dec A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd pshort m=1 w=1.12u l=0.15u 
Mpinv_nmos Z A gnd gnd nshort m=1 w=0.36u l=0.15u 
.ENDS pinv_dec

.SUBCKT and2_dec A B Z vdd gnd
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 1
Xpand2_dec_nand A B zb_int vdd gnd nand2_dec
Xpand2_dec_inv zb_int Z vdd gnd pinv_dec
.ENDS and2_dec
* NGSPICE file created from nand3_dec.ext - technology: EFS8A


* Top level circuit nand3_dec
.subckt nand3_dec A B C Z vdd gnd

M1001 Z A a_n346_328# gnd nshort W=0.74u L=0.15u m=1
M1002 a_n346_256# C gnd gnd nshort W=0.74u L=0.15u m=1
M1003 a_n346_328# B a_n346_256# gnd nshort W=0.74u L=0.15u m=1
M1000 Z B vdd vdd pshort W=1.12u L=0.15u m=1
M1004 Z A vdd vdd pshort W=1.12u L=0.15u m=1
M1005 Z C vdd vdd pshort W=1.12u L=0.15u m=1
.ends


.SUBCKT and3_dec A B C Z vdd gnd
* INPUT : A 
* INPUT : B 
* INPUT : C 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 1
Xpand3_dec_nand A B C zb_int vdd gnd nand3_dec
Xpand3_dec_inv zb_int Z vdd gnd pinv_dec
.ENDS and3_dec

.SUBCKT hierarchical_predecode2x4 in_0 in_1 out_0 out_1 out_2 out_3 vdd gnd
* INPUT : in_0 
* INPUT : in_1 
* OUTPUT: out_0 
* OUTPUT: out_1 
* OUTPUT: out_2 
* OUTPUT: out_3 
* POWER : vdd 
* GROUND: gnd 
Xpre_inv_0 in_0 inbar_0 vdd gnd pinv_dec
Xpre_inv_1 in_1 inbar_1 vdd gnd pinv_dec
XXpre2x4_and_0 inbar_0 inbar_1 out_0 vdd gnd and2_dec
XXpre2x4_and_1 in_0 inbar_1 out_1 vdd gnd and2_dec
XXpre2x4_and_2 inbar_0 in_1 out_2 vdd gnd and2_dec
XXpre2x4_and_3 in_0 in_1 out_3 vdd gnd and2_dec
.ENDS hierarchical_predecode2x4

.SUBCKT hierarchical_predecode3x8 in_0 in_1 in_2 out_0 out_1 out_2 out_3 out_4 out_5 out_6 out_7 vdd gnd
* INPUT : in_0 
* INPUT : in_1 
* INPUT : in_2 
* OUTPUT: out_0 
* OUTPUT: out_1 
* OUTPUT: out_2 
* OUTPUT: out_3 
* OUTPUT: out_4 
* OUTPUT: out_5 
* OUTPUT: out_6 
* OUTPUT: out_7 
* POWER : vdd 
* GROUND: gnd 
Xpre_inv_0 in_0 inbar_0 vdd gnd pinv_dec
Xpre_inv_1 in_1 inbar_1 vdd gnd pinv_dec
Xpre_inv_2 in_2 inbar_2 vdd gnd pinv_dec
XXpre3x8_and_0 inbar_0 inbar_1 inbar_2 out_0 vdd gnd and3_dec
XXpre3x8_and_1 in_0 inbar_1 inbar_2 out_1 vdd gnd and3_dec
XXpre3x8_and_2 inbar_0 in_1 inbar_2 out_2 vdd gnd and3_dec
XXpre3x8_and_3 in_0 in_1 inbar_2 out_3 vdd gnd and3_dec
XXpre3x8_and_4 inbar_0 inbar_1 in_2 out_4 vdd gnd and3_dec
XXpre3x8_and_5 in_0 inbar_1 in_2 out_5 vdd gnd and3_dec
XXpre3x8_and_6 inbar_0 in_1 in_2 out_6 vdd gnd and3_dec
XXpre3x8_and_7 in_0 in_1 in_2 out_7 vdd gnd and3_dec
.ENDS hierarchical_predecode3x8

.SUBCKT hierarchical_decoder addr_0 addr_1 addr_2 addr_3 decode_0 decode_1 decode_2 decode_3 decode_4 decode_5 decode_6 decode_7 decode_8 decode_9 decode_10 decode_11 decode_12 decode_13 decode_14 decode_15 vdd gnd
* INPUT : addr_0 
* INPUT : addr_1 
* INPUT : addr_2 
* INPUT : addr_3 
* OUTPUT: decode_0 
* OUTPUT: decode_1 
* OUTPUT: decode_2 
* OUTPUT: decode_3 
* OUTPUT: decode_4 
* OUTPUT: decode_5 
* OUTPUT: decode_6 
* OUTPUT: decode_7 
* OUTPUT: decode_8 
* OUTPUT: decode_9 
* OUTPUT: decode_10 
* OUTPUT: decode_11 
* OUTPUT: decode_12 
* OUTPUT: decode_13 
* OUTPUT: decode_14 
* OUTPUT: decode_15 
* POWER : vdd 
* GROUND: gnd 
Xpre_0 addr_0 addr_1 out_0 out_1 out_2 out_3 vdd gnd hierarchical_predecode2x4
Xpre_1 addr_2 addr_3 out_4 out_5 out_6 out_7 vdd gnd hierarchical_predecode2x4
XDEC_AND_0 out_0 out_4 decode_0 vdd gnd and2_dec
XDEC_AND_4 out_0 out_5 decode_4 vdd gnd and2_dec
XDEC_AND_8 out_0 out_6 decode_8 vdd gnd and2_dec
XDEC_AND_12 out_0 out_7 decode_12 vdd gnd and2_dec
XDEC_AND_1 out_1 out_4 decode_1 vdd gnd and2_dec
XDEC_AND_5 out_1 out_5 decode_5 vdd gnd and2_dec
XDEC_AND_9 out_1 out_6 decode_9 vdd gnd and2_dec
XDEC_AND_13 out_1 out_7 decode_13 vdd gnd and2_dec
XDEC_AND_2 out_2 out_4 decode_2 vdd gnd and2_dec
XDEC_AND_6 out_2 out_5 decode_6 vdd gnd and2_dec
XDEC_AND_10 out_2 out_6 decode_10 vdd gnd and2_dec
XDEC_AND_14 out_2 out_7 decode_14 vdd gnd and2_dec
XDEC_AND_3 out_3 out_4 decode_3 vdd gnd and2_dec
XDEC_AND_7 out_3 out_5 decode_7 vdd gnd and2_dec
XDEC_AND_11 out_3 out_6 decode_11 vdd gnd and2_dec
XDEC_AND_15 out_3 out_7 decode_15 vdd gnd and2_dec
.ENDS hierarchical_decoder

* ptx M{0} {1} nshort m=1 w=0.74u l=0.15u pd=1.78u ps=1.78u as=0.28p ad=0.28p

* ptx M{0} {1} pshort m=1 w=3.0u l=0.15u pd=6.30u ps=6.30u as=1.12p ad=1.12p

.SUBCKT pinv_dec_0 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd pshort m=1 w=3.0u l=0.15u 
Mpinv_nmos Z A gnd gnd nshort m=1 w=0.74u l=0.15u 
.ENDS pinv_dec_0

.SUBCKT wordline_driver A B Z vdd gnd
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Xwld_nand A B zb_int vdd gnd nand2_dec
Xwl_driver zb_int Z vdd gnd pinv_dec_0
.ENDS wordline_driver

.SUBCKT wordline_driver_array in_0 in_1 in_2 in_3 in_4 in_5 in_6 in_7 in_8 in_9 in_10 in_11 in_12 in_13 in_14 in_15 wl_0 wl_1 wl_2 wl_3 wl_4 wl_5 wl_6 wl_7 wl_8 wl_9 wl_10 wl_11 wl_12 wl_13 wl_14 wl_15 en vdd gnd
* INPUT : in_0 
* INPUT : in_1 
* INPUT : in_2 
* INPUT : in_3 
* INPUT : in_4 
* INPUT : in_5 
* INPUT : in_6 
* INPUT : in_7 
* INPUT : in_8 
* INPUT : in_9 
* INPUT : in_10 
* INPUT : in_11 
* INPUT : in_12 
* INPUT : in_13 
* INPUT : in_14 
* INPUT : in_15 
* OUTPUT: wl_0 
* OUTPUT: wl_1 
* OUTPUT: wl_2 
* OUTPUT: wl_3 
* OUTPUT: wl_4 
* OUTPUT: wl_5 
* OUTPUT: wl_6 
* OUTPUT: wl_7 
* OUTPUT: wl_8 
* OUTPUT: wl_9 
* OUTPUT: wl_10 
* OUTPUT: wl_11 
* OUTPUT: wl_12 
* OUTPUT: wl_13 
* OUTPUT: wl_14 
* OUTPUT: wl_15 
* INPUT : en 
* POWER : vdd 
* GROUND: gnd 
* rows: 16 cols: 2
Xwl_driver_and0 in_0 en wl_0 vdd gnd wordline_driver
Xwl_driver_and1 in_1 en wl_1 vdd gnd wordline_driver
Xwl_driver_and2 in_2 en wl_2 vdd gnd wordline_driver
Xwl_driver_and3 in_3 en wl_3 vdd gnd wordline_driver
Xwl_driver_and4 in_4 en wl_4 vdd gnd wordline_driver
Xwl_driver_and5 in_5 en wl_5 vdd gnd wordline_driver
Xwl_driver_and6 in_6 en wl_6 vdd gnd wordline_driver
Xwl_driver_and7 in_7 en wl_7 vdd gnd wordline_driver
Xwl_driver_and8 in_8 en wl_8 vdd gnd wordline_driver
Xwl_driver_and9 in_9 en wl_9 vdd gnd wordline_driver
Xwl_driver_and10 in_10 en wl_10 vdd gnd wordline_driver
Xwl_driver_and11 in_11 en wl_11 vdd gnd wordline_driver
Xwl_driver_and12 in_12 en wl_12 vdd gnd wordline_driver
Xwl_driver_and13 in_13 en wl_13 vdd gnd wordline_driver
Xwl_driver_and14 in_14 en wl_14 vdd gnd wordline_driver
Xwl_driver_and15 in_15 en wl_15 vdd gnd wordline_driver
.ENDS wordline_driver_array

.SUBCKT port_address addr_0 addr_1 addr_2 addr_3 wl_en wl_0 wl_1 wl_2 wl_3 wl_4 wl_5 wl_6 wl_7 wl_8 wl_9 wl_10 wl_11 wl_12 wl_13 wl_14 wl_15 vdd gnd
* INPUT : addr_0 
* INPUT : addr_1 
* INPUT : addr_2 
* INPUT : addr_3 
* INPUT : wl_en 
* OUTPUT: wl_0 
* OUTPUT: wl_1 
* OUTPUT: wl_2 
* OUTPUT: wl_3 
* OUTPUT: wl_4 
* OUTPUT: wl_5 
* OUTPUT: wl_6 
* OUTPUT: wl_7 
* OUTPUT: wl_8 
* OUTPUT: wl_9 
* OUTPUT: wl_10 
* OUTPUT: wl_11 
* OUTPUT: wl_12 
* OUTPUT: wl_13 
* OUTPUT: wl_14 
* OUTPUT: wl_15 
* POWER : vdd 
* GROUND: gnd 
Xrow_decoder addr_0 addr_1 addr_2 addr_3 dec_out_0 dec_out_1 dec_out_2 dec_out_3 dec_out_4 dec_out_5 dec_out_6 dec_out_7 dec_out_8 dec_out_9 dec_out_10 dec_out_11 dec_out_12 dec_out_13 dec_out_14 dec_out_15 vdd gnd hierarchical_decoder
Xwordline_driver dec_out_0 dec_out_1 dec_out_2 dec_out_3 dec_out_4 dec_out_5 dec_out_6 dec_out_7 dec_out_8 dec_out_9 dec_out_10 dec_out_11 dec_out_12 dec_out_13 dec_out_14 dec_out_15 wl_0 wl_1 wl_2 wl_3 wl_4 wl_5 wl_6 wl_7 wl_8 wl_9 wl_10 wl_11 wl_12 wl_13 wl_14 wl_15 wl_en vdd gnd wordline_driver_array
.ENDS port_address

.SUBCKT cell_1rw_1r bl0 br0 bl1 br1 wl0 wl1 vdd gnd
** N=11 EP=8 IP=0 FDC=16
*.SEEDPROM

* Bitcell Core
M0 Q wl1 bl1 gnd npd W=0.21u L=0.15u m=1
M1 gnd Q_bar Q gnd npd W=0.21u L=0.15u m=1
M2 gnd Q_bar Q gnd npd W=0.21u L=0.15u m=1
M3 bl0 wl0 Q gnd npd W=0.21u L=0.15u m=1
M4 Q_bar wl1 br1 gnd npd W=0.21u L=0.15u m=1
M5 gnd Q Q_bar gnd npd W=0.21u L=0.15u m=1
M6 gnd Q Q_bar gnd npd W=0.21u L=0.15u m=1
M7 br0 wl0 Q_bar gnd npd W=0.21u L=0.15u m=1
M8 vdd Q Q_bar vdd ppu W=0.14u L=0.15u m=1
M9 Q Q_bar vdd vdd ppu W=0.14u L=0.15u m=1

* drainOnly PMOS
M10 Q_bar wl1 Q_bar vdd ppu W=0.14u L=0.08u m=1
M11 Q wl0 Q vdd ppu W=0.14u L=0.08u m=1

* drainOnly NMOS
M12 bl1 gnd bl1 gnd npd W=0.21u L=0.08u m=1
M14 br1 gnd br1 gnd npd W=0.21u L=0.08u m=1

.ENDS

.SUBCKT bitcell_array bl0_0 br0_0 bl1_0 br1_0 bl0_1 br0_1 bl1_1 br1_1 wl0_0 wl1_0 wl0_1 wl1_1 wl0_2 wl1_2 wl0_3 wl1_3 wl0_4 wl1_4 wl0_5 wl1_5 wl0_6 wl1_6 wl0_7 wl1_7 wl0_8 wl1_8 wl0_9 wl1_9 wl0_10 wl1_10 wl0_11 wl1_11 wl0_12 wl1_12 wl0_13 wl1_13 wl0_14 wl1_14 wl0_15 wl1_15 vdd gnd
* INOUT : bl0_0 
* INOUT : br0_0 
* INOUT : bl1_0 
* INOUT : br1_0 
* INOUT : bl0_1 
* INOUT : br0_1 
* INOUT : bl1_1 
* INOUT : br1_1 
* INPUT : wl0_0 
* INPUT : wl1_0 
* INPUT : wl0_1 
* INPUT : wl1_1 
* INPUT : wl0_2 
* INPUT : wl1_2 
* INPUT : wl0_3 
* INPUT : wl1_3 
* INPUT : wl0_4 
* INPUT : wl1_4 
* INPUT : wl0_5 
* INPUT : wl1_5 
* INPUT : wl0_6 
* INPUT : wl1_6 
* INPUT : wl0_7 
* INPUT : wl1_7 
* INPUT : wl0_8 
* INPUT : wl1_8 
* INPUT : wl0_9 
* INPUT : wl1_9 
* INPUT : wl0_10 
* INPUT : wl1_10 
* INPUT : wl0_11 
* INPUT : wl1_11 
* INPUT : wl0_12 
* INPUT : wl1_12 
* INPUT : wl0_13 
* INPUT : wl1_13 
* INPUT : wl0_14 
* INPUT : wl1_14 
* INPUT : wl0_15 
* INPUT : wl1_15 
* POWER : vdd 
* GROUND: gnd 
* rows: 16 cols: 2
Xbit_r0_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_0 wl1_0 vdd gnd cell_1rw_1r
Xbit_r1_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_1 wl1_1 vdd gnd cell_1rw_1r
Xbit_r2_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_2 wl1_2 vdd gnd cell_1rw_1r
Xbit_r3_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_3 wl1_3 vdd gnd cell_1rw_1r
Xbit_r4_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_4 wl1_4 vdd gnd cell_1rw_1r
Xbit_r5_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_5 wl1_5 vdd gnd cell_1rw_1r
Xbit_r6_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_6 wl1_6 vdd gnd cell_1rw_1r
Xbit_r7_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_7 wl1_7 vdd gnd cell_1rw_1r
Xbit_r8_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_8 wl1_8 vdd gnd cell_1rw_1r
Xbit_r9_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_9 wl1_9 vdd gnd cell_1rw_1r
Xbit_r10_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_10 wl1_10 vdd gnd cell_1rw_1r
Xbit_r11_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_11 wl1_11 vdd gnd cell_1rw_1r
Xbit_r12_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_12 wl1_12 vdd gnd cell_1rw_1r
Xbit_r13_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_13 wl1_13 vdd gnd cell_1rw_1r
Xbit_r14_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_14 wl1_14 vdd gnd cell_1rw_1r
Xbit_r15_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_15 wl1_15 vdd gnd cell_1rw_1r
Xbit_r0_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_0 wl1_0 vdd gnd cell_1rw_1r
Xbit_r1_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_1 wl1_1 vdd gnd cell_1rw_1r
Xbit_r2_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_2 wl1_2 vdd gnd cell_1rw_1r
Xbit_r3_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_3 wl1_3 vdd gnd cell_1rw_1r
Xbit_r4_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_4 wl1_4 vdd gnd cell_1rw_1r
Xbit_r5_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_5 wl1_5 vdd gnd cell_1rw_1r
Xbit_r6_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_6 wl1_6 vdd gnd cell_1rw_1r
Xbit_r7_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_7 wl1_7 vdd gnd cell_1rw_1r
Xbit_r8_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_8 wl1_8 vdd gnd cell_1rw_1r
Xbit_r9_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_9 wl1_9 vdd gnd cell_1rw_1r
Xbit_r10_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_10 wl1_10 vdd gnd cell_1rw_1r
Xbit_r11_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_11 wl1_11 vdd gnd cell_1rw_1r
Xbit_r12_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_12 wl1_12 vdd gnd cell_1rw_1r
Xbit_r13_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_13 wl1_13 vdd gnd cell_1rw_1r
Xbit_r14_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_14 wl1_14 vdd gnd cell_1rw_1r
Xbit_r15_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_15 wl1_15 vdd gnd cell_1rw_1r
.ENDS bitcell_array
* Ingore first line
.SUBCKT replica_cell_1rw_1r bl0 br0 bl1 br1 wl0 wl1 vdd gnd
** N=9 EP=8 IP=0 FDC=16
*.SEEDPROM

* Bitcell Core
M0 Q wl1 bl1 gnd npd W=0.21u L=0.15u m=1
M1 gnd vdd Q gnd npd W=0.21u L=0.15u m=1
M2 gnd vdd Q gnd npd W=0.21u L=0.15u m=1
M3 bl0 wl0 Q gnd npd W=0.21u L=0.15u m=1
M4 vdd wl1 br1 gnd npd W=0.21u L=0.15u m=1
M5 gnd Q vdd gnd npd W=0.21u L=0.15u m=1
M6 gnd Q vdd gnd npd W=0.21u L=0.15u m=1
M7 br0 wl0 vdd gnd npd W=0.21u L=0.15u m=1
M8 vdd Q vdd vdd ppu W=0.14u L=0.15u m=1
M9 Q vdd vdd vdd ppu W=0.14u L=0.15u m=1

* drainOnly PMOS
* M10 vdd wl1 vdd vdd ppuu L=0.08 W=0.14
* M11 Q wl0 Q vdd ppuu L=0.08 W=0.14

* drainOnly NMOS
M12 bl1 gnd bl1 gnd npd W=0.21u L=0.08u m=1
M14 br1 gnd br1 gnd npd W=0.21u L=0.08u m=1

.ENDS

.SUBCKT dummy_cell_1rw_1r bl0 br0 bl1 br1 wl0 wl1 vdd gnd
** N=14 EP=6 IP=0 FDC=16
*.SEEDPROM

* Bitcell Core
M1 1 gnd gnd gnd npd W=0.21u L=0.15u m=1
M2 1 wl1 bl1 gnd npd W=0.21u L=0.15u m=1
M3 2 gnd gnd gnd npd W=0.21u L=0.15u m=1
M4 2 wl1 br1 gnd npd W=0.21u L=0.15u m=1
M5 3 gnd gnd gnd npd W=0.21u L=0.15u m=1
M6 3 wl0 bl0 gnd npd W=0.21u L=0.15u m=1
M7 4 gnd gnd gnd npd W=0.21u L=0.15u m=1
M8 4 wl0 br0 gnd npd W=0.21u L=0.15u m=1

* drainOnly NMOS
M9 bl1 gnd bl1 gnd npd W=0.21u L=0.08u m=1
M10 br1 gnd br1 gnd npd W=0.21u L=0.08u m=1

.ENDS

.SUBCKT replica_column bl0_0 br0_0 bl1_0 br1_0 wl0_0 wl1_0 wl0_1 wl1_1 wl0_2 wl1_2 wl0_3 wl1_3 wl0_4 wl1_4 wl0_5 wl1_5 wl0_6 wl1_6 wl0_7 wl1_7 wl0_8 wl1_8 wl0_9 wl1_9 wl0_10 wl1_10 wl0_11 wl1_11 wl0_12 wl1_12 wl0_13 wl1_13 wl0_14 wl1_14 wl0_15 wl1_15 wl0_16 wl1_16 wl0_17 wl1_17 wl0_18 wl1_18 wl0_19 wl1_19 vdd gnd
* OUTPUT: bl0_0 
* OUTPUT: br0_0 
* OUTPUT: bl1_0 
* OUTPUT: br1_0 
* INPUT : wl0_0 
* INPUT : wl1_0 
* INPUT : wl0_1 
* INPUT : wl1_1 
* INPUT : wl0_2 
* INPUT : wl1_2 
* INPUT : wl0_3 
* INPUT : wl1_3 
* INPUT : wl0_4 
* INPUT : wl1_4 
* INPUT : wl0_5 
* INPUT : wl1_5 
* INPUT : wl0_6 
* INPUT : wl1_6 
* INPUT : wl0_7 
* INPUT : wl1_7 
* INPUT : wl0_8 
* INPUT : wl1_8 
* INPUT : wl0_9 
* INPUT : wl1_9 
* INPUT : wl0_10 
* INPUT : wl1_10 
* INPUT : wl0_11 
* INPUT : wl1_11 
* INPUT : wl0_12 
* INPUT : wl1_12 
* INPUT : wl0_13 
* INPUT : wl1_13 
* INPUT : wl0_14 
* INPUT : wl1_14 
* INPUT : wl0_15 
* INPUT : wl1_15 
* INPUT : wl0_16 
* INPUT : wl1_16 
* INPUT : wl0_17 
* INPUT : wl1_17 
* INPUT : wl0_18 
* INPUT : wl1_18 
* INPUT : wl0_19 
* INPUT : wl1_19 
* POWER : vdd 
* GROUND: gnd 
Xrbc_1 bl0_0 br0_0 bl1_0 br1_0 wl0_1 wl1_1 vdd gnd replica_cell_1rw_1r
Xrbc_2 bl0_0 br0_0 bl1_0 br1_0 wl0_2 wl1_2 vdd gnd replica_cell_1rw_1r
Xrbc_3 bl0_0 br0_0 bl1_0 br1_0 wl0_3 wl1_3 vdd gnd replica_cell_1rw_1r
Xrbc_4 bl0_0 br0_0 bl1_0 br1_0 wl0_4 wl1_4 vdd gnd replica_cell_1rw_1r
Xrbc_5 bl0_0 br0_0 bl1_0 br1_0 wl0_5 wl1_5 vdd gnd replica_cell_1rw_1r
Xrbc_6 bl0_0 br0_0 bl1_0 br1_0 wl0_6 wl1_6 vdd gnd replica_cell_1rw_1r
Xrbc_7 bl0_0 br0_0 bl1_0 br1_0 wl0_7 wl1_7 vdd gnd replica_cell_1rw_1r
Xrbc_8 bl0_0 br0_0 bl1_0 br1_0 wl0_8 wl1_8 vdd gnd replica_cell_1rw_1r
Xrbc_9 bl0_0 br0_0 bl1_0 br1_0 wl0_9 wl1_9 vdd gnd replica_cell_1rw_1r
Xrbc_10 bl0_0 br0_0 bl1_0 br1_0 wl0_10 wl1_10 vdd gnd replica_cell_1rw_1r
Xrbc_11 bl0_0 br0_0 bl1_0 br1_0 wl0_11 wl1_11 vdd gnd replica_cell_1rw_1r
Xrbc_12 bl0_0 br0_0 bl1_0 br1_0 wl0_12 wl1_12 vdd gnd replica_cell_1rw_1r
Xrbc_13 bl0_0 br0_0 bl1_0 br1_0 wl0_13 wl1_13 vdd gnd replica_cell_1rw_1r
Xrbc_14 bl0_0 br0_0 bl1_0 br1_0 wl0_14 wl1_14 vdd gnd replica_cell_1rw_1r
Xrbc_15 bl0_0 br0_0 bl1_0 br1_0 wl0_15 wl1_15 vdd gnd replica_cell_1rw_1r
Xrbc_16 bl0_0 br0_0 bl1_0 br1_0 wl0_16 wl1_16 vdd gnd replica_cell_1rw_1r
Xrbc_17 bl0_0 br0_0 bl1_0 br1_0 wl0_17 wl1_17 vdd gnd replica_cell_1rw_1r
Xrbc_18 bl0_0 br0_0 bl1_0 br1_0 wl0_18 wl1_18 vdd gnd dummy_cell_1rw_1r
.ENDS replica_column

.SUBCKT replica_column_0 bl0_0 br0_0 bl1_0 br1_0 wl0_0 wl1_0 wl0_1 wl1_1 wl0_2 wl1_2 wl0_3 wl1_3 wl0_4 wl1_4 wl0_5 wl1_5 wl0_6 wl1_6 wl0_7 wl1_7 wl0_8 wl1_8 wl0_9 wl1_9 wl0_10 wl1_10 wl0_11 wl1_11 wl0_12 wl1_12 wl0_13 wl1_13 wl0_14 wl1_14 wl0_15 wl1_15 wl0_16 wl1_16 wl0_17 wl1_17 wl0_18 wl1_18 wl0_19 wl1_19 vdd gnd
* OUTPUT: bl0_0 
* OUTPUT: br0_0 
* OUTPUT: bl1_0 
* OUTPUT: br1_0 
* INPUT : wl0_0 
* INPUT : wl1_0 
* INPUT : wl0_1 
* INPUT : wl1_1 
* INPUT : wl0_2 
* INPUT : wl1_2 
* INPUT : wl0_3 
* INPUT : wl1_3 
* INPUT : wl0_4 
* INPUT : wl1_4 
* INPUT : wl0_5 
* INPUT : wl1_5 
* INPUT : wl0_6 
* INPUT : wl1_6 
* INPUT : wl0_7 
* INPUT : wl1_7 
* INPUT : wl0_8 
* INPUT : wl1_8 
* INPUT : wl0_9 
* INPUT : wl1_9 
* INPUT : wl0_10 
* INPUT : wl1_10 
* INPUT : wl0_11 
* INPUT : wl1_11 
* INPUT : wl0_12 
* INPUT : wl1_12 
* INPUT : wl0_13 
* INPUT : wl1_13 
* INPUT : wl0_14 
* INPUT : wl1_14 
* INPUT : wl0_15 
* INPUT : wl1_15 
* INPUT : wl0_16 
* INPUT : wl1_16 
* INPUT : wl0_17 
* INPUT : wl1_17 
* INPUT : wl0_18 
* INPUT : wl1_18 
* INPUT : wl0_19 
* INPUT : wl1_19 
* POWER : vdd 
* GROUND: gnd 
Xrbc_1 bl0_0 br0_0 bl1_0 br1_0 wl0_1 wl1_1 vdd gnd dummy_cell_1rw_1r
Xrbc_2 bl0_0 br0_0 bl1_0 br1_0 wl0_2 wl1_2 vdd gnd replica_cell_1rw_1r
Xrbc_3 bl0_0 br0_0 bl1_0 br1_0 wl0_3 wl1_3 vdd gnd replica_cell_1rw_1r
Xrbc_4 bl0_0 br0_0 bl1_0 br1_0 wl0_4 wl1_4 vdd gnd replica_cell_1rw_1r
Xrbc_5 bl0_0 br0_0 bl1_0 br1_0 wl0_5 wl1_5 vdd gnd replica_cell_1rw_1r
Xrbc_6 bl0_0 br0_0 bl1_0 br1_0 wl0_6 wl1_6 vdd gnd replica_cell_1rw_1r
Xrbc_7 bl0_0 br0_0 bl1_0 br1_0 wl0_7 wl1_7 vdd gnd replica_cell_1rw_1r
Xrbc_8 bl0_0 br0_0 bl1_0 br1_0 wl0_8 wl1_8 vdd gnd replica_cell_1rw_1r
Xrbc_9 bl0_0 br0_0 bl1_0 br1_0 wl0_9 wl1_9 vdd gnd replica_cell_1rw_1r
Xrbc_10 bl0_0 br0_0 bl1_0 br1_0 wl0_10 wl1_10 vdd gnd replica_cell_1rw_1r
Xrbc_11 bl0_0 br0_0 bl1_0 br1_0 wl0_11 wl1_11 vdd gnd replica_cell_1rw_1r
Xrbc_12 bl0_0 br0_0 bl1_0 br1_0 wl0_12 wl1_12 vdd gnd replica_cell_1rw_1r
Xrbc_13 bl0_0 br0_0 bl1_0 br1_0 wl0_13 wl1_13 vdd gnd replica_cell_1rw_1r
Xrbc_14 bl0_0 br0_0 bl1_0 br1_0 wl0_14 wl1_14 vdd gnd replica_cell_1rw_1r
Xrbc_15 bl0_0 br0_0 bl1_0 br1_0 wl0_15 wl1_15 vdd gnd replica_cell_1rw_1r
Xrbc_16 bl0_0 br0_0 bl1_0 br1_0 wl0_16 wl1_16 vdd gnd replica_cell_1rw_1r
Xrbc_17 bl0_0 br0_0 bl1_0 br1_0 wl0_17 wl1_17 vdd gnd replica_cell_1rw_1r
Xrbc_18 bl0_0 br0_0 bl1_0 br1_0 wl0_18 wl1_18 vdd gnd replica_cell_1rw_1r
.ENDS replica_column_0

.SUBCKT dummy_array bl0_0 br0_0 bl1_0 br1_0 bl0_1 br0_1 bl1_1 br1_1 wl0_0 wl1_0 vdd gnd
* INOUT : bl0_0 
* INOUT : br0_0 
* INOUT : bl1_0 
* INOUT : br1_0 
* INOUT : bl0_1 
* INOUT : br0_1 
* INOUT : bl1_1 
* INOUT : br1_1 
* INPUT : wl0_0 
* INPUT : wl1_0 
* POWER : vdd 
* GROUND: gnd 
* rows: 1 cols: 2
Xbit_r0_c0 bl0_0 br0_0 bl1_0 br1_0 wl0_0 wl1_0 vdd gnd dummy_cell_1rw_1r
Xbit_r0_c1 bl0_1 br0_1 bl1_1 br1_1 wl0_0 wl1_0 vdd gnd dummy_cell_1rw_1r
.ENDS dummy_array

.SUBCKT replica_bitcell_array bl0_0 br0_0 bl1_0 br1_0 bl0_1 br0_1 bl1_1 br1_1 rbl_bl0_0 rbl_br0_0 rbl_bl1_1 rbl_br1_1 wl0_0 wl1_0 wl0_1 wl1_1 wl0_2 wl1_2 wl0_3 wl1_3 wl0_4 wl1_4 wl0_5 wl1_5 wl0_6 wl1_6 wl0_7 wl1_7 wl0_8 wl1_8 wl0_9 wl1_9 wl0_10 wl1_10 wl0_11 wl1_11 wl0_12 wl1_12 wl0_13 wl1_13 wl0_14 wl1_14 wl0_15 wl1_15 rbl_wl0_0 rbl_wl1_1 vdd gnd
* INOUT : bl0_0 
* INOUT : br0_0 
* INOUT : bl1_0 
* INOUT : br1_0 
* INOUT : bl0_1 
* INOUT : br0_1 
* INOUT : bl1_1 
* INOUT : br1_1 
* OUTPUT: rbl_bl0_0 
* OUTPUT: rbl_br0_0 
* OUTPUT: rbl_bl1_1 
* OUTPUT: rbl_br1_1 
* INPUT : wl0_0 
* INPUT : wl1_0 
* INPUT : wl0_1 
* INPUT : wl1_1 
* INPUT : wl0_2 
* INPUT : wl1_2 
* INPUT : wl0_3 
* INPUT : wl1_3 
* INPUT : wl0_4 
* INPUT : wl1_4 
* INPUT : wl0_5 
* INPUT : wl1_5 
* INPUT : wl0_6 
* INPUT : wl1_6 
* INPUT : wl0_7 
* INPUT : wl1_7 
* INPUT : wl0_8 
* INPUT : wl1_8 
* INPUT : wl0_9 
* INPUT : wl1_9 
* INPUT : wl0_10 
* INPUT : wl1_10 
* INPUT : wl0_11 
* INPUT : wl1_11 
* INPUT : wl0_12 
* INPUT : wl1_12 
* INPUT : wl0_13 
* INPUT : wl1_13 
* INPUT : wl0_14 
* INPUT : wl1_14 
* INPUT : wl0_15 
* INPUT : wl1_15 
* INPUT : rbl_wl0_0 
* INPUT : rbl_wl1_1 
* POWER : vdd 
* GROUND: gnd 
* rows: 16 cols: 2
Xbitcell_array bl0_0 br0_0 bl1_0 br1_0 bl0_1 br0_1 bl1_1 br1_1 wl0_0 wl1_0 wl0_1 wl1_1 wl0_2 wl1_2 wl0_3 wl1_3 wl0_4 wl1_4 wl0_5 wl1_5 wl0_6 wl1_6 wl0_7 wl1_7 wl0_8 wl1_8 wl0_9 wl1_9 wl0_10 wl1_10 wl0_11 wl1_11 wl0_12 wl1_12 wl0_13 wl1_13 wl0_14 wl1_14 wl0_15 wl1_15 vdd gnd bitcell_array
Xreplica_col_0 rbl_bl0_0 rbl_br0_0 rbl_bl1_0 rbl_br1_0 dummy_wl0_bot dummy_wl1_bot rbl_wl0_0 rbl_wl1_0 wl0_0 wl1_0 wl0_1 wl1_1 wl0_2 wl1_2 wl0_3 wl1_3 wl0_4 wl1_4 wl0_5 wl1_5 wl0_6 wl1_6 wl0_7 wl1_7 wl0_8 wl1_8 wl0_9 wl1_9 wl0_10 wl1_10 wl0_11 wl1_11 wl0_12 wl1_12 wl0_13 wl1_13 wl0_14 wl1_14 wl0_15 wl1_15 rbl_wl0_1 rbl_wl1_1 dummy_wl0_top dummy_wl1_top vdd gnd replica_column
Xreplica_col_1 rbl_bl0_1 rbl_br0_1 rbl_bl1_1 rbl_br1_1 dummy_wl0_bot dummy_wl1_bot rbl_wl0_0 rbl_wl1_0 wl0_0 wl1_0 wl0_1 wl1_1 wl0_2 wl1_2 wl0_3 wl1_3 wl0_4 wl1_4 wl0_5 wl1_5 wl0_6 wl1_6 wl0_7 wl1_7 wl0_8 wl1_8 wl0_9 wl1_9 wl0_10 wl1_10 wl0_11 wl1_11 wl0_12 wl1_12 wl0_13 wl1_13 wl0_14 wl1_14 wl0_15 wl1_15 rbl_wl0_1 rbl_wl1_1 dummy_wl0_top dummy_wl1_top vdd gnd replica_column_0
Xdummy_row_0 bl0_0 br0_0 bl1_0 br1_0 bl0_1 br0_1 bl1_1 br1_1 rbl_wl0_0 rbl_wl1_0 vdd gnd dummy_array
Xdummy_row_1 bl0_0 br0_0 bl1_0 br1_0 bl0_1 br0_1 bl1_1 br1_1 rbl_wl0_1 rbl_wl1_1 vdd gnd dummy_array
.ENDS replica_bitcell_array

.SUBCKT bank dout0_0 dout0_1 dout1_0 dout1_1 rbl_bl0_0 rbl_bl1_1 din0_0 din0_1 addr0_0 addr0_1 addr0_2 addr0_3 addr1_0 addr1_1 addr1_2 addr1_3 s_en0 s_en1 p_en_bar0 p_en_bar1 w_en0 wl_en0 wl_en1 vdd gnd
* OUTPUT: dout0_0 
* OUTPUT: dout0_1 
* OUTPUT: dout1_0 
* OUTPUT: dout1_1 
* OUTPUT: rbl_bl0_0 
* OUTPUT: rbl_bl1_1 
* INPUT : din0_0 
* INPUT : din0_1 
* INPUT : addr0_0 
* INPUT : addr0_1 
* INPUT : addr0_2 
* INPUT : addr0_3 
* INPUT : addr1_0 
* INPUT : addr1_1 
* INPUT : addr1_2 
* INPUT : addr1_3 
* INPUT : s_en0 
* INPUT : s_en1 
* INPUT : p_en_bar0 
* INPUT : p_en_bar1 
* INPUT : w_en0 
* INPUT : wl_en0 
* INPUT : wl_en1 
* POWER : vdd 
* GROUND: gnd 
Xreplica_bitcell_array bl0_0 br0_0 bl1_0 br1_0 bl0_1 br0_1 bl1_1 br1_1 rbl_bl0_0 rbl_br0_0 rbl_bl1_1 rbl_br1_1 wl0_0 wl1_0 wl0_1 wl1_1 wl0_2 wl1_2 wl0_3 wl1_3 wl0_4 wl1_4 wl0_5 wl1_5 wl0_6 wl1_6 wl0_7 wl1_7 wl0_8 wl1_8 wl0_9 wl1_9 wl0_10 wl1_10 wl0_11 wl1_11 wl0_12 wl1_12 wl0_13 wl1_13 wl0_14 wl1_14 wl0_15 wl1_15 wl_en0 wl_en1 vdd gnd replica_bitcell_array
Xport_data0 rbl_bl0_0 rbl_br0_0 bl0_0 br0_0 bl0_1 br0_1 dout0_0 dout0_1 din0_0 din0_1 s_en0 p_en_bar0 w_en0 vdd gnd port_data
Xport_data1 rbl_bl1_1 rbl_br1_1 bl1_0 br1_0 bl1_1 br1_1 dout1_0 dout1_1 s_en1 p_en_bar1 vdd gnd port_data_0
Xport_address0 addr0_0 addr0_1 addr0_2 addr0_3 wl_en0 wl0_0 wl0_1 wl0_2 wl0_3 wl0_4 wl0_5 wl0_6 wl0_7 wl0_8 wl0_9 wl0_10 wl0_11 wl0_12 wl0_13 wl0_14 wl0_15 vdd gnd port_address
Xport_address1 addr1_0 addr1_1 addr1_2 addr1_3 wl_en1 wl1_0 wl1_1 wl1_2 wl1_3 wl1_4 wl1_5 wl1_6 wl1_7 wl1_8 wl1_9 wl1_10 wl1_11 wl1_12 wl1_13 wl1_14 wl1_15 vdd gnd port_address
.ENDS bank

* ptx M{0} {1} nshort m=2 w=0.74u l=0.15u pd=1.78u ps=1.78u as=0.28p ad=0.28p

* ptx M{0} {1} pshort m=2 w=1.26u l=0.15u pd=2.82u ps=2.82u as=0.47p ad=0.47p

.SUBCKT pinv A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd pshort m=2 w=1.26u l=0.15u 
Mpinv_nmos Z A gnd gnd nshort m=2 w=0.74u l=0.15u 
.ENDS pinv

* ptx M{0} {1} nshort m=3 w=1.68u l=0.15u pd=3.66u ps=3.66u as=0.63p ad=0.63p

* ptx M{0} {1} pshort m=3 w=1.68u l=0.15u pd=3.66u ps=3.66u as=0.63p ad=0.63p

.SUBCKT pinv_0 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd pshort m=3 w=1.68u l=0.15u 
Mpinv_nmos Z A gnd gnd nshort m=3 w=1.68u l=0.15u 
.ENDS pinv_0

.SUBCKT dff_buf_0 D Q Qb clk vdd gnd
* INPUT : D 
* OUTPUT: Q 
* OUTPUT: Qb 
* INPUT : clk 
* POWER : vdd 
* GROUND: gnd 
* inv1: 2 inv2: 4
Xdff_buf_dff D qint clk vdd gnd dff
Xdff_buf_inv1 qint Qb vdd gnd pinv
Xdff_buf_inv2 Qb Q vdd gnd pinv_0
.ENDS dff_buf_0

.SUBCKT dff_buf_array din_0 din_1 dout_0 dout_bar_0 dout_1 dout_bar_1 clk vdd gnd
* INPUT : din_0 
* INPUT : din_1 
* OUTPUT: dout_0 
* OUTPUT: dout_bar_0 
* OUTPUT: dout_1 
* OUTPUT: dout_bar_1 
* INPUT : clk 
* POWER : vdd 
* GROUND: gnd 
* inv1: 2 inv2: 4
Xdff_r0_c0 din_0 dout_0 dout_bar_0 clk vdd gnd dff_buf_0
Xdff_r1_c0 din_1 dout_1 dout_bar_1 clk vdd gnd dff_buf_0
.ENDS dff_buf_array

* ptx M{0} {1} nshort m=1 w=0.74u l=0.15u pd=1.78u ps=1.78u as=0.28p ad=0.28p

* ptx M{0} {1} nshort m=1 w=0.74u l=0.15u pd=1.78u ps=1.78u as=0.28p ad=0.28p

* ptx M{0} {1} pshort m=1 w=1.12u l=0.15u pd=2.54u ps=2.54u as=0.42p ad=0.42p

.SUBCKT pnand2 A B Z vdd gnd
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpnand2_pmos1 vdd A Z vdd pshort m=1 w=1.12u l=0.15u 
Mpnand2_pmos2 Z B vdd vdd pshort m=1 w=1.12u l=0.15u 
Mpnand2_nmos1 Z B net1 gnd nshort m=1 w=0.74u l=0.15u 
Mpnand2_nmos2 net1 A gnd gnd nshort m=1 w=0.74u l=0.15u 
.ENDS pnand2

* ptx M{0} {1} nshort m=7 w=1.68u l=0.15u pd=3.66u ps=3.66u as=0.63p ad=0.63p

* ptx M{0} {1} pshort m=7 w=2.0u l=0.15u pd=4.30u ps=4.30u as=0.75p ad=0.75p

.SUBCKT pinv_1 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd pshort m=7 w=2.0u l=0.15u 
Mpinv_nmos Z A gnd gnd nshort m=7 w=1.68u l=0.15u 
.ENDS pinv_1

.SUBCKT pdriver A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [12]
Xbuf_inv1 A Z vdd gnd pinv_1
.ENDS pdriver

.SUBCKT pand2 A B Z vdd gnd
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Xpand2_nand A B zb_int vdd gnd pnand2
Xpand2_inv zb_int Z vdd gnd pdriver
.ENDS pand2

.SUBCKT pinv_2 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd pshort m=1 w=1.12u l=0.15u 
Mpinv_nmos Z A gnd gnd nshort m=1 w=0.36u l=0.15u 
.ENDS pinv_2

.SUBCKT pinv_3 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd pshort m=2 w=1.26u l=0.15u 
Mpinv_nmos Z A gnd gnd nshort m=2 w=0.74u l=0.15u 
.ENDS pinv_3

.SUBCKT pbuf A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Xbuf_inv1 A zb_int vdd gnd pinv_2
Xbuf_inv2 zb_int Z vdd gnd pinv_3
.ENDS pbuf

.SUBCKT pinv_4 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd pshort m=1 w=1.12u l=0.15u 
Mpinv_nmos Z A gnd gnd nshort m=1 w=0.36u l=0.15u 
.ENDS pinv_4

* ptx M{0} {1} nshort m=3 w=2.0u l=0.15u pd=4.30u ps=4.30u as=0.75p ad=0.75p

* ptx M{0} {1} pshort m=3 w=2.0u l=0.15u pd=4.30u ps=4.30u as=0.75p ad=0.75p

.SUBCKT pinv_5 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd pshort m=3 w=2.0u l=0.15u 
Mpinv_nmos Z A gnd gnd nshort m=3 w=2.0u l=0.15u 
.ENDS pinv_5

* ptx M{0} {1} nshort m=9 w=2.0u l=0.15u pd=4.30u ps=4.30u as=0.75p ad=0.75p

* ptx M{0} {1} pshort m=9 w=2.0u l=0.15u pd=4.30u ps=4.30u as=0.75p ad=0.75p

.SUBCKT pinv_6 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd pshort m=9 w=2.0u l=0.15u 
Mpinv_nmos Z A gnd gnd nshort m=9 w=2.0u l=0.15u 
.ENDS pinv_6

.SUBCKT pdriver_0 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [1, 2, 5, 15]
Xbuf_inv1 A Zb1_int vdd gnd pinv_4
Xbuf_inv2 Zb1_int Zb2_int vdd gnd pinv_3
Xbuf_inv3 Zb2_int Zb3_int vdd gnd pinv_5
Xbuf_inv4 Zb3_int Z vdd gnd pinv_6
.ENDS pdriver_0

.SUBCKT pinv_7 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd pshort m=1 w=1.12u l=0.15u 
Mpinv_nmos Z A gnd gnd nshort m=1 w=0.36u l=0.15u 
.ENDS pinv_7

.SUBCKT pdriver_1 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [1, 1, 2, 5]
Xbuf_inv1 A Zb1_int vdd gnd pinv_4
Xbuf_inv2 Zb1_int Zb2_int vdd gnd pinv_7
Xbuf_inv3 Zb2_int Zb3_int vdd gnd pinv_3
Xbuf_inv4 Zb3_int Z vdd gnd pinv_5
.ENDS pdriver_1

* ptx M{0} {1} nshort m=1 w=0.74u l=0.15u pd=1.78u ps=1.78u as=0.28p ad=0.28p

.SUBCKT pnand3 A B C Z vdd gnd
* INPUT : A 
* INPUT : B 
* INPUT : C 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpnand3_pmos1 vdd A Z vdd pshort m=1 w=1.12u l=0.15u 
Mpnand3_pmos2 Z B vdd vdd pshort m=1 w=1.12u l=0.15u 
Mpnand3_pmos3 Z C vdd vdd pshort m=1 w=1.12u l=0.15u 
Mpnand3_nmos1 Z C net1 gnd nshort m=1 w=0.74u l=0.15u 
Mpnand3_nmos2 net1 B net2 gnd nshort m=1 w=0.74u l=0.15u 
Mpnand3_nmos3 net2 A gnd gnd nshort m=1 w=0.74u l=0.15u 
.ENDS pnand3

* ptx M{0} {1} nshort m=6 w=2.0u l=0.15u pd=4.30u ps=4.30u as=0.75p ad=0.75p

* ptx M{0} {1} pshort m=6 w=2.0u l=0.15u pd=4.30u ps=4.30u as=0.75p ad=0.75p

.SUBCKT pinv_8 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd pshort m=6 w=2.0u l=0.15u 
Mpinv_nmos Z A gnd gnd nshort m=6 w=2.0u l=0.15u 
.ENDS pinv_8

.SUBCKT pdriver_2 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [10]
Xbuf_inv1 A Z vdd gnd pinv_8
.ENDS pdriver_2

.SUBCKT pand3 A B C Z vdd gnd
* INPUT : A 
* INPUT : B 
* INPUT : C 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Xpand3_nand A B C zb_int vdd gnd pnand3
Xpand3_inv zb_int Z vdd gnd pdriver_2
.ENDS pand3

.SUBCKT pinv_9 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd pshort m=2 w=1.26u l=0.15u 
Mpinv_nmos Z A gnd gnd nshort m=2 w=0.74u l=0.15u 
.ENDS pinv_9

.SUBCKT pdriver_3 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [2]
Xbuf_inv1 A Z vdd gnd pinv_9
.ENDS pdriver_3

.SUBCKT pand3_0 A B C Z vdd gnd
* INPUT : A 
* INPUT : B 
* INPUT : C 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Xpand3_nand A B C zb_int vdd gnd pnand3
Xpand3_inv zb_int Z vdd gnd pdriver_3
.ENDS pand3_0

.SUBCKT pdriver_4 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [1, 1]
Xbuf_inv1 A Zb1_int vdd gnd pinv_4
Xbuf_inv2 Zb1_int Z vdd gnd pinv_7
.ENDS pdriver_4

.SUBCKT pnand2_0 A B Z vdd gnd
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpnand2_pmos1 vdd A Z vdd pshort m=1 w=1.12u l=0.15u 
Mpnand2_pmos2 Z B vdd vdd pshort m=1 w=1.12u l=0.15u 
Mpnand2_nmos1 Z B net1 gnd nshort m=1 w=0.74u l=0.15u 
Mpnand2_nmos2 net1 A gnd gnd nshort m=1 w=0.74u l=0.15u 
.ENDS pnand2_0

.SUBCKT pinv_10 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd pshort m=1 w=1.12u l=0.15u 
Mpinv_nmos Z A gnd gnd nshort m=1 w=0.36u l=0.15u 
.ENDS pinv_10

.SUBCKT delay_chain in out vdd gnd
* INPUT : in 
* OUTPUT: out 
* POWER : vdd 
* GROUND: gnd 
* fanouts: [4, 4, 4, 4, 4, 4, 4, 4, 4]
Xdinv0 in dout_1 vdd gnd pinv_10
Xdload_0_0 dout_1 n_0_0 vdd gnd pinv_10
Xdload_0_1 dout_1 n_0_1 vdd gnd pinv_10
Xdload_0_2 dout_1 n_0_2 vdd gnd pinv_10
Xdload_0_3 dout_1 n_0_3 vdd gnd pinv_10
Xdinv1 dout_1 dout_2 vdd gnd pinv_10
Xdload_1_0 dout_2 n_1_0 vdd gnd pinv_10
Xdload_1_1 dout_2 n_1_1 vdd gnd pinv_10
Xdload_1_2 dout_2 n_1_2 vdd gnd pinv_10
Xdload_1_3 dout_2 n_1_3 vdd gnd pinv_10
Xdinv2 dout_2 dout_3 vdd gnd pinv_10
Xdload_2_0 dout_3 n_2_0 vdd gnd pinv_10
Xdload_2_1 dout_3 n_2_1 vdd gnd pinv_10
Xdload_2_2 dout_3 n_2_2 vdd gnd pinv_10
Xdload_2_3 dout_3 n_2_3 vdd gnd pinv_10
Xdinv3 dout_3 dout_4 vdd gnd pinv_10
Xdload_3_0 dout_4 n_3_0 vdd gnd pinv_10
Xdload_3_1 dout_4 n_3_1 vdd gnd pinv_10
Xdload_3_2 dout_4 n_3_2 vdd gnd pinv_10
Xdload_3_3 dout_4 n_3_3 vdd gnd pinv_10
Xdinv4 dout_4 dout_5 vdd gnd pinv_10
Xdload_4_0 dout_5 n_4_0 vdd gnd pinv_10
Xdload_4_1 dout_5 n_4_1 vdd gnd pinv_10
Xdload_4_2 dout_5 n_4_2 vdd gnd pinv_10
Xdload_4_3 dout_5 n_4_3 vdd gnd pinv_10
Xdinv5 dout_5 dout_6 vdd gnd pinv_10
Xdload_5_0 dout_6 n_5_0 vdd gnd pinv_10
Xdload_5_1 dout_6 n_5_1 vdd gnd pinv_10
Xdload_5_2 dout_6 n_5_2 vdd gnd pinv_10
Xdload_5_3 dout_6 n_5_3 vdd gnd pinv_10
Xdinv6 dout_6 dout_7 vdd gnd pinv_10
Xdload_6_0 dout_7 n_6_0 vdd gnd pinv_10
Xdload_6_1 dout_7 n_6_1 vdd gnd pinv_10
Xdload_6_2 dout_7 n_6_2 vdd gnd pinv_10
Xdload_6_3 dout_7 n_6_3 vdd gnd pinv_10
Xdinv7 dout_7 dout_8 vdd gnd pinv_10
Xdload_7_0 dout_8 n_7_0 vdd gnd pinv_10
Xdload_7_1 dout_8 n_7_1 vdd gnd pinv_10
Xdload_7_2 dout_8 n_7_2 vdd gnd pinv_10
Xdload_7_3 dout_8 n_7_3 vdd gnd pinv_10
Xdinv8 dout_8 out vdd gnd pinv_10
Xdload_8_0 out n_8_0 vdd gnd pinv_10
Xdload_8_1 out n_8_1 vdd gnd pinv_10
Xdload_8_2 out n_8_2 vdd gnd pinv_10
Xdload_8_3 out n_8_3 vdd gnd pinv_10
.ENDS delay_chain

.SUBCKT control_logic_rw csb web clk rbl_bl s_en w_en p_en_bar wl_en clk_buf vdd gnd
* INPUT : csb 
* INPUT : web 
* INPUT : clk 
* INPUT : rbl_bl 
* OUTPUT: s_en 
* OUTPUT: w_en 
* OUTPUT: p_en_bar 
* OUTPUT: wl_en 
* OUTPUT: clk_buf 
* POWER : vdd 
* GROUND: gnd 
* word_size 2
Xctrl_dffs csb web cs_bar cs we_bar we clk_buf vdd gnd dff_buf_array
Xclkbuf clk clk_buf vdd gnd pdriver_0
Xinv_clk_bar clk_buf clk_bar vdd gnd pinv_2
Xand2_gated_clk_bar clk_bar cs gated_clk_bar vdd gnd pand2
Xand2_gated_clk_buf clk_buf cs gated_clk_buf vdd gnd pand2
Xbuf_wl_en gated_clk_bar wl_en vdd gnd pdriver_1
Xrbl_bl_delay_inv rbl_bl_delay rbl_bl_delay_bar vdd gnd pinv_2
Xw_en_and we rbl_bl_delay_bar gated_clk_bar w_en vdd gnd pand3
Xbuf_s_en_and rbl_bl_delay gated_clk_bar we_bar s_en vdd gnd pand3_0
Xdelay_chain rbl_bl rbl_bl_delay vdd gnd delay_chain
Xnand_p_en_bar gated_clk_buf rbl_bl_delay p_en_bar_unbuf vdd gnd pnand2_0
Xbuf_p_en_bar p_en_bar_unbuf p_en_bar vdd gnd pdriver_4
.ENDS control_logic_rw

.SUBCKT dff_buf_array_0 din_0 dout_0 dout_bar_0 clk vdd gnd
* INPUT : din_0 
* OUTPUT: dout_0 
* OUTPUT: dout_bar_0 
* INPUT : clk 
* POWER : vdd 
* GROUND: gnd 
* inv1: 2 inv2: 4
Xdff_r0_c0 din_0 dout_0 dout_bar_0 clk vdd gnd dff_buf_0
.ENDS dff_buf_array_0

.SUBCKT pinv_11 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd pshort m=3 w=1.68u l=0.15u 
Mpinv_nmos Z A gnd gnd nshort m=3 w=1.68u l=0.15u 
.ENDS pinv_11

* ptx M{0} {1} nshort m=8 w=1.68u l=0.15u pd=3.66u ps=3.66u as=0.63p ad=0.63p

* ptx M{0} {1} pshort m=8 w=2.0u l=0.15u pd=4.30u ps=4.30u as=0.75p ad=0.75p

.SUBCKT pinv_12 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd pshort m=8 w=2.0u l=0.15u 
Mpinv_nmos Z A gnd gnd nshort m=8 w=1.68u l=0.15u 
.ENDS pinv_12

.SUBCKT pdriver_5 A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [1, 1, 4, 13]
Xbuf_inv1 A Zb1_int vdd gnd pinv_4
Xbuf_inv2 Zb1_int Zb2_int vdd gnd pinv_7
Xbuf_inv3 Zb2_int Zb3_int vdd gnd pinv_11
Xbuf_inv4 Zb3_int Z vdd gnd pinv_12
.ENDS pdriver_5

.SUBCKT control_logic_r csb clk rbl_bl s_en p_en_bar wl_en clk_buf vdd gnd
* INPUT : csb 
* INPUT : clk 
* INPUT : rbl_bl 
* OUTPUT: s_en 
* OUTPUT: p_en_bar 
* OUTPUT: wl_en 
* OUTPUT: clk_buf 
* POWER : vdd 
* GROUND: gnd 
* word_size 2
Xctrl_dffs csb cs_bar cs clk_buf vdd gnd dff_buf_array_0
Xclkbuf clk clk_buf vdd gnd pdriver_5
Xinv_clk_bar clk_buf clk_bar vdd gnd pinv_2
Xand2_gated_clk_bar clk_bar cs gated_clk_bar vdd gnd pand2
Xand2_gated_clk_buf clk_buf cs gated_clk_buf vdd gnd pand2
Xbuf_wl_en gated_clk_bar wl_en vdd gnd pdriver_1
Xbuf_s_en_and rbl_bl_delay gated_clk_bar cs s_en vdd gnd pand3_0
Xdelay_chain rbl_bl rbl_bl_delay vdd gnd delay_chain
Xnand_p_en_bar gated_clk_buf rbl_bl_delay p_en_bar_unbuf vdd gnd pnand2_0
Xbuf_p_en_bar p_en_bar_unbuf p_en_bar vdd gnd pdriver_4
.ENDS control_logic_r

.SUBCKT sram_2_16_sky130 din0[0] din0[1] addr0[0] addr0[1] addr0[2] addr0[3] addr1[0] addr1[1] addr1[2] addr1[3] csb0 csb1 web0 clk0 clk1 dout0[0] dout0[1] dout1[0] dout1[1] vdd gnd
* INPUT : din0[0] 
* INPUT : din0[1] 
* INPUT : addr0[0] 
* INPUT : addr0[1] 
* INPUT : addr0[2] 
* INPUT : addr0[3] 
* INPUT : addr1[0] 
* INPUT : addr1[1] 
* INPUT : addr1[2] 
* INPUT : addr1[3] 
* INPUT : csb0 
* INPUT : csb1 
* INPUT : web0 
* INPUT : clk0 
* INPUT : clk1 
* OUTPUT: dout0[0] 
* OUTPUT: dout0[1] 
* OUTPUT: dout1[0] 
* OUTPUT: dout1[1] 
* POWER : vdd 
* GROUND: gnd 
Xbank0 dout0[0] dout0[1] dout1[0] dout1[1] rbl_bl0 rbl_bl1 bank_din0[0] bank_din0[1] a0[0] a0[1] a0[2] a0[3] a1[0] a1[1] a1[2] a1[3] s_en0 s_en1 p_en_bar0 p_en_bar1 w_en0 wl_en0 wl_en1 vdd gnd bank
Xcontrol0 csb0 web0 clk0 rbl_bl0 s_en0 w_en0 p_en_bar0 wl_en0 clk_buf0 vdd gnd control_logic_rw
Xcontrol1 csb1 clk1 rbl_bl1 s_en1 p_en_bar1 wl_en1 clk_buf1 vdd gnd control_logic_r
Xrow_address0 addr0[0] addr0[1] addr0[2] addr0[3] a0[0] a0[1] a0[2] a0[3] clk_buf0 vdd gnd row_addr_dff
Xrow_address1 addr1[0] addr1[1] addr1[2] addr1[3] a1[0] a1[1] a1[2] a1[3] clk_buf1 vdd gnd row_addr_dff
Xdata_dff0 din0[0] din0[1] bank_din0[0] bank_din0[1] clk_buf0 vdd gnd data_dff
.ENDS sram_2_16_sky130
