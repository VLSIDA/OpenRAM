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

* ptx M{0} {1} n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p

* ptx M{0} {1} p m=1 w=3.2u l=0.4u pd=7.2u ps=7.2u as=3.2p ad=3.2p

.SUBCKT pinv_2 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=3.2u l=0.4u pd=7.2u ps=7.2u as=3.2p ad=3.2p
Mpinv_nmos Z A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pinv_2

.SUBCKT dff_inv_2 D Q Qb clk vdd gnd
Xdff_inv_dff D Q clk vdd gnd dff
Xdff_inv_inv1 Q Qb vdd gnd pinv_2
.ENDS dff_inv_2

.SUBCKT dff_inv_array_2x1_1 din_0 din_1 dout_0 dout_bar_0 dout_1 dout_bar_1 clk vdd gnd
XXdff_r0_c0 din_0 dout_0 dout_bar_0 clk vdd gnd dff_inv_2
XXdff_r1_c0 din_1 dout_1 dout_bar_1 clk vdd gnd dff_inv_2
.ENDS dff_inv_array_2x1_1

* ptx M{0} {1} p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p

.SUBCKT pnand2_1 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pnand2_1

.SUBCKT pnand3_1 A B C Z vdd gnd
Mpnand3_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_pmos3 Z C vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_nmos1 Z C net1 gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_nmos2 net1 B net2 gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_nmos3 net2 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pnand3_1

* ptx M{0} {1} n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p

.SUBCKT pinv_3 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
.ENDS pinv_3

.SUBCKT pinv_4 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=3.2u l=0.4u pd=7.2u ps=7.2u as=3.2p ad=3.2p
Mpinv_nmos Z A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pinv_4

* ptx M{0} {1} n m=1 w=3.2u l=0.4u pd=7.2u ps=7.2u as=3.2p ad=3.2p

* ptx M{0} {1} p m=1 w=6.4u l=0.4u pd=13.600000000000001u ps=13.600000000000001u as=6.4p ad=6.4p

.SUBCKT pinv_5 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=6.4u l=0.4u pd=13.600000000000001u ps=13.600000000000001u as=6.4p ad=6.4p
Mpinv_nmos Z A gnd gnd n m=1 w=3.2u l=0.4u pd=7.2u ps=7.2u as=3.2p ad=3.2p
.ENDS pinv_5

.SUBCKT pinvbuf_2_4_1 A Zb Z vdd gnd
Xbuf_inv1 A zb_int vdd gnd pinv_3
Xbuf_inv2 zb_int z_int vdd gnd pinv_4
Xbuf_inv3 z_int Zb vdd gnd pinv_5
Xbuf_inv4 zb_int Z vdd gnd pinv_5
.ENDS pinvbuf_2_4_1

.SUBCKT pinv_6 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
.ENDS pinv_6

.SUBCKT pinv_7 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=6.4u l=0.4u pd=13.600000000000001u ps=13.600000000000001u as=6.4p ad=6.4p
Mpinv_nmos Z A gnd gnd n m=1 w=3.2u l=0.4u pd=7.2u ps=7.2u as=3.2p ad=3.2p
.ENDS pinv_7

* ptx M{0} {1} n m=1 w=12.8u l=0.4u pd=26.400000000000002u ps=26.400000000000002u as=12.8p ad=12.8p

* ptx M{0} {1} p m=1 w=25.6u l=0.4u pd=52.0u ps=52.0u as=25.6p ad=25.6p

.SUBCKT pinv_8 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=25.6u l=0.4u pd=52.0u ps=52.0u as=25.6p ad=25.6p
Mpinv_nmos Z A gnd gnd n m=1 w=12.8u l=0.4u pd=26.400000000000002u ps=26.400000000000002u as=12.8p ad=12.8p
.ENDS pinv_8

* ptx M{0} {1} n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p

* ptx M{0} {1} p m=1 w=0.6000000000000001u l=0.4u pd=2.0u ps=2.0u as=0.6000000000000001p ad=0.6000000000000001p

* ptx M{0} {1} n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p

* ptx M{0} {1} n m=1 w=1.2000000000000002u l=0.4u pd=3.2u ps=3.2u as=1.2000000000000002p ad=1.2000000000000002p

.SUBCKT replica_pbitcell_1RW_1W_1R bl0 br0 bl1 br1 bl2 br2 wl0 wl1 wl2 vdd gnd
Minverter_nmos_left Q vdd gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Minverter_nmos_right gnd Q vdd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Minverter_pmos_left Q vdd vdd vdd p m=1 w=0.6000000000000001u l=0.4u pd=2.0u ps=2.0u as=0.6000000000000001p ad=0.6000000000000001p
Minverter_pmos_right vdd Q vdd vdd p m=1 w=0.6000000000000001u l=0.4u pd=2.0u ps=2.0u as=0.6000000000000001p ad=0.6000000000000001p
Mreadwrite_nmos_left0 bl0 wl0 Q gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
Mreadwrite_nmos_right0 vdd wl0 br0 gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
Mwrite_nmos_left0 bl1 wl1 Q gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
Mwrite_nmos_right0 vdd wl1 br1 gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
Mread_access_nmos_left0 RA_to_R_left0 vdd gnd gnd n m=1 w=1.2000000000000002u l=0.4u pd=3.2u ps=3.2u as=1.2000000000000002p ad=1.2000000000000002p
Mread_access_nmos_right0 gnd Q RA_to_R_right0 gnd n m=1 w=1.2000000000000002u l=0.4u pd=3.2u ps=3.2u as=1.2000000000000002p ad=1.2000000000000002p
Mread_nmos_left0 bl2 wl2 RA_to_R_left0 gnd n m=1 w=1.2000000000000002u l=0.4u pd=3.2u ps=3.2u as=1.2000000000000002p ad=1.2000000000000002p
Mread_nmos_right0 RA_to_R_right0 wl2 br2 gnd n m=1 w=1.2000000000000002u l=0.4u pd=3.2u ps=3.2u as=1.2000000000000002p ad=1.2000000000000002p
.ENDS replica_pbitcell_1RW_1W_1R

.SUBCKT replica_pbitcell bl0 br0 bl1 br1 bl2 br2 wl0 wl1 wl2 vdd gnd
Xpbitcell bl0 br0 bl1 br1 bl2 br2 wl0 wl1 wl2 vdd gnd replica_pbitcell_1RW_1W_1R
.ENDS replica_pbitcell

