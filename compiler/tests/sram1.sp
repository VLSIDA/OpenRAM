**************************************************
* OpenRAM generated memory.
* Words: 16
* Data bits: 4
* Banks: 1
* Column mux: 1:1
**************************************************
* Positive edge-triggered FF
.subckt dff D Q clk vdd gnd
M0 vdd clk a_2_6# vdd p w=12u l=0.6u
+ ad=0p pd=0u as=0p ps=0u
M1 a_17_74# D vdd vdd p w=6u l=0.6u
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
M9 vdd Q a_76_84# vdd p w=3u l=0.6u
+ ad=0p pd=0u as=0p ps=0u
M10 gnd clk a_2_6# gnd n w=6u l=0.6u
+ ad=0p pd=0u as=0p ps=0u
M11 Q a_66_6# vdd vdd p w=12u l=0.6u
+ ad=0p pd=0u as=0p ps=0u
M12 a_17_6# D gnd gnd n w=3u l=0.6u
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
M20 gnd Q a_76_6# gnd n w=3u l=0.6u
+ ad=0p pd=0u as=0p ps=0u
M21 Q a_66_6# gnd gnd n w=6u l=0.6u
+ ad=0p pd=0u as=0p ps=0u
.ends dff

* ptx M{0} {1} n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p

* ptx M{0} {1} p m=1 w=4.8u l=0.6u pd=10.799999999999999u ps=10.799999999999999u as=7.199999999999999p ad=7.199999999999999p

.SUBCKT pinv_2 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=4.8u l=0.6u pd=10.799999999999999u ps=10.799999999999999u as=7.199999999999999p ad=7.199999999999999p
Mpinv_nmos Z A gnd gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
.ENDS pinv_2

.SUBCKT dff_inv_2 D Q Qb clk vdd gnd
Xdff_inv_dff D Q clk vdd gnd dff
Xdff_inv_inv1 Q Qb vdd gnd pinv_2
.ENDS dff_inv_2

.SUBCKT dff_array_3x1 din[0] din[1] din[2] dout[0] dout_bar[0] dout[1] dout_bar[1] dout[2] dout_bar[2] clk vdd gnd
XXdff_r0_c0 din[0] dout[0] dout_bar[0] clk vdd gnd dff_inv_2
XXdff_r1_c0 din[1] dout[1] dout_bar[1] clk vdd gnd dff_inv_2
XXdff_r2_c0 din[2] dout[2] dout_bar[2] clk vdd gnd dff_inv_2
.ENDS dff_array_3x1

* ptx M{0} {1} p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p

.SUBCKT pnand2_1 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
.ENDS pnand2_1

.SUBCKT pnand3_1 A B C Z vdd gnd
Mpnand3_pmos1 vdd A Z vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand3_pmos2 Z B vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand3_pmos3 Z C vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand3_nmos1 Z C net1 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand3_nmos2 net1 B net2 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand3_nmos3 net2 A gnd gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
.ENDS pnand3_1

* ptx M{0} {1} n m=1 w=1.2u l=0.6u pd=3.5999999999999996u ps=3.5999999999999996u as=1.7999999999999998p ad=1.7999999999999998p

.SUBCKT pinv_3 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.5999999999999996u ps=3.5999999999999996u as=1.7999999999999998p ad=1.7999999999999998p
.ENDS pinv_3

* ptx M{0} {1} n m=1 w=4.8u l=0.6u pd=10.799999999999999u ps=10.799999999999999u as=7.199999999999999p ad=7.199999999999999p

* ptx M{0} {1} p m=1 w=9.6u l=0.6u pd=20.4u ps=20.4u as=14.399999999999999p ad=14.399999999999999p

.SUBCKT pinv_4 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=9.6u l=0.6u pd=20.4u ps=20.4u as=14.399999999999999p ad=14.399999999999999p
Mpinv_nmos Z A gnd gnd n m=1 w=4.8u l=0.6u pd=10.799999999999999u ps=10.799999999999999u as=7.199999999999999p ad=7.199999999999999p
.ENDS pinv_4

* ptx M{0} {1} n m=4 w=4.8u l=0.6u pd=10.799999999999999u ps=10.799999999999999u as=7.199999999999999p ad=7.199999999999999p

* ptx M{0} {1} p m=4 w=9.6u l=0.6u pd=20.4u ps=20.4u as=14.399999999999999p ad=14.399999999999999p

.SUBCKT pinv_5 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=4 w=9.6u l=0.6u pd=20.4u ps=20.4u as=14.399999999999999p ad=14.399999999999999p
Mpinv_nmos Z A gnd gnd n m=4 w=4.8u l=0.6u pd=10.799999999999999u ps=10.799999999999999u as=7.199999999999999p ad=7.199999999999999p
.ENDS pinv_5