.SUBCKT pbitcell_1RW_1W_1R bl0 br0 bl1 br1 bl2 br2 wl0 wl1 wl2 vdd gnd
Minverter_nmos_left Q Q_bar gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Minverter_nmos_right gnd Q Q_bar gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Minverter_pmos_left Q Q_bar vdd vdd p m=1 w=0.6000000000000001u l=0.4u pd=2.0u ps=2.0u as=0.6000000000000001p ad=0.6000000000000001p
Minverter_pmos_right vdd Q Q_bar vdd p m=1 w=0.6000000000000001u l=0.4u pd=2.0u ps=2.0u as=0.6000000000000001p ad=0.6000000000000001p
Mreadwrite_nmos_left0 bl0 wl0 Q gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
Mreadwrite_nmos_right0 Q_bar wl0 br0 gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
Mwrite_nmos_left0 bl1 wl1 Q gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
Mwrite_nmos_right0 Q_bar wl1 br1 gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
Mread_access_nmos_left0 RA_to_R_left0 Q_bar gnd gnd n m=1 w=1.2000000000000002u l=0.4u pd=3.2u ps=3.2u as=1.2000000000000002p ad=1.2000000000000002p
Mread_access_nmos_right0 gnd Q RA_to_R_right0 gnd n m=1 w=1.2000000000000002u l=0.4u pd=3.2u ps=3.2u as=1.2000000000000002p ad=1.2000000000000002p
Mread_nmos_left0 bl2 wl2 RA_to_R_left0 gnd n m=1 w=1.2000000000000002u l=0.4u pd=3.2u ps=3.2u as=1.2000000000000002p ad=1.2000000000000002p
Mread_nmos_right0 RA_to_R_right0 wl2 br2 gnd n m=1 w=1.2000000000000002u l=0.4u pd=3.2u ps=3.2u as=1.2000000000000002p ad=1.2000000000000002p
.ENDS pbitcell_1RW_1W_1R

.SUBCKT bitcell_array_8x1_1 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_0 wl1_0 wl2_0 wl0_1 wl1_1 wl2_1 wl0_2 wl1_2 wl2_2 wl0_3 wl1_3 wl2_3 wl0_4 wl1_4 wl2_4 wl0_5 wl1_5 wl2_5 wl0_6 wl1_6 wl2_6 wl0_7 wl1_7 wl2_7 vdd gnd
Xbit_r0_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_0 wl1_0 wl2_0 vdd gnd pbitcell_1RW_1W_1R
Xbit_r1_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_1 wl1_1 wl2_1 vdd gnd pbitcell_1RW_1W_1R
Xbit_r2_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_2 wl1_2 wl2_2 vdd gnd pbitcell_1RW_1W_1R
Xbit_r3_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_3 wl1_3 wl2_3 vdd gnd pbitcell_1RW_1W_1R
Xbit_r4_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_4 wl1_4 wl2_4 vdd gnd pbitcell_1RW_1W_1R
Xbit_r5_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_5 wl1_5 wl2_5 vdd gnd pbitcell_1RW_1W_1R
Xbit_r6_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_6 wl1_6 wl2_6 vdd gnd pbitcell_1RW_1W_1R
Xbit_r7_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_7 wl1_7 wl2_7 vdd gnd pbitcell_1RW_1W_1R
.ENDS bitcell_array_8x1_1

.SUBCKT pinv_9 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
.ENDS pinv_9

.SUBCKT delay_chain_1 in out vdd gnd
Xdinv0 in dout_1 vdd gnd pinv_9
Xdload_0_0 dout_1 n_0_0 vdd gnd pinv_9
Xdload_0_1 dout_1 n_0_1 vdd gnd pinv_9
Xdload_0_2 dout_1 n_0_2 vdd gnd pinv_9
Xdinv1 dout_1 dout_2 vdd gnd pinv_9
Xdload_1_0 dout_2 n_1_0 vdd gnd pinv_9
Xdload_1_1 dout_2 n_1_1 vdd gnd pinv_9
Xdload_1_2 dout_2 n_1_2 vdd gnd pinv_9
Xdinv2 dout_2 dout_3 vdd gnd pinv_9
Xdload_2_0 dout_3 n_2_0 vdd gnd pinv_9
Xdload_2_1 dout_3 n_2_1 vdd gnd pinv_9
Xdload_2_2 dout_3 n_2_2 vdd gnd pinv_9
Xdinv3 dout_3 out vdd gnd pinv_9
Xdload_3_0 out n_3_0 vdd gnd pinv_9
Xdload_3_1 out n_3_1 vdd gnd pinv_9
Xdload_3_2 out n_3_2 vdd gnd pinv_9
.ENDS delay_chain_1

.SUBCKT pinv_10 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
.ENDS pinv_10

* ptx M{0} {1} p m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p

.SUBCKT replica_bitline_rw en out vdd gnd
Xrbl_inv bl0_0 out vdd gnd pinv_10
Mrbl_access_tx vdd delayed_en bl0_0 vdd p m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
Xdelay_chain en delayed_en vdd gnd delay_chain_1
Xbitcell bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 delayed_en delayed_en delayed_en vdd gnd replica_pbitcell
Xload bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd vdd gnd bitcell_array_8x1_1
.ENDS replica_bitline_rw

.SUBCKT control_logic_rw csb web clk s_en w_en clk_buf_bar clk_buf vdd gnd
Xctrl_dffs csb web cs_bar cs we_bar we clk_buf vdd gnd dff_inv_array_2x1_1
Xclkbuf clk clk_buf_bar clk_buf vdd gnd pinvbuf_2_4_1
Xnand3_w_en_bar clk_buf_bar cs we w_en_bar vdd gnd pnand3_1
Xinv_pre_w_en w_en_bar pre_w_en vdd gnd pinv_6
Xinv_pre_w_en_bar pre_w_en pre_w_en_bar vdd gnd pinv_7
Xinv_w_en2 pre_w_en_bar w_en vdd gnd pinv_8
Xnand2_rbl_in_bar clk_buf_bar cs rbl_in_bar vdd gnd pnand2_1
Xinv_rbl_in rbl_in_bar rbl_in vdd gnd pinv_6
Xinv_pre_s_en_bar pre_s_en pre_s_en_bar vdd gnd pinv_7
Xinv_s_en pre_s_en_bar s_en vdd gnd pinv_8
Xreplica_bitline rbl_in pre_s_en vdd gnd replica_bitline_rw
.ENDS control_logic_rw

.SUBCKT pinv_12 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=3.2u l=0.4u pd=7.2u ps=7.2u as=3.2p ad=3.2p
Mpinv_nmos Z A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pinv_12

.SUBCKT dff_inv_4 D Q Qb clk vdd gnd
Xdff_inv_dff D Q clk vdd gnd dff
Xdff_inv_inv1 Q Qb vdd gnd pinv_12
.ENDS dff_inv_4

.SUBCKT dff_inv_array_1x1_2 din_0 dout_0 dout_bar_0 clk vdd gnd
XXdff_r0_c0 din_0 dout_0 dout_bar_0 clk vdd gnd dff_inv_4
.ENDS dff_inv_array_1x1_2

.SUBCKT pnand2_2 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pnand2_2

.SUBCKT pnand3_2 A B C Z vdd gnd
Mpnand3_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_pmos3 Z C vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_nmos1 Z C net1 gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_nmos2 net1 B net2 gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_nmos3 net2 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pnand3_2

.SUBCKT pinv_13 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
.ENDS pinv_13

.SUBCKT pinv_14 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=3.2u l=0.4u pd=7.2u ps=7.2u as=3.2p ad=3.2p
Mpinv_nmos Z A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pinv_14

.SUBCKT pinv_15 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=6.4u l=0.4u pd=13.600000000000001u ps=13.600000000000001u as=6.4p ad=6.4p
Mpinv_nmos Z A gnd gnd n m=1 w=3.2u l=0.4u pd=7.2u ps=7.2u as=3.2p ad=3.2p
.ENDS pinv_15

.SUBCKT pinvbuf_2_4_2 A Zb Z vdd gnd
Xbuf_inv1 A zb_int vdd gnd pinv_13
Xbuf_inv2 zb_int z_int vdd gnd pinv_14
Xbuf_inv3 z_int Zb vdd gnd pinv_15
Xbuf_inv4 zb_int Z vdd gnd pinv_15
.ENDS pinvbuf_2_4_2

.SUBCKT pinv_16 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
.ENDS pinv_16

.SUBCKT pinv_17 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=6.4u l=0.4u pd=13.600000000000001u ps=13.600000000000001u as=6.4p ad=6.4p
Mpinv_nmos Z A gnd gnd n m=1 w=3.2u l=0.4u pd=7.2u ps=7.2u as=3.2p ad=3.2p
.ENDS pinv_17

.SUBCKT pinv_18 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=25.6u l=0.4u pd=52.0u ps=52.0u as=25.6p ad=25.6p
Mpinv_nmos Z A gnd gnd n m=1 w=12.8u l=0.4u pd=26.400000000000002u ps=26.400000000000002u as=12.8p ad=12.8p
.ENDS pinv_18

.SUBCKT control_logic_w csb clk w_en clk_buf_bar clk_buf vdd gnd
Xctrl_dffs csb cs_bar cs clk_buf vdd gnd dff_inv_array_1x1_2
Xclkbuf clk clk_buf_bar clk_buf vdd gnd pinvbuf_2_4_2
Xnand3_w_en_bar clk_buf_bar cs w_en_bar vdd gnd pnand2_2
Xinv_pre_w_en w_en_bar pre_w_en vdd gnd pinv_16
Xinv_pre_w_en_bar pre_w_en pre_w_en_bar vdd gnd pinv_17
Xinv_w_en2 pre_w_en_bar w_en vdd gnd pinv_18
.ENDS control_logic_w

.SUBCKT pinv_20 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=3.2u l=0.4u pd=7.2u ps=7.2u as=3.2p ad=3.2p
Mpinv_nmos Z A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pinv_20

.SUBCKT dff_inv_6 D Q Qb clk vdd gnd
Xdff_inv_dff D Q clk vdd gnd dff
Xdff_inv_inv1 Q Qb vdd gnd pinv_20
.ENDS dff_inv_6

.SUBCKT dff_inv_array_1x1_3 din_0 dout_0 dout_bar_0 clk vdd gnd
XXdff_r0_c0 din_0 dout_0 dout_bar_0 clk vdd gnd dff_inv_6
.ENDS dff_inv_array_1x1_3

.SUBCKT pnand2_3 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pnand2_3

.SUBCKT pnand3_3 A B C Z vdd gnd
Mpnand3_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_pmos3 Z C vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_nmos1 Z C net1 gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_nmos2 net1 B net2 gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_nmos3 net2 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pnand3_3

.SUBCKT pinv_21 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
.ENDS pinv_21

.SUBCKT pinv_22 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=3.2u l=0.4u pd=7.2u ps=7.2u as=3.2p ad=3.2p
Mpinv_nmos Z A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pinv_22

.SUBCKT pinv_23 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=6.4u l=0.4u pd=13.600000000000001u ps=13.600000000000001u as=6.4p ad=6.4p
Mpinv_nmos Z A gnd gnd n m=1 w=3.2u l=0.4u pd=7.2u ps=7.2u as=3.2p ad=3.2p
.ENDS pinv_23

.SUBCKT pinvbuf_2_4_3 A Zb Z vdd gnd
Xbuf_inv1 A zb_int vdd gnd pinv_21
Xbuf_inv2 zb_int z_int vdd gnd pinv_22
Xbuf_inv3 z_int Zb vdd gnd pinv_23
Xbuf_inv4 zb_int Z vdd gnd pinv_23
.ENDS pinvbuf_2_4_3

.SUBCKT pinv_24 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
.ENDS pinv_24

.SUBCKT pinv_25 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=6.4u l=0.4u pd=13.600000000000001u ps=13.600000000000001u as=6.4p ad=6.4p
Mpinv_nmos Z A gnd gnd n m=1 w=3.2u l=0.4u pd=7.2u ps=7.2u as=3.2p ad=3.2p
.ENDS pinv_25

.SUBCKT pinv_26 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=25.6u l=0.4u pd=52.0u ps=52.0u as=25.6p ad=25.6p
Mpinv_nmos Z A gnd gnd n m=1 w=12.8u l=0.4u pd=26.400000000000002u ps=26.400000000000002u as=12.8p ad=12.8p
.ENDS pinv_26