.SUBCKT pinvbuf_4_16 A Zb Z vdd gnd
Xbuf_inv1 A zb_int vdd gnd pinv_3
Xbuf_inv2 zb_int z_int vdd gnd pinv_4
Xbuf_inv3 z_int Zb vdd gnd pinv_5
Xbuf_inv4 zb_int Z vdd gnd pinv_5
.ENDS pinvbuf_4_16

.SUBCKT pinv_6 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.5999999999999996u ps=3.5999999999999996u as=1.7999999999999998p ad=1.7999999999999998p
.ENDS pinv_6

.SUBCKT pinv_7 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=9.6u l=0.6u pd=20.4u ps=20.4u as=14.399999999999999p ad=14.399999999999999p
Mpinv_nmos Z A gnd gnd n m=1 w=4.8u l=0.6u pd=10.799999999999999u ps=10.799999999999999u as=7.199999999999999p ad=7.199999999999999p
.ENDS pinv_7

.SUBCKT pinv_8 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=4 w=9.6u l=0.6u pd=20.4u ps=20.4u as=14.399999999999999p ad=14.399999999999999p
Mpinv_nmos Z A gnd gnd n m=4 w=4.8u l=0.6u pd=10.799999999999999u ps=10.799999999999999u as=7.199999999999999p ad=7.199999999999999p
.ENDS pinv_8

*********************** "cell_6t" ******************************
.SUBCKT replica_cell_6t bl br wl vdd gnd
M_1 gnd net_2 vdd vdd p W='0.9u' L=1.2u
M_2 net_2 gnd vdd vdd p W='0.9u' L=1.2u
M_3 br wl net_2 gnd n W='1.2u' L=0.6u
M_4 bl wl gnd gnd n W='1.2u' L=0.6u
M_5 net_2 gnd gnd gnd n W='2.4u' L=0.6u
M_6 gnd net_2 gnd gnd n W='2.4u' L=0.6u
.ENDS	$ replica_cell_6t

*********************** "cell_6t" ******************************
.SUBCKT cell_6t bl br wl vdd gnd
M_1 net_1 net_2 vdd vdd p W='0.9u' L=1.2u
M_2 net_2 net_1 vdd vdd p W='0.9u' L=1.2u
M_3 br wl net_2 gnd n W='1.2u' L=0.6u
M_4 bl wl net_1 gnd n W='1.2u' L=0.6u
M_5 net_2 net_1 gnd gnd n W='2.4u' L=0.6u
M_6 net_1 net_2 gnd gnd n W='2.4u' L=0.6u
.ENDS	$ cell_6t

.SUBCKT bitline_load bl[0] br[0] wl[0] wl[1] wl[2] wl[3] vdd gnd
Xbit_r0_c0 bl[0] br[0] wl[0] vdd gnd cell_6t
Xbit_r1_c0 bl[0] br[0] wl[1] vdd gnd cell_6t
Xbit_r2_c0 bl[0] br[0] wl[2] vdd gnd cell_6t
Xbit_r3_c0 bl[0] br[0] wl[3] vdd gnd cell_6t
.ENDS bitline_load

.SUBCKT pinv_9 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.5999999999999996u ps=3.5999999999999996u as=1.7999999999999998p ad=1.7999999999999998p
.ENDS pinv_9

.SUBCKT delay_chain in out vdd gnd
Xdinv0 in dout_1 vdd gnd pinv_9
Xdload_0_0 dout_1 n_0_0 vdd gnd pinv_9
Xdload_0_1 dout_1 n_0_1 vdd gnd pinv_9
Xdload_0_2 dout_1 n_0_2 vdd gnd pinv_9
Xdinv1 dout_1 dout_2 vdd gnd pinv_9
Xdload_1_0 dout_2 n_1_0 vdd gnd pinv_9
Xdload_1_1 dout_2 n_1_1 vdd gnd pinv_9
Xdload_1_2 dout_2 n_1_2 vdd gnd pinv_9
Xdinv2 dout_2 out vdd gnd pinv_9
Xdload_2_0 out n_2_0 vdd gnd pinv_9
Xdload_2_1 out n_2_1 vdd gnd pinv_9
Xdload_2_2 out n_2_2 vdd gnd pinv_9
.ENDS delay_chain

.SUBCKT pinv_10 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.5999999999999996u ps=3.5999999999999996u as=1.7999999999999998p ad=1.7999999999999998p
.ENDS pinv_10

* ptx M{0} {1} p m=1 w=1.2u l=0.6u pd=3.5999999999999996u ps=3.5999999999999996u as=1.7999999999999998p ad=1.7999999999999998p

.SUBCKT replica_bitline en out vdd gnd
Xrbl_inv bl[0] out vdd gnd pinv_10
Mrbl_access_tx vdd delayed_en bl[0] vdd p m=1 w=1.2u l=0.6u pd=3.5999999999999996u ps=3.5999999999999996u as=1.7999999999999998p ad=1.7999999999999998p
Xdelay_chain en delayed_en vdd gnd delay_chain
Xbitcell bl[0] br[0] delayed_en vdd gnd replica_cell_6t
Xload bl[0] br[0] gnd gnd gnd gnd vdd gnd bitline_load
.ENDS replica_bitline