.SUBCKT bitcell_array_8x1_2 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_0 wl1_0 wl2_0 wl0_1 wl1_1 wl2_1 wl0_2 wl1_2 wl2_2 wl0_3 wl1_3 wl2_3 wl0_4 wl1_4 wl2_4 wl0_5 wl1_5 wl2_5 wl0_6 wl1_6 wl2_6 wl0_7 wl1_7 wl2_7 vdd gnd
Xbit_r0_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_0 wl1_0 wl2_0 vdd gnd pbitcell_1RW_1W_1R
Xbit_r1_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_1 wl1_1 wl2_1 vdd gnd pbitcell_1RW_1W_1R
Xbit_r2_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_2 wl1_2 wl2_2 vdd gnd pbitcell_1RW_1W_1R
Xbit_r3_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_3 wl1_3 wl2_3 vdd gnd pbitcell_1RW_1W_1R
Xbit_r4_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_4 wl1_4 wl2_4 vdd gnd pbitcell_1RW_1W_1R
Xbit_r5_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_5 wl1_5 wl2_5 vdd gnd pbitcell_1RW_1W_1R
Xbit_r6_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_6 wl1_6 wl2_6 vdd gnd pbitcell_1RW_1W_1R
Xbit_r7_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_7 wl1_7 wl2_7 vdd gnd pbitcell_1RW_1W_1R
.ENDS bitcell_array_8x1_2

.SUBCKT pinv_27 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
.ENDS pinv_27

.SUBCKT delay_chain_2 in out vdd gnd
Xdinv0 in dout_1 vdd gnd pinv_27
Xdload_0_0 dout_1 n_0_0 vdd gnd pinv_27
Xdload_0_1 dout_1 n_0_1 vdd gnd pinv_27
Xdload_0_2 dout_1 n_0_2 vdd gnd pinv_27
Xdinv1 dout_1 dout_2 vdd gnd pinv_27
Xdload_1_0 dout_2 n_1_0 vdd gnd pinv_27
Xdload_1_1 dout_2 n_1_1 vdd gnd pinv_27
Xdload_1_2 dout_2 n_1_2 vdd gnd pinv_27
Xdinv2 dout_2 dout_3 vdd gnd pinv_27
Xdload_2_0 dout_3 n_2_0 vdd gnd pinv_27
Xdload_2_1 dout_3 n_2_1 vdd gnd pinv_27
Xdload_2_2 dout_3 n_2_2 vdd gnd pinv_27
Xdinv3 dout_3 out vdd gnd pinv_27
Xdload_3_0 out n_3_0 vdd gnd pinv_27
Xdload_3_1 out n_3_1 vdd gnd pinv_27
Xdload_3_2 out n_3_2 vdd gnd pinv_27
.ENDS delay_chain_2

.SUBCKT pinv_28 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
.ENDS pinv_28

.SUBCKT replica_bitline_r en out vdd gnd
Xrbl_inv bl0_0 out vdd gnd pinv_28
Mrbl_access_tx vdd delayed_en bl0_0 vdd p m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
Xdelay_chain en delayed_en vdd gnd delay_chain_2
Xbitcell bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 delayed_en delayed_en delayed_en vdd gnd replica_pbitcell
Xload bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd vdd gnd bitcell_array_8x1_2
.ENDS replica_bitline_r

.SUBCKT control_logic_r csb clk s_en clk_buf_bar clk_buf vdd gnd
Xctrl_dffs csb cs_bar cs clk_buf vdd gnd dff_inv_array_1x1_3
Xclkbuf clk clk_buf_bar clk_buf vdd gnd pinvbuf_2_4_3
Xnand2_rbl_in_bar clk_buf_bar cs rbl_in_bar vdd gnd pnand2_3
Xinv_rbl_in rbl_in_bar rbl_in vdd gnd pinv_24
Xinv_pre_s_en_bar pre_s_en pre_s_en_bar vdd gnd pinv_25
Xinv_s_en pre_s_en_bar s_en vdd gnd pinv_26
Xreplica_bitline rbl_in pre_s_en vdd gnd replica_bitline_r
.ENDS control_logic_r

.SUBCKT row_addr_dff din_0 din_1 din_2 din_3 dout_0 dout_1 dout_2 dout_3 clk vdd gnd
XXdff_r0_c0 din_0 dout_0 clk vdd gnd dff
XXdff_r1_c0 din_1 dout_1 clk vdd gnd dff
XXdff_r2_c0 din_2 dout_2 clk vdd gnd dff
XXdff_r3_c0 din_3 dout_3 clk vdd gnd dff
.ENDS row_addr_dff

.SUBCKT data_dff din_0 din_1 dout_0 dout_1 clk vdd gnd
XXdff_r0_c0 din_0 dout_0 clk vdd gnd dff
XXdff_r0_c1 din_1 dout_1 clk vdd gnd dff
.ENDS data_dff

.SUBCKT bitcell_array_16x2_1 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_0 wl1_0 wl2_0 wl0_1 wl1_1 wl2_1 wl0_2 wl1_2 wl2_2 wl0_3 wl1_3 wl2_3 wl0_4 wl1_4 wl2_4 wl0_5 wl1_5 wl2_5 wl0_6 wl1_6 wl2_6 wl0_7 wl1_7 wl2_7 wl0_8 wl1_8 wl2_8 wl0_9 wl1_9 wl2_9 wl0_10 wl1_10 wl2_10 wl0_11 wl1_11 wl2_11 wl0_12 wl1_12 wl2_12 wl0_13 wl1_13 wl2_13 wl0_14 wl1_14 wl2_14 wl0_15 wl1_15 wl2_15 vdd gnd
Xbit_r0_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_0 wl1_0 wl2_0 vdd gnd pbitcell_1RW_1W_1R
Xbit_r1_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_1 wl1_1 wl2_1 vdd gnd pbitcell_1RW_1W_1R
Xbit_r2_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_2 wl1_2 wl2_2 vdd gnd pbitcell_1RW_1W_1R
Xbit_r3_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_3 wl1_3 wl2_3 vdd gnd pbitcell_1RW_1W_1R
Xbit_r4_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_4 wl1_4 wl2_4 vdd gnd pbitcell_1RW_1W_1R
Xbit_r5_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_5 wl1_5 wl2_5 vdd gnd pbitcell_1RW_1W_1R
Xbit_r6_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_6 wl1_6 wl2_6 vdd gnd pbitcell_1RW_1W_1R
Xbit_r7_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_7 wl1_7 wl2_7 vdd gnd pbitcell_1RW_1W_1R
Xbit_r8_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_8 wl1_8 wl2_8 vdd gnd pbitcell_1RW_1W_1R
Xbit_r9_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_9 wl1_9 wl2_9 vdd gnd pbitcell_1RW_1W_1R
Xbit_r10_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_10 wl1_10 wl2_10 vdd gnd pbitcell_1RW_1W_1R
Xbit_r11_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_11 wl1_11 wl2_11 vdd gnd pbitcell_1RW_1W_1R
Xbit_r12_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_12 wl1_12 wl2_12 vdd gnd pbitcell_1RW_1W_1R
Xbit_r13_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_13 wl1_13 wl2_13 vdd gnd pbitcell_1RW_1W_1R
Xbit_r14_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_14 wl1_14 wl2_14 vdd gnd pbitcell_1RW_1W_1R
Xbit_r15_c0 bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 wl0_15 wl1_15 wl2_15 vdd gnd pbitcell_1RW_1W_1R
Xbit_r0_c1 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_0 wl1_0 wl2_0 vdd gnd pbitcell_1RW_1W_1R
Xbit_r1_c1 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_1 wl1_1 wl2_1 vdd gnd pbitcell_1RW_1W_1R
Xbit_r2_c1 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_2 wl1_2 wl2_2 vdd gnd pbitcell_1RW_1W_1R
Xbit_r3_c1 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_3 wl1_3 wl2_3 vdd gnd pbitcell_1RW_1W_1R
Xbit_r4_c1 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_4 wl1_4 wl2_4 vdd gnd pbitcell_1RW_1W_1R
Xbit_r5_c1 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_5 wl1_5 wl2_5 vdd gnd pbitcell_1RW_1W_1R
Xbit_r6_c1 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_6 wl1_6 wl2_6 vdd gnd pbitcell_1RW_1W_1R
Xbit_r7_c1 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_7 wl1_7 wl2_7 vdd gnd pbitcell_1RW_1W_1R
Xbit_r8_c1 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_8 wl1_8 wl2_8 vdd gnd pbitcell_1RW_1W_1R
Xbit_r9_c1 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_9 wl1_9 wl2_9 vdd gnd pbitcell_1RW_1W_1R
Xbit_r10_c1 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_10 wl1_10 wl2_10 vdd gnd pbitcell_1RW_1W_1R
Xbit_r11_c1 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_11 wl1_11 wl2_11 vdd gnd pbitcell_1RW_1W_1R
Xbit_r12_c1 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_12 wl1_12 wl2_12 vdd gnd pbitcell_1RW_1W_1R
Xbit_r13_c1 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_13 wl1_13 wl2_13 vdd gnd pbitcell_1RW_1W_1R
Xbit_r14_c1 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_14 wl1_14 wl2_14 vdd gnd pbitcell_1RW_1W_1R
Xbit_r15_c1 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_15 wl1_15 wl2_15 vdd gnd pbitcell_1RW_1W_1R
.ENDS bitcell_array_16x2_1

* ptx M{0} {1} p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p

.SUBCKT precharge_1 bl br en vdd
Mlower_pmos bl en br vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mupper_pmos1 bl en vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mupper_pmos2 br en vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS precharge_1

.SUBCKT precharge_array_1 bl_0 br_0 bl_1 br_1 en vdd
Xpre_column_0 bl_0 br_0 en vdd precharge_1
Xpre_column_1 bl_1 br_1 en vdd precharge_1
.ENDS precharge_array_1

.SUBCKT precharge_2 bl br en vdd
Mlower_pmos bl en br vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mupper_pmos1 bl en vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mupper_pmos2 br en vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS precharge_2

.SUBCKT precharge_array_2 bl_0 br_0 bl_1 br_1 en vdd
Xpre_column_0 bl_0 br_0 en vdd precharge_2
Xpre_column_1 bl_1 br_1 en vdd precharge_2
.ENDS precharge_array_2
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

.SUBCKT write_driver_array data_0 data_1 bl_0 br_0 bl_1 br_1 en vdd gnd
XXwrite_driver0 data_0 bl_0 br_0 en vdd gnd write_driver
XXwrite_driver1 data_1 bl_1 br_1 en vdd gnd write_driver
.ENDS write_driver_array

.SUBCKT pinv_29 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
.ENDS pinv_29

.SUBCKT pnand2_4 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pnand2_4

.SUBCKT pnand3_4 A B C Z vdd gnd
Mpnand3_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_pmos3 Z C vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_nmos1 Z C net1 gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_nmos2 net1 B net2 gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_nmos3 net2 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pnand3_4

.SUBCKT pinv_30 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
.ENDS pinv_30

.SUBCKT pnand2_5 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pnand2_5

.SUBCKT pre2x4 in_0 in_1 out_0 out_1 out_2 out_3 vdd gnd
XXpre_inv_0 in_0 inbar_0 vdd gnd pinv_30
XXpre_inv_1 in_1 inbar_1 vdd gnd pinv_30
XXpre_nand_inv_0 Z_0 out_0 vdd gnd pinv_30
XXpre_nand_inv_1 Z_1 out_1 vdd gnd pinv_30
XXpre_nand_inv_2 Z_2 out_2 vdd gnd pinv_30
XXpre_nand_inv_3 Z_3 out_3 vdd gnd pinv_30
XXpre2x4_nand_0 inbar_0 inbar_1 Z_0 vdd gnd pnand2_5
XXpre2x4_nand_1 in_0 inbar_1 Z_1 vdd gnd pnand2_5
XXpre2x4_nand_2 inbar_0 in_1 Z_2 vdd gnd pnand2_5
XXpre2x4_nand_3 in_0 in_1 Z_3 vdd gnd pnand2_5
.ENDS pre2x4

.SUBCKT pinv_31 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
.ENDS pinv_31

.SUBCKT pnand3_5 A B C Z vdd gnd
Mpnand3_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_pmos3 Z C vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_nmos1 Z C net1 gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_nmos2 net1 B net2 gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand3_nmos3 net2 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pnand3_5