.SUBCKT control_logic csb web oeb clk s_en w_en tri_en tri_en_bar clk_buf_bar clk_buf vdd gnd
Xctrl_dffs csb web oeb cs_bar cs we_bar we oe_bar oe clk_buf vdd gnd dff_array_3x1
Xclkbuf clk clk_buf_bar clk_buf vdd gnd pinvbuf_4_16
Xnand3_w_en_bar clk_buf_bar cs we w_en_bar vdd gnd pnand3_1
Xinv_pre_w_en w_en_bar pre_w_en vdd gnd pinv_6
Xinv_pre_w_en_bar pre_w_en pre_w_en_bar vdd gnd pinv_7
Xinv_w_en2 pre_w_en_bar w_en vdd gnd pinv_8
Xinv_tri_en1 pre_tri_en_bar pre_tri_en1 vdd gnd pinv_7
Xtri_en_buf1 pre_tri_en1 pre_tri_en_bar1 vdd gnd pinv_7
Xtri_en_buf2 pre_tri_en_bar1 tri_en vdd gnd pinv_8
Xnand2_tri_en clk_buf_bar oe pre_tri_en_bar vdd gnd pnand2_1
Xtri_en_bar_buf1 pre_tri_en_bar pre_tri_en2 vdd gnd pinv_7
Xtri_en_bar_buf2 pre_tri_en2 tri_en_bar vdd gnd pinv_8
Xnand3_rblk_bar clk_buf_bar oe cs rblk_bar vdd gnd pnand3_1
Xinv_rblk rblk_bar rblk vdd gnd pinv_6
Xinv_s_en pre_s_en_bar s_en vdd gnd pinv_8
Xinv_pre_s_en_bar pre_s_en pre_s_en_bar vdd gnd pinv_7
Xreplica_bitline rblk pre_s_en vdd gnd replica_bitline
.ENDS control_logic

.SUBCKT dff_array din[0] din[1] din[2] din[3] dout[0] dout[1] dout[2] dout[3] clk vdd gnd
XXdff_r0_c0 din[0] dout[0] clk vdd gnd dff
XXdff_r1_c0 din[1] dout[1] clk vdd gnd dff
XXdff_r2_c0 din[2] dout[2] clk vdd gnd dff
XXdff_r3_c0 din[3] dout[3] clk vdd gnd dff
.ENDS dff_array

.SUBCKT bitcell_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] vdd gnd
Xbit_r0_c0 bl[0] br[0] wl[0] vdd gnd cell_6t
Xbit_r1_c0 bl[0] br[0] wl[1] vdd gnd cell_6t
Xbit_r2_c0 bl[0] br[0] wl[2] vdd gnd cell_6t
Xbit_r3_c0 bl[0] br[0] wl[3] vdd gnd cell_6t
Xbit_r4_c0 bl[0] br[0] wl[4] vdd gnd cell_6t
Xbit_r5_c0 bl[0] br[0] wl[5] vdd gnd cell_6t
Xbit_r6_c0 bl[0] br[0] wl[6] vdd gnd cell_6t
Xbit_r7_c0 bl[0] br[0] wl[7] vdd gnd cell_6t
Xbit_r8_c0 bl[0] br[0] wl[8] vdd gnd cell_6t
Xbit_r9_c0 bl[0] br[0] wl[9] vdd gnd cell_6t
Xbit_r10_c0 bl[0] br[0] wl[10] vdd gnd cell_6t
Xbit_r11_c0 bl[0] br[0] wl[11] vdd gnd cell_6t
Xbit_r12_c0 bl[0] br[0] wl[12] vdd gnd cell_6t
Xbit_r13_c0 bl[0] br[0] wl[13] vdd gnd cell_6t
Xbit_r14_c0 bl[0] br[0] wl[14] vdd gnd cell_6t
Xbit_r15_c0 bl[0] br[0] wl[15] vdd gnd cell_6t
Xbit_r0_c1 bl[1] br[1] wl[0] vdd gnd cell_6t
Xbit_r1_c1 bl[1] br[1] wl[1] vdd gnd cell_6t
Xbit_r2_c1 bl[1] br[1] wl[2] vdd gnd cell_6t
Xbit_r3_c1 bl[1] br[1] wl[3] vdd gnd cell_6t
Xbit_r4_c1 bl[1] br[1] wl[4] vdd gnd cell_6t
Xbit_r5_c1 bl[1] br[1] wl[5] vdd gnd cell_6t
Xbit_r6_c1 bl[1] br[1] wl[6] vdd gnd cell_6t
Xbit_r7_c1 bl[1] br[1] wl[7] vdd gnd cell_6t
Xbit_r8_c1 bl[1] br[1] wl[8] vdd gnd cell_6t
Xbit_r9_c1 bl[1] br[1] wl[9] vdd gnd cell_6t
Xbit_r10_c1 bl[1] br[1] wl[10] vdd gnd cell_6t
Xbit_r11_c1 bl[1] br[1] wl[11] vdd gnd cell_6t
Xbit_r12_c1 bl[1] br[1] wl[12] vdd gnd cell_6t
Xbit_r13_c1 bl[1] br[1] wl[13] vdd gnd cell_6t
Xbit_r14_c1 bl[1] br[1] wl[14] vdd gnd cell_6t
Xbit_r15_c1 bl[1] br[1] wl[15] vdd gnd cell_6t
Xbit_r0_c2 bl[2] br[2] wl[0] vdd gnd cell_6t
Xbit_r1_c2 bl[2] br[2] wl[1] vdd gnd cell_6t
Xbit_r2_c2 bl[2] br[2] wl[2] vdd gnd cell_6t
Xbit_r3_c2 bl[2] br[2] wl[3] vdd gnd cell_6t
Xbit_r4_c2 bl[2] br[2] wl[4] vdd gnd cell_6t
Xbit_r5_c2 bl[2] br[2] wl[5] vdd gnd cell_6t
Xbit_r6_c2 bl[2] br[2] wl[6] vdd gnd cell_6t
Xbit_r7_c2 bl[2] br[2] wl[7] vdd gnd cell_6t
Xbit_r8_c2 bl[2] br[2] wl[8] vdd gnd cell_6t
Xbit_r9_c2 bl[2] br[2] wl[9] vdd gnd cell_6t
Xbit_r10_c2 bl[2] br[2] wl[10] vdd gnd cell_6t
Xbit_r11_c2 bl[2] br[2] wl[11] vdd gnd cell_6t
Xbit_r12_c2 bl[2] br[2] wl[12] vdd gnd cell_6t
Xbit_r13_c2 bl[2] br[2] wl[13] vdd gnd cell_6t
Xbit_r14_c2 bl[2] br[2] wl[14] vdd gnd cell_6t
Xbit_r15_c2 bl[2] br[2] wl[15] vdd gnd cell_6t
Xbit_r0_c3 bl[3] br[3] wl[0] vdd gnd cell_6t
Xbit_r1_c3 bl[3] br[3] wl[1] vdd gnd cell_6t
Xbit_r2_c3 bl[3] br[3] wl[2] vdd gnd cell_6t
Xbit_r3_c3 bl[3] br[3] wl[3] vdd gnd cell_6t
Xbit_r4_c3 bl[3] br[3] wl[4] vdd gnd cell_6t
Xbit_r5_c3 bl[3] br[3] wl[5] vdd gnd cell_6t
Xbit_r6_c3 bl[3] br[3] wl[6] vdd gnd cell_6t
Xbit_r7_c3 bl[3] br[3] wl[7] vdd gnd cell_6t
Xbit_r8_c3 bl[3] br[3] wl[8] vdd gnd cell_6t
Xbit_r9_c3 bl[3] br[3] wl[9] vdd gnd cell_6t
Xbit_r10_c3 bl[3] br[3] wl[10] vdd gnd cell_6t
Xbit_r11_c3 bl[3] br[3] wl[11] vdd gnd cell_6t
Xbit_r12_c3 bl[3] br[3] wl[12] vdd gnd cell_6t
Xbit_r13_c3 bl[3] br[3] wl[13] vdd gnd cell_6t
Xbit_r14_c3 bl[3] br[3] wl[14] vdd gnd cell_6t
Xbit_r15_c3 bl[3] br[3] wl[15] vdd gnd cell_6t
.ENDS bitcell_array

* ptx M{0} {1} p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p

.SUBCKT precharge bl br en vdd
Mlower_pmos bl en br vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mupper_pmos1 bl en vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mupper_pmos2 br en vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
.ENDS precharge

.SUBCKT precharge_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] en vdd
Xpre_column_0 bl[0] br[0] en vdd precharge
Xpre_column_1 bl[1] br[1] en vdd precharge
Xpre_column_2 bl[2] br[2] en vdd precharge
Xpre_column_3 bl[3] br[3] en vdd precharge
.ENDS precharge_array
*********************** "sense_amp" ******************************

.SUBCKT sense_amp bl br dout en vdd gnd
M_1 dout net_1 vdd vdd p W='5.4*1u' L=0.6u
M_2 dout net_1 net_2 gnd n W='2.7*1u' L=0.6u
M_3 net_1 dout vdd vdd p W='5.4*1u' L=0.6u
M_4 net_1 dout net_2 gnd n W='2.7*1u' L=0.6u
M_5 bl en dout vdd p W='7.2*1u' L=0.6u
M_6 br en net_1 vdd p W='7.2*1u' L=0.6u
M_7 net_2 en gnd gnd n W='2.7*1u' L=0.6u
.ENDS	 sense_amp