.SUBCKT pre3x8 in_0 in_1 in_2 out_0 out_1 out_2 out_3 out_4 out_5 out_6 out_7 vdd gnd
XXpre_inv_0 in_0 inbar_0 vdd gnd pinv_31
XXpre_inv_1 in_1 inbar_1 vdd gnd pinv_31
XXpre_inv_2 in_2 inbar_2 vdd gnd pinv_31
XXpre_nand_inv_0 Z_0 out_0 vdd gnd pinv_31
XXpre_nand_inv_1 Z_1 out_1 vdd gnd pinv_31
XXpre_nand_inv_2 Z_2 out_2 vdd gnd pinv_31
XXpre_nand_inv_3 Z_3 out_3 vdd gnd pinv_31
XXpre_nand_inv_4 Z_4 out_4 vdd gnd pinv_31
XXpre_nand_inv_5 Z_5 out_5 vdd gnd pinv_31
XXpre_nand_inv_6 Z_6 out_6 vdd gnd pinv_31
XXpre_nand_inv_7 Z_7 out_7 vdd gnd pinv_31
XXpre3x8_nand_0 inbar_0 inbar_1 inbar_2 Z_0 vdd gnd pnand3_5
XXpre3x8_nand_1 in_0 inbar_1 inbar_2 Z_1 vdd gnd pnand3_5
XXpre3x8_nand_2 inbar_0 in_1 inbar_2 Z_2 vdd gnd pnand3_5
XXpre3x8_nand_3 in_0 in_1 inbar_2 Z_3 vdd gnd pnand3_5
XXpre3x8_nand_4 inbar_0 inbar_1 in_2 Z_4 vdd gnd pnand3_5
XXpre3x8_nand_5 in_0 inbar_1 in_2 Z_5 vdd gnd pnand3_5
XXpre3x8_nand_6 inbar_0 in_1 in_2 Z_6 vdd gnd pnand3_5
XXpre3x8_nand_7 in_0 in_1 in_2 Z_7 vdd gnd pnand3_5
.ENDS pre3x8

.SUBCKT hierarchical_decoder_16rows addr_0 addr_1 addr_2 addr_3 decode_0 decode_1 decode_2 decode_3 decode_4 decode_5 decode_6 decode_7 decode_8 decode_9 decode_10 decode_11 decode_12 decode_13 decode_14 decode_15 vdd gnd
Xpre_0 addr_0 addr_1 out_0 out_1 out_2 out_3 vdd gnd pre2x4
Xpre_1 addr_2 addr_3 out_4 out_5 out_6 out_7 vdd gnd pre2x4
XDEC_NAND_0 out_0 out_4 Z_0 vdd gnd pnand2_4
XDEC_NAND_1 out_0 out_5 Z_1 vdd gnd pnand2_4
XDEC_NAND_2 out_0 out_6 Z_2 vdd gnd pnand2_4
XDEC_NAND_3 out_0 out_7 Z_3 vdd gnd pnand2_4
XDEC_NAND_4 out_1 out_4 Z_4 vdd gnd pnand2_4
XDEC_NAND_5 out_1 out_5 Z_5 vdd gnd pnand2_4
XDEC_NAND_6 out_1 out_6 Z_6 vdd gnd pnand2_4
XDEC_NAND_7 out_1 out_7 Z_7 vdd gnd pnand2_4
XDEC_NAND_8 out_2 out_4 Z_8 vdd gnd pnand2_4
XDEC_NAND_9 out_2 out_5 Z_9 vdd gnd pnand2_4
XDEC_NAND_10 out_2 out_6 Z_10 vdd gnd pnand2_4
XDEC_NAND_11 out_2 out_7 Z_11 vdd gnd pnand2_4
XDEC_NAND_12 out_3 out_4 Z_12 vdd gnd pnand2_4
XDEC_NAND_13 out_3 out_5 Z_13 vdd gnd pnand2_4
XDEC_NAND_14 out_3 out_6 Z_14 vdd gnd pnand2_4
XDEC_NAND_15 out_3 out_7 Z_15 vdd gnd pnand2_4
XDEC_INV_0 Z_0 decode_0 vdd gnd pinv_29
XDEC_INV_1 Z_1 decode_1 vdd gnd pinv_29
XDEC_INV_2 Z_2 decode_2 vdd gnd pinv_29
XDEC_INV_3 Z_3 decode_3 vdd gnd pinv_29
XDEC_INV_4 Z_4 decode_4 vdd gnd pinv_29
XDEC_INV_5 Z_5 decode_5 vdd gnd pinv_29
XDEC_INV_6 Z_6 decode_6 vdd gnd pinv_29
XDEC_INV_7 Z_7 decode_7 vdd gnd pinv_29
XDEC_INV_8 Z_8 decode_8 vdd gnd pinv_29
XDEC_INV_9 Z_9 decode_9 vdd gnd pinv_29
XDEC_INV_10 Z_10 decode_10 vdd gnd pinv_29
XDEC_INV_11 Z_11 decode_11 vdd gnd pinv_29
XDEC_INV_12 Z_12 decode_12 vdd gnd pinv_29
XDEC_INV_13 Z_13 decode_13 vdd gnd pinv_29
XDEC_INV_14 Z_14 decode_14 vdd gnd pinv_29
XDEC_INV_15 Z_15 decode_15 vdd gnd pinv_29
.ENDS hierarchical_decoder_16rows

.SUBCKT pinv_32 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
.ENDS pinv_32

.SUBCKT pinv_33 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
.ENDS pinv_33

.SUBCKT pnand2_6 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
.ENDS pnand2_6