.SUBCKT sense_amp_array data[0] bl[0] br[0] data[1] bl[1] br[1] data[2] bl[2] br[2] data[3] bl[3] br[3] en vdd gnd
Xsa_d0 bl[0] br[0] data[0] en vdd gnd sense_amp
Xsa_d1 bl[1] br[1] data[1] en vdd gnd sense_amp
Xsa_d2 bl[2] br[2] data[2] en vdd gnd sense_amp
Xsa_d3 bl[3] br[3] data[3] en vdd gnd sense_amp
.ENDS sense_amp_array
*********************** Write_Driver ******************************
.SUBCKT write_driver din bl br en vdd gnd

**** Inverter to conver Data_in to data_in_bar ******
M_1 net_3 din gnd gnd n W='1.2*1u' L=0.6u
M_2 net_3 din vdd vdd p W='2.1*1u' L=0.6u

**** 2input nand gate follwed by inverter to drive BL ******
M_3 net_2 en net_7 gnd n W='2.1*1u' L=0.6u
M_4 net_7 din gnd gnd n W='2.1*1u' L=0.6u
M_5 net_2 en vdd vdd p W='2.1*1u' L=0.6u
M_6 net_2 din vdd vdd p W='2.1*1u' L=0.6u


M_7 net_1 net_2 vdd vdd p W='2.1*1u' L=0.6u
M_8 net_1 net_2 gnd gnd n W='1.2*1u' L=0.6u

**** 2input nand gate follwed by inverter to drive BR******

M_9 net_4 en vdd vdd p W='2.1*1u' L=0.6u
M_10 net_4 en net_8 gnd n W='2.1*1u' L=0.6u
M_11 net_8 net_3 gnd gnd n W='2.1*1u' L=0.6u
M_12 net_4 net_3 vdd vdd p W='2.1*1u' L=0.6u

M_13 net_6 net_4 vdd vdd p W='2.1*1u' L=0.6u
M_14 net_6 net_4 gnd gnd n W='1.2*1u' L=0.6u

************************************************

M_15 bl net_6 net_5 gnd n W='3.6*1u' L=0.6u
M_16 br net_1 net_5 gnd n W='3.6*1u' L=0.6u
M_17 net_5 en gnd gnd n W='3.6*1u' L=0.6u



.ENDS	$ write_driver


.SUBCKT write_driver_array data[0] data[1] data[2] data[3] bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] en vdd gnd
XXwrite_driver0 data[0] bl[0] br[0] en vdd gnd write_driver
XXwrite_driver1 data[1] bl[1] br[1] en vdd gnd write_driver
XXwrite_driver2 data[2] bl[2] br[2] en vdd gnd write_driver
XXwrite_driver3 data[3] bl[3] br[3] en vdd gnd write_driver
.ENDS write_driver_array

.SUBCKT pinv_11 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.5999999999999996u ps=3.5999999999999996u as=1.7999999999999998p ad=1.7999999999999998p
.ENDS pinv_11

.SUBCKT pnand2_2 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
.ENDS pnand2_2

.SUBCKT pnand3_2 A B C Z vdd gnd
Mpnand3_pmos1 vdd A Z vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand3_pmos2 Z B vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand3_pmos3 Z C vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand3_nmos1 Z C net1 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand3_nmos2 net1 B net2 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand3_nmos3 net2 A gnd gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
.ENDS pnand3_2

.SUBCKT pinv_12 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.5999999999999996u ps=3.5999999999999996u as=1.7999999999999998p ad=1.7999999999999998p
.ENDS pinv_12

.SUBCKT pnand2_3 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
.ENDS pnand2_3

.SUBCKT pre2x4 in[0] in[1] out[0] out[1] out[2] out[3] vdd gnd
XXpre_inv[0] in[0] inbar[0] vdd gnd pinv_12
XXpre_inv[1] in[1] inbar[1] vdd gnd pinv_12
XXpre_nand_inv[0] Z[0] out[0] vdd gnd pinv_12
XXpre_nand_inv[1] Z[1] out[1] vdd gnd pinv_12
XXpre_nand_inv[2] Z[2] out[2] vdd gnd pinv_12
XXpre_nand_inv[3] Z[3] out[3] vdd gnd pinv_12
XXpre2x4_nand[0] inbar[0] inbar[1] Z[0] vdd gnd pnand2_3
XXpre2x4_nand[1] in[0] inbar[1] Z[1] vdd gnd pnand2_3
XXpre2x4_nand[2] inbar[0] in[1] Z[2] vdd gnd pnand2_3
XXpre2x4_nand[3] in[0] in[1] Z[3] vdd gnd pnand2_3
.ENDS pre2x4

.SUBCKT pinv_13 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.5999999999999996u ps=3.5999999999999996u as=1.7999999999999998p ad=1.7999999999999998p
.ENDS pinv_13

.SUBCKT pnand3_3 A B C Z vdd gnd
Mpnand3_pmos1 vdd A Z vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand3_pmos2 Z B vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand3_pmos3 Z C vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand3_nmos1 Z C net1 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand3_nmos2 net1 B net2 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand3_nmos3 net2 A gnd gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
.ENDS pnand3_3

.SUBCKT pre3x8 in[0] in[1] in[2] out[0] out[1] out[2] out[3] out[4] out[5] out[6] out[7] vdd gnd
XXpre_inv[0] in[0] inbar[0] vdd gnd pinv_13
XXpre_inv[1] in[1] inbar[1] vdd gnd pinv_13
XXpre_inv[2] in[2] inbar[2] vdd gnd pinv_13
XXpre_nand_inv[0] Z[0] out[0] vdd gnd pinv_13
XXpre_nand_inv[1] Z[1] out[1] vdd gnd pinv_13
XXpre_nand_inv[2] Z[2] out[2] vdd gnd pinv_13
XXpre_nand_inv[3] Z[3] out[3] vdd gnd pinv_13
XXpre_nand_inv[4] Z[4] out[4] vdd gnd pinv_13
XXpre_nand_inv[5] Z[5] out[5] vdd gnd pinv_13
XXpre_nand_inv[6] Z[6] out[6] vdd gnd pinv_13
XXpre_nand_inv[7] Z[7] out[7] vdd gnd pinv_13
XXpre3x8_nand[0] inbar[0] inbar[1] inbar[2] Z[0] vdd gnd pnand3_3
XXpre3x8_nand[1] in[0] inbar[1] inbar[2] Z[1] vdd gnd pnand3_3
XXpre3x8_nand[2] inbar[0] in[1] inbar[2] Z[2] vdd gnd pnand3_3
XXpre3x8_nand[3] in[0] in[1] inbar[2] Z[3] vdd gnd pnand3_3
XXpre3x8_nand[4] inbar[0] inbar[1] in[2] Z[4] vdd gnd pnand3_3
XXpre3x8_nand[5] in[0] inbar[1] in[2] Z[5] vdd gnd pnand3_3
XXpre3x8_nand[6] inbar[0] in[1] in[2] Z[6] vdd gnd pnand3_3
XXpre3x8_nand[7] in[0] in[1] in[2] Z[7] vdd gnd pnand3_3
.ENDS pre3x8

.SUBCKT hierarchical_decoder_16rows A[0] A[1] A[2] A[3] decode[0] decode[1] decode[2] decode[3] decode[4] decode[5] decode[6] decode[7] decode[8] decode[9] decode[10] decode[11] decode[12] decode[13] decode[14] decode[15] vdd gnd
Xpre[0] A[0] A[1] out[0] out[1] out[2] out[3] vdd gnd pre2x4
Xpre[1] A[2] A[3] out[4] out[5] out[6] out[7] vdd gnd pre2x4
XDEC_NAND[0] out[0] out[4] Z[0] vdd gnd pnand2_2
XDEC_NAND[1] out[0] out[5] Z[1] vdd gnd pnand2_2
XDEC_NAND[2] out[0] out[6] Z[2] vdd gnd pnand2_2
XDEC_NAND[3] out[0] out[7] Z[3] vdd gnd pnand2_2
XDEC_NAND[4] out[1] out[4] Z[4] vdd gnd pnand2_2
XDEC_NAND[5] out[1] out[5] Z[5] vdd gnd pnand2_2
XDEC_NAND[6] out[1] out[6] Z[6] vdd gnd pnand2_2
XDEC_NAND[7] out[1] out[7] Z[7] vdd gnd pnand2_2
XDEC_NAND[8] out[2] out[4] Z[8] vdd gnd pnand2_2
XDEC_NAND[9] out[2] out[5] Z[9] vdd gnd pnand2_2
XDEC_NAND[10] out[2] out[6] Z[10] vdd gnd pnand2_2
XDEC_NAND[11] out[2] out[7] Z[11] vdd gnd pnand2_2
XDEC_NAND[12] out[3] out[4] Z[12] vdd gnd pnand2_2
XDEC_NAND[13] out[3] out[5] Z[13] vdd gnd pnand2_2
XDEC_NAND[14] out[3] out[6] Z[14] vdd gnd pnand2_2
XDEC_NAND[15] out[3] out[7] Z[15] vdd gnd pnand2_2
XDEC_INV_[0] Z[0] decode[0] vdd gnd pinv_11
XDEC_INV_[1] Z[1] decode[1] vdd gnd pinv_11
XDEC_INV_[2] Z[2] decode[2] vdd gnd pinv_11
XDEC_INV_[3] Z[3] decode[3] vdd gnd pinv_11
XDEC_INV_[4] Z[4] decode[4] vdd gnd pinv_11
XDEC_INV_[5] Z[5] decode[5] vdd gnd pinv_11
XDEC_INV_[6] Z[6] decode[6] vdd gnd pinv_11
XDEC_INV_[7] Z[7] decode[7] vdd gnd pinv_11
XDEC_INV_[8] Z[8] decode[8] vdd gnd pinv_11
XDEC_INV_[9] Z[9] decode[9] vdd gnd pinv_11
XDEC_INV_[10] Z[10] decode[10] vdd gnd pinv_11
XDEC_INV_[11] Z[11] decode[11] vdd gnd pinv_11
XDEC_INV_[12] Z[12] decode[12] vdd gnd pinv_11
XDEC_INV_[13] Z[13] decode[13] vdd gnd pinv_11
XDEC_INV_[14] Z[14] decode[14] vdd gnd pinv_11
XDEC_INV_[15] Z[15] decode[15] vdd gnd pinv_11
.ENDS hierarchical_decoder_16rows
*********************** tri_gate ******************************