.SUBCKT wordline_driver in_0 in_1 in_2 in_3 in_4 in_5 in_6 in_7 in_8 in_9 in_10 in_11 in_12 in_13 in_14 in_15 wl_0 wl_1 wl_2 wl_3 wl_4 wl_5 wl_6 wl_7 wl_8 wl_9 wl_10 wl_11 wl_12 wl_13 wl_14 wl_15 en vdd gnd
Xwl_driver_inv_en0 en en_bar_0 vdd gnd pinv_33
Xwl_driver_nand0 en_bar_0 in_0 wl_bar_0 vdd gnd pnand2_6
Xwl_driver_inv0 wl_bar_0 wl_0 vdd gnd pinv_32
Xwl_driver_inv_en1 en en_bar_1 vdd gnd pinv_33
Xwl_driver_nand1 en_bar_1 in_1 wl_bar_1 vdd gnd pnand2_6
Xwl_driver_inv1 wl_bar_1 wl_1 vdd gnd pinv_32
Xwl_driver_inv_en2 en en_bar_2 vdd gnd pinv_33
Xwl_driver_nand2 en_bar_2 in_2 wl_bar_2 vdd gnd pnand2_6
Xwl_driver_inv2 wl_bar_2 wl_2 vdd gnd pinv_32
Xwl_driver_inv_en3 en en_bar_3 vdd gnd pinv_33
Xwl_driver_nand3 en_bar_3 in_3 wl_bar_3 vdd gnd pnand2_6
Xwl_driver_inv3 wl_bar_3 wl_3 vdd gnd pinv_32
Xwl_driver_inv_en4 en en_bar_4 vdd gnd pinv_33
Xwl_driver_nand4 en_bar_4 in_4 wl_bar_4 vdd gnd pnand2_6
Xwl_driver_inv4 wl_bar_4 wl_4 vdd gnd pinv_32
Xwl_driver_inv_en5 en en_bar_5 vdd gnd pinv_33
Xwl_driver_nand5 en_bar_5 in_5 wl_bar_5 vdd gnd pnand2_6
Xwl_driver_inv5 wl_bar_5 wl_5 vdd gnd pinv_32
Xwl_driver_inv_en6 en en_bar_6 vdd gnd pinv_33
Xwl_driver_nand6 en_bar_6 in_6 wl_bar_6 vdd gnd pnand2_6
Xwl_driver_inv6 wl_bar_6 wl_6 vdd gnd pinv_32
Xwl_driver_inv_en7 en en_bar_7 vdd gnd pinv_33
Xwl_driver_nand7 en_bar_7 in_7 wl_bar_7 vdd gnd pnand2_6
Xwl_driver_inv7 wl_bar_7 wl_7 vdd gnd pinv_32
Xwl_driver_inv_en8 en en_bar_8 vdd gnd pinv_33
Xwl_driver_nand8 en_bar_8 in_8 wl_bar_8 vdd gnd pnand2_6
Xwl_driver_inv8 wl_bar_8 wl_8 vdd gnd pinv_32
Xwl_driver_inv_en9 en en_bar_9 vdd gnd pinv_33
Xwl_driver_nand9 en_bar_9 in_9 wl_bar_9 vdd gnd pnand2_6
Xwl_driver_inv9 wl_bar_9 wl_9 vdd gnd pinv_32
Xwl_driver_inv_en10 en en_bar_10 vdd gnd pinv_33
Xwl_driver_nand10 en_bar_10 in_10 wl_bar_10 vdd gnd pnand2_6
Xwl_driver_inv10 wl_bar_10 wl_10 vdd gnd pinv_32
Xwl_driver_inv_en11 en en_bar_11 vdd gnd pinv_33
Xwl_driver_nand11 en_bar_11 in_11 wl_bar_11 vdd gnd pnand2_6
Xwl_driver_inv11 wl_bar_11 wl_11 vdd gnd pinv_32
Xwl_driver_inv_en12 en en_bar_12 vdd gnd pinv_33
Xwl_driver_nand12 en_bar_12 in_12 wl_bar_12 vdd gnd pnand2_6
Xwl_driver_inv12 wl_bar_12 wl_12 vdd gnd pinv_32
Xwl_driver_inv_en13 en en_bar_13 vdd gnd pinv_33
Xwl_driver_nand13 en_bar_13 in_13 wl_bar_13 vdd gnd pnand2_6
Xwl_driver_inv13 wl_bar_13 wl_13 vdd gnd pinv_32
Xwl_driver_inv_en14 en en_bar_14 vdd gnd pinv_33
Xwl_driver_nand14 en_bar_14 in_14 wl_bar_14 vdd gnd pnand2_6
Xwl_driver_inv14 wl_bar_14 wl_14 vdd gnd pinv_32
Xwl_driver_inv_en15 en en_bar_15 vdd gnd pinv_33
Xwl_driver_nand15 en_bar_15 in_15 wl_bar_15 vdd gnd pnand2_6
Xwl_driver_inv15 wl_bar_15 wl_15 vdd gnd pinv_32
.ENDS wordline_driver

.SUBCKT pinv_34 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.0u ps=4.0u as=1.6p ad=1.6p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.4000000000000004u ps=2.4000000000000004u as=0.8p ad=0.8p
.ENDS pinv_34

.SUBCKT bank dout0_0 dout0_1 dout2_0 dout2_1 din0_0 din0_1 din1_0 din1_1 addr0_0 addr0_1 addr0_2 addr0_3 addr1_0 addr1_1 addr1_2 addr1_3 addr2_0 addr2_1 addr2_2 addr2_3 s_en0 s_en2 w_en0 w_en1 clk_buf_bar0 clk_buf0 clk_buf_bar1 clk_buf1 clk_buf_bar2 clk_buf2 vdd gnd
Xbitcell_array bl0_0 br0_0 bl1_0 br1_0 bl2_0 br2_0 bl0_1 br0_1 bl1_1 br1_1 bl2_1 br2_1 wl0_0 wl1_0 wl2_0 wl0_1 wl1_1 wl2_1 wl0_2 wl1_2 wl2_2 wl0_3 wl1_3 wl2_3 wl0_4 wl1_4 wl2_4 wl0_5 wl1_5 wl2_5 wl0_6 wl1_6 wl2_6 wl0_7 wl1_7 wl2_7 wl0_8 wl1_8 wl2_8 wl0_9 wl1_9 wl2_9 wl0_10 wl1_10 wl2_10 wl0_11 wl1_11 wl2_11 wl0_12 wl1_12 wl2_12 wl0_13 wl1_13 wl2_13 wl0_14 wl1_14 wl2_14 wl0_15 wl1_15 wl2_15 vdd gnd bitcell_array_16x2_1
Xprecharge_array0 bl0_0 br0_0 bl0_1 br0_1 clk_buf_bar0 vdd precharge_array_1
Xprecharge_array2 bl2_0 br2_0 bl2_1 br2_1 clk_buf_bar2 vdd precharge_array_2
Xsense_amp_array0 dout0_0 bl0_0 br0_0 dout0_1 bl0_1 br0_1 s_en0 vdd gnd sense_amp_array
Xsense_amp_array2 dout2_0 bl2_0 br2_0 dout2_1 bl2_1 br2_1 s_en2 vdd gnd sense_amp_array
Xwrite_driver_array0 din0_0 din0_1 bl0_0 br0_0 bl0_1 br0_1 w_en0 vdd gnd write_driver_array
Xwrite_driver_array1 din1_0 din1_1 bl1_0 br1_0 bl1_1 br1_1 w_en1 vdd gnd write_driver_array
Xrow_decoder0 addr0_0 addr0_1 addr0_2 addr0_3 dec_out0_0 dec_out0_1 dec_out0_2 dec_out0_3 dec_out0_4 dec_out0_5 dec_out0_6 dec_out0_7 dec_out0_8 dec_out0_9 dec_out0_10 dec_out0_11 dec_out0_12 dec_out0_13 dec_out0_14 dec_out0_15 vdd gnd hierarchical_decoder_16rows
Xrow_decoder1 addr1_0 addr1_1 addr1_2 addr1_3 dec_out1_0 dec_out1_1 dec_out1_2 dec_out1_3 dec_out1_4 dec_out1_5 dec_out1_6 dec_out1_7 dec_out1_8 dec_out1_9 dec_out1_10 dec_out1_11 dec_out1_12 dec_out1_13 dec_out1_14 dec_out1_15 vdd gnd hierarchical_decoder_16rows
Xrow_decoder2 addr2_0 addr2_1 addr2_2 addr2_3 dec_out2_0 dec_out2_1 dec_out2_2 dec_out2_3 dec_out2_4 dec_out2_5 dec_out2_6 dec_out2_7 dec_out2_8 dec_out2_9 dec_out2_10 dec_out2_11 dec_out2_12 dec_out2_13 dec_out2_14 dec_out2_15 vdd gnd hierarchical_decoder_16rows
Xwordline_driver0 dec_out0_0 dec_out0_1 dec_out0_2 dec_out0_3 dec_out0_4 dec_out0_5 dec_out0_6 dec_out0_7 dec_out0_8 dec_out0_9 dec_out0_10 dec_out0_11 dec_out0_12 dec_out0_13 dec_out0_14 dec_out0_15 wl0_0 wl0_1 wl0_2 wl0_3 wl0_4 wl0_5 wl0_6 wl0_7 wl0_8 wl0_9 wl0_10 wl0_11 wl0_12 wl0_13 wl0_14 wl0_15 clk_buf0 vdd gnd wordline_driver
Xwordline_driver1 dec_out1_0 dec_out1_1 dec_out1_2 dec_out1_3 dec_out1_4 dec_out1_5 dec_out1_6 dec_out1_7 dec_out1_8 dec_out1_9 dec_out1_10 dec_out1_11 dec_out1_12 dec_out1_13 dec_out1_14 dec_out1_15 wl1_0 wl1_1 wl1_2 wl1_3 wl1_4 wl1_5 wl1_6 wl1_7 wl1_8 wl1_9 wl1_10 wl1_11 wl1_12 wl1_13 wl1_14 wl1_15 clk_buf1 vdd gnd wordline_driver
Xwordline_driver2 dec_out2_0 dec_out2_1 dec_out2_2 dec_out2_3 dec_out2_4 dec_out2_5 dec_out2_6 dec_out2_7 dec_out2_8 dec_out2_9 dec_out2_10 dec_out2_11 dec_out2_12 dec_out2_13 dec_out2_14 dec_out2_15 wl2_0 wl2_1 wl2_2 wl2_3 wl2_4 wl2_5 wl2_6 wl2_7 wl2_8 wl2_9 wl2_10 wl2_11 wl2_12 wl2_13 wl2_14 wl2_15 clk_buf2 vdd gnd wordline_driver
.ENDS bank

.SUBCKT sram_2_16_scn4m_subm DIN0[0] DIN0[1] DIN1[0] DIN1[1] ADDR0[0] ADDR0[1] ADDR0[2] ADDR0[3] ADDR1[0] ADDR1[1] ADDR1[2] ADDR1[3] ADDR2[0] ADDR2[1] ADDR2[2] ADDR2[3] csb0 csb1 csb2 web0 clk0 clk1 clk2 DOUT0[0] DOUT0[1] DOUT2[0] DOUT2[1] vdd gnd
Xbank0 DOUT0[0] DOUT0[1] DOUT2[0] DOUT2[1] BANK_DIN0[0] BANK_DIN0[1] BANK_DIN1[0] BANK_DIN1[1] A0[0] A0[1] A0[2] A0[3] A1[0] A1[1] A1[2] A1[3] A2[0] A2[1] A2[2] A2[3] s_en0 s_en2 w_en0 w_en1 clk_buf_bar0 clk_buf0 clk_buf_bar1 clk_buf1 clk_buf_bar2 clk_buf2 vdd gnd bank
Xcontrol0 csb0 web0 clk0 s_en0 w_en0 clk_buf_bar0 clk_buf0 vdd gnd control_logic_rw
Xcontrol1 csb1 clk1 w_en1 clk_buf_bar1 clk_buf1 vdd gnd control_logic_w
Xcontrol2 csb2 clk2 s_en2 clk_buf_bar2 clk_buf2 vdd gnd control_logic_r
Xrow_address0 ADDR0[0] ADDR0[1] ADDR0[2] ADDR0[3] A0[0] A0[1] A0[2] A0[3] clk_buf0 vdd gnd row_addr_dff
Xrow_address1 ADDR1[0] ADDR1[1] ADDR1[2] ADDR1[3] A1[0] A1[1] A1[2] A1[3] clk_buf1 vdd gnd row_addr_dff
Xrow_address2 ADDR2[0] ADDR2[1] ADDR2[2] ADDR2[3] A2[0] A2[1] A2[2] A2[3] clk_buf2 vdd gnd row_addr_dff
Xdata_dff0 DIN0[0] DIN0[1] BANK_DIN0[0] BANK_DIN0[1] clk_buf0 vdd gnd data_dff
Xdata_dff1 DIN1[0] DIN1[1] BANK_DIN1[0] BANK_DIN1[1] clk_buf1 vdd gnd data_dff
.ENDS sram_2_16_scn4m_subm