.SUBCKT tri_gate in out en en_bar vdd gnd

M_1 net_2 in_inv gnd gnd n W='1.2*1u' L=0.6u
M_2 net_3 in_inv vdd vdd p W='2.4*1u' L=0.6u
M_3 out en_bar net_3 vdd p W='2.4*1u' L=0.6u
M_4 out en net_2 gnd n W='1.2*1u' L=0.6u
M_5 in_inv in vdd vdd p W='2.4*1u' L=0.6u
M_6 in_inv in gnd gnd n W='1.2*1u' L=0.6u


.ENDS	

.SUBCKT tri_gate_array in[0] in[1] in[2] in[3] out[0] out[1] out[2] out[3] en en_bar vdd gnd
XXtri_gate0 in[0] out[0] en en_bar vdd gnd tri_gate
XXtri_gate1 in[1] out[1] en en_bar vdd gnd tri_gate
XXtri_gate2 in[2] out[2] en en_bar vdd gnd tri_gate
XXtri_gate3 in[3] out[3] en en_bar vdd gnd tri_gate
.ENDS tri_gate_array

.SUBCKT pinv_14 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.5999999999999996u ps=3.5999999999999996u as=1.7999999999999998p ad=1.7999999999999998p
.ENDS pinv_14

.SUBCKT pinv_15 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.5999999999999996u ps=3.5999999999999996u as=1.7999999999999998p ad=1.7999999999999998p
.ENDS pinv_15

.SUBCKT pnand2_4 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
.ENDS pnand2_4

.SUBCKT wordline_driver in[0] in[1] in[2] in[3] in[4] in[5] in[6] in[7] in[8] in[9] in[10] in[11] in[12] in[13] in[14] in[15] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] en vdd gnd
Xwl_driver_inv_en0 en en_bar[0] vdd gnd pinv_15
Xwl_driver_nand0 en_bar[0] in[0] net[0] vdd gnd pnand2_4
Xwl_driver_inv0 net[0] wl[0] vdd gnd pinv_14
Xwl_driver_inv_en1 en en_bar[1] vdd gnd pinv_15
Xwl_driver_nand1 en_bar[1] in[1] net[1] vdd gnd pnand2_4
Xwl_driver_inv1 net[1] wl[1] vdd gnd pinv_14
Xwl_driver_inv_en2 en en_bar[2] vdd gnd pinv_15
Xwl_driver_nand2 en_bar[2] in[2] net[2] vdd gnd pnand2_4
Xwl_driver_inv2 net[2] wl[2] vdd gnd pinv_14
Xwl_driver_inv_en3 en en_bar[3] vdd gnd pinv_15
Xwl_driver_nand3 en_bar[3] in[3] net[3] vdd gnd pnand2_4
Xwl_driver_inv3 net[3] wl[3] vdd gnd pinv_14
Xwl_driver_inv_en4 en en_bar[4] vdd gnd pinv_15
Xwl_driver_nand4 en_bar[4] in[4] net[4] vdd gnd pnand2_4
Xwl_driver_inv4 net[4] wl[4] vdd gnd pinv_14
Xwl_driver_inv_en5 en en_bar[5] vdd gnd pinv_15
Xwl_driver_nand5 en_bar[5] in[5] net[5] vdd gnd pnand2_4
Xwl_driver_inv5 net[5] wl[5] vdd gnd pinv_14
Xwl_driver_inv_en6 en en_bar[6] vdd gnd pinv_15
Xwl_driver_nand6 en_bar[6] in[6] net[6] vdd gnd pnand2_4
Xwl_driver_inv6 net[6] wl[6] vdd gnd pinv_14
Xwl_driver_inv_en7 en en_bar[7] vdd gnd pinv_15
Xwl_driver_nand7 en_bar[7] in[7] net[7] vdd gnd pnand2_4
Xwl_driver_inv7 net[7] wl[7] vdd gnd pinv_14
Xwl_driver_inv_en8 en en_bar[8] vdd gnd pinv_15
Xwl_driver_nand8 en_bar[8] in[8] net[8] vdd gnd pnand2_4
Xwl_driver_inv8 net[8] wl[8] vdd gnd pinv_14
Xwl_driver_inv_en9 en en_bar[9] vdd gnd pinv_15
Xwl_driver_nand9 en_bar[9] in[9] net[9] vdd gnd pnand2_4
Xwl_driver_inv9 net[9] wl[9] vdd gnd pinv_14
Xwl_driver_inv_en10 en en_bar[10] vdd gnd pinv_15
Xwl_driver_nand10 en_bar[10] in[10] net[10] vdd gnd pnand2_4
Xwl_driver_inv10 net[10] wl[10] vdd gnd pinv_14
Xwl_driver_inv_en11 en en_bar[11] vdd gnd pinv_15
Xwl_driver_nand11 en_bar[11] in[11] net[11] vdd gnd pnand2_4
Xwl_driver_inv11 net[11] wl[11] vdd gnd pinv_14
Xwl_driver_inv_en12 en en_bar[12] vdd gnd pinv_15
Xwl_driver_nand12 en_bar[12] in[12] net[12] vdd gnd pnand2_4
Xwl_driver_inv12 net[12] wl[12] vdd gnd pinv_14
Xwl_driver_inv_en13 en en_bar[13] vdd gnd pinv_15
Xwl_driver_nand13 en_bar[13] in[13] net[13] vdd gnd pnand2_4
Xwl_driver_inv13 net[13] wl[13] vdd gnd pinv_14
Xwl_driver_inv_en14 en en_bar[14] vdd gnd pinv_15
Xwl_driver_nand14 en_bar[14] in[14] net[14] vdd gnd pnand2_4
Xwl_driver_inv14 net[14] wl[14] vdd gnd pinv_14
Xwl_driver_inv_en15 en en_bar[15] vdd gnd pinv_15
Xwl_driver_nand15 en_bar[15] in[15] net[15] vdd gnd pnand2_4
Xwl_driver_inv15 net[15] wl[15] vdd gnd pinv_14
.ENDS wordline_driver

.SUBCKT pinv_16 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.5999999999999996p ad=3.5999999999999996p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.5999999999999996u ps=3.5999999999999996u as=1.7999999999999998p ad=1.7999999999999998p
.ENDS pinv_16

.SUBCKT bank DOUT[0] DOUT[1] DOUT[2] DOUT[3] DIN[0] DIN[1] DIN[2] DIN[3] A[0] A[1] A[2] A[3] s_en w_en tri_en_bar tri_en clk_buf_bar clk_buf vdd gnd
Xbitcell_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] vdd gnd bitcell_array
Xprecharge_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] clk_buf_bar vdd precharge_array
Xsense_amp_array sa_out[0] bl[0] br[0] sa_out[1] bl[1] br[1] sa_out[2] bl[2] br[2] sa_out[3] bl[3] br[3] s_en vdd gnd sense_amp_array
Xwrite_driver_array DIN[0] DIN[1] DIN[2] DIN[3] bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] w_en vdd gnd write_driver_array
Xtri_gate_array sa_out[0] sa_out[1] sa_out[2] sa_out[3] DOUT[0] DOUT[1] DOUT[2] DOUT[3] tri_en tri_en_bar vdd gnd tri_gate_array
Xrow_decoder A[0] A[1] A[2] A[3] dec_out[0] dec_out[1] dec_out[2] dec_out[3] dec_out[4] dec_out[5] dec_out[6] dec_out[7] dec_out[8] dec_out[9] dec_out[10] dec_out[11] dec_out[12] dec_out[13] dec_out[14] dec_out[15] vdd gnd hierarchical_decoder_16rows
Xwordline_driver dec_out[0] dec_out[1] dec_out[2] dec_out[3] dec_out[4] dec_out[5] dec_out[6] dec_out[7] dec_out[8] dec_out[9] dec_out[10] dec_out[11] dec_out[12] dec_out[13] dec_out[14] dec_out[15] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] clk_buf vdd gnd wordline_driver
.ENDS bank

.SUBCKT sram1 DIN[0] DIN[1] DIN[2] DIN[3] ADDR[0] ADDR[1] ADDR[2] ADDR[3] csb web oeb clk DOUT[0] DOUT[1] DOUT[2] DOUT[3] vdd gnd
Xbank0 DOUT[0] DOUT[1] DOUT[2] DOUT[3] DIN[0] DIN[1] DIN[2] DIN[3] A[0] A[1] A[2] A[3] s_en w_en tri_en_bar tri_en clk_buf_bar clk_buf vdd gnd bank
Xcontrol csb_s web_s oeb_s clk s_en w_en tri_en tri_en_bar clk_buf_bar clk_buf vdd gnd control_logic
Xaddress ADDR[0] ADDR[1] ADDR[2] ADDR[3] A[0] A[1] A[2] A[3] clk_buf vdd gnd dff_array
Xaddress ADDR[0] ADDR[1] ADDR[2] ADDR[3] A[0] A[1] A[2] A[3] clk_buf vdd gnd dff_array
.ENDS sram1
