**************************************************
* OpenRAM generated memory.
* Words: 256
* Data bits: 32
* Banks: 1
* Column mux: 4:1
**************************************************

* ptx M{0} {1} n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p

* ptx M{0} {1} p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p

.SUBCKT pnand2_1 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
.ENDS pnand2_1

.SUBCKT pnand3_1 A B C Z vdd gnd
Mpnand3_pmos1 vdd A Z vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand3_pmos2 Z B vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand3_pmos3 Z C vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand3_nmos1 Z C net1 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand3_nmos2 net1 B net2 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand3_nmos3 net2 A gnd gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
.ENDS pnand3_1

* ptx M{0} {1} n m=1 w=1.2u l=0.6u pd=3.6u ps=3.6u as=1.8p ad=1.8p

* ptx M{0} {1} p m=1 w=3.6u l=0.6u pd=8.4u ps=8.4u as=5.4p ad=5.4p

.SUBCKT pnor2_1 A B Z vdd gnd
Mpnor2_pmos1 vdd A net1 vdd p m=1 w=3.6u l=0.6u pd=8.4u ps=8.4u as=5.4p ad=5.4p
Mpnor2_pmos2 net1 B Z vdd p m=1 w=3.6u l=0.6u pd=8.4u ps=8.4u as=5.4p ad=5.4p
Mpnor2_nmos1 Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.6u ps=3.6u as=1.8p ad=1.8p
Mpnor2_nmos2 Z B gnd gnd n m=1 w=1.2u l=0.6u pd=3.6u ps=3.6u as=1.8p ad=1.8p
.ENDS pnor2_1

.SUBCKT pinv_1 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.6u ps=3.6u as=1.8p ad=1.8p
.ENDS pinv_1

* ptx M{0} {1} n m=2 w=1.2u l=0.6u pd=3.6u ps=3.6u as=1.8p ad=1.8p

* ptx M{0} {1} p m=2 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p

.SUBCKT pinv_2 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=2 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpinv_nmos Z A gnd gnd n m=2 w=1.2u l=0.6u pd=3.6u ps=3.6u as=1.8p ad=1.8p
.ENDS pinv_2

* ptx M{0} {1} n m=3 w=1.65u l=0.6u pd=4.5u ps=4.5u as=2.475p ad=2.475p

* ptx M{0} {1} p m=3 w=3.15u l=0.6u pd=7.5u ps=7.5u as=4.725p ad=4.725p

.SUBCKT pinv_3 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=3 w=3.15u l=0.6u pd=7.5u ps=7.5u as=4.725p ad=4.725p
Mpinv_nmos Z A gnd gnd n m=3 w=1.65u l=0.6u pd=4.5u ps=4.5u as=2.475p ad=2.475p
.ENDS pinv_3

* ptx M{0} {1} n m=5 w=1.95u l=0.6u pd=5.1u ps=5.1u as=2.925p ad=2.925p

* ptx M{0} {1} p m=5 w=3.9u l=0.6u pd=9.0u ps=9.0u as=5.85p ad=5.85p

.SUBCKT pinv_4 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=5 w=3.9u l=0.6u pd=9.0u ps=9.0u as=5.85p ad=5.85p
Mpinv_nmos Z A gnd gnd n m=5 w=1.95u l=0.6u pd=5.1u ps=5.1u as=2.925p ad=2.925p
.ENDS pinv_4

* ptx M{0} {1} n m=10 w=1.95u l=0.6u pd=5.1u ps=5.1u as=2.925p ad=2.925p

* ptx M{0} {1} p m=10 w=3.9u l=0.6u pd=9.0u ps=9.0u as=5.85p ad=5.85p

.SUBCKT pinv_5 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=10 w=3.9u l=0.6u pd=9.0u ps=9.0u as=5.85p ad=5.85p
Mpinv_nmos Z A gnd gnd n m=10 w=1.95u l=0.6u pd=5.1u ps=5.1u as=2.925p ad=2.925p
.ENDS pinv_5
*master-slave flip-flop with both output and inverted ouput

.subckt ms_flop din dout dout_bar clk vdd gnd
xmaster din mout mout_bar clk clk_bar vdd gnd dlatch
xslave mout_bar dout_bar dout clk_bar clk_nn vdd gnd dlatch
.ends flop

.subckt dlatch din dout dout_bar clk clk_bar vdd gnd
*clk inverter
mPff1 clk_bar clk vdd vdd p W=1.8u L=0.6u m=1
mNff1 clk_bar clk gnd gnd n W=0.9u L=0.6u m=1

*transmission gate 1
mtmP1 din clk int1 vdd p W=1.8u L=0.6u m=1
mtmN1 din clk_bar int1 gnd n W=0.9u L=0.6u m=1

*foward inverter
mPff3 dout_bar int1 vdd vdd p W=1.8u L=0.6u m=1
mNff3 dout_bar int1 gnd gnd n W=0.9u L=0.6u m=1

*backward inverter
mPff4 dout dout_bar vdd vdd p W=1.8u L=0.6u m=1
mNf4 dout dout_bar gnd gnd n W=0.9u L=0.6u m=1

*transmission gate 2
mtmP2 int1 clk_bar dout vdd p W=1.8u L=0.6u m=1
mtmN2 int1 clk dout gnd n W=0.9u L=0.6u m=1
.ends dlatch


.SUBCKT msf_control din[0] din[1] din[2] dout[0] dout_bar[0] dout[1] dout_bar[1] dout[2] dout_bar[2] clk vdd gnd
XXdff0 din[0] dout[0] dout_bar[0] clk vdd gnd ms_flop
XXdff1 din[1] dout[1] dout_bar[1] clk vdd gnd ms_flop
XXdff2 din[2] dout[2] dout_bar[2] clk vdd gnd ms_flop
.ENDS msf_control

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

.SUBCKT bitline_load bl[0] br[0] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] vdd gnd
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
.ENDS bitline_load

.SUBCKT pinv_6 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.6u ps=3.6u as=1.8p ad=1.8p
.ENDS pinv_6

.SUBCKT delay_chain in out vdd gnd
Xdinv0 in s1 vdd gnd pinv_6
Xdinv1 s1 s2n1 vdd gnd pinv_6
Xdinv2 s1 s2n2 vdd gnd pinv_6
Xdinv3 s1 s2 vdd gnd pinv_6
Xdinv4 s2 s3n1 vdd gnd pinv_6
Xdinv5 s2 s3n2 vdd gnd pinv_6
Xdinv6 s2 s3 vdd gnd pinv_6
Xdinv7 s3 s4n1 vdd gnd pinv_6
Xdinv8 s3 s4n2 vdd gnd pinv_6
Xdinv9 s3 s4 vdd gnd pinv_6
Xdinv10 s4 s5n1 vdd gnd pinv_6
Xdinv11 s4 s5n2 vdd gnd pinv_6
Xdinv12 s4 out vdd gnd pinv_6
.ENDS delay_chain

.SUBCKT pinv_7 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.6u ps=3.6u as=1.8p ad=1.8p
.ENDS pinv_7

* ptx M{0} {1} p m=1 w=1.2u l=0.6u pd=3.6u ps=3.6u as=1.8p ad=1.8p

.SUBCKT replica_bitline en out vdd gnd
Xrbl_inv bl[0] out vdd gnd pinv_7
Mrbl_access_tx vdd delayed_en bl[0] vdd p m=1 w=1.2u l=0.6u pd=3.6u ps=3.6u as=1.8p ad=1.8p
Xdelay_chain en delayed_en vdd gnd delay_chain
Xbitcell bl[0] br[0] delayed_en vdd gnd replica_cell_6t
Xload bl[0] br[0] gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd gnd vdd gnd bitline_load
.ENDS replica_bitline

.SUBCKT control_logic csb web oeb clk s_en w_en tri_en tri_en_bar clk_bar clk_buf vdd gnd
Xmsf_control oeb csb web oe_bar oe cs_bar cs we_bar we clk_buf vdd gnd msf_control
Xinv_clk1_bar clk clk1_bar vdd gnd pinv_2
Xinv_clk2 clk1_bar clk2 vdd gnd pinv_3
Xinv_clk_bar clk2 clk_bar vdd gnd pinv_4
Xinv_clk_buf clk_bar clk_buf vdd gnd pinv_5
Xnand3_rblk_bar clk_bar oe cs rblk_bar vdd gnd pnand3_1
Xinv_rblk rblk_bar rblk vdd gnd pinv_1
Xnor2_tri_en clk_buf oe_bar tri_en vdd gnd pnor2_1
Xnand2_tri_en clk_bar oe tri_en_bar vdd gnd pnand2_1
Xinv_s_en pre_s_en_bar s_en vdd gnd pinv_1
Xinv_pre_s_en_bar pre_s_en pre_s_en_bar vdd gnd pinv_1
Xnand3_w_en_bar clk_bar cs we w_en_bar vdd gnd pnand3_1
Xinv_pre_w_en w_en_bar pre_w_en vdd gnd pinv_1
Xinv_pre_w_en_bar pre_w_en pre_w_en_bar vdd gnd pinv_1
Xinv_w_en2 pre_w_en_bar w_en vdd gnd pinv_1
Xreplica_bitline rblk pre_s_en vdd gnd replica_bitline
.ENDS control_logic

.SUBCKT bitcell_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] bl[8] br[8] bl[9] br[9] bl[10] br[10] bl[11] br[11] bl[12] br[12] bl[13] br[13] bl[14] br[14] bl[15] br[15] bl[16] br[16] bl[17] br[17] bl[18] br[18] bl[19] br[19] bl[20] br[20] bl[21] br[21] bl[22] br[22] bl[23] br[23] bl[24] br[24] bl[25] br[25] bl[26] br[26] bl[27] br[27] bl[28] br[28] bl[29] br[29] bl[30] br[30] bl[31] br[31] bl[32] br[32] bl[33] br[33] bl[34] br[34] bl[35] br[35] bl[36] br[36] bl[37] br[37] bl[38] br[38] bl[39] br[39] bl[40] br[40] bl[41] br[41] bl[42] br[42] bl[43] br[43] bl[44] br[44] bl[45] br[45] bl[46] br[46] bl[47] br[47] bl[48] br[48] bl[49] br[49] bl[50] br[50] bl[51] br[51] bl[52] br[52] bl[53] br[53] bl[54] br[54] bl[55] br[55] bl[56] br[56] bl[57] br[57] bl[58] br[58] bl[59] br[59] bl[60] br[60] bl[61] br[61] bl[62] br[62] bl[63] br[63] bl[64] br[64] bl[65] br[65] bl[66] br[66] bl[67] br[67] bl[68] br[68] bl[69] br[69] bl[70] br[70] bl[71] br[71] bl[72] br[72] bl[73] br[73] bl[74] br[74] bl[75] br[75] bl[76] br[76] bl[77] br[77] bl[78] br[78] bl[79] br[79] bl[80] br[80] bl[81] br[81] bl[82] br[82] bl[83] br[83] bl[84] br[84] bl[85] br[85] bl[86] br[86] bl[87] br[87] bl[88] br[88] bl[89] br[89] bl[90] br[90] bl[91] br[91] bl[92] br[92] bl[93] br[93] bl[94] br[94] bl[95] br[95] bl[96] br[96] bl[97] br[97] bl[98] br[98] bl[99] br[99] bl[100] br[100] bl[101] br[101] bl[102] br[102] bl[103] br[103] bl[104] br[104] bl[105] br[105] bl[106] br[106] bl[107] br[107] bl[108] br[108] bl[109] br[109] bl[110] br[110] bl[111] br[111] bl[112] br[112] bl[113] br[113] bl[114] br[114] bl[115] br[115] bl[116] br[116] bl[117] br[117] bl[118] br[118] bl[119] br[119] bl[120] br[120] bl[121] br[121] bl[122] br[122] bl[123] br[123] bl[124] br[124] bl[125] br[125] bl[126] br[126] bl[127] br[127] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] wl[16] wl[17] wl[18] wl[19] wl[20] wl[21] wl[22] wl[23] wl[24] wl[25] wl[26] wl[27] wl[28] wl[29] wl[30] wl[31] wl[32] wl[33] wl[34] wl[35] wl[36] wl[37] wl[38] wl[39] wl[40] wl[41] wl[42] wl[43] wl[44] wl[45] wl[46] wl[47] wl[48] wl[49] wl[50] wl[51] wl[52] wl[53] wl[54] wl[55] wl[56] wl[57] wl[58] wl[59] wl[60] wl[61] wl[62] wl[63] vdd gnd
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
Xbit_r16_c0 bl[0] br[0] wl[16] vdd gnd cell_6t
Xbit_r17_c0 bl[0] br[0] wl[17] vdd gnd cell_6t
Xbit_r18_c0 bl[0] br[0] wl[18] vdd gnd cell_6t
Xbit_r19_c0 bl[0] br[0] wl[19] vdd gnd cell_6t
Xbit_r20_c0 bl[0] br[0] wl[20] vdd gnd cell_6t
Xbit_r21_c0 bl[0] br[0] wl[21] vdd gnd cell_6t
Xbit_r22_c0 bl[0] br[0] wl[22] vdd gnd cell_6t
Xbit_r23_c0 bl[0] br[0] wl[23] vdd gnd cell_6t
Xbit_r24_c0 bl[0] br[0] wl[24] vdd gnd cell_6t
Xbit_r25_c0 bl[0] br[0] wl[25] vdd gnd cell_6t
Xbit_r26_c0 bl[0] br[0] wl[26] vdd gnd cell_6t
Xbit_r27_c0 bl[0] br[0] wl[27] vdd gnd cell_6t
Xbit_r28_c0 bl[0] br[0] wl[28] vdd gnd cell_6t
Xbit_r29_c0 bl[0] br[0] wl[29] vdd gnd cell_6t
Xbit_r30_c0 bl[0] br[0] wl[30] vdd gnd cell_6t
Xbit_r31_c0 bl[0] br[0] wl[31] vdd gnd cell_6t
Xbit_r32_c0 bl[0] br[0] wl[32] vdd gnd cell_6t
Xbit_r33_c0 bl[0] br[0] wl[33] vdd gnd cell_6t
Xbit_r34_c0 bl[0] br[0] wl[34] vdd gnd cell_6t
Xbit_r35_c0 bl[0] br[0] wl[35] vdd gnd cell_6t
Xbit_r36_c0 bl[0] br[0] wl[36] vdd gnd cell_6t
Xbit_r37_c0 bl[0] br[0] wl[37] vdd gnd cell_6t
Xbit_r38_c0 bl[0] br[0] wl[38] vdd gnd cell_6t
Xbit_r39_c0 bl[0] br[0] wl[39] vdd gnd cell_6t
Xbit_r40_c0 bl[0] br[0] wl[40] vdd gnd cell_6t
Xbit_r41_c0 bl[0] br[0] wl[41] vdd gnd cell_6t
Xbit_r42_c0 bl[0] br[0] wl[42] vdd gnd cell_6t
Xbit_r43_c0 bl[0] br[0] wl[43] vdd gnd cell_6t
Xbit_r44_c0 bl[0] br[0] wl[44] vdd gnd cell_6t
Xbit_r45_c0 bl[0] br[0] wl[45] vdd gnd cell_6t
Xbit_r46_c0 bl[0] br[0] wl[46] vdd gnd cell_6t
Xbit_r47_c0 bl[0] br[0] wl[47] vdd gnd cell_6t
Xbit_r48_c0 bl[0] br[0] wl[48] vdd gnd cell_6t
Xbit_r49_c0 bl[0] br[0] wl[49] vdd gnd cell_6t
Xbit_r50_c0 bl[0] br[0] wl[50] vdd gnd cell_6t
Xbit_r51_c0 bl[0] br[0] wl[51] vdd gnd cell_6t
Xbit_r52_c0 bl[0] br[0] wl[52] vdd gnd cell_6t
Xbit_r53_c0 bl[0] br[0] wl[53] vdd gnd cell_6t
Xbit_r54_c0 bl[0] br[0] wl[54] vdd gnd cell_6t
Xbit_r55_c0 bl[0] br[0] wl[55] vdd gnd cell_6t
Xbit_r56_c0 bl[0] br[0] wl[56] vdd gnd cell_6t
Xbit_r57_c0 bl[0] br[0] wl[57] vdd gnd cell_6t
Xbit_r58_c0 bl[0] br[0] wl[58] vdd gnd cell_6t
Xbit_r59_c0 bl[0] br[0] wl[59] vdd gnd cell_6t
Xbit_r60_c0 bl[0] br[0] wl[60] vdd gnd cell_6t
Xbit_r61_c0 bl[0] br[0] wl[61] vdd gnd cell_6t
Xbit_r62_c0 bl[0] br[0] wl[62] vdd gnd cell_6t
Xbit_r63_c0 bl[0] br[0] wl[63] vdd gnd cell_6t
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
Xbit_r16_c1 bl[1] br[1] wl[16] vdd gnd cell_6t
Xbit_r17_c1 bl[1] br[1] wl[17] vdd gnd cell_6t
Xbit_r18_c1 bl[1] br[1] wl[18] vdd gnd cell_6t
Xbit_r19_c1 bl[1] br[1] wl[19] vdd gnd cell_6t
Xbit_r20_c1 bl[1] br[1] wl[20] vdd gnd cell_6t
Xbit_r21_c1 bl[1] br[1] wl[21] vdd gnd cell_6t
Xbit_r22_c1 bl[1] br[1] wl[22] vdd gnd cell_6t
Xbit_r23_c1 bl[1] br[1] wl[23] vdd gnd cell_6t
Xbit_r24_c1 bl[1] br[1] wl[24] vdd gnd cell_6t
Xbit_r25_c1 bl[1] br[1] wl[25] vdd gnd cell_6t
Xbit_r26_c1 bl[1] br[1] wl[26] vdd gnd cell_6t
Xbit_r27_c1 bl[1] br[1] wl[27] vdd gnd cell_6t
Xbit_r28_c1 bl[1] br[1] wl[28] vdd gnd cell_6t
Xbit_r29_c1 bl[1] br[1] wl[29] vdd gnd cell_6t
Xbit_r30_c1 bl[1] br[1] wl[30] vdd gnd cell_6t
Xbit_r31_c1 bl[1] br[1] wl[31] vdd gnd cell_6t
Xbit_r32_c1 bl[1] br[1] wl[32] vdd gnd cell_6t
Xbit_r33_c1 bl[1] br[1] wl[33] vdd gnd cell_6t
Xbit_r34_c1 bl[1] br[1] wl[34] vdd gnd cell_6t
Xbit_r35_c1 bl[1] br[1] wl[35] vdd gnd cell_6t
Xbit_r36_c1 bl[1] br[1] wl[36] vdd gnd cell_6t
Xbit_r37_c1 bl[1] br[1] wl[37] vdd gnd cell_6t
Xbit_r38_c1 bl[1] br[1] wl[38] vdd gnd cell_6t
Xbit_r39_c1 bl[1] br[1] wl[39] vdd gnd cell_6t
Xbit_r40_c1 bl[1] br[1] wl[40] vdd gnd cell_6t
Xbit_r41_c1 bl[1] br[1] wl[41] vdd gnd cell_6t
Xbit_r42_c1 bl[1] br[1] wl[42] vdd gnd cell_6t
Xbit_r43_c1 bl[1] br[1] wl[43] vdd gnd cell_6t
Xbit_r44_c1 bl[1] br[1] wl[44] vdd gnd cell_6t
Xbit_r45_c1 bl[1] br[1] wl[45] vdd gnd cell_6t
Xbit_r46_c1 bl[1] br[1] wl[46] vdd gnd cell_6t
Xbit_r47_c1 bl[1] br[1] wl[47] vdd gnd cell_6t
Xbit_r48_c1 bl[1] br[1] wl[48] vdd gnd cell_6t
Xbit_r49_c1 bl[1] br[1] wl[49] vdd gnd cell_6t
Xbit_r50_c1 bl[1] br[1] wl[50] vdd gnd cell_6t
Xbit_r51_c1 bl[1] br[1] wl[51] vdd gnd cell_6t
Xbit_r52_c1 bl[1] br[1] wl[52] vdd gnd cell_6t
Xbit_r53_c1 bl[1] br[1] wl[53] vdd gnd cell_6t
Xbit_r54_c1 bl[1] br[1] wl[54] vdd gnd cell_6t
Xbit_r55_c1 bl[1] br[1] wl[55] vdd gnd cell_6t
Xbit_r56_c1 bl[1] br[1] wl[56] vdd gnd cell_6t
Xbit_r57_c1 bl[1] br[1] wl[57] vdd gnd cell_6t
Xbit_r58_c1 bl[1] br[1] wl[58] vdd gnd cell_6t
Xbit_r59_c1 bl[1] br[1] wl[59] vdd gnd cell_6t
Xbit_r60_c1 bl[1] br[1] wl[60] vdd gnd cell_6t
Xbit_r61_c1 bl[1] br[1] wl[61] vdd gnd cell_6t
Xbit_r62_c1 bl[1] br[1] wl[62] vdd gnd cell_6t
Xbit_r63_c1 bl[1] br[1] wl[63] vdd gnd cell_6t
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
Xbit_r16_c2 bl[2] br[2] wl[16] vdd gnd cell_6t
Xbit_r17_c2 bl[2] br[2] wl[17] vdd gnd cell_6t
Xbit_r18_c2 bl[2] br[2] wl[18] vdd gnd cell_6t
Xbit_r19_c2 bl[2] br[2] wl[19] vdd gnd cell_6t
Xbit_r20_c2 bl[2] br[2] wl[20] vdd gnd cell_6t
Xbit_r21_c2 bl[2] br[2] wl[21] vdd gnd cell_6t
Xbit_r22_c2 bl[2] br[2] wl[22] vdd gnd cell_6t
Xbit_r23_c2 bl[2] br[2] wl[23] vdd gnd cell_6t
Xbit_r24_c2 bl[2] br[2] wl[24] vdd gnd cell_6t
Xbit_r25_c2 bl[2] br[2] wl[25] vdd gnd cell_6t
Xbit_r26_c2 bl[2] br[2] wl[26] vdd gnd cell_6t
Xbit_r27_c2 bl[2] br[2] wl[27] vdd gnd cell_6t
Xbit_r28_c2 bl[2] br[2] wl[28] vdd gnd cell_6t
Xbit_r29_c2 bl[2] br[2] wl[29] vdd gnd cell_6t
Xbit_r30_c2 bl[2] br[2] wl[30] vdd gnd cell_6t
Xbit_r31_c2 bl[2] br[2] wl[31] vdd gnd cell_6t
Xbit_r32_c2 bl[2] br[2] wl[32] vdd gnd cell_6t
Xbit_r33_c2 bl[2] br[2] wl[33] vdd gnd cell_6t
Xbit_r34_c2 bl[2] br[2] wl[34] vdd gnd cell_6t
Xbit_r35_c2 bl[2] br[2] wl[35] vdd gnd cell_6t
Xbit_r36_c2 bl[2] br[2] wl[36] vdd gnd cell_6t
Xbit_r37_c2 bl[2] br[2] wl[37] vdd gnd cell_6t
Xbit_r38_c2 bl[2] br[2] wl[38] vdd gnd cell_6t
Xbit_r39_c2 bl[2] br[2] wl[39] vdd gnd cell_6t
Xbit_r40_c2 bl[2] br[2] wl[40] vdd gnd cell_6t
Xbit_r41_c2 bl[2] br[2] wl[41] vdd gnd cell_6t
Xbit_r42_c2 bl[2] br[2] wl[42] vdd gnd cell_6t
Xbit_r43_c2 bl[2] br[2] wl[43] vdd gnd cell_6t
Xbit_r44_c2 bl[2] br[2] wl[44] vdd gnd cell_6t
Xbit_r45_c2 bl[2] br[2] wl[45] vdd gnd cell_6t
Xbit_r46_c2 bl[2] br[2] wl[46] vdd gnd cell_6t
Xbit_r47_c2 bl[2] br[2] wl[47] vdd gnd cell_6t
Xbit_r48_c2 bl[2] br[2] wl[48] vdd gnd cell_6t
Xbit_r49_c2 bl[2] br[2] wl[49] vdd gnd cell_6t
Xbit_r50_c2 bl[2] br[2] wl[50] vdd gnd cell_6t
Xbit_r51_c2 bl[2] br[2] wl[51] vdd gnd cell_6t
Xbit_r52_c2 bl[2] br[2] wl[52] vdd gnd cell_6t
Xbit_r53_c2 bl[2] br[2] wl[53] vdd gnd cell_6t
Xbit_r54_c2 bl[2] br[2] wl[54] vdd gnd cell_6t
Xbit_r55_c2 bl[2] br[2] wl[55] vdd gnd cell_6t
Xbit_r56_c2 bl[2] br[2] wl[56] vdd gnd cell_6t
Xbit_r57_c2 bl[2] br[2] wl[57] vdd gnd cell_6t
Xbit_r58_c2 bl[2] br[2] wl[58] vdd gnd cell_6t
Xbit_r59_c2 bl[2] br[2] wl[59] vdd gnd cell_6t
Xbit_r60_c2 bl[2] br[2] wl[60] vdd gnd cell_6t
Xbit_r61_c2 bl[2] br[2] wl[61] vdd gnd cell_6t
Xbit_r62_c2 bl[2] br[2] wl[62] vdd gnd cell_6t
Xbit_r63_c2 bl[2] br[2] wl[63] vdd gnd cell_6t
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
Xbit_r16_c3 bl[3] br[3] wl[16] vdd gnd cell_6t
Xbit_r17_c3 bl[3] br[3] wl[17] vdd gnd cell_6t
Xbit_r18_c3 bl[3] br[3] wl[18] vdd gnd cell_6t
Xbit_r19_c3 bl[3] br[3] wl[19] vdd gnd cell_6t
Xbit_r20_c3 bl[3] br[3] wl[20] vdd gnd cell_6t
Xbit_r21_c3 bl[3] br[3] wl[21] vdd gnd cell_6t
Xbit_r22_c3 bl[3] br[3] wl[22] vdd gnd cell_6t
Xbit_r23_c3 bl[3] br[3] wl[23] vdd gnd cell_6t
Xbit_r24_c3 bl[3] br[3] wl[24] vdd gnd cell_6t
Xbit_r25_c3 bl[3] br[3] wl[25] vdd gnd cell_6t
Xbit_r26_c3 bl[3] br[3] wl[26] vdd gnd cell_6t
Xbit_r27_c3 bl[3] br[3] wl[27] vdd gnd cell_6t
Xbit_r28_c3 bl[3] br[3] wl[28] vdd gnd cell_6t
Xbit_r29_c3 bl[3] br[3] wl[29] vdd gnd cell_6t
Xbit_r30_c3 bl[3] br[3] wl[30] vdd gnd cell_6t
Xbit_r31_c3 bl[3] br[3] wl[31] vdd gnd cell_6t
Xbit_r32_c3 bl[3] br[3] wl[32] vdd gnd cell_6t
Xbit_r33_c3 bl[3] br[3] wl[33] vdd gnd cell_6t
Xbit_r34_c3 bl[3] br[3] wl[34] vdd gnd cell_6t
Xbit_r35_c3 bl[3] br[3] wl[35] vdd gnd cell_6t
Xbit_r36_c3 bl[3] br[3] wl[36] vdd gnd cell_6t
Xbit_r37_c3 bl[3] br[3] wl[37] vdd gnd cell_6t
Xbit_r38_c3 bl[3] br[3] wl[38] vdd gnd cell_6t
Xbit_r39_c3 bl[3] br[3] wl[39] vdd gnd cell_6t
Xbit_r40_c3 bl[3] br[3] wl[40] vdd gnd cell_6t
Xbit_r41_c3 bl[3] br[3] wl[41] vdd gnd cell_6t
Xbit_r42_c3 bl[3] br[3] wl[42] vdd gnd cell_6t
Xbit_r43_c3 bl[3] br[3] wl[43] vdd gnd cell_6t
Xbit_r44_c3 bl[3] br[3] wl[44] vdd gnd cell_6t
Xbit_r45_c3 bl[3] br[3] wl[45] vdd gnd cell_6t
Xbit_r46_c3 bl[3] br[3] wl[46] vdd gnd cell_6t
Xbit_r47_c3 bl[3] br[3] wl[47] vdd gnd cell_6t
Xbit_r48_c3 bl[3] br[3] wl[48] vdd gnd cell_6t
Xbit_r49_c3 bl[3] br[3] wl[49] vdd gnd cell_6t
Xbit_r50_c3 bl[3] br[3] wl[50] vdd gnd cell_6t
Xbit_r51_c3 bl[3] br[3] wl[51] vdd gnd cell_6t
Xbit_r52_c3 bl[3] br[3] wl[52] vdd gnd cell_6t
Xbit_r53_c3 bl[3] br[3] wl[53] vdd gnd cell_6t
Xbit_r54_c3 bl[3] br[3] wl[54] vdd gnd cell_6t
Xbit_r55_c3 bl[3] br[3] wl[55] vdd gnd cell_6t
Xbit_r56_c3 bl[3] br[3] wl[56] vdd gnd cell_6t
Xbit_r57_c3 bl[3] br[3] wl[57] vdd gnd cell_6t
Xbit_r58_c3 bl[3] br[3] wl[58] vdd gnd cell_6t
Xbit_r59_c3 bl[3] br[3] wl[59] vdd gnd cell_6t
Xbit_r60_c3 bl[3] br[3] wl[60] vdd gnd cell_6t
Xbit_r61_c3 bl[3] br[3] wl[61] vdd gnd cell_6t
Xbit_r62_c3 bl[3] br[3] wl[62] vdd gnd cell_6t
Xbit_r63_c3 bl[3] br[3] wl[63] vdd gnd cell_6t
Xbit_r0_c4 bl[4] br[4] wl[0] vdd gnd cell_6t
Xbit_r1_c4 bl[4] br[4] wl[1] vdd gnd cell_6t
Xbit_r2_c4 bl[4] br[4] wl[2] vdd gnd cell_6t
Xbit_r3_c4 bl[4] br[4] wl[3] vdd gnd cell_6t
Xbit_r4_c4 bl[4] br[4] wl[4] vdd gnd cell_6t
Xbit_r5_c4 bl[4] br[4] wl[5] vdd gnd cell_6t
Xbit_r6_c4 bl[4] br[4] wl[6] vdd gnd cell_6t
Xbit_r7_c4 bl[4] br[4] wl[7] vdd gnd cell_6t
Xbit_r8_c4 bl[4] br[4] wl[8] vdd gnd cell_6t
Xbit_r9_c4 bl[4] br[4] wl[9] vdd gnd cell_6t
Xbit_r10_c4 bl[4] br[4] wl[10] vdd gnd cell_6t
Xbit_r11_c4 bl[4] br[4] wl[11] vdd gnd cell_6t
Xbit_r12_c4 bl[4] br[4] wl[12] vdd gnd cell_6t
Xbit_r13_c4 bl[4] br[4] wl[13] vdd gnd cell_6t
Xbit_r14_c4 bl[4] br[4] wl[14] vdd gnd cell_6t
Xbit_r15_c4 bl[4] br[4] wl[15] vdd gnd cell_6t
Xbit_r16_c4 bl[4] br[4] wl[16] vdd gnd cell_6t
Xbit_r17_c4 bl[4] br[4] wl[17] vdd gnd cell_6t
Xbit_r18_c4 bl[4] br[4] wl[18] vdd gnd cell_6t
Xbit_r19_c4 bl[4] br[4] wl[19] vdd gnd cell_6t
Xbit_r20_c4 bl[4] br[4] wl[20] vdd gnd cell_6t
Xbit_r21_c4 bl[4] br[4] wl[21] vdd gnd cell_6t
Xbit_r22_c4 bl[4] br[4] wl[22] vdd gnd cell_6t
Xbit_r23_c4 bl[4] br[4] wl[23] vdd gnd cell_6t
Xbit_r24_c4 bl[4] br[4] wl[24] vdd gnd cell_6t
Xbit_r25_c4 bl[4] br[4] wl[25] vdd gnd cell_6t
Xbit_r26_c4 bl[4] br[4] wl[26] vdd gnd cell_6t
Xbit_r27_c4 bl[4] br[4] wl[27] vdd gnd cell_6t
Xbit_r28_c4 bl[4] br[4] wl[28] vdd gnd cell_6t
Xbit_r29_c4 bl[4] br[4] wl[29] vdd gnd cell_6t
Xbit_r30_c4 bl[4] br[4] wl[30] vdd gnd cell_6t
Xbit_r31_c4 bl[4] br[4] wl[31] vdd gnd cell_6t
Xbit_r32_c4 bl[4] br[4] wl[32] vdd gnd cell_6t
Xbit_r33_c4 bl[4] br[4] wl[33] vdd gnd cell_6t
Xbit_r34_c4 bl[4] br[4] wl[34] vdd gnd cell_6t
Xbit_r35_c4 bl[4] br[4] wl[35] vdd gnd cell_6t
Xbit_r36_c4 bl[4] br[4] wl[36] vdd gnd cell_6t
Xbit_r37_c4 bl[4] br[4] wl[37] vdd gnd cell_6t
Xbit_r38_c4 bl[4] br[4] wl[38] vdd gnd cell_6t
Xbit_r39_c4 bl[4] br[4] wl[39] vdd gnd cell_6t
Xbit_r40_c4 bl[4] br[4] wl[40] vdd gnd cell_6t
Xbit_r41_c4 bl[4] br[4] wl[41] vdd gnd cell_6t
Xbit_r42_c4 bl[4] br[4] wl[42] vdd gnd cell_6t
Xbit_r43_c4 bl[4] br[4] wl[43] vdd gnd cell_6t
Xbit_r44_c4 bl[4] br[4] wl[44] vdd gnd cell_6t
Xbit_r45_c4 bl[4] br[4] wl[45] vdd gnd cell_6t
Xbit_r46_c4 bl[4] br[4] wl[46] vdd gnd cell_6t
Xbit_r47_c4 bl[4] br[4] wl[47] vdd gnd cell_6t
Xbit_r48_c4 bl[4] br[4] wl[48] vdd gnd cell_6t
Xbit_r49_c4 bl[4] br[4] wl[49] vdd gnd cell_6t
Xbit_r50_c4 bl[4] br[4] wl[50] vdd gnd cell_6t
Xbit_r51_c4 bl[4] br[4] wl[51] vdd gnd cell_6t
Xbit_r52_c4 bl[4] br[4] wl[52] vdd gnd cell_6t
Xbit_r53_c4 bl[4] br[4] wl[53] vdd gnd cell_6t
Xbit_r54_c4 bl[4] br[4] wl[54] vdd gnd cell_6t
Xbit_r55_c4 bl[4] br[4] wl[55] vdd gnd cell_6t
Xbit_r56_c4 bl[4] br[4] wl[56] vdd gnd cell_6t
Xbit_r57_c4 bl[4] br[4] wl[57] vdd gnd cell_6t
Xbit_r58_c4 bl[4] br[4] wl[58] vdd gnd cell_6t
Xbit_r59_c4 bl[4] br[4] wl[59] vdd gnd cell_6t
Xbit_r60_c4 bl[4] br[4] wl[60] vdd gnd cell_6t
Xbit_r61_c4 bl[4] br[4] wl[61] vdd gnd cell_6t
Xbit_r62_c4 bl[4] br[4] wl[62] vdd gnd cell_6t
Xbit_r63_c4 bl[4] br[4] wl[63] vdd gnd cell_6t
Xbit_r0_c5 bl[5] br[5] wl[0] vdd gnd cell_6t
Xbit_r1_c5 bl[5] br[5] wl[1] vdd gnd cell_6t
Xbit_r2_c5 bl[5] br[5] wl[2] vdd gnd cell_6t
Xbit_r3_c5 bl[5] br[5] wl[3] vdd gnd cell_6t
Xbit_r4_c5 bl[5] br[5] wl[4] vdd gnd cell_6t
Xbit_r5_c5 bl[5] br[5] wl[5] vdd gnd cell_6t
Xbit_r6_c5 bl[5] br[5] wl[6] vdd gnd cell_6t
Xbit_r7_c5 bl[5] br[5] wl[7] vdd gnd cell_6t
Xbit_r8_c5 bl[5] br[5] wl[8] vdd gnd cell_6t
Xbit_r9_c5 bl[5] br[5] wl[9] vdd gnd cell_6t
Xbit_r10_c5 bl[5] br[5] wl[10] vdd gnd cell_6t
Xbit_r11_c5 bl[5] br[5] wl[11] vdd gnd cell_6t
Xbit_r12_c5 bl[5] br[5] wl[12] vdd gnd cell_6t
Xbit_r13_c5 bl[5] br[5] wl[13] vdd gnd cell_6t
Xbit_r14_c5 bl[5] br[5] wl[14] vdd gnd cell_6t
Xbit_r15_c5 bl[5] br[5] wl[15] vdd gnd cell_6t
Xbit_r16_c5 bl[5] br[5] wl[16] vdd gnd cell_6t
Xbit_r17_c5 bl[5] br[5] wl[17] vdd gnd cell_6t
Xbit_r18_c5 bl[5] br[5] wl[18] vdd gnd cell_6t
Xbit_r19_c5 bl[5] br[5] wl[19] vdd gnd cell_6t
Xbit_r20_c5 bl[5] br[5] wl[20] vdd gnd cell_6t
Xbit_r21_c5 bl[5] br[5] wl[21] vdd gnd cell_6t
Xbit_r22_c5 bl[5] br[5] wl[22] vdd gnd cell_6t
Xbit_r23_c5 bl[5] br[5] wl[23] vdd gnd cell_6t
Xbit_r24_c5 bl[5] br[5] wl[24] vdd gnd cell_6t
Xbit_r25_c5 bl[5] br[5] wl[25] vdd gnd cell_6t
Xbit_r26_c5 bl[5] br[5] wl[26] vdd gnd cell_6t
Xbit_r27_c5 bl[5] br[5] wl[27] vdd gnd cell_6t
Xbit_r28_c5 bl[5] br[5] wl[28] vdd gnd cell_6t
Xbit_r29_c5 bl[5] br[5] wl[29] vdd gnd cell_6t
Xbit_r30_c5 bl[5] br[5] wl[30] vdd gnd cell_6t
Xbit_r31_c5 bl[5] br[5] wl[31] vdd gnd cell_6t
Xbit_r32_c5 bl[5] br[5] wl[32] vdd gnd cell_6t
Xbit_r33_c5 bl[5] br[5] wl[33] vdd gnd cell_6t
Xbit_r34_c5 bl[5] br[5] wl[34] vdd gnd cell_6t
Xbit_r35_c5 bl[5] br[5] wl[35] vdd gnd cell_6t
Xbit_r36_c5 bl[5] br[5] wl[36] vdd gnd cell_6t
Xbit_r37_c5 bl[5] br[5] wl[37] vdd gnd cell_6t
Xbit_r38_c5 bl[5] br[5] wl[38] vdd gnd cell_6t
Xbit_r39_c5 bl[5] br[5] wl[39] vdd gnd cell_6t
Xbit_r40_c5 bl[5] br[5] wl[40] vdd gnd cell_6t
Xbit_r41_c5 bl[5] br[5] wl[41] vdd gnd cell_6t
Xbit_r42_c5 bl[5] br[5] wl[42] vdd gnd cell_6t
Xbit_r43_c5 bl[5] br[5] wl[43] vdd gnd cell_6t
Xbit_r44_c5 bl[5] br[5] wl[44] vdd gnd cell_6t
Xbit_r45_c5 bl[5] br[5] wl[45] vdd gnd cell_6t
Xbit_r46_c5 bl[5] br[5] wl[46] vdd gnd cell_6t
Xbit_r47_c5 bl[5] br[5] wl[47] vdd gnd cell_6t
Xbit_r48_c5 bl[5] br[5] wl[48] vdd gnd cell_6t
Xbit_r49_c5 bl[5] br[5] wl[49] vdd gnd cell_6t
Xbit_r50_c5 bl[5] br[5] wl[50] vdd gnd cell_6t
Xbit_r51_c5 bl[5] br[5] wl[51] vdd gnd cell_6t
Xbit_r52_c5 bl[5] br[5] wl[52] vdd gnd cell_6t
Xbit_r53_c5 bl[5] br[5] wl[53] vdd gnd cell_6t
Xbit_r54_c5 bl[5] br[5] wl[54] vdd gnd cell_6t
Xbit_r55_c5 bl[5] br[5] wl[55] vdd gnd cell_6t
Xbit_r56_c5 bl[5] br[5] wl[56] vdd gnd cell_6t
Xbit_r57_c5 bl[5] br[5] wl[57] vdd gnd cell_6t
Xbit_r58_c5 bl[5] br[5] wl[58] vdd gnd cell_6t
Xbit_r59_c5 bl[5] br[5] wl[59] vdd gnd cell_6t
Xbit_r60_c5 bl[5] br[5] wl[60] vdd gnd cell_6t
Xbit_r61_c5 bl[5] br[5] wl[61] vdd gnd cell_6t
Xbit_r62_c5 bl[5] br[5] wl[62] vdd gnd cell_6t
Xbit_r63_c5 bl[5] br[5] wl[63] vdd gnd cell_6t
Xbit_r0_c6 bl[6] br[6] wl[0] vdd gnd cell_6t
Xbit_r1_c6 bl[6] br[6] wl[1] vdd gnd cell_6t
Xbit_r2_c6 bl[6] br[6] wl[2] vdd gnd cell_6t
Xbit_r3_c6 bl[6] br[6] wl[3] vdd gnd cell_6t
Xbit_r4_c6 bl[6] br[6] wl[4] vdd gnd cell_6t
Xbit_r5_c6 bl[6] br[6] wl[5] vdd gnd cell_6t
Xbit_r6_c6 bl[6] br[6] wl[6] vdd gnd cell_6t
Xbit_r7_c6 bl[6] br[6] wl[7] vdd gnd cell_6t
Xbit_r8_c6 bl[6] br[6] wl[8] vdd gnd cell_6t
Xbit_r9_c6 bl[6] br[6] wl[9] vdd gnd cell_6t
Xbit_r10_c6 bl[6] br[6] wl[10] vdd gnd cell_6t
Xbit_r11_c6 bl[6] br[6] wl[11] vdd gnd cell_6t
Xbit_r12_c6 bl[6] br[6] wl[12] vdd gnd cell_6t
Xbit_r13_c6 bl[6] br[6] wl[13] vdd gnd cell_6t
Xbit_r14_c6 bl[6] br[6] wl[14] vdd gnd cell_6t
Xbit_r15_c6 bl[6] br[6] wl[15] vdd gnd cell_6t
Xbit_r16_c6 bl[6] br[6] wl[16] vdd gnd cell_6t
Xbit_r17_c6 bl[6] br[6] wl[17] vdd gnd cell_6t
Xbit_r18_c6 bl[6] br[6] wl[18] vdd gnd cell_6t
Xbit_r19_c6 bl[6] br[6] wl[19] vdd gnd cell_6t
Xbit_r20_c6 bl[6] br[6] wl[20] vdd gnd cell_6t
Xbit_r21_c6 bl[6] br[6] wl[21] vdd gnd cell_6t
Xbit_r22_c6 bl[6] br[6] wl[22] vdd gnd cell_6t
Xbit_r23_c6 bl[6] br[6] wl[23] vdd gnd cell_6t
Xbit_r24_c6 bl[6] br[6] wl[24] vdd gnd cell_6t
Xbit_r25_c6 bl[6] br[6] wl[25] vdd gnd cell_6t
Xbit_r26_c6 bl[6] br[6] wl[26] vdd gnd cell_6t
Xbit_r27_c6 bl[6] br[6] wl[27] vdd gnd cell_6t
Xbit_r28_c6 bl[6] br[6] wl[28] vdd gnd cell_6t
Xbit_r29_c6 bl[6] br[6] wl[29] vdd gnd cell_6t
Xbit_r30_c6 bl[6] br[6] wl[30] vdd gnd cell_6t
Xbit_r31_c6 bl[6] br[6] wl[31] vdd gnd cell_6t
Xbit_r32_c6 bl[6] br[6] wl[32] vdd gnd cell_6t
Xbit_r33_c6 bl[6] br[6] wl[33] vdd gnd cell_6t
Xbit_r34_c6 bl[6] br[6] wl[34] vdd gnd cell_6t
Xbit_r35_c6 bl[6] br[6] wl[35] vdd gnd cell_6t
Xbit_r36_c6 bl[6] br[6] wl[36] vdd gnd cell_6t
Xbit_r37_c6 bl[6] br[6] wl[37] vdd gnd cell_6t
Xbit_r38_c6 bl[6] br[6] wl[38] vdd gnd cell_6t
Xbit_r39_c6 bl[6] br[6] wl[39] vdd gnd cell_6t
Xbit_r40_c6 bl[6] br[6] wl[40] vdd gnd cell_6t
Xbit_r41_c6 bl[6] br[6] wl[41] vdd gnd cell_6t
Xbit_r42_c6 bl[6] br[6] wl[42] vdd gnd cell_6t
Xbit_r43_c6 bl[6] br[6] wl[43] vdd gnd cell_6t
Xbit_r44_c6 bl[6] br[6] wl[44] vdd gnd cell_6t
Xbit_r45_c6 bl[6] br[6] wl[45] vdd gnd cell_6t
Xbit_r46_c6 bl[6] br[6] wl[46] vdd gnd cell_6t
Xbit_r47_c6 bl[6] br[6] wl[47] vdd gnd cell_6t
Xbit_r48_c6 bl[6] br[6] wl[48] vdd gnd cell_6t
Xbit_r49_c6 bl[6] br[6] wl[49] vdd gnd cell_6t
Xbit_r50_c6 bl[6] br[6] wl[50] vdd gnd cell_6t
Xbit_r51_c6 bl[6] br[6] wl[51] vdd gnd cell_6t
Xbit_r52_c6 bl[6] br[6] wl[52] vdd gnd cell_6t
Xbit_r53_c6 bl[6] br[6] wl[53] vdd gnd cell_6t
Xbit_r54_c6 bl[6] br[6] wl[54] vdd gnd cell_6t
Xbit_r55_c6 bl[6] br[6] wl[55] vdd gnd cell_6t
Xbit_r56_c6 bl[6] br[6] wl[56] vdd gnd cell_6t
Xbit_r57_c6 bl[6] br[6] wl[57] vdd gnd cell_6t
Xbit_r58_c6 bl[6] br[6] wl[58] vdd gnd cell_6t
Xbit_r59_c6 bl[6] br[6] wl[59] vdd gnd cell_6t
Xbit_r60_c6 bl[6] br[6] wl[60] vdd gnd cell_6t
Xbit_r61_c6 bl[6] br[6] wl[61] vdd gnd cell_6t
Xbit_r62_c6 bl[6] br[6] wl[62] vdd gnd cell_6t
Xbit_r63_c6 bl[6] br[6] wl[63] vdd gnd cell_6t
Xbit_r0_c7 bl[7] br[7] wl[0] vdd gnd cell_6t
Xbit_r1_c7 bl[7] br[7] wl[1] vdd gnd cell_6t
Xbit_r2_c7 bl[7] br[7] wl[2] vdd gnd cell_6t
Xbit_r3_c7 bl[7] br[7] wl[3] vdd gnd cell_6t
Xbit_r4_c7 bl[7] br[7] wl[4] vdd gnd cell_6t
Xbit_r5_c7 bl[7] br[7] wl[5] vdd gnd cell_6t
Xbit_r6_c7 bl[7] br[7] wl[6] vdd gnd cell_6t
Xbit_r7_c7 bl[7] br[7] wl[7] vdd gnd cell_6t
Xbit_r8_c7 bl[7] br[7] wl[8] vdd gnd cell_6t
Xbit_r9_c7 bl[7] br[7] wl[9] vdd gnd cell_6t
Xbit_r10_c7 bl[7] br[7] wl[10] vdd gnd cell_6t
Xbit_r11_c7 bl[7] br[7] wl[11] vdd gnd cell_6t
Xbit_r12_c7 bl[7] br[7] wl[12] vdd gnd cell_6t
Xbit_r13_c7 bl[7] br[7] wl[13] vdd gnd cell_6t
Xbit_r14_c7 bl[7] br[7] wl[14] vdd gnd cell_6t
Xbit_r15_c7 bl[7] br[7] wl[15] vdd gnd cell_6t
Xbit_r16_c7 bl[7] br[7] wl[16] vdd gnd cell_6t
Xbit_r17_c7 bl[7] br[7] wl[17] vdd gnd cell_6t
Xbit_r18_c7 bl[7] br[7] wl[18] vdd gnd cell_6t
Xbit_r19_c7 bl[7] br[7] wl[19] vdd gnd cell_6t
Xbit_r20_c7 bl[7] br[7] wl[20] vdd gnd cell_6t
Xbit_r21_c7 bl[7] br[7] wl[21] vdd gnd cell_6t
Xbit_r22_c7 bl[7] br[7] wl[22] vdd gnd cell_6t
Xbit_r23_c7 bl[7] br[7] wl[23] vdd gnd cell_6t
Xbit_r24_c7 bl[7] br[7] wl[24] vdd gnd cell_6t
Xbit_r25_c7 bl[7] br[7] wl[25] vdd gnd cell_6t
Xbit_r26_c7 bl[7] br[7] wl[26] vdd gnd cell_6t
Xbit_r27_c7 bl[7] br[7] wl[27] vdd gnd cell_6t
Xbit_r28_c7 bl[7] br[7] wl[28] vdd gnd cell_6t
Xbit_r29_c7 bl[7] br[7] wl[29] vdd gnd cell_6t
Xbit_r30_c7 bl[7] br[7] wl[30] vdd gnd cell_6t
Xbit_r31_c7 bl[7] br[7] wl[31] vdd gnd cell_6t
Xbit_r32_c7 bl[7] br[7] wl[32] vdd gnd cell_6t
Xbit_r33_c7 bl[7] br[7] wl[33] vdd gnd cell_6t
Xbit_r34_c7 bl[7] br[7] wl[34] vdd gnd cell_6t
Xbit_r35_c7 bl[7] br[7] wl[35] vdd gnd cell_6t
Xbit_r36_c7 bl[7] br[7] wl[36] vdd gnd cell_6t
Xbit_r37_c7 bl[7] br[7] wl[37] vdd gnd cell_6t
Xbit_r38_c7 bl[7] br[7] wl[38] vdd gnd cell_6t
Xbit_r39_c7 bl[7] br[7] wl[39] vdd gnd cell_6t
Xbit_r40_c7 bl[7] br[7] wl[40] vdd gnd cell_6t
Xbit_r41_c7 bl[7] br[7] wl[41] vdd gnd cell_6t
Xbit_r42_c7 bl[7] br[7] wl[42] vdd gnd cell_6t
Xbit_r43_c7 bl[7] br[7] wl[43] vdd gnd cell_6t
Xbit_r44_c7 bl[7] br[7] wl[44] vdd gnd cell_6t
Xbit_r45_c7 bl[7] br[7] wl[45] vdd gnd cell_6t
Xbit_r46_c7 bl[7] br[7] wl[46] vdd gnd cell_6t
Xbit_r47_c7 bl[7] br[7] wl[47] vdd gnd cell_6t
Xbit_r48_c7 bl[7] br[7] wl[48] vdd gnd cell_6t
Xbit_r49_c7 bl[7] br[7] wl[49] vdd gnd cell_6t
Xbit_r50_c7 bl[7] br[7] wl[50] vdd gnd cell_6t
Xbit_r51_c7 bl[7] br[7] wl[51] vdd gnd cell_6t
Xbit_r52_c7 bl[7] br[7] wl[52] vdd gnd cell_6t
Xbit_r53_c7 bl[7] br[7] wl[53] vdd gnd cell_6t
Xbit_r54_c7 bl[7] br[7] wl[54] vdd gnd cell_6t
Xbit_r55_c7 bl[7] br[7] wl[55] vdd gnd cell_6t
Xbit_r56_c7 bl[7] br[7] wl[56] vdd gnd cell_6t
Xbit_r57_c7 bl[7] br[7] wl[57] vdd gnd cell_6t
Xbit_r58_c7 bl[7] br[7] wl[58] vdd gnd cell_6t
Xbit_r59_c7 bl[7] br[7] wl[59] vdd gnd cell_6t
Xbit_r60_c7 bl[7] br[7] wl[60] vdd gnd cell_6t
Xbit_r61_c7 bl[7] br[7] wl[61] vdd gnd cell_6t
Xbit_r62_c7 bl[7] br[7] wl[62] vdd gnd cell_6t
Xbit_r63_c7 bl[7] br[7] wl[63] vdd gnd cell_6t
Xbit_r0_c8 bl[8] br[8] wl[0] vdd gnd cell_6t
Xbit_r1_c8 bl[8] br[8] wl[1] vdd gnd cell_6t
Xbit_r2_c8 bl[8] br[8] wl[2] vdd gnd cell_6t
Xbit_r3_c8 bl[8] br[8] wl[3] vdd gnd cell_6t
Xbit_r4_c8 bl[8] br[8] wl[4] vdd gnd cell_6t
Xbit_r5_c8 bl[8] br[8] wl[5] vdd gnd cell_6t
Xbit_r6_c8 bl[8] br[8] wl[6] vdd gnd cell_6t
Xbit_r7_c8 bl[8] br[8] wl[7] vdd gnd cell_6t
Xbit_r8_c8 bl[8] br[8] wl[8] vdd gnd cell_6t
Xbit_r9_c8 bl[8] br[8] wl[9] vdd gnd cell_6t
Xbit_r10_c8 bl[8] br[8] wl[10] vdd gnd cell_6t
Xbit_r11_c8 bl[8] br[8] wl[11] vdd gnd cell_6t
Xbit_r12_c8 bl[8] br[8] wl[12] vdd gnd cell_6t
Xbit_r13_c8 bl[8] br[8] wl[13] vdd gnd cell_6t
Xbit_r14_c8 bl[8] br[8] wl[14] vdd gnd cell_6t
Xbit_r15_c8 bl[8] br[8] wl[15] vdd gnd cell_6t
Xbit_r16_c8 bl[8] br[8] wl[16] vdd gnd cell_6t
Xbit_r17_c8 bl[8] br[8] wl[17] vdd gnd cell_6t
Xbit_r18_c8 bl[8] br[8] wl[18] vdd gnd cell_6t
Xbit_r19_c8 bl[8] br[8] wl[19] vdd gnd cell_6t
Xbit_r20_c8 bl[8] br[8] wl[20] vdd gnd cell_6t
Xbit_r21_c8 bl[8] br[8] wl[21] vdd gnd cell_6t
Xbit_r22_c8 bl[8] br[8] wl[22] vdd gnd cell_6t
Xbit_r23_c8 bl[8] br[8] wl[23] vdd gnd cell_6t
Xbit_r24_c8 bl[8] br[8] wl[24] vdd gnd cell_6t
Xbit_r25_c8 bl[8] br[8] wl[25] vdd gnd cell_6t
Xbit_r26_c8 bl[8] br[8] wl[26] vdd gnd cell_6t
Xbit_r27_c8 bl[8] br[8] wl[27] vdd gnd cell_6t
Xbit_r28_c8 bl[8] br[8] wl[28] vdd gnd cell_6t
Xbit_r29_c8 bl[8] br[8] wl[29] vdd gnd cell_6t
Xbit_r30_c8 bl[8] br[8] wl[30] vdd gnd cell_6t
Xbit_r31_c8 bl[8] br[8] wl[31] vdd gnd cell_6t
Xbit_r32_c8 bl[8] br[8] wl[32] vdd gnd cell_6t
Xbit_r33_c8 bl[8] br[8] wl[33] vdd gnd cell_6t
Xbit_r34_c8 bl[8] br[8] wl[34] vdd gnd cell_6t
Xbit_r35_c8 bl[8] br[8] wl[35] vdd gnd cell_6t
Xbit_r36_c8 bl[8] br[8] wl[36] vdd gnd cell_6t
Xbit_r37_c8 bl[8] br[8] wl[37] vdd gnd cell_6t
Xbit_r38_c8 bl[8] br[8] wl[38] vdd gnd cell_6t
Xbit_r39_c8 bl[8] br[8] wl[39] vdd gnd cell_6t
Xbit_r40_c8 bl[8] br[8] wl[40] vdd gnd cell_6t
Xbit_r41_c8 bl[8] br[8] wl[41] vdd gnd cell_6t
Xbit_r42_c8 bl[8] br[8] wl[42] vdd gnd cell_6t
Xbit_r43_c8 bl[8] br[8] wl[43] vdd gnd cell_6t
Xbit_r44_c8 bl[8] br[8] wl[44] vdd gnd cell_6t
Xbit_r45_c8 bl[8] br[8] wl[45] vdd gnd cell_6t
Xbit_r46_c8 bl[8] br[8] wl[46] vdd gnd cell_6t
Xbit_r47_c8 bl[8] br[8] wl[47] vdd gnd cell_6t
Xbit_r48_c8 bl[8] br[8] wl[48] vdd gnd cell_6t
Xbit_r49_c8 bl[8] br[8] wl[49] vdd gnd cell_6t
Xbit_r50_c8 bl[8] br[8] wl[50] vdd gnd cell_6t
Xbit_r51_c8 bl[8] br[8] wl[51] vdd gnd cell_6t
Xbit_r52_c8 bl[8] br[8] wl[52] vdd gnd cell_6t
Xbit_r53_c8 bl[8] br[8] wl[53] vdd gnd cell_6t
Xbit_r54_c8 bl[8] br[8] wl[54] vdd gnd cell_6t
Xbit_r55_c8 bl[8] br[8] wl[55] vdd gnd cell_6t
Xbit_r56_c8 bl[8] br[8] wl[56] vdd gnd cell_6t
Xbit_r57_c8 bl[8] br[8] wl[57] vdd gnd cell_6t
Xbit_r58_c8 bl[8] br[8] wl[58] vdd gnd cell_6t
Xbit_r59_c8 bl[8] br[8] wl[59] vdd gnd cell_6t
Xbit_r60_c8 bl[8] br[8] wl[60] vdd gnd cell_6t
Xbit_r61_c8 bl[8] br[8] wl[61] vdd gnd cell_6t
Xbit_r62_c8 bl[8] br[8] wl[62] vdd gnd cell_6t
Xbit_r63_c8 bl[8] br[8] wl[63] vdd gnd cell_6t
Xbit_r0_c9 bl[9] br[9] wl[0] vdd gnd cell_6t
Xbit_r1_c9 bl[9] br[9] wl[1] vdd gnd cell_6t
Xbit_r2_c9 bl[9] br[9] wl[2] vdd gnd cell_6t
Xbit_r3_c9 bl[9] br[9] wl[3] vdd gnd cell_6t
Xbit_r4_c9 bl[9] br[9] wl[4] vdd gnd cell_6t
Xbit_r5_c9 bl[9] br[9] wl[5] vdd gnd cell_6t
Xbit_r6_c9 bl[9] br[9] wl[6] vdd gnd cell_6t
Xbit_r7_c9 bl[9] br[9] wl[7] vdd gnd cell_6t
Xbit_r8_c9 bl[9] br[9] wl[8] vdd gnd cell_6t
Xbit_r9_c9 bl[9] br[9] wl[9] vdd gnd cell_6t
Xbit_r10_c9 bl[9] br[9] wl[10] vdd gnd cell_6t
Xbit_r11_c9 bl[9] br[9] wl[11] vdd gnd cell_6t
Xbit_r12_c9 bl[9] br[9] wl[12] vdd gnd cell_6t
Xbit_r13_c9 bl[9] br[9] wl[13] vdd gnd cell_6t
Xbit_r14_c9 bl[9] br[9] wl[14] vdd gnd cell_6t
Xbit_r15_c9 bl[9] br[9] wl[15] vdd gnd cell_6t
Xbit_r16_c9 bl[9] br[9] wl[16] vdd gnd cell_6t
Xbit_r17_c9 bl[9] br[9] wl[17] vdd gnd cell_6t
Xbit_r18_c9 bl[9] br[9] wl[18] vdd gnd cell_6t
Xbit_r19_c9 bl[9] br[9] wl[19] vdd gnd cell_6t
Xbit_r20_c9 bl[9] br[9] wl[20] vdd gnd cell_6t
Xbit_r21_c9 bl[9] br[9] wl[21] vdd gnd cell_6t
Xbit_r22_c9 bl[9] br[9] wl[22] vdd gnd cell_6t
Xbit_r23_c9 bl[9] br[9] wl[23] vdd gnd cell_6t
Xbit_r24_c9 bl[9] br[9] wl[24] vdd gnd cell_6t
Xbit_r25_c9 bl[9] br[9] wl[25] vdd gnd cell_6t
Xbit_r26_c9 bl[9] br[9] wl[26] vdd gnd cell_6t
Xbit_r27_c9 bl[9] br[9] wl[27] vdd gnd cell_6t
Xbit_r28_c9 bl[9] br[9] wl[28] vdd gnd cell_6t
Xbit_r29_c9 bl[9] br[9] wl[29] vdd gnd cell_6t
Xbit_r30_c9 bl[9] br[9] wl[30] vdd gnd cell_6t
Xbit_r31_c9 bl[9] br[9] wl[31] vdd gnd cell_6t
Xbit_r32_c9 bl[9] br[9] wl[32] vdd gnd cell_6t
Xbit_r33_c9 bl[9] br[9] wl[33] vdd gnd cell_6t
Xbit_r34_c9 bl[9] br[9] wl[34] vdd gnd cell_6t
Xbit_r35_c9 bl[9] br[9] wl[35] vdd gnd cell_6t
Xbit_r36_c9 bl[9] br[9] wl[36] vdd gnd cell_6t
Xbit_r37_c9 bl[9] br[9] wl[37] vdd gnd cell_6t
Xbit_r38_c9 bl[9] br[9] wl[38] vdd gnd cell_6t
Xbit_r39_c9 bl[9] br[9] wl[39] vdd gnd cell_6t
Xbit_r40_c9 bl[9] br[9] wl[40] vdd gnd cell_6t
Xbit_r41_c9 bl[9] br[9] wl[41] vdd gnd cell_6t
Xbit_r42_c9 bl[9] br[9] wl[42] vdd gnd cell_6t
Xbit_r43_c9 bl[9] br[9] wl[43] vdd gnd cell_6t
Xbit_r44_c9 bl[9] br[9] wl[44] vdd gnd cell_6t
Xbit_r45_c9 bl[9] br[9] wl[45] vdd gnd cell_6t
Xbit_r46_c9 bl[9] br[9] wl[46] vdd gnd cell_6t
Xbit_r47_c9 bl[9] br[9] wl[47] vdd gnd cell_6t
Xbit_r48_c9 bl[9] br[9] wl[48] vdd gnd cell_6t
Xbit_r49_c9 bl[9] br[9] wl[49] vdd gnd cell_6t
Xbit_r50_c9 bl[9] br[9] wl[50] vdd gnd cell_6t
Xbit_r51_c9 bl[9] br[9] wl[51] vdd gnd cell_6t
Xbit_r52_c9 bl[9] br[9] wl[52] vdd gnd cell_6t
Xbit_r53_c9 bl[9] br[9] wl[53] vdd gnd cell_6t
Xbit_r54_c9 bl[9] br[9] wl[54] vdd gnd cell_6t
Xbit_r55_c9 bl[9] br[9] wl[55] vdd gnd cell_6t
Xbit_r56_c9 bl[9] br[9] wl[56] vdd gnd cell_6t
Xbit_r57_c9 bl[9] br[9] wl[57] vdd gnd cell_6t
Xbit_r58_c9 bl[9] br[9] wl[58] vdd gnd cell_6t
Xbit_r59_c9 bl[9] br[9] wl[59] vdd gnd cell_6t
Xbit_r60_c9 bl[9] br[9] wl[60] vdd gnd cell_6t
Xbit_r61_c9 bl[9] br[9] wl[61] vdd gnd cell_6t
Xbit_r62_c9 bl[9] br[9] wl[62] vdd gnd cell_6t
Xbit_r63_c9 bl[9] br[9] wl[63] vdd gnd cell_6t
Xbit_r0_c10 bl[10] br[10] wl[0] vdd gnd cell_6t
Xbit_r1_c10 bl[10] br[10] wl[1] vdd gnd cell_6t
Xbit_r2_c10 bl[10] br[10] wl[2] vdd gnd cell_6t
Xbit_r3_c10 bl[10] br[10] wl[3] vdd gnd cell_6t
Xbit_r4_c10 bl[10] br[10] wl[4] vdd gnd cell_6t
Xbit_r5_c10 bl[10] br[10] wl[5] vdd gnd cell_6t
Xbit_r6_c10 bl[10] br[10] wl[6] vdd gnd cell_6t
Xbit_r7_c10 bl[10] br[10] wl[7] vdd gnd cell_6t
Xbit_r8_c10 bl[10] br[10] wl[8] vdd gnd cell_6t
Xbit_r9_c10 bl[10] br[10] wl[9] vdd gnd cell_6t
Xbit_r10_c10 bl[10] br[10] wl[10] vdd gnd cell_6t
Xbit_r11_c10 bl[10] br[10] wl[11] vdd gnd cell_6t
Xbit_r12_c10 bl[10] br[10] wl[12] vdd gnd cell_6t
Xbit_r13_c10 bl[10] br[10] wl[13] vdd gnd cell_6t
Xbit_r14_c10 bl[10] br[10] wl[14] vdd gnd cell_6t
Xbit_r15_c10 bl[10] br[10] wl[15] vdd gnd cell_6t
Xbit_r16_c10 bl[10] br[10] wl[16] vdd gnd cell_6t
Xbit_r17_c10 bl[10] br[10] wl[17] vdd gnd cell_6t
Xbit_r18_c10 bl[10] br[10] wl[18] vdd gnd cell_6t
Xbit_r19_c10 bl[10] br[10] wl[19] vdd gnd cell_6t
Xbit_r20_c10 bl[10] br[10] wl[20] vdd gnd cell_6t
Xbit_r21_c10 bl[10] br[10] wl[21] vdd gnd cell_6t
Xbit_r22_c10 bl[10] br[10] wl[22] vdd gnd cell_6t
Xbit_r23_c10 bl[10] br[10] wl[23] vdd gnd cell_6t
Xbit_r24_c10 bl[10] br[10] wl[24] vdd gnd cell_6t
Xbit_r25_c10 bl[10] br[10] wl[25] vdd gnd cell_6t
Xbit_r26_c10 bl[10] br[10] wl[26] vdd gnd cell_6t
Xbit_r27_c10 bl[10] br[10] wl[27] vdd gnd cell_6t
Xbit_r28_c10 bl[10] br[10] wl[28] vdd gnd cell_6t
Xbit_r29_c10 bl[10] br[10] wl[29] vdd gnd cell_6t
Xbit_r30_c10 bl[10] br[10] wl[30] vdd gnd cell_6t
Xbit_r31_c10 bl[10] br[10] wl[31] vdd gnd cell_6t
Xbit_r32_c10 bl[10] br[10] wl[32] vdd gnd cell_6t
Xbit_r33_c10 bl[10] br[10] wl[33] vdd gnd cell_6t
Xbit_r34_c10 bl[10] br[10] wl[34] vdd gnd cell_6t
Xbit_r35_c10 bl[10] br[10] wl[35] vdd gnd cell_6t
Xbit_r36_c10 bl[10] br[10] wl[36] vdd gnd cell_6t
Xbit_r37_c10 bl[10] br[10] wl[37] vdd gnd cell_6t
Xbit_r38_c10 bl[10] br[10] wl[38] vdd gnd cell_6t
Xbit_r39_c10 bl[10] br[10] wl[39] vdd gnd cell_6t
Xbit_r40_c10 bl[10] br[10] wl[40] vdd gnd cell_6t
Xbit_r41_c10 bl[10] br[10] wl[41] vdd gnd cell_6t
Xbit_r42_c10 bl[10] br[10] wl[42] vdd gnd cell_6t
Xbit_r43_c10 bl[10] br[10] wl[43] vdd gnd cell_6t
Xbit_r44_c10 bl[10] br[10] wl[44] vdd gnd cell_6t
Xbit_r45_c10 bl[10] br[10] wl[45] vdd gnd cell_6t
Xbit_r46_c10 bl[10] br[10] wl[46] vdd gnd cell_6t
Xbit_r47_c10 bl[10] br[10] wl[47] vdd gnd cell_6t
Xbit_r48_c10 bl[10] br[10] wl[48] vdd gnd cell_6t
Xbit_r49_c10 bl[10] br[10] wl[49] vdd gnd cell_6t
Xbit_r50_c10 bl[10] br[10] wl[50] vdd gnd cell_6t
Xbit_r51_c10 bl[10] br[10] wl[51] vdd gnd cell_6t
Xbit_r52_c10 bl[10] br[10] wl[52] vdd gnd cell_6t
Xbit_r53_c10 bl[10] br[10] wl[53] vdd gnd cell_6t
Xbit_r54_c10 bl[10] br[10] wl[54] vdd gnd cell_6t
Xbit_r55_c10 bl[10] br[10] wl[55] vdd gnd cell_6t
Xbit_r56_c10 bl[10] br[10] wl[56] vdd gnd cell_6t
Xbit_r57_c10 bl[10] br[10] wl[57] vdd gnd cell_6t
Xbit_r58_c10 bl[10] br[10] wl[58] vdd gnd cell_6t
Xbit_r59_c10 bl[10] br[10] wl[59] vdd gnd cell_6t
Xbit_r60_c10 bl[10] br[10] wl[60] vdd gnd cell_6t
Xbit_r61_c10 bl[10] br[10] wl[61] vdd gnd cell_6t
Xbit_r62_c10 bl[10] br[10] wl[62] vdd gnd cell_6t
Xbit_r63_c10 bl[10] br[10] wl[63] vdd gnd cell_6t
Xbit_r0_c11 bl[11] br[11] wl[0] vdd gnd cell_6t
Xbit_r1_c11 bl[11] br[11] wl[1] vdd gnd cell_6t
Xbit_r2_c11 bl[11] br[11] wl[2] vdd gnd cell_6t
Xbit_r3_c11 bl[11] br[11] wl[3] vdd gnd cell_6t
Xbit_r4_c11 bl[11] br[11] wl[4] vdd gnd cell_6t
Xbit_r5_c11 bl[11] br[11] wl[5] vdd gnd cell_6t
Xbit_r6_c11 bl[11] br[11] wl[6] vdd gnd cell_6t
Xbit_r7_c11 bl[11] br[11] wl[7] vdd gnd cell_6t
Xbit_r8_c11 bl[11] br[11] wl[8] vdd gnd cell_6t
Xbit_r9_c11 bl[11] br[11] wl[9] vdd gnd cell_6t
Xbit_r10_c11 bl[11] br[11] wl[10] vdd gnd cell_6t
Xbit_r11_c11 bl[11] br[11] wl[11] vdd gnd cell_6t
Xbit_r12_c11 bl[11] br[11] wl[12] vdd gnd cell_6t
Xbit_r13_c11 bl[11] br[11] wl[13] vdd gnd cell_6t
Xbit_r14_c11 bl[11] br[11] wl[14] vdd gnd cell_6t
Xbit_r15_c11 bl[11] br[11] wl[15] vdd gnd cell_6t
Xbit_r16_c11 bl[11] br[11] wl[16] vdd gnd cell_6t
Xbit_r17_c11 bl[11] br[11] wl[17] vdd gnd cell_6t
Xbit_r18_c11 bl[11] br[11] wl[18] vdd gnd cell_6t
Xbit_r19_c11 bl[11] br[11] wl[19] vdd gnd cell_6t
Xbit_r20_c11 bl[11] br[11] wl[20] vdd gnd cell_6t
Xbit_r21_c11 bl[11] br[11] wl[21] vdd gnd cell_6t
Xbit_r22_c11 bl[11] br[11] wl[22] vdd gnd cell_6t
Xbit_r23_c11 bl[11] br[11] wl[23] vdd gnd cell_6t
Xbit_r24_c11 bl[11] br[11] wl[24] vdd gnd cell_6t
Xbit_r25_c11 bl[11] br[11] wl[25] vdd gnd cell_6t
Xbit_r26_c11 bl[11] br[11] wl[26] vdd gnd cell_6t
Xbit_r27_c11 bl[11] br[11] wl[27] vdd gnd cell_6t
Xbit_r28_c11 bl[11] br[11] wl[28] vdd gnd cell_6t
Xbit_r29_c11 bl[11] br[11] wl[29] vdd gnd cell_6t
Xbit_r30_c11 bl[11] br[11] wl[30] vdd gnd cell_6t
Xbit_r31_c11 bl[11] br[11] wl[31] vdd gnd cell_6t
Xbit_r32_c11 bl[11] br[11] wl[32] vdd gnd cell_6t
Xbit_r33_c11 bl[11] br[11] wl[33] vdd gnd cell_6t
Xbit_r34_c11 bl[11] br[11] wl[34] vdd gnd cell_6t
Xbit_r35_c11 bl[11] br[11] wl[35] vdd gnd cell_6t
Xbit_r36_c11 bl[11] br[11] wl[36] vdd gnd cell_6t
Xbit_r37_c11 bl[11] br[11] wl[37] vdd gnd cell_6t
Xbit_r38_c11 bl[11] br[11] wl[38] vdd gnd cell_6t
Xbit_r39_c11 bl[11] br[11] wl[39] vdd gnd cell_6t
Xbit_r40_c11 bl[11] br[11] wl[40] vdd gnd cell_6t
Xbit_r41_c11 bl[11] br[11] wl[41] vdd gnd cell_6t
Xbit_r42_c11 bl[11] br[11] wl[42] vdd gnd cell_6t
Xbit_r43_c11 bl[11] br[11] wl[43] vdd gnd cell_6t
Xbit_r44_c11 bl[11] br[11] wl[44] vdd gnd cell_6t
Xbit_r45_c11 bl[11] br[11] wl[45] vdd gnd cell_6t
Xbit_r46_c11 bl[11] br[11] wl[46] vdd gnd cell_6t
Xbit_r47_c11 bl[11] br[11] wl[47] vdd gnd cell_6t
Xbit_r48_c11 bl[11] br[11] wl[48] vdd gnd cell_6t
Xbit_r49_c11 bl[11] br[11] wl[49] vdd gnd cell_6t
Xbit_r50_c11 bl[11] br[11] wl[50] vdd gnd cell_6t
Xbit_r51_c11 bl[11] br[11] wl[51] vdd gnd cell_6t
Xbit_r52_c11 bl[11] br[11] wl[52] vdd gnd cell_6t
Xbit_r53_c11 bl[11] br[11] wl[53] vdd gnd cell_6t
Xbit_r54_c11 bl[11] br[11] wl[54] vdd gnd cell_6t
Xbit_r55_c11 bl[11] br[11] wl[55] vdd gnd cell_6t
Xbit_r56_c11 bl[11] br[11] wl[56] vdd gnd cell_6t
Xbit_r57_c11 bl[11] br[11] wl[57] vdd gnd cell_6t
Xbit_r58_c11 bl[11] br[11] wl[58] vdd gnd cell_6t
Xbit_r59_c11 bl[11] br[11] wl[59] vdd gnd cell_6t
Xbit_r60_c11 bl[11] br[11] wl[60] vdd gnd cell_6t
Xbit_r61_c11 bl[11] br[11] wl[61] vdd gnd cell_6t
Xbit_r62_c11 bl[11] br[11] wl[62] vdd gnd cell_6t
Xbit_r63_c11 bl[11] br[11] wl[63] vdd gnd cell_6t
Xbit_r0_c12 bl[12] br[12] wl[0] vdd gnd cell_6t
Xbit_r1_c12 bl[12] br[12] wl[1] vdd gnd cell_6t
Xbit_r2_c12 bl[12] br[12] wl[2] vdd gnd cell_6t
Xbit_r3_c12 bl[12] br[12] wl[3] vdd gnd cell_6t
Xbit_r4_c12 bl[12] br[12] wl[4] vdd gnd cell_6t
Xbit_r5_c12 bl[12] br[12] wl[5] vdd gnd cell_6t
Xbit_r6_c12 bl[12] br[12] wl[6] vdd gnd cell_6t
Xbit_r7_c12 bl[12] br[12] wl[7] vdd gnd cell_6t
Xbit_r8_c12 bl[12] br[12] wl[8] vdd gnd cell_6t
Xbit_r9_c12 bl[12] br[12] wl[9] vdd gnd cell_6t
Xbit_r10_c12 bl[12] br[12] wl[10] vdd gnd cell_6t
Xbit_r11_c12 bl[12] br[12] wl[11] vdd gnd cell_6t
Xbit_r12_c12 bl[12] br[12] wl[12] vdd gnd cell_6t
Xbit_r13_c12 bl[12] br[12] wl[13] vdd gnd cell_6t
Xbit_r14_c12 bl[12] br[12] wl[14] vdd gnd cell_6t
Xbit_r15_c12 bl[12] br[12] wl[15] vdd gnd cell_6t
Xbit_r16_c12 bl[12] br[12] wl[16] vdd gnd cell_6t
Xbit_r17_c12 bl[12] br[12] wl[17] vdd gnd cell_6t
Xbit_r18_c12 bl[12] br[12] wl[18] vdd gnd cell_6t
Xbit_r19_c12 bl[12] br[12] wl[19] vdd gnd cell_6t
Xbit_r20_c12 bl[12] br[12] wl[20] vdd gnd cell_6t
Xbit_r21_c12 bl[12] br[12] wl[21] vdd gnd cell_6t
Xbit_r22_c12 bl[12] br[12] wl[22] vdd gnd cell_6t
Xbit_r23_c12 bl[12] br[12] wl[23] vdd gnd cell_6t
Xbit_r24_c12 bl[12] br[12] wl[24] vdd gnd cell_6t
Xbit_r25_c12 bl[12] br[12] wl[25] vdd gnd cell_6t
Xbit_r26_c12 bl[12] br[12] wl[26] vdd gnd cell_6t
Xbit_r27_c12 bl[12] br[12] wl[27] vdd gnd cell_6t
Xbit_r28_c12 bl[12] br[12] wl[28] vdd gnd cell_6t
Xbit_r29_c12 bl[12] br[12] wl[29] vdd gnd cell_6t
Xbit_r30_c12 bl[12] br[12] wl[30] vdd gnd cell_6t
Xbit_r31_c12 bl[12] br[12] wl[31] vdd gnd cell_6t
Xbit_r32_c12 bl[12] br[12] wl[32] vdd gnd cell_6t
Xbit_r33_c12 bl[12] br[12] wl[33] vdd gnd cell_6t
Xbit_r34_c12 bl[12] br[12] wl[34] vdd gnd cell_6t
Xbit_r35_c12 bl[12] br[12] wl[35] vdd gnd cell_6t
Xbit_r36_c12 bl[12] br[12] wl[36] vdd gnd cell_6t
Xbit_r37_c12 bl[12] br[12] wl[37] vdd gnd cell_6t
Xbit_r38_c12 bl[12] br[12] wl[38] vdd gnd cell_6t
Xbit_r39_c12 bl[12] br[12] wl[39] vdd gnd cell_6t
Xbit_r40_c12 bl[12] br[12] wl[40] vdd gnd cell_6t
Xbit_r41_c12 bl[12] br[12] wl[41] vdd gnd cell_6t
Xbit_r42_c12 bl[12] br[12] wl[42] vdd gnd cell_6t
Xbit_r43_c12 bl[12] br[12] wl[43] vdd gnd cell_6t
Xbit_r44_c12 bl[12] br[12] wl[44] vdd gnd cell_6t
Xbit_r45_c12 bl[12] br[12] wl[45] vdd gnd cell_6t
Xbit_r46_c12 bl[12] br[12] wl[46] vdd gnd cell_6t
Xbit_r47_c12 bl[12] br[12] wl[47] vdd gnd cell_6t
Xbit_r48_c12 bl[12] br[12] wl[48] vdd gnd cell_6t
Xbit_r49_c12 bl[12] br[12] wl[49] vdd gnd cell_6t
Xbit_r50_c12 bl[12] br[12] wl[50] vdd gnd cell_6t
Xbit_r51_c12 bl[12] br[12] wl[51] vdd gnd cell_6t
Xbit_r52_c12 bl[12] br[12] wl[52] vdd gnd cell_6t
Xbit_r53_c12 bl[12] br[12] wl[53] vdd gnd cell_6t
Xbit_r54_c12 bl[12] br[12] wl[54] vdd gnd cell_6t
Xbit_r55_c12 bl[12] br[12] wl[55] vdd gnd cell_6t
Xbit_r56_c12 bl[12] br[12] wl[56] vdd gnd cell_6t
Xbit_r57_c12 bl[12] br[12] wl[57] vdd gnd cell_6t
Xbit_r58_c12 bl[12] br[12] wl[58] vdd gnd cell_6t
Xbit_r59_c12 bl[12] br[12] wl[59] vdd gnd cell_6t
Xbit_r60_c12 bl[12] br[12] wl[60] vdd gnd cell_6t
Xbit_r61_c12 bl[12] br[12] wl[61] vdd gnd cell_6t
Xbit_r62_c12 bl[12] br[12] wl[62] vdd gnd cell_6t
Xbit_r63_c12 bl[12] br[12] wl[63] vdd gnd cell_6t
Xbit_r0_c13 bl[13] br[13] wl[0] vdd gnd cell_6t
Xbit_r1_c13 bl[13] br[13] wl[1] vdd gnd cell_6t
Xbit_r2_c13 bl[13] br[13] wl[2] vdd gnd cell_6t
Xbit_r3_c13 bl[13] br[13] wl[3] vdd gnd cell_6t
Xbit_r4_c13 bl[13] br[13] wl[4] vdd gnd cell_6t
Xbit_r5_c13 bl[13] br[13] wl[5] vdd gnd cell_6t
Xbit_r6_c13 bl[13] br[13] wl[6] vdd gnd cell_6t
Xbit_r7_c13 bl[13] br[13] wl[7] vdd gnd cell_6t
Xbit_r8_c13 bl[13] br[13] wl[8] vdd gnd cell_6t
Xbit_r9_c13 bl[13] br[13] wl[9] vdd gnd cell_6t
Xbit_r10_c13 bl[13] br[13] wl[10] vdd gnd cell_6t
Xbit_r11_c13 bl[13] br[13] wl[11] vdd gnd cell_6t
Xbit_r12_c13 bl[13] br[13] wl[12] vdd gnd cell_6t
Xbit_r13_c13 bl[13] br[13] wl[13] vdd gnd cell_6t
Xbit_r14_c13 bl[13] br[13] wl[14] vdd gnd cell_6t
Xbit_r15_c13 bl[13] br[13] wl[15] vdd gnd cell_6t
Xbit_r16_c13 bl[13] br[13] wl[16] vdd gnd cell_6t
Xbit_r17_c13 bl[13] br[13] wl[17] vdd gnd cell_6t
Xbit_r18_c13 bl[13] br[13] wl[18] vdd gnd cell_6t
Xbit_r19_c13 bl[13] br[13] wl[19] vdd gnd cell_6t
Xbit_r20_c13 bl[13] br[13] wl[20] vdd gnd cell_6t
Xbit_r21_c13 bl[13] br[13] wl[21] vdd gnd cell_6t
Xbit_r22_c13 bl[13] br[13] wl[22] vdd gnd cell_6t
Xbit_r23_c13 bl[13] br[13] wl[23] vdd gnd cell_6t
Xbit_r24_c13 bl[13] br[13] wl[24] vdd gnd cell_6t
Xbit_r25_c13 bl[13] br[13] wl[25] vdd gnd cell_6t
Xbit_r26_c13 bl[13] br[13] wl[26] vdd gnd cell_6t
Xbit_r27_c13 bl[13] br[13] wl[27] vdd gnd cell_6t
Xbit_r28_c13 bl[13] br[13] wl[28] vdd gnd cell_6t
Xbit_r29_c13 bl[13] br[13] wl[29] vdd gnd cell_6t
Xbit_r30_c13 bl[13] br[13] wl[30] vdd gnd cell_6t
Xbit_r31_c13 bl[13] br[13] wl[31] vdd gnd cell_6t
Xbit_r32_c13 bl[13] br[13] wl[32] vdd gnd cell_6t
Xbit_r33_c13 bl[13] br[13] wl[33] vdd gnd cell_6t
Xbit_r34_c13 bl[13] br[13] wl[34] vdd gnd cell_6t
Xbit_r35_c13 bl[13] br[13] wl[35] vdd gnd cell_6t
Xbit_r36_c13 bl[13] br[13] wl[36] vdd gnd cell_6t
Xbit_r37_c13 bl[13] br[13] wl[37] vdd gnd cell_6t
Xbit_r38_c13 bl[13] br[13] wl[38] vdd gnd cell_6t
Xbit_r39_c13 bl[13] br[13] wl[39] vdd gnd cell_6t
Xbit_r40_c13 bl[13] br[13] wl[40] vdd gnd cell_6t
Xbit_r41_c13 bl[13] br[13] wl[41] vdd gnd cell_6t
Xbit_r42_c13 bl[13] br[13] wl[42] vdd gnd cell_6t
Xbit_r43_c13 bl[13] br[13] wl[43] vdd gnd cell_6t
Xbit_r44_c13 bl[13] br[13] wl[44] vdd gnd cell_6t
Xbit_r45_c13 bl[13] br[13] wl[45] vdd gnd cell_6t
Xbit_r46_c13 bl[13] br[13] wl[46] vdd gnd cell_6t
Xbit_r47_c13 bl[13] br[13] wl[47] vdd gnd cell_6t
Xbit_r48_c13 bl[13] br[13] wl[48] vdd gnd cell_6t
Xbit_r49_c13 bl[13] br[13] wl[49] vdd gnd cell_6t
Xbit_r50_c13 bl[13] br[13] wl[50] vdd gnd cell_6t
Xbit_r51_c13 bl[13] br[13] wl[51] vdd gnd cell_6t
Xbit_r52_c13 bl[13] br[13] wl[52] vdd gnd cell_6t
Xbit_r53_c13 bl[13] br[13] wl[53] vdd gnd cell_6t
Xbit_r54_c13 bl[13] br[13] wl[54] vdd gnd cell_6t
Xbit_r55_c13 bl[13] br[13] wl[55] vdd gnd cell_6t
Xbit_r56_c13 bl[13] br[13] wl[56] vdd gnd cell_6t
Xbit_r57_c13 bl[13] br[13] wl[57] vdd gnd cell_6t
Xbit_r58_c13 bl[13] br[13] wl[58] vdd gnd cell_6t
Xbit_r59_c13 bl[13] br[13] wl[59] vdd gnd cell_6t
Xbit_r60_c13 bl[13] br[13] wl[60] vdd gnd cell_6t
Xbit_r61_c13 bl[13] br[13] wl[61] vdd gnd cell_6t
Xbit_r62_c13 bl[13] br[13] wl[62] vdd gnd cell_6t
Xbit_r63_c13 bl[13] br[13] wl[63] vdd gnd cell_6t
Xbit_r0_c14 bl[14] br[14] wl[0] vdd gnd cell_6t
Xbit_r1_c14 bl[14] br[14] wl[1] vdd gnd cell_6t
Xbit_r2_c14 bl[14] br[14] wl[2] vdd gnd cell_6t
Xbit_r3_c14 bl[14] br[14] wl[3] vdd gnd cell_6t
Xbit_r4_c14 bl[14] br[14] wl[4] vdd gnd cell_6t
Xbit_r5_c14 bl[14] br[14] wl[5] vdd gnd cell_6t
Xbit_r6_c14 bl[14] br[14] wl[6] vdd gnd cell_6t
Xbit_r7_c14 bl[14] br[14] wl[7] vdd gnd cell_6t
Xbit_r8_c14 bl[14] br[14] wl[8] vdd gnd cell_6t
Xbit_r9_c14 bl[14] br[14] wl[9] vdd gnd cell_6t
Xbit_r10_c14 bl[14] br[14] wl[10] vdd gnd cell_6t
Xbit_r11_c14 bl[14] br[14] wl[11] vdd gnd cell_6t
Xbit_r12_c14 bl[14] br[14] wl[12] vdd gnd cell_6t
Xbit_r13_c14 bl[14] br[14] wl[13] vdd gnd cell_6t
Xbit_r14_c14 bl[14] br[14] wl[14] vdd gnd cell_6t
Xbit_r15_c14 bl[14] br[14] wl[15] vdd gnd cell_6t
Xbit_r16_c14 bl[14] br[14] wl[16] vdd gnd cell_6t
Xbit_r17_c14 bl[14] br[14] wl[17] vdd gnd cell_6t
Xbit_r18_c14 bl[14] br[14] wl[18] vdd gnd cell_6t
Xbit_r19_c14 bl[14] br[14] wl[19] vdd gnd cell_6t
Xbit_r20_c14 bl[14] br[14] wl[20] vdd gnd cell_6t
Xbit_r21_c14 bl[14] br[14] wl[21] vdd gnd cell_6t
Xbit_r22_c14 bl[14] br[14] wl[22] vdd gnd cell_6t
Xbit_r23_c14 bl[14] br[14] wl[23] vdd gnd cell_6t
Xbit_r24_c14 bl[14] br[14] wl[24] vdd gnd cell_6t
Xbit_r25_c14 bl[14] br[14] wl[25] vdd gnd cell_6t
Xbit_r26_c14 bl[14] br[14] wl[26] vdd gnd cell_6t
Xbit_r27_c14 bl[14] br[14] wl[27] vdd gnd cell_6t
Xbit_r28_c14 bl[14] br[14] wl[28] vdd gnd cell_6t
Xbit_r29_c14 bl[14] br[14] wl[29] vdd gnd cell_6t
Xbit_r30_c14 bl[14] br[14] wl[30] vdd gnd cell_6t
Xbit_r31_c14 bl[14] br[14] wl[31] vdd gnd cell_6t
Xbit_r32_c14 bl[14] br[14] wl[32] vdd gnd cell_6t
Xbit_r33_c14 bl[14] br[14] wl[33] vdd gnd cell_6t
Xbit_r34_c14 bl[14] br[14] wl[34] vdd gnd cell_6t
Xbit_r35_c14 bl[14] br[14] wl[35] vdd gnd cell_6t
Xbit_r36_c14 bl[14] br[14] wl[36] vdd gnd cell_6t
Xbit_r37_c14 bl[14] br[14] wl[37] vdd gnd cell_6t
Xbit_r38_c14 bl[14] br[14] wl[38] vdd gnd cell_6t
Xbit_r39_c14 bl[14] br[14] wl[39] vdd gnd cell_6t
Xbit_r40_c14 bl[14] br[14] wl[40] vdd gnd cell_6t
Xbit_r41_c14 bl[14] br[14] wl[41] vdd gnd cell_6t
Xbit_r42_c14 bl[14] br[14] wl[42] vdd gnd cell_6t
Xbit_r43_c14 bl[14] br[14] wl[43] vdd gnd cell_6t
Xbit_r44_c14 bl[14] br[14] wl[44] vdd gnd cell_6t
Xbit_r45_c14 bl[14] br[14] wl[45] vdd gnd cell_6t
Xbit_r46_c14 bl[14] br[14] wl[46] vdd gnd cell_6t
Xbit_r47_c14 bl[14] br[14] wl[47] vdd gnd cell_6t
Xbit_r48_c14 bl[14] br[14] wl[48] vdd gnd cell_6t
Xbit_r49_c14 bl[14] br[14] wl[49] vdd gnd cell_6t
Xbit_r50_c14 bl[14] br[14] wl[50] vdd gnd cell_6t
Xbit_r51_c14 bl[14] br[14] wl[51] vdd gnd cell_6t
Xbit_r52_c14 bl[14] br[14] wl[52] vdd gnd cell_6t
Xbit_r53_c14 bl[14] br[14] wl[53] vdd gnd cell_6t
Xbit_r54_c14 bl[14] br[14] wl[54] vdd gnd cell_6t
Xbit_r55_c14 bl[14] br[14] wl[55] vdd gnd cell_6t
Xbit_r56_c14 bl[14] br[14] wl[56] vdd gnd cell_6t
Xbit_r57_c14 bl[14] br[14] wl[57] vdd gnd cell_6t
Xbit_r58_c14 bl[14] br[14] wl[58] vdd gnd cell_6t
Xbit_r59_c14 bl[14] br[14] wl[59] vdd gnd cell_6t
Xbit_r60_c14 bl[14] br[14] wl[60] vdd gnd cell_6t
Xbit_r61_c14 bl[14] br[14] wl[61] vdd gnd cell_6t
Xbit_r62_c14 bl[14] br[14] wl[62] vdd gnd cell_6t
Xbit_r63_c14 bl[14] br[14] wl[63] vdd gnd cell_6t
Xbit_r0_c15 bl[15] br[15] wl[0] vdd gnd cell_6t
Xbit_r1_c15 bl[15] br[15] wl[1] vdd gnd cell_6t
Xbit_r2_c15 bl[15] br[15] wl[2] vdd gnd cell_6t
Xbit_r3_c15 bl[15] br[15] wl[3] vdd gnd cell_6t
Xbit_r4_c15 bl[15] br[15] wl[4] vdd gnd cell_6t
Xbit_r5_c15 bl[15] br[15] wl[5] vdd gnd cell_6t
Xbit_r6_c15 bl[15] br[15] wl[6] vdd gnd cell_6t
Xbit_r7_c15 bl[15] br[15] wl[7] vdd gnd cell_6t
Xbit_r8_c15 bl[15] br[15] wl[8] vdd gnd cell_6t
Xbit_r9_c15 bl[15] br[15] wl[9] vdd gnd cell_6t
Xbit_r10_c15 bl[15] br[15] wl[10] vdd gnd cell_6t
Xbit_r11_c15 bl[15] br[15] wl[11] vdd gnd cell_6t
Xbit_r12_c15 bl[15] br[15] wl[12] vdd gnd cell_6t
Xbit_r13_c15 bl[15] br[15] wl[13] vdd gnd cell_6t
Xbit_r14_c15 bl[15] br[15] wl[14] vdd gnd cell_6t
Xbit_r15_c15 bl[15] br[15] wl[15] vdd gnd cell_6t
Xbit_r16_c15 bl[15] br[15] wl[16] vdd gnd cell_6t
Xbit_r17_c15 bl[15] br[15] wl[17] vdd gnd cell_6t
Xbit_r18_c15 bl[15] br[15] wl[18] vdd gnd cell_6t
Xbit_r19_c15 bl[15] br[15] wl[19] vdd gnd cell_6t
Xbit_r20_c15 bl[15] br[15] wl[20] vdd gnd cell_6t
Xbit_r21_c15 bl[15] br[15] wl[21] vdd gnd cell_6t
Xbit_r22_c15 bl[15] br[15] wl[22] vdd gnd cell_6t
Xbit_r23_c15 bl[15] br[15] wl[23] vdd gnd cell_6t
Xbit_r24_c15 bl[15] br[15] wl[24] vdd gnd cell_6t
Xbit_r25_c15 bl[15] br[15] wl[25] vdd gnd cell_6t
Xbit_r26_c15 bl[15] br[15] wl[26] vdd gnd cell_6t
Xbit_r27_c15 bl[15] br[15] wl[27] vdd gnd cell_6t
Xbit_r28_c15 bl[15] br[15] wl[28] vdd gnd cell_6t
Xbit_r29_c15 bl[15] br[15] wl[29] vdd gnd cell_6t
Xbit_r30_c15 bl[15] br[15] wl[30] vdd gnd cell_6t
Xbit_r31_c15 bl[15] br[15] wl[31] vdd gnd cell_6t
Xbit_r32_c15 bl[15] br[15] wl[32] vdd gnd cell_6t
Xbit_r33_c15 bl[15] br[15] wl[33] vdd gnd cell_6t
Xbit_r34_c15 bl[15] br[15] wl[34] vdd gnd cell_6t
Xbit_r35_c15 bl[15] br[15] wl[35] vdd gnd cell_6t
Xbit_r36_c15 bl[15] br[15] wl[36] vdd gnd cell_6t
Xbit_r37_c15 bl[15] br[15] wl[37] vdd gnd cell_6t
Xbit_r38_c15 bl[15] br[15] wl[38] vdd gnd cell_6t
Xbit_r39_c15 bl[15] br[15] wl[39] vdd gnd cell_6t
Xbit_r40_c15 bl[15] br[15] wl[40] vdd gnd cell_6t
Xbit_r41_c15 bl[15] br[15] wl[41] vdd gnd cell_6t
Xbit_r42_c15 bl[15] br[15] wl[42] vdd gnd cell_6t
Xbit_r43_c15 bl[15] br[15] wl[43] vdd gnd cell_6t
Xbit_r44_c15 bl[15] br[15] wl[44] vdd gnd cell_6t
Xbit_r45_c15 bl[15] br[15] wl[45] vdd gnd cell_6t
Xbit_r46_c15 bl[15] br[15] wl[46] vdd gnd cell_6t
Xbit_r47_c15 bl[15] br[15] wl[47] vdd gnd cell_6t
Xbit_r48_c15 bl[15] br[15] wl[48] vdd gnd cell_6t
Xbit_r49_c15 bl[15] br[15] wl[49] vdd gnd cell_6t
Xbit_r50_c15 bl[15] br[15] wl[50] vdd gnd cell_6t
Xbit_r51_c15 bl[15] br[15] wl[51] vdd gnd cell_6t
Xbit_r52_c15 bl[15] br[15] wl[52] vdd gnd cell_6t
Xbit_r53_c15 bl[15] br[15] wl[53] vdd gnd cell_6t
Xbit_r54_c15 bl[15] br[15] wl[54] vdd gnd cell_6t
Xbit_r55_c15 bl[15] br[15] wl[55] vdd gnd cell_6t
Xbit_r56_c15 bl[15] br[15] wl[56] vdd gnd cell_6t
Xbit_r57_c15 bl[15] br[15] wl[57] vdd gnd cell_6t
Xbit_r58_c15 bl[15] br[15] wl[58] vdd gnd cell_6t
Xbit_r59_c15 bl[15] br[15] wl[59] vdd gnd cell_6t
Xbit_r60_c15 bl[15] br[15] wl[60] vdd gnd cell_6t
Xbit_r61_c15 bl[15] br[15] wl[61] vdd gnd cell_6t
Xbit_r62_c15 bl[15] br[15] wl[62] vdd gnd cell_6t
Xbit_r63_c15 bl[15] br[15] wl[63] vdd gnd cell_6t
Xbit_r0_c16 bl[16] br[16] wl[0] vdd gnd cell_6t
Xbit_r1_c16 bl[16] br[16] wl[1] vdd gnd cell_6t
Xbit_r2_c16 bl[16] br[16] wl[2] vdd gnd cell_6t
Xbit_r3_c16 bl[16] br[16] wl[3] vdd gnd cell_6t
Xbit_r4_c16 bl[16] br[16] wl[4] vdd gnd cell_6t
Xbit_r5_c16 bl[16] br[16] wl[5] vdd gnd cell_6t
Xbit_r6_c16 bl[16] br[16] wl[6] vdd gnd cell_6t
Xbit_r7_c16 bl[16] br[16] wl[7] vdd gnd cell_6t
Xbit_r8_c16 bl[16] br[16] wl[8] vdd gnd cell_6t
Xbit_r9_c16 bl[16] br[16] wl[9] vdd gnd cell_6t
Xbit_r10_c16 bl[16] br[16] wl[10] vdd gnd cell_6t
Xbit_r11_c16 bl[16] br[16] wl[11] vdd gnd cell_6t
Xbit_r12_c16 bl[16] br[16] wl[12] vdd gnd cell_6t
Xbit_r13_c16 bl[16] br[16] wl[13] vdd gnd cell_6t
Xbit_r14_c16 bl[16] br[16] wl[14] vdd gnd cell_6t
Xbit_r15_c16 bl[16] br[16] wl[15] vdd gnd cell_6t
Xbit_r16_c16 bl[16] br[16] wl[16] vdd gnd cell_6t
Xbit_r17_c16 bl[16] br[16] wl[17] vdd gnd cell_6t
Xbit_r18_c16 bl[16] br[16] wl[18] vdd gnd cell_6t
Xbit_r19_c16 bl[16] br[16] wl[19] vdd gnd cell_6t
Xbit_r20_c16 bl[16] br[16] wl[20] vdd gnd cell_6t
Xbit_r21_c16 bl[16] br[16] wl[21] vdd gnd cell_6t
Xbit_r22_c16 bl[16] br[16] wl[22] vdd gnd cell_6t
Xbit_r23_c16 bl[16] br[16] wl[23] vdd gnd cell_6t
Xbit_r24_c16 bl[16] br[16] wl[24] vdd gnd cell_6t
Xbit_r25_c16 bl[16] br[16] wl[25] vdd gnd cell_6t
Xbit_r26_c16 bl[16] br[16] wl[26] vdd gnd cell_6t
Xbit_r27_c16 bl[16] br[16] wl[27] vdd gnd cell_6t
Xbit_r28_c16 bl[16] br[16] wl[28] vdd gnd cell_6t
Xbit_r29_c16 bl[16] br[16] wl[29] vdd gnd cell_6t
Xbit_r30_c16 bl[16] br[16] wl[30] vdd gnd cell_6t
Xbit_r31_c16 bl[16] br[16] wl[31] vdd gnd cell_6t
Xbit_r32_c16 bl[16] br[16] wl[32] vdd gnd cell_6t
Xbit_r33_c16 bl[16] br[16] wl[33] vdd gnd cell_6t
Xbit_r34_c16 bl[16] br[16] wl[34] vdd gnd cell_6t
Xbit_r35_c16 bl[16] br[16] wl[35] vdd gnd cell_6t
Xbit_r36_c16 bl[16] br[16] wl[36] vdd gnd cell_6t
Xbit_r37_c16 bl[16] br[16] wl[37] vdd gnd cell_6t
Xbit_r38_c16 bl[16] br[16] wl[38] vdd gnd cell_6t
Xbit_r39_c16 bl[16] br[16] wl[39] vdd gnd cell_6t
Xbit_r40_c16 bl[16] br[16] wl[40] vdd gnd cell_6t
Xbit_r41_c16 bl[16] br[16] wl[41] vdd gnd cell_6t
Xbit_r42_c16 bl[16] br[16] wl[42] vdd gnd cell_6t
Xbit_r43_c16 bl[16] br[16] wl[43] vdd gnd cell_6t
Xbit_r44_c16 bl[16] br[16] wl[44] vdd gnd cell_6t
Xbit_r45_c16 bl[16] br[16] wl[45] vdd gnd cell_6t
Xbit_r46_c16 bl[16] br[16] wl[46] vdd gnd cell_6t
Xbit_r47_c16 bl[16] br[16] wl[47] vdd gnd cell_6t
Xbit_r48_c16 bl[16] br[16] wl[48] vdd gnd cell_6t
Xbit_r49_c16 bl[16] br[16] wl[49] vdd gnd cell_6t
Xbit_r50_c16 bl[16] br[16] wl[50] vdd gnd cell_6t
Xbit_r51_c16 bl[16] br[16] wl[51] vdd gnd cell_6t
Xbit_r52_c16 bl[16] br[16] wl[52] vdd gnd cell_6t
Xbit_r53_c16 bl[16] br[16] wl[53] vdd gnd cell_6t
Xbit_r54_c16 bl[16] br[16] wl[54] vdd gnd cell_6t
Xbit_r55_c16 bl[16] br[16] wl[55] vdd gnd cell_6t
Xbit_r56_c16 bl[16] br[16] wl[56] vdd gnd cell_6t
Xbit_r57_c16 bl[16] br[16] wl[57] vdd gnd cell_6t
Xbit_r58_c16 bl[16] br[16] wl[58] vdd gnd cell_6t
Xbit_r59_c16 bl[16] br[16] wl[59] vdd gnd cell_6t
Xbit_r60_c16 bl[16] br[16] wl[60] vdd gnd cell_6t
Xbit_r61_c16 bl[16] br[16] wl[61] vdd gnd cell_6t
Xbit_r62_c16 bl[16] br[16] wl[62] vdd gnd cell_6t
Xbit_r63_c16 bl[16] br[16] wl[63] vdd gnd cell_6t
Xbit_r0_c17 bl[17] br[17] wl[0] vdd gnd cell_6t
Xbit_r1_c17 bl[17] br[17] wl[1] vdd gnd cell_6t
Xbit_r2_c17 bl[17] br[17] wl[2] vdd gnd cell_6t
Xbit_r3_c17 bl[17] br[17] wl[3] vdd gnd cell_6t
Xbit_r4_c17 bl[17] br[17] wl[4] vdd gnd cell_6t
Xbit_r5_c17 bl[17] br[17] wl[5] vdd gnd cell_6t
Xbit_r6_c17 bl[17] br[17] wl[6] vdd gnd cell_6t
Xbit_r7_c17 bl[17] br[17] wl[7] vdd gnd cell_6t
Xbit_r8_c17 bl[17] br[17] wl[8] vdd gnd cell_6t
Xbit_r9_c17 bl[17] br[17] wl[9] vdd gnd cell_6t
Xbit_r10_c17 bl[17] br[17] wl[10] vdd gnd cell_6t
Xbit_r11_c17 bl[17] br[17] wl[11] vdd gnd cell_6t
Xbit_r12_c17 bl[17] br[17] wl[12] vdd gnd cell_6t
Xbit_r13_c17 bl[17] br[17] wl[13] vdd gnd cell_6t
Xbit_r14_c17 bl[17] br[17] wl[14] vdd gnd cell_6t
Xbit_r15_c17 bl[17] br[17] wl[15] vdd gnd cell_6t
Xbit_r16_c17 bl[17] br[17] wl[16] vdd gnd cell_6t
Xbit_r17_c17 bl[17] br[17] wl[17] vdd gnd cell_6t
Xbit_r18_c17 bl[17] br[17] wl[18] vdd gnd cell_6t
Xbit_r19_c17 bl[17] br[17] wl[19] vdd gnd cell_6t
Xbit_r20_c17 bl[17] br[17] wl[20] vdd gnd cell_6t
Xbit_r21_c17 bl[17] br[17] wl[21] vdd gnd cell_6t
Xbit_r22_c17 bl[17] br[17] wl[22] vdd gnd cell_6t
Xbit_r23_c17 bl[17] br[17] wl[23] vdd gnd cell_6t
Xbit_r24_c17 bl[17] br[17] wl[24] vdd gnd cell_6t
Xbit_r25_c17 bl[17] br[17] wl[25] vdd gnd cell_6t
Xbit_r26_c17 bl[17] br[17] wl[26] vdd gnd cell_6t
Xbit_r27_c17 bl[17] br[17] wl[27] vdd gnd cell_6t
Xbit_r28_c17 bl[17] br[17] wl[28] vdd gnd cell_6t
Xbit_r29_c17 bl[17] br[17] wl[29] vdd gnd cell_6t
Xbit_r30_c17 bl[17] br[17] wl[30] vdd gnd cell_6t
Xbit_r31_c17 bl[17] br[17] wl[31] vdd gnd cell_6t
Xbit_r32_c17 bl[17] br[17] wl[32] vdd gnd cell_6t
Xbit_r33_c17 bl[17] br[17] wl[33] vdd gnd cell_6t
Xbit_r34_c17 bl[17] br[17] wl[34] vdd gnd cell_6t
Xbit_r35_c17 bl[17] br[17] wl[35] vdd gnd cell_6t
Xbit_r36_c17 bl[17] br[17] wl[36] vdd gnd cell_6t
Xbit_r37_c17 bl[17] br[17] wl[37] vdd gnd cell_6t
Xbit_r38_c17 bl[17] br[17] wl[38] vdd gnd cell_6t
Xbit_r39_c17 bl[17] br[17] wl[39] vdd gnd cell_6t
Xbit_r40_c17 bl[17] br[17] wl[40] vdd gnd cell_6t
Xbit_r41_c17 bl[17] br[17] wl[41] vdd gnd cell_6t
Xbit_r42_c17 bl[17] br[17] wl[42] vdd gnd cell_6t
Xbit_r43_c17 bl[17] br[17] wl[43] vdd gnd cell_6t
Xbit_r44_c17 bl[17] br[17] wl[44] vdd gnd cell_6t
Xbit_r45_c17 bl[17] br[17] wl[45] vdd gnd cell_6t
Xbit_r46_c17 bl[17] br[17] wl[46] vdd gnd cell_6t
Xbit_r47_c17 bl[17] br[17] wl[47] vdd gnd cell_6t
Xbit_r48_c17 bl[17] br[17] wl[48] vdd gnd cell_6t
Xbit_r49_c17 bl[17] br[17] wl[49] vdd gnd cell_6t
Xbit_r50_c17 bl[17] br[17] wl[50] vdd gnd cell_6t
Xbit_r51_c17 bl[17] br[17] wl[51] vdd gnd cell_6t
Xbit_r52_c17 bl[17] br[17] wl[52] vdd gnd cell_6t
Xbit_r53_c17 bl[17] br[17] wl[53] vdd gnd cell_6t
Xbit_r54_c17 bl[17] br[17] wl[54] vdd gnd cell_6t
Xbit_r55_c17 bl[17] br[17] wl[55] vdd gnd cell_6t
Xbit_r56_c17 bl[17] br[17] wl[56] vdd gnd cell_6t
Xbit_r57_c17 bl[17] br[17] wl[57] vdd gnd cell_6t
Xbit_r58_c17 bl[17] br[17] wl[58] vdd gnd cell_6t
Xbit_r59_c17 bl[17] br[17] wl[59] vdd gnd cell_6t
Xbit_r60_c17 bl[17] br[17] wl[60] vdd gnd cell_6t
Xbit_r61_c17 bl[17] br[17] wl[61] vdd gnd cell_6t
Xbit_r62_c17 bl[17] br[17] wl[62] vdd gnd cell_6t
Xbit_r63_c17 bl[17] br[17] wl[63] vdd gnd cell_6t
Xbit_r0_c18 bl[18] br[18] wl[0] vdd gnd cell_6t
Xbit_r1_c18 bl[18] br[18] wl[1] vdd gnd cell_6t
Xbit_r2_c18 bl[18] br[18] wl[2] vdd gnd cell_6t
Xbit_r3_c18 bl[18] br[18] wl[3] vdd gnd cell_6t
Xbit_r4_c18 bl[18] br[18] wl[4] vdd gnd cell_6t
Xbit_r5_c18 bl[18] br[18] wl[5] vdd gnd cell_6t
Xbit_r6_c18 bl[18] br[18] wl[6] vdd gnd cell_6t
Xbit_r7_c18 bl[18] br[18] wl[7] vdd gnd cell_6t
Xbit_r8_c18 bl[18] br[18] wl[8] vdd gnd cell_6t
Xbit_r9_c18 bl[18] br[18] wl[9] vdd gnd cell_6t
Xbit_r10_c18 bl[18] br[18] wl[10] vdd gnd cell_6t
Xbit_r11_c18 bl[18] br[18] wl[11] vdd gnd cell_6t
Xbit_r12_c18 bl[18] br[18] wl[12] vdd gnd cell_6t
Xbit_r13_c18 bl[18] br[18] wl[13] vdd gnd cell_6t
Xbit_r14_c18 bl[18] br[18] wl[14] vdd gnd cell_6t
Xbit_r15_c18 bl[18] br[18] wl[15] vdd gnd cell_6t
Xbit_r16_c18 bl[18] br[18] wl[16] vdd gnd cell_6t
Xbit_r17_c18 bl[18] br[18] wl[17] vdd gnd cell_6t
Xbit_r18_c18 bl[18] br[18] wl[18] vdd gnd cell_6t
Xbit_r19_c18 bl[18] br[18] wl[19] vdd gnd cell_6t
Xbit_r20_c18 bl[18] br[18] wl[20] vdd gnd cell_6t
Xbit_r21_c18 bl[18] br[18] wl[21] vdd gnd cell_6t
Xbit_r22_c18 bl[18] br[18] wl[22] vdd gnd cell_6t
Xbit_r23_c18 bl[18] br[18] wl[23] vdd gnd cell_6t
Xbit_r24_c18 bl[18] br[18] wl[24] vdd gnd cell_6t
Xbit_r25_c18 bl[18] br[18] wl[25] vdd gnd cell_6t
Xbit_r26_c18 bl[18] br[18] wl[26] vdd gnd cell_6t
Xbit_r27_c18 bl[18] br[18] wl[27] vdd gnd cell_6t
Xbit_r28_c18 bl[18] br[18] wl[28] vdd gnd cell_6t
Xbit_r29_c18 bl[18] br[18] wl[29] vdd gnd cell_6t
Xbit_r30_c18 bl[18] br[18] wl[30] vdd gnd cell_6t
Xbit_r31_c18 bl[18] br[18] wl[31] vdd gnd cell_6t
Xbit_r32_c18 bl[18] br[18] wl[32] vdd gnd cell_6t
Xbit_r33_c18 bl[18] br[18] wl[33] vdd gnd cell_6t
Xbit_r34_c18 bl[18] br[18] wl[34] vdd gnd cell_6t
Xbit_r35_c18 bl[18] br[18] wl[35] vdd gnd cell_6t
Xbit_r36_c18 bl[18] br[18] wl[36] vdd gnd cell_6t
Xbit_r37_c18 bl[18] br[18] wl[37] vdd gnd cell_6t
Xbit_r38_c18 bl[18] br[18] wl[38] vdd gnd cell_6t
Xbit_r39_c18 bl[18] br[18] wl[39] vdd gnd cell_6t
Xbit_r40_c18 bl[18] br[18] wl[40] vdd gnd cell_6t
Xbit_r41_c18 bl[18] br[18] wl[41] vdd gnd cell_6t
Xbit_r42_c18 bl[18] br[18] wl[42] vdd gnd cell_6t
Xbit_r43_c18 bl[18] br[18] wl[43] vdd gnd cell_6t
Xbit_r44_c18 bl[18] br[18] wl[44] vdd gnd cell_6t
Xbit_r45_c18 bl[18] br[18] wl[45] vdd gnd cell_6t
Xbit_r46_c18 bl[18] br[18] wl[46] vdd gnd cell_6t
Xbit_r47_c18 bl[18] br[18] wl[47] vdd gnd cell_6t
Xbit_r48_c18 bl[18] br[18] wl[48] vdd gnd cell_6t
Xbit_r49_c18 bl[18] br[18] wl[49] vdd gnd cell_6t
Xbit_r50_c18 bl[18] br[18] wl[50] vdd gnd cell_6t
Xbit_r51_c18 bl[18] br[18] wl[51] vdd gnd cell_6t
Xbit_r52_c18 bl[18] br[18] wl[52] vdd gnd cell_6t
Xbit_r53_c18 bl[18] br[18] wl[53] vdd gnd cell_6t
Xbit_r54_c18 bl[18] br[18] wl[54] vdd gnd cell_6t
Xbit_r55_c18 bl[18] br[18] wl[55] vdd gnd cell_6t
Xbit_r56_c18 bl[18] br[18] wl[56] vdd gnd cell_6t
Xbit_r57_c18 bl[18] br[18] wl[57] vdd gnd cell_6t
Xbit_r58_c18 bl[18] br[18] wl[58] vdd gnd cell_6t
Xbit_r59_c18 bl[18] br[18] wl[59] vdd gnd cell_6t
Xbit_r60_c18 bl[18] br[18] wl[60] vdd gnd cell_6t
Xbit_r61_c18 bl[18] br[18] wl[61] vdd gnd cell_6t
Xbit_r62_c18 bl[18] br[18] wl[62] vdd gnd cell_6t
Xbit_r63_c18 bl[18] br[18] wl[63] vdd gnd cell_6t
Xbit_r0_c19 bl[19] br[19] wl[0] vdd gnd cell_6t
Xbit_r1_c19 bl[19] br[19] wl[1] vdd gnd cell_6t
Xbit_r2_c19 bl[19] br[19] wl[2] vdd gnd cell_6t
Xbit_r3_c19 bl[19] br[19] wl[3] vdd gnd cell_6t
Xbit_r4_c19 bl[19] br[19] wl[4] vdd gnd cell_6t
Xbit_r5_c19 bl[19] br[19] wl[5] vdd gnd cell_6t
Xbit_r6_c19 bl[19] br[19] wl[6] vdd gnd cell_6t
Xbit_r7_c19 bl[19] br[19] wl[7] vdd gnd cell_6t
Xbit_r8_c19 bl[19] br[19] wl[8] vdd gnd cell_6t
Xbit_r9_c19 bl[19] br[19] wl[9] vdd gnd cell_6t
Xbit_r10_c19 bl[19] br[19] wl[10] vdd gnd cell_6t
Xbit_r11_c19 bl[19] br[19] wl[11] vdd gnd cell_6t
Xbit_r12_c19 bl[19] br[19] wl[12] vdd gnd cell_6t
Xbit_r13_c19 bl[19] br[19] wl[13] vdd gnd cell_6t
Xbit_r14_c19 bl[19] br[19] wl[14] vdd gnd cell_6t
Xbit_r15_c19 bl[19] br[19] wl[15] vdd gnd cell_6t
Xbit_r16_c19 bl[19] br[19] wl[16] vdd gnd cell_6t
Xbit_r17_c19 bl[19] br[19] wl[17] vdd gnd cell_6t
Xbit_r18_c19 bl[19] br[19] wl[18] vdd gnd cell_6t
Xbit_r19_c19 bl[19] br[19] wl[19] vdd gnd cell_6t
Xbit_r20_c19 bl[19] br[19] wl[20] vdd gnd cell_6t
Xbit_r21_c19 bl[19] br[19] wl[21] vdd gnd cell_6t
Xbit_r22_c19 bl[19] br[19] wl[22] vdd gnd cell_6t
Xbit_r23_c19 bl[19] br[19] wl[23] vdd gnd cell_6t
Xbit_r24_c19 bl[19] br[19] wl[24] vdd gnd cell_6t
Xbit_r25_c19 bl[19] br[19] wl[25] vdd gnd cell_6t
Xbit_r26_c19 bl[19] br[19] wl[26] vdd gnd cell_6t
Xbit_r27_c19 bl[19] br[19] wl[27] vdd gnd cell_6t
Xbit_r28_c19 bl[19] br[19] wl[28] vdd gnd cell_6t
Xbit_r29_c19 bl[19] br[19] wl[29] vdd gnd cell_6t
Xbit_r30_c19 bl[19] br[19] wl[30] vdd gnd cell_6t
Xbit_r31_c19 bl[19] br[19] wl[31] vdd gnd cell_6t
Xbit_r32_c19 bl[19] br[19] wl[32] vdd gnd cell_6t
Xbit_r33_c19 bl[19] br[19] wl[33] vdd gnd cell_6t
Xbit_r34_c19 bl[19] br[19] wl[34] vdd gnd cell_6t
Xbit_r35_c19 bl[19] br[19] wl[35] vdd gnd cell_6t
Xbit_r36_c19 bl[19] br[19] wl[36] vdd gnd cell_6t
Xbit_r37_c19 bl[19] br[19] wl[37] vdd gnd cell_6t
Xbit_r38_c19 bl[19] br[19] wl[38] vdd gnd cell_6t
Xbit_r39_c19 bl[19] br[19] wl[39] vdd gnd cell_6t
Xbit_r40_c19 bl[19] br[19] wl[40] vdd gnd cell_6t
Xbit_r41_c19 bl[19] br[19] wl[41] vdd gnd cell_6t
Xbit_r42_c19 bl[19] br[19] wl[42] vdd gnd cell_6t
Xbit_r43_c19 bl[19] br[19] wl[43] vdd gnd cell_6t
Xbit_r44_c19 bl[19] br[19] wl[44] vdd gnd cell_6t
Xbit_r45_c19 bl[19] br[19] wl[45] vdd gnd cell_6t
Xbit_r46_c19 bl[19] br[19] wl[46] vdd gnd cell_6t
Xbit_r47_c19 bl[19] br[19] wl[47] vdd gnd cell_6t
Xbit_r48_c19 bl[19] br[19] wl[48] vdd gnd cell_6t
Xbit_r49_c19 bl[19] br[19] wl[49] vdd gnd cell_6t
Xbit_r50_c19 bl[19] br[19] wl[50] vdd gnd cell_6t
Xbit_r51_c19 bl[19] br[19] wl[51] vdd gnd cell_6t
Xbit_r52_c19 bl[19] br[19] wl[52] vdd gnd cell_6t
Xbit_r53_c19 bl[19] br[19] wl[53] vdd gnd cell_6t
Xbit_r54_c19 bl[19] br[19] wl[54] vdd gnd cell_6t
Xbit_r55_c19 bl[19] br[19] wl[55] vdd gnd cell_6t
Xbit_r56_c19 bl[19] br[19] wl[56] vdd gnd cell_6t
Xbit_r57_c19 bl[19] br[19] wl[57] vdd gnd cell_6t
Xbit_r58_c19 bl[19] br[19] wl[58] vdd gnd cell_6t
Xbit_r59_c19 bl[19] br[19] wl[59] vdd gnd cell_6t
Xbit_r60_c19 bl[19] br[19] wl[60] vdd gnd cell_6t
Xbit_r61_c19 bl[19] br[19] wl[61] vdd gnd cell_6t
Xbit_r62_c19 bl[19] br[19] wl[62] vdd gnd cell_6t
Xbit_r63_c19 bl[19] br[19] wl[63] vdd gnd cell_6t
Xbit_r0_c20 bl[20] br[20] wl[0] vdd gnd cell_6t
Xbit_r1_c20 bl[20] br[20] wl[1] vdd gnd cell_6t
Xbit_r2_c20 bl[20] br[20] wl[2] vdd gnd cell_6t
Xbit_r3_c20 bl[20] br[20] wl[3] vdd gnd cell_6t
Xbit_r4_c20 bl[20] br[20] wl[4] vdd gnd cell_6t
Xbit_r5_c20 bl[20] br[20] wl[5] vdd gnd cell_6t
Xbit_r6_c20 bl[20] br[20] wl[6] vdd gnd cell_6t
Xbit_r7_c20 bl[20] br[20] wl[7] vdd gnd cell_6t
Xbit_r8_c20 bl[20] br[20] wl[8] vdd gnd cell_6t
Xbit_r9_c20 bl[20] br[20] wl[9] vdd gnd cell_6t
Xbit_r10_c20 bl[20] br[20] wl[10] vdd gnd cell_6t
Xbit_r11_c20 bl[20] br[20] wl[11] vdd gnd cell_6t
Xbit_r12_c20 bl[20] br[20] wl[12] vdd gnd cell_6t
Xbit_r13_c20 bl[20] br[20] wl[13] vdd gnd cell_6t
Xbit_r14_c20 bl[20] br[20] wl[14] vdd gnd cell_6t
Xbit_r15_c20 bl[20] br[20] wl[15] vdd gnd cell_6t
Xbit_r16_c20 bl[20] br[20] wl[16] vdd gnd cell_6t
Xbit_r17_c20 bl[20] br[20] wl[17] vdd gnd cell_6t
Xbit_r18_c20 bl[20] br[20] wl[18] vdd gnd cell_6t
Xbit_r19_c20 bl[20] br[20] wl[19] vdd gnd cell_6t
Xbit_r20_c20 bl[20] br[20] wl[20] vdd gnd cell_6t
Xbit_r21_c20 bl[20] br[20] wl[21] vdd gnd cell_6t
Xbit_r22_c20 bl[20] br[20] wl[22] vdd gnd cell_6t
Xbit_r23_c20 bl[20] br[20] wl[23] vdd gnd cell_6t
Xbit_r24_c20 bl[20] br[20] wl[24] vdd gnd cell_6t
Xbit_r25_c20 bl[20] br[20] wl[25] vdd gnd cell_6t
Xbit_r26_c20 bl[20] br[20] wl[26] vdd gnd cell_6t
Xbit_r27_c20 bl[20] br[20] wl[27] vdd gnd cell_6t
Xbit_r28_c20 bl[20] br[20] wl[28] vdd gnd cell_6t
Xbit_r29_c20 bl[20] br[20] wl[29] vdd gnd cell_6t
Xbit_r30_c20 bl[20] br[20] wl[30] vdd gnd cell_6t
Xbit_r31_c20 bl[20] br[20] wl[31] vdd gnd cell_6t
Xbit_r32_c20 bl[20] br[20] wl[32] vdd gnd cell_6t
Xbit_r33_c20 bl[20] br[20] wl[33] vdd gnd cell_6t
Xbit_r34_c20 bl[20] br[20] wl[34] vdd gnd cell_6t
Xbit_r35_c20 bl[20] br[20] wl[35] vdd gnd cell_6t
Xbit_r36_c20 bl[20] br[20] wl[36] vdd gnd cell_6t
Xbit_r37_c20 bl[20] br[20] wl[37] vdd gnd cell_6t
Xbit_r38_c20 bl[20] br[20] wl[38] vdd gnd cell_6t
Xbit_r39_c20 bl[20] br[20] wl[39] vdd gnd cell_6t
Xbit_r40_c20 bl[20] br[20] wl[40] vdd gnd cell_6t
Xbit_r41_c20 bl[20] br[20] wl[41] vdd gnd cell_6t
Xbit_r42_c20 bl[20] br[20] wl[42] vdd gnd cell_6t
Xbit_r43_c20 bl[20] br[20] wl[43] vdd gnd cell_6t
Xbit_r44_c20 bl[20] br[20] wl[44] vdd gnd cell_6t
Xbit_r45_c20 bl[20] br[20] wl[45] vdd gnd cell_6t
Xbit_r46_c20 bl[20] br[20] wl[46] vdd gnd cell_6t
Xbit_r47_c20 bl[20] br[20] wl[47] vdd gnd cell_6t
Xbit_r48_c20 bl[20] br[20] wl[48] vdd gnd cell_6t
Xbit_r49_c20 bl[20] br[20] wl[49] vdd gnd cell_6t
Xbit_r50_c20 bl[20] br[20] wl[50] vdd gnd cell_6t
Xbit_r51_c20 bl[20] br[20] wl[51] vdd gnd cell_6t
Xbit_r52_c20 bl[20] br[20] wl[52] vdd gnd cell_6t
Xbit_r53_c20 bl[20] br[20] wl[53] vdd gnd cell_6t
Xbit_r54_c20 bl[20] br[20] wl[54] vdd gnd cell_6t
Xbit_r55_c20 bl[20] br[20] wl[55] vdd gnd cell_6t
Xbit_r56_c20 bl[20] br[20] wl[56] vdd gnd cell_6t
Xbit_r57_c20 bl[20] br[20] wl[57] vdd gnd cell_6t
Xbit_r58_c20 bl[20] br[20] wl[58] vdd gnd cell_6t
Xbit_r59_c20 bl[20] br[20] wl[59] vdd gnd cell_6t
Xbit_r60_c20 bl[20] br[20] wl[60] vdd gnd cell_6t
Xbit_r61_c20 bl[20] br[20] wl[61] vdd gnd cell_6t
Xbit_r62_c20 bl[20] br[20] wl[62] vdd gnd cell_6t
Xbit_r63_c20 bl[20] br[20] wl[63] vdd gnd cell_6t
Xbit_r0_c21 bl[21] br[21] wl[0] vdd gnd cell_6t
Xbit_r1_c21 bl[21] br[21] wl[1] vdd gnd cell_6t
Xbit_r2_c21 bl[21] br[21] wl[2] vdd gnd cell_6t
Xbit_r3_c21 bl[21] br[21] wl[3] vdd gnd cell_6t
Xbit_r4_c21 bl[21] br[21] wl[4] vdd gnd cell_6t
Xbit_r5_c21 bl[21] br[21] wl[5] vdd gnd cell_6t
Xbit_r6_c21 bl[21] br[21] wl[6] vdd gnd cell_6t
Xbit_r7_c21 bl[21] br[21] wl[7] vdd gnd cell_6t
Xbit_r8_c21 bl[21] br[21] wl[8] vdd gnd cell_6t
Xbit_r9_c21 bl[21] br[21] wl[9] vdd gnd cell_6t
Xbit_r10_c21 bl[21] br[21] wl[10] vdd gnd cell_6t
Xbit_r11_c21 bl[21] br[21] wl[11] vdd gnd cell_6t
Xbit_r12_c21 bl[21] br[21] wl[12] vdd gnd cell_6t
Xbit_r13_c21 bl[21] br[21] wl[13] vdd gnd cell_6t
Xbit_r14_c21 bl[21] br[21] wl[14] vdd gnd cell_6t
Xbit_r15_c21 bl[21] br[21] wl[15] vdd gnd cell_6t
Xbit_r16_c21 bl[21] br[21] wl[16] vdd gnd cell_6t
Xbit_r17_c21 bl[21] br[21] wl[17] vdd gnd cell_6t
Xbit_r18_c21 bl[21] br[21] wl[18] vdd gnd cell_6t
Xbit_r19_c21 bl[21] br[21] wl[19] vdd gnd cell_6t
Xbit_r20_c21 bl[21] br[21] wl[20] vdd gnd cell_6t
Xbit_r21_c21 bl[21] br[21] wl[21] vdd gnd cell_6t
Xbit_r22_c21 bl[21] br[21] wl[22] vdd gnd cell_6t
Xbit_r23_c21 bl[21] br[21] wl[23] vdd gnd cell_6t
Xbit_r24_c21 bl[21] br[21] wl[24] vdd gnd cell_6t
Xbit_r25_c21 bl[21] br[21] wl[25] vdd gnd cell_6t
Xbit_r26_c21 bl[21] br[21] wl[26] vdd gnd cell_6t
Xbit_r27_c21 bl[21] br[21] wl[27] vdd gnd cell_6t
Xbit_r28_c21 bl[21] br[21] wl[28] vdd gnd cell_6t
Xbit_r29_c21 bl[21] br[21] wl[29] vdd gnd cell_6t
Xbit_r30_c21 bl[21] br[21] wl[30] vdd gnd cell_6t
Xbit_r31_c21 bl[21] br[21] wl[31] vdd gnd cell_6t
Xbit_r32_c21 bl[21] br[21] wl[32] vdd gnd cell_6t
Xbit_r33_c21 bl[21] br[21] wl[33] vdd gnd cell_6t
Xbit_r34_c21 bl[21] br[21] wl[34] vdd gnd cell_6t
Xbit_r35_c21 bl[21] br[21] wl[35] vdd gnd cell_6t
Xbit_r36_c21 bl[21] br[21] wl[36] vdd gnd cell_6t
Xbit_r37_c21 bl[21] br[21] wl[37] vdd gnd cell_6t
Xbit_r38_c21 bl[21] br[21] wl[38] vdd gnd cell_6t
Xbit_r39_c21 bl[21] br[21] wl[39] vdd gnd cell_6t
Xbit_r40_c21 bl[21] br[21] wl[40] vdd gnd cell_6t
Xbit_r41_c21 bl[21] br[21] wl[41] vdd gnd cell_6t
Xbit_r42_c21 bl[21] br[21] wl[42] vdd gnd cell_6t
Xbit_r43_c21 bl[21] br[21] wl[43] vdd gnd cell_6t
Xbit_r44_c21 bl[21] br[21] wl[44] vdd gnd cell_6t
Xbit_r45_c21 bl[21] br[21] wl[45] vdd gnd cell_6t
Xbit_r46_c21 bl[21] br[21] wl[46] vdd gnd cell_6t
Xbit_r47_c21 bl[21] br[21] wl[47] vdd gnd cell_6t
Xbit_r48_c21 bl[21] br[21] wl[48] vdd gnd cell_6t
Xbit_r49_c21 bl[21] br[21] wl[49] vdd gnd cell_6t
Xbit_r50_c21 bl[21] br[21] wl[50] vdd gnd cell_6t
Xbit_r51_c21 bl[21] br[21] wl[51] vdd gnd cell_6t
Xbit_r52_c21 bl[21] br[21] wl[52] vdd gnd cell_6t
Xbit_r53_c21 bl[21] br[21] wl[53] vdd gnd cell_6t
Xbit_r54_c21 bl[21] br[21] wl[54] vdd gnd cell_6t
Xbit_r55_c21 bl[21] br[21] wl[55] vdd gnd cell_6t
Xbit_r56_c21 bl[21] br[21] wl[56] vdd gnd cell_6t
Xbit_r57_c21 bl[21] br[21] wl[57] vdd gnd cell_6t
Xbit_r58_c21 bl[21] br[21] wl[58] vdd gnd cell_6t
Xbit_r59_c21 bl[21] br[21] wl[59] vdd gnd cell_6t
Xbit_r60_c21 bl[21] br[21] wl[60] vdd gnd cell_6t
Xbit_r61_c21 bl[21] br[21] wl[61] vdd gnd cell_6t
Xbit_r62_c21 bl[21] br[21] wl[62] vdd gnd cell_6t
Xbit_r63_c21 bl[21] br[21] wl[63] vdd gnd cell_6t
Xbit_r0_c22 bl[22] br[22] wl[0] vdd gnd cell_6t
Xbit_r1_c22 bl[22] br[22] wl[1] vdd gnd cell_6t
Xbit_r2_c22 bl[22] br[22] wl[2] vdd gnd cell_6t
Xbit_r3_c22 bl[22] br[22] wl[3] vdd gnd cell_6t
Xbit_r4_c22 bl[22] br[22] wl[4] vdd gnd cell_6t
Xbit_r5_c22 bl[22] br[22] wl[5] vdd gnd cell_6t
Xbit_r6_c22 bl[22] br[22] wl[6] vdd gnd cell_6t
Xbit_r7_c22 bl[22] br[22] wl[7] vdd gnd cell_6t
Xbit_r8_c22 bl[22] br[22] wl[8] vdd gnd cell_6t
Xbit_r9_c22 bl[22] br[22] wl[9] vdd gnd cell_6t
Xbit_r10_c22 bl[22] br[22] wl[10] vdd gnd cell_6t
Xbit_r11_c22 bl[22] br[22] wl[11] vdd gnd cell_6t
Xbit_r12_c22 bl[22] br[22] wl[12] vdd gnd cell_6t
Xbit_r13_c22 bl[22] br[22] wl[13] vdd gnd cell_6t
Xbit_r14_c22 bl[22] br[22] wl[14] vdd gnd cell_6t
Xbit_r15_c22 bl[22] br[22] wl[15] vdd gnd cell_6t
Xbit_r16_c22 bl[22] br[22] wl[16] vdd gnd cell_6t
Xbit_r17_c22 bl[22] br[22] wl[17] vdd gnd cell_6t
Xbit_r18_c22 bl[22] br[22] wl[18] vdd gnd cell_6t
Xbit_r19_c22 bl[22] br[22] wl[19] vdd gnd cell_6t
Xbit_r20_c22 bl[22] br[22] wl[20] vdd gnd cell_6t
Xbit_r21_c22 bl[22] br[22] wl[21] vdd gnd cell_6t
Xbit_r22_c22 bl[22] br[22] wl[22] vdd gnd cell_6t
Xbit_r23_c22 bl[22] br[22] wl[23] vdd gnd cell_6t
Xbit_r24_c22 bl[22] br[22] wl[24] vdd gnd cell_6t
Xbit_r25_c22 bl[22] br[22] wl[25] vdd gnd cell_6t
Xbit_r26_c22 bl[22] br[22] wl[26] vdd gnd cell_6t
Xbit_r27_c22 bl[22] br[22] wl[27] vdd gnd cell_6t
Xbit_r28_c22 bl[22] br[22] wl[28] vdd gnd cell_6t
Xbit_r29_c22 bl[22] br[22] wl[29] vdd gnd cell_6t
Xbit_r30_c22 bl[22] br[22] wl[30] vdd gnd cell_6t
Xbit_r31_c22 bl[22] br[22] wl[31] vdd gnd cell_6t
Xbit_r32_c22 bl[22] br[22] wl[32] vdd gnd cell_6t
Xbit_r33_c22 bl[22] br[22] wl[33] vdd gnd cell_6t
Xbit_r34_c22 bl[22] br[22] wl[34] vdd gnd cell_6t
Xbit_r35_c22 bl[22] br[22] wl[35] vdd gnd cell_6t
Xbit_r36_c22 bl[22] br[22] wl[36] vdd gnd cell_6t
Xbit_r37_c22 bl[22] br[22] wl[37] vdd gnd cell_6t
Xbit_r38_c22 bl[22] br[22] wl[38] vdd gnd cell_6t
Xbit_r39_c22 bl[22] br[22] wl[39] vdd gnd cell_6t
Xbit_r40_c22 bl[22] br[22] wl[40] vdd gnd cell_6t
Xbit_r41_c22 bl[22] br[22] wl[41] vdd gnd cell_6t
Xbit_r42_c22 bl[22] br[22] wl[42] vdd gnd cell_6t
Xbit_r43_c22 bl[22] br[22] wl[43] vdd gnd cell_6t
Xbit_r44_c22 bl[22] br[22] wl[44] vdd gnd cell_6t
Xbit_r45_c22 bl[22] br[22] wl[45] vdd gnd cell_6t
Xbit_r46_c22 bl[22] br[22] wl[46] vdd gnd cell_6t
Xbit_r47_c22 bl[22] br[22] wl[47] vdd gnd cell_6t
Xbit_r48_c22 bl[22] br[22] wl[48] vdd gnd cell_6t
Xbit_r49_c22 bl[22] br[22] wl[49] vdd gnd cell_6t
Xbit_r50_c22 bl[22] br[22] wl[50] vdd gnd cell_6t
Xbit_r51_c22 bl[22] br[22] wl[51] vdd gnd cell_6t
Xbit_r52_c22 bl[22] br[22] wl[52] vdd gnd cell_6t
Xbit_r53_c22 bl[22] br[22] wl[53] vdd gnd cell_6t
Xbit_r54_c22 bl[22] br[22] wl[54] vdd gnd cell_6t
Xbit_r55_c22 bl[22] br[22] wl[55] vdd gnd cell_6t
Xbit_r56_c22 bl[22] br[22] wl[56] vdd gnd cell_6t
Xbit_r57_c22 bl[22] br[22] wl[57] vdd gnd cell_6t
Xbit_r58_c22 bl[22] br[22] wl[58] vdd gnd cell_6t
Xbit_r59_c22 bl[22] br[22] wl[59] vdd gnd cell_6t
Xbit_r60_c22 bl[22] br[22] wl[60] vdd gnd cell_6t
Xbit_r61_c22 bl[22] br[22] wl[61] vdd gnd cell_6t
Xbit_r62_c22 bl[22] br[22] wl[62] vdd gnd cell_6t
Xbit_r63_c22 bl[22] br[22] wl[63] vdd gnd cell_6t
Xbit_r0_c23 bl[23] br[23] wl[0] vdd gnd cell_6t
Xbit_r1_c23 bl[23] br[23] wl[1] vdd gnd cell_6t
Xbit_r2_c23 bl[23] br[23] wl[2] vdd gnd cell_6t
Xbit_r3_c23 bl[23] br[23] wl[3] vdd gnd cell_6t
Xbit_r4_c23 bl[23] br[23] wl[4] vdd gnd cell_6t
Xbit_r5_c23 bl[23] br[23] wl[5] vdd gnd cell_6t
Xbit_r6_c23 bl[23] br[23] wl[6] vdd gnd cell_6t
Xbit_r7_c23 bl[23] br[23] wl[7] vdd gnd cell_6t
Xbit_r8_c23 bl[23] br[23] wl[8] vdd gnd cell_6t
Xbit_r9_c23 bl[23] br[23] wl[9] vdd gnd cell_6t
Xbit_r10_c23 bl[23] br[23] wl[10] vdd gnd cell_6t
Xbit_r11_c23 bl[23] br[23] wl[11] vdd gnd cell_6t
Xbit_r12_c23 bl[23] br[23] wl[12] vdd gnd cell_6t
Xbit_r13_c23 bl[23] br[23] wl[13] vdd gnd cell_6t
Xbit_r14_c23 bl[23] br[23] wl[14] vdd gnd cell_6t
Xbit_r15_c23 bl[23] br[23] wl[15] vdd gnd cell_6t
Xbit_r16_c23 bl[23] br[23] wl[16] vdd gnd cell_6t
Xbit_r17_c23 bl[23] br[23] wl[17] vdd gnd cell_6t
Xbit_r18_c23 bl[23] br[23] wl[18] vdd gnd cell_6t
Xbit_r19_c23 bl[23] br[23] wl[19] vdd gnd cell_6t
Xbit_r20_c23 bl[23] br[23] wl[20] vdd gnd cell_6t
Xbit_r21_c23 bl[23] br[23] wl[21] vdd gnd cell_6t
Xbit_r22_c23 bl[23] br[23] wl[22] vdd gnd cell_6t
Xbit_r23_c23 bl[23] br[23] wl[23] vdd gnd cell_6t
Xbit_r24_c23 bl[23] br[23] wl[24] vdd gnd cell_6t
Xbit_r25_c23 bl[23] br[23] wl[25] vdd gnd cell_6t
Xbit_r26_c23 bl[23] br[23] wl[26] vdd gnd cell_6t
Xbit_r27_c23 bl[23] br[23] wl[27] vdd gnd cell_6t
Xbit_r28_c23 bl[23] br[23] wl[28] vdd gnd cell_6t
Xbit_r29_c23 bl[23] br[23] wl[29] vdd gnd cell_6t
Xbit_r30_c23 bl[23] br[23] wl[30] vdd gnd cell_6t
Xbit_r31_c23 bl[23] br[23] wl[31] vdd gnd cell_6t
Xbit_r32_c23 bl[23] br[23] wl[32] vdd gnd cell_6t
Xbit_r33_c23 bl[23] br[23] wl[33] vdd gnd cell_6t
Xbit_r34_c23 bl[23] br[23] wl[34] vdd gnd cell_6t
Xbit_r35_c23 bl[23] br[23] wl[35] vdd gnd cell_6t
Xbit_r36_c23 bl[23] br[23] wl[36] vdd gnd cell_6t
Xbit_r37_c23 bl[23] br[23] wl[37] vdd gnd cell_6t
Xbit_r38_c23 bl[23] br[23] wl[38] vdd gnd cell_6t
Xbit_r39_c23 bl[23] br[23] wl[39] vdd gnd cell_6t
Xbit_r40_c23 bl[23] br[23] wl[40] vdd gnd cell_6t
Xbit_r41_c23 bl[23] br[23] wl[41] vdd gnd cell_6t
Xbit_r42_c23 bl[23] br[23] wl[42] vdd gnd cell_6t
Xbit_r43_c23 bl[23] br[23] wl[43] vdd gnd cell_6t
Xbit_r44_c23 bl[23] br[23] wl[44] vdd gnd cell_6t
Xbit_r45_c23 bl[23] br[23] wl[45] vdd gnd cell_6t
Xbit_r46_c23 bl[23] br[23] wl[46] vdd gnd cell_6t
Xbit_r47_c23 bl[23] br[23] wl[47] vdd gnd cell_6t
Xbit_r48_c23 bl[23] br[23] wl[48] vdd gnd cell_6t
Xbit_r49_c23 bl[23] br[23] wl[49] vdd gnd cell_6t
Xbit_r50_c23 bl[23] br[23] wl[50] vdd gnd cell_6t
Xbit_r51_c23 bl[23] br[23] wl[51] vdd gnd cell_6t
Xbit_r52_c23 bl[23] br[23] wl[52] vdd gnd cell_6t
Xbit_r53_c23 bl[23] br[23] wl[53] vdd gnd cell_6t
Xbit_r54_c23 bl[23] br[23] wl[54] vdd gnd cell_6t
Xbit_r55_c23 bl[23] br[23] wl[55] vdd gnd cell_6t
Xbit_r56_c23 bl[23] br[23] wl[56] vdd gnd cell_6t
Xbit_r57_c23 bl[23] br[23] wl[57] vdd gnd cell_6t
Xbit_r58_c23 bl[23] br[23] wl[58] vdd gnd cell_6t
Xbit_r59_c23 bl[23] br[23] wl[59] vdd gnd cell_6t
Xbit_r60_c23 bl[23] br[23] wl[60] vdd gnd cell_6t
Xbit_r61_c23 bl[23] br[23] wl[61] vdd gnd cell_6t
Xbit_r62_c23 bl[23] br[23] wl[62] vdd gnd cell_6t
Xbit_r63_c23 bl[23] br[23] wl[63] vdd gnd cell_6t
Xbit_r0_c24 bl[24] br[24] wl[0] vdd gnd cell_6t
Xbit_r1_c24 bl[24] br[24] wl[1] vdd gnd cell_6t
Xbit_r2_c24 bl[24] br[24] wl[2] vdd gnd cell_6t
Xbit_r3_c24 bl[24] br[24] wl[3] vdd gnd cell_6t
Xbit_r4_c24 bl[24] br[24] wl[4] vdd gnd cell_6t
Xbit_r5_c24 bl[24] br[24] wl[5] vdd gnd cell_6t
Xbit_r6_c24 bl[24] br[24] wl[6] vdd gnd cell_6t
Xbit_r7_c24 bl[24] br[24] wl[7] vdd gnd cell_6t
Xbit_r8_c24 bl[24] br[24] wl[8] vdd gnd cell_6t
Xbit_r9_c24 bl[24] br[24] wl[9] vdd gnd cell_6t
Xbit_r10_c24 bl[24] br[24] wl[10] vdd gnd cell_6t
Xbit_r11_c24 bl[24] br[24] wl[11] vdd gnd cell_6t
Xbit_r12_c24 bl[24] br[24] wl[12] vdd gnd cell_6t
Xbit_r13_c24 bl[24] br[24] wl[13] vdd gnd cell_6t
Xbit_r14_c24 bl[24] br[24] wl[14] vdd gnd cell_6t
Xbit_r15_c24 bl[24] br[24] wl[15] vdd gnd cell_6t
Xbit_r16_c24 bl[24] br[24] wl[16] vdd gnd cell_6t
Xbit_r17_c24 bl[24] br[24] wl[17] vdd gnd cell_6t
Xbit_r18_c24 bl[24] br[24] wl[18] vdd gnd cell_6t
Xbit_r19_c24 bl[24] br[24] wl[19] vdd gnd cell_6t
Xbit_r20_c24 bl[24] br[24] wl[20] vdd gnd cell_6t
Xbit_r21_c24 bl[24] br[24] wl[21] vdd gnd cell_6t
Xbit_r22_c24 bl[24] br[24] wl[22] vdd gnd cell_6t
Xbit_r23_c24 bl[24] br[24] wl[23] vdd gnd cell_6t
Xbit_r24_c24 bl[24] br[24] wl[24] vdd gnd cell_6t
Xbit_r25_c24 bl[24] br[24] wl[25] vdd gnd cell_6t
Xbit_r26_c24 bl[24] br[24] wl[26] vdd gnd cell_6t
Xbit_r27_c24 bl[24] br[24] wl[27] vdd gnd cell_6t
Xbit_r28_c24 bl[24] br[24] wl[28] vdd gnd cell_6t
Xbit_r29_c24 bl[24] br[24] wl[29] vdd gnd cell_6t
Xbit_r30_c24 bl[24] br[24] wl[30] vdd gnd cell_6t
Xbit_r31_c24 bl[24] br[24] wl[31] vdd gnd cell_6t
Xbit_r32_c24 bl[24] br[24] wl[32] vdd gnd cell_6t
Xbit_r33_c24 bl[24] br[24] wl[33] vdd gnd cell_6t
Xbit_r34_c24 bl[24] br[24] wl[34] vdd gnd cell_6t
Xbit_r35_c24 bl[24] br[24] wl[35] vdd gnd cell_6t
Xbit_r36_c24 bl[24] br[24] wl[36] vdd gnd cell_6t
Xbit_r37_c24 bl[24] br[24] wl[37] vdd gnd cell_6t
Xbit_r38_c24 bl[24] br[24] wl[38] vdd gnd cell_6t
Xbit_r39_c24 bl[24] br[24] wl[39] vdd gnd cell_6t
Xbit_r40_c24 bl[24] br[24] wl[40] vdd gnd cell_6t
Xbit_r41_c24 bl[24] br[24] wl[41] vdd gnd cell_6t
Xbit_r42_c24 bl[24] br[24] wl[42] vdd gnd cell_6t
Xbit_r43_c24 bl[24] br[24] wl[43] vdd gnd cell_6t
Xbit_r44_c24 bl[24] br[24] wl[44] vdd gnd cell_6t
Xbit_r45_c24 bl[24] br[24] wl[45] vdd gnd cell_6t
Xbit_r46_c24 bl[24] br[24] wl[46] vdd gnd cell_6t
Xbit_r47_c24 bl[24] br[24] wl[47] vdd gnd cell_6t
Xbit_r48_c24 bl[24] br[24] wl[48] vdd gnd cell_6t
Xbit_r49_c24 bl[24] br[24] wl[49] vdd gnd cell_6t
Xbit_r50_c24 bl[24] br[24] wl[50] vdd gnd cell_6t
Xbit_r51_c24 bl[24] br[24] wl[51] vdd gnd cell_6t
Xbit_r52_c24 bl[24] br[24] wl[52] vdd gnd cell_6t
Xbit_r53_c24 bl[24] br[24] wl[53] vdd gnd cell_6t
Xbit_r54_c24 bl[24] br[24] wl[54] vdd gnd cell_6t
Xbit_r55_c24 bl[24] br[24] wl[55] vdd gnd cell_6t
Xbit_r56_c24 bl[24] br[24] wl[56] vdd gnd cell_6t
Xbit_r57_c24 bl[24] br[24] wl[57] vdd gnd cell_6t
Xbit_r58_c24 bl[24] br[24] wl[58] vdd gnd cell_6t
Xbit_r59_c24 bl[24] br[24] wl[59] vdd gnd cell_6t
Xbit_r60_c24 bl[24] br[24] wl[60] vdd gnd cell_6t
Xbit_r61_c24 bl[24] br[24] wl[61] vdd gnd cell_6t
Xbit_r62_c24 bl[24] br[24] wl[62] vdd gnd cell_6t
Xbit_r63_c24 bl[24] br[24] wl[63] vdd gnd cell_6t
Xbit_r0_c25 bl[25] br[25] wl[0] vdd gnd cell_6t
Xbit_r1_c25 bl[25] br[25] wl[1] vdd gnd cell_6t
Xbit_r2_c25 bl[25] br[25] wl[2] vdd gnd cell_6t
Xbit_r3_c25 bl[25] br[25] wl[3] vdd gnd cell_6t
Xbit_r4_c25 bl[25] br[25] wl[4] vdd gnd cell_6t
Xbit_r5_c25 bl[25] br[25] wl[5] vdd gnd cell_6t
Xbit_r6_c25 bl[25] br[25] wl[6] vdd gnd cell_6t
Xbit_r7_c25 bl[25] br[25] wl[7] vdd gnd cell_6t
Xbit_r8_c25 bl[25] br[25] wl[8] vdd gnd cell_6t
Xbit_r9_c25 bl[25] br[25] wl[9] vdd gnd cell_6t
Xbit_r10_c25 bl[25] br[25] wl[10] vdd gnd cell_6t
Xbit_r11_c25 bl[25] br[25] wl[11] vdd gnd cell_6t
Xbit_r12_c25 bl[25] br[25] wl[12] vdd gnd cell_6t
Xbit_r13_c25 bl[25] br[25] wl[13] vdd gnd cell_6t
Xbit_r14_c25 bl[25] br[25] wl[14] vdd gnd cell_6t
Xbit_r15_c25 bl[25] br[25] wl[15] vdd gnd cell_6t
Xbit_r16_c25 bl[25] br[25] wl[16] vdd gnd cell_6t
Xbit_r17_c25 bl[25] br[25] wl[17] vdd gnd cell_6t
Xbit_r18_c25 bl[25] br[25] wl[18] vdd gnd cell_6t
Xbit_r19_c25 bl[25] br[25] wl[19] vdd gnd cell_6t
Xbit_r20_c25 bl[25] br[25] wl[20] vdd gnd cell_6t
Xbit_r21_c25 bl[25] br[25] wl[21] vdd gnd cell_6t
Xbit_r22_c25 bl[25] br[25] wl[22] vdd gnd cell_6t
Xbit_r23_c25 bl[25] br[25] wl[23] vdd gnd cell_6t
Xbit_r24_c25 bl[25] br[25] wl[24] vdd gnd cell_6t
Xbit_r25_c25 bl[25] br[25] wl[25] vdd gnd cell_6t
Xbit_r26_c25 bl[25] br[25] wl[26] vdd gnd cell_6t
Xbit_r27_c25 bl[25] br[25] wl[27] vdd gnd cell_6t
Xbit_r28_c25 bl[25] br[25] wl[28] vdd gnd cell_6t
Xbit_r29_c25 bl[25] br[25] wl[29] vdd gnd cell_6t
Xbit_r30_c25 bl[25] br[25] wl[30] vdd gnd cell_6t
Xbit_r31_c25 bl[25] br[25] wl[31] vdd gnd cell_6t
Xbit_r32_c25 bl[25] br[25] wl[32] vdd gnd cell_6t
Xbit_r33_c25 bl[25] br[25] wl[33] vdd gnd cell_6t
Xbit_r34_c25 bl[25] br[25] wl[34] vdd gnd cell_6t
Xbit_r35_c25 bl[25] br[25] wl[35] vdd gnd cell_6t
Xbit_r36_c25 bl[25] br[25] wl[36] vdd gnd cell_6t
Xbit_r37_c25 bl[25] br[25] wl[37] vdd gnd cell_6t
Xbit_r38_c25 bl[25] br[25] wl[38] vdd gnd cell_6t
Xbit_r39_c25 bl[25] br[25] wl[39] vdd gnd cell_6t
Xbit_r40_c25 bl[25] br[25] wl[40] vdd gnd cell_6t
Xbit_r41_c25 bl[25] br[25] wl[41] vdd gnd cell_6t
Xbit_r42_c25 bl[25] br[25] wl[42] vdd gnd cell_6t
Xbit_r43_c25 bl[25] br[25] wl[43] vdd gnd cell_6t
Xbit_r44_c25 bl[25] br[25] wl[44] vdd gnd cell_6t
Xbit_r45_c25 bl[25] br[25] wl[45] vdd gnd cell_6t
Xbit_r46_c25 bl[25] br[25] wl[46] vdd gnd cell_6t
Xbit_r47_c25 bl[25] br[25] wl[47] vdd gnd cell_6t
Xbit_r48_c25 bl[25] br[25] wl[48] vdd gnd cell_6t
Xbit_r49_c25 bl[25] br[25] wl[49] vdd gnd cell_6t
Xbit_r50_c25 bl[25] br[25] wl[50] vdd gnd cell_6t
Xbit_r51_c25 bl[25] br[25] wl[51] vdd gnd cell_6t
Xbit_r52_c25 bl[25] br[25] wl[52] vdd gnd cell_6t
Xbit_r53_c25 bl[25] br[25] wl[53] vdd gnd cell_6t
Xbit_r54_c25 bl[25] br[25] wl[54] vdd gnd cell_6t
Xbit_r55_c25 bl[25] br[25] wl[55] vdd gnd cell_6t
Xbit_r56_c25 bl[25] br[25] wl[56] vdd gnd cell_6t
Xbit_r57_c25 bl[25] br[25] wl[57] vdd gnd cell_6t
Xbit_r58_c25 bl[25] br[25] wl[58] vdd gnd cell_6t
Xbit_r59_c25 bl[25] br[25] wl[59] vdd gnd cell_6t
Xbit_r60_c25 bl[25] br[25] wl[60] vdd gnd cell_6t
Xbit_r61_c25 bl[25] br[25] wl[61] vdd gnd cell_6t
Xbit_r62_c25 bl[25] br[25] wl[62] vdd gnd cell_6t
Xbit_r63_c25 bl[25] br[25] wl[63] vdd gnd cell_6t
Xbit_r0_c26 bl[26] br[26] wl[0] vdd gnd cell_6t
Xbit_r1_c26 bl[26] br[26] wl[1] vdd gnd cell_6t
Xbit_r2_c26 bl[26] br[26] wl[2] vdd gnd cell_6t
Xbit_r3_c26 bl[26] br[26] wl[3] vdd gnd cell_6t
Xbit_r4_c26 bl[26] br[26] wl[4] vdd gnd cell_6t
Xbit_r5_c26 bl[26] br[26] wl[5] vdd gnd cell_6t
Xbit_r6_c26 bl[26] br[26] wl[6] vdd gnd cell_6t
Xbit_r7_c26 bl[26] br[26] wl[7] vdd gnd cell_6t
Xbit_r8_c26 bl[26] br[26] wl[8] vdd gnd cell_6t
Xbit_r9_c26 bl[26] br[26] wl[9] vdd gnd cell_6t
Xbit_r10_c26 bl[26] br[26] wl[10] vdd gnd cell_6t
Xbit_r11_c26 bl[26] br[26] wl[11] vdd gnd cell_6t
Xbit_r12_c26 bl[26] br[26] wl[12] vdd gnd cell_6t
Xbit_r13_c26 bl[26] br[26] wl[13] vdd gnd cell_6t
Xbit_r14_c26 bl[26] br[26] wl[14] vdd gnd cell_6t
Xbit_r15_c26 bl[26] br[26] wl[15] vdd gnd cell_6t
Xbit_r16_c26 bl[26] br[26] wl[16] vdd gnd cell_6t
Xbit_r17_c26 bl[26] br[26] wl[17] vdd gnd cell_6t
Xbit_r18_c26 bl[26] br[26] wl[18] vdd gnd cell_6t
Xbit_r19_c26 bl[26] br[26] wl[19] vdd gnd cell_6t
Xbit_r20_c26 bl[26] br[26] wl[20] vdd gnd cell_6t
Xbit_r21_c26 bl[26] br[26] wl[21] vdd gnd cell_6t
Xbit_r22_c26 bl[26] br[26] wl[22] vdd gnd cell_6t
Xbit_r23_c26 bl[26] br[26] wl[23] vdd gnd cell_6t
Xbit_r24_c26 bl[26] br[26] wl[24] vdd gnd cell_6t
Xbit_r25_c26 bl[26] br[26] wl[25] vdd gnd cell_6t
Xbit_r26_c26 bl[26] br[26] wl[26] vdd gnd cell_6t
Xbit_r27_c26 bl[26] br[26] wl[27] vdd gnd cell_6t
Xbit_r28_c26 bl[26] br[26] wl[28] vdd gnd cell_6t
Xbit_r29_c26 bl[26] br[26] wl[29] vdd gnd cell_6t
Xbit_r30_c26 bl[26] br[26] wl[30] vdd gnd cell_6t
Xbit_r31_c26 bl[26] br[26] wl[31] vdd gnd cell_6t
Xbit_r32_c26 bl[26] br[26] wl[32] vdd gnd cell_6t
Xbit_r33_c26 bl[26] br[26] wl[33] vdd gnd cell_6t
Xbit_r34_c26 bl[26] br[26] wl[34] vdd gnd cell_6t
Xbit_r35_c26 bl[26] br[26] wl[35] vdd gnd cell_6t
Xbit_r36_c26 bl[26] br[26] wl[36] vdd gnd cell_6t
Xbit_r37_c26 bl[26] br[26] wl[37] vdd gnd cell_6t
Xbit_r38_c26 bl[26] br[26] wl[38] vdd gnd cell_6t
Xbit_r39_c26 bl[26] br[26] wl[39] vdd gnd cell_6t
Xbit_r40_c26 bl[26] br[26] wl[40] vdd gnd cell_6t
Xbit_r41_c26 bl[26] br[26] wl[41] vdd gnd cell_6t
Xbit_r42_c26 bl[26] br[26] wl[42] vdd gnd cell_6t
Xbit_r43_c26 bl[26] br[26] wl[43] vdd gnd cell_6t
Xbit_r44_c26 bl[26] br[26] wl[44] vdd gnd cell_6t
Xbit_r45_c26 bl[26] br[26] wl[45] vdd gnd cell_6t
Xbit_r46_c26 bl[26] br[26] wl[46] vdd gnd cell_6t
Xbit_r47_c26 bl[26] br[26] wl[47] vdd gnd cell_6t
Xbit_r48_c26 bl[26] br[26] wl[48] vdd gnd cell_6t
Xbit_r49_c26 bl[26] br[26] wl[49] vdd gnd cell_6t
Xbit_r50_c26 bl[26] br[26] wl[50] vdd gnd cell_6t
Xbit_r51_c26 bl[26] br[26] wl[51] vdd gnd cell_6t
Xbit_r52_c26 bl[26] br[26] wl[52] vdd gnd cell_6t
Xbit_r53_c26 bl[26] br[26] wl[53] vdd gnd cell_6t
Xbit_r54_c26 bl[26] br[26] wl[54] vdd gnd cell_6t
Xbit_r55_c26 bl[26] br[26] wl[55] vdd gnd cell_6t
Xbit_r56_c26 bl[26] br[26] wl[56] vdd gnd cell_6t
Xbit_r57_c26 bl[26] br[26] wl[57] vdd gnd cell_6t
Xbit_r58_c26 bl[26] br[26] wl[58] vdd gnd cell_6t
Xbit_r59_c26 bl[26] br[26] wl[59] vdd gnd cell_6t
Xbit_r60_c26 bl[26] br[26] wl[60] vdd gnd cell_6t
Xbit_r61_c26 bl[26] br[26] wl[61] vdd gnd cell_6t
Xbit_r62_c26 bl[26] br[26] wl[62] vdd gnd cell_6t
Xbit_r63_c26 bl[26] br[26] wl[63] vdd gnd cell_6t
Xbit_r0_c27 bl[27] br[27] wl[0] vdd gnd cell_6t
Xbit_r1_c27 bl[27] br[27] wl[1] vdd gnd cell_6t
Xbit_r2_c27 bl[27] br[27] wl[2] vdd gnd cell_6t
Xbit_r3_c27 bl[27] br[27] wl[3] vdd gnd cell_6t
Xbit_r4_c27 bl[27] br[27] wl[4] vdd gnd cell_6t
Xbit_r5_c27 bl[27] br[27] wl[5] vdd gnd cell_6t
Xbit_r6_c27 bl[27] br[27] wl[6] vdd gnd cell_6t
Xbit_r7_c27 bl[27] br[27] wl[7] vdd gnd cell_6t
Xbit_r8_c27 bl[27] br[27] wl[8] vdd gnd cell_6t
Xbit_r9_c27 bl[27] br[27] wl[9] vdd gnd cell_6t
Xbit_r10_c27 bl[27] br[27] wl[10] vdd gnd cell_6t
Xbit_r11_c27 bl[27] br[27] wl[11] vdd gnd cell_6t
Xbit_r12_c27 bl[27] br[27] wl[12] vdd gnd cell_6t
Xbit_r13_c27 bl[27] br[27] wl[13] vdd gnd cell_6t
Xbit_r14_c27 bl[27] br[27] wl[14] vdd gnd cell_6t
Xbit_r15_c27 bl[27] br[27] wl[15] vdd gnd cell_6t
Xbit_r16_c27 bl[27] br[27] wl[16] vdd gnd cell_6t
Xbit_r17_c27 bl[27] br[27] wl[17] vdd gnd cell_6t
Xbit_r18_c27 bl[27] br[27] wl[18] vdd gnd cell_6t
Xbit_r19_c27 bl[27] br[27] wl[19] vdd gnd cell_6t
Xbit_r20_c27 bl[27] br[27] wl[20] vdd gnd cell_6t
Xbit_r21_c27 bl[27] br[27] wl[21] vdd gnd cell_6t
Xbit_r22_c27 bl[27] br[27] wl[22] vdd gnd cell_6t
Xbit_r23_c27 bl[27] br[27] wl[23] vdd gnd cell_6t
Xbit_r24_c27 bl[27] br[27] wl[24] vdd gnd cell_6t
Xbit_r25_c27 bl[27] br[27] wl[25] vdd gnd cell_6t
Xbit_r26_c27 bl[27] br[27] wl[26] vdd gnd cell_6t
Xbit_r27_c27 bl[27] br[27] wl[27] vdd gnd cell_6t
Xbit_r28_c27 bl[27] br[27] wl[28] vdd gnd cell_6t
Xbit_r29_c27 bl[27] br[27] wl[29] vdd gnd cell_6t
Xbit_r30_c27 bl[27] br[27] wl[30] vdd gnd cell_6t
Xbit_r31_c27 bl[27] br[27] wl[31] vdd gnd cell_6t
Xbit_r32_c27 bl[27] br[27] wl[32] vdd gnd cell_6t
Xbit_r33_c27 bl[27] br[27] wl[33] vdd gnd cell_6t
Xbit_r34_c27 bl[27] br[27] wl[34] vdd gnd cell_6t
Xbit_r35_c27 bl[27] br[27] wl[35] vdd gnd cell_6t
Xbit_r36_c27 bl[27] br[27] wl[36] vdd gnd cell_6t
Xbit_r37_c27 bl[27] br[27] wl[37] vdd gnd cell_6t
Xbit_r38_c27 bl[27] br[27] wl[38] vdd gnd cell_6t
Xbit_r39_c27 bl[27] br[27] wl[39] vdd gnd cell_6t
Xbit_r40_c27 bl[27] br[27] wl[40] vdd gnd cell_6t
Xbit_r41_c27 bl[27] br[27] wl[41] vdd gnd cell_6t
Xbit_r42_c27 bl[27] br[27] wl[42] vdd gnd cell_6t
Xbit_r43_c27 bl[27] br[27] wl[43] vdd gnd cell_6t
Xbit_r44_c27 bl[27] br[27] wl[44] vdd gnd cell_6t
Xbit_r45_c27 bl[27] br[27] wl[45] vdd gnd cell_6t
Xbit_r46_c27 bl[27] br[27] wl[46] vdd gnd cell_6t
Xbit_r47_c27 bl[27] br[27] wl[47] vdd gnd cell_6t
Xbit_r48_c27 bl[27] br[27] wl[48] vdd gnd cell_6t
Xbit_r49_c27 bl[27] br[27] wl[49] vdd gnd cell_6t
Xbit_r50_c27 bl[27] br[27] wl[50] vdd gnd cell_6t
Xbit_r51_c27 bl[27] br[27] wl[51] vdd gnd cell_6t
Xbit_r52_c27 bl[27] br[27] wl[52] vdd gnd cell_6t
Xbit_r53_c27 bl[27] br[27] wl[53] vdd gnd cell_6t
Xbit_r54_c27 bl[27] br[27] wl[54] vdd gnd cell_6t
Xbit_r55_c27 bl[27] br[27] wl[55] vdd gnd cell_6t
Xbit_r56_c27 bl[27] br[27] wl[56] vdd gnd cell_6t
Xbit_r57_c27 bl[27] br[27] wl[57] vdd gnd cell_6t
Xbit_r58_c27 bl[27] br[27] wl[58] vdd gnd cell_6t
Xbit_r59_c27 bl[27] br[27] wl[59] vdd gnd cell_6t
Xbit_r60_c27 bl[27] br[27] wl[60] vdd gnd cell_6t
Xbit_r61_c27 bl[27] br[27] wl[61] vdd gnd cell_6t
Xbit_r62_c27 bl[27] br[27] wl[62] vdd gnd cell_6t
Xbit_r63_c27 bl[27] br[27] wl[63] vdd gnd cell_6t
Xbit_r0_c28 bl[28] br[28] wl[0] vdd gnd cell_6t
Xbit_r1_c28 bl[28] br[28] wl[1] vdd gnd cell_6t
Xbit_r2_c28 bl[28] br[28] wl[2] vdd gnd cell_6t
Xbit_r3_c28 bl[28] br[28] wl[3] vdd gnd cell_6t
Xbit_r4_c28 bl[28] br[28] wl[4] vdd gnd cell_6t
Xbit_r5_c28 bl[28] br[28] wl[5] vdd gnd cell_6t
Xbit_r6_c28 bl[28] br[28] wl[6] vdd gnd cell_6t
Xbit_r7_c28 bl[28] br[28] wl[7] vdd gnd cell_6t
Xbit_r8_c28 bl[28] br[28] wl[8] vdd gnd cell_6t
Xbit_r9_c28 bl[28] br[28] wl[9] vdd gnd cell_6t
Xbit_r10_c28 bl[28] br[28] wl[10] vdd gnd cell_6t
Xbit_r11_c28 bl[28] br[28] wl[11] vdd gnd cell_6t
Xbit_r12_c28 bl[28] br[28] wl[12] vdd gnd cell_6t
Xbit_r13_c28 bl[28] br[28] wl[13] vdd gnd cell_6t
Xbit_r14_c28 bl[28] br[28] wl[14] vdd gnd cell_6t
Xbit_r15_c28 bl[28] br[28] wl[15] vdd gnd cell_6t
Xbit_r16_c28 bl[28] br[28] wl[16] vdd gnd cell_6t
Xbit_r17_c28 bl[28] br[28] wl[17] vdd gnd cell_6t
Xbit_r18_c28 bl[28] br[28] wl[18] vdd gnd cell_6t
Xbit_r19_c28 bl[28] br[28] wl[19] vdd gnd cell_6t
Xbit_r20_c28 bl[28] br[28] wl[20] vdd gnd cell_6t
Xbit_r21_c28 bl[28] br[28] wl[21] vdd gnd cell_6t
Xbit_r22_c28 bl[28] br[28] wl[22] vdd gnd cell_6t
Xbit_r23_c28 bl[28] br[28] wl[23] vdd gnd cell_6t
Xbit_r24_c28 bl[28] br[28] wl[24] vdd gnd cell_6t
Xbit_r25_c28 bl[28] br[28] wl[25] vdd gnd cell_6t
Xbit_r26_c28 bl[28] br[28] wl[26] vdd gnd cell_6t
Xbit_r27_c28 bl[28] br[28] wl[27] vdd gnd cell_6t
Xbit_r28_c28 bl[28] br[28] wl[28] vdd gnd cell_6t
Xbit_r29_c28 bl[28] br[28] wl[29] vdd gnd cell_6t
Xbit_r30_c28 bl[28] br[28] wl[30] vdd gnd cell_6t
Xbit_r31_c28 bl[28] br[28] wl[31] vdd gnd cell_6t
Xbit_r32_c28 bl[28] br[28] wl[32] vdd gnd cell_6t
Xbit_r33_c28 bl[28] br[28] wl[33] vdd gnd cell_6t
Xbit_r34_c28 bl[28] br[28] wl[34] vdd gnd cell_6t
Xbit_r35_c28 bl[28] br[28] wl[35] vdd gnd cell_6t
Xbit_r36_c28 bl[28] br[28] wl[36] vdd gnd cell_6t
Xbit_r37_c28 bl[28] br[28] wl[37] vdd gnd cell_6t
Xbit_r38_c28 bl[28] br[28] wl[38] vdd gnd cell_6t
Xbit_r39_c28 bl[28] br[28] wl[39] vdd gnd cell_6t
Xbit_r40_c28 bl[28] br[28] wl[40] vdd gnd cell_6t
Xbit_r41_c28 bl[28] br[28] wl[41] vdd gnd cell_6t
Xbit_r42_c28 bl[28] br[28] wl[42] vdd gnd cell_6t
Xbit_r43_c28 bl[28] br[28] wl[43] vdd gnd cell_6t
Xbit_r44_c28 bl[28] br[28] wl[44] vdd gnd cell_6t
Xbit_r45_c28 bl[28] br[28] wl[45] vdd gnd cell_6t
Xbit_r46_c28 bl[28] br[28] wl[46] vdd gnd cell_6t
Xbit_r47_c28 bl[28] br[28] wl[47] vdd gnd cell_6t
Xbit_r48_c28 bl[28] br[28] wl[48] vdd gnd cell_6t
Xbit_r49_c28 bl[28] br[28] wl[49] vdd gnd cell_6t
Xbit_r50_c28 bl[28] br[28] wl[50] vdd gnd cell_6t
Xbit_r51_c28 bl[28] br[28] wl[51] vdd gnd cell_6t
Xbit_r52_c28 bl[28] br[28] wl[52] vdd gnd cell_6t
Xbit_r53_c28 bl[28] br[28] wl[53] vdd gnd cell_6t
Xbit_r54_c28 bl[28] br[28] wl[54] vdd gnd cell_6t
Xbit_r55_c28 bl[28] br[28] wl[55] vdd gnd cell_6t
Xbit_r56_c28 bl[28] br[28] wl[56] vdd gnd cell_6t
Xbit_r57_c28 bl[28] br[28] wl[57] vdd gnd cell_6t
Xbit_r58_c28 bl[28] br[28] wl[58] vdd gnd cell_6t
Xbit_r59_c28 bl[28] br[28] wl[59] vdd gnd cell_6t
Xbit_r60_c28 bl[28] br[28] wl[60] vdd gnd cell_6t
Xbit_r61_c28 bl[28] br[28] wl[61] vdd gnd cell_6t
Xbit_r62_c28 bl[28] br[28] wl[62] vdd gnd cell_6t
Xbit_r63_c28 bl[28] br[28] wl[63] vdd gnd cell_6t
Xbit_r0_c29 bl[29] br[29] wl[0] vdd gnd cell_6t
Xbit_r1_c29 bl[29] br[29] wl[1] vdd gnd cell_6t
Xbit_r2_c29 bl[29] br[29] wl[2] vdd gnd cell_6t
Xbit_r3_c29 bl[29] br[29] wl[3] vdd gnd cell_6t
Xbit_r4_c29 bl[29] br[29] wl[4] vdd gnd cell_6t
Xbit_r5_c29 bl[29] br[29] wl[5] vdd gnd cell_6t
Xbit_r6_c29 bl[29] br[29] wl[6] vdd gnd cell_6t
Xbit_r7_c29 bl[29] br[29] wl[7] vdd gnd cell_6t
Xbit_r8_c29 bl[29] br[29] wl[8] vdd gnd cell_6t
Xbit_r9_c29 bl[29] br[29] wl[9] vdd gnd cell_6t
Xbit_r10_c29 bl[29] br[29] wl[10] vdd gnd cell_6t
Xbit_r11_c29 bl[29] br[29] wl[11] vdd gnd cell_6t
Xbit_r12_c29 bl[29] br[29] wl[12] vdd gnd cell_6t
Xbit_r13_c29 bl[29] br[29] wl[13] vdd gnd cell_6t
Xbit_r14_c29 bl[29] br[29] wl[14] vdd gnd cell_6t
Xbit_r15_c29 bl[29] br[29] wl[15] vdd gnd cell_6t
Xbit_r16_c29 bl[29] br[29] wl[16] vdd gnd cell_6t
Xbit_r17_c29 bl[29] br[29] wl[17] vdd gnd cell_6t
Xbit_r18_c29 bl[29] br[29] wl[18] vdd gnd cell_6t
Xbit_r19_c29 bl[29] br[29] wl[19] vdd gnd cell_6t
Xbit_r20_c29 bl[29] br[29] wl[20] vdd gnd cell_6t
Xbit_r21_c29 bl[29] br[29] wl[21] vdd gnd cell_6t
Xbit_r22_c29 bl[29] br[29] wl[22] vdd gnd cell_6t
Xbit_r23_c29 bl[29] br[29] wl[23] vdd gnd cell_6t
Xbit_r24_c29 bl[29] br[29] wl[24] vdd gnd cell_6t
Xbit_r25_c29 bl[29] br[29] wl[25] vdd gnd cell_6t
Xbit_r26_c29 bl[29] br[29] wl[26] vdd gnd cell_6t
Xbit_r27_c29 bl[29] br[29] wl[27] vdd gnd cell_6t
Xbit_r28_c29 bl[29] br[29] wl[28] vdd gnd cell_6t
Xbit_r29_c29 bl[29] br[29] wl[29] vdd gnd cell_6t
Xbit_r30_c29 bl[29] br[29] wl[30] vdd gnd cell_6t
Xbit_r31_c29 bl[29] br[29] wl[31] vdd gnd cell_6t
Xbit_r32_c29 bl[29] br[29] wl[32] vdd gnd cell_6t
Xbit_r33_c29 bl[29] br[29] wl[33] vdd gnd cell_6t
Xbit_r34_c29 bl[29] br[29] wl[34] vdd gnd cell_6t
Xbit_r35_c29 bl[29] br[29] wl[35] vdd gnd cell_6t
Xbit_r36_c29 bl[29] br[29] wl[36] vdd gnd cell_6t
Xbit_r37_c29 bl[29] br[29] wl[37] vdd gnd cell_6t
Xbit_r38_c29 bl[29] br[29] wl[38] vdd gnd cell_6t
Xbit_r39_c29 bl[29] br[29] wl[39] vdd gnd cell_6t
Xbit_r40_c29 bl[29] br[29] wl[40] vdd gnd cell_6t
Xbit_r41_c29 bl[29] br[29] wl[41] vdd gnd cell_6t
Xbit_r42_c29 bl[29] br[29] wl[42] vdd gnd cell_6t
Xbit_r43_c29 bl[29] br[29] wl[43] vdd gnd cell_6t
Xbit_r44_c29 bl[29] br[29] wl[44] vdd gnd cell_6t
Xbit_r45_c29 bl[29] br[29] wl[45] vdd gnd cell_6t
Xbit_r46_c29 bl[29] br[29] wl[46] vdd gnd cell_6t
Xbit_r47_c29 bl[29] br[29] wl[47] vdd gnd cell_6t
Xbit_r48_c29 bl[29] br[29] wl[48] vdd gnd cell_6t
Xbit_r49_c29 bl[29] br[29] wl[49] vdd gnd cell_6t
Xbit_r50_c29 bl[29] br[29] wl[50] vdd gnd cell_6t
Xbit_r51_c29 bl[29] br[29] wl[51] vdd gnd cell_6t
Xbit_r52_c29 bl[29] br[29] wl[52] vdd gnd cell_6t
Xbit_r53_c29 bl[29] br[29] wl[53] vdd gnd cell_6t
Xbit_r54_c29 bl[29] br[29] wl[54] vdd gnd cell_6t
Xbit_r55_c29 bl[29] br[29] wl[55] vdd gnd cell_6t
Xbit_r56_c29 bl[29] br[29] wl[56] vdd gnd cell_6t
Xbit_r57_c29 bl[29] br[29] wl[57] vdd gnd cell_6t
Xbit_r58_c29 bl[29] br[29] wl[58] vdd gnd cell_6t
Xbit_r59_c29 bl[29] br[29] wl[59] vdd gnd cell_6t
Xbit_r60_c29 bl[29] br[29] wl[60] vdd gnd cell_6t
Xbit_r61_c29 bl[29] br[29] wl[61] vdd gnd cell_6t
Xbit_r62_c29 bl[29] br[29] wl[62] vdd gnd cell_6t
Xbit_r63_c29 bl[29] br[29] wl[63] vdd gnd cell_6t
Xbit_r0_c30 bl[30] br[30] wl[0] vdd gnd cell_6t
Xbit_r1_c30 bl[30] br[30] wl[1] vdd gnd cell_6t
Xbit_r2_c30 bl[30] br[30] wl[2] vdd gnd cell_6t
Xbit_r3_c30 bl[30] br[30] wl[3] vdd gnd cell_6t
Xbit_r4_c30 bl[30] br[30] wl[4] vdd gnd cell_6t
Xbit_r5_c30 bl[30] br[30] wl[5] vdd gnd cell_6t
Xbit_r6_c30 bl[30] br[30] wl[6] vdd gnd cell_6t
Xbit_r7_c30 bl[30] br[30] wl[7] vdd gnd cell_6t
Xbit_r8_c30 bl[30] br[30] wl[8] vdd gnd cell_6t
Xbit_r9_c30 bl[30] br[30] wl[9] vdd gnd cell_6t
Xbit_r10_c30 bl[30] br[30] wl[10] vdd gnd cell_6t
Xbit_r11_c30 bl[30] br[30] wl[11] vdd gnd cell_6t
Xbit_r12_c30 bl[30] br[30] wl[12] vdd gnd cell_6t
Xbit_r13_c30 bl[30] br[30] wl[13] vdd gnd cell_6t
Xbit_r14_c30 bl[30] br[30] wl[14] vdd gnd cell_6t
Xbit_r15_c30 bl[30] br[30] wl[15] vdd gnd cell_6t
Xbit_r16_c30 bl[30] br[30] wl[16] vdd gnd cell_6t
Xbit_r17_c30 bl[30] br[30] wl[17] vdd gnd cell_6t
Xbit_r18_c30 bl[30] br[30] wl[18] vdd gnd cell_6t
Xbit_r19_c30 bl[30] br[30] wl[19] vdd gnd cell_6t
Xbit_r20_c30 bl[30] br[30] wl[20] vdd gnd cell_6t
Xbit_r21_c30 bl[30] br[30] wl[21] vdd gnd cell_6t
Xbit_r22_c30 bl[30] br[30] wl[22] vdd gnd cell_6t
Xbit_r23_c30 bl[30] br[30] wl[23] vdd gnd cell_6t
Xbit_r24_c30 bl[30] br[30] wl[24] vdd gnd cell_6t
Xbit_r25_c30 bl[30] br[30] wl[25] vdd gnd cell_6t
Xbit_r26_c30 bl[30] br[30] wl[26] vdd gnd cell_6t
Xbit_r27_c30 bl[30] br[30] wl[27] vdd gnd cell_6t
Xbit_r28_c30 bl[30] br[30] wl[28] vdd gnd cell_6t
Xbit_r29_c30 bl[30] br[30] wl[29] vdd gnd cell_6t
Xbit_r30_c30 bl[30] br[30] wl[30] vdd gnd cell_6t
Xbit_r31_c30 bl[30] br[30] wl[31] vdd gnd cell_6t
Xbit_r32_c30 bl[30] br[30] wl[32] vdd gnd cell_6t
Xbit_r33_c30 bl[30] br[30] wl[33] vdd gnd cell_6t
Xbit_r34_c30 bl[30] br[30] wl[34] vdd gnd cell_6t
Xbit_r35_c30 bl[30] br[30] wl[35] vdd gnd cell_6t
Xbit_r36_c30 bl[30] br[30] wl[36] vdd gnd cell_6t
Xbit_r37_c30 bl[30] br[30] wl[37] vdd gnd cell_6t
Xbit_r38_c30 bl[30] br[30] wl[38] vdd gnd cell_6t
Xbit_r39_c30 bl[30] br[30] wl[39] vdd gnd cell_6t
Xbit_r40_c30 bl[30] br[30] wl[40] vdd gnd cell_6t
Xbit_r41_c30 bl[30] br[30] wl[41] vdd gnd cell_6t
Xbit_r42_c30 bl[30] br[30] wl[42] vdd gnd cell_6t
Xbit_r43_c30 bl[30] br[30] wl[43] vdd gnd cell_6t
Xbit_r44_c30 bl[30] br[30] wl[44] vdd gnd cell_6t
Xbit_r45_c30 bl[30] br[30] wl[45] vdd gnd cell_6t
Xbit_r46_c30 bl[30] br[30] wl[46] vdd gnd cell_6t
Xbit_r47_c30 bl[30] br[30] wl[47] vdd gnd cell_6t
Xbit_r48_c30 bl[30] br[30] wl[48] vdd gnd cell_6t
Xbit_r49_c30 bl[30] br[30] wl[49] vdd gnd cell_6t
Xbit_r50_c30 bl[30] br[30] wl[50] vdd gnd cell_6t
Xbit_r51_c30 bl[30] br[30] wl[51] vdd gnd cell_6t
Xbit_r52_c30 bl[30] br[30] wl[52] vdd gnd cell_6t
Xbit_r53_c30 bl[30] br[30] wl[53] vdd gnd cell_6t
Xbit_r54_c30 bl[30] br[30] wl[54] vdd gnd cell_6t
Xbit_r55_c30 bl[30] br[30] wl[55] vdd gnd cell_6t
Xbit_r56_c30 bl[30] br[30] wl[56] vdd gnd cell_6t
Xbit_r57_c30 bl[30] br[30] wl[57] vdd gnd cell_6t
Xbit_r58_c30 bl[30] br[30] wl[58] vdd gnd cell_6t
Xbit_r59_c30 bl[30] br[30] wl[59] vdd gnd cell_6t
Xbit_r60_c30 bl[30] br[30] wl[60] vdd gnd cell_6t
Xbit_r61_c30 bl[30] br[30] wl[61] vdd gnd cell_6t
Xbit_r62_c30 bl[30] br[30] wl[62] vdd gnd cell_6t
Xbit_r63_c30 bl[30] br[30] wl[63] vdd gnd cell_6t
Xbit_r0_c31 bl[31] br[31] wl[0] vdd gnd cell_6t
Xbit_r1_c31 bl[31] br[31] wl[1] vdd gnd cell_6t
Xbit_r2_c31 bl[31] br[31] wl[2] vdd gnd cell_6t
Xbit_r3_c31 bl[31] br[31] wl[3] vdd gnd cell_6t
Xbit_r4_c31 bl[31] br[31] wl[4] vdd gnd cell_6t
Xbit_r5_c31 bl[31] br[31] wl[5] vdd gnd cell_6t
Xbit_r6_c31 bl[31] br[31] wl[6] vdd gnd cell_6t
Xbit_r7_c31 bl[31] br[31] wl[7] vdd gnd cell_6t
Xbit_r8_c31 bl[31] br[31] wl[8] vdd gnd cell_6t
Xbit_r9_c31 bl[31] br[31] wl[9] vdd gnd cell_6t
Xbit_r10_c31 bl[31] br[31] wl[10] vdd gnd cell_6t
Xbit_r11_c31 bl[31] br[31] wl[11] vdd gnd cell_6t
Xbit_r12_c31 bl[31] br[31] wl[12] vdd gnd cell_6t
Xbit_r13_c31 bl[31] br[31] wl[13] vdd gnd cell_6t
Xbit_r14_c31 bl[31] br[31] wl[14] vdd gnd cell_6t
Xbit_r15_c31 bl[31] br[31] wl[15] vdd gnd cell_6t
Xbit_r16_c31 bl[31] br[31] wl[16] vdd gnd cell_6t
Xbit_r17_c31 bl[31] br[31] wl[17] vdd gnd cell_6t
Xbit_r18_c31 bl[31] br[31] wl[18] vdd gnd cell_6t
Xbit_r19_c31 bl[31] br[31] wl[19] vdd gnd cell_6t
Xbit_r20_c31 bl[31] br[31] wl[20] vdd gnd cell_6t
Xbit_r21_c31 bl[31] br[31] wl[21] vdd gnd cell_6t
Xbit_r22_c31 bl[31] br[31] wl[22] vdd gnd cell_6t
Xbit_r23_c31 bl[31] br[31] wl[23] vdd gnd cell_6t
Xbit_r24_c31 bl[31] br[31] wl[24] vdd gnd cell_6t
Xbit_r25_c31 bl[31] br[31] wl[25] vdd gnd cell_6t
Xbit_r26_c31 bl[31] br[31] wl[26] vdd gnd cell_6t
Xbit_r27_c31 bl[31] br[31] wl[27] vdd gnd cell_6t
Xbit_r28_c31 bl[31] br[31] wl[28] vdd gnd cell_6t
Xbit_r29_c31 bl[31] br[31] wl[29] vdd gnd cell_6t
Xbit_r30_c31 bl[31] br[31] wl[30] vdd gnd cell_6t
Xbit_r31_c31 bl[31] br[31] wl[31] vdd gnd cell_6t
Xbit_r32_c31 bl[31] br[31] wl[32] vdd gnd cell_6t
Xbit_r33_c31 bl[31] br[31] wl[33] vdd gnd cell_6t
Xbit_r34_c31 bl[31] br[31] wl[34] vdd gnd cell_6t
Xbit_r35_c31 bl[31] br[31] wl[35] vdd gnd cell_6t
Xbit_r36_c31 bl[31] br[31] wl[36] vdd gnd cell_6t
Xbit_r37_c31 bl[31] br[31] wl[37] vdd gnd cell_6t
Xbit_r38_c31 bl[31] br[31] wl[38] vdd gnd cell_6t
Xbit_r39_c31 bl[31] br[31] wl[39] vdd gnd cell_6t
Xbit_r40_c31 bl[31] br[31] wl[40] vdd gnd cell_6t
Xbit_r41_c31 bl[31] br[31] wl[41] vdd gnd cell_6t
Xbit_r42_c31 bl[31] br[31] wl[42] vdd gnd cell_6t
Xbit_r43_c31 bl[31] br[31] wl[43] vdd gnd cell_6t
Xbit_r44_c31 bl[31] br[31] wl[44] vdd gnd cell_6t
Xbit_r45_c31 bl[31] br[31] wl[45] vdd gnd cell_6t
Xbit_r46_c31 bl[31] br[31] wl[46] vdd gnd cell_6t
Xbit_r47_c31 bl[31] br[31] wl[47] vdd gnd cell_6t
Xbit_r48_c31 bl[31] br[31] wl[48] vdd gnd cell_6t
Xbit_r49_c31 bl[31] br[31] wl[49] vdd gnd cell_6t
Xbit_r50_c31 bl[31] br[31] wl[50] vdd gnd cell_6t
Xbit_r51_c31 bl[31] br[31] wl[51] vdd gnd cell_6t
Xbit_r52_c31 bl[31] br[31] wl[52] vdd gnd cell_6t
Xbit_r53_c31 bl[31] br[31] wl[53] vdd gnd cell_6t
Xbit_r54_c31 bl[31] br[31] wl[54] vdd gnd cell_6t
Xbit_r55_c31 bl[31] br[31] wl[55] vdd gnd cell_6t
Xbit_r56_c31 bl[31] br[31] wl[56] vdd gnd cell_6t
Xbit_r57_c31 bl[31] br[31] wl[57] vdd gnd cell_6t
Xbit_r58_c31 bl[31] br[31] wl[58] vdd gnd cell_6t
Xbit_r59_c31 bl[31] br[31] wl[59] vdd gnd cell_6t
Xbit_r60_c31 bl[31] br[31] wl[60] vdd gnd cell_6t
Xbit_r61_c31 bl[31] br[31] wl[61] vdd gnd cell_6t
Xbit_r62_c31 bl[31] br[31] wl[62] vdd gnd cell_6t
Xbit_r63_c31 bl[31] br[31] wl[63] vdd gnd cell_6t
Xbit_r0_c32 bl[32] br[32] wl[0] vdd gnd cell_6t
Xbit_r1_c32 bl[32] br[32] wl[1] vdd gnd cell_6t
Xbit_r2_c32 bl[32] br[32] wl[2] vdd gnd cell_6t
Xbit_r3_c32 bl[32] br[32] wl[3] vdd gnd cell_6t
Xbit_r4_c32 bl[32] br[32] wl[4] vdd gnd cell_6t
Xbit_r5_c32 bl[32] br[32] wl[5] vdd gnd cell_6t
Xbit_r6_c32 bl[32] br[32] wl[6] vdd gnd cell_6t
Xbit_r7_c32 bl[32] br[32] wl[7] vdd gnd cell_6t
Xbit_r8_c32 bl[32] br[32] wl[8] vdd gnd cell_6t
Xbit_r9_c32 bl[32] br[32] wl[9] vdd gnd cell_6t
Xbit_r10_c32 bl[32] br[32] wl[10] vdd gnd cell_6t
Xbit_r11_c32 bl[32] br[32] wl[11] vdd gnd cell_6t
Xbit_r12_c32 bl[32] br[32] wl[12] vdd gnd cell_6t
Xbit_r13_c32 bl[32] br[32] wl[13] vdd gnd cell_6t
Xbit_r14_c32 bl[32] br[32] wl[14] vdd gnd cell_6t
Xbit_r15_c32 bl[32] br[32] wl[15] vdd gnd cell_6t
Xbit_r16_c32 bl[32] br[32] wl[16] vdd gnd cell_6t
Xbit_r17_c32 bl[32] br[32] wl[17] vdd gnd cell_6t
Xbit_r18_c32 bl[32] br[32] wl[18] vdd gnd cell_6t
Xbit_r19_c32 bl[32] br[32] wl[19] vdd gnd cell_6t
Xbit_r20_c32 bl[32] br[32] wl[20] vdd gnd cell_6t
Xbit_r21_c32 bl[32] br[32] wl[21] vdd gnd cell_6t
Xbit_r22_c32 bl[32] br[32] wl[22] vdd gnd cell_6t
Xbit_r23_c32 bl[32] br[32] wl[23] vdd gnd cell_6t
Xbit_r24_c32 bl[32] br[32] wl[24] vdd gnd cell_6t
Xbit_r25_c32 bl[32] br[32] wl[25] vdd gnd cell_6t
Xbit_r26_c32 bl[32] br[32] wl[26] vdd gnd cell_6t
Xbit_r27_c32 bl[32] br[32] wl[27] vdd gnd cell_6t
Xbit_r28_c32 bl[32] br[32] wl[28] vdd gnd cell_6t
Xbit_r29_c32 bl[32] br[32] wl[29] vdd gnd cell_6t
Xbit_r30_c32 bl[32] br[32] wl[30] vdd gnd cell_6t
Xbit_r31_c32 bl[32] br[32] wl[31] vdd gnd cell_6t
Xbit_r32_c32 bl[32] br[32] wl[32] vdd gnd cell_6t
Xbit_r33_c32 bl[32] br[32] wl[33] vdd gnd cell_6t
Xbit_r34_c32 bl[32] br[32] wl[34] vdd gnd cell_6t
Xbit_r35_c32 bl[32] br[32] wl[35] vdd gnd cell_6t
Xbit_r36_c32 bl[32] br[32] wl[36] vdd gnd cell_6t
Xbit_r37_c32 bl[32] br[32] wl[37] vdd gnd cell_6t
Xbit_r38_c32 bl[32] br[32] wl[38] vdd gnd cell_6t
Xbit_r39_c32 bl[32] br[32] wl[39] vdd gnd cell_6t
Xbit_r40_c32 bl[32] br[32] wl[40] vdd gnd cell_6t
Xbit_r41_c32 bl[32] br[32] wl[41] vdd gnd cell_6t
Xbit_r42_c32 bl[32] br[32] wl[42] vdd gnd cell_6t
Xbit_r43_c32 bl[32] br[32] wl[43] vdd gnd cell_6t
Xbit_r44_c32 bl[32] br[32] wl[44] vdd gnd cell_6t
Xbit_r45_c32 bl[32] br[32] wl[45] vdd gnd cell_6t
Xbit_r46_c32 bl[32] br[32] wl[46] vdd gnd cell_6t
Xbit_r47_c32 bl[32] br[32] wl[47] vdd gnd cell_6t
Xbit_r48_c32 bl[32] br[32] wl[48] vdd gnd cell_6t
Xbit_r49_c32 bl[32] br[32] wl[49] vdd gnd cell_6t
Xbit_r50_c32 bl[32] br[32] wl[50] vdd gnd cell_6t
Xbit_r51_c32 bl[32] br[32] wl[51] vdd gnd cell_6t
Xbit_r52_c32 bl[32] br[32] wl[52] vdd gnd cell_6t
Xbit_r53_c32 bl[32] br[32] wl[53] vdd gnd cell_6t
Xbit_r54_c32 bl[32] br[32] wl[54] vdd gnd cell_6t
Xbit_r55_c32 bl[32] br[32] wl[55] vdd gnd cell_6t
Xbit_r56_c32 bl[32] br[32] wl[56] vdd gnd cell_6t
Xbit_r57_c32 bl[32] br[32] wl[57] vdd gnd cell_6t
Xbit_r58_c32 bl[32] br[32] wl[58] vdd gnd cell_6t
Xbit_r59_c32 bl[32] br[32] wl[59] vdd gnd cell_6t
Xbit_r60_c32 bl[32] br[32] wl[60] vdd gnd cell_6t
Xbit_r61_c32 bl[32] br[32] wl[61] vdd gnd cell_6t
Xbit_r62_c32 bl[32] br[32] wl[62] vdd gnd cell_6t
Xbit_r63_c32 bl[32] br[32] wl[63] vdd gnd cell_6t
Xbit_r0_c33 bl[33] br[33] wl[0] vdd gnd cell_6t
Xbit_r1_c33 bl[33] br[33] wl[1] vdd gnd cell_6t
Xbit_r2_c33 bl[33] br[33] wl[2] vdd gnd cell_6t
Xbit_r3_c33 bl[33] br[33] wl[3] vdd gnd cell_6t
Xbit_r4_c33 bl[33] br[33] wl[4] vdd gnd cell_6t
Xbit_r5_c33 bl[33] br[33] wl[5] vdd gnd cell_6t
Xbit_r6_c33 bl[33] br[33] wl[6] vdd gnd cell_6t
Xbit_r7_c33 bl[33] br[33] wl[7] vdd gnd cell_6t
Xbit_r8_c33 bl[33] br[33] wl[8] vdd gnd cell_6t
Xbit_r9_c33 bl[33] br[33] wl[9] vdd gnd cell_6t
Xbit_r10_c33 bl[33] br[33] wl[10] vdd gnd cell_6t
Xbit_r11_c33 bl[33] br[33] wl[11] vdd gnd cell_6t
Xbit_r12_c33 bl[33] br[33] wl[12] vdd gnd cell_6t
Xbit_r13_c33 bl[33] br[33] wl[13] vdd gnd cell_6t
Xbit_r14_c33 bl[33] br[33] wl[14] vdd gnd cell_6t
Xbit_r15_c33 bl[33] br[33] wl[15] vdd gnd cell_6t
Xbit_r16_c33 bl[33] br[33] wl[16] vdd gnd cell_6t
Xbit_r17_c33 bl[33] br[33] wl[17] vdd gnd cell_6t
Xbit_r18_c33 bl[33] br[33] wl[18] vdd gnd cell_6t
Xbit_r19_c33 bl[33] br[33] wl[19] vdd gnd cell_6t
Xbit_r20_c33 bl[33] br[33] wl[20] vdd gnd cell_6t
Xbit_r21_c33 bl[33] br[33] wl[21] vdd gnd cell_6t
Xbit_r22_c33 bl[33] br[33] wl[22] vdd gnd cell_6t
Xbit_r23_c33 bl[33] br[33] wl[23] vdd gnd cell_6t
Xbit_r24_c33 bl[33] br[33] wl[24] vdd gnd cell_6t
Xbit_r25_c33 bl[33] br[33] wl[25] vdd gnd cell_6t
Xbit_r26_c33 bl[33] br[33] wl[26] vdd gnd cell_6t
Xbit_r27_c33 bl[33] br[33] wl[27] vdd gnd cell_6t
Xbit_r28_c33 bl[33] br[33] wl[28] vdd gnd cell_6t
Xbit_r29_c33 bl[33] br[33] wl[29] vdd gnd cell_6t
Xbit_r30_c33 bl[33] br[33] wl[30] vdd gnd cell_6t
Xbit_r31_c33 bl[33] br[33] wl[31] vdd gnd cell_6t
Xbit_r32_c33 bl[33] br[33] wl[32] vdd gnd cell_6t
Xbit_r33_c33 bl[33] br[33] wl[33] vdd gnd cell_6t
Xbit_r34_c33 bl[33] br[33] wl[34] vdd gnd cell_6t
Xbit_r35_c33 bl[33] br[33] wl[35] vdd gnd cell_6t
Xbit_r36_c33 bl[33] br[33] wl[36] vdd gnd cell_6t
Xbit_r37_c33 bl[33] br[33] wl[37] vdd gnd cell_6t
Xbit_r38_c33 bl[33] br[33] wl[38] vdd gnd cell_6t
Xbit_r39_c33 bl[33] br[33] wl[39] vdd gnd cell_6t
Xbit_r40_c33 bl[33] br[33] wl[40] vdd gnd cell_6t
Xbit_r41_c33 bl[33] br[33] wl[41] vdd gnd cell_6t
Xbit_r42_c33 bl[33] br[33] wl[42] vdd gnd cell_6t
Xbit_r43_c33 bl[33] br[33] wl[43] vdd gnd cell_6t
Xbit_r44_c33 bl[33] br[33] wl[44] vdd gnd cell_6t
Xbit_r45_c33 bl[33] br[33] wl[45] vdd gnd cell_6t
Xbit_r46_c33 bl[33] br[33] wl[46] vdd gnd cell_6t
Xbit_r47_c33 bl[33] br[33] wl[47] vdd gnd cell_6t
Xbit_r48_c33 bl[33] br[33] wl[48] vdd gnd cell_6t
Xbit_r49_c33 bl[33] br[33] wl[49] vdd gnd cell_6t
Xbit_r50_c33 bl[33] br[33] wl[50] vdd gnd cell_6t
Xbit_r51_c33 bl[33] br[33] wl[51] vdd gnd cell_6t
Xbit_r52_c33 bl[33] br[33] wl[52] vdd gnd cell_6t
Xbit_r53_c33 bl[33] br[33] wl[53] vdd gnd cell_6t
Xbit_r54_c33 bl[33] br[33] wl[54] vdd gnd cell_6t
Xbit_r55_c33 bl[33] br[33] wl[55] vdd gnd cell_6t
Xbit_r56_c33 bl[33] br[33] wl[56] vdd gnd cell_6t
Xbit_r57_c33 bl[33] br[33] wl[57] vdd gnd cell_6t
Xbit_r58_c33 bl[33] br[33] wl[58] vdd gnd cell_6t
Xbit_r59_c33 bl[33] br[33] wl[59] vdd gnd cell_6t
Xbit_r60_c33 bl[33] br[33] wl[60] vdd gnd cell_6t
Xbit_r61_c33 bl[33] br[33] wl[61] vdd gnd cell_6t
Xbit_r62_c33 bl[33] br[33] wl[62] vdd gnd cell_6t
Xbit_r63_c33 bl[33] br[33] wl[63] vdd gnd cell_6t
Xbit_r0_c34 bl[34] br[34] wl[0] vdd gnd cell_6t
Xbit_r1_c34 bl[34] br[34] wl[1] vdd gnd cell_6t
Xbit_r2_c34 bl[34] br[34] wl[2] vdd gnd cell_6t
Xbit_r3_c34 bl[34] br[34] wl[3] vdd gnd cell_6t
Xbit_r4_c34 bl[34] br[34] wl[4] vdd gnd cell_6t
Xbit_r5_c34 bl[34] br[34] wl[5] vdd gnd cell_6t
Xbit_r6_c34 bl[34] br[34] wl[6] vdd gnd cell_6t
Xbit_r7_c34 bl[34] br[34] wl[7] vdd gnd cell_6t
Xbit_r8_c34 bl[34] br[34] wl[8] vdd gnd cell_6t
Xbit_r9_c34 bl[34] br[34] wl[9] vdd gnd cell_6t
Xbit_r10_c34 bl[34] br[34] wl[10] vdd gnd cell_6t
Xbit_r11_c34 bl[34] br[34] wl[11] vdd gnd cell_6t
Xbit_r12_c34 bl[34] br[34] wl[12] vdd gnd cell_6t
Xbit_r13_c34 bl[34] br[34] wl[13] vdd gnd cell_6t
Xbit_r14_c34 bl[34] br[34] wl[14] vdd gnd cell_6t
Xbit_r15_c34 bl[34] br[34] wl[15] vdd gnd cell_6t
Xbit_r16_c34 bl[34] br[34] wl[16] vdd gnd cell_6t
Xbit_r17_c34 bl[34] br[34] wl[17] vdd gnd cell_6t
Xbit_r18_c34 bl[34] br[34] wl[18] vdd gnd cell_6t
Xbit_r19_c34 bl[34] br[34] wl[19] vdd gnd cell_6t
Xbit_r20_c34 bl[34] br[34] wl[20] vdd gnd cell_6t
Xbit_r21_c34 bl[34] br[34] wl[21] vdd gnd cell_6t
Xbit_r22_c34 bl[34] br[34] wl[22] vdd gnd cell_6t
Xbit_r23_c34 bl[34] br[34] wl[23] vdd gnd cell_6t
Xbit_r24_c34 bl[34] br[34] wl[24] vdd gnd cell_6t
Xbit_r25_c34 bl[34] br[34] wl[25] vdd gnd cell_6t
Xbit_r26_c34 bl[34] br[34] wl[26] vdd gnd cell_6t
Xbit_r27_c34 bl[34] br[34] wl[27] vdd gnd cell_6t
Xbit_r28_c34 bl[34] br[34] wl[28] vdd gnd cell_6t
Xbit_r29_c34 bl[34] br[34] wl[29] vdd gnd cell_6t
Xbit_r30_c34 bl[34] br[34] wl[30] vdd gnd cell_6t
Xbit_r31_c34 bl[34] br[34] wl[31] vdd gnd cell_6t
Xbit_r32_c34 bl[34] br[34] wl[32] vdd gnd cell_6t
Xbit_r33_c34 bl[34] br[34] wl[33] vdd gnd cell_6t
Xbit_r34_c34 bl[34] br[34] wl[34] vdd gnd cell_6t
Xbit_r35_c34 bl[34] br[34] wl[35] vdd gnd cell_6t
Xbit_r36_c34 bl[34] br[34] wl[36] vdd gnd cell_6t
Xbit_r37_c34 bl[34] br[34] wl[37] vdd gnd cell_6t
Xbit_r38_c34 bl[34] br[34] wl[38] vdd gnd cell_6t
Xbit_r39_c34 bl[34] br[34] wl[39] vdd gnd cell_6t
Xbit_r40_c34 bl[34] br[34] wl[40] vdd gnd cell_6t
Xbit_r41_c34 bl[34] br[34] wl[41] vdd gnd cell_6t
Xbit_r42_c34 bl[34] br[34] wl[42] vdd gnd cell_6t
Xbit_r43_c34 bl[34] br[34] wl[43] vdd gnd cell_6t
Xbit_r44_c34 bl[34] br[34] wl[44] vdd gnd cell_6t
Xbit_r45_c34 bl[34] br[34] wl[45] vdd gnd cell_6t
Xbit_r46_c34 bl[34] br[34] wl[46] vdd gnd cell_6t
Xbit_r47_c34 bl[34] br[34] wl[47] vdd gnd cell_6t
Xbit_r48_c34 bl[34] br[34] wl[48] vdd gnd cell_6t
Xbit_r49_c34 bl[34] br[34] wl[49] vdd gnd cell_6t
Xbit_r50_c34 bl[34] br[34] wl[50] vdd gnd cell_6t
Xbit_r51_c34 bl[34] br[34] wl[51] vdd gnd cell_6t
Xbit_r52_c34 bl[34] br[34] wl[52] vdd gnd cell_6t
Xbit_r53_c34 bl[34] br[34] wl[53] vdd gnd cell_6t
Xbit_r54_c34 bl[34] br[34] wl[54] vdd gnd cell_6t
Xbit_r55_c34 bl[34] br[34] wl[55] vdd gnd cell_6t
Xbit_r56_c34 bl[34] br[34] wl[56] vdd gnd cell_6t
Xbit_r57_c34 bl[34] br[34] wl[57] vdd gnd cell_6t
Xbit_r58_c34 bl[34] br[34] wl[58] vdd gnd cell_6t
Xbit_r59_c34 bl[34] br[34] wl[59] vdd gnd cell_6t
Xbit_r60_c34 bl[34] br[34] wl[60] vdd gnd cell_6t
Xbit_r61_c34 bl[34] br[34] wl[61] vdd gnd cell_6t
Xbit_r62_c34 bl[34] br[34] wl[62] vdd gnd cell_6t
Xbit_r63_c34 bl[34] br[34] wl[63] vdd gnd cell_6t
Xbit_r0_c35 bl[35] br[35] wl[0] vdd gnd cell_6t
Xbit_r1_c35 bl[35] br[35] wl[1] vdd gnd cell_6t
Xbit_r2_c35 bl[35] br[35] wl[2] vdd gnd cell_6t
Xbit_r3_c35 bl[35] br[35] wl[3] vdd gnd cell_6t
Xbit_r4_c35 bl[35] br[35] wl[4] vdd gnd cell_6t
Xbit_r5_c35 bl[35] br[35] wl[5] vdd gnd cell_6t
Xbit_r6_c35 bl[35] br[35] wl[6] vdd gnd cell_6t
Xbit_r7_c35 bl[35] br[35] wl[7] vdd gnd cell_6t
Xbit_r8_c35 bl[35] br[35] wl[8] vdd gnd cell_6t
Xbit_r9_c35 bl[35] br[35] wl[9] vdd gnd cell_6t
Xbit_r10_c35 bl[35] br[35] wl[10] vdd gnd cell_6t
Xbit_r11_c35 bl[35] br[35] wl[11] vdd gnd cell_6t
Xbit_r12_c35 bl[35] br[35] wl[12] vdd gnd cell_6t
Xbit_r13_c35 bl[35] br[35] wl[13] vdd gnd cell_6t
Xbit_r14_c35 bl[35] br[35] wl[14] vdd gnd cell_6t
Xbit_r15_c35 bl[35] br[35] wl[15] vdd gnd cell_6t
Xbit_r16_c35 bl[35] br[35] wl[16] vdd gnd cell_6t
Xbit_r17_c35 bl[35] br[35] wl[17] vdd gnd cell_6t
Xbit_r18_c35 bl[35] br[35] wl[18] vdd gnd cell_6t
Xbit_r19_c35 bl[35] br[35] wl[19] vdd gnd cell_6t
Xbit_r20_c35 bl[35] br[35] wl[20] vdd gnd cell_6t
Xbit_r21_c35 bl[35] br[35] wl[21] vdd gnd cell_6t
Xbit_r22_c35 bl[35] br[35] wl[22] vdd gnd cell_6t
Xbit_r23_c35 bl[35] br[35] wl[23] vdd gnd cell_6t
Xbit_r24_c35 bl[35] br[35] wl[24] vdd gnd cell_6t
Xbit_r25_c35 bl[35] br[35] wl[25] vdd gnd cell_6t
Xbit_r26_c35 bl[35] br[35] wl[26] vdd gnd cell_6t
Xbit_r27_c35 bl[35] br[35] wl[27] vdd gnd cell_6t
Xbit_r28_c35 bl[35] br[35] wl[28] vdd gnd cell_6t
Xbit_r29_c35 bl[35] br[35] wl[29] vdd gnd cell_6t
Xbit_r30_c35 bl[35] br[35] wl[30] vdd gnd cell_6t
Xbit_r31_c35 bl[35] br[35] wl[31] vdd gnd cell_6t
Xbit_r32_c35 bl[35] br[35] wl[32] vdd gnd cell_6t
Xbit_r33_c35 bl[35] br[35] wl[33] vdd gnd cell_6t
Xbit_r34_c35 bl[35] br[35] wl[34] vdd gnd cell_6t
Xbit_r35_c35 bl[35] br[35] wl[35] vdd gnd cell_6t
Xbit_r36_c35 bl[35] br[35] wl[36] vdd gnd cell_6t
Xbit_r37_c35 bl[35] br[35] wl[37] vdd gnd cell_6t
Xbit_r38_c35 bl[35] br[35] wl[38] vdd gnd cell_6t
Xbit_r39_c35 bl[35] br[35] wl[39] vdd gnd cell_6t
Xbit_r40_c35 bl[35] br[35] wl[40] vdd gnd cell_6t
Xbit_r41_c35 bl[35] br[35] wl[41] vdd gnd cell_6t
Xbit_r42_c35 bl[35] br[35] wl[42] vdd gnd cell_6t
Xbit_r43_c35 bl[35] br[35] wl[43] vdd gnd cell_6t
Xbit_r44_c35 bl[35] br[35] wl[44] vdd gnd cell_6t
Xbit_r45_c35 bl[35] br[35] wl[45] vdd gnd cell_6t
Xbit_r46_c35 bl[35] br[35] wl[46] vdd gnd cell_6t
Xbit_r47_c35 bl[35] br[35] wl[47] vdd gnd cell_6t
Xbit_r48_c35 bl[35] br[35] wl[48] vdd gnd cell_6t
Xbit_r49_c35 bl[35] br[35] wl[49] vdd gnd cell_6t
Xbit_r50_c35 bl[35] br[35] wl[50] vdd gnd cell_6t
Xbit_r51_c35 bl[35] br[35] wl[51] vdd gnd cell_6t
Xbit_r52_c35 bl[35] br[35] wl[52] vdd gnd cell_6t
Xbit_r53_c35 bl[35] br[35] wl[53] vdd gnd cell_6t
Xbit_r54_c35 bl[35] br[35] wl[54] vdd gnd cell_6t
Xbit_r55_c35 bl[35] br[35] wl[55] vdd gnd cell_6t
Xbit_r56_c35 bl[35] br[35] wl[56] vdd gnd cell_6t
Xbit_r57_c35 bl[35] br[35] wl[57] vdd gnd cell_6t
Xbit_r58_c35 bl[35] br[35] wl[58] vdd gnd cell_6t
Xbit_r59_c35 bl[35] br[35] wl[59] vdd gnd cell_6t
Xbit_r60_c35 bl[35] br[35] wl[60] vdd gnd cell_6t
Xbit_r61_c35 bl[35] br[35] wl[61] vdd gnd cell_6t
Xbit_r62_c35 bl[35] br[35] wl[62] vdd gnd cell_6t
Xbit_r63_c35 bl[35] br[35] wl[63] vdd gnd cell_6t
Xbit_r0_c36 bl[36] br[36] wl[0] vdd gnd cell_6t
Xbit_r1_c36 bl[36] br[36] wl[1] vdd gnd cell_6t
Xbit_r2_c36 bl[36] br[36] wl[2] vdd gnd cell_6t
Xbit_r3_c36 bl[36] br[36] wl[3] vdd gnd cell_6t
Xbit_r4_c36 bl[36] br[36] wl[4] vdd gnd cell_6t
Xbit_r5_c36 bl[36] br[36] wl[5] vdd gnd cell_6t
Xbit_r6_c36 bl[36] br[36] wl[6] vdd gnd cell_6t
Xbit_r7_c36 bl[36] br[36] wl[7] vdd gnd cell_6t
Xbit_r8_c36 bl[36] br[36] wl[8] vdd gnd cell_6t
Xbit_r9_c36 bl[36] br[36] wl[9] vdd gnd cell_6t
Xbit_r10_c36 bl[36] br[36] wl[10] vdd gnd cell_6t
Xbit_r11_c36 bl[36] br[36] wl[11] vdd gnd cell_6t
Xbit_r12_c36 bl[36] br[36] wl[12] vdd gnd cell_6t
Xbit_r13_c36 bl[36] br[36] wl[13] vdd gnd cell_6t
Xbit_r14_c36 bl[36] br[36] wl[14] vdd gnd cell_6t
Xbit_r15_c36 bl[36] br[36] wl[15] vdd gnd cell_6t
Xbit_r16_c36 bl[36] br[36] wl[16] vdd gnd cell_6t
Xbit_r17_c36 bl[36] br[36] wl[17] vdd gnd cell_6t
Xbit_r18_c36 bl[36] br[36] wl[18] vdd gnd cell_6t
Xbit_r19_c36 bl[36] br[36] wl[19] vdd gnd cell_6t
Xbit_r20_c36 bl[36] br[36] wl[20] vdd gnd cell_6t
Xbit_r21_c36 bl[36] br[36] wl[21] vdd gnd cell_6t
Xbit_r22_c36 bl[36] br[36] wl[22] vdd gnd cell_6t
Xbit_r23_c36 bl[36] br[36] wl[23] vdd gnd cell_6t
Xbit_r24_c36 bl[36] br[36] wl[24] vdd gnd cell_6t
Xbit_r25_c36 bl[36] br[36] wl[25] vdd gnd cell_6t
Xbit_r26_c36 bl[36] br[36] wl[26] vdd gnd cell_6t
Xbit_r27_c36 bl[36] br[36] wl[27] vdd gnd cell_6t
Xbit_r28_c36 bl[36] br[36] wl[28] vdd gnd cell_6t
Xbit_r29_c36 bl[36] br[36] wl[29] vdd gnd cell_6t
Xbit_r30_c36 bl[36] br[36] wl[30] vdd gnd cell_6t
Xbit_r31_c36 bl[36] br[36] wl[31] vdd gnd cell_6t
Xbit_r32_c36 bl[36] br[36] wl[32] vdd gnd cell_6t
Xbit_r33_c36 bl[36] br[36] wl[33] vdd gnd cell_6t
Xbit_r34_c36 bl[36] br[36] wl[34] vdd gnd cell_6t
Xbit_r35_c36 bl[36] br[36] wl[35] vdd gnd cell_6t
Xbit_r36_c36 bl[36] br[36] wl[36] vdd gnd cell_6t
Xbit_r37_c36 bl[36] br[36] wl[37] vdd gnd cell_6t
Xbit_r38_c36 bl[36] br[36] wl[38] vdd gnd cell_6t
Xbit_r39_c36 bl[36] br[36] wl[39] vdd gnd cell_6t
Xbit_r40_c36 bl[36] br[36] wl[40] vdd gnd cell_6t
Xbit_r41_c36 bl[36] br[36] wl[41] vdd gnd cell_6t
Xbit_r42_c36 bl[36] br[36] wl[42] vdd gnd cell_6t
Xbit_r43_c36 bl[36] br[36] wl[43] vdd gnd cell_6t
Xbit_r44_c36 bl[36] br[36] wl[44] vdd gnd cell_6t
Xbit_r45_c36 bl[36] br[36] wl[45] vdd gnd cell_6t
Xbit_r46_c36 bl[36] br[36] wl[46] vdd gnd cell_6t
Xbit_r47_c36 bl[36] br[36] wl[47] vdd gnd cell_6t
Xbit_r48_c36 bl[36] br[36] wl[48] vdd gnd cell_6t
Xbit_r49_c36 bl[36] br[36] wl[49] vdd gnd cell_6t
Xbit_r50_c36 bl[36] br[36] wl[50] vdd gnd cell_6t
Xbit_r51_c36 bl[36] br[36] wl[51] vdd gnd cell_6t
Xbit_r52_c36 bl[36] br[36] wl[52] vdd gnd cell_6t
Xbit_r53_c36 bl[36] br[36] wl[53] vdd gnd cell_6t
Xbit_r54_c36 bl[36] br[36] wl[54] vdd gnd cell_6t
Xbit_r55_c36 bl[36] br[36] wl[55] vdd gnd cell_6t
Xbit_r56_c36 bl[36] br[36] wl[56] vdd gnd cell_6t
Xbit_r57_c36 bl[36] br[36] wl[57] vdd gnd cell_6t
Xbit_r58_c36 bl[36] br[36] wl[58] vdd gnd cell_6t
Xbit_r59_c36 bl[36] br[36] wl[59] vdd gnd cell_6t
Xbit_r60_c36 bl[36] br[36] wl[60] vdd gnd cell_6t
Xbit_r61_c36 bl[36] br[36] wl[61] vdd gnd cell_6t
Xbit_r62_c36 bl[36] br[36] wl[62] vdd gnd cell_6t
Xbit_r63_c36 bl[36] br[36] wl[63] vdd gnd cell_6t
Xbit_r0_c37 bl[37] br[37] wl[0] vdd gnd cell_6t
Xbit_r1_c37 bl[37] br[37] wl[1] vdd gnd cell_6t
Xbit_r2_c37 bl[37] br[37] wl[2] vdd gnd cell_6t
Xbit_r3_c37 bl[37] br[37] wl[3] vdd gnd cell_6t
Xbit_r4_c37 bl[37] br[37] wl[4] vdd gnd cell_6t
Xbit_r5_c37 bl[37] br[37] wl[5] vdd gnd cell_6t
Xbit_r6_c37 bl[37] br[37] wl[6] vdd gnd cell_6t
Xbit_r7_c37 bl[37] br[37] wl[7] vdd gnd cell_6t
Xbit_r8_c37 bl[37] br[37] wl[8] vdd gnd cell_6t
Xbit_r9_c37 bl[37] br[37] wl[9] vdd gnd cell_6t
Xbit_r10_c37 bl[37] br[37] wl[10] vdd gnd cell_6t
Xbit_r11_c37 bl[37] br[37] wl[11] vdd gnd cell_6t
Xbit_r12_c37 bl[37] br[37] wl[12] vdd gnd cell_6t
Xbit_r13_c37 bl[37] br[37] wl[13] vdd gnd cell_6t
Xbit_r14_c37 bl[37] br[37] wl[14] vdd gnd cell_6t
Xbit_r15_c37 bl[37] br[37] wl[15] vdd gnd cell_6t
Xbit_r16_c37 bl[37] br[37] wl[16] vdd gnd cell_6t
Xbit_r17_c37 bl[37] br[37] wl[17] vdd gnd cell_6t
Xbit_r18_c37 bl[37] br[37] wl[18] vdd gnd cell_6t
Xbit_r19_c37 bl[37] br[37] wl[19] vdd gnd cell_6t
Xbit_r20_c37 bl[37] br[37] wl[20] vdd gnd cell_6t
Xbit_r21_c37 bl[37] br[37] wl[21] vdd gnd cell_6t
Xbit_r22_c37 bl[37] br[37] wl[22] vdd gnd cell_6t
Xbit_r23_c37 bl[37] br[37] wl[23] vdd gnd cell_6t
Xbit_r24_c37 bl[37] br[37] wl[24] vdd gnd cell_6t
Xbit_r25_c37 bl[37] br[37] wl[25] vdd gnd cell_6t
Xbit_r26_c37 bl[37] br[37] wl[26] vdd gnd cell_6t
Xbit_r27_c37 bl[37] br[37] wl[27] vdd gnd cell_6t
Xbit_r28_c37 bl[37] br[37] wl[28] vdd gnd cell_6t
Xbit_r29_c37 bl[37] br[37] wl[29] vdd gnd cell_6t
Xbit_r30_c37 bl[37] br[37] wl[30] vdd gnd cell_6t
Xbit_r31_c37 bl[37] br[37] wl[31] vdd gnd cell_6t
Xbit_r32_c37 bl[37] br[37] wl[32] vdd gnd cell_6t
Xbit_r33_c37 bl[37] br[37] wl[33] vdd gnd cell_6t
Xbit_r34_c37 bl[37] br[37] wl[34] vdd gnd cell_6t
Xbit_r35_c37 bl[37] br[37] wl[35] vdd gnd cell_6t
Xbit_r36_c37 bl[37] br[37] wl[36] vdd gnd cell_6t
Xbit_r37_c37 bl[37] br[37] wl[37] vdd gnd cell_6t
Xbit_r38_c37 bl[37] br[37] wl[38] vdd gnd cell_6t
Xbit_r39_c37 bl[37] br[37] wl[39] vdd gnd cell_6t
Xbit_r40_c37 bl[37] br[37] wl[40] vdd gnd cell_6t
Xbit_r41_c37 bl[37] br[37] wl[41] vdd gnd cell_6t
Xbit_r42_c37 bl[37] br[37] wl[42] vdd gnd cell_6t
Xbit_r43_c37 bl[37] br[37] wl[43] vdd gnd cell_6t
Xbit_r44_c37 bl[37] br[37] wl[44] vdd gnd cell_6t
Xbit_r45_c37 bl[37] br[37] wl[45] vdd gnd cell_6t
Xbit_r46_c37 bl[37] br[37] wl[46] vdd gnd cell_6t
Xbit_r47_c37 bl[37] br[37] wl[47] vdd gnd cell_6t
Xbit_r48_c37 bl[37] br[37] wl[48] vdd gnd cell_6t
Xbit_r49_c37 bl[37] br[37] wl[49] vdd gnd cell_6t
Xbit_r50_c37 bl[37] br[37] wl[50] vdd gnd cell_6t
Xbit_r51_c37 bl[37] br[37] wl[51] vdd gnd cell_6t
Xbit_r52_c37 bl[37] br[37] wl[52] vdd gnd cell_6t
Xbit_r53_c37 bl[37] br[37] wl[53] vdd gnd cell_6t
Xbit_r54_c37 bl[37] br[37] wl[54] vdd gnd cell_6t
Xbit_r55_c37 bl[37] br[37] wl[55] vdd gnd cell_6t
Xbit_r56_c37 bl[37] br[37] wl[56] vdd gnd cell_6t
Xbit_r57_c37 bl[37] br[37] wl[57] vdd gnd cell_6t
Xbit_r58_c37 bl[37] br[37] wl[58] vdd gnd cell_6t
Xbit_r59_c37 bl[37] br[37] wl[59] vdd gnd cell_6t
Xbit_r60_c37 bl[37] br[37] wl[60] vdd gnd cell_6t
Xbit_r61_c37 bl[37] br[37] wl[61] vdd gnd cell_6t
Xbit_r62_c37 bl[37] br[37] wl[62] vdd gnd cell_6t
Xbit_r63_c37 bl[37] br[37] wl[63] vdd gnd cell_6t
Xbit_r0_c38 bl[38] br[38] wl[0] vdd gnd cell_6t
Xbit_r1_c38 bl[38] br[38] wl[1] vdd gnd cell_6t
Xbit_r2_c38 bl[38] br[38] wl[2] vdd gnd cell_6t
Xbit_r3_c38 bl[38] br[38] wl[3] vdd gnd cell_6t
Xbit_r4_c38 bl[38] br[38] wl[4] vdd gnd cell_6t
Xbit_r5_c38 bl[38] br[38] wl[5] vdd gnd cell_6t
Xbit_r6_c38 bl[38] br[38] wl[6] vdd gnd cell_6t
Xbit_r7_c38 bl[38] br[38] wl[7] vdd gnd cell_6t
Xbit_r8_c38 bl[38] br[38] wl[8] vdd gnd cell_6t
Xbit_r9_c38 bl[38] br[38] wl[9] vdd gnd cell_6t
Xbit_r10_c38 bl[38] br[38] wl[10] vdd gnd cell_6t
Xbit_r11_c38 bl[38] br[38] wl[11] vdd gnd cell_6t
Xbit_r12_c38 bl[38] br[38] wl[12] vdd gnd cell_6t
Xbit_r13_c38 bl[38] br[38] wl[13] vdd gnd cell_6t
Xbit_r14_c38 bl[38] br[38] wl[14] vdd gnd cell_6t
Xbit_r15_c38 bl[38] br[38] wl[15] vdd gnd cell_6t
Xbit_r16_c38 bl[38] br[38] wl[16] vdd gnd cell_6t
Xbit_r17_c38 bl[38] br[38] wl[17] vdd gnd cell_6t
Xbit_r18_c38 bl[38] br[38] wl[18] vdd gnd cell_6t
Xbit_r19_c38 bl[38] br[38] wl[19] vdd gnd cell_6t
Xbit_r20_c38 bl[38] br[38] wl[20] vdd gnd cell_6t
Xbit_r21_c38 bl[38] br[38] wl[21] vdd gnd cell_6t
Xbit_r22_c38 bl[38] br[38] wl[22] vdd gnd cell_6t
Xbit_r23_c38 bl[38] br[38] wl[23] vdd gnd cell_6t
Xbit_r24_c38 bl[38] br[38] wl[24] vdd gnd cell_6t
Xbit_r25_c38 bl[38] br[38] wl[25] vdd gnd cell_6t
Xbit_r26_c38 bl[38] br[38] wl[26] vdd gnd cell_6t
Xbit_r27_c38 bl[38] br[38] wl[27] vdd gnd cell_6t
Xbit_r28_c38 bl[38] br[38] wl[28] vdd gnd cell_6t
Xbit_r29_c38 bl[38] br[38] wl[29] vdd gnd cell_6t
Xbit_r30_c38 bl[38] br[38] wl[30] vdd gnd cell_6t
Xbit_r31_c38 bl[38] br[38] wl[31] vdd gnd cell_6t
Xbit_r32_c38 bl[38] br[38] wl[32] vdd gnd cell_6t
Xbit_r33_c38 bl[38] br[38] wl[33] vdd gnd cell_6t
Xbit_r34_c38 bl[38] br[38] wl[34] vdd gnd cell_6t
Xbit_r35_c38 bl[38] br[38] wl[35] vdd gnd cell_6t
Xbit_r36_c38 bl[38] br[38] wl[36] vdd gnd cell_6t
Xbit_r37_c38 bl[38] br[38] wl[37] vdd gnd cell_6t
Xbit_r38_c38 bl[38] br[38] wl[38] vdd gnd cell_6t
Xbit_r39_c38 bl[38] br[38] wl[39] vdd gnd cell_6t
Xbit_r40_c38 bl[38] br[38] wl[40] vdd gnd cell_6t
Xbit_r41_c38 bl[38] br[38] wl[41] vdd gnd cell_6t
Xbit_r42_c38 bl[38] br[38] wl[42] vdd gnd cell_6t
Xbit_r43_c38 bl[38] br[38] wl[43] vdd gnd cell_6t
Xbit_r44_c38 bl[38] br[38] wl[44] vdd gnd cell_6t
Xbit_r45_c38 bl[38] br[38] wl[45] vdd gnd cell_6t
Xbit_r46_c38 bl[38] br[38] wl[46] vdd gnd cell_6t
Xbit_r47_c38 bl[38] br[38] wl[47] vdd gnd cell_6t
Xbit_r48_c38 bl[38] br[38] wl[48] vdd gnd cell_6t
Xbit_r49_c38 bl[38] br[38] wl[49] vdd gnd cell_6t
Xbit_r50_c38 bl[38] br[38] wl[50] vdd gnd cell_6t
Xbit_r51_c38 bl[38] br[38] wl[51] vdd gnd cell_6t
Xbit_r52_c38 bl[38] br[38] wl[52] vdd gnd cell_6t
Xbit_r53_c38 bl[38] br[38] wl[53] vdd gnd cell_6t
Xbit_r54_c38 bl[38] br[38] wl[54] vdd gnd cell_6t
Xbit_r55_c38 bl[38] br[38] wl[55] vdd gnd cell_6t
Xbit_r56_c38 bl[38] br[38] wl[56] vdd gnd cell_6t
Xbit_r57_c38 bl[38] br[38] wl[57] vdd gnd cell_6t
Xbit_r58_c38 bl[38] br[38] wl[58] vdd gnd cell_6t
Xbit_r59_c38 bl[38] br[38] wl[59] vdd gnd cell_6t
Xbit_r60_c38 bl[38] br[38] wl[60] vdd gnd cell_6t
Xbit_r61_c38 bl[38] br[38] wl[61] vdd gnd cell_6t
Xbit_r62_c38 bl[38] br[38] wl[62] vdd gnd cell_6t
Xbit_r63_c38 bl[38] br[38] wl[63] vdd gnd cell_6t
Xbit_r0_c39 bl[39] br[39] wl[0] vdd gnd cell_6t
Xbit_r1_c39 bl[39] br[39] wl[1] vdd gnd cell_6t
Xbit_r2_c39 bl[39] br[39] wl[2] vdd gnd cell_6t
Xbit_r3_c39 bl[39] br[39] wl[3] vdd gnd cell_6t
Xbit_r4_c39 bl[39] br[39] wl[4] vdd gnd cell_6t
Xbit_r5_c39 bl[39] br[39] wl[5] vdd gnd cell_6t
Xbit_r6_c39 bl[39] br[39] wl[6] vdd gnd cell_6t
Xbit_r7_c39 bl[39] br[39] wl[7] vdd gnd cell_6t
Xbit_r8_c39 bl[39] br[39] wl[8] vdd gnd cell_6t
Xbit_r9_c39 bl[39] br[39] wl[9] vdd gnd cell_6t
Xbit_r10_c39 bl[39] br[39] wl[10] vdd gnd cell_6t
Xbit_r11_c39 bl[39] br[39] wl[11] vdd gnd cell_6t
Xbit_r12_c39 bl[39] br[39] wl[12] vdd gnd cell_6t
Xbit_r13_c39 bl[39] br[39] wl[13] vdd gnd cell_6t
Xbit_r14_c39 bl[39] br[39] wl[14] vdd gnd cell_6t
Xbit_r15_c39 bl[39] br[39] wl[15] vdd gnd cell_6t
Xbit_r16_c39 bl[39] br[39] wl[16] vdd gnd cell_6t
Xbit_r17_c39 bl[39] br[39] wl[17] vdd gnd cell_6t
Xbit_r18_c39 bl[39] br[39] wl[18] vdd gnd cell_6t
Xbit_r19_c39 bl[39] br[39] wl[19] vdd gnd cell_6t
Xbit_r20_c39 bl[39] br[39] wl[20] vdd gnd cell_6t
Xbit_r21_c39 bl[39] br[39] wl[21] vdd gnd cell_6t
Xbit_r22_c39 bl[39] br[39] wl[22] vdd gnd cell_6t
Xbit_r23_c39 bl[39] br[39] wl[23] vdd gnd cell_6t
Xbit_r24_c39 bl[39] br[39] wl[24] vdd gnd cell_6t
Xbit_r25_c39 bl[39] br[39] wl[25] vdd gnd cell_6t
Xbit_r26_c39 bl[39] br[39] wl[26] vdd gnd cell_6t
Xbit_r27_c39 bl[39] br[39] wl[27] vdd gnd cell_6t
Xbit_r28_c39 bl[39] br[39] wl[28] vdd gnd cell_6t
Xbit_r29_c39 bl[39] br[39] wl[29] vdd gnd cell_6t
Xbit_r30_c39 bl[39] br[39] wl[30] vdd gnd cell_6t
Xbit_r31_c39 bl[39] br[39] wl[31] vdd gnd cell_6t
Xbit_r32_c39 bl[39] br[39] wl[32] vdd gnd cell_6t
Xbit_r33_c39 bl[39] br[39] wl[33] vdd gnd cell_6t
Xbit_r34_c39 bl[39] br[39] wl[34] vdd gnd cell_6t
Xbit_r35_c39 bl[39] br[39] wl[35] vdd gnd cell_6t
Xbit_r36_c39 bl[39] br[39] wl[36] vdd gnd cell_6t
Xbit_r37_c39 bl[39] br[39] wl[37] vdd gnd cell_6t
Xbit_r38_c39 bl[39] br[39] wl[38] vdd gnd cell_6t
Xbit_r39_c39 bl[39] br[39] wl[39] vdd gnd cell_6t
Xbit_r40_c39 bl[39] br[39] wl[40] vdd gnd cell_6t
Xbit_r41_c39 bl[39] br[39] wl[41] vdd gnd cell_6t
Xbit_r42_c39 bl[39] br[39] wl[42] vdd gnd cell_6t
Xbit_r43_c39 bl[39] br[39] wl[43] vdd gnd cell_6t
Xbit_r44_c39 bl[39] br[39] wl[44] vdd gnd cell_6t
Xbit_r45_c39 bl[39] br[39] wl[45] vdd gnd cell_6t
Xbit_r46_c39 bl[39] br[39] wl[46] vdd gnd cell_6t
Xbit_r47_c39 bl[39] br[39] wl[47] vdd gnd cell_6t
Xbit_r48_c39 bl[39] br[39] wl[48] vdd gnd cell_6t
Xbit_r49_c39 bl[39] br[39] wl[49] vdd gnd cell_6t
Xbit_r50_c39 bl[39] br[39] wl[50] vdd gnd cell_6t
Xbit_r51_c39 bl[39] br[39] wl[51] vdd gnd cell_6t
Xbit_r52_c39 bl[39] br[39] wl[52] vdd gnd cell_6t
Xbit_r53_c39 bl[39] br[39] wl[53] vdd gnd cell_6t
Xbit_r54_c39 bl[39] br[39] wl[54] vdd gnd cell_6t
Xbit_r55_c39 bl[39] br[39] wl[55] vdd gnd cell_6t
Xbit_r56_c39 bl[39] br[39] wl[56] vdd gnd cell_6t
Xbit_r57_c39 bl[39] br[39] wl[57] vdd gnd cell_6t
Xbit_r58_c39 bl[39] br[39] wl[58] vdd gnd cell_6t
Xbit_r59_c39 bl[39] br[39] wl[59] vdd gnd cell_6t
Xbit_r60_c39 bl[39] br[39] wl[60] vdd gnd cell_6t
Xbit_r61_c39 bl[39] br[39] wl[61] vdd gnd cell_6t
Xbit_r62_c39 bl[39] br[39] wl[62] vdd gnd cell_6t
Xbit_r63_c39 bl[39] br[39] wl[63] vdd gnd cell_6t
Xbit_r0_c40 bl[40] br[40] wl[0] vdd gnd cell_6t
Xbit_r1_c40 bl[40] br[40] wl[1] vdd gnd cell_6t
Xbit_r2_c40 bl[40] br[40] wl[2] vdd gnd cell_6t
Xbit_r3_c40 bl[40] br[40] wl[3] vdd gnd cell_6t
Xbit_r4_c40 bl[40] br[40] wl[4] vdd gnd cell_6t
Xbit_r5_c40 bl[40] br[40] wl[5] vdd gnd cell_6t
Xbit_r6_c40 bl[40] br[40] wl[6] vdd gnd cell_6t
Xbit_r7_c40 bl[40] br[40] wl[7] vdd gnd cell_6t
Xbit_r8_c40 bl[40] br[40] wl[8] vdd gnd cell_6t
Xbit_r9_c40 bl[40] br[40] wl[9] vdd gnd cell_6t
Xbit_r10_c40 bl[40] br[40] wl[10] vdd gnd cell_6t
Xbit_r11_c40 bl[40] br[40] wl[11] vdd gnd cell_6t
Xbit_r12_c40 bl[40] br[40] wl[12] vdd gnd cell_6t
Xbit_r13_c40 bl[40] br[40] wl[13] vdd gnd cell_6t
Xbit_r14_c40 bl[40] br[40] wl[14] vdd gnd cell_6t
Xbit_r15_c40 bl[40] br[40] wl[15] vdd gnd cell_6t
Xbit_r16_c40 bl[40] br[40] wl[16] vdd gnd cell_6t
Xbit_r17_c40 bl[40] br[40] wl[17] vdd gnd cell_6t
Xbit_r18_c40 bl[40] br[40] wl[18] vdd gnd cell_6t
Xbit_r19_c40 bl[40] br[40] wl[19] vdd gnd cell_6t
Xbit_r20_c40 bl[40] br[40] wl[20] vdd gnd cell_6t
Xbit_r21_c40 bl[40] br[40] wl[21] vdd gnd cell_6t
Xbit_r22_c40 bl[40] br[40] wl[22] vdd gnd cell_6t
Xbit_r23_c40 bl[40] br[40] wl[23] vdd gnd cell_6t
Xbit_r24_c40 bl[40] br[40] wl[24] vdd gnd cell_6t
Xbit_r25_c40 bl[40] br[40] wl[25] vdd gnd cell_6t
Xbit_r26_c40 bl[40] br[40] wl[26] vdd gnd cell_6t
Xbit_r27_c40 bl[40] br[40] wl[27] vdd gnd cell_6t
Xbit_r28_c40 bl[40] br[40] wl[28] vdd gnd cell_6t
Xbit_r29_c40 bl[40] br[40] wl[29] vdd gnd cell_6t
Xbit_r30_c40 bl[40] br[40] wl[30] vdd gnd cell_6t
Xbit_r31_c40 bl[40] br[40] wl[31] vdd gnd cell_6t
Xbit_r32_c40 bl[40] br[40] wl[32] vdd gnd cell_6t
Xbit_r33_c40 bl[40] br[40] wl[33] vdd gnd cell_6t
Xbit_r34_c40 bl[40] br[40] wl[34] vdd gnd cell_6t
Xbit_r35_c40 bl[40] br[40] wl[35] vdd gnd cell_6t
Xbit_r36_c40 bl[40] br[40] wl[36] vdd gnd cell_6t
Xbit_r37_c40 bl[40] br[40] wl[37] vdd gnd cell_6t
Xbit_r38_c40 bl[40] br[40] wl[38] vdd gnd cell_6t
Xbit_r39_c40 bl[40] br[40] wl[39] vdd gnd cell_6t
Xbit_r40_c40 bl[40] br[40] wl[40] vdd gnd cell_6t
Xbit_r41_c40 bl[40] br[40] wl[41] vdd gnd cell_6t
Xbit_r42_c40 bl[40] br[40] wl[42] vdd gnd cell_6t
Xbit_r43_c40 bl[40] br[40] wl[43] vdd gnd cell_6t
Xbit_r44_c40 bl[40] br[40] wl[44] vdd gnd cell_6t
Xbit_r45_c40 bl[40] br[40] wl[45] vdd gnd cell_6t
Xbit_r46_c40 bl[40] br[40] wl[46] vdd gnd cell_6t
Xbit_r47_c40 bl[40] br[40] wl[47] vdd gnd cell_6t
Xbit_r48_c40 bl[40] br[40] wl[48] vdd gnd cell_6t
Xbit_r49_c40 bl[40] br[40] wl[49] vdd gnd cell_6t
Xbit_r50_c40 bl[40] br[40] wl[50] vdd gnd cell_6t
Xbit_r51_c40 bl[40] br[40] wl[51] vdd gnd cell_6t
Xbit_r52_c40 bl[40] br[40] wl[52] vdd gnd cell_6t
Xbit_r53_c40 bl[40] br[40] wl[53] vdd gnd cell_6t
Xbit_r54_c40 bl[40] br[40] wl[54] vdd gnd cell_6t
Xbit_r55_c40 bl[40] br[40] wl[55] vdd gnd cell_6t
Xbit_r56_c40 bl[40] br[40] wl[56] vdd gnd cell_6t
Xbit_r57_c40 bl[40] br[40] wl[57] vdd gnd cell_6t
Xbit_r58_c40 bl[40] br[40] wl[58] vdd gnd cell_6t
Xbit_r59_c40 bl[40] br[40] wl[59] vdd gnd cell_6t
Xbit_r60_c40 bl[40] br[40] wl[60] vdd gnd cell_6t
Xbit_r61_c40 bl[40] br[40] wl[61] vdd gnd cell_6t
Xbit_r62_c40 bl[40] br[40] wl[62] vdd gnd cell_6t
Xbit_r63_c40 bl[40] br[40] wl[63] vdd gnd cell_6t
Xbit_r0_c41 bl[41] br[41] wl[0] vdd gnd cell_6t
Xbit_r1_c41 bl[41] br[41] wl[1] vdd gnd cell_6t
Xbit_r2_c41 bl[41] br[41] wl[2] vdd gnd cell_6t
Xbit_r3_c41 bl[41] br[41] wl[3] vdd gnd cell_6t
Xbit_r4_c41 bl[41] br[41] wl[4] vdd gnd cell_6t
Xbit_r5_c41 bl[41] br[41] wl[5] vdd gnd cell_6t
Xbit_r6_c41 bl[41] br[41] wl[6] vdd gnd cell_6t
Xbit_r7_c41 bl[41] br[41] wl[7] vdd gnd cell_6t
Xbit_r8_c41 bl[41] br[41] wl[8] vdd gnd cell_6t
Xbit_r9_c41 bl[41] br[41] wl[9] vdd gnd cell_6t
Xbit_r10_c41 bl[41] br[41] wl[10] vdd gnd cell_6t
Xbit_r11_c41 bl[41] br[41] wl[11] vdd gnd cell_6t
Xbit_r12_c41 bl[41] br[41] wl[12] vdd gnd cell_6t
Xbit_r13_c41 bl[41] br[41] wl[13] vdd gnd cell_6t
Xbit_r14_c41 bl[41] br[41] wl[14] vdd gnd cell_6t
Xbit_r15_c41 bl[41] br[41] wl[15] vdd gnd cell_6t
Xbit_r16_c41 bl[41] br[41] wl[16] vdd gnd cell_6t
Xbit_r17_c41 bl[41] br[41] wl[17] vdd gnd cell_6t
Xbit_r18_c41 bl[41] br[41] wl[18] vdd gnd cell_6t
Xbit_r19_c41 bl[41] br[41] wl[19] vdd gnd cell_6t
Xbit_r20_c41 bl[41] br[41] wl[20] vdd gnd cell_6t
Xbit_r21_c41 bl[41] br[41] wl[21] vdd gnd cell_6t
Xbit_r22_c41 bl[41] br[41] wl[22] vdd gnd cell_6t
Xbit_r23_c41 bl[41] br[41] wl[23] vdd gnd cell_6t
Xbit_r24_c41 bl[41] br[41] wl[24] vdd gnd cell_6t
Xbit_r25_c41 bl[41] br[41] wl[25] vdd gnd cell_6t
Xbit_r26_c41 bl[41] br[41] wl[26] vdd gnd cell_6t
Xbit_r27_c41 bl[41] br[41] wl[27] vdd gnd cell_6t
Xbit_r28_c41 bl[41] br[41] wl[28] vdd gnd cell_6t
Xbit_r29_c41 bl[41] br[41] wl[29] vdd gnd cell_6t
Xbit_r30_c41 bl[41] br[41] wl[30] vdd gnd cell_6t
Xbit_r31_c41 bl[41] br[41] wl[31] vdd gnd cell_6t
Xbit_r32_c41 bl[41] br[41] wl[32] vdd gnd cell_6t
Xbit_r33_c41 bl[41] br[41] wl[33] vdd gnd cell_6t
Xbit_r34_c41 bl[41] br[41] wl[34] vdd gnd cell_6t
Xbit_r35_c41 bl[41] br[41] wl[35] vdd gnd cell_6t
Xbit_r36_c41 bl[41] br[41] wl[36] vdd gnd cell_6t
Xbit_r37_c41 bl[41] br[41] wl[37] vdd gnd cell_6t
Xbit_r38_c41 bl[41] br[41] wl[38] vdd gnd cell_6t
Xbit_r39_c41 bl[41] br[41] wl[39] vdd gnd cell_6t
Xbit_r40_c41 bl[41] br[41] wl[40] vdd gnd cell_6t
Xbit_r41_c41 bl[41] br[41] wl[41] vdd gnd cell_6t
Xbit_r42_c41 bl[41] br[41] wl[42] vdd gnd cell_6t
Xbit_r43_c41 bl[41] br[41] wl[43] vdd gnd cell_6t
Xbit_r44_c41 bl[41] br[41] wl[44] vdd gnd cell_6t
Xbit_r45_c41 bl[41] br[41] wl[45] vdd gnd cell_6t
Xbit_r46_c41 bl[41] br[41] wl[46] vdd gnd cell_6t
Xbit_r47_c41 bl[41] br[41] wl[47] vdd gnd cell_6t
Xbit_r48_c41 bl[41] br[41] wl[48] vdd gnd cell_6t
Xbit_r49_c41 bl[41] br[41] wl[49] vdd gnd cell_6t
Xbit_r50_c41 bl[41] br[41] wl[50] vdd gnd cell_6t
Xbit_r51_c41 bl[41] br[41] wl[51] vdd gnd cell_6t
Xbit_r52_c41 bl[41] br[41] wl[52] vdd gnd cell_6t
Xbit_r53_c41 bl[41] br[41] wl[53] vdd gnd cell_6t
Xbit_r54_c41 bl[41] br[41] wl[54] vdd gnd cell_6t
Xbit_r55_c41 bl[41] br[41] wl[55] vdd gnd cell_6t
Xbit_r56_c41 bl[41] br[41] wl[56] vdd gnd cell_6t
Xbit_r57_c41 bl[41] br[41] wl[57] vdd gnd cell_6t
Xbit_r58_c41 bl[41] br[41] wl[58] vdd gnd cell_6t
Xbit_r59_c41 bl[41] br[41] wl[59] vdd gnd cell_6t
Xbit_r60_c41 bl[41] br[41] wl[60] vdd gnd cell_6t
Xbit_r61_c41 bl[41] br[41] wl[61] vdd gnd cell_6t
Xbit_r62_c41 bl[41] br[41] wl[62] vdd gnd cell_6t
Xbit_r63_c41 bl[41] br[41] wl[63] vdd gnd cell_6t
Xbit_r0_c42 bl[42] br[42] wl[0] vdd gnd cell_6t
Xbit_r1_c42 bl[42] br[42] wl[1] vdd gnd cell_6t
Xbit_r2_c42 bl[42] br[42] wl[2] vdd gnd cell_6t
Xbit_r3_c42 bl[42] br[42] wl[3] vdd gnd cell_6t
Xbit_r4_c42 bl[42] br[42] wl[4] vdd gnd cell_6t
Xbit_r5_c42 bl[42] br[42] wl[5] vdd gnd cell_6t
Xbit_r6_c42 bl[42] br[42] wl[6] vdd gnd cell_6t
Xbit_r7_c42 bl[42] br[42] wl[7] vdd gnd cell_6t
Xbit_r8_c42 bl[42] br[42] wl[8] vdd gnd cell_6t
Xbit_r9_c42 bl[42] br[42] wl[9] vdd gnd cell_6t
Xbit_r10_c42 bl[42] br[42] wl[10] vdd gnd cell_6t
Xbit_r11_c42 bl[42] br[42] wl[11] vdd gnd cell_6t
Xbit_r12_c42 bl[42] br[42] wl[12] vdd gnd cell_6t
Xbit_r13_c42 bl[42] br[42] wl[13] vdd gnd cell_6t
Xbit_r14_c42 bl[42] br[42] wl[14] vdd gnd cell_6t
Xbit_r15_c42 bl[42] br[42] wl[15] vdd gnd cell_6t
Xbit_r16_c42 bl[42] br[42] wl[16] vdd gnd cell_6t
Xbit_r17_c42 bl[42] br[42] wl[17] vdd gnd cell_6t
Xbit_r18_c42 bl[42] br[42] wl[18] vdd gnd cell_6t
Xbit_r19_c42 bl[42] br[42] wl[19] vdd gnd cell_6t
Xbit_r20_c42 bl[42] br[42] wl[20] vdd gnd cell_6t
Xbit_r21_c42 bl[42] br[42] wl[21] vdd gnd cell_6t
Xbit_r22_c42 bl[42] br[42] wl[22] vdd gnd cell_6t
Xbit_r23_c42 bl[42] br[42] wl[23] vdd gnd cell_6t
Xbit_r24_c42 bl[42] br[42] wl[24] vdd gnd cell_6t
Xbit_r25_c42 bl[42] br[42] wl[25] vdd gnd cell_6t
Xbit_r26_c42 bl[42] br[42] wl[26] vdd gnd cell_6t
Xbit_r27_c42 bl[42] br[42] wl[27] vdd gnd cell_6t
Xbit_r28_c42 bl[42] br[42] wl[28] vdd gnd cell_6t
Xbit_r29_c42 bl[42] br[42] wl[29] vdd gnd cell_6t
Xbit_r30_c42 bl[42] br[42] wl[30] vdd gnd cell_6t
Xbit_r31_c42 bl[42] br[42] wl[31] vdd gnd cell_6t
Xbit_r32_c42 bl[42] br[42] wl[32] vdd gnd cell_6t
Xbit_r33_c42 bl[42] br[42] wl[33] vdd gnd cell_6t
Xbit_r34_c42 bl[42] br[42] wl[34] vdd gnd cell_6t
Xbit_r35_c42 bl[42] br[42] wl[35] vdd gnd cell_6t
Xbit_r36_c42 bl[42] br[42] wl[36] vdd gnd cell_6t
Xbit_r37_c42 bl[42] br[42] wl[37] vdd gnd cell_6t
Xbit_r38_c42 bl[42] br[42] wl[38] vdd gnd cell_6t
Xbit_r39_c42 bl[42] br[42] wl[39] vdd gnd cell_6t
Xbit_r40_c42 bl[42] br[42] wl[40] vdd gnd cell_6t
Xbit_r41_c42 bl[42] br[42] wl[41] vdd gnd cell_6t
Xbit_r42_c42 bl[42] br[42] wl[42] vdd gnd cell_6t
Xbit_r43_c42 bl[42] br[42] wl[43] vdd gnd cell_6t
Xbit_r44_c42 bl[42] br[42] wl[44] vdd gnd cell_6t
Xbit_r45_c42 bl[42] br[42] wl[45] vdd gnd cell_6t
Xbit_r46_c42 bl[42] br[42] wl[46] vdd gnd cell_6t
Xbit_r47_c42 bl[42] br[42] wl[47] vdd gnd cell_6t
Xbit_r48_c42 bl[42] br[42] wl[48] vdd gnd cell_6t
Xbit_r49_c42 bl[42] br[42] wl[49] vdd gnd cell_6t
Xbit_r50_c42 bl[42] br[42] wl[50] vdd gnd cell_6t
Xbit_r51_c42 bl[42] br[42] wl[51] vdd gnd cell_6t
Xbit_r52_c42 bl[42] br[42] wl[52] vdd gnd cell_6t
Xbit_r53_c42 bl[42] br[42] wl[53] vdd gnd cell_6t
Xbit_r54_c42 bl[42] br[42] wl[54] vdd gnd cell_6t
Xbit_r55_c42 bl[42] br[42] wl[55] vdd gnd cell_6t
Xbit_r56_c42 bl[42] br[42] wl[56] vdd gnd cell_6t
Xbit_r57_c42 bl[42] br[42] wl[57] vdd gnd cell_6t
Xbit_r58_c42 bl[42] br[42] wl[58] vdd gnd cell_6t
Xbit_r59_c42 bl[42] br[42] wl[59] vdd gnd cell_6t
Xbit_r60_c42 bl[42] br[42] wl[60] vdd gnd cell_6t
Xbit_r61_c42 bl[42] br[42] wl[61] vdd gnd cell_6t
Xbit_r62_c42 bl[42] br[42] wl[62] vdd gnd cell_6t
Xbit_r63_c42 bl[42] br[42] wl[63] vdd gnd cell_6t
Xbit_r0_c43 bl[43] br[43] wl[0] vdd gnd cell_6t
Xbit_r1_c43 bl[43] br[43] wl[1] vdd gnd cell_6t
Xbit_r2_c43 bl[43] br[43] wl[2] vdd gnd cell_6t
Xbit_r3_c43 bl[43] br[43] wl[3] vdd gnd cell_6t
Xbit_r4_c43 bl[43] br[43] wl[4] vdd gnd cell_6t
Xbit_r5_c43 bl[43] br[43] wl[5] vdd gnd cell_6t
Xbit_r6_c43 bl[43] br[43] wl[6] vdd gnd cell_6t
Xbit_r7_c43 bl[43] br[43] wl[7] vdd gnd cell_6t
Xbit_r8_c43 bl[43] br[43] wl[8] vdd gnd cell_6t
Xbit_r9_c43 bl[43] br[43] wl[9] vdd gnd cell_6t
Xbit_r10_c43 bl[43] br[43] wl[10] vdd gnd cell_6t
Xbit_r11_c43 bl[43] br[43] wl[11] vdd gnd cell_6t
Xbit_r12_c43 bl[43] br[43] wl[12] vdd gnd cell_6t
Xbit_r13_c43 bl[43] br[43] wl[13] vdd gnd cell_6t
Xbit_r14_c43 bl[43] br[43] wl[14] vdd gnd cell_6t
Xbit_r15_c43 bl[43] br[43] wl[15] vdd gnd cell_6t
Xbit_r16_c43 bl[43] br[43] wl[16] vdd gnd cell_6t
Xbit_r17_c43 bl[43] br[43] wl[17] vdd gnd cell_6t
Xbit_r18_c43 bl[43] br[43] wl[18] vdd gnd cell_6t
Xbit_r19_c43 bl[43] br[43] wl[19] vdd gnd cell_6t
Xbit_r20_c43 bl[43] br[43] wl[20] vdd gnd cell_6t
Xbit_r21_c43 bl[43] br[43] wl[21] vdd gnd cell_6t
Xbit_r22_c43 bl[43] br[43] wl[22] vdd gnd cell_6t
Xbit_r23_c43 bl[43] br[43] wl[23] vdd gnd cell_6t
Xbit_r24_c43 bl[43] br[43] wl[24] vdd gnd cell_6t
Xbit_r25_c43 bl[43] br[43] wl[25] vdd gnd cell_6t
Xbit_r26_c43 bl[43] br[43] wl[26] vdd gnd cell_6t
Xbit_r27_c43 bl[43] br[43] wl[27] vdd gnd cell_6t
Xbit_r28_c43 bl[43] br[43] wl[28] vdd gnd cell_6t
Xbit_r29_c43 bl[43] br[43] wl[29] vdd gnd cell_6t
Xbit_r30_c43 bl[43] br[43] wl[30] vdd gnd cell_6t
Xbit_r31_c43 bl[43] br[43] wl[31] vdd gnd cell_6t
Xbit_r32_c43 bl[43] br[43] wl[32] vdd gnd cell_6t
Xbit_r33_c43 bl[43] br[43] wl[33] vdd gnd cell_6t
Xbit_r34_c43 bl[43] br[43] wl[34] vdd gnd cell_6t
Xbit_r35_c43 bl[43] br[43] wl[35] vdd gnd cell_6t
Xbit_r36_c43 bl[43] br[43] wl[36] vdd gnd cell_6t
Xbit_r37_c43 bl[43] br[43] wl[37] vdd gnd cell_6t
Xbit_r38_c43 bl[43] br[43] wl[38] vdd gnd cell_6t
Xbit_r39_c43 bl[43] br[43] wl[39] vdd gnd cell_6t
Xbit_r40_c43 bl[43] br[43] wl[40] vdd gnd cell_6t
Xbit_r41_c43 bl[43] br[43] wl[41] vdd gnd cell_6t
Xbit_r42_c43 bl[43] br[43] wl[42] vdd gnd cell_6t
Xbit_r43_c43 bl[43] br[43] wl[43] vdd gnd cell_6t
Xbit_r44_c43 bl[43] br[43] wl[44] vdd gnd cell_6t
Xbit_r45_c43 bl[43] br[43] wl[45] vdd gnd cell_6t
Xbit_r46_c43 bl[43] br[43] wl[46] vdd gnd cell_6t
Xbit_r47_c43 bl[43] br[43] wl[47] vdd gnd cell_6t
Xbit_r48_c43 bl[43] br[43] wl[48] vdd gnd cell_6t
Xbit_r49_c43 bl[43] br[43] wl[49] vdd gnd cell_6t
Xbit_r50_c43 bl[43] br[43] wl[50] vdd gnd cell_6t
Xbit_r51_c43 bl[43] br[43] wl[51] vdd gnd cell_6t
Xbit_r52_c43 bl[43] br[43] wl[52] vdd gnd cell_6t
Xbit_r53_c43 bl[43] br[43] wl[53] vdd gnd cell_6t
Xbit_r54_c43 bl[43] br[43] wl[54] vdd gnd cell_6t
Xbit_r55_c43 bl[43] br[43] wl[55] vdd gnd cell_6t
Xbit_r56_c43 bl[43] br[43] wl[56] vdd gnd cell_6t
Xbit_r57_c43 bl[43] br[43] wl[57] vdd gnd cell_6t
Xbit_r58_c43 bl[43] br[43] wl[58] vdd gnd cell_6t
Xbit_r59_c43 bl[43] br[43] wl[59] vdd gnd cell_6t
Xbit_r60_c43 bl[43] br[43] wl[60] vdd gnd cell_6t
Xbit_r61_c43 bl[43] br[43] wl[61] vdd gnd cell_6t
Xbit_r62_c43 bl[43] br[43] wl[62] vdd gnd cell_6t
Xbit_r63_c43 bl[43] br[43] wl[63] vdd gnd cell_6t
Xbit_r0_c44 bl[44] br[44] wl[0] vdd gnd cell_6t
Xbit_r1_c44 bl[44] br[44] wl[1] vdd gnd cell_6t
Xbit_r2_c44 bl[44] br[44] wl[2] vdd gnd cell_6t
Xbit_r3_c44 bl[44] br[44] wl[3] vdd gnd cell_6t
Xbit_r4_c44 bl[44] br[44] wl[4] vdd gnd cell_6t
Xbit_r5_c44 bl[44] br[44] wl[5] vdd gnd cell_6t
Xbit_r6_c44 bl[44] br[44] wl[6] vdd gnd cell_6t
Xbit_r7_c44 bl[44] br[44] wl[7] vdd gnd cell_6t
Xbit_r8_c44 bl[44] br[44] wl[8] vdd gnd cell_6t
Xbit_r9_c44 bl[44] br[44] wl[9] vdd gnd cell_6t
Xbit_r10_c44 bl[44] br[44] wl[10] vdd gnd cell_6t
Xbit_r11_c44 bl[44] br[44] wl[11] vdd gnd cell_6t
Xbit_r12_c44 bl[44] br[44] wl[12] vdd gnd cell_6t
Xbit_r13_c44 bl[44] br[44] wl[13] vdd gnd cell_6t
Xbit_r14_c44 bl[44] br[44] wl[14] vdd gnd cell_6t
Xbit_r15_c44 bl[44] br[44] wl[15] vdd gnd cell_6t
Xbit_r16_c44 bl[44] br[44] wl[16] vdd gnd cell_6t
Xbit_r17_c44 bl[44] br[44] wl[17] vdd gnd cell_6t
Xbit_r18_c44 bl[44] br[44] wl[18] vdd gnd cell_6t
Xbit_r19_c44 bl[44] br[44] wl[19] vdd gnd cell_6t
Xbit_r20_c44 bl[44] br[44] wl[20] vdd gnd cell_6t
Xbit_r21_c44 bl[44] br[44] wl[21] vdd gnd cell_6t
Xbit_r22_c44 bl[44] br[44] wl[22] vdd gnd cell_6t
Xbit_r23_c44 bl[44] br[44] wl[23] vdd gnd cell_6t
Xbit_r24_c44 bl[44] br[44] wl[24] vdd gnd cell_6t
Xbit_r25_c44 bl[44] br[44] wl[25] vdd gnd cell_6t
Xbit_r26_c44 bl[44] br[44] wl[26] vdd gnd cell_6t
Xbit_r27_c44 bl[44] br[44] wl[27] vdd gnd cell_6t
Xbit_r28_c44 bl[44] br[44] wl[28] vdd gnd cell_6t
Xbit_r29_c44 bl[44] br[44] wl[29] vdd gnd cell_6t
Xbit_r30_c44 bl[44] br[44] wl[30] vdd gnd cell_6t
Xbit_r31_c44 bl[44] br[44] wl[31] vdd gnd cell_6t
Xbit_r32_c44 bl[44] br[44] wl[32] vdd gnd cell_6t
Xbit_r33_c44 bl[44] br[44] wl[33] vdd gnd cell_6t
Xbit_r34_c44 bl[44] br[44] wl[34] vdd gnd cell_6t
Xbit_r35_c44 bl[44] br[44] wl[35] vdd gnd cell_6t
Xbit_r36_c44 bl[44] br[44] wl[36] vdd gnd cell_6t
Xbit_r37_c44 bl[44] br[44] wl[37] vdd gnd cell_6t
Xbit_r38_c44 bl[44] br[44] wl[38] vdd gnd cell_6t
Xbit_r39_c44 bl[44] br[44] wl[39] vdd gnd cell_6t
Xbit_r40_c44 bl[44] br[44] wl[40] vdd gnd cell_6t
Xbit_r41_c44 bl[44] br[44] wl[41] vdd gnd cell_6t
Xbit_r42_c44 bl[44] br[44] wl[42] vdd gnd cell_6t
Xbit_r43_c44 bl[44] br[44] wl[43] vdd gnd cell_6t
Xbit_r44_c44 bl[44] br[44] wl[44] vdd gnd cell_6t
Xbit_r45_c44 bl[44] br[44] wl[45] vdd gnd cell_6t
Xbit_r46_c44 bl[44] br[44] wl[46] vdd gnd cell_6t
Xbit_r47_c44 bl[44] br[44] wl[47] vdd gnd cell_6t
Xbit_r48_c44 bl[44] br[44] wl[48] vdd gnd cell_6t
Xbit_r49_c44 bl[44] br[44] wl[49] vdd gnd cell_6t
Xbit_r50_c44 bl[44] br[44] wl[50] vdd gnd cell_6t
Xbit_r51_c44 bl[44] br[44] wl[51] vdd gnd cell_6t
Xbit_r52_c44 bl[44] br[44] wl[52] vdd gnd cell_6t
Xbit_r53_c44 bl[44] br[44] wl[53] vdd gnd cell_6t
Xbit_r54_c44 bl[44] br[44] wl[54] vdd gnd cell_6t
Xbit_r55_c44 bl[44] br[44] wl[55] vdd gnd cell_6t
Xbit_r56_c44 bl[44] br[44] wl[56] vdd gnd cell_6t
Xbit_r57_c44 bl[44] br[44] wl[57] vdd gnd cell_6t
Xbit_r58_c44 bl[44] br[44] wl[58] vdd gnd cell_6t
Xbit_r59_c44 bl[44] br[44] wl[59] vdd gnd cell_6t
Xbit_r60_c44 bl[44] br[44] wl[60] vdd gnd cell_6t
Xbit_r61_c44 bl[44] br[44] wl[61] vdd gnd cell_6t
Xbit_r62_c44 bl[44] br[44] wl[62] vdd gnd cell_6t
Xbit_r63_c44 bl[44] br[44] wl[63] vdd gnd cell_6t
Xbit_r0_c45 bl[45] br[45] wl[0] vdd gnd cell_6t
Xbit_r1_c45 bl[45] br[45] wl[1] vdd gnd cell_6t
Xbit_r2_c45 bl[45] br[45] wl[2] vdd gnd cell_6t
Xbit_r3_c45 bl[45] br[45] wl[3] vdd gnd cell_6t
Xbit_r4_c45 bl[45] br[45] wl[4] vdd gnd cell_6t
Xbit_r5_c45 bl[45] br[45] wl[5] vdd gnd cell_6t
Xbit_r6_c45 bl[45] br[45] wl[6] vdd gnd cell_6t
Xbit_r7_c45 bl[45] br[45] wl[7] vdd gnd cell_6t
Xbit_r8_c45 bl[45] br[45] wl[8] vdd gnd cell_6t
Xbit_r9_c45 bl[45] br[45] wl[9] vdd gnd cell_6t
Xbit_r10_c45 bl[45] br[45] wl[10] vdd gnd cell_6t
Xbit_r11_c45 bl[45] br[45] wl[11] vdd gnd cell_6t
Xbit_r12_c45 bl[45] br[45] wl[12] vdd gnd cell_6t
Xbit_r13_c45 bl[45] br[45] wl[13] vdd gnd cell_6t
Xbit_r14_c45 bl[45] br[45] wl[14] vdd gnd cell_6t
Xbit_r15_c45 bl[45] br[45] wl[15] vdd gnd cell_6t
Xbit_r16_c45 bl[45] br[45] wl[16] vdd gnd cell_6t
Xbit_r17_c45 bl[45] br[45] wl[17] vdd gnd cell_6t
Xbit_r18_c45 bl[45] br[45] wl[18] vdd gnd cell_6t
Xbit_r19_c45 bl[45] br[45] wl[19] vdd gnd cell_6t
Xbit_r20_c45 bl[45] br[45] wl[20] vdd gnd cell_6t
Xbit_r21_c45 bl[45] br[45] wl[21] vdd gnd cell_6t
Xbit_r22_c45 bl[45] br[45] wl[22] vdd gnd cell_6t
Xbit_r23_c45 bl[45] br[45] wl[23] vdd gnd cell_6t
Xbit_r24_c45 bl[45] br[45] wl[24] vdd gnd cell_6t
Xbit_r25_c45 bl[45] br[45] wl[25] vdd gnd cell_6t
Xbit_r26_c45 bl[45] br[45] wl[26] vdd gnd cell_6t
Xbit_r27_c45 bl[45] br[45] wl[27] vdd gnd cell_6t
Xbit_r28_c45 bl[45] br[45] wl[28] vdd gnd cell_6t
Xbit_r29_c45 bl[45] br[45] wl[29] vdd gnd cell_6t
Xbit_r30_c45 bl[45] br[45] wl[30] vdd gnd cell_6t
Xbit_r31_c45 bl[45] br[45] wl[31] vdd gnd cell_6t
Xbit_r32_c45 bl[45] br[45] wl[32] vdd gnd cell_6t
Xbit_r33_c45 bl[45] br[45] wl[33] vdd gnd cell_6t
Xbit_r34_c45 bl[45] br[45] wl[34] vdd gnd cell_6t
Xbit_r35_c45 bl[45] br[45] wl[35] vdd gnd cell_6t
Xbit_r36_c45 bl[45] br[45] wl[36] vdd gnd cell_6t
Xbit_r37_c45 bl[45] br[45] wl[37] vdd gnd cell_6t
Xbit_r38_c45 bl[45] br[45] wl[38] vdd gnd cell_6t
Xbit_r39_c45 bl[45] br[45] wl[39] vdd gnd cell_6t
Xbit_r40_c45 bl[45] br[45] wl[40] vdd gnd cell_6t
Xbit_r41_c45 bl[45] br[45] wl[41] vdd gnd cell_6t
Xbit_r42_c45 bl[45] br[45] wl[42] vdd gnd cell_6t
Xbit_r43_c45 bl[45] br[45] wl[43] vdd gnd cell_6t
Xbit_r44_c45 bl[45] br[45] wl[44] vdd gnd cell_6t
Xbit_r45_c45 bl[45] br[45] wl[45] vdd gnd cell_6t
Xbit_r46_c45 bl[45] br[45] wl[46] vdd gnd cell_6t
Xbit_r47_c45 bl[45] br[45] wl[47] vdd gnd cell_6t
Xbit_r48_c45 bl[45] br[45] wl[48] vdd gnd cell_6t
Xbit_r49_c45 bl[45] br[45] wl[49] vdd gnd cell_6t
Xbit_r50_c45 bl[45] br[45] wl[50] vdd gnd cell_6t
Xbit_r51_c45 bl[45] br[45] wl[51] vdd gnd cell_6t
Xbit_r52_c45 bl[45] br[45] wl[52] vdd gnd cell_6t
Xbit_r53_c45 bl[45] br[45] wl[53] vdd gnd cell_6t
Xbit_r54_c45 bl[45] br[45] wl[54] vdd gnd cell_6t
Xbit_r55_c45 bl[45] br[45] wl[55] vdd gnd cell_6t
Xbit_r56_c45 bl[45] br[45] wl[56] vdd gnd cell_6t
Xbit_r57_c45 bl[45] br[45] wl[57] vdd gnd cell_6t
Xbit_r58_c45 bl[45] br[45] wl[58] vdd gnd cell_6t
Xbit_r59_c45 bl[45] br[45] wl[59] vdd gnd cell_6t
Xbit_r60_c45 bl[45] br[45] wl[60] vdd gnd cell_6t
Xbit_r61_c45 bl[45] br[45] wl[61] vdd gnd cell_6t
Xbit_r62_c45 bl[45] br[45] wl[62] vdd gnd cell_6t
Xbit_r63_c45 bl[45] br[45] wl[63] vdd gnd cell_6t
Xbit_r0_c46 bl[46] br[46] wl[0] vdd gnd cell_6t
Xbit_r1_c46 bl[46] br[46] wl[1] vdd gnd cell_6t
Xbit_r2_c46 bl[46] br[46] wl[2] vdd gnd cell_6t
Xbit_r3_c46 bl[46] br[46] wl[3] vdd gnd cell_6t
Xbit_r4_c46 bl[46] br[46] wl[4] vdd gnd cell_6t
Xbit_r5_c46 bl[46] br[46] wl[5] vdd gnd cell_6t
Xbit_r6_c46 bl[46] br[46] wl[6] vdd gnd cell_6t
Xbit_r7_c46 bl[46] br[46] wl[7] vdd gnd cell_6t
Xbit_r8_c46 bl[46] br[46] wl[8] vdd gnd cell_6t
Xbit_r9_c46 bl[46] br[46] wl[9] vdd gnd cell_6t
Xbit_r10_c46 bl[46] br[46] wl[10] vdd gnd cell_6t
Xbit_r11_c46 bl[46] br[46] wl[11] vdd gnd cell_6t
Xbit_r12_c46 bl[46] br[46] wl[12] vdd gnd cell_6t
Xbit_r13_c46 bl[46] br[46] wl[13] vdd gnd cell_6t
Xbit_r14_c46 bl[46] br[46] wl[14] vdd gnd cell_6t
Xbit_r15_c46 bl[46] br[46] wl[15] vdd gnd cell_6t
Xbit_r16_c46 bl[46] br[46] wl[16] vdd gnd cell_6t
Xbit_r17_c46 bl[46] br[46] wl[17] vdd gnd cell_6t
Xbit_r18_c46 bl[46] br[46] wl[18] vdd gnd cell_6t
Xbit_r19_c46 bl[46] br[46] wl[19] vdd gnd cell_6t
Xbit_r20_c46 bl[46] br[46] wl[20] vdd gnd cell_6t
Xbit_r21_c46 bl[46] br[46] wl[21] vdd gnd cell_6t
Xbit_r22_c46 bl[46] br[46] wl[22] vdd gnd cell_6t
Xbit_r23_c46 bl[46] br[46] wl[23] vdd gnd cell_6t
Xbit_r24_c46 bl[46] br[46] wl[24] vdd gnd cell_6t
Xbit_r25_c46 bl[46] br[46] wl[25] vdd gnd cell_6t
Xbit_r26_c46 bl[46] br[46] wl[26] vdd gnd cell_6t
Xbit_r27_c46 bl[46] br[46] wl[27] vdd gnd cell_6t
Xbit_r28_c46 bl[46] br[46] wl[28] vdd gnd cell_6t
Xbit_r29_c46 bl[46] br[46] wl[29] vdd gnd cell_6t
Xbit_r30_c46 bl[46] br[46] wl[30] vdd gnd cell_6t
Xbit_r31_c46 bl[46] br[46] wl[31] vdd gnd cell_6t
Xbit_r32_c46 bl[46] br[46] wl[32] vdd gnd cell_6t
Xbit_r33_c46 bl[46] br[46] wl[33] vdd gnd cell_6t
Xbit_r34_c46 bl[46] br[46] wl[34] vdd gnd cell_6t
Xbit_r35_c46 bl[46] br[46] wl[35] vdd gnd cell_6t
Xbit_r36_c46 bl[46] br[46] wl[36] vdd gnd cell_6t
Xbit_r37_c46 bl[46] br[46] wl[37] vdd gnd cell_6t
Xbit_r38_c46 bl[46] br[46] wl[38] vdd gnd cell_6t
Xbit_r39_c46 bl[46] br[46] wl[39] vdd gnd cell_6t
Xbit_r40_c46 bl[46] br[46] wl[40] vdd gnd cell_6t
Xbit_r41_c46 bl[46] br[46] wl[41] vdd gnd cell_6t
Xbit_r42_c46 bl[46] br[46] wl[42] vdd gnd cell_6t
Xbit_r43_c46 bl[46] br[46] wl[43] vdd gnd cell_6t
Xbit_r44_c46 bl[46] br[46] wl[44] vdd gnd cell_6t
Xbit_r45_c46 bl[46] br[46] wl[45] vdd gnd cell_6t
Xbit_r46_c46 bl[46] br[46] wl[46] vdd gnd cell_6t
Xbit_r47_c46 bl[46] br[46] wl[47] vdd gnd cell_6t
Xbit_r48_c46 bl[46] br[46] wl[48] vdd gnd cell_6t
Xbit_r49_c46 bl[46] br[46] wl[49] vdd gnd cell_6t
Xbit_r50_c46 bl[46] br[46] wl[50] vdd gnd cell_6t
Xbit_r51_c46 bl[46] br[46] wl[51] vdd gnd cell_6t
Xbit_r52_c46 bl[46] br[46] wl[52] vdd gnd cell_6t
Xbit_r53_c46 bl[46] br[46] wl[53] vdd gnd cell_6t
Xbit_r54_c46 bl[46] br[46] wl[54] vdd gnd cell_6t
Xbit_r55_c46 bl[46] br[46] wl[55] vdd gnd cell_6t
Xbit_r56_c46 bl[46] br[46] wl[56] vdd gnd cell_6t
Xbit_r57_c46 bl[46] br[46] wl[57] vdd gnd cell_6t
Xbit_r58_c46 bl[46] br[46] wl[58] vdd gnd cell_6t
Xbit_r59_c46 bl[46] br[46] wl[59] vdd gnd cell_6t
Xbit_r60_c46 bl[46] br[46] wl[60] vdd gnd cell_6t
Xbit_r61_c46 bl[46] br[46] wl[61] vdd gnd cell_6t
Xbit_r62_c46 bl[46] br[46] wl[62] vdd gnd cell_6t
Xbit_r63_c46 bl[46] br[46] wl[63] vdd gnd cell_6t
Xbit_r0_c47 bl[47] br[47] wl[0] vdd gnd cell_6t
Xbit_r1_c47 bl[47] br[47] wl[1] vdd gnd cell_6t
Xbit_r2_c47 bl[47] br[47] wl[2] vdd gnd cell_6t
Xbit_r3_c47 bl[47] br[47] wl[3] vdd gnd cell_6t
Xbit_r4_c47 bl[47] br[47] wl[4] vdd gnd cell_6t
Xbit_r5_c47 bl[47] br[47] wl[5] vdd gnd cell_6t
Xbit_r6_c47 bl[47] br[47] wl[6] vdd gnd cell_6t
Xbit_r7_c47 bl[47] br[47] wl[7] vdd gnd cell_6t
Xbit_r8_c47 bl[47] br[47] wl[8] vdd gnd cell_6t
Xbit_r9_c47 bl[47] br[47] wl[9] vdd gnd cell_6t
Xbit_r10_c47 bl[47] br[47] wl[10] vdd gnd cell_6t
Xbit_r11_c47 bl[47] br[47] wl[11] vdd gnd cell_6t
Xbit_r12_c47 bl[47] br[47] wl[12] vdd gnd cell_6t
Xbit_r13_c47 bl[47] br[47] wl[13] vdd gnd cell_6t
Xbit_r14_c47 bl[47] br[47] wl[14] vdd gnd cell_6t
Xbit_r15_c47 bl[47] br[47] wl[15] vdd gnd cell_6t
Xbit_r16_c47 bl[47] br[47] wl[16] vdd gnd cell_6t
Xbit_r17_c47 bl[47] br[47] wl[17] vdd gnd cell_6t
Xbit_r18_c47 bl[47] br[47] wl[18] vdd gnd cell_6t
Xbit_r19_c47 bl[47] br[47] wl[19] vdd gnd cell_6t
Xbit_r20_c47 bl[47] br[47] wl[20] vdd gnd cell_6t
Xbit_r21_c47 bl[47] br[47] wl[21] vdd gnd cell_6t
Xbit_r22_c47 bl[47] br[47] wl[22] vdd gnd cell_6t
Xbit_r23_c47 bl[47] br[47] wl[23] vdd gnd cell_6t
Xbit_r24_c47 bl[47] br[47] wl[24] vdd gnd cell_6t
Xbit_r25_c47 bl[47] br[47] wl[25] vdd gnd cell_6t
Xbit_r26_c47 bl[47] br[47] wl[26] vdd gnd cell_6t
Xbit_r27_c47 bl[47] br[47] wl[27] vdd gnd cell_6t
Xbit_r28_c47 bl[47] br[47] wl[28] vdd gnd cell_6t
Xbit_r29_c47 bl[47] br[47] wl[29] vdd gnd cell_6t
Xbit_r30_c47 bl[47] br[47] wl[30] vdd gnd cell_6t
Xbit_r31_c47 bl[47] br[47] wl[31] vdd gnd cell_6t
Xbit_r32_c47 bl[47] br[47] wl[32] vdd gnd cell_6t
Xbit_r33_c47 bl[47] br[47] wl[33] vdd gnd cell_6t
Xbit_r34_c47 bl[47] br[47] wl[34] vdd gnd cell_6t
Xbit_r35_c47 bl[47] br[47] wl[35] vdd gnd cell_6t
Xbit_r36_c47 bl[47] br[47] wl[36] vdd gnd cell_6t
Xbit_r37_c47 bl[47] br[47] wl[37] vdd gnd cell_6t
Xbit_r38_c47 bl[47] br[47] wl[38] vdd gnd cell_6t
Xbit_r39_c47 bl[47] br[47] wl[39] vdd gnd cell_6t
Xbit_r40_c47 bl[47] br[47] wl[40] vdd gnd cell_6t
Xbit_r41_c47 bl[47] br[47] wl[41] vdd gnd cell_6t
Xbit_r42_c47 bl[47] br[47] wl[42] vdd gnd cell_6t
Xbit_r43_c47 bl[47] br[47] wl[43] vdd gnd cell_6t
Xbit_r44_c47 bl[47] br[47] wl[44] vdd gnd cell_6t
Xbit_r45_c47 bl[47] br[47] wl[45] vdd gnd cell_6t
Xbit_r46_c47 bl[47] br[47] wl[46] vdd gnd cell_6t
Xbit_r47_c47 bl[47] br[47] wl[47] vdd gnd cell_6t
Xbit_r48_c47 bl[47] br[47] wl[48] vdd gnd cell_6t
Xbit_r49_c47 bl[47] br[47] wl[49] vdd gnd cell_6t
Xbit_r50_c47 bl[47] br[47] wl[50] vdd gnd cell_6t
Xbit_r51_c47 bl[47] br[47] wl[51] vdd gnd cell_6t
Xbit_r52_c47 bl[47] br[47] wl[52] vdd gnd cell_6t
Xbit_r53_c47 bl[47] br[47] wl[53] vdd gnd cell_6t
Xbit_r54_c47 bl[47] br[47] wl[54] vdd gnd cell_6t
Xbit_r55_c47 bl[47] br[47] wl[55] vdd gnd cell_6t
Xbit_r56_c47 bl[47] br[47] wl[56] vdd gnd cell_6t
Xbit_r57_c47 bl[47] br[47] wl[57] vdd gnd cell_6t
Xbit_r58_c47 bl[47] br[47] wl[58] vdd gnd cell_6t
Xbit_r59_c47 bl[47] br[47] wl[59] vdd gnd cell_6t
Xbit_r60_c47 bl[47] br[47] wl[60] vdd gnd cell_6t
Xbit_r61_c47 bl[47] br[47] wl[61] vdd gnd cell_6t
Xbit_r62_c47 bl[47] br[47] wl[62] vdd gnd cell_6t
Xbit_r63_c47 bl[47] br[47] wl[63] vdd gnd cell_6t
Xbit_r0_c48 bl[48] br[48] wl[0] vdd gnd cell_6t
Xbit_r1_c48 bl[48] br[48] wl[1] vdd gnd cell_6t
Xbit_r2_c48 bl[48] br[48] wl[2] vdd gnd cell_6t
Xbit_r3_c48 bl[48] br[48] wl[3] vdd gnd cell_6t
Xbit_r4_c48 bl[48] br[48] wl[4] vdd gnd cell_6t
Xbit_r5_c48 bl[48] br[48] wl[5] vdd gnd cell_6t
Xbit_r6_c48 bl[48] br[48] wl[6] vdd gnd cell_6t
Xbit_r7_c48 bl[48] br[48] wl[7] vdd gnd cell_6t
Xbit_r8_c48 bl[48] br[48] wl[8] vdd gnd cell_6t
Xbit_r9_c48 bl[48] br[48] wl[9] vdd gnd cell_6t
Xbit_r10_c48 bl[48] br[48] wl[10] vdd gnd cell_6t
Xbit_r11_c48 bl[48] br[48] wl[11] vdd gnd cell_6t
Xbit_r12_c48 bl[48] br[48] wl[12] vdd gnd cell_6t
Xbit_r13_c48 bl[48] br[48] wl[13] vdd gnd cell_6t
Xbit_r14_c48 bl[48] br[48] wl[14] vdd gnd cell_6t
Xbit_r15_c48 bl[48] br[48] wl[15] vdd gnd cell_6t
Xbit_r16_c48 bl[48] br[48] wl[16] vdd gnd cell_6t
Xbit_r17_c48 bl[48] br[48] wl[17] vdd gnd cell_6t
Xbit_r18_c48 bl[48] br[48] wl[18] vdd gnd cell_6t
Xbit_r19_c48 bl[48] br[48] wl[19] vdd gnd cell_6t
Xbit_r20_c48 bl[48] br[48] wl[20] vdd gnd cell_6t
Xbit_r21_c48 bl[48] br[48] wl[21] vdd gnd cell_6t
Xbit_r22_c48 bl[48] br[48] wl[22] vdd gnd cell_6t
Xbit_r23_c48 bl[48] br[48] wl[23] vdd gnd cell_6t
Xbit_r24_c48 bl[48] br[48] wl[24] vdd gnd cell_6t
Xbit_r25_c48 bl[48] br[48] wl[25] vdd gnd cell_6t
Xbit_r26_c48 bl[48] br[48] wl[26] vdd gnd cell_6t
Xbit_r27_c48 bl[48] br[48] wl[27] vdd gnd cell_6t
Xbit_r28_c48 bl[48] br[48] wl[28] vdd gnd cell_6t
Xbit_r29_c48 bl[48] br[48] wl[29] vdd gnd cell_6t
Xbit_r30_c48 bl[48] br[48] wl[30] vdd gnd cell_6t
Xbit_r31_c48 bl[48] br[48] wl[31] vdd gnd cell_6t
Xbit_r32_c48 bl[48] br[48] wl[32] vdd gnd cell_6t
Xbit_r33_c48 bl[48] br[48] wl[33] vdd gnd cell_6t
Xbit_r34_c48 bl[48] br[48] wl[34] vdd gnd cell_6t
Xbit_r35_c48 bl[48] br[48] wl[35] vdd gnd cell_6t
Xbit_r36_c48 bl[48] br[48] wl[36] vdd gnd cell_6t
Xbit_r37_c48 bl[48] br[48] wl[37] vdd gnd cell_6t
Xbit_r38_c48 bl[48] br[48] wl[38] vdd gnd cell_6t
Xbit_r39_c48 bl[48] br[48] wl[39] vdd gnd cell_6t
Xbit_r40_c48 bl[48] br[48] wl[40] vdd gnd cell_6t
Xbit_r41_c48 bl[48] br[48] wl[41] vdd gnd cell_6t
Xbit_r42_c48 bl[48] br[48] wl[42] vdd gnd cell_6t
Xbit_r43_c48 bl[48] br[48] wl[43] vdd gnd cell_6t
Xbit_r44_c48 bl[48] br[48] wl[44] vdd gnd cell_6t
Xbit_r45_c48 bl[48] br[48] wl[45] vdd gnd cell_6t
Xbit_r46_c48 bl[48] br[48] wl[46] vdd gnd cell_6t
Xbit_r47_c48 bl[48] br[48] wl[47] vdd gnd cell_6t
Xbit_r48_c48 bl[48] br[48] wl[48] vdd gnd cell_6t
Xbit_r49_c48 bl[48] br[48] wl[49] vdd gnd cell_6t
Xbit_r50_c48 bl[48] br[48] wl[50] vdd gnd cell_6t
Xbit_r51_c48 bl[48] br[48] wl[51] vdd gnd cell_6t
Xbit_r52_c48 bl[48] br[48] wl[52] vdd gnd cell_6t
Xbit_r53_c48 bl[48] br[48] wl[53] vdd gnd cell_6t
Xbit_r54_c48 bl[48] br[48] wl[54] vdd gnd cell_6t
Xbit_r55_c48 bl[48] br[48] wl[55] vdd gnd cell_6t
Xbit_r56_c48 bl[48] br[48] wl[56] vdd gnd cell_6t
Xbit_r57_c48 bl[48] br[48] wl[57] vdd gnd cell_6t
Xbit_r58_c48 bl[48] br[48] wl[58] vdd gnd cell_6t
Xbit_r59_c48 bl[48] br[48] wl[59] vdd gnd cell_6t
Xbit_r60_c48 bl[48] br[48] wl[60] vdd gnd cell_6t
Xbit_r61_c48 bl[48] br[48] wl[61] vdd gnd cell_6t
Xbit_r62_c48 bl[48] br[48] wl[62] vdd gnd cell_6t
Xbit_r63_c48 bl[48] br[48] wl[63] vdd gnd cell_6t
Xbit_r0_c49 bl[49] br[49] wl[0] vdd gnd cell_6t
Xbit_r1_c49 bl[49] br[49] wl[1] vdd gnd cell_6t
Xbit_r2_c49 bl[49] br[49] wl[2] vdd gnd cell_6t
Xbit_r3_c49 bl[49] br[49] wl[3] vdd gnd cell_6t
Xbit_r4_c49 bl[49] br[49] wl[4] vdd gnd cell_6t
Xbit_r5_c49 bl[49] br[49] wl[5] vdd gnd cell_6t
Xbit_r6_c49 bl[49] br[49] wl[6] vdd gnd cell_6t
Xbit_r7_c49 bl[49] br[49] wl[7] vdd gnd cell_6t
Xbit_r8_c49 bl[49] br[49] wl[8] vdd gnd cell_6t
Xbit_r9_c49 bl[49] br[49] wl[9] vdd gnd cell_6t
Xbit_r10_c49 bl[49] br[49] wl[10] vdd gnd cell_6t
Xbit_r11_c49 bl[49] br[49] wl[11] vdd gnd cell_6t
Xbit_r12_c49 bl[49] br[49] wl[12] vdd gnd cell_6t
Xbit_r13_c49 bl[49] br[49] wl[13] vdd gnd cell_6t
Xbit_r14_c49 bl[49] br[49] wl[14] vdd gnd cell_6t
Xbit_r15_c49 bl[49] br[49] wl[15] vdd gnd cell_6t
Xbit_r16_c49 bl[49] br[49] wl[16] vdd gnd cell_6t
Xbit_r17_c49 bl[49] br[49] wl[17] vdd gnd cell_6t
Xbit_r18_c49 bl[49] br[49] wl[18] vdd gnd cell_6t
Xbit_r19_c49 bl[49] br[49] wl[19] vdd gnd cell_6t
Xbit_r20_c49 bl[49] br[49] wl[20] vdd gnd cell_6t
Xbit_r21_c49 bl[49] br[49] wl[21] vdd gnd cell_6t
Xbit_r22_c49 bl[49] br[49] wl[22] vdd gnd cell_6t
Xbit_r23_c49 bl[49] br[49] wl[23] vdd gnd cell_6t
Xbit_r24_c49 bl[49] br[49] wl[24] vdd gnd cell_6t
Xbit_r25_c49 bl[49] br[49] wl[25] vdd gnd cell_6t
Xbit_r26_c49 bl[49] br[49] wl[26] vdd gnd cell_6t
Xbit_r27_c49 bl[49] br[49] wl[27] vdd gnd cell_6t
Xbit_r28_c49 bl[49] br[49] wl[28] vdd gnd cell_6t
Xbit_r29_c49 bl[49] br[49] wl[29] vdd gnd cell_6t
Xbit_r30_c49 bl[49] br[49] wl[30] vdd gnd cell_6t
Xbit_r31_c49 bl[49] br[49] wl[31] vdd gnd cell_6t
Xbit_r32_c49 bl[49] br[49] wl[32] vdd gnd cell_6t
Xbit_r33_c49 bl[49] br[49] wl[33] vdd gnd cell_6t
Xbit_r34_c49 bl[49] br[49] wl[34] vdd gnd cell_6t
Xbit_r35_c49 bl[49] br[49] wl[35] vdd gnd cell_6t
Xbit_r36_c49 bl[49] br[49] wl[36] vdd gnd cell_6t
Xbit_r37_c49 bl[49] br[49] wl[37] vdd gnd cell_6t
Xbit_r38_c49 bl[49] br[49] wl[38] vdd gnd cell_6t
Xbit_r39_c49 bl[49] br[49] wl[39] vdd gnd cell_6t
Xbit_r40_c49 bl[49] br[49] wl[40] vdd gnd cell_6t
Xbit_r41_c49 bl[49] br[49] wl[41] vdd gnd cell_6t
Xbit_r42_c49 bl[49] br[49] wl[42] vdd gnd cell_6t
Xbit_r43_c49 bl[49] br[49] wl[43] vdd gnd cell_6t
Xbit_r44_c49 bl[49] br[49] wl[44] vdd gnd cell_6t
Xbit_r45_c49 bl[49] br[49] wl[45] vdd gnd cell_6t
Xbit_r46_c49 bl[49] br[49] wl[46] vdd gnd cell_6t
Xbit_r47_c49 bl[49] br[49] wl[47] vdd gnd cell_6t
Xbit_r48_c49 bl[49] br[49] wl[48] vdd gnd cell_6t
Xbit_r49_c49 bl[49] br[49] wl[49] vdd gnd cell_6t
Xbit_r50_c49 bl[49] br[49] wl[50] vdd gnd cell_6t
Xbit_r51_c49 bl[49] br[49] wl[51] vdd gnd cell_6t
Xbit_r52_c49 bl[49] br[49] wl[52] vdd gnd cell_6t
Xbit_r53_c49 bl[49] br[49] wl[53] vdd gnd cell_6t
Xbit_r54_c49 bl[49] br[49] wl[54] vdd gnd cell_6t
Xbit_r55_c49 bl[49] br[49] wl[55] vdd gnd cell_6t
Xbit_r56_c49 bl[49] br[49] wl[56] vdd gnd cell_6t
Xbit_r57_c49 bl[49] br[49] wl[57] vdd gnd cell_6t
Xbit_r58_c49 bl[49] br[49] wl[58] vdd gnd cell_6t
Xbit_r59_c49 bl[49] br[49] wl[59] vdd gnd cell_6t
Xbit_r60_c49 bl[49] br[49] wl[60] vdd gnd cell_6t
Xbit_r61_c49 bl[49] br[49] wl[61] vdd gnd cell_6t
Xbit_r62_c49 bl[49] br[49] wl[62] vdd gnd cell_6t
Xbit_r63_c49 bl[49] br[49] wl[63] vdd gnd cell_6t
Xbit_r0_c50 bl[50] br[50] wl[0] vdd gnd cell_6t
Xbit_r1_c50 bl[50] br[50] wl[1] vdd gnd cell_6t
Xbit_r2_c50 bl[50] br[50] wl[2] vdd gnd cell_6t
Xbit_r3_c50 bl[50] br[50] wl[3] vdd gnd cell_6t
Xbit_r4_c50 bl[50] br[50] wl[4] vdd gnd cell_6t
Xbit_r5_c50 bl[50] br[50] wl[5] vdd gnd cell_6t
Xbit_r6_c50 bl[50] br[50] wl[6] vdd gnd cell_6t
Xbit_r7_c50 bl[50] br[50] wl[7] vdd gnd cell_6t
Xbit_r8_c50 bl[50] br[50] wl[8] vdd gnd cell_6t
Xbit_r9_c50 bl[50] br[50] wl[9] vdd gnd cell_6t
Xbit_r10_c50 bl[50] br[50] wl[10] vdd gnd cell_6t
Xbit_r11_c50 bl[50] br[50] wl[11] vdd gnd cell_6t
Xbit_r12_c50 bl[50] br[50] wl[12] vdd gnd cell_6t
Xbit_r13_c50 bl[50] br[50] wl[13] vdd gnd cell_6t
Xbit_r14_c50 bl[50] br[50] wl[14] vdd gnd cell_6t
Xbit_r15_c50 bl[50] br[50] wl[15] vdd gnd cell_6t
Xbit_r16_c50 bl[50] br[50] wl[16] vdd gnd cell_6t
Xbit_r17_c50 bl[50] br[50] wl[17] vdd gnd cell_6t
Xbit_r18_c50 bl[50] br[50] wl[18] vdd gnd cell_6t
Xbit_r19_c50 bl[50] br[50] wl[19] vdd gnd cell_6t
Xbit_r20_c50 bl[50] br[50] wl[20] vdd gnd cell_6t
Xbit_r21_c50 bl[50] br[50] wl[21] vdd gnd cell_6t
Xbit_r22_c50 bl[50] br[50] wl[22] vdd gnd cell_6t
Xbit_r23_c50 bl[50] br[50] wl[23] vdd gnd cell_6t
Xbit_r24_c50 bl[50] br[50] wl[24] vdd gnd cell_6t
Xbit_r25_c50 bl[50] br[50] wl[25] vdd gnd cell_6t
Xbit_r26_c50 bl[50] br[50] wl[26] vdd gnd cell_6t
Xbit_r27_c50 bl[50] br[50] wl[27] vdd gnd cell_6t
Xbit_r28_c50 bl[50] br[50] wl[28] vdd gnd cell_6t
Xbit_r29_c50 bl[50] br[50] wl[29] vdd gnd cell_6t
Xbit_r30_c50 bl[50] br[50] wl[30] vdd gnd cell_6t
Xbit_r31_c50 bl[50] br[50] wl[31] vdd gnd cell_6t
Xbit_r32_c50 bl[50] br[50] wl[32] vdd gnd cell_6t
Xbit_r33_c50 bl[50] br[50] wl[33] vdd gnd cell_6t
Xbit_r34_c50 bl[50] br[50] wl[34] vdd gnd cell_6t
Xbit_r35_c50 bl[50] br[50] wl[35] vdd gnd cell_6t
Xbit_r36_c50 bl[50] br[50] wl[36] vdd gnd cell_6t
Xbit_r37_c50 bl[50] br[50] wl[37] vdd gnd cell_6t
Xbit_r38_c50 bl[50] br[50] wl[38] vdd gnd cell_6t
Xbit_r39_c50 bl[50] br[50] wl[39] vdd gnd cell_6t
Xbit_r40_c50 bl[50] br[50] wl[40] vdd gnd cell_6t
Xbit_r41_c50 bl[50] br[50] wl[41] vdd gnd cell_6t
Xbit_r42_c50 bl[50] br[50] wl[42] vdd gnd cell_6t
Xbit_r43_c50 bl[50] br[50] wl[43] vdd gnd cell_6t
Xbit_r44_c50 bl[50] br[50] wl[44] vdd gnd cell_6t
Xbit_r45_c50 bl[50] br[50] wl[45] vdd gnd cell_6t
Xbit_r46_c50 bl[50] br[50] wl[46] vdd gnd cell_6t
Xbit_r47_c50 bl[50] br[50] wl[47] vdd gnd cell_6t
Xbit_r48_c50 bl[50] br[50] wl[48] vdd gnd cell_6t
Xbit_r49_c50 bl[50] br[50] wl[49] vdd gnd cell_6t
Xbit_r50_c50 bl[50] br[50] wl[50] vdd gnd cell_6t
Xbit_r51_c50 bl[50] br[50] wl[51] vdd gnd cell_6t
Xbit_r52_c50 bl[50] br[50] wl[52] vdd gnd cell_6t
Xbit_r53_c50 bl[50] br[50] wl[53] vdd gnd cell_6t
Xbit_r54_c50 bl[50] br[50] wl[54] vdd gnd cell_6t
Xbit_r55_c50 bl[50] br[50] wl[55] vdd gnd cell_6t
Xbit_r56_c50 bl[50] br[50] wl[56] vdd gnd cell_6t
Xbit_r57_c50 bl[50] br[50] wl[57] vdd gnd cell_6t
Xbit_r58_c50 bl[50] br[50] wl[58] vdd gnd cell_6t
Xbit_r59_c50 bl[50] br[50] wl[59] vdd gnd cell_6t
Xbit_r60_c50 bl[50] br[50] wl[60] vdd gnd cell_6t
Xbit_r61_c50 bl[50] br[50] wl[61] vdd gnd cell_6t
Xbit_r62_c50 bl[50] br[50] wl[62] vdd gnd cell_6t
Xbit_r63_c50 bl[50] br[50] wl[63] vdd gnd cell_6t
Xbit_r0_c51 bl[51] br[51] wl[0] vdd gnd cell_6t
Xbit_r1_c51 bl[51] br[51] wl[1] vdd gnd cell_6t
Xbit_r2_c51 bl[51] br[51] wl[2] vdd gnd cell_6t
Xbit_r3_c51 bl[51] br[51] wl[3] vdd gnd cell_6t
Xbit_r4_c51 bl[51] br[51] wl[4] vdd gnd cell_6t
Xbit_r5_c51 bl[51] br[51] wl[5] vdd gnd cell_6t
Xbit_r6_c51 bl[51] br[51] wl[6] vdd gnd cell_6t
Xbit_r7_c51 bl[51] br[51] wl[7] vdd gnd cell_6t
Xbit_r8_c51 bl[51] br[51] wl[8] vdd gnd cell_6t
Xbit_r9_c51 bl[51] br[51] wl[9] vdd gnd cell_6t
Xbit_r10_c51 bl[51] br[51] wl[10] vdd gnd cell_6t
Xbit_r11_c51 bl[51] br[51] wl[11] vdd gnd cell_6t
Xbit_r12_c51 bl[51] br[51] wl[12] vdd gnd cell_6t
Xbit_r13_c51 bl[51] br[51] wl[13] vdd gnd cell_6t
Xbit_r14_c51 bl[51] br[51] wl[14] vdd gnd cell_6t
Xbit_r15_c51 bl[51] br[51] wl[15] vdd gnd cell_6t
Xbit_r16_c51 bl[51] br[51] wl[16] vdd gnd cell_6t
Xbit_r17_c51 bl[51] br[51] wl[17] vdd gnd cell_6t
Xbit_r18_c51 bl[51] br[51] wl[18] vdd gnd cell_6t
Xbit_r19_c51 bl[51] br[51] wl[19] vdd gnd cell_6t
Xbit_r20_c51 bl[51] br[51] wl[20] vdd gnd cell_6t
Xbit_r21_c51 bl[51] br[51] wl[21] vdd gnd cell_6t
Xbit_r22_c51 bl[51] br[51] wl[22] vdd gnd cell_6t
Xbit_r23_c51 bl[51] br[51] wl[23] vdd gnd cell_6t
Xbit_r24_c51 bl[51] br[51] wl[24] vdd gnd cell_6t
Xbit_r25_c51 bl[51] br[51] wl[25] vdd gnd cell_6t
Xbit_r26_c51 bl[51] br[51] wl[26] vdd gnd cell_6t
Xbit_r27_c51 bl[51] br[51] wl[27] vdd gnd cell_6t
Xbit_r28_c51 bl[51] br[51] wl[28] vdd gnd cell_6t
Xbit_r29_c51 bl[51] br[51] wl[29] vdd gnd cell_6t
Xbit_r30_c51 bl[51] br[51] wl[30] vdd gnd cell_6t
Xbit_r31_c51 bl[51] br[51] wl[31] vdd gnd cell_6t
Xbit_r32_c51 bl[51] br[51] wl[32] vdd gnd cell_6t
Xbit_r33_c51 bl[51] br[51] wl[33] vdd gnd cell_6t
Xbit_r34_c51 bl[51] br[51] wl[34] vdd gnd cell_6t
Xbit_r35_c51 bl[51] br[51] wl[35] vdd gnd cell_6t
Xbit_r36_c51 bl[51] br[51] wl[36] vdd gnd cell_6t
Xbit_r37_c51 bl[51] br[51] wl[37] vdd gnd cell_6t
Xbit_r38_c51 bl[51] br[51] wl[38] vdd gnd cell_6t
Xbit_r39_c51 bl[51] br[51] wl[39] vdd gnd cell_6t
Xbit_r40_c51 bl[51] br[51] wl[40] vdd gnd cell_6t
Xbit_r41_c51 bl[51] br[51] wl[41] vdd gnd cell_6t
Xbit_r42_c51 bl[51] br[51] wl[42] vdd gnd cell_6t
Xbit_r43_c51 bl[51] br[51] wl[43] vdd gnd cell_6t
Xbit_r44_c51 bl[51] br[51] wl[44] vdd gnd cell_6t
Xbit_r45_c51 bl[51] br[51] wl[45] vdd gnd cell_6t
Xbit_r46_c51 bl[51] br[51] wl[46] vdd gnd cell_6t
Xbit_r47_c51 bl[51] br[51] wl[47] vdd gnd cell_6t
Xbit_r48_c51 bl[51] br[51] wl[48] vdd gnd cell_6t
Xbit_r49_c51 bl[51] br[51] wl[49] vdd gnd cell_6t
Xbit_r50_c51 bl[51] br[51] wl[50] vdd gnd cell_6t
Xbit_r51_c51 bl[51] br[51] wl[51] vdd gnd cell_6t
Xbit_r52_c51 bl[51] br[51] wl[52] vdd gnd cell_6t
Xbit_r53_c51 bl[51] br[51] wl[53] vdd gnd cell_6t
Xbit_r54_c51 bl[51] br[51] wl[54] vdd gnd cell_6t
Xbit_r55_c51 bl[51] br[51] wl[55] vdd gnd cell_6t
Xbit_r56_c51 bl[51] br[51] wl[56] vdd gnd cell_6t
Xbit_r57_c51 bl[51] br[51] wl[57] vdd gnd cell_6t
Xbit_r58_c51 bl[51] br[51] wl[58] vdd gnd cell_6t
Xbit_r59_c51 bl[51] br[51] wl[59] vdd gnd cell_6t
Xbit_r60_c51 bl[51] br[51] wl[60] vdd gnd cell_6t
Xbit_r61_c51 bl[51] br[51] wl[61] vdd gnd cell_6t
Xbit_r62_c51 bl[51] br[51] wl[62] vdd gnd cell_6t
Xbit_r63_c51 bl[51] br[51] wl[63] vdd gnd cell_6t
Xbit_r0_c52 bl[52] br[52] wl[0] vdd gnd cell_6t
Xbit_r1_c52 bl[52] br[52] wl[1] vdd gnd cell_6t
Xbit_r2_c52 bl[52] br[52] wl[2] vdd gnd cell_6t
Xbit_r3_c52 bl[52] br[52] wl[3] vdd gnd cell_6t
Xbit_r4_c52 bl[52] br[52] wl[4] vdd gnd cell_6t
Xbit_r5_c52 bl[52] br[52] wl[5] vdd gnd cell_6t
Xbit_r6_c52 bl[52] br[52] wl[6] vdd gnd cell_6t
Xbit_r7_c52 bl[52] br[52] wl[7] vdd gnd cell_6t
Xbit_r8_c52 bl[52] br[52] wl[8] vdd gnd cell_6t
Xbit_r9_c52 bl[52] br[52] wl[9] vdd gnd cell_6t
Xbit_r10_c52 bl[52] br[52] wl[10] vdd gnd cell_6t
Xbit_r11_c52 bl[52] br[52] wl[11] vdd gnd cell_6t
Xbit_r12_c52 bl[52] br[52] wl[12] vdd gnd cell_6t
Xbit_r13_c52 bl[52] br[52] wl[13] vdd gnd cell_6t
Xbit_r14_c52 bl[52] br[52] wl[14] vdd gnd cell_6t
Xbit_r15_c52 bl[52] br[52] wl[15] vdd gnd cell_6t
Xbit_r16_c52 bl[52] br[52] wl[16] vdd gnd cell_6t
Xbit_r17_c52 bl[52] br[52] wl[17] vdd gnd cell_6t
Xbit_r18_c52 bl[52] br[52] wl[18] vdd gnd cell_6t
Xbit_r19_c52 bl[52] br[52] wl[19] vdd gnd cell_6t
Xbit_r20_c52 bl[52] br[52] wl[20] vdd gnd cell_6t
Xbit_r21_c52 bl[52] br[52] wl[21] vdd gnd cell_6t
Xbit_r22_c52 bl[52] br[52] wl[22] vdd gnd cell_6t
Xbit_r23_c52 bl[52] br[52] wl[23] vdd gnd cell_6t
Xbit_r24_c52 bl[52] br[52] wl[24] vdd gnd cell_6t
Xbit_r25_c52 bl[52] br[52] wl[25] vdd gnd cell_6t
Xbit_r26_c52 bl[52] br[52] wl[26] vdd gnd cell_6t
Xbit_r27_c52 bl[52] br[52] wl[27] vdd gnd cell_6t
Xbit_r28_c52 bl[52] br[52] wl[28] vdd gnd cell_6t
Xbit_r29_c52 bl[52] br[52] wl[29] vdd gnd cell_6t
Xbit_r30_c52 bl[52] br[52] wl[30] vdd gnd cell_6t
Xbit_r31_c52 bl[52] br[52] wl[31] vdd gnd cell_6t
Xbit_r32_c52 bl[52] br[52] wl[32] vdd gnd cell_6t
Xbit_r33_c52 bl[52] br[52] wl[33] vdd gnd cell_6t
Xbit_r34_c52 bl[52] br[52] wl[34] vdd gnd cell_6t
Xbit_r35_c52 bl[52] br[52] wl[35] vdd gnd cell_6t
Xbit_r36_c52 bl[52] br[52] wl[36] vdd gnd cell_6t
Xbit_r37_c52 bl[52] br[52] wl[37] vdd gnd cell_6t
Xbit_r38_c52 bl[52] br[52] wl[38] vdd gnd cell_6t
Xbit_r39_c52 bl[52] br[52] wl[39] vdd gnd cell_6t
Xbit_r40_c52 bl[52] br[52] wl[40] vdd gnd cell_6t
Xbit_r41_c52 bl[52] br[52] wl[41] vdd gnd cell_6t
Xbit_r42_c52 bl[52] br[52] wl[42] vdd gnd cell_6t
Xbit_r43_c52 bl[52] br[52] wl[43] vdd gnd cell_6t
Xbit_r44_c52 bl[52] br[52] wl[44] vdd gnd cell_6t
Xbit_r45_c52 bl[52] br[52] wl[45] vdd gnd cell_6t
Xbit_r46_c52 bl[52] br[52] wl[46] vdd gnd cell_6t
Xbit_r47_c52 bl[52] br[52] wl[47] vdd gnd cell_6t
Xbit_r48_c52 bl[52] br[52] wl[48] vdd gnd cell_6t
Xbit_r49_c52 bl[52] br[52] wl[49] vdd gnd cell_6t
Xbit_r50_c52 bl[52] br[52] wl[50] vdd gnd cell_6t
Xbit_r51_c52 bl[52] br[52] wl[51] vdd gnd cell_6t
Xbit_r52_c52 bl[52] br[52] wl[52] vdd gnd cell_6t
Xbit_r53_c52 bl[52] br[52] wl[53] vdd gnd cell_6t
Xbit_r54_c52 bl[52] br[52] wl[54] vdd gnd cell_6t
Xbit_r55_c52 bl[52] br[52] wl[55] vdd gnd cell_6t
Xbit_r56_c52 bl[52] br[52] wl[56] vdd gnd cell_6t
Xbit_r57_c52 bl[52] br[52] wl[57] vdd gnd cell_6t
Xbit_r58_c52 bl[52] br[52] wl[58] vdd gnd cell_6t
Xbit_r59_c52 bl[52] br[52] wl[59] vdd gnd cell_6t
Xbit_r60_c52 bl[52] br[52] wl[60] vdd gnd cell_6t
Xbit_r61_c52 bl[52] br[52] wl[61] vdd gnd cell_6t
Xbit_r62_c52 bl[52] br[52] wl[62] vdd gnd cell_6t
Xbit_r63_c52 bl[52] br[52] wl[63] vdd gnd cell_6t
Xbit_r0_c53 bl[53] br[53] wl[0] vdd gnd cell_6t
Xbit_r1_c53 bl[53] br[53] wl[1] vdd gnd cell_6t
Xbit_r2_c53 bl[53] br[53] wl[2] vdd gnd cell_6t
Xbit_r3_c53 bl[53] br[53] wl[3] vdd gnd cell_6t
Xbit_r4_c53 bl[53] br[53] wl[4] vdd gnd cell_6t
Xbit_r5_c53 bl[53] br[53] wl[5] vdd gnd cell_6t
Xbit_r6_c53 bl[53] br[53] wl[6] vdd gnd cell_6t
Xbit_r7_c53 bl[53] br[53] wl[7] vdd gnd cell_6t
Xbit_r8_c53 bl[53] br[53] wl[8] vdd gnd cell_6t
Xbit_r9_c53 bl[53] br[53] wl[9] vdd gnd cell_6t
Xbit_r10_c53 bl[53] br[53] wl[10] vdd gnd cell_6t
Xbit_r11_c53 bl[53] br[53] wl[11] vdd gnd cell_6t
Xbit_r12_c53 bl[53] br[53] wl[12] vdd gnd cell_6t
Xbit_r13_c53 bl[53] br[53] wl[13] vdd gnd cell_6t
Xbit_r14_c53 bl[53] br[53] wl[14] vdd gnd cell_6t
Xbit_r15_c53 bl[53] br[53] wl[15] vdd gnd cell_6t
Xbit_r16_c53 bl[53] br[53] wl[16] vdd gnd cell_6t
Xbit_r17_c53 bl[53] br[53] wl[17] vdd gnd cell_6t
Xbit_r18_c53 bl[53] br[53] wl[18] vdd gnd cell_6t
Xbit_r19_c53 bl[53] br[53] wl[19] vdd gnd cell_6t
Xbit_r20_c53 bl[53] br[53] wl[20] vdd gnd cell_6t
Xbit_r21_c53 bl[53] br[53] wl[21] vdd gnd cell_6t
Xbit_r22_c53 bl[53] br[53] wl[22] vdd gnd cell_6t
Xbit_r23_c53 bl[53] br[53] wl[23] vdd gnd cell_6t
Xbit_r24_c53 bl[53] br[53] wl[24] vdd gnd cell_6t
Xbit_r25_c53 bl[53] br[53] wl[25] vdd gnd cell_6t
Xbit_r26_c53 bl[53] br[53] wl[26] vdd gnd cell_6t
Xbit_r27_c53 bl[53] br[53] wl[27] vdd gnd cell_6t
Xbit_r28_c53 bl[53] br[53] wl[28] vdd gnd cell_6t
Xbit_r29_c53 bl[53] br[53] wl[29] vdd gnd cell_6t
Xbit_r30_c53 bl[53] br[53] wl[30] vdd gnd cell_6t
Xbit_r31_c53 bl[53] br[53] wl[31] vdd gnd cell_6t
Xbit_r32_c53 bl[53] br[53] wl[32] vdd gnd cell_6t
Xbit_r33_c53 bl[53] br[53] wl[33] vdd gnd cell_6t
Xbit_r34_c53 bl[53] br[53] wl[34] vdd gnd cell_6t
Xbit_r35_c53 bl[53] br[53] wl[35] vdd gnd cell_6t
Xbit_r36_c53 bl[53] br[53] wl[36] vdd gnd cell_6t
Xbit_r37_c53 bl[53] br[53] wl[37] vdd gnd cell_6t
Xbit_r38_c53 bl[53] br[53] wl[38] vdd gnd cell_6t
Xbit_r39_c53 bl[53] br[53] wl[39] vdd gnd cell_6t
Xbit_r40_c53 bl[53] br[53] wl[40] vdd gnd cell_6t
Xbit_r41_c53 bl[53] br[53] wl[41] vdd gnd cell_6t
Xbit_r42_c53 bl[53] br[53] wl[42] vdd gnd cell_6t
Xbit_r43_c53 bl[53] br[53] wl[43] vdd gnd cell_6t
Xbit_r44_c53 bl[53] br[53] wl[44] vdd gnd cell_6t
Xbit_r45_c53 bl[53] br[53] wl[45] vdd gnd cell_6t
Xbit_r46_c53 bl[53] br[53] wl[46] vdd gnd cell_6t
Xbit_r47_c53 bl[53] br[53] wl[47] vdd gnd cell_6t
Xbit_r48_c53 bl[53] br[53] wl[48] vdd gnd cell_6t
Xbit_r49_c53 bl[53] br[53] wl[49] vdd gnd cell_6t
Xbit_r50_c53 bl[53] br[53] wl[50] vdd gnd cell_6t
Xbit_r51_c53 bl[53] br[53] wl[51] vdd gnd cell_6t
Xbit_r52_c53 bl[53] br[53] wl[52] vdd gnd cell_6t
Xbit_r53_c53 bl[53] br[53] wl[53] vdd gnd cell_6t
Xbit_r54_c53 bl[53] br[53] wl[54] vdd gnd cell_6t
Xbit_r55_c53 bl[53] br[53] wl[55] vdd gnd cell_6t
Xbit_r56_c53 bl[53] br[53] wl[56] vdd gnd cell_6t
Xbit_r57_c53 bl[53] br[53] wl[57] vdd gnd cell_6t
Xbit_r58_c53 bl[53] br[53] wl[58] vdd gnd cell_6t
Xbit_r59_c53 bl[53] br[53] wl[59] vdd gnd cell_6t
Xbit_r60_c53 bl[53] br[53] wl[60] vdd gnd cell_6t
Xbit_r61_c53 bl[53] br[53] wl[61] vdd gnd cell_6t
Xbit_r62_c53 bl[53] br[53] wl[62] vdd gnd cell_6t
Xbit_r63_c53 bl[53] br[53] wl[63] vdd gnd cell_6t
Xbit_r0_c54 bl[54] br[54] wl[0] vdd gnd cell_6t
Xbit_r1_c54 bl[54] br[54] wl[1] vdd gnd cell_6t
Xbit_r2_c54 bl[54] br[54] wl[2] vdd gnd cell_6t
Xbit_r3_c54 bl[54] br[54] wl[3] vdd gnd cell_6t
Xbit_r4_c54 bl[54] br[54] wl[4] vdd gnd cell_6t
Xbit_r5_c54 bl[54] br[54] wl[5] vdd gnd cell_6t
Xbit_r6_c54 bl[54] br[54] wl[6] vdd gnd cell_6t
Xbit_r7_c54 bl[54] br[54] wl[7] vdd gnd cell_6t
Xbit_r8_c54 bl[54] br[54] wl[8] vdd gnd cell_6t
Xbit_r9_c54 bl[54] br[54] wl[9] vdd gnd cell_6t
Xbit_r10_c54 bl[54] br[54] wl[10] vdd gnd cell_6t
Xbit_r11_c54 bl[54] br[54] wl[11] vdd gnd cell_6t
Xbit_r12_c54 bl[54] br[54] wl[12] vdd gnd cell_6t
Xbit_r13_c54 bl[54] br[54] wl[13] vdd gnd cell_6t
Xbit_r14_c54 bl[54] br[54] wl[14] vdd gnd cell_6t
Xbit_r15_c54 bl[54] br[54] wl[15] vdd gnd cell_6t
Xbit_r16_c54 bl[54] br[54] wl[16] vdd gnd cell_6t
Xbit_r17_c54 bl[54] br[54] wl[17] vdd gnd cell_6t
Xbit_r18_c54 bl[54] br[54] wl[18] vdd gnd cell_6t
Xbit_r19_c54 bl[54] br[54] wl[19] vdd gnd cell_6t
Xbit_r20_c54 bl[54] br[54] wl[20] vdd gnd cell_6t
Xbit_r21_c54 bl[54] br[54] wl[21] vdd gnd cell_6t
Xbit_r22_c54 bl[54] br[54] wl[22] vdd gnd cell_6t
Xbit_r23_c54 bl[54] br[54] wl[23] vdd gnd cell_6t
Xbit_r24_c54 bl[54] br[54] wl[24] vdd gnd cell_6t
Xbit_r25_c54 bl[54] br[54] wl[25] vdd gnd cell_6t
Xbit_r26_c54 bl[54] br[54] wl[26] vdd gnd cell_6t
Xbit_r27_c54 bl[54] br[54] wl[27] vdd gnd cell_6t
Xbit_r28_c54 bl[54] br[54] wl[28] vdd gnd cell_6t
Xbit_r29_c54 bl[54] br[54] wl[29] vdd gnd cell_6t
Xbit_r30_c54 bl[54] br[54] wl[30] vdd gnd cell_6t
Xbit_r31_c54 bl[54] br[54] wl[31] vdd gnd cell_6t
Xbit_r32_c54 bl[54] br[54] wl[32] vdd gnd cell_6t
Xbit_r33_c54 bl[54] br[54] wl[33] vdd gnd cell_6t
Xbit_r34_c54 bl[54] br[54] wl[34] vdd gnd cell_6t
Xbit_r35_c54 bl[54] br[54] wl[35] vdd gnd cell_6t
Xbit_r36_c54 bl[54] br[54] wl[36] vdd gnd cell_6t
Xbit_r37_c54 bl[54] br[54] wl[37] vdd gnd cell_6t
Xbit_r38_c54 bl[54] br[54] wl[38] vdd gnd cell_6t
Xbit_r39_c54 bl[54] br[54] wl[39] vdd gnd cell_6t
Xbit_r40_c54 bl[54] br[54] wl[40] vdd gnd cell_6t
Xbit_r41_c54 bl[54] br[54] wl[41] vdd gnd cell_6t
Xbit_r42_c54 bl[54] br[54] wl[42] vdd gnd cell_6t
Xbit_r43_c54 bl[54] br[54] wl[43] vdd gnd cell_6t
Xbit_r44_c54 bl[54] br[54] wl[44] vdd gnd cell_6t
Xbit_r45_c54 bl[54] br[54] wl[45] vdd gnd cell_6t
Xbit_r46_c54 bl[54] br[54] wl[46] vdd gnd cell_6t
Xbit_r47_c54 bl[54] br[54] wl[47] vdd gnd cell_6t
Xbit_r48_c54 bl[54] br[54] wl[48] vdd gnd cell_6t
Xbit_r49_c54 bl[54] br[54] wl[49] vdd gnd cell_6t
Xbit_r50_c54 bl[54] br[54] wl[50] vdd gnd cell_6t
Xbit_r51_c54 bl[54] br[54] wl[51] vdd gnd cell_6t
Xbit_r52_c54 bl[54] br[54] wl[52] vdd gnd cell_6t
Xbit_r53_c54 bl[54] br[54] wl[53] vdd gnd cell_6t
Xbit_r54_c54 bl[54] br[54] wl[54] vdd gnd cell_6t
Xbit_r55_c54 bl[54] br[54] wl[55] vdd gnd cell_6t
Xbit_r56_c54 bl[54] br[54] wl[56] vdd gnd cell_6t
Xbit_r57_c54 bl[54] br[54] wl[57] vdd gnd cell_6t
Xbit_r58_c54 bl[54] br[54] wl[58] vdd gnd cell_6t
Xbit_r59_c54 bl[54] br[54] wl[59] vdd gnd cell_6t
Xbit_r60_c54 bl[54] br[54] wl[60] vdd gnd cell_6t
Xbit_r61_c54 bl[54] br[54] wl[61] vdd gnd cell_6t
Xbit_r62_c54 bl[54] br[54] wl[62] vdd gnd cell_6t
Xbit_r63_c54 bl[54] br[54] wl[63] vdd gnd cell_6t
Xbit_r0_c55 bl[55] br[55] wl[0] vdd gnd cell_6t
Xbit_r1_c55 bl[55] br[55] wl[1] vdd gnd cell_6t
Xbit_r2_c55 bl[55] br[55] wl[2] vdd gnd cell_6t
Xbit_r3_c55 bl[55] br[55] wl[3] vdd gnd cell_6t
Xbit_r4_c55 bl[55] br[55] wl[4] vdd gnd cell_6t
Xbit_r5_c55 bl[55] br[55] wl[5] vdd gnd cell_6t
Xbit_r6_c55 bl[55] br[55] wl[6] vdd gnd cell_6t
Xbit_r7_c55 bl[55] br[55] wl[7] vdd gnd cell_6t
Xbit_r8_c55 bl[55] br[55] wl[8] vdd gnd cell_6t
Xbit_r9_c55 bl[55] br[55] wl[9] vdd gnd cell_6t
Xbit_r10_c55 bl[55] br[55] wl[10] vdd gnd cell_6t
Xbit_r11_c55 bl[55] br[55] wl[11] vdd gnd cell_6t
Xbit_r12_c55 bl[55] br[55] wl[12] vdd gnd cell_6t
Xbit_r13_c55 bl[55] br[55] wl[13] vdd gnd cell_6t
Xbit_r14_c55 bl[55] br[55] wl[14] vdd gnd cell_6t
Xbit_r15_c55 bl[55] br[55] wl[15] vdd gnd cell_6t
Xbit_r16_c55 bl[55] br[55] wl[16] vdd gnd cell_6t
Xbit_r17_c55 bl[55] br[55] wl[17] vdd gnd cell_6t
Xbit_r18_c55 bl[55] br[55] wl[18] vdd gnd cell_6t
Xbit_r19_c55 bl[55] br[55] wl[19] vdd gnd cell_6t
Xbit_r20_c55 bl[55] br[55] wl[20] vdd gnd cell_6t
Xbit_r21_c55 bl[55] br[55] wl[21] vdd gnd cell_6t
Xbit_r22_c55 bl[55] br[55] wl[22] vdd gnd cell_6t
Xbit_r23_c55 bl[55] br[55] wl[23] vdd gnd cell_6t
Xbit_r24_c55 bl[55] br[55] wl[24] vdd gnd cell_6t
Xbit_r25_c55 bl[55] br[55] wl[25] vdd gnd cell_6t
Xbit_r26_c55 bl[55] br[55] wl[26] vdd gnd cell_6t
Xbit_r27_c55 bl[55] br[55] wl[27] vdd gnd cell_6t
Xbit_r28_c55 bl[55] br[55] wl[28] vdd gnd cell_6t
Xbit_r29_c55 bl[55] br[55] wl[29] vdd gnd cell_6t
Xbit_r30_c55 bl[55] br[55] wl[30] vdd gnd cell_6t
Xbit_r31_c55 bl[55] br[55] wl[31] vdd gnd cell_6t
Xbit_r32_c55 bl[55] br[55] wl[32] vdd gnd cell_6t
Xbit_r33_c55 bl[55] br[55] wl[33] vdd gnd cell_6t
Xbit_r34_c55 bl[55] br[55] wl[34] vdd gnd cell_6t
Xbit_r35_c55 bl[55] br[55] wl[35] vdd gnd cell_6t
Xbit_r36_c55 bl[55] br[55] wl[36] vdd gnd cell_6t
Xbit_r37_c55 bl[55] br[55] wl[37] vdd gnd cell_6t
Xbit_r38_c55 bl[55] br[55] wl[38] vdd gnd cell_6t
Xbit_r39_c55 bl[55] br[55] wl[39] vdd gnd cell_6t
Xbit_r40_c55 bl[55] br[55] wl[40] vdd gnd cell_6t
Xbit_r41_c55 bl[55] br[55] wl[41] vdd gnd cell_6t
Xbit_r42_c55 bl[55] br[55] wl[42] vdd gnd cell_6t
Xbit_r43_c55 bl[55] br[55] wl[43] vdd gnd cell_6t
Xbit_r44_c55 bl[55] br[55] wl[44] vdd gnd cell_6t
Xbit_r45_c55 bl[55] br[55] wl[45] vdd gnd cell_6t
Xbit_r46_c55 bl[55] br[55] wl[46] vdd gnd cell_6t
Xbit_r47_c55 bl[55] br[55] wl[47] vdd gnd cell_6t
Xbit_r48_c55 bl[55] br[55] wl[48] vdd gnd cell_6t
Xbit_r49_c55 bl[55] br[55] wl[49] vdd gnd cell_6t
Xbit_r50_c55 bl[55] br[55] wl[50] vdd gnd cell_6t
Xbit_r51_c55 bl[55] br[55] wl[51] vdd gnd cell_6t
Xbit_r52_c55 bl[55] br[55] wl[52] vdd gnd cell_6t
Xbit_r53_c55 bl[55] br[55] wl[53] vdd gnd cell_6t
Xbit_r54_c55 bl[55] br[55] wl[54] vdd gnd cell_6t
Xbit_r55_c55 bl[55] br[55] wl[55] vdd gnd cell_6t
Xbit_r56_c55 bl[55] br[55] wl[56] vdd gnd cell_6t
Xbit_r57_c55 bl[55] br[55] wl[57] vdd gnd cell_6t
Xbit_r58_c55 bl[55] br[55] wl[58] vdd gnd cell_6t
Xbit_r59_c55 bl[55] br[55] wl[59] vdd gnd cell_6t
Xbit_r60_c55 bl[55] br[55] wl[60] vdd gnd cell_6t
Xbit_r61_c55 bl[55] br[55] wl[61] vdd gnd cell_6t
Xbit_r62_c55 bl[55] br[55] wl[62] vdd gnd cell_6t
Xbit_r63_c55 bl[55] br[55] wl[63] vdd gnd cell_6t
Xbit_r0_c56 bl[56] br[56] wl[0] vdd gnd cell_6t
Xbit_r1_c56 bl[56] br[56] wl[1] vdd gnd cell_6t
Xbit_r2_c56 bl[56] br[56] wl[2] vdd gnd cell_6t
Xbit_r3_c56 bl[56] br[56] wl[3] vdd gnd cell_6t
Xbit_r4_c56 bl[56] br[56] wl[4] vdd gnd cell_6t
Xbit_r5_c56 bl[56] br[56] wl[5] vdd gnd cell_6t
Xbit_r6_c56 bl[56] br[56] wl[6] vdd gnd cell_6t
Xbit_r7_c56 bl[56] br[56] wl[7] vdd gnd cell_6t
Xbit_r8_c56 bl[56] br[56] wl[8] vdd gnd cell_6t
Xbit_r9_c56 bl[56] br[56] wl[9] vdd gnd cell_6t
Xbit_r10_c56 bl[56] br[56] wl[10] vdd gnd cell_6t
Xbit_r11_c56 bl[56] br[56] wl[11] vdd gnd cell_6t
Xbit_r12_c56 bl[56] br[56] wl[12] vdd gnd cell_6t
Xbit_r13_c56 bl[56] br[56] wl[13] vdd gnd cell_6t
Xbit_r14_c56 bl[56] br[56] wl[14] vdd gnd cell_6t
Xbit_r15_c56 bl[56] br[56] wl[15] vdd gnd cell_6t
Xbit_r16_c56 bl[56] br[56] wl[16] vdd gnd cell_6t
Xbit_r17_c56 bl[56] br[56] wl[17] vdd gnd cell_6t
Xbit_r18_c56 bl[56] br[56] wl[18] vdd gnd cell_6t
Xbit_r19_c56 bl[56] br[56] wl[19] vdd gnd cell_6t
Xbit_r20_c56 bl[56] br[56] wl[20] vdd gnd cell_6t
Xbit_r21_c56 bl[56] br[56] wl[21] vdd gnd cell_6t
Xbit_r22_c56 bl[56] br[56] wl[22] vdd gnd cell_6t
Xbit_r23_c56 bl[56] br[56] wl[23] vdd gnd cell_6t
Xbit_r24_c56 bl[56] br[56] wl[24] vdd gnd cell_6t
Xbit_r25_c56 bl[56] br[56] wl[25] vdd gnd cell_6t
Xbit_r26_c56 bl[56] br[56] wl[26] vdd gnd cell_6t
Xbit_r27_c56 bl[56] br[56] wl[27] vdd gnd cell_6t
Xbit_r28_c56 bl[56] br[56] wl[28] vdd gnd cell_6t
Xbit_r29_c56 bl[56] br[56] wl[29] vdd gnd cell_6t
Xbit_r30_c56 bl[56] br[56] wl[30] vdd gnd cell_6t
Xbit_r31_c56 bl[56] br[56] wl[31] vdd gnd cell_6t
Xbit_r32_c56 bl[56] br[56] wl[32] vdd gnd cell_6t
Xbit_r33_c56 bl[56] br[56] wl[33] vdd gnd cell_6t
Xbit_r34_c56 bl[56] br[56] wl[34] vdd gnd cell_6t
Xbit_r35_c56 bl[56] br[56] wl[35] vdd gnd cell_6t
Xbit_r36_c56 bl[56] br[56] wl[36] vdd gnd cell_6t
Xbit_r37_c56 bl[56] br[56] wl[37] vdd gnd cell_6t
Xbit_r38_c56 bl[56] br[56] wl[38] vdd gnd cell_6t
Xbit_r39_c56 bl[56] br[56] wl[39] vdd gnd cell_6t
Xbit_r40_c56 bl[56] br[56] wl[40] vdd gnd cell_6t
Xbit_r41_c56 bl[56] br[56] wl[41] vdd gnd cell_6t
Xbit_r42_c56 bl[56] br[56] wl[42] vdd gnd cell_6t
Xbit_r43_c56 bl[56] br[56] wl[43] vdd gnd cell_6t
Xbit_r44_c56 bl[56] br[56] wl[44] vdd gnd cell_6t
Xbit_r45_c56 bl[56] br[56] wl[45] vdd gnd cell_6t
Xbit_r46_c56 bl[56] br[56] wl[46] vdd gnd cell_6t
Xbit_r47_c56 bl[56] br[56] wl[47] vdd gnd cell_6t
Xbit_r48_c56 bl[56] br[56] wl[48] vdd gnd cell_6t
Xbit_r49_c56 bl[56] br[56] wl[49] vdd gnd cell_6t
Xbit_r50_c56 bl[56] br[56] wl[50] vdd gnd cell_6t
Xbit_r51_c56 bl[56] br[56] wl[51] vdd gnd cell_6t
Xbit_r52_c56 bl[56] br[56] wl[52] vdd gnd cell_6t
Xbit_r53_c56 bl[56] br[56] wl[53] vdd gnd cell_6t
Xbit_r54_c56 bl[56] br[56] wl[54] vdd gnd cell_6t
Xbit_r55_c56 bl[56] br[56] wl[55] vdd gnd cell_6t
Xbit_r56_c56 bl[56] br[56] wl[56] vdd gnd cell_6t
Xbit_r57_c56 bl[56] br[56] wl[57] vdd gnd cell_6t
Xbit_r58_c56 bl[56] br[56] wl[58] vdd gnd cell_6t
Xbit_r59_c56 bl[56] br[56] wl[59] vdd gnd cell_6t
Xbit_r60_c56 bl[56] br[56] wl[60] vdd gnd cell_6t
Xbit_r61_c56 bl[56] br[56] wl[61] vdd gnd cell_6t
Xbit_r62_c56 bl[56] br[56] wl[62] vdd gnd cell_6t
Xbit_r63_c56 bl[56] br[56] wl[63] vdd gnd cell_6t
Xbit_r0_c57 bl[57] br[57] wl[0] vdd gnd cell_6t
Xbit_r1_c57 bl[57] br[57] wl[1] vdd gnd cell_6t
Xbit_r2_c57 bl[57] br[57] wl[2] vdd gnd cell_6t
Xbit_r3_c57 bl[57] br[57] wl[3] vdd gnd cell_6t
Xbit_r4_c57 bl[57] br[57] wl[4] vdd gnd cell_6t
Xbit_r5_c57 bl[57] br[57] wl[5] vdd gnd cell_6t
Xbit_r6_c57 bl[57] br[57] wl[6] vdd gnd cell_6t
Xbit_r7_c57 bl[57] br[57] wl[7] vdd gnd cell_6t
Xbit_r8_c57 bl[57] br[57] wl[8] vdd gnd cell_6t
Xbit_r9_c57 bl[57] br[57] wl[9] vdd gnd cell_6t
Xbit_r10_c57 bl[57] br[57] wl[10] vdd gnd cell_6t
Xbit_r11_c57 bl[57] br[57] wl[11] vdd gnd cell_6t
Xbit_r12_c57 bl[57] br[57] wl[12] vdd gnd cell_6t
Xbit_r13_c57 bl[57] br[57] wl[13] vdd gnd cell_6t
Xbit_r14_c57 bl[57] br[57] wl[14] vdd gnd cell_6t
Xbit_r15_c57 bl[57] br[57] wl[15] vdd gnd cell_6t
Xbit_r16_c57 bl[57] br[57] wl[16] vdd gnd cell_6t
Xbit_r17_c57 bl[57] br[57] wl[17] vdd gnd cell_6t
Xbit_r18_c57 bl[57] br[57] wl[18] vdd gnd cell_6t
Xbit_r19_c57 bl[57] br[57] wl[19] vdd gnd cell_6t
Xbit_r20_c57 bl[57] br[57] wl[20] vdd gnd cell_6t
Xbit_r21_c57 bl[57] br[57] wl[21] vdd gnd cell_6t
Xbit_r22_c57 bl[57] br[57] wl[22] vdd gnd cell_6t
Xbit_r23_c57 bl[57] br[57] wl[23] vdd gnd cell_6t
Xbit_r24_c57 bl[57] br[57] wl[24] vdd gnd cell_6t
Xbit_r25_c57 bl[57] br[57] wl[25] vdd gnd cell_6t
Xbit_r26_c57 bl[57] br[57] wl[26] vdd gnd cell_6t
Xbit_r27_c57 bl[57] br[57] wl[27] vdd gnd cell_6t
Xbit_r28_c57 bl[57] br[57] wl[28] vdd gnd cell_6t
Xbit_r29_c57 bl[57] br[57] wl[29] vdd gnd cell_6t
Xbit_r30_c57 bl[57] br[57] wl[30] vdd gnd cell_6t
Xbit_r31_c57 bl[57] br[57] wl[31] vdd gnd cell_6t
Xbit_r32_c57 bl[57] br[57] wl[32] vdd gnd cell_6t
Xbit_r33_c57 bl[57] br[57] wl[33] vdd gnd cell_6t
Xbit_r34_c57 bl[57] br[57] wl[34] vdd gnd cell_6t
Xbit_r35_c57 bl[57] br[57] wl[35] vdd gnd cell_6t
Xbit_r36_c57 bl[57] br[57] wl[36] vdd gnd cell_6t
Xbit_r37_c57 bl[57] br[57] wl[37] vdd gnd cell_6t
Xbit_r38_c57 bl[57] br[57] wl[38] vdd gnd cell_6t
Xbit_r39_c57 bl[57] br[57] wl[39] vdd gnd cell_6t
Xbit_r40_c57 bl[57] br[57] wl[40] vdd gnd cell_6t
Xbit_r41_c57 bl[57] br[57] wl[41] vdd gnd cell_6t
Xbit_r42_c57 bl[57] br[57] wl[42] vdd gnd cell_6t
Xbit_r43_c57 bl[57] br[57] wl[43] vdd gnd cell_6t
Xbit_r44_c57 bl[57] br[57] wl[44] vdd gnd cell_6t
Xbit_r45_c57 bl[57] br[57] wl[45] vdd gnd cell_6t
Xbit_r46_c57 bl[57] br[57] wl[46] vdd gnd cell_6t
Xbit_r47_c57 bl[57] br[57] wl[47] vdd gnd cell_6t
Xbit_r48_c57 bl[57] br[57] wl[48] vdd gnd cell_6t
Xbit_r49_c57 bl[57] br[57] wl[49] vdd gnd cell_6t
Xbit_r50_c57 bl[57] br[57] wl[50] vdd gnd cell_6t
Xbit_r51_c57 bl[57] br[57] wl[51] vdd gnd cell_6t
Xbit_r52_c57 bl[57] br[57] wl[52] vdd gnd cell_6t
Xbit_r53_c57 bl[57] br[57] wl[53] vdd gnd cell_6t
Xbit_r54_c57 bl[57] br[57] wl[54] vdd gnd cell_6t
Xbit_r55_c57 bl[57] br[57] wl[55] vdd gnd cell_6t
Xbit_r56_c57 bl[57] br[57] wl[56] vdd gnd cell_6t
Xbit_r57_c57 bl[57] br[57] wl[57] vdd gnd cell_6t
Xbit_r58_c57 bl[57] br[57] wl[58] vdd gnd cell_6t
Xbit_r59_c57 bl[57] br[57] wl[59] vdd gnd cell_6t
Xbit_r60_c57 bl[57] br[57] wl[60] vdd gnd cell_6t
Xbit_r61_c57 bl[57] br[57] wl[61] vdd gnd cell_6t
Xbit_r62_c57 bl[57] br[57] wl[62] vdd gnd cell_6t
Xbit_r63_c57 bl[57] br[57] wl[63] vdd gnd cell_6t
Xbit_r0_c58 bl[58] br[58] wl[0] vdd gnd cell_6t
Xbit_r1_c58 bl[58] br[58] wl[1] vdd gnd cell_6t
Xbit_r2_c58 bl[58] br[58] wl[2] vdd gnd cell_6t
Xbit_r3_c58 bl[58] br[58] wl[3] vdd gnd cell_6t
Xbit_r4_c58 bl[58] br[58] wl[4] vdd gnd cell_6t
Xbit_r5_c58 bl[58] br[58] wl[5] vdd gnd cell_6t
Xbit_r6_c58 bl[58] br[58] wl[6] vdd gnd cell_6t
Xbit_r7_c58 bl[58] br[58] wl[7] vdd gnd cell_6t
Xbit_r8_c58 bl[58] br[58] wl[8] vdd gnd cell_6t
Xbit_r9_c58 bl[58] br[58] wl[9] vdd gnd cell_6t
Xbit_r10_c58 bl[58] br[58] wl[10] vdd gnd cell_6t
Xbit_r11_c58 bl[58] br[58] wl[11] vdd gnd cell_6t
Xbit_r12_c58 bl[58] br[58] wl[12] vdd gnd cell_6t
Xbit_r13_c58 bl[58] br[58] wl[13] vdd gnd cell_6t
Xbit_r14_c58 bl[58] br[58] wl[14] vdd gnd cell_6t
Xbit_r15_c58 bl[58] br[58] wl[15] vdd gnd cell_6t
Xbit_r16_c58 bl[58] br[58] wl[16] vdd gnd cell_6t
Xbit_r17_c58 bl[58] br[58] wl[17] vdd gnd cell_6t
Xbit_r18_c58 bl[58] br[58] wl[18] vdd gnd cell_6t
Xbit_r19_c58 bl[58] br[58] wl[19] vdd gnd cell_6t
Xbit_r20_c58 bl[58] br[58] wl[20] vdd gnd cell_6t
Xbit_r21_c58 bl[58] br[58] wl[21] vdd gnd cell_6t
Xbit_r22_c58 bl[58] br[58] wl[22] vdd gnd cell_6t
Xbit_r23_c58 bl[58] br[58] wl[23] vdd gnd cell_6t
Xbit_r24_c58 bl[58] br[58] wl[24] vdd gnd cell_6t
Xbit_r25_c58 bl[58] br[58] wl[25] vdd gnd cell_6t
Xbit_r26_c58 bl[58] br[58] wl[26] vdd gnd cell_6t
Xbit_r27_c58 bl[58] br[58] wl[27] vdd gnd cell_6t
Xbit_r28_c58 bl[58] br[58] wl[28] vdd gnd cell_6t
Xbit_r29_c58 bl[58] br[58] wl[29] vdd gnd cell_6t
Xbit_r30_c58 bl[58] br[58] wl[30] vdd gnd cell_6t
Xbit_r31_c58 bl[58] br[58] wl[31] vdd gnd cell_6t
Xbit_r32_c58 bl[58] br[58] wl[32] vdd gnd cell_6t
Xbit_r33_c58 bl[58] br[58] wl[33] vdd gnd cell_6t
Xbit_r34_c58 bl[58] br[58] wl[34] vdd gnd cell_6t
Xbit_r35_c58 bl[58] br[58] wl[35] vdd gnd cell_6t
Xbit_r36_c58 bl[58] br[58] wl[36] vdd gnd cell_6t
Xbit_r37_c58 bl[58] br[58] wl[37] vdd gnd cell_6t
Xbit_r38_c58 bl[58] br[58] wl[38] vdd gnd cell_6t
Xbit_r39_c58 bl[58] br[58] wl[39] vdd gnd cell_6t
Xbit_r40_c58 bl[58] br[58] wl[40] vdd gnd cell_6t
Xbit_r41_c58 bl[58] br[58] wl[41] vdd gnd cell_6t
Xbit_r42_c58 bl[58] br[58] wl[42] vdd gnd cell_6t
Xbit_r43_c58 bl[58] br[58] wl[43] vdd gnd cell_6t
Xbit_r44_c58 bl[58] br[58] wl[44] vdd gnd cell_6t
Xbit_r45_c58 bl[58] br[58] wl[45] vdd gnd cell_6t
Xbit_r46_c58 bl[58] br[58] wl[46] vdd gnd cell_6t
Xbit_r47_c58 bl[58] br[58] wl[47] vdd gnd cell_6t
Xbit_r48_c58 bl[58] br[58] wl[48] vdd gnd cell_6t
Xbit_r49_c58 bl[58] br[58] wl[49] vdd gnd cell_6t
Xbit_r50_c58 bl[58] br[58] wl[50] vdd gnd cell_6t
Xbit_r51_c58 bl[58] br[58] wl[51] vdd gnd cell_6t
Xbit_r52_c58 bl[58] br[58] wl[52] vdd gnd cell_6t
Xbit_r53_c58 bl[58] br[58] wl[53] vdd gnd cell_6t
Xbit_r54_c58 bl[58] br[58] wl[54] vdd gnd cell_6t
Xbit_r55_c58 bl[58] br[58] wl[55] vdd gnd cell_6t
Xbit_r56_c58 bl[58] br[58] wl[56] vdd gnd cell_6t
Xbit_r57_c58 bl[58] br[58] wl[57] vdd gnd cell_6t
Xbit_r58_c58 bl[58] br[58] wl[58] vdd gnd cell_6t
Xbit_r59_c58 bl[58] br[58] wl[59] vdd gnd cell_6t
Xbit_r60_c58 bl[58] br[58] wl[60] vdd gnd cell_6t
Xbit_r61_c58 bl[58] br[58] wl[61] vdd gnd cell_6t
Xbit_r62_c58 bl[58] br[58] wl[62] vdd gnd cell_6t
Xbit_r63_c58 bl[58] br[58] wl[63] vdd gnd cell_6t
Xbit_r0_c59 bl[59] br[59] wl[0] vdd gnd cell_6t
Xbit_r1_c59 bl[59] br[59] wl[1] vdd gnd cell_6t
Xbit_r2_c59 bl[59] br[59] wl[2] vdd gnd cell_6t
Xbit_r3_c59 bl[59] br[59] wl[3] vdd gnd cell_6t
Xbit_r4_c59 bl[59] br[59] wl[4] vdd gnd cell_6t
Xbit_r5_c59 bl[59] br[59] wl[5] vdd gnd cell_6t
Xbit_r6_c59 bl[59] br[59] wl[6] vdd gnd cell_6t
Xbit_r7_c59 bl[59] br[59] wl[7] vdd gnd cell_6t
Xbit_r8_c59 bl[59] br[59] wl[8] vdd gnd cell_6t
Xbit_r9_c59 bl[59] br[59] wl[9] vdd gnd cell_6t
Xbit_r10_c59 bl[59] br[59] wl[10] vdd gnd cell_6t
Xbit_r11_c59 bl[59] br[59] wl[11] vdd gnd cell_6t
Xbit_r12_c59 bl[59] br[59] wl[12] vdd gnd cell_6t
Xbit_r13_c59 bl[59] br[59] wl[13] vdd gnd cell_6t
Xbit_r14_c59 bl[59] br[59] wl[14] vdd gnd cell_6t
Xbit_r15_c59 bl[59] br[59] wl[15] vdd gnd cell_6t
Xbit_r16_c59 bl[59] br[59] wl[16] vdd gnd cell_6t
Xbit_r17_c59 bl[59] br[59] wl[17] vdd gnd cell_6t
Xbit_r18_c59 bl[59] br[59] wl[18] vdd gnd cell_6t
Xbit_r19_c59 bl[59] br[59] wl[19] vdd gnd cell_6t
Xbit_r20_c59 bl[59] br[59] wl[20] vdd gnd cell_6t
Xbit_r21_c59 bl[59] br[59] wl[21] vdd gnd cell_6t
Xbit_r22_c59 bl[59] br[59] wl[22] vdd gnd cell_6t
Xbit_r23_c59 bl[59] br[59] wl[23] vdd gnd cell_6t
Xbit_r24_c59 bl[59] br[59] wl[24] vdd gnd cell_6t
Xbit_r25_c59 bl[59] br[59] wl[25] vdd gnd cell_6t
Xbit_r26_c59 bl[59] br[59] wl[26] vdd gnd cell_6t
Xbit_r27_c59 bl[59] br[59] wl[27] vdd gnd cell_6t
Xbit_r28_c59 bl[59] br[59] wl[28] vdd gnd cell_6t
Xbit_r29_c59 bl[59] br[59] wl[29] vdd gnd cell_6t
Xbit_r30_c59 bl[59] br[59] wl[30] vdd gnd cell_6t
Xbit_r31_c59 bl[59] br[59] wl[31] vdd gnd cell_6t
Xbit_r32_c59 bl[59] br[59] wl[32] vdd gnd cell_6t
Xbit_r33_c59 bl[59] br[59] wl[33] vdd gnd cell_6t
Xbit_r34_c59 bl[59] br[59] wl[34] vdd gnd cell_6t
Xbit_r35_c59 bl[59] br[59] wl[35] vdd gnd cell_6t
Xbit_r36_c59 bl[59] br[59] wl[36] vdd gnd cell_6t
Xbit_r37_c59 bl[59] br[59] wl[37] vdd gnd cell_6t
Xbit_r38_c59 bl[59] br[59] wl[38] vdd gnd cell_6t
Xbit_r39_c59 bl[59] br[59] wl[39] vdd gnd cell_6t
Xbit_r40_c59 bl[59] br[59] wl[40] vdd gnd cell_6t
Xbit_r41_c59 bl[59] br[59] wl[41] vdd gnd cell_6t
Xbit_r42_c59 bl[59] br[59] wl[42] vdd gnd cell_6t
Xbit_r43_c59 bl[59] br[59] wl[43] vdd gnd cell_6t
Xbit_r44_c59 bl[59] br[59] wl[44] vdd gnd cell_6t
Xbit_r45_c59 bl[59] br[59] wl[45] vdd gnd cell_6t
Xbit_r46_c59 bl[59] br[59] wl[46] vdd gnd cell_6t
Xbit_r47_c59 bl[59] br[59] wl[47] vdd gnd cell_6t
Xbit_r48_c59 bl[59] br[59] wl[48] vdd gnd cell_6t
Xbit_r49_c59 bl[59] br[59] wl[49] vdd gnd cell_6t
Xbit_r50_c59 bl[59] br[59] wl[50] vdd gnd cell_6t
Xbit_r51_c59 bl[59] br[59] wl[51] vdd gnd cell_6t
Xbit_r52_c59 bl[59] br[59] wl[52] vdd gnd cell_6t
Xbit_r53_c59 bl[59] br[59] wl[53] vdd gnd cell_6t
Xbit_r54_c59 bl[59] br[59] wl[54] vdd gnd cell_6t
Xbit_r55_c59 bl[59] br[59] wl[55] vdd gnd cell_6t
Xbit_r56_c59 bl[59] br[59] wl[56] vdd gnd cell_6t
Xbit_r57_c59 bl[59] br[59] wl[57] vdd gnd cell_6t
Xbit_r58_c59 bl[59] br[59] wl[58] vdd gnd cell_6t
Xbit_r59_c59 bl[59] br[59] wl[59] vdd gnd cell_6t
Xbit_r60_c59 bl[59] br[59] wl[60] vdd gnd cell_6t
Xbit_r61_c59 bl[59] br[59] wl[61] vdd gnd cell_6t
Xbit_r62_c59 bl[59] br[59] wl[62] vdd gnd cell_6t
Xbit_r63_c59 bl[59] br[59] wl[63] vdd gnd cell_6t
Xbit_r0_c60 bl[60] br[60] wl[0] vdd gnd cell_6t
Xbit_r1_c60 bl[60] br[60] wl[1] vdd gnd cell_6t
Xbit_r2_c60 bl[60] br[60] wl[2] vdd gnd cell_6t
Xbit_r3_c60 bl[60] br[60] wl[3] vdd gnd cell_6t
Xbit_r4_c60 bl[60] br[60] wl[4] vdd gnd cell_6t
Xbit_r5_c60 bl[60] br[60] wl[5] vdd gnd cell_6t
Xbit_r6_c60 bl[60] br[60] wl[6] vdd gnd cell_6t
Xbit_r7_c60 bl[60] br[60] wl[7] vdd gnd cell_6t
Xbit_r8_c60 bl[60] br[60] wl[8] vdd gnd cell_6t
Xbit_r9_c60 bl[60] br[60] wl[9] vdd gnd cell_6t
Xbit_r10_c60 bl[60] br[60] wl[10] vdd gnd cell_6t
Xbit_r11_c60 bl[60] br[60] wl[11] vdd gnd cell_6t
Xbit_r12_c60 bl[60] br[60] wl[12] vdd gnd cell_6t
Xbit_r13_c60 bl[60] br[60] wl[13] vdd gnd cell_6t
Xbit_r14_c60 bl[60] br[60] wl[14] vdd gnd cell_6t
Xbit_r15_c60 bl[60] br[60] wl[15] vdd gnd cell_6t
Xbit_r16_c60 bl[60] br[60] wl[16] vdd gnd cell_6t
Xbit_r17_c60 bl[60] br[60] wl[17] vdd gnd cell_6t
Xbit_r18_c60 bl[60] br[60] wl[18] vdd gnd cell_6t
Xbit_r19_c60 bl[60] br[60] wl[19] vdd gnd cell_6t
Xbit_r20_c60 bl[60] br[60] wl[20] vdd gnd cell_6t
Xbit_r21_c60 bl[60] br[60] wl[21] vdd gnd cell_6t
Xbit_r22_c60 bl[60] br[60] wl[22] vdd gnd cell_6t
Xbit_r23_c60 bl[60] br[60] wl[23] vdd gnd cell_6t
Xbit_r24_c60 bl[60] br[60] wl[24] vdd gnd cell_6t
Xbit_r25_c60 bl[60] br[60] wl[25] vdd gnd cell_6t
Xbit_r26_c60 bl[60] br[60] wl[26] vdd gnd cell_6t
Xbit_r27_c60 bl[60] br[60] wl[27] vdd gnd cell_6t
Xbit_r28_c60 bl[60] br[60] wl[28] vdd gnd cell_6t
Xbit_r29_c60 bl[60] br[60] wl[29] vdd gnd cell_6t
Xbit_r30_c60 bl[60] br[60] wl[30] vdd gnd cell_6t
Xbit_r31_c60 bl[60] br[60] wl[31] vdd gnd cell_6t
Xbit_r32_c60 bl[60] br[60] wl[32] vdd gnd cell_6t
Xbit_r33_c60 bl[60] br[60] wl[33] vdd gnd cell_6t
Xbit_r34_c60 bl[60] br[60] wl[34] vdd gnd cell_6t
Xbit_r35_c60 bl[60] br[60] wl[35] vdd gnd cell_6t
Xbit_r36_c60 bl[60] br[60] wl[36] vdd gnd cell_6t
Xbit_r37_c60 bl[60] br[60] wl[37] vdd gnd cell_6t
Xbit_r38_c60 bl[60] br[60] wl[38] vdd gnd cell_6t
Xbit_r39_c60 bl[60] br[60] wl[39] vdd gnd cell_6t
Xbit_r40_c60 bl[60] br[60] wl[40] vdd gnd cell_6t
Xbit_r41_c60 bl[60] br[60] wl[41] vdd gnd cell_6t
Xbit_r42_c60 bl[60] br[60] wl[42] vdd gnd cell_6t
Xbit_r43_c60 bl[60] br[60] wl[43] vdd gnd cell_6t
Xbit_r44_c60 bl[60] br[60] wl[44] vdd gnd cell_6t
Xbit_r45_c60 bl[60] br[60] wl[45] vdd gnd cell_6t
Xbit_r46_c60 bl[60] br[60] wl[46] vdd gnd cell_6t
Xbit_r47_c60 bl[60] br[60] wl[47] vdd gnd cell_6t
Xbit_r48_c60 bl[60] br[60] wl[48] vdd gnd cell_6t
Xbit_r49_c60 bl[60] br[60] wl[49] vdd gnd cell_6t
Xbit_r50_c60 bl[60] br[60] wl[50] vdd gnd cell_6t
Xbit_r51_c60 bl[60] br[60] wl[51] vdd gnd cell_6t
Xbit_r52_c60 bl[60] br[60] wl[52] vdd gnd cell_6t
Xbit_r53_c60 bl[60] br[60] wl[53] vdd gnd cell_6t
Xbit_r54_c60 bl[60] br[60] wl[54] vdd gnd cell_6t
Xbit_r55_c60 bl[60] br[60] wl[55] vdd gnd cell_6t
Xbit_r56_c60 bl[60] br[60] wl[56] vdd gnd cell_6t
Xbit_r57_c60 bl[60] br[60] wl[57] vdd gnd cell_6t
Xbit_r58_c60 bl[60] br[60] wl[58] vdd gnd cell_6t
Xbit_r59_c60 bl[60] br[60] wl[59] vdd gnd cell_6t
Xbit_r60_c60 bl[60] br[60] wl[60] vdd gnd cell_6t
Xbit_r61_c60 bl[60] br[60] wl[61] vdd gnd cell_6t
Xbit_r62_c60 bl[60] br[60] wl[62] vdd gnd cell_6t
Xbit_r63_c60 bl[60] br[60] wl[63] vdd gnd cell_6t
Xbit_r0_c61 bl[61] br[61] wl[0] vdd gnd cell_6t
Xbit_r1_c61 bl[61] br[61] wl[1] vdd gnd cell_6t
Xbit_r2_c61 bl[61] br[61] wl[2] vdd gnd cell_6t
Xbit_r3_c61 bl[61] br[61] wl[3] vdd gnd cell_6t
Xbit_r4_c61 bl[61] br[61] wl[4] vdd gnd cell_6t
Xbit_r5_c61 bl[61] br[61] wl[5] vdd gnd cell_6t
Xbit_r6_c61 bl[61] br[61] wl[6] vdd gnd cell_6t
Xbit_r7_c61 bl[61] br[61] wl[7] vdd gnd cell_6t
Xbit_r8_c61 bl[61] br[61] wl[8] vdd gnd cell_6t
Xbit_r9_c61 bl[61] br[61] wl[9] vdd gnd cell_6t
Xbit_r10_c61 bl[61] br[61] wl[10] vdd gnd cell_6t
Xbit_r11_c61 bl[61] br[61] wl[11] vdd gnd cell_6t
Xbit_r12_c61 bl[61] br[61] wl[12] vdd gnd cell_6t
Xbit_r13_c61 bl[61] br[61] wl[13] vdd gnd cell_6t
Xbit_r14_c61 bl[61] br[61] wl[14] vdd gnd cell_6t
Xbit_r15_c61 bl[61] br[61] wl[15] vdd gnd cell_6t
Xbit_r16_c61 bl[61] br[61] wl[16] vdd gnd cell_6t
Xbit_r17_c61 bl[61] br[61] wl[17] vdd gnd cell_6t
Xbit_r18_c61 bl[61] br[61] wl[18] vdd gnd cell_6t
Xbit_r19_c61 bl[61] br[61] wl[19] vdd gnd cell_6t
Xbit_r20_c61 bl[61] br[61] wl[20] vdd gnd cell_6t
Xbit_r21_c61 bl[61] br[61] wl[21] vdd gnd cell_6t
Xbit_r22_c61 bl[61] br[61] wl[22] vdd gnd cell_6t
Xbit_r23_c61 bl[61] br[61] wl[23] vdd gnd cell_6t
Xbit_r24_c61 bl[61] br[61] wl[24] vdd gnd cell_6t
Xbit_r25_c61 bl[61] br[61] wl[25] vdd gnd cell_6t
Xbit_r26_c61 bl[61] br[61] wl[26] vdd gnd cell_6t
Xbit_r27_c61 bl[61] br[61] wl[27] vdd gnd cell_6t
Xbit_r28_c61 bl[61] br[61] wl[28] vdd gnd cell_6t
Xbit_r29_c61 bl[61] br[61] wl[29] vdd gnd cell_6t
Xbit_r30_c61 bl[61] br[61] wl[30] vdd gnd cell_6t
Xbit_r31_c61 bl[61] br[61] wl[31] vdd gnd cell_6t
Xbit_r32_c61 bl[61] br[61] wl[32] vdd gnd cell_6t
Xbit_r33_c61 bl[61] br[61] wl[33] vdd gnd cell_6t
Xbit_r34_c61 bl[61] br[61] wl[34] vdd gnd cell_6t
Xbit_r35_c61 bl[61] br[61] wl[35] vdd gnd cell_6t
Xbit_r36_c61 bl[61] br[61] wl[36] vdd gnd cell_6t
Xbit_r37_c61 bl[61] br[61] wl[37] vdd gnd cell_6t
Xbit_r38_c61 bl[61] br[61] wl[38] vdd gnd cell_6t
Xbit_r39_c61 bl[61] br[61] wl[39] vdd gnd cell_6t
Xbit_r40_c61 bl[61] br[61] wl[40] vdd gnd cell_6t
Xbit_r41_c61 bl[61] br[61] wl[41] vdd gnd cell_6t
Xbit_r42_c61 bl[61] br[61] wl[42] vdd gnd cell_6t
Xbit_r43_c61 bl[61] br[61] wl[43] vdd gnd cell_6t
Xbit_r44_c61 bl[61] br[61] wl[44] vdd gnd cell_6t
Xbit_r45_c61 bl[61] br[61] wl[45] vdd gnd cell_6t
Xbit_r46_c61 bl[61] br[61] wl[46] vdd gnd cell_6t
Xbit_r47_c61 bl[61] br[61] wl[47] vdd gnd cell_6t
Xbit_r48_c61 bl[61] br[61] wl[48] vdd gnd cell_6t
Xbit_r49_c61 bl[61] br[61] wl[49] vdd gnd cell_6t
Xbit_r50_c61 bl[61] br[61] wl[50] vdd gnd cell_6t
Xbit_r51_c61 bl[61] br[61] wl[51] vdd gnd cell_6t
Xbit_r52_c61 bl[61] br[61] wl[52] vdd gnd cell_6t
Xbit_r53_c61 bl[61] br[61] wl[53] vdd gnd cell_6t
Xbit_r54_c61 bl[61] br[61] wl[54] vdd gnd cell_6t
Xbit_r55_c61 bl[61] br[61] wl[55] vdd gnd cell_6t
Xbit_r56_c61 bl[61] br[61] wl[56] vdd gnd cell_6t
Xbit_r57_c61 bl[61] br[61] wl[57] vdd gnd cell_6t
Xbit_r58_c61 bl[61] br[61] wl[58] vdd gnd cell_6t
Xbit_r59_c61 bl[61] br[61] wl[59] vdd gnd cell_6t
Xbit_r60_c61 bl[61] br[61] wl[60] vdd gnd cell_6t
Xbit_r61_c61 bl[61] br[61] wl[61] vdd gnd cell_6t
Xbit_r62_c61 bl[61] br[61] wl[62] vdd gnd cell_6t
Xbit_r63_c61 bl[61] br[61] wl[63] vdd gnd cell_6t
Xbit_r0_c62 bl[62] br[62] wl[0] vdd gnd cell_6t
Xbit_r1_c62 bl[62] br[62] wl[1] vdd gnd cell_6t
Xbit_r2_c62 bl[62] br[62] wl[2] vdd gnd cell_6t
Xbit_r3_c62 bl[62] br[62] wl[3] vdd gnd cell_6t
Xbit_r4_c62 bl[62] br[62] wl[4] vdd gnd cell_6t
Xbit_r5_c62 bl[62] br[62] wl[5] vdd gnd cell_6t
Xbit_r6_c62 bl[62] br[62] wl[6] vdd gnd cell_6t
Xbit_r7_c62 bl[62] br[62] wl[7] vdd gnd cell_6t
Xbit_r8_c62 bl[62] br[62] wl[8] vdd gnd cell_6t
Xbit_r9_c62 bl[62] br[62] wl[9] vdd gnd cell_6t
Xbit_r10_c62 bl[62] br[62] wl[10] vdd gnd cell_6t
Xbit_r11_c62 bl[62] br[62] wl[11] vdd gnd cell_6t
Xbit_r12_c62 bl[62] br[62] wl[12] vdd gnd cell_6t
Xbit_r13_c62 bl[62] br[62] wl[13] vdd gnd cell_6t
Xbit_r14_c62 bl[62] br[62] wl[14] vdd gnd cell_6t
Xbit_r15_c62 bl[62] br[62] wl[15] vdd gnd cell_6t
Xbit_r16_c62 bl[62] br[62] wl[16] vdd gnd cell_6t
Xbit_r17_c62 bl[62] br[62] wl[17] vdd gnd cell_6t
Xbit_r18_c62 bl[62] br[62] wl[18] vdd gnd cell_6t
Xbit_r19_c62 bl[62] br[62] wl[19] vdd gnd cell_6t
Xbit_r20_c62 bl[62] br[62] wl[20] vdd gnd cell_6t
Xbit_r21_c62 bl[62] br[62] wl[21] vdd gnd cell_6t
Xbit_r22_c62 bl[62] br[62] wl[22] vdd gnd cell_6t
Xbit_r23_c62 bl[62] br[62] wl[23] vdd gnd cell_6t
Xbit_r24_c62 bl[62] br[62] wl[24] vdd gnd cell_6t
Xbit_r25_c62 bl[62] br[62] wl[25] vdd gnd cell_6t
Xbit_r26_c62 bl[62] br[62] wl[26] vdd gnd cell_6t
Xbit_r27_c62 bl[62] br[62] wl[27] vdd gnd cell_6t
Xbit_r28_c62 bl[62] br[62] wl[28] vdd gnd cell_6t
Xbit_r29_c62 bl[62] br[62] wl[29] vdd gnd cell_6t
Xbit_r30_c62 bl[62] br[62] wl[30] vdd gnd cell_6t
Xbit_r31_c62 bl[62] br[62] wl[31] vdd gnd cell_6t
Xbit_r32_c62 bl[62] br[62] wl[32] vdd gnd cell_6t
Xbit_r33_c62 bl[62] br[62] wl[33] vdd gnd cell_6t
Xbit_r34_c62 bl[62] br[62] wl[34] vdd gnd cell_6t
Xbit_r35_c62 bl[62] br[62] wl[35] vdd gnd cell_6t
Xbit_r36_c62 bl[62] br[62] wl[36] vdd gnd cell_6t
Xbit_r37_c62 bl[62] br[62] wl[37] vdd gnd cell_6t
Xbit_r38_c62 bl[62] br[62] wl[38] vdd gnd cell_6t
Xbit_r39_c62 bl[62] br[62] wl[39] vdd gnd cell_6t
Xbit_r40_c62 bl[62] br[62] wl[40] vdd gnd cell_6t
Xbit_r41_c62 bl[62] br[62] wl[41] vdd gnd cell_6t
Xbit_r42_c62 bl[62] br[62] wl[42] vdd gnd cell_6t
Xbit_r43_c62 bl[62] br[62] wl[43] vdd gnd cell_6t
Xbit_r44_c62 bl[62] br[62] wl[44] vdd gnd cell_6t
Xbit_r45_c62 bl[62] br[62] wl[45] vdd gnd cell_6t
Xbit_r46_c62 bl[62] br[62] wl[46] vdd gnd cell_6t
Xbit_r47_c62 bl[62] br[62] wl[47] vdd gnd cell_6t
Xbit_r48_c62 bl[62] br[62] wl[48] vdd gnd cell_6t
Xbit_r49_c62 bl[62] br[62] wl[49] vdd gnd cell_6t
Xbit_r50_c62 bl[62] br[62] wl[50] vdd gnd cell_6t
Xbit_r51_c62 bl[62] br[62] wl[51] vdd gnd cell_6t
Xbit_r52_c62 bl[62] br[62] wl[52] vdd gnd cell_6t
Xbit_r53_c62 bl[62] br[62] wl[53] vdd gnd cell_6t
Xbit_r54_c62 bl[62] br[62] wl[54] vdd gnd cell_6t
Xbit_r55_c62 bl[62] br[62] wl[55] vdd gnd cell_6t
Xbit_r56_c62 bl[62] br[62] wl[56] vdd gnd cell_6t
Xbit_r57_c62 bl[62] br[62] wl[57] vdd gnd cell_6t
Xbit_r58_c62 bl[62] br[62] wl[58] vdd gnd cell_6t
Xbit_r59_c62 bl[62] br[62] wl[59] vdd gnd cell_6t
Xbit_r60_c62 bl[62] br[62] wl[60] vdd gnd cell_6t
Xbit_r61_c62 bl[62] br[62] wl[61] vdd gnd cell_6t
Xbit_r62_c62 bl[62] br[62] wl[62] vdd gnd cell_6t
Xbit_r63_c62 bl[62] br[62] wl[63] vdd gnd cell_6t
Xbit_r0_c63 bl[63] br[63] wl[0] vdd gnd cell_6t
Xbit_r1_c63 bl[63] br[63] wl[1] vdd gnd cell_6t
Xbit_r2_c63 bl[63] br[63] wl[2] vdd gnd cell_6t
Xbit_r3_c63 bl[63] br[63] wl[3] vdd gnd cell_6t
Xbit_r4_c63 bl[63] br[63] wl[4] vdd gnd cell_6t
Xbit_r5_c63 bl[63] br[63] wl[5] vdd gnd cell_6t
Xbit_r6_c63 bl[63] br[63] wl[6] vdd gnd cell_6t
Xbit_r7_c63 bl[63] br[63] wl[7] vdd gnd cell_6t
Xbit_r8_c63 bl[63] br[63] wl[8] vdd gnd cell_6t
Xbit_r9_c63 bl[63] br[63] wl[9] vdd gnd cell_6t
Xbit_r10_c63 bl[63] br[63] wl[10] vdd gnd cell_6t
Xbit_r11_c63 bl[63] br[63] wl[11] vdd gnd cell_6t
Xbit_r12_c63 bl[63] br[63] wl[12] vdd gnd cell_6t
Xbit_r13_c63 bl[63] br[63] wl[13] vdd gnd cell_6t
Xbit_r14_c63 bl[63] br[63] wl[14] vdd gnd cell_6t
Xbit_r15_c63 bl[63] br[63] wl[15] vdd gnd cell_6t
Xbit_r16_c63 bl[63] br[63] wl[16] vdd gnd cell_6t
Xbit_r17_c63 bl[63] br[63] wl[17] vdd gnd cell_6t
Xbit_r18_c63 bl[63] br[63] wl[18] vdd gnd cell_6t
Xbit_r19_c63 bl[63] br[63] wl[19] vdd gnd cell_6t
Xbit_r20_c63 bl[63] br[63] wl[20] vdd gnd cell_6t
Xbit_r21_c63 bl[63] br[63] wl[21] vdd gnd cell_6t
Xbit_r22_c63 bl[63] br[63] wl[22] vdd gnd cell_6t
Xbit_r23_c63 bl[63] br[63] wl[23] vdd gnd cell_6t
Xbit_r24_c63 bl[63] br[63] wl[24] vdd gnd cell_6t
Xbit_r25_c63 bl[63] br[63] wl[25] vdd gnd cell_6t
Xbit_r26_c63 bl[63] br[63] wl[26] vdd gnd cell_6t
Xbit_r27_c63 bl[63] br[63] wl[27] vdd gnd cell_6t
Xbit_r28_c63 bl[63] br[63] wl[28] vdd gnd cell_6t
Xbit_r29_c63 bl[63] br[63] wl[29] vdd gnd cell_6t
Xbit_r30_c63 bl[63] br[63] wl[30] vdd gnd cell_6t
Xbit_r31_c63 bl[63] br[63] wl[31] vdd gnd cell_6t
Xbit_r32_c63 bl[63] br[63] wl[32] vdd gnd cell_6t
Xbit_r33_c63 bl[63] br[63] wl[33] vdd gnd cell_6t
Xbit_r34_c63 bl[63] br[63] wl[34] vdd gnd cell_6t
Xbit_r35_c63 bl[63] br[63] wl[35] vdd gnd cell_6t
Xbit_r36_c63 bl[63] br[63] wl[36] vdd gnd cell_6t
Xbit_r37_c63 bl[63] br[63] wl[37] vdd gnd cell_6t
Xbit_r38_c63 bl[63] br[63] wl[38] vdd gnd cell_6t
Xbit_r39_c63 bl[63] br[63] wl[39] vdd gnd cell_6t
Xbit_r40_c63 bl[63] br[63] wl[40] vdd gnd cell_6t
Xbit_r41_c63 bl[63] br[63] wl[41] vdd gnd cell_6t
Xbit_r42_c63 bl[63] br[63] wl[42] vdd gnd cell_6t
Xbit_r43_c63 bl[63] br[63] wl[43] vdd gnd cell_6t
Xbit_r44_c63 bl[63] br[63] wl[44] vdd gnd cell_6t
Xbit_r45_c63 bl[63] br[63] wl[45] vdd gnd cell_6t
Xbit_r46_c63 bl[63] br[63] wl[46] vdd gnd cell_6t
Xbit_r47_c63 bl[63] br[63] wl[47] vdd gnd cell_6t
Xbit_r48_c63 bl[63] br[63] wl[48] vdd gnd cell_6t
Xbit_r49_c63 bl[63] br[63] wl[49] vdd gnd cell_6t
Xbit_r50_c63 bl[63] br[63] wl[50] vdd gnd cell_6t
Xbit_r51_c63 bl[63] br[63] wl[51] vdd gnd cell_6t
Xbit_r52_c63 bl[63] br[63] wl[52] vdd gnd cell_6t
Xbit_r53_c63 bl[63] br[63] wl[53] vdd gnd cell_6t
Xbit_r54_c63 bl[63] br[63] wl[54] vdd gnd cell_6t
Xbit_r55_c63 bl[63] br[63] wl[55] vdd gnd cell_6t
Xbit_r56_c63 bl[63] br[63] wl[56] vdd gnd cell_6t
Xbit_r57_c63 bl[63] br[63] wl[57] vdd gnd cell_6t
Xbit_r58_c63 bl[63] br[63] wl[58] vdd gnd cell_6t
Xbit_r59_c63 bl[63] br[63] wl[59] vdd gnd cell_6t
Xbit_r60_c63 bl[63] br[63] wl[60] vdd gnd cell_6t
Xbit_r61_c63 bl[63] br[63] wl[61] vdd gnd cell_6t
Xbit_r62_c63 bl[63] br[63] wl[62] vdd gnd cell_6t
Xbit_r63_c63 bl[63] br[63] wl[63] vdd gnd cell_6t
Xbit_r0_c64 bl[64] br[64] wl[0] vdd gnd cell_6t
Xbit_r1_c64 bl[64] br[64] wl[1] vdd gnd cell_6t
Xbit_r2_c64 bl[64] br[64] wl[2] vdd gnd cell_6t
Xbit_r3_c64 bl[64] br[64] wl[3] vdd gnd cell_6t
Xbit_r4_c64 bl[64] br[64] wl[4] vdd gnd cell_6t
Xbit_r5_c64 bl[64] br[64] wl[5] vdd gnd cell_6t
Xbit_r6_c64 bl[64] br[64] wl[6] vdd gnd cell_6t
Xbit_r7_c64 bl[64] br[64] wl[7] vdd gnd cell_6t
Xbit_r8_c64 bl[64] br[64] wl[8] vdd gnd cell_6t
Xbit_r9_c64 bl[64] br[64] wl[9] vdd gnd cell_6t
Xbit_r10_c64 bl[64] br[64] wl[10] vdd gnd cell_6t
Xbit_r11_c64 bl[64] br[64] wl[11] vdd gnd cell_6t
Xbit_r12_c64 bl[64] br[64] wl[12] vdd gnd cell_6t
Xbit_r13_c64 bl[64] br[64] wl[13] vdd gnd cell_6t
Xbit_r14_c64 bl[64] br[64] wl[14] vdd gnd cell_6t
Xbit_r15_c64 bl[64] br[64] wl[15] vdd gnd cell_6t
Xbit_r16_c64 bl[64] br[64] wl[16] vdd gnd cell_6t
Xbit_r17_c64 bl[64] br[64] wl[17] vdd gnd cell_6t
Xbit_r18_c64 bl[64] br[64] wl[18] vdd gnd cell_6t
Xbit_r19_c64 bl[64] br[64] wl[19] vdd gnd cell_6t
Xbit_r20_c64 bl[64] br[64] wl[20] vdd gnd cell_6t
Xbit_r21_c64 bl[64] br[64] wl[21] vdd gnd cell_6t
Xbit_r22_c64 bl[64] br[64] wl[22] vdd gnd cell_6t
Xbit_r23_c64 bl[64] br[64] wl[23] vdd gnd cell_6t
Xbit_r24_c64 bl[64] br[64] wl[24] vdd gnd cell_6t
Xbit_r25_c64 bl[64] br[64] wl[25] vdd gnd cell_6t
Xbit_r26_c64 bl[64] br[64] wl[26] vdd gnd cell_6t
Xbit_r27_c64 bl[64] br[64] wl[27] vdd gnd cell_6t
Xbit_r28_c64 bl[64] br[64] wl[28] vdd gnd cell_6t
Xbit_r29_c64 bl[64] br[64] wl[29] vdd gnd cell_6t
Xbit_r30_c64 bl[64] br[64] wl[30] vdd gnd cell_6t
Xbit_r31_c64 bl[64] br[64] wl[31] vdd gnd cell_6t
Xbit_r32_c64 bl[64] br[64] wl[32] vdd gnd cell_6t
Xbit_r33_c64 bl[64] br[64] wl[33] vdd gnd cell_6t
Xbit_r34_c64 bl[64] br[64] wl[34] vdd gnd cell_6t
Xbit_r35_c64 bl[64] br[64] wl[35] vdd gnd cell_6t
Xbit_r36_c64 bl[64] br[64] wl[36] vdd gnd cell_6t
Xbit_r37_c64 bl[64] br[64] wl[37] vdd gnd cell_6t
Xbit_r38_c64 bl[64] br[64] wl[38] vdd gnd cell_6t
Xbit_r39_c64 bl[64] br[64] wl[39] vdd gnd cell_6t
Xbit_r40_c64 bl[64] br[64] wl[40] vdd gnd cell_6t
Xbit_r41_c64 bl[64] br[64] wl[41] vdd gnd cell_6t
Xbit_r42_c64 bl[64] br[64] wl[42] vdd gnd cell_6t
Xbit_r43_c64 bl[64] br[64] wl[43] vdd gnd cell_6t
Xbit_r44_c64 bl[64] br[64] wl[44] vdd gnd cell_6t
Xbit_r45_c64 bl[64] br[64] wl[45] vdd gnd cell_6t
Xbit_r46_c64 bl[64] br[64] wl[46] vdd gnd cell_6t
Xbit_r47_c64 bl[64] br[64] wl[47] vdd gnd cell_6t
Xbit_r48_c64 bl[64] br[64] wl[48] vdd gnd cell_6t
Xbit_r49_c64 bl[64] br[64] wl[49] vdd gnd cell_6t
Xbit_r50_c64 bl[64] br[64] wl[50] vdd gnd cell_6t
Xbit_r51_c64 bl[64] br[64] wl[51] vdd gnd cell_6t
Xbit_r52_c64 bl[64] br[64] wl[52] vdd gnd cell_6t
Xbit_r53_c64 bl[64] br[64] wl[53] vdd gnd cell_6t
Xbit_r54_c64 bl[64] br[64] wl[54] vdd gnd cell_6t
Xbit_r55_c64 bl[64] br[64] wl[55] vdd gnd cell_6t
Xbit_r56_c64 bl[64] br[64] wl[56] vdd gnd cell_6t
Xbit_r57_c64 bl[64] br[64] wl[57] vdd gnd cell_6t
Xbit_r58_c64 bl[64] br[64] wl[58] vdd gnd cell_6t
Xbit_r59_c64 bl[64] br[64] wl[59] vdd gnd cell_6t
Xbit_r60_c64 bl[64] br[64] wl[60] vdd gnd cell_6t
Xbit_r61_c64 bl[64] br[64] wl[61] vdd gnd cell_6t
Xbit_r62_c64 bl[64] br[64] wl[62] vdd gnd cell_6t
Xbit_r63_c64 bl[64] br[64] wl[63] vdd gnd cell_6t
Xbit_r0_c65 bl[65] br[65] wl[0] vdd gnd cell_6t
Xbit_r1_c65 bl[65] br[65] wl[1] vdd gnd cell_6t
Xbit_r2_c65 bl[65] br[65] wl[2] vdd gnd cell_6t
Xbit_r3_c65 bl[65] br[65] wl[3] vdd gnd cell_6t
Xbit_r4_c65 bl[65] br[65] wl[4] vdd gnd cell_6t
Xbit_r5_c65 bl[65] br[65] wl[5] vdd gnd cell_6t
Xbit_r6_c65 bl[65] br[65] wl[6] vdd gnd cell_6t
Xbit_r7_c65 bl[65] br[65] wl[7] vdd gnd cell_6t
Xbit_r8_c65 bl[65] br[65] wl[8] vdd gnd cell_6t
Xbit_r9_c65 bl[65] br[65] wl[9] vdd gnd cell_6t
Xbit_r10_c65 bl[65] br[65] wl[10] vdd gnd cell_6t
Xbit_r11_c65 bl[65] br[65] wl[11] vdd gnd cell_6t
Xbit_r12_c65 bl[65] br[65] wl[12] vdd gnd cell_6t
Xbit_r13_c65 bl[65] br[65] wl[13] vdd gnd cell_6t
Xbit_r14_c65 bl[65] br[65] wl[14] vdd gnd cell_6t
Xbit_r15_c65 bl[65] br[65] wl[15] vdd gnd cell_6t
Xbit_r16_c65 bl[65] br[65] wl[16] vdd gnd cell_6t
Xbit_r17_c65 bl[65] br[65] wl[17] vdd gnd cell_6t
Xbit_r18_c65 bl[65] br[65] wl[18] vdd gnd cell_6t
Xbit_r19_c65 bl[65] br[65] wl[19] vdd gnd cell_6t
Xbit_r20_c65 bl[65] br[65] wl[20] vdd gnd cell_6t
Xbit_r21_c65 bl[65] br[65] wl[21] vdd gnd cell_6t
Xbit_r22_c65 bl[65] br[65] wl[22] vdd gnd cell_6t
Xbit_r23_c65 bl[65] br[65] wl[23] vdd gnd cell_6t
Xbit_r24_c65 bl[65] br[65] wl[24] vdd gnd cell_6t
Xbit_r25_c65 bl[65] br[65] wl[25] vdd gnd cell_6t
Xbit_r26_c65 bl[65] br[65] wl[26] vdd gnd cell_6t
Xbit_r27_c65 bl[65] br[65] wl[27] vdd gnd cell_6t
Xbit_r28_c65 bl[65] br[65] wl[28] vdd gnd cell_6t
Xbit_r29_c65 bl[65] br[65] wl[29] vdd gnd cell_6t
Xbit_r30_c65 bl[65] br[65] wl[30] vdd gnd cell_6t
Xbit_r31_c65 bl[65] br[65] wl[31] vdd gnd cell_6t
Xbit_r32_c65 bl[65] br[65] wl[32] vdd gnd cell_6t
Xbit_r33_c65 bl[65] br[65] wl[33] vdd gnd cell_6t
Xbit_r34_c65 bl[65] br[65] wl[34] vdd gnd cell_6t
Xbit_r35_c65 bl[65] br[65] wl[35] vdd gnd cell_6t
Xbit_r36_c65 bl[65] br[65] wl[36] vdd gnd cell_6t
Xbit_r37_c65 bl[65] br[65] wl[37] vdd gnd cell_6t
Xbit_r38_c65 bl[65] br[65] wl[38] vdd gnd cell_6t
Xbit_r39_c65 bl[65] br[65] wl[39] vdd gnd cell_6t
Xbit_r40_c65 bl[65] br[65] wl[40] vdd gnd cell_6t
Xbit_r41_c65 bl[65] br[65] wl[41] vdd gnd cell_6t
Xbit_r42_c65 bl[65] br[65] wl[42] vdd gnd cell_6t
Xbit_r43_c65 bl[65] br[65] wl[43] vdd gnd cell_6t
Xbit_r44_c65 bl[65] br[65] wl[44] vdd gnd cell_6t
Xbit_r45_c65 bl[65] br[65] wl[45] vdd gnd cell_6t
Xbit_r46_c65 bl[65] br[65] wl[46] vdd gnd cell_6t
Xbit_r47_c65 bl[65] br[65] wl[47] vdd gnd cell_6t
Xbit_r48_c65 bl[65] br[65] wl[48] vdd gnd cell_6t
Xbit_r49_c65 bl[65] br[65] wl[49] vdd gnd cell_6t
Xbit_r50_c65 bl[65] br[65] wl[50] vdd gnd cell_6t
Xbit_r51_c65 bl[65] br[65] wl[51] vdd gnd cell_6t
Xbit_r52_c65 bl[65] br[65] wl[52] vdd gnd cell_6t
Xbit_r53_c65 bl[65] br[65] wl[53] vdd gnd cell_6t
Xbit_r54_c65 bl[65] br[65] wl[54] vdd gnd cell_6t
Xbit_r55_c65 bl[65] br[65] wl[55] vdd gnd cell_6t
Xbit_r56_c65 bl[65] br[65] wl[56] vdd gnd cell_6t
Xbit_r57_c65 bl[65] br[65] wl[57] vdd gnd cell_6t
Xbit_r58_c65 bl[65] br[65] wl[58] vdd gnd cell_6t
Xbit_r59_c65 bl[65] br[65] wl[59] vdd gnd cell_6t
Xbit_r60_c65 bl[65] br[65] wl[60] vdd gnd cell_6t
Xbit_r61_c65 bl[65] br[65] wl[61] vdd gnd cell_6t
Xbit_r62_c65 bl[65] br[65] wl[62] vdd gnd cell_6t
Xbit_r63_c65 bl[65] br[65] wl[63] vdd gnd cell_6t
Xbit_r0_c66 bl[66] br[66] wl[0] vdd gnd cell_6t
Xbit_r1_c66 bl[66] br[66] wl[1] vdd gnd cell_6t
Xbit_r2_c66 bl[66] br[66] wl[2] vdd gnd cell_6t
Xbit_r3_c66 bl[66] br[66] wl[3] vdd gnd cell_6t
Xbit_r4_c66 bl[66] br[66] wl[4] vdd gnd cell_6t
Xbit_r5_c66 bl[66] br[66] wl[5] vdd gnd cell_6t
Xbit_r6_c66 bl[66] br[66] wl[6] vdd gnd cell_6t
Xbit_r7_c66 bl[66] br[66] wl[7] vdd gnd cell_6t
Xbit_r8_c66 bl[66] br[66] wl[8] vdd gnd cell_6t
Xbit_r9_c66 bl[66] br[66] wl[9] vdd gnd cell_6t
Xbit_r10_c66 bl[66] br[66] wl[10] vdd gnd cell_6t
Xbit_r11_c66 bl[66] br[66] wl[11] vdd gnd cell_6t
Xbit_r12_c66 bl[66] br[66] wl[12] vdd gnd cell_6t
Xbit_r13_c66 bl[66] br[66] wl[13] vdd gnd cell_6t
Xbit_r14_c66 bl[66] br[66] wl[14] vdd gnd cell_6t
Xbit_r15_c66 bl[66] br[66] wl[15] vdd gnd cell_6t
Xbit_r16_c66 bl[66] br[66] wl[16] vdd gnd cell_6t
Xbit_r17_c66 bl[66] br[66] wl[17] vdd gnd cell_6t
Xbit_r18_c66 bl[66] br[66] wl[18] vdd gnd cell_6t
Xbit_r19_c66 bl[66] br[66] wl[19] vdd gnd cell_6t
Xbit_r20_c66 bl[66] br[66] wl[20] vdd gnd cell_6t
Xbit_r21_c66 bl[66] br[66] wl[21] vdd gnd cell_6t
Xbit_r22_c66 bl[66] br[66] wl[22] vdd gnd cell_6t
Xbit_r23_c66 bl[66] br[66] wl[23] vdd gnd cell_6t
Xbit_r24_c66 bl[66] br[66] wl[24] vdd gnd cell_6t
Xbit_r25_c66 bl[66] br[66] wl[25] vdd gnd cell_6t
Xbit_r26_c66 bl[66] br[66] wl[26] vdd gnd cell_6t
Xbit_r27_c66 bl[66] br[66] wl[27] vdd gnd cell_6t
Xbit_r28_c66 bl[66] br[66] wl[28] vdd gnd cell_6t
Xbit_r29_c66 bl[66] br[66] wl[29] vdd gnd cell_6t
Xbit_r30_c66 bl[66] br[66] wl[30] vdd gnd cell_6t
Xbit_r31_c66 bl[66] br[66] wl[31] vdd gnd cell_6t
Xbit_r32_c66 bl[66] br[66] wl[32] vdd gnd cell_6t
Xbit_r33_c66 bl[66] br[66] wl[33] vdd gnd cell_6t
Xbit_r34_c66 bl[66] br[66] wl[34] vdd gnd cell_6t
Xbit_r35_c66 bl[66] br[66] wl[35] vdd gnd cell_6t
Xbit_r36_c66 bl[66] br[66] wl[36] vdd gnd cell_6t
Xbit_r37_c66 bl[66] br[66] wl[37] vdd gnd cell_6t
Xbit_r38_c66 bl[66] br[66] wl[38] vdd gnd cell_6t
Xbit_r39_c66 bl[66] br[66] wl[39] vdd gnd cell_6t
Xbit_r40_c66 bl[66] br[66] wl[40] vdd gnd cell_6t
Xbit_r41_c66 bl[66] br[66] wl[41] vdd gnd cell_6t
Xbit_r42_c66 bl[66] br[66] wl[42] vdd gnd cell_6t
Xbit_r43_c66 bl[66] br[66] wl[43] vdd gnd cell_6t
Xbit_r44_c66 bl[66] br[66] wl[44] vdd gnd cell_6t
Xbit_r45_c66 bl[66] br[66] wl[45] vdd gnd cell_6t
Xbit_r46_c66 bl[66] br[66] wl[46] vdd gnd cell_6t
Xbit_r47_c66 bl[66] br[66] wl[47] vdd gnd cell_6t
Xbit_r48_c66 bl[66] br[66] wl[48] vdd gnd cell_6t
Xbit_r49_c66 bl[66] br[66] wl[49] vdd gnd cell_6t
Xbit_r50_c66 bl[66] br[66] wl[50] vdd gnd cell_6t
Xbit_r51_c66 bl[66] br[66] wl[51] vdd gnd cell_6t
Xbit_r52_c66 bl[66] br[66] wl[52] vdd gnd cell_6t
Xbit_r53_c66 bl[66] br[66] wl[53] vdd gnd cell_6t
Xbit_r54_c66 bl[66] br[66] wl[54] vdd gnd cell_6t
Xbit_r55_c66 bl[66] br[66] wl[55] vdd gnd cell_6t
Xbit_r56_c66 bl[66] br[66] wl[56] vdd gnd cell_6t
Xbit_r57_c66 bl[66] br[66] wl[57] vdd gnd cell_6t
Xbit_r58_c66 bl[66] br[66] wl[58] vdd gnd cell_6t
Xbit_r59_c66 bl[66] br[66] wl[59] vdd gnd cell_6t
Xbit_r60_c66 bl[66] br[66] wl[60] vdd gnd cell_6t
Xbit_r61_c66 bl[66] br[66] wl[61] vdd gnd cell_6t
Xbit_r62_c66 bl[66] br[66] wl[62] vdd gnd cell_6t
Xbit_r63_c66 bl[66] br[66] wl[63] vdd gnd cell_6t
Xbit_r0_c67 bl[67] br[67] wl[0] vdd gnd cell_6t
Xbit_r1_c67 bl[67] br[67] wl[1] vdd gnd cell_6t
Xbit_r2_c67 bl[67] br[67] wl[2] vdd gnd cell_6t
Xbit_r3_c67 bl[67] br[67] wl[3] vdd gnd cell_6t
Xbit_r4_c67 bl[67] br[67] wl[4] vdd gnd cell_6t
Xbit_r5_c67 bl[67] br[67] wl[5] vdd gnd cell_6t
Xbit_r6_c67 bl[67] br[67] wl[6] vdd gnd cell_6t
Xbit_r7_c67 bl[67] br[67] wl[7] vdd gnd cell_6t
Xbit_r8_c67 bl[67] br[67] wl[8] vdd gnd cell_6t
Xbit_r9_c67 bl[67] br[67] wl[9] vdd gnd cell_6t
Xbit_r10_c67 bl[67] br[67] wl[10] vdd gnd cell_6t
Xbit_r11_c67 bl[67] br[67] wl[11] vdd gnd cell_6t
Xbit_r12_c67 bl[67] br[67] wl[12] vdd gnd cell_6t
Xbit_r13_c67 bl[67] br[67] wl[13] vdd gnd cell_6t
Xbit_r14_c67 bl[67] br[67] wl[14] vdd gnd cell_6t
Xbit_r15_c67 bl[67] br[67] wl[15] vdd gnd cell_6t
Xbit_r16_c67 bl[67] br[67] wl[16] vdd gnd cell_6t
Xbit_r17_c67 bl[67] br[67] wl[17] vdd gnd cell_6t
Xbit_r18_c67 bl[67] br[67] wl[18] vdd gnd cell_6t
Xbit_r19_c67 bl[67] br[67] wl[19] vdd gnd cell_6t
Xbit_r20_c67 bl[67] br[67] wl[20] vdd gnd cell_6t
Xbit_r21_c67 bl[67] br[67] wl[21] vdd gnd cell_6t
Xbit_r22_c67 bl[67] br[67] wl[22] vdd gnd cell_6t
Xbit_r23_c67 bl[67] br[67] wl[23] vdd gnd cell_6t
Xbit_r24_c67 bl[67] br[67] wl[24] vdd gnd cell_6t
Xbit_r25_c67 bl[67] br[67] wl[25] vdd gnd cell_6t
Xbit_r26_c67 bl[67] br[67] wl[26] vdd gnd cell_6t
Xbit_r27_c67 bl[67] br[67] wl[27] vdd gnd cell_6t
Xbit_r28_c67 bl[67] br[67] wl[28] vdd gnd cell_6t
Xbit_r29_c67 bl[67] br[67] wl[29] vdd gnd cell_6t
Xbit_r30_c67 bl[67] br[67] wl[30] vdd gnd cell_6t
Xbit_r31_c67 bl[67] br[67] wl[31] vdd gnd cell_6t
Xbit_r32_c67 bl[67] br[67] wl[32] vdd gnd cell_6t
Xbit_r33_c67 bl[67] br[67] wl[33] vdd gnd cell_6t
Xbit_r34_c67 bl[67] br[67] wl[34] vdd gnd cell_6t
Xbit_r35_c67 bl[67] br[67] wl[35] vdd gnd cell_6t
Xbit_r36_c67 bl[67] br[67] wl[36] vdd gnd cell_6t
Xbit_r37_c67 bl[67] br[67] wl[37] vdd gnd cell_6t
Xbit_r38_c67 bl[67] br[67] wl[38] vdd gnd cell_6t
Xbit_r39_c67 bl[67] br[67] wl[39] vdd gnd cell_6t
Xbit_r40_c67 bl[67] br[67] wl[40] vdd gnd cell_6t
Xbit_r41_c67 bl[67] br[67] wl[41] vdd gnd cell_6t
Xbit_r42_c67 bl[67] br[67] wl[42] vdd gnd cell_6t
Xbit_r43_c67 bl[67] br[67] wl[43] vdd gnd cell_6t
Xbit_r44_c67 bl[67] br[67] wl[44] vdd gnd cell_6t
Xbit_r45_c67 bl[67] br[67] wl[45] vdd gnd cell_6t
Xbit_r46_c67 bl[67] br[67] wl[46] vdd gnd cell_6t
Xbit_r47_c67 bl[67] br[67] wl[47] vdd gnd cell_6t
Xbit_r48_c67 bl[67] br[67] wl[48] vdd gnd cell_6t
Xbit_r49_c67 bl[67] br[67] wl[49] vdd gnd cell_6t
Xbit_r50_c67 bl[67] br[67] wl[50] vdd gnd cell_6t
Xbit_r51_c67 bl[67] br[67] wl[51] vdd gnd cell_6t
Xbit_r52_c67 bl[67] br[67] wl[52] vdd gnd cell_6t
Xbit_r53_c67 bl[67] br[67] wl[53] vdd gnd cell_6t
Xbit_r54_c67 bl[67] br[67] wl[54] vdd gnd cell_6t
Xbit_r55_c67 bl[67] br[67] wl[55] vdd gnd cell_6t
Xbit_r56_c67 bl[67] br[67] wl[56] vdd gnd cell_6t
Xbit_r57_c67 bl[67] br[67] wl[57] vdd gnd cell_6t
Xbit_r58_c67 bl[67] br[67] wl[58] vdd gnd cell_6t
Xbit_r59_c67 bl[67] br[67] wl[59] vdd gnd cell_6t
Xbit_r60_c67 bl[67] br[67] wl[60] vdd gnd cell_6t
Xbit_r61_c67 bl[67] br[67] wl[61] vdd gnd cell_6t
Xbit_r62_c67 bl[67] br[67] wl[62] vdd gnd cell_6t
Xbit_r63_c67 bl[67] br[67] wl[63] vdd gnd cell_6t
Xbit_r0_c68 bl[68] br[68] wl[0] vdd gnd cell_6t
Xbit_r1_c68 bl[68] br[68] wl[1] vdd gnd cell_6t
Xbit_r2_c68 bl[68] br[68] wl[2] vdd gnd cell_6t
Xbit_r3_c68 bl[68] br[68] wl[3] vdd gnd cell_6t
Xbit_r4_c68 bl[68] br[68] wl[4] vdd gnd cell_6t
Xbit_r5_c68 bl[68] br[68] wl[5] vdd gnd cell_6t
Xbit_r6_c68 bl[68] br[68] wl[6] vdd gnd cell_6t
Xbit_r7_c68 bl[68] br[68] wl[7] vdd gnd cell_6t
Xbit_r8_c68 bl[68] br[68] wl[8] vdd gnd cell_6t
Xbit_r9_c68 bl[68] br[68] wl[9] vdd gnd cell_6t
Xbit_r10_c68 bl[68] br[68] wl[10] vdd gnd cell_6t
Xbit_r11_c68 bl[68] br[68] wl[11] vdd gnd cell_6t
Xbit_r12_c68 bl[68] br[68] wl[12] vdd gnd cell_6t
Xbit_r13_c68 bl[68] br[68] wl[13] vdd gnd cell_6t
Xbit_r14_c68 bl[68] br[68] wl[14] vdd gnd cell_6t
Xbit_r15_c68 bl[68] br[68] wl[15] vdd gnd cell_6t
Xbit_r16_c68 bl[68] br[68] wl[16] vdd gnd cell_6t
Xbit_r17_c68 bl[68] br[68] wl[17] vdd gnd cell_6t
Xbit_r18_c68 bl[68] br[68] wl[18] vdd gnd cell_6t
Xbit_r19_c68 bl[68] br[68] wl[19] vdd gnd cell_6t
Xbit_r20_c68 bl[68] br[68] wl[20] vdd gnd cell_6t
Xbit_r21_c68 bl[68] br[68] wl[21] vdd gnd cell_6t
Xbit_r22_c68 bl[68] br[68] wl[22] vdd gnd cell_6t
Xbit_r23_c68 bl[68] br[68] wl[23] vdd gnd cell_6t
Xbit_r24_c68 bl[68] br[68] wl[24] vdd gnd cell_6t
Xbit_r25_c68 bl[68] br[68] wl[25] vdd gnd cell_6t
Xbit_r26_c68 bl[68] br[68] wl[26] vdd gnd cell_6t
Xbit_r27_c68 bl[68] br[68] wl[27] vdd gnd cell_6t
Xbit_r28_c68 bl[68] br[68] wl[28] vdd gnd cell_6t
Xbit_r29_c68 bl[68] br[68] wl[29] vdd gnd cell_6t
Xbit_r30_c68 bl[68] br[68] wl[30] vdd gnd cell_6t
Xbit_r31_c68 bl[68] br[68] wl[31] vdd gnd cell_6t
Xbit_r32_c68 bl[68] br[68] wl[32] vdd gnd cell_6t
Xbit_r33_c68 bl[68] br[68] wl[33] vdd gnd cell_6t
Xbit_r34_c68 bl[68] br[68] wl[34] vdd gnd cell_6t
Xbit_r35_c68 bl[68] br[68] wl[35] vdd gnd cell_6t
Xbit_r36_c68 bl[68] br[68] wl[36] vdd gnd cell_6t
Xbit_r37_c68 bl[68] br[68] wl[37] vdd gnd cell_6t
Xbit_r38_c68 bl[68] br[68] wl[38] vdd gnd cell_6t
Xbit_r39_c68 bl[68] br[68] wl[39] vdd gnd cell_6t
Xbit_r40_c68 bl[68] br[68] wl[40] vdd gnd cell_6t
Xbit_r41_c68 bl[68] br[68] wl[41] vdd gnd cell_6t
Xbit_r42_c68 bl[68] br[68] wl[42] vdd gnd cell_6t
Xbit_r43_c68 bl[68] br[68] wl[43] vdd gnd cell_6t
Xbit_r44_c68 bl[68] br[68] wl[44] vdd gnd cell_6t
Xbit_r45_c68 bl[68] br[68] wl[45] vdd gnd cell_6t
Xbit_r46_c68 bl[68] br[68] wl[46] vdd gnd cell_6t
Xbit_r47_c68 bl[68] br[68] wl[47] vdd gnd cell_6t
Xbit_r48_c68 bl[68] br[68] wl[48] vdd gnd cell_6t
Xbit_r49_c68 bl[68] br[68] wl[49] vdd gnd cell_6t
Xbit_r50_c68 bl[68] br[68] wl[50] vdd gnd cell_6t
Xbit_r51_c68 bl[68] br[68] wl[51] vdd gnd cell_6t
Xbit_r52_c68 bl[68] br[68] wl[52] vdd gnd cell_6t
Xbit_r53_c68 bl[68] br[68] wl[53] vdd gnd cell_6t
Xbit_r54_c68 bl[68] br[68] wl[54] vdd gnd cell_6t
Xbit_r55_c68 bl[68] br[68] wl[55] vdd gnd cell_6t
Xbit_r56_c68 bl[68] br[68] wl[56] vdd gnd cell_6t
Xbit_r57_c68 bl[68] br[68] wl[57] vdd gnd cell_6t
Xbit_r58_c68 bl[68] br[68] wl[58] vdd gnd cell_6t
Xbit_r59_c68 bl[68] br[68] wl[59] vdd gnd cell_6t
Xbit_r60_c68 bl[68] br[68] wl[60] vdd gnd cell_6t
Xbit_r61_c68 bl[68] br[68] wl[61] vdd gnd cell_6t
Xbit_r62_c68 bl[68] br[68] wl[62] vdd gnd cell_6t
Xbit_r63_c68 bl[68] br[68] wl[63] vdd gnd cell_6t
Xbit_r0_c69 bl[69] br[69] wl[0] vdd gnd cell_6t
Xbit_r1_c69 bl[69] br[69] wl[1] vdd gnd cell_6t
Xbit_r2_c69 bl[69] br[69] wl[2] vdd gnd cell_6t
Xbit_r3_c69 bl[69] br[69] wl[3] vdd gnd cell_6t
Xbit_r4_c69 bl[69] br[69] wl[4] vdd gnd cell_6t
Xbit_r5_c69 bl[69] br[69] wl[5] vdd gnd cell_6t
Xbit_r6_c69 bl[69] br[69] wl[6] vdd gnd cell_6t
Xbit_r7_c69 bl[69] br[69] wl[7] vdd gnd cell_6t
Xbit_r8_c69 bl[69] br[69] wl[8] vdd gnd cell_6t
Xbit_r9_c69 bl[69] br[69] wl[9] vdd gnd cell_6t
Xbit_r10_c69 bl[69] br[69] wl[10] vdd gnd cell_6t
Xbit_r11_c69 bl[69] br[69] wl[11] vdd gnd cell_6t
Xbit_r12_c69 bl[69] br[69] wl[12] vdd gnd cell_6t
Xbit_r13_c69 bl[69] br[69] wl[13] vdd gnd cell_6t
Xbit_r14_c69 bl[69] br[69] wl[14] vdd gnd cell_6t
Xbit_r15_c69 bl[69] br[69] wl[15] vdd gnd cell_6t
Xbit_r16_c69 bl[69] br[69] wl[16] vdd gnd cell_6t
Xbit_r17_c69 bl[69] br[69] wl[17] vdd gnd cell_6t
Xbit_r18_c69 bl[69] br[69] wl[18] vdd gnd cell_6t
Xbit_r19_c69 bl[69] br[69] wl[19] vdd gnd cell_6t
Xbit_r20_c69 bl[69] br[69] wl[20] vdd gnd cell_6t
Xbit_r21_c69 bl[69] br[69] wl[21] vdd gnd cell_6t
Xbit_r22_c69 bl[69] br[69] wl[22] vdd gnd cell_6t
Xbit_r23_c69 bl[69] br[69] wl[23] vdd gnd cell_6t
Xbit_r24_c69 bl[69] br[69] wl[24] vdd gnd cell_6t
Xbit_r25_c69 bl[69] br[69] wl[25] vdd gnd cell_6t
Xbit_r26_c69 bl[69] br[69] wl[26] vdd gnd cell_6t
Xbit_r27_c69 bl[69] br[69] wl[27] vdd gnd cell_6t
Xbit_r28_c69 bl[69] br[69] wl[28] vdd gnd cell_6t
Xbit_r29_c69 bl[69] br[69] wl[29] vdd gnd cell_6t
Xbit_r30_c69 bl[69] br[69] wl[30] vdd gnd cell_6t
Xbit_r31_c69 bl[69] br[69] wl[31] vdd gnd cell_6t
Xbit_r32_c69 bl[69] br[69] wl[32] vdd gnd cell_6t
Xbit_r33_c69 bl[69] br[69] wl[33] vdd gnd cell_6t
Xbit_r34_c69 bl[69] br[69] wl[34] vdd gnd cell_6t
Xbit_r35_c69 bl[69] br[69] wl[35] vdd gnd cell_6t
Xbit_r36_c69 bl[69] br[69] wl[36] vdd gnd cell_6t
Xbit_r37_c69 bl[69] br[69] wl[37] vdd gnd cell_6t
Xbit_r38_c69 bl[69] br[69] wl[38] vdd gnd cell_6t
Xbit_r39_c69 bl[69] br[69] wl[39] vdd gnd cell_6t
Xbit_r40_c69 bl[69] br[69] wl[40] vdd gnd cell_6t
Xbit_r41_c69 bl[69] br[69] wl[41] vdd gnd cell_6t
Xbit_r42_c69 bl[69] br[69] wl[42] vdd gnd cell_6t
Xbit_r43_c69 bl[69] br[69] wl[43] vdd gnd cell_6t
Xbit_r44_c69 bl[69] br[69] wl[44] vdd gnd cell_6t
Xbit_r45_c69 bl[69] br[69] wl[45] vdd gnd cell_6t
Xbit_r46_c69 bl[69] br[69] wl[46] vdd gnd cell_6t
Xbit_r47_c69 bl[69] br[69] wl[47] vdd gnd cell_6t
Xbit_r48_c69 bl[69] br[69] wl[48] vdd gnd cell_6t
Xbit_r49_c69 bl[69] br[69] wl[49] vdd gnd cell_6t
Xbit_r50_c69 bl[69] br[69] wl[50] vdd gnd cell_6t
Xbit_r51_c69 bl[69] br[69] wl[51] vdd gnd cell_6t
Xbit_r52_c69 bl[69] br[69] wl[52] vdd gnd cell_6t
Xbit_r53_c69 bl[69] br[69] wl[53] vdd gnd cell_6t
Xbit_r54_c69 bl[69] br[69] wl[54] vdd gnd cell_6t
Xbit_r55_c69 bl[69] br[69] wl[55] vdd gnd cell_6t
Xbit_r56_c69 bl[69] br[69] wl[56] vdd gnd cell_6t
Xbit_r57_c69 bl[69] br[69] wl[57] vdd gnd cell_6t
Xbit_r58_c69 bl[69] br[69] wl[58] vdd gnd cell_6t
Xbit_r59_c69 bl[69] br[69] wl[59] vdd gnd cell_6t
Xbit_r60_c69 bl[69] br[69] wl[60] vdd gnd cell_6t
Xbit_r61_c69 bl[69] br[69] wl[61] vdd gnd cell_6t
Xbit_r62_c69 bl[69] br[69] wl[62] vdd gnd cell_6t
Xbit_r63_c69 bl[69] br[69] wl[63] vdd gnd cell_6t
Xbit_r0_c70 bl[70] br[70] wl[0] vdd gnd cell_6t
Xbit_r1_c70 bl[70] br[70] wl[1] vdd gnd cell_6t
Xbit_r2_c70 bl[70] br[70] wl[2] vdd gnd cell_6t
Xbit_r3_c70 bl[70] br[70] wl[3] vdd gnd cell_6t
Xbit_r4_c70 bl[70] br[70] wl[4] vdd gnd cell_6t
Xbit_r5_c70 bl[70] br[70] wl[5] vdd gnd cell_6t
Xbit_r6_c70 bl[70] br[70] wl[6] vdd gnd cell_6t
Xbit_r7_c70 bl[70] br[70] wl[7] vdd gnd cell_6t
Xbit_r8_c70 bl[70] br[70] wl[8] vdd gnd cell_6t
Xbit_r9_c70 bl[70] br[70] wl[9] vdd gnd cell_6t
Xbit_r10_c70 bl[70] br[70] wl[10] vdd gnd cell_6t
Xbit_r11_c70 bl[70] br[70] wl[11] vdd gnd cell_6t
Xbit_r12_c70 bl[70] br[70] wl[12] vdd gnd cell_6t
Xbit_r13_c70 bl[70] br[70] wl[13] vdd gnd cell_6t
Xbit_r14_c70 bl[70] br[70] wl[14] vdd gnd cell_6t
Xbit_r15_c70 bl[70] br[70] wl[15] vdd gnd cell_6t
Xbit_r16_c70 bl[70] br[70] wl[16] vdd gnd cell_6t
Xbit_r17_c70 bl[70] br[70] wl[17] vdd gnd cell_6t
Xbit_r18_c70 bl[70] br[70] wl[18] vdd gnd cell_6t
Xbit_r19_c70 bl[70] br[70] wl[19] vdd gnd cell_6t
Xbit_r20_c70 bl[70] br[70] wl[20] vdd gnd cell_6t
Xbit_r21_c70 bl[70] br[70] wl[21] vdd gnd cell_6t
Xbit_r22_c70 bl[70] br[70] wl[22] vdd gnd cell_6t
Xbit_r23_c70 bl[70] br[70] wl[23] vdd gnd cell_6t
Xbit_r24_c70 bl[70] br[70] wl[24] vdd gnd cell_6t
Xbit_r25_c70 bl[70] br[70] wl[25] vdd gnd cell_6t
Xbit_r26_c70 bl[70] br[70] wl[26] vdd gnd cell_6t
Xbit_r27_c70 bl[70] br[70] wl[27] vdd gnd cell_6t
Xbit_r28_c70 bl[70] br[70] wl[28] vdd gnd cell_6t
Xbit_r29_c70 bl[70] br[70] wl[29] vdd gnd cell_6t
Xbit_r30_c70 bl[70] br[70] wl[30] vdd gnd cell_6t
Xbit_r31_c70 bl[70] br[70] wl[31] vdd gnd cell_6t
Xbit_r32_c70 bl[70] br[70] wl[32] vdd gnd cell_6t
Xbit_r33_c70 bl[70] br[70] wl[33] vdd gnd cell_6t
Xbit_r34_c70 bl[70] br[70] wl[34] vdd gnd cell_6t
Xbit_r35_c70 bl[70] br[70] wl[35] vdd gnd cell_6t
Xbit_r36_c70 bl[70] br[70] wl[36] vdd gnd cell_6t
Xbit_r37_c70 bl[70] br[70] wl[37] vdd gnd cell_6t
Xbit_r38_c70 bl[70] br[70] wl[38] vdd gnd cell_6t
Xbit_r39_c70 bl[70] br[70] wl[39] vdd gnd cell_6t
Xbit_r40_c70 bl[70] br[70] wl[40] vdd gnd cell_6t
Xbit_r41_c70 bl[70] br[70] wl[41] vdd gnd cell_6t
Xbit_r42_c70 bl[70] br[70] wl[42] vdd gnd cell_6t
Xbit_r43_c70 bl[70] br[70] wl[43] vdd gnd cell_6t
Xbit_r44_c70 bl[70] br[70] wl[44] vdd gnd cell_6t
Xbit_r45_c70 bl[70] br[70] wl[45] vdd gnd cell_6t
Xbit_r46_c70 bl[70] br[70] wl[46] vdd gnd cell_6t
Xbit_r47_c70 bl[70] br[70] wl[47] vdd gnd cell_6t
Xbit_r48_c70 bl[70] br[70] wl[48] vdd gnd cell_6t
Xbit_r49_c70 bl[70] br[70] wl[49] vdd gnd cell_6t
Xbit_r50_c70 bl[70] br[70] wl[50] vdd gnd cell_6t
Xbit_r51_c70 bl[70] br[70] wl[51] vdd gnd cell_6t
Xbit_r52_c70 bl[70] br[70] wl[52] vdd gnd cell_6t
Xbit_r53_c70 bl[70] br[70] wl[53] vdd gnd cell_6t
Xbit_r54_c70 bl[70] br[70] wl[54] vdd gnd cell_6t
Xbit_r55_c70 bl[70] br[70] wl[55] vdd gnd cell_6t
Xbit_r56_c70 bl[70] br[70] wl[56] vdd gnd cell_6t
Xbit_r57_c70 bl[70] br[70] wl[57] vdd gnd cell_6t
Xbit_r58_c70 bl[70] br[70] wl[58] vdd gnd cell_6t
Xbit_r59_c70 bl[70] br[70] wl[59] vdd gnd cell_6t
Xbit_r60_c70 bl[70] br[70] wl[60] vdd gnd cell_6t
Xbit_r61_c70 bl[70] br[70] wl[61] vdd gnd cell_6t
Xbit_r62_c70 bl[70] br[70] wl[62] vdd gnd cell_6t
Xbit_r63_c70 bl[70] br[70] wl[63] vdd gnd cell_6t
Xbit_r0_c71 bl[71] br[71] wl[0] vdd gnd cell_6t
Xbit_r1_c71 bl[71] br[71] wl[1] vdd gnd cell_6t
Xbit_r2_c71 bl[71] br[71] wl[2] vdd gnd cell_6t
Xbit_r3_c71 bl[71] br[71] wl[3] vdd gnd cell_6t
Xbit_r4_c71 bl[71] br[71] wl[4] vdd gnd cell_6t
Xbit_r5_c71 bl[71] br[71] wl[5] vdd gnd cell_6t
Xbit_r6_c71 bl[71] br[71] wl[6] vdd gnd cell_6t
Xbit_r7_c71 bl[71] br[71] wl[7] vdd gnd cell_6t
Xbit_r8_c71 bl[71] br[71] wl[8] vdd gnd cell_6t
Xbit_r9_c71 bl[71] br[71] wl[9] vdd gnd cell_6t
Xbit_r10_c71 bl[71] br[71] wl[10] vdd gnd cell_6t
Xbit_r11_c71 bl[71] br[71] wl[11] vdd gnd cell_6t
Xbit_r12_c71 bl[71] br[71] wl[12] vdd gnd cell_6t
Xbit_r13_c71 bl[71] br[71] wl[13] vdd gnd cell_6t
Xbit_r14_c71 bl[71] br[71] wl[14] vdd gnd cell_6t
Xbit_r15_c71 bl[71] br[71] wl[15] vdd gnd cell_6t
Xbit_r16_c71 bl[71] br[71] wl[16] vdd gnd cell_6t
Xbit_r17_c71 bl[71] br[71] wl[17] vdd gnd cell_6t
Xbit_r18_c71 bl[71] br[71] wl[18] vdd gnd cell_6t
Xbit_r19_c71 bl[71] br[71] wl[19] vdd gnd cell_6t
Xbit_r20_c71 bl[71] br[71] wl[20] vdd gnd cell_6t
Xbit_r21_c71 bl[71] br[71] wl[21] vdd gnd cell_6t
Xbit_r22_c71 bl[71] br[71] wl[22] vdd gnd cell_6t
Xbit_r23_c71 bl[71] br[71] wl[23] vdd gnd cell_6t
Xbit_r24_c71 bl[71] br[71] wl[24] vdd gnd cell_6t
Xbit_r25_c71 bl[71] br[71] wl[25] vdd gnd cell_6t
Xbit_r26_c71 bl[71] br[71] wl[26] vdd gnd cell_6t
Xbit_r27_c71 bl[71] br[71] wl[27] vdd gnd cell_6t
Xbit_r28_c71 bl[71] br[71] wl[28] vdd gnd cell_6t
Xbit_r29_c71 bl[71] br[71] wl[29] vdd gnd cell_6t
Xbit_r30_c71 bl[71] br[71] wl[30] vdd gnd cell_6t
Xbit_r31_c71 bl[71] br[71] wl[31] vdd gnd cell_6t
Xbit_r32_c71 bl[71] br[71] wl[32] vdd gnd cell_6t
Xbit_r33_c71 bl[71] br[71] wl[33] vdd gnd cell_6t
Xbit_r34_c71 bl[71] br[71] wl[34] vdd gnd cell_6t
Xbit_r35_c71 bl[71] br[71] wl[35] vdd gnd cell_6t
Xbit_r36_c71 bl[71] br[71] wl[36] vdd gnd cell_6t
Xbit_r37_c71 bl[71] br[71] wl[37] vdd gnd cell_6t
Xbit_r38_c71 bl[71] br[71] wl[38] vdd gnd cell_6t
Xbit_r39_c71 bl[71] br[71] wl[39] vdd gnd cell_6t
Xbit_r40_c71 bl[71] br[71] wl[40] vdd gnd cell_6t
Xbit_r41_c71 bl[71] br[71] wl[41] vdd gnd cell_6t
Xbit_r42_c71 bl[71] br[71] wl[42] vdd gnd cell_6t
Xbit_r43_c71 bl[71] br[71] wl[43] vdd gnd cell_6t
Xbit_r44_c71 bl[71] br[71] wl[44] vdd gnd cell_6t
Xbit_r45_c71 bl[71] br[71] wl[45] vdd gnd cell_6t
Xbit_r46_c71 bl[71] br[71] wl[46] vdd gnd cell_6t
Xbit_r47_c71 bl[71] br[71] wl[47] vdd gnd cell_6t
Xbit_r48_c71 bl[71] br[71] wl[48] vdd gnd cell_6t
Xbit_r49_c71 bl[71] br[71] wl[49] vdd gnd cell_6t
Xbit_r50_c71 bl[71] br[71] wl[50] vdd gnd cell_6t
Xbit_r51_c71 bl[71] br[71] wl[51] vdd gnd cell_6t
Xbit_r52_c71 bl[71] br[71] wl[52] vdd gnd cell_6t
Xbit_r53_c71 bl[71] br[71] wl[53] vdd gnd cell_6t
Xbit_r54_c71 bl[71] br[71] wl[54] vdd gnd cell_6t
Xbit_r55_c71 bl[71] br[71] wl[55] vdd gnd cell_6t
Xbit_r56_c71 bl[71] br[71] wl[56] vdd gnd cell_6t
Xbit_r57_c71 bl[71] br[71] wl[57] vdd gnd cell_6t
Xbit_r58_c71 bl[71] br[71] wl[58] vdd gnd cell_6t
Xbit_r59_c71 bl[71] br[71] wl[59] vdd gnd cell_6t
Xbit_r60_c71 bl[71] br[71] wl[60] vdd gnd cell_6t
Xbit_r61_c71 bl[71] br[71] wl[61] vdd gnd cell_6t
Xbit_r62_c71 bl[71] br[71] wl[62] vdd gnd cell_6t
Xbit_r63_c71 bl[71] br[71] wl[63] vdd gnd cell_6t
Xbit_r0_c72 bl[72] br[72] wl[0] vdd gnd cell_6t
Xbit_r1_c72 bl[72] br[72] wl[1] vdd gnd cell_6t
Xbit_r2_c72 bl[72] br[72] wl[2] vdd gnd cell_6t
Xbit_r3_c72 bl[72] br[72] wl[3] vdd gnd cell_6t
Xbit_r4_c72 bl[72] br[72] wl[4] vdd gnd cell_6t
Xbit_r5_c72 bl[72] br[72] wl[5] vdd gnd cell_6t
Xbit_r6_c72 bl[72] br[72] wl[6] vdd gnd cell_6t
Xbit_r7_c72 bl[72] br[72] wl[7] vdd gnd cell_6t
Xbit_r8_c72 bl[72] br[72] wl[8] vdd gnd cell_6t
Xbit_r9_c72 bl[72] br[72] wl[9] vdd gnd cell_6t
Xbit_r10_c72 bl[72] br[72] wl[10] vdd gnd cell_6t
Xbit_r11_c72 bl[72] br[72] wl[11] vdd gnd cell_6t
Xbit_r12_c72 bl[72] br[72] wl[12] vdd gnd cell_6t
Xbit_r13_c72 bl[72] br[72] wl[13] vdd gnd cell_6t
Xbit_r14_c72 bl[72] br[72] wl[14] vdd gnd cell_6t
Xbit_r15_c72 bl[72] br[72] wl[15] vdd gnd cell_6t
Xbit_r16_c72 bl[72] br[72] wl[16] vdd gnd cell_6t
Xbit_r17_c72 bl[72] br[72] wl[17] vdd gnd cell_6t
Xbit_r18_c72 bl[72] br[72] wl[18] vdd gnd cell_6t
Xbit_r19_c72 bl[72] br[72] wl[19] vdd gnd cell_6t
Xbit_r20_c72 bl[72] br[72] wl[20] vdd gnd cell_6t
Xbit_r21_c72 bl[72] br[72] wl[21] vdd gnd cell_6t
Xbit_r22_c72 bl[72] br[72] wl[22] vdd gnd cell_6t
Xbit_r23_c72 bl[72] br[72] wl[23] vdd gnd cell_6t
Xbit_r24_c72 bl[72] br[72] wl[24] vdd gnd cell_6t
Xbit_r25_c72 bl[72] br[72] wl[25] vdd gnd cell_6t
Xbit_r26_c72 bl[72] br[72] wl[26] vdd gnd cell_6t
Xbit_r27_c72 bl[72] br[72] wl[27] vdd gnd cell_6t
Xbit_r28_c72 bl[72] br[72] wl[28] vdd gnd cell_6t
Xbit_r29_c72 bl[72] br[72] wl[29] vdd gnd cell_6t
Xbit_r30_c72 bl[72] br[72] wl[30] vdd gnd cell_6t
Xbit_r31_c72 bl[72] br[72] wl[31] vdd gnd cell_6t
Xbit_r32_c72 bl[72] br[72] wl[32] vdd gnd cell_6t
Xbit_r33_c72 bl[72] br[72] wl[33] vdd gnd cell_6t
Xbit_r34_c72 bl[72] br[72] wl[34] vdd gnd cell_6t
Xbit_r35_c72 bl[72] br[72] wl[35] vdd gnd cell_6t
Xbit_r36_c72 bl[72] br[72] wl[36] vdd gnd cell_6t
Xbit_r37_c72 bl[72] br[72] wl[37] vdd gnd cell_6t
Xbit_r38_c72 bl[72] br[72] wl[38] vdd gnd cell_6t
Xbit_r39_c72 bl[72] br[72] wl[39] vdd gnd cell_6t
Xbit_r40_c72 bl[72] br[72] wl[40] vdd gnd cell_6t
Xbit_r41_c72 bl[72] br[72] wl[41] vdd gnd cell_6t
Xbit_r42_c72 bl[72] br[72] wl[42] vdd gnd cell_6t
Xbit_r43_c72 bl[72] br[72] wl[43] vdd gnd cell_6t
Xbit_r44_c72 bl[72] br[72] wl[44] vdd gnd cell_6t
Xbit_r45_c72 bl[72] br[72] wl[45] vdd gnd cell_6t
Xbit_r46_c72 bl[72] br[72] wl[46] vdd gnd cell_6t
Xbit_r47_c72 bl[72] br[72] wl[47] vdd gnd cell_6t
Xbit_r48_c72 bl[72] br[72] wl[48] vdd gnd cell_6t
Xbit_r49_c72 bl[72] br[72] wl[49] vdd gnd cell_6t
Xbit_r50_c72 bl[72] br[72] wl[50] vdd gnd cell_6t
Xbit_r51_c72 bl[72] br[72] wl[51] vdd gnd cell_6t
Xbit_r52_c72 bl[72] br[72] wl[52] vdd gnd cell_6t
Xbit_r53_c72 bl[72] br[72] wl[53] vdd gnd cell_6t
Xbit_r54_c72 bl[72] br[72] wl[54] vdd gnd cell_6t
Xbit_r55_c72 bl[72] br[72] wl[55] vdd gnd cell_6t
Xbit_r56_c72 bl[72] br[72] wl[56] vdd gnd cell_6t
Xbit_r57_c72 bl[72] br[72] wl[57] vdd gnd cell_6t
Xbit_r58_c72 bl[72] br[72] wl[58] vdd gnd cell_6t
Xbit_r59_c72 bl[72] br[72] wl[59] vdd gnd cell_6t
Xbit_r60_c72 bl[72] br[72] wl[60] vdd gnd cell_6t
Xbit_r61_c72 bl[72] br[72] wl[61] vdd gnd cell_6t
Xbit_r62_c72 bl[72] br[72] wl[62] vdd gnd cell_6t
Xbit_r63_c72 bl[72] br[72] wl[63] vdd gnd cell_6t
Xbit_r0_c73 bl[73] br[73] wl[0] vdd gnd cell_6t
Xbit_r1_c73 bl[73] br[73] wl[1] vdd gnd cell_6t
Xbit_r2_c73 bl[73] br[73] wl[2] vdd gnd cell_6t
Xbit_r3_c73 bl[73] br[73] wl[3] vdd gnd cell_6t
Xbit_r4_c73 bl[73] br[73] wl[4] vdd gnd cell_6t
Xbit_r5_c73 bl[73] br[73] wl[5] vdd gnd cell_6t
Xbit_r6_c73 bl[73] br[73] wl[6] vdd gnd cell_6t
Xbit_r7_c73 bl[73] br[73] wl[7] vdd gnd cell_6t
Xbit_r8_c73 bl[73] br[73] wl[8] vdd gnd cell_6t
Xbit_r9_c73 bl[73] br[73] wl[9] vdd gnd cell_6t
Xbit_r10_c73 bl[73] br[73] wl[10] vdd gnd cell_6t
Xbit_r11_c73 bl[73] br[73] wl[11] vdd gnd cell_6t
Xbit_r12_c73 bl[73] br[73] wl[12] vdd gnd cell_6t
Xbit_r13_c73 bl[73] br[73] wl[13] vdd gnd cell_6t
Xbit_r14_c73 bl[73] br[73] wl[14] vdd gnd cell_6t
Xbit_r15_c73 bl[73] br[73] wl[15] vdd gnd cell_6t
Xbit_r16_c73 bl[73] br[73] wl[16] vdd gnd cell_6t
Xbit_r17_c73 bl[73] br[73] wl[17] vdd gnd cell_6t
Xbit_r18_c73 bl[73] br[73] wl[18] vdd gnd cell_6t
Xbit_r19_c73 bl[73] br[73] wl[19] vdd gnd cell_6t
Xbit_r20_c73 bl[73] br[73] wl[20] vdd gnd cell_6t
Xbit_r21_c73 bl[73] br[73] wl[21] vdd gnd cell_6t
Xbit_r22_c73 bl[73] br[73] wl[22] vdd gnd cell_6t
Xbit_r23_c73 bl[73] br[73] wl[23] vdd gnd cell_6t
Xbit_r24_c73 bl[73] br[73] wl[24] vdd gnd cell_6t
Xbit_r25_c73 bl[73] br[73] wl[25] vdd gnd cell_6t
Xbit_r26_c73 bl[73] br[73] wl[26] vdd gnd cell_6t
Xbit_r27_c73 bl[73] br[73] wl[27] vdd gnd cell_6t
Xbit_r28_c73 bl[73] br[73] wl[28] vdd gnd cell_6t
Xbit_r29_c73 bl[73] br[73] wl[29] vdd gnd cell_6t
Xbit_r30_c73 bl[73] br[73] wl[30] vdd gnd cell_6t
Xbit_r31_c73 bl[73] br[73] wl[31] vdd gnd cell_6t
Xbit_r32_c73 bl[73] br[73] wl[32] vdd gnd cell_6t
Xbit_r33_c73 bl[73] br[73] wl[33] vdd gnd cell_6t
Xbit_r34_c73 bl[73] br[73] wl[34] vdd gnd cell_6t
Xbit_r35_c73 bl[73] br[73] wl[35] vdd gnd cell_6t
Xbit_r36_c73 bl[73] br[73] wl[36] vdd gnd cell_6t
Xbit_r37_c73 bl[73] br[73] wl[37] vdd gnd cell_6t
Xbit_r38_c73 bl[73] br[73] wl[38] vdd gnd cell_6t
Xbit_r39_c73 bl[73] br[73] wl[39] vdd gnd cell_6t
Xbit_r40_c73 bl[73] br[73] wl[40] vdd gnd cell_6t
Xbit_r41_c73 bl[73] br[73] wl[41] vdd gnd cell_6t
Xbit_r42_c73 bl[73] br[73] wl[42] vdd gnd cell_6t
Xbit_r43_c73 bl[73] br[73] wl[43] vdd gnd cell_6t
Xbit_r44_c73 bl[73] br[73] wl[44] vdd gnd cell_6t
Xbit_r45_c73 bl[73] br[73] wl[45] vdd gnd cell_6t
Xbit_r46_c73 bl[73] br[73] wl[46] vdd gnd cell_6t
Xbit_r47_c73 bl[73] br[73] wl[47] vdd gnd cell_6t
Xbit_r48_c73 bl[73] br[73] wl[48] vdd gnd cell_6t
Xbit_r49_c73 bl[73] br[73] wl[49] vdd gnd cell_6t
Xbit_r50_c73 bl[73] br[73] wl[50] vdd gnd cell_6t
Xbit_r51_c73 bl[73] br[73] wl[51] vdd gnd cell_6t
Xbit_r52_c73 bl[73] br[73] wl[52] vdd gnd cell_6t
Xbit_r53_c73 bl[73] br[73] wl[53] vdd gnd cell_6t
Xbit_r54_c73 bl[73] br[73] wl[54] vdd gnd cell_6t
Xbit_r55_c73 bl[73] br[73] wl[55] vdd gnd cell_6t
Xbit_r56_c73 bl[73] br[73] wl[56] vdd gnd cell_6t
Xbit_r57_c73 bl[73] br[73] wl[57] vdd gnd cell_6t
Xbit_r58_c73 bl[73] br[73] wl[58] vdd gnd cell_6t
Xbit_r59_c73 bl[73] br[73] wl[59] vdd gnd cell_6t
Xbit_r60_c73 bl[73] br[73] wl[60] vdd gnd cell_6t
Xbit_r61_c73 bl[73] br[73] wl[61] vdd gnd cell_6t
Xbit_r62_c73 bl[73] br[73] wl[62] vdd gnd cell_6t
Xbit_r63_c73 bl[73] br[73] wl[63] vdd gnd cell_6t
Xbit_r0_c74 bl[74] br[74] wl[0] vdd gnd cell_6t
Xbit_r1_c74 bl[74] br[74] wl[1] vdd gnd cell_6t
Xbit_r2_c74 bl[74] br[74] wl[2] vdd gnd cell_6t
Xbit_r3_c74 bl[74] br[74] wl[3] vdd gnd cell_6t
Xbit_r4_c74 bl[74] br[74] wl[4] vdd gnd cell_6t
Xbit_r5_c74 bl[74] br[74] wl[5] vdd gnd cell_6t
Xbit_r6_c74 bl[74] br[74] wl[6] vdd gnd cell_6t
Xbit_r7_c74 bl[74] br[74] wl[7] vdd gnd cell_6t
Xbit_r8_c74 bl[74] br[74] wl[8] vdd gnd cell_6t
Xbit_r9_c74 bl[74] br[74] wl[9] vdd gnd cell_6t
Xbit_r10_c74 bl[74] br[74] wl[10] vdd gnd cell_6t
Xbit_r11_c74 bl[74] br[74] wl[11] vdd gnd cell_6t
Xbit_r12_c74 bl[74] br[74] wl[12] vdd gnd cell_6t
Xbit_r13_c74 bl[74] br[74] wl[13] vdd gnd cell_6t
Xbit_r14_c74 bl[74] br[74] wl[14] vdd gnd cell_6t
Xbit_r15_c74 bl[74] br[74] wl[15] vdd gnd cell_6t
Xbit_r16_c74 bl[74] br[74] wl[16] vdd gnd cell_6t
Xbit_r17_c74 bl[74] br[74] wl[17] vdd gnd cell_6t
Xbit_r18_c74 bl[74] br[74] wl[18] vdd gnd cell_6t
Xbit_r19_c74 bl[74] br[74] wl[19] vdd gnd cell_6t
Xbit_r20_c74 bl[74] br[74] wl[20] vdd gnd cell_6t
Xbit_r21_c74 bl[74] br[74] wl[21] vdd gnd cell_6t
Xbit_r22_c74 bl[74] br[74] wl[22] vdd gnd cell_6t
Xbit_r23_c74 bl[74] br[74] wl[23] vdd gnd cell_6t
Xbit_r24_c74 bl[74] br[74] wl[24] vdd gnd cell_6t
Xbit_r25_c74 bl[74] br[74] wl[25] vdd gnd cell_6t
Xbit_r26_c74 bl[74] br[74] wl[26] vdd gnd cell_6t
Xbit_r27_c74 bl[74] br[74] wl[27] vdd gnd cell_6t
Xbit_r28_c74 bl[74] br[74] wl[28] vdd gnd cell_6t
Xbit_r29_c74 bl[74] br[74] wl[29] vdd gnd cell_6t
Xbit_r30_c74 bl[74] br[74] wl[30] vdd gnd cell_6t
Xbit_r31_c74 bl[74] br[74] wl[31] vdd gnd cell_6t
Xbit_r32_c74 bl[74] br[74] wl[32] vdd gnd cell_6t
Xbit_r33_c74 bl[74] br[74] wl[33] vdd gnd cell_6t
Xbit_r34_c74 bl[74] br[74] wl[34] vdd gnd cell_6t
Xbit_r35_c74 bl[74] br[74] wl[35] vdd gnd cell_6t
Xbit_r36_c74 bl[74] br[74] wl[36] vdd gnd cell_6t
Xbit_r37_c74 bl[74] br[74] wl[37] vdd gnd cell_6t
Xbit_r38_c74 bl[74] br[74] wl[38] vdd gnd cell_6t
Xbit_r39_c74 bl[74] br[74] wl[39] vdd gnd cell_6t
Xbit_r40_c74 bl[74] br[74] wl[40] vdd gnd cell_6t
Xbit_r41_c74 bl[74] br[74] wl[41] vdd gnd cell_6t
Xbit_r42_c74 bl[74] br[74] wl[42] vdd gnd cell_6t
Xbit_r43_c74 bl[74] br[74] wl[43] vdd gnd cell_6t
Xbit_r44_c74 bl[74] br[74] wl[44] vdd gnd cell_6t
Xbit_r45_c74 bl[74] br[74] wl[45] vdd gnd cell_6t
Xbit_r46_c74 bl[74] br[74] wl[46] vdd gnd cell_6t
Xbit_r47_c74 bl[74] br[74] wl[47] vdd gnd cell_6t
Xbit_r48_c74 bl[74] br[74] wl[48] vdd gnd cell_6t
Xbit_r49_c74 bl[74] br[74] wl[49] vdd gnd cell_6t
Xbit_r50_c74 bl[74] br[74] wl[50] vdd gnd cell_6t
Xbit_r51_c74 bl[74] br[74] wl[51] vdd gnd cell_6t
Xbit_r52_c74 bl[74] br[74] wl[52] vdd gnd cell_6t
Xbit_r53_c74 bl[74] br[74] wl[53] vdd gnd cell_6t
Xbit_r54_c74 bl[74] br[74] wl[54] vdd gnd cell_6t
Xbit_r55_c74 bl[74] br[74] wl[55] vdd gnd cell_6t
Xbit_r56_c74 bl[74] br[74] wl[56] vdd gnd cell_6t
Xbit_r57_c74 bl[74] br[74] wl[57] vdd gnd cell_6t
Xbit_r58_c74 bl[74] br[74] wl[58] vdd gnd cell_6t
Xbit_r59_c74 bl[74] br[74] wl[59] vdd gnd cell_6t
Xbit_r60_c74 bl[74] br[74] wl[60] vdd gnd cell_6t
Xbit_r61_c74 bl[74] br[74] wl[61] vdd gnd cell_6t
Xbit_r62_c74 bl[74] br[74] wl[62] vdd gnd cell_6t
Xbit_r63_c74 bl[74] br[74] wl[63] vdd gnd cell_6t
Xbit_r0_c75 bl[75] br[75] wl[0] vdd gnd cell_6t
Xbit_r1_c75 bl[75] br[75] wl[1] vdd gnd cell_6t
Xbit_r2_c75 bl[75] br[75] wl[2] vdd gnd cell_6t
Xbit_r3_c75 bl[75] br[75] wl[3] vdd gnd cell_6t
Xbit_r4_c75 bl[75] br[75] wl[4] vdd gnd cell_6t
Xbit_r5_c75 bl[75] br[75] wl[5] vdd gnd cell_6t
Xbit_r6_c75 bl[75] br[75] wl[6] vdd gnd cell_6t
Xbit_r7_c75 bl[75] br[75] wl[7] vdd gnd cell_6t
Xbit_r8_c75 bl[75] br[75] wl[8] vdd gnd cell_6t
Xbit_r9_c75 bl[75] br[75] wl[9] vdd gnd cell_6t
Xbit_r10_c75 bl[75] br[75] wl[10] vdd gnd cell_6t
Xbit_r11_c75 bl[75] br[75] wl[11] vdd gnd cell_6t
Xbit_r12_c75 bl[75] br[75] wl[12] vdd gnd cell_6t
Xbit_r13_c75 bl[75] br[75] wl[13] vdd gnd cell_6t
Xbit_r14_c75 bl[75] br[75] wl[14] vdd gnd cell_6t
Xbit_r15_c75 bl[75] br[75] wl[15] vdd gnd cell_6t
Xbit_r16_c75 bl[75] br[75] wl[16] vdd gnd cell_6t
Xbit_r17_c75 bl[75] br[75] wl[17] vdd gnd cell_6t
Xbit_r18_c75 bl[75] br[75] wl[18] vdd gnd cell_6t
Xbit_r19_c75 bl[75] br[75] wl[19] vdd gnd cell_6t
Xbit_r20_c75 bl[75] br[75] wl[20] vdd gnd cell_6t
Xbit_r21_c75 bl[75] br[75] wl[21] vdd gnd cell_6t
Xbit_r22_c75 bl[75] br[75] wl[22] vdd gnd cell_6t
Xbit_r23_c75 bl[75] br[75] wl[23] vdd gnd cell_6t
Xbit_r24_c75 bl[75] br[75] wl[24] vdd gnd cell_6t
Xbit_r25_c75 bl[75] br[75] wl[25] vdd gnd cell_6t
Xbit_r26_c75 bl[75] br[75] wl[26] vdd gnd cell_6t
Xbit_r27_c75 bl[75] br[75] wl[27] vdd gnd cell_6t
Xbit_r28_c75 bl[75] br[75] wl[28] vdd gnd cell_6t
Xbit_r29_c75 bl[75] br[75] wl[29] vdd gnd cell_6t
Xbit_r30_c75 bl[75] br[75] wl[30] vdd gnd cell_6t
Xbit_r31_c75 bl[75] br[75] wl[31] vdd gnd cell_6t
Xbit_r32_c75 bl[75] br[75] wl[32] vdd gnd cell_6t
Xbit_r33_c75 bl[75] br[75] wl[33] vdd gnd cell_6t
Xbit_r34_c75 bl[75] br[75] wl[34] vdd gnd cell_6t
Xbit_r35_c75 bl[75] br[75] wl[35] vdd gnd cell_6t
Xbit_r36_c75 bl[75] br[75] wl[36] vdd gnd cell_6t
Xbit_r37_c75 bl[75] br[75] wl[37] vdd gnd cell_6t
Xbit_r38_c75 bl[75] br[75] wl[38] vdd gnd cell_6t
Xbit_r39_c75 bl[75] br[75] wl[39] vdd gnd cell_6t
Xbit_r40_c75 bl[75] br[75] wl[40] vdd gnd cell_6t
Xbit_r41_c75 bl[75] br[75] wl[41] vdd gnd cell_6t
Xbit_r42_c75 bl[75] br[75] wl[42] vdd gnd cell_6t
Xbit_r43_c75 bl[75] br[75] wl[43] vdd gnd cell_6t
Xbit_r44_c75 bl[75] br[75] wl[44] vdd gnd cell_6t
Xbit_r45_c75 bl[75] br[75] wl[45] vdd gnd cell_6t
Xbit_r46_c75 bl[75] br[75] wl[46] vdd gnd cell_6t
Xbit_r47_c75 bl[75] br[75] wl[47] vdd gnd cell_6t
Xbit_r48_c75 bl[75] br[75] wl[48] vdd gnd cell_6t
Xbit_r49_c75 bl[75] br[75] wl[49] vdd gnd cell_6t
Xbit_r50_c75 bl[75] br[75] wl[50] vdd gnd cell_6t
Xbit_r51_c75 bl[75] br[75] wl[51] vdd gnd cell_6t
Xbit_r52_c75 bl[75] br[75] wl[52] vdd gnd cell_6t
Xbit_r53_c75 bl[75] br[75] wl[53] vdd gnd cell_6t
Xbit_r54_c75 bl[75] br[75] wl[54] vdd gnd cell_6t
Xbit_r55_c75 bl[75] br[75] wl[55] vdd gnd cell_6t
Xbit_r56_c75 bl[75] br[75] wl[56] vdd gnd cell_6t
Xbit_r57_c75 bl[75] br[75] wl[57] vdd gnd cell_6t
Xbit_r58_c75 bl[75] br[75] wl[58] vdd gnd cell_6t
Xbit_r59_c75 bl[75] br[75] wl[59] vdd gnd cell_6t
Xbit_r60_c75 bl[75] br[75] wl[60] vdd gnd cell_6t
Xbit_r61_c75 bl[75] br[75] wl[61] vdd gnd cell_6t
Xbit_r62_c75 bl[75] br[75] wl[62] vdd gnd cell_6t
Xbit_r63_c75 bl[75] br[75] wl[63] vdd gnd cell_6t
Xbit_r0_c76 bl[76] br[76] wl[0] vdd gnd cell_6t
Xbit_r1_c76 bl[76] br[76] wl[1] vdd gnd cell_6t
Xbit_r2_c76 bl[76] br[76] wl[2] vdd gnd cell_6t
Xbit_r3_c76 bl[76] br[76] wl[3] vdd gnd cell_6t
Xbit_r4_c76 bl[76] br[76] wl[4] vdd gnd cell_6t
Xbit_r5_c76 bl[76] br[76] wl[5] vdd gnd cell_6t
Xbit_r6_c76 bl[76] br[76] wl[6] vdd gnd cell_6t
Xbit_r7_c76 bl[76] br[76] wl[7] vdd gnd cell_6t
Xbit_r8_c76 bl[76] br[76] wl[8] vdd gnd cell_6t
Xbit_r9_c76 bl[76] br[76] wl[9] vdd gnd cell_6t
Xbit_r10_c76 bl[76] br[76] wl[10] vdd gnd cell_6t
Xbit_r11_c76 bl[76] br[76] wl[11] vdd gnd cell_6t
Xbit_r12_c76 bl[76] br[76] wl[12] vdd gnd cell_6t
Xbit_r13_c76 bl[76] br[76] wl[13] vdd gnd cell_6t
Xbit_r14_c76 bl[76] br[76] wl[14] vdd gnd cell_6t
Xbit_r15_c76 bl[76] br[76] wl[15] vdd gnd cell_6t
Xbit_r16_c76 bl[76] br[76] wl[16] vdd gnd cell_6t
Xbit_r17_c76 bl[76] br[76] wl[17] vdd gnd cell_6t
Xbit_r18_c76 bl[76] br[76] wl[18] vdd gnd cell_6t
Xbit_r19_c76 bl[76] br[76] wl[19] vdd gnd cell_6t
Xbit_r20_c76 bl[76] br[76] wl[20] vdd gnd cell_6t
Xbit_r21_c76 bl[76] br[76] wl[21] vdd gnd cell_6t
Xbit_r22_c76 bl[76] br[76] wl[22] vdd gnd cell_6t
Xbit_r23_c76 bl[76] br[76] wl[23] vdd gnd cell_6t
Xbit_r24_c76 bl[76] br[76] wl[24] vdd gnd cell_6t
Xbit_r25_c76 bl[76] br[76] wl[25] vdd gnd cell_6t
Xbit_r26_c76 bl[76] br[76] wl[26] vdd gnd cell_6t
Xbit_r27_c76 bl[76] br[76] wl[27] vdd gnd cell_6t
Xbit_r28_c76 bl[76] br[76] wl[28] vdd gnd cell_6t
Xbit_r29_c76 bl[76] br[76] wl[29] vdd gnd cell_6t
Xbit_r30_c76 bl[76] br[76] wl[30] vdd gnd cell_6t
Xbit_r31_c76 bl[76] br[76] wl[31] vdd gnd cell_6t
Xbit_r32_c76 bl[76] br[76] wl[32] vdd gnd cell_6t
Xbit_r33_c76 bl[76] br[76] wl[33] vdd gnd cell_6t
Xbit_r34_c76 bl[76] br[76] wl[34] vdd gnd cell_6t
Xbit_r35_c76 bl[76] br[76] wl[35] vdd gnd cell_6t
Xbit_r36_c76 bl[76] br[76] wl[36] vdd gnd cell_6t
Xbit_r37_c76 bl[76] br[76] wl[37] vdd gnd cell_6t
Xbit_r38_c76 bl[76] br[76] wl[38] vdd gnd cell_6t
Xbit_r39_c76 bl[76] br[76] wl[39] vdd gnd cell_6t
Xbit_r40_c76 bl[76] br[76] wl[40] vdd gnd cell_6t
Xbit_r41_c76 bl[76] br[76] wl[41] vdd gnd cell_6t
Xbit_r42_c76 bl[76] br[76] wl[42] vdd gnd cell_6t
Xbit_r43_c76 bl[76] br[76] wl[43] vdd gnd cell_6t
Xbit_r44_c76 bl[76] br[76] wl[44] vdd gnd cell_6t
Xbit_r45_c76 bl[76] br[76] wl[45] vdd gnd cell_6t
Xbit_r46_c76 bl[76] br[76] wl[46] vdd gnd cell_6t
Xbit_r47_c76 bl[76] br[76] wl[47] vdd gnd cell_6t
Xbit_r48_c76 bl[76] br[76] wl[48] vdd gnd cell_6t
Xbit_r49_c76 bl[76] br[76] wl[49] vdd gnd cell_6t
Xbit_r50_c76 bl[76] br[76] wl[50] vdd gnd cell_6t
Xbit_r51_c76 bl[76] br[76] wl[51] vdd gnd cell_6t
Xbit_r52_c76 bl[76] br[76] wl[52] vdd gnd cell_6t
Xbit_r53_c76 bl[76] br[76] wl[53] vdd gnd cell_6t
Xbit_r54_c76 bl[76] br[76] wl[54] vdd gnd cell_6t
Xbit_r55_c76 bl[76] br[76] wl[55] vdd gnd cell_6t
Xbit_r56_c76 bl[76] br[76] wl[56] vdd gnd cell_6t
Xbit_r57_c76 bl[76] br[76] wl[57] vdd gnd cell_6t
Xbit_r58_c76 bl[76] br[76] wl[58] vdd gnd cell_6t
Xbit_r59_c76 bl[76] br[76] wl[59] vdd gnd cell_6t
Xbit_r60_c76 bl[76] br[76] wl[60] vdd gnd cell_6t
Xbit_r61_c76 bl[76] br[76] wl[61] vdd gnd cell_6t
Xbit_r62_c76 bl[76] br[76] wl[62] vdd gnd cell_6t
Xbit_r63_c76 bl[76] br[76] wl[63] vdd gnd cell_6t
Xbit_r0_c77 bl[77] br[77] wl[0] vdd gnd cell_6t
Xbit_r1_c77 bl[77] br[77] wl[1] vdd gnd cell_6t
Xbit_r2_c77 bl[77] br[77] wl[2] vdd gnd cell_6t
Xbit_r3_c77 bl[77] br[77] wl[3] vdd gnd cell_6t
Xbit_r4_c77 bl[77] br[77] wl[4] vdd gnd cell_6t
Xbit_r5_c77 bl[77] br[77] wl[5] vdd gnd cell_6t
Xbit_r6_c77 bl[77] br[77] wl[6] vdd gnd cell_6t
Xbit_r7_c77 bl[77] br[77] wl[7] vdd gnd cell_6t
Xbit_r8_c77 bl[77] br[77] wl[8] vdd gnd cell_6t
Xbit_r9_c77 bl[77] br[77] wl[9] vdd gnd cell_6t
Xbit_r10_c77 bl[77] br[77] wl[10] vdd gnd cell_6t
Xbit_r11_c77 bl[77] br[77] wl[11] vdd gnd cell_6t
Xbit_r12_c77 bl[77] br[77] wl[12] vdd gnd cell_6t
Xbit_r13_c77 bl[77] br[77] wl[13] vdd gnd cell_6t
Xbit_r14_c77 bl[77] br[77] wl[14] vdd gnd cell_6t
Xbit_r15_c77 bl[77] br[77] wl[15] vdd gnd cell_6t
Xbit_r16_c77 bl[77] br[77] wl[16] vdd gnd cell_6t
Xbit_r17_c77 bl[77] br[77] wl[17] vdd gnd cell_6t
Xbit_r18_c77 bl[77] br[77] wl[18] vdd gnd cell_6t
Xbit_r19_c77 bl[77] br[77] wl[19] vdd gnd cell_6t
Xbit_r20_c77 bl[77] br[77] wl[20] vdd gnd cell_6t
Xbit_r21_c77 bl[77] br[77] wl[21] vdd gnd cell_6t
Xbit_r22_c77 bl[77] br[77] wl[22] vdd gnd cell_6t
Xbit_r23_c77 bl[77] br[77] wl[23] vdd gnd cell_6t
Xbit_r24_c77 bl[77] br[77] wl[24] vdd gnd cell_6t
Xbit_r25_c77 bl[77] br[77] wl[25] vdd gnd cell_6t
Xbit_r26_c77 bl[77] br[77] wl[26] vdd gnd cell_6t
Xbit_r27_c77 bl[77] br[77] wl[27] vdd gnd cell_6t
Xbit_r28_c77 bl[77] br[77] wl[28] vdd gnd cell_6t
Xbit_r29_c77 bl[77] br[77] wl[29] vdd gnd cell_6t
Xbit_r30_c77 bl[77] br[77] wl[30] vdd gnd cell_6t
Xbit_r31_c77 bl[77] br[77] wl[31] vdd gnd cell_6t
Xbit_r32_c77 bl[77] br[77] wl[32] vdd gnd cell_6t
Xbit_r33_c77 bl[77] br[77] wl[33] vdd gnd cell_6t
Xbit_r34_c77 bl[77] br[77] wl[34] vdd gnd cell_6t
Xbit_r35_c77 bl[77] br[77] wl[35] vdd gnd cell_6t
Xbit_r36_c77 bl[77] br[77] wl[36] vdd gnd cell_6t
Xbit_r37_c77 bl[77] br[77] wl[37] vdd gnd cell_6t
Xbit_r38_c77 bl[77] br[77] wl[38] vdd gnd cell_6t
Xbit_r39_c77 bl[77] br[77] wl[39] vdd gnd cell_6t
Xbit_r40_c77 bl[77] br[77] wl[40] vdd gnd cell_6t
Xbit_r41_c77 bl[77] br[77] wl[41] vdd gnd cell_6t
Xbit_r42_c77 bl[77] br[77] wl[42] vdd gnd cell_6t
Xbit_r43_c77 bl[77] br[77] wl[43] vdd gnd cell_6t
Xbit_r44_c77 bl[77] br[77] wl[44] vdd gnd cell_6t
Xbit_r45_c77 bl[77] br[77] wl[45] vdd gnd cell_6t
Xbit_r46_c77 bl[77] br[77] wl[46] vdd gnd cell_6t
Xbit_r47_c77 bl[77] br[77] wl[47] vdd gnd cell_6t
Xbit_r48_c77 bl[77] br[77] wl[48] vdd gnd cell_6t
Xbit_r49_c77 bl[77] br[77] wl[49] vdd gnd cell_6t
Xbit_r50_c77 bl[77] br[77] wl[50] vdd gnd cell_6t
Xbit_r51_c77 bl[77] br[77] wl[51] vdd gnd cell_6t
Xbit_r52_c77 bl[77] br[77] wl[52] vdd gnd cell_6t
Xbit_r53_c77 bl[77] br[77] wl[53] vdd gnd cell_6t
Xbit_r54_c77 bl[77] br[77] wl[54] vdd gnd cell_6t
Xbit_r55_c77 bl[77] br[77] wl[55] vdd gnd cell_6t
Xbit_r56_c77 bl[77] br[77] wl[56] vdd gnd cell_6t
Xbit_r57_c77 bl[77] br[77] wl[57] vdd gnd cell_6t
Xbit_r58_c77 bl[77] br[77] wl[58] vdd gnd cell_6t
Xbit_r59_c77 bl[77] br[77] wl[59] vdd gnd cell_6t
Xbit_r60_c77 bl[77] br[77] wl[60] vdd gnd cell_6t
Xbit_r61_c77 bl[77] br[77] wl[61] vdd gnd cell_6t
Xbit_r62_c77 bl[77] br[77] wl[62] vdd gnd cell_6t
Xbit_r63_c77 bl[77] br[77] wl[63] vdd gnd cell_6t
Xbit_r0_c78 bl[78] br[78] wl[0] vdd gnd cell_6t
Xbit_r1_c78 bl[78] br[78] wl[1] vdd gnd cell_6t
Xbit_r2_c78 bl[78] br[78] wl[2] vdd gnd cell_6t
Xbit_r3_c78 bl[78] br[78] wl[3] vdd gnd cell_6t
Xbit_r4_c78 bl[78] br[78] wl[4] vdd gnd cell_6t
Xbit_r5_c78 bl[78] br[78] wl[5] vdd gnd cell_6t
Xbit_r6_c78 bl[78] br[78] wl[6] vdd gnd cell_6t
Xbit_r7_c78 bl[78] br[78] wl[7] vdd gnd cell_6t
Xbit_r8_c78 bl[78] br[78] wl[8] vdd gnd cell_6t
Xbit_r9_c78 bl[78] br[78] wl[9] vdd gnd cell_6t
Xbit_r10_c78 bl[78] br[78] wl[10] vdd gnd cell_6t
Xbit_r11_c78 bl[78] br[78] wl[11] vdd gnd cell_6t
Xbit_r12_c78 bl[78] br[78] wl[12] vdd gnd cell_6t
Xbit_r13_c78 bl[78] br[78] wl[13] vdd gnd cell_6t
Xbit_r14_c78 bl[78] br[78] wl[14] vdd gnd cell_6t
Xbit_r15_c78 bl[78] br[78] wl[15] vdd gnd cell_6t
Xbit_r16_c78 bl[78] br[78] wl[16] vdd gnd cell_6t
Xbit_r17_c78 bl[78] br[78] wl[17] vdd gnd cell_6t
Xbit_r18_c78 bl[78] br[78] wl[18] vdd gnd cell_6t
Xbit_r19_c78 bl[78] br[78] wl[19] vdd gnd cell_6t
Xbit_r20_c78 bl[78] br[78] wl[20] vdd gnd cell_6t
Xbit_r21_c78 bl[78] br[78] wl[21] vdd gnd cell_6t
Xbit_r22_c78 bl[78] br[78] wl[22] vdd gnd cell_6t
Xbit_r23_c78 bl[78] br[78] wl[23] vdd gnd cell_6t
Xbit_r24_c78 bl[78] br[78] wl[24] vdd gnd cell_6t
Xbit_r25_c78 bl[78] br[78] wl[25] vdd gnd cell_6t
Xbit_r26_c78 bl[78] br[78] wl[26] vdd gnd cell_6t
Xbit_r27_c78 bl[78] br[78] wl[27] vdd gnd cell_6t
Xbit_r28_c78 bl[78] br[78] wl[28] vdd gnd cell_6t
Xbit_r29_c78 bl[78] br[78] wl[29] vdd gnd cell_6t
Xbit_r30_c78 bl[78] br[78] wl[30] vdd gnd cell_6t
Xbit_r31_c78 bl[78] br[78] wl[31] vdd gnd cell_6t
Xbit_r32_c78 bl[78] br[78] wl[32] vdd gnd cell_6t
Xbit_r33_c78 bl[78] br[78] wl[33] vdd gnd cell_6t
Xbit_r34_c78 bl[78] br[78] wl[34] vdd gnd cell_6t
Xbit_r35_c78 bl[78] br[78] wl[35] vdd gnd cell_6t
Xbit_r36_c78 bl[78] br[78] wl[36] vdd gnd cell_6t
Xbit_r37_c78 bl[78] br[78] wl[37] vdd gnd cell_6t
Xbit_r38_c78 bl[78] br[78] wl[38] vdd gnd cell_6t
Xbit_r39_c78 bl[78] br[78] wl[39] vdd gnd cell_6t
Xbit_r40_c78 bl[78] br[78] wl[40] vdd gnd cell_6t
Xbit_r41_c78 bl[78] br[78] wl[41] vdd gnd cell_6t
Xbit_r42_c78 bl[78] br[78] wl[42] vdd gnd cell_6t
Xbit_r43_c78 bl[78] br[78] wl[43] vdd gnd cell_6t
Xbit_r44_c78 bl[78] br[78] wl[44] vdd gnd cell_6t
Xbit_r45_c78 bl[78] br[78] wl[45] vdd gnd cell_6t
Xbit_r46_c78 bl[78] br[78] wl[46] vdd gnd cell_6t
Xbit_r47_c78 bl[78] br[78] wl[47] vdd gnd cell_6t
Xbit_r48_c78 bl[78] br[78] wl[48] vdd gnd cell_6t
Xbit_r49_c78 bl[78] br[78] wl[49] vdd gnd cell_6t
Xbit_r50_c78 bl[78] br[78] wl[50] vdd gnd cell_6t
Xbit_r51_c78 bl[78] br[78] wl[51] vdd gnd cell_6t
Xbit_r52_c78 bl[78] br[78] wl[52] vdd gnd cell_6t
Xbit_r53_c78 bl[78] br[78] wl[53] vdd gnd cell_6t
Xbit_r54_c78 bl[78] br[78] wl[54] vdd gnd cell_6t
Xbit_r55_c78 bl[78] br[78] wl[55] vdd gnd cell_6t
Xbit_r56_c78 bl[78] br[78] wl[56] vdd gnd cell_6t
Xbit_r57_c78 bl[78] br[78] wl[57] vdd gnd cell_6t
Xbit_r58_c78 bl[78] br[78] wl[58] vdd gnd cell_6t
Xbit_r59_c78 bl[78] br[78] wl[59] vdd gnd cell_6t
Xbit_r60_c78 bl[78] br[78] wl[60] vdd gnd cell_6t
Xbit_r61_c78 bl[78] br[78] wl[61] vdd gnd cell_6t
Xbit_r62_c78 bl[78] br[78] wl[62] vdd gnd cell_6t
Xbit_r63_c78 bl[78] br[78] wl[63] vdd gnd cell_6t
Xbit_r0_c79 bl[79] br[79] wl[0] vdd gnd cell_6t
Xbit_r1_c79 bl[79] br[79] wl[1] vdd gnd cell_6t
Xbit_r2_c79 bl[79] br[79] wl[2] vdd gnd cell_6t
Xbit_r3_c79 bl[79] br[79] wl[3] vdd gnd cell_6t
Xbit_r4_c79 bl[79] br[79] wl[4] vdd gnd cell_6t
Xbit_r5_c79 bl[79] br[79] wl[5] vdd gnd cell_6t
Xbit_r6_c79 bl[79] br[79] wl[6] vdd gnd cell_6t
Xbit_r7_c79 bl[79] br[79] wl[7] vdd gnd cell_6t
Xbit_r8_c79 bl[79] br[79] wl[8] vdd gnd cell_6t
Xbit_r9_c79 bl[79] br[79] wl[9] vdd gnd cell_6t
Xbit_r10_c79 bl[79] br[79] wl[10] vdd gnd cell_6t
Xbit_r11_c79 bl[79] br[79] wl[11] vdd gnd cell_6t
Xbit_r12_c79 bl[79] br[79] wl[12] vdd gnd cell_6t
Xbit_r13_c79 bl[79] br[79] wl[13] vdd gnd cell_6t
Xbit_r14_c79 bl[79] br[79] wl[14] vdd gnd cell_6t
Xbit_r15_c79 bl[79] br[79] wl[15] vdd gnd cell_6t
Xbit_r16_c79 bl[79] br[79] wl[16] vdd gnd cell_6t
Xbit_r17_c79 bl[79] br[79] wl[17] vdd gnd cell_6t
Xbit_r18_c79 bl[79] br[79] wl[18] vdd gnd cell_6t
Xbit_r19_c79 bl[79] br[79] wl[19] vdd gnd cell_6t
Xbit_r20_c79 bl[79] br[79] wl[20] vdd gnd cell_6t
Xbit_r21_c79 bl[79] br[79] wl[21] vdd gnd cell_6t
Xbit_r22_c79 bl[79] br[79] wl[22] vdd gnd cell_6t
Xbit_r23_c79 bl[79] br[79] wl[23] vdd gnd cell_6t
Xbit_r24_c79 bl[79] br[79] wl[24] vdd gnd cell_6t
Xbit_r25_c79 bl[79] br[79] wl[25] vdd gnd cell_6t
Xbit_r26_c79 bl[79] br[79] wl[26] vdd gnd cell_6t
Xbit_r27_c79 bl[79] br[79] wl[27] vdd gnd cell_6t
Xbit_r28_c79 bl[79] br[79] wl[28] vdd gnd cell_6t
Xbit_r29_c79 bl[79] br[79] wl[29] vdd gnd cell_6t
Xbit_r30_c79 bl[79] br[79] wl[30] vdd gnd cell_6t
Xbit_r31_c79 bl[79] br[79] wl[31] vdd gnd cell_6t
Xbit_r32_c79 bl[79] br[79] wl[32] vdd gnd cell_6t
Xbit_r33_c79 bl[79] br[79] wl[33] vdd gnd cell_6t
Xbit_r34_c79 bl[79] br[79] wl[34] vdd gnd cell_6t
Xbit_r35_c79 bl[79] br[79] wl[35] vdd gnd cell_6t
Xbit_r36_c79 bl[79] br[79] wl[36] vdd gnd cell_6t
Xbit_r37_c79 bl[79] br[79] wl[37] vdd gnd cell_6t
Xbit_r38_c79 bl[79] br[79] wl[38] vdd gnd cell_6t
Xbit_r39_c79 bl[79] br[79] wl[39] vdd gnd cell_6t
Xbit_r40_c79 bl[79] br[79] wl[40] vdd gnd cell_6t
Xbit_r41_c79 bl[79] br[79] wl[41] vdd gnd cell_6t
Xbit_r42_c79 bl[79] br[79] wl[42] vdd gnd cell_6t
Xbit_r43_c79 bl[79] br[79] wl[43] vdd gnd cell_6t
Xbit_r44_c79 bl[79] br[79] wl[44] vdd gnd cell_6t
Xbit_r45_c79 bl[79] br[79] wl[45] vdd gnd cell_6t
Xbit_r46_c79 bl[79] br[79] wl[46] vdd gnd cell_6t
Xbit_r47_c79 bl[79] br[79] wl[47] vdd gnd cell_6t
Xbit_r48_c79 bl[79] br[79] wl[48] vdd gnd cell_6t
Xbit_r49_c79 bl[79] br[79] wl[49] vdd gnd cell_6t
Xbit_r50_c79 bl[79] br[79] wl[50] vdd gnd cell_6t
Xbit_r51_c79 bl[79] br[79] wl[51] vdd gnd cell_6t
Xbit_r52_c79 bl[79] br[79] wl[52] vdd gnd cell_6t
Xbit_r53_c79 bl[79] br[79] wl[53] vdd gnd cell_6t
Xbit_r54_c79 bl[79] br[79] wl[54] vdd gnd cell_6t
Xbit_r55_c79 bl[79] br[79] wl[55] vdd gnd cell_6t
Xbit_r56_c79 bl[79] br[79] wl[56] vdd gnd cell_6t
Xbit_r57_c79 bl[79] br[79] wl[57] vdd gnd cell_6t
Xbit_r58_c79 bl[79] br[79] wl[58] vdd gnd cell_6t
Xbit_r59_c79 bl[79] br[79] wl[59] vdd gnd cell_6t
Xbit_r60_c79 bl[79] br[79] wl[60] vdd gnd cell_6t
Xbit_r61_c79 bl[79] br[79] wl[61] vdd gnd cell_6t
Xbit_r62_c79 bl[79] br[79] wl[62] vdd gnd cell_6t
Xbit_r63_c79 bl[79] br[79] wl[63] vdd gnd cell_6t
Xbit_r0_c80 bl[80] br[80] wl[0] vdd gnd cell_6t
Xbit_r1_c80 bl[80] br[80] wl[1] vdd gnd cell_6t
Xbit_r2_c80 bl[80] br[80] wl[2] vdd gnd cell_6t
Xbit_r3_c80 bl[80] br[80] wl[3] vdd gnd cell_6t
Xbit_r4_c80 bl[80] br[80] wl[4] vdd gnd cell_6t
Xbit_r5_c80 bl[80] br[80] wl[5] vdd gnd cell_6t
Xbit_r6_c80 bl[80] br[80] wl[6] vdd gnd cell_6t
Xbit_r7_c80 bl[80] br[80] wl[7] vdd gnd cell_6t
Xbit_r8_c80 bl[80] br[80] wl[8] vdd gnd cell_6t
Xbit_r9_c80 bl[80] br[80] wl[9] vdd gnd cell_6t
Xbit_r10_c80 bl[80] br[80] wl[10] vdd gnd cell_6t
Xbit_r11_c80 bl[80] br[80] wl[11] vdd gnd cell_6t
Xbit_r12_c80 bl[80] br[80] wl[12] vdd gnd cell_6t
Xbit_r13_c80 bl[80] br[80] wl[13] vdd gnd cell_6t
Xbit_r14_c80 bl[80] br[80] wl[14] vdd gnd cell_6t
Xbit_r15_c80 bl[80] br[80] wl[15] vdd gnd cell_6t
Xbit_r16_c80 bl[80] br[80] wl[16] vdd gnd cell_6t
Xbit_r17_c80 bl[80] br[80] wl[17] vdd gnd cell_6t
Xbit_r18_c80 bl[80] br[80] wl[18] vdd gnd cell_6t
Xbit_r19_c80 bl[80] br[80] wl[19] vdd gnd cell_6t
Xbit_r20_c80 bl[80] br[80] wl[20] vdd gnd cell_6t
Xbit_r21_c80 bl[80] br[80] wl[21] vdd gnd cell_6t
Xbit_r22_c80 bl[80] br[80] wl[22] vdd gnd cell_6t
Xbit_r23_c80 bl[80] br[80] wl[23] vdd gnd cell_6t
Xbit_r24_c80 bl[80] br[80] wl[24] vdd gnd cell_6t
Xbit_r25_c80 bl[80] br[80] wl[25] vdd gnd cell_6t
Xbit_r26_c80 bl[80] br[80] wl[26] vdd gnd cell_6t
Xbit_r27_c80 bl[80] br[80] wl[27] vdd gnd cell_6t
Xbit_r28_c80 bl[80] br[80] wl[28] vdd gnd cell_6t
Xbit_r29_c80 bl[80] br[80] wl[29] vdd gnd cell_6t
Xbit_r30_c80 bl[80] br[80] wl[30] vdd gnd cell_6t
Xbit_r31_c80 bl[80] br[80] wl[31] vdd gnd cell_6t
Xbit_r32_c80 bl[80] br[80] wl[32] vdd gnd cell_6t
Xbit_r33_c80 bl[80] br[80] wl[33] vdd gnd cell_6t
Xbit_r34_c80 bl[80] br[80] wl[34] vdd gnd cell_6t
Xbit_r35_c80 bl[80] br[80] wl[35] vdd gnd cell_6t
Xbit_r36_c80 bl[80] br[80] wl[36] vdd gnd cell_6t
Xbit_r37_c80 bl[80] br[80] wl[37] vdd gnd cell_6t
Xbit_r38_c80 bl[80] br[80] wl[38] vdd gnd cell_6t
Xbit_r39_c80 bl[80] br[80] wl[39] vdd gnd cell_6t
Xbit_r40_c80 bl[80] br[80] wl[40] vdd gnd cell_6t
Xbit_r41_c80 bl[80] br[80] wl[41] vdd gnd cell_6t
Xbit_r42_c80 bl[80] br[80] wl[42] vdd gnd cell_6t
Xbit_r43_c80 bl[80] br[80] wl[43] vdd gnd cell_6t
Xbit_r44_c80 bl[80] br[80] wl[44] vdd gnd cell_6t
Xbit_r45_c80 bl[80] br[80] wl[45] vdd gnd cell_6t
Xbit_r46_c80 bl[80] br[80] wl[46] vdd gnd cell_6t
Xbit_r47_c80 bl[80] br[80] wl[47] vdd gnd cell_6t
Xbit_r48_c80 bl[80] br[80] wl[48] vdd gnd cell_6t
Xbit_r49_c80 bl[80] br[80] wl[49] vdd gnd cell_6t
Xbit_r50_c80 bl[80] br[80] wl[50] vdd gnd cell_6t
Xbit_r51_c80 bl[80] br[80] wl[51] vdd gnd cell_6t
Xbit_r52_c80 bl[80] br[80] wl[52] vdd gnd cell_6t
Xbit_r53_c80 bl[80] br[80] wl[53] vdd gnd cell_6t
Xbit_r54_c80 bl[80] br[80] wl[54] vdd gnd cell_6t
Xbit_r55_c80 bl[80] br[80] wl[55] vdd gnd cell_6t
Xbit_r56_c80 bl[80] br[80] wl[56] vdd gnd cell_6t
Xbit_r57_c80 bl[80] br[80] wl[57] vdd gnd cell_6t
Xbit_r58_c80 bl[80] br[80] wl[58] vdd gnd cell_6t
Xbit_r59_c80 bl[80] br[80] wl[59] vdd gnd cell_6t
Xbit_r60_c80 bl[80] br[80] wl[60] vdd gnd cell_6t
Xbit_r61_c80 bl[80] br[80] wl[61] vdd gnd cell_6t
Xbit_r62_c80 bl[80] br[80] wl[62] vdd gnd cell_6t
Xbit_r63_c80 bl[80] br[80] wl[63] vdd gnd cell_6t
Xbit_r0_c81 bl[81] br[81] wl[0] vdd gnd cell_6t
Xbit_r1_c81 bl[81] br[81] wl[1] vdd gnd cell_6t
Xbit_r2_c81 bl[81] br[81] wl[2] vdd gnd cell_6t
Xbit_r3_c81 bl[81] br[81] wl[3] vdd gnd cell_6t
Xbit_r4_c81 bl[81] br[81] wl[4] vdd gnd cell_6t
Xbit_r5_c81 bl[81] br[81] wl[5] vdd gnd cell_6t
Xbit_r6_c81 bl[81] br[81] wl[6] vdd gnd cell_6t
Xbit_r7_c81 bl[81] br[81] wl[7] vdd gnd cell_6t
Xbit_r8_c81 bl[81] br[81] wl[8] vdd gnd cell_6t
Xbit_r9_c81 bl[81] br[81] wl[9] vdd gnd cell_6t
Xbit_r10_c81 bl[81] br[81] wl[10] vdd gnd cell_6t
Xbit_r11_c81 bl[81] br[81] wl[11] vdd gnd cell_6t
Xbit_r12_c81 bl[81] br[81] wl[12] vdd gnd cell_6t
Xbit_r13_c81 bl[81] br[81] wl[13] vdd gnd cell_6t
Xbit_r14_c81 bl[81] br[81] wl[14] vdd gnd cell_6t
Xbit_r15_c81 bl[81] br[81] wl[15] vdd gnd cell_6t
Xbit_r16_c81 bl[81] br[81] wl[16] vdd gnd cell_6t
Xbit_r17_c81 bl[81] br[81] wl[17] vdd gnd cell_6t
Xbit_r18_c81 bl[81] br[81] wl[18] vdd gnd cell_6t
Xbit_r19_c81 bl[81] br[81] wl[19] vdd gnd cell_6t
Xbit_r20_c81 bl[81] br[81] wl[20] vdd gnd cell_6t
Xbit_r21_c81 bl[81] br[81] wl[21] vdd gnd cell_6t
Xbit_r22_c81 bl[81] br[81] wl[22] vdd gnd cell_6t
Xbit_r23_c81 bl[81] br[81] wl[23] vdd gnd cell_6t
Xbit_r24_c81 bl[81] br[81] wl[24] vdd gnd cell_6t
Xbit_r25_c81 bl[81] br[81] wl[25] vdd gnd cell_6t
Xbit_r26_c81 bl[81] br[81] wl[26] vdd gnd cell_6t
Xbit_r27_c81 bl[81] br[81] wl[27] vdd gnd cell_6t
Xbit_r28_c81 bl[81] br[81] wl[28] vdd gnd cell_6t
Xbit_r29_c81 bl[81] br[81] wl[29] vdd gnd cell_6t
Xbit_r30_c81 bl[81] br[81] wl[30] vdd gnd cell_6t
Xbit_r31_c81 bl[81] br[81] wl[31] vdd gnd cell_6t
Xbit_r32_c81 bl[81] br[81] wl[32] vdd gnd cell_6t
Xbit_r33_c81 bl[81] br[81] wl[33] vdd gnd cell_6t
Xbit_r34_c81 bl[81] br[81] wl[34] vdd gnd cell_6t
Xbit_r35_c81 bl[81] br[81] wl[35] vdd gnd cell_6t
Xbit_r36_c81 bl[81] br[81] wl[36] vdd gnd cell_6t
Xbit_r37_c81 bl[81] br[81] wl[37] vdd gnd cell_6t
Xbit_r38_c81 bl[81] br[81] wl[38] vdd gnd cell_6t
Xbit_r39_c81 bl[81] br[81] wl[39] vdd gnd cell_6t
Xbit_r40_c81 bl[81] br[81] wl[40] vdd gnd cell_6t
Xbit_r41_c81 bl[81] br[81] wl[41] vdd gnd cell_6t
Xbit_r42_c81 bl[81] br[81] wl[42] vdd gnd cell_6t
Xbit_r43_c81 bl[81] br[81] wl[43] vdd gnd cell_6t
Xbit_r44_c81 bl[81] br[81] wl[44] vdd gnd cell_6t
Xbit_r45_c81 bl[81] br[81] wl[45] vdd gnd cell_6t
Xbit_r46_c81 bl[81] br[81] wl[46] vdd gnd cell_6t
Xbit_r47_c81 bl[81] br[81] wl[47] vdd gnd cell_6t
Xbit_r48_c81 bl[81] br[81] wl[48] vdd gnd cell_6t
Xbit_r49_c81 bl[81] br[81] wl[49] vdd gnd cell_6t
Xbit_r50_c81 bl[81] br[81] wl[50] vdd gnd cell_6t
Xbit_r51_c81 bl[81] br[81] wl[51] vdd gnd cell_6t
Xbit_r52_c81 bl[81] br[81] wl[52] vdd gnd cell_6t
Xbit_r53_c81 bl[81] br[81] wl[53] vdd gnd cell_6t
Xbit_r54_c81 bl[81] br[81] wl[54] vdd gnd cell_6t
Xbit_r55_c81 bl[81] br[81] wl[55] vdd gnd cell_6t
Xbit_r56_c81 bl[81] br[81] wl[56] vdd gnd cell_6t
Xbit_r57_c81 bl[81] br[81] wl[57] vdd gnd cell_6t
Xbit_r58_c81 bl[81] br[81] wl[58] vdd gnd cell_6t
Xbit_r59_c81 bl[81] br[81] wl[59] vdd gnd cell_6t
Xbit_r60_c81 bl[81] br[81] wl[60] vdd gnd cell_6t
Xbit_r61_c81 bl[81] br[81] wl[61] vdd gnd cell_6t
Xbit_r62_c81 bl[81] br[81] wl[62] vdd gnd cell_6t
Xbit_r63_c81 bl[81] br[81] wl[63] vdd gnd cell_6t
Xbit_r0_c82 bl[82] br[82] wl[0] vdd gnd cell_6t
Xbit_r1_c82 bl[82] br[82] wl[1] vdd gnd cell_6t
Xbit_r2_c82 bl[82] br[82] wl[2] vdd gnd cell_6t
Xbit_r3_c82 bl[82] br[82] wl[3] vdd gnd cell_6t
Xbit_r4_c82 bl[82] br[82] wl[4] vdd gnd cell_6t
Xbit_r5_c82 bl[82] br[82] wl[5] vdd gnd cell_6t
Xbit_r6_c82 bl[82] br[82] wl[6] vdd gnd cell_6t
Xbit_r7_c82 bl[82] br[82] wl[7] vdd gnd cell_6t
Xbit_r8_c82 bl[82] br[82] wl[8] vdd gnd cell_6t
Xbit_r9_c82 bl[82] br[82] wl[9] vdd gnd cell_6t
Xbit_r10_c82 bl[82] br[82] wl[10] vdd gnd cell_6t
Xbit_r11_c82 bl[82] br[82] wl[11] vdd gnd cell_6t
Xbit_r12_c82 bl[82] br[82] wl[12] vdd gnd cell_6t
Xbit_r13_c82 bl[82] br[82] wl[13] vdd gnd cell_6t
Xbit_r14_c82 bl[82] br[82] wl[14] vdd gnd cell_6t
Xbit_r15_c82 bl[82] br[82] wl[15] vdd gnd cell_6t
Xbit_r16_c82 bl[82] br[82] wl[16] vdd gnd cell_6t
Xbit_r17_c82 bl[82] br[82] wl[17] vdd gnd cell_6t
Xbit_r18_c82 bl[82] br[82] wl[18] vdd gnd cell_6t
Xbit_r19_c82 bl[82] br[82] wl[19] vdd gnd cell_6t
Xbit_r20_c82 bl[82] br[82] wl[20] vdd gnd cell_6t
Xbit_r21_c82 bl[82] br[82] wl[21] vdd gnd cell_6t
Xbit_r22_c82 bl[82] br[82] wl[22] vdd gnd cell_6t
Xbit_r23_c82 bl[82] br[82] wl[23] vdd gnd cell_6t
Xbit_r24_c82 bl[82] br[82] wl[24] vdd gnd cell_6t
Xbit_r25_c82 bl[82] br[82] wl[25] vdd gnd cell_6t
Xbit_r26_c82 bl[82] br[82] wl[26] vdd gnd cell_6t
Xbit_r27_c82 bl[82] br[82] wl[27] vdd gnd cell_6t
Xbit_r28_c82 bl[82] br[82] wl[28] vdd gnd cell_6t
Xbit_r29_c82 bl[82] br[82] wl[29] vdd gnd cell_6t
Xbit_r30_c82 bl[82] br[82] wl[30] vdd gnd cell_6t
Xbit_r31_c82 bl[82] br[82] wl[31] vdd gnd cell_6t
Xbit_r32_c82 bl[82] br[82] wl[32] vdd gnd cell_6t
Xbit_r33_c82 bl[82] br[82] wl[33] vdd gnd cell_6t
Xbit_r34_c82 bl[82] br[82] wl[34] vdd gnd cell_6t
Xbit_r35_c82 bl[82] br[82] wl[35] vdd gnd cell_6t
Xbit_r36_c82 bl[82] br[82] wl[36] vdd gnd cell_6t
Xbit_r37_c82 bl[82] br[82] wl[37] vdd gnd cell_6t
Xbit_r38_c82 bl[82] br[82] wl[38] vdd gnd cell_6t
Xbit_r39_c82 bl[82] br[82] wl[39] vdd gnd cell_6t
Xbit_r40_c82 bl[82] br[82] wl[40] vdd gnd cell_6t
Xbit_r41_c82 bl[82] br[82] wl[41] vdd gnd cell_6t
Xbit_r42_c82 bl[82] br[82] wl[42] vdd gnd cell_6t
Xbit_r43_c82 bl[82] br[82] wl[43] vdd gnd cell_6t
Xbit_r44_c82 bl[82] br[82] wl[44] vdd gnd cell_6t
Xbit_r45_c82 bl[82] br[82] wl[45] vdd gnd cell_6t
Xbit_r46_c82 bl[82] br[82] wl[46] vdd gnd cell_6t
Xbit_r47_c82 bl[82] br[82] wl[47] vdd gnd cell_6t
Xbit_r48_c82 bl[82] br[82] wl[48] vdd gnd cell_6t
Xbit_r49_c82 bl[82] br[82] wl[49] vdd gnd cell_6t
Xbit_r50_c82 bl[82] br[82] wl[50] vdd gnd cell_6t
Xbit_r51_c82 bl[82] br[82] wl[51] vdd gnd cell_6t
Xbit_r52_c82 bl[82] br[82] wl[52] vdd gnd cell_6t
Xbit_r53_c82 bl[82] br[82] wl[53] vdd gnd cell_6t
Xbit_r54_c82 bl[82] br[82] wl[54] vdd gnd cell_6t
Xbit_r55_c82 bl[82] br[82] wl[55] vdd gnd cell_6t
Xbit_r56_c82 bl[82] br[82] wl[56] vdd gnd cell_6t
Xbit_r57_c82 bl[82] br[82] wl[57] vdd gnd cell_6t
Xbit_r58_c82 bl[82] br[82] wl[58] vdd gnd cell_6t
Xbit_r59_c82 bl[82] br[82] wl[59] vdd gnd cell_6t
Xbit_r60_c82 bl[82] br[82] wl[60] vdd gnd cell_6t
Xbit_r61_c82 bl[82] br[82] wl[61] vdd gnd cell_6t
Xbit_r62_c82 bl[82] br[82] wl[62] vdd gnd cell_6t
Xbit_r63_c82 bl[82] br[82] wl[63] vdd gnd cell_6t
Xbit_r0_c83 bl[83] br[83] wl[0] vdd gnd cell_6t
Xbit_r1_c83 bl[83] br[83] wl[1] vdd gnd cell_6t
Xbit_r2_c83 bl[83] br[83] wl[2] vdd gnd cell_6t
Xbit_r3_c83 bl[83] br[83] wl[3] vdd gnd cell_6t
Xbit_r4_c83 bl[83] br[83] wl[4] vdd gnd cell_6t
Xbit_r5_c83 bl[83] br[83] wl[5] vdd gnd cell_6t
Xbit_r6_c83 bl[83] br[83] wl[6] vdd gnd cell_6t
Xbit_r7_c83 bl[83] br[83] wl[7] vdd gnd cell_6t
Xbit_r8_c83 bl[83] br[83] wl[8] vdd gnd cell_6t
Xbit_r9_c83 bl[83] br[83] wl[9] vdd gnd cell_6t
Xbit_r10_c83 bl[83] br[83] wl[10] vdd gnd cell_6t
Xbit_r11_c83 bl[83] br[83] wl[11] vdd gnd cell_6t
Xbit_r12_c83 bl[83] br[83] wl[12] vdd gnd cell_6t
Xbit_r13_c83 bl[83] br[83] wl[13] vdd gnd cell_6t
Xbit_r14_c83 bl[83] br[83] wl[14] vdd gnd cell_6t
Xbit_r15_c83 bl[83] br[83] wl[15] vdd gnd cell_6t
Xbit_r16_c83 bl[83] br[83] wl[16] vdd gnd cell_6t
Xbit_r17_c83 bl[83] br[83] wl[17] vdd gnd cell_6t
Xbit_r18_c83 bl[83] br[83] wl[18] vdd gnd cell_6t
Xbit_r19_c83 bl[83] br[83] wl[19] vdd gnd cell_6t
Xbit_r20_c83 bl[83] br[83] wl[20] vdd gnd cell_6t
Xbit_r21_c83 bl[83] br[83] wl[21] vdd gnd cell_6t
Xbit_r22_c83 bl[83] br[83] wl[22] vdd gnd cell_6t
Xbit_r23_c83 bl[83] br[83] wl[23] vdd gnd cell_6t
Xbit_r24_c83 bl[83] br[83] wl[24] vdd gnd cell_6t
Xbit_r25_c83 bl[83] br[83] wl[25] vdd gnd cell_6t
Xbit_r26_c83 bl[83] br[83] wl[26] vdd gnd cell_6t
Xbit_r27_c83 bl[83] br[83] wl[27] vdd gnd cell_6t
Xbit_r28_c83 bl[83] br[83] wl[28] vdd gnd cell_6t
Xbit_r29_c83 bl[83] br[83] wl[29] vdd gnd cell_6t
Xbit_r30_c83 bl[83] br[83] wl[30] vdd gnd cell_6t
Xbit_r31_c83 bl[83] br[83] wl[31] vdd gnd cell_6t
Xbit_r32_c83 bl[83] br[83] wl[32] vdd gnd cell_6t
Xbit_r33_c83 bl[83] br[83] wl[33] vdd gnd cell_6t
Xbit_r34_c83 bl[83] br[83] wl[34] vdd gnd cell_6t
Xbit_r35_c83 bl[83] br[83] wl[35] vdd gnd cell_6t
Xbit_r36_c83 bl[83] br[83] wl[36] vdd gnd cell_6t
Xbit_r37_c83 bl[83] br[83] wl[37] vdd gnd cell_6t
Xbit_r38_c83 bl[83] br[83] wl[38] vdd gnd cell_6t
Xbit_r39_c83 bl[83] br[83] wl[39] vdd gnd cell_6t
Xbit_r40_c83 bl[83] br[83] wl[40] vdd gnd cell_6t
Xbit_r41_c83 bl[83] br[83] wl[41] vdd gnd cell_6t
Xbit_r42_c83 bl[83] br[83] wl[42] vdd gnd cell_6t
Xbit_r43_c83 bl[83] br[83] wl[43] vdd gnd cell_6t
Xbit_r44_c83 bl[83] br[83] wl[44] vdd gnd cell_6t
Xbit_r45_c83 bl[83] br[83] wl[45] vdd gnd cell_6t
Xbit_r46_c83 bl[83] br[83] wl[46] vdd gnd cell_6t
Xbit_r47_c83 bl[83] br[83] wl[47] vdd gnd cell_6t
Xbit_r48_c83 bl[83] br[83] wl[48] vdd gnd cell_6t
Xbit_r49_c83 bl[83] br[83] wl[49] vdd gnd cell_6t
Xbit_r50_c83 bl[83] br[83] wl[50] vdd gnd cell_6t
Xbit_r51_c83 bl[83] br[83] wl[51] vdd gnd cell_6t
Xbit_r52_c83 bl[83] br[83] wl[52] vdd gnd cell_6t
Xbit_r53_c83 bl[83] br[83] wl[53] vdd gnd cell_6t
Xbit_r54_c83 bl[83] br[83] wl[54] vdd gnd cell_6t
Xbit_r55_c83 bl[83] br[83] wl[55] vdd gnd cell_6t
Xbit_r56_c83 bl[83] br[83] wl[56] vdd gnd cell_6t
Xbit_r57_c83 bl[83] br[83] wl[57] vdd gnd cell_6t
Xbit_r58_c83 bl[83] br[83] wl[58] vdd gnd cell_6t
Xbit_r59_c83 bl[83] br[83] wl[59] vdd gnd cell_6t
Xbit_r60_c83 bl[83] br[83] wl[60] vdd gnd cell_6t
Xbit_r61_c83 bl[83] br[83] wl[61] vdd gnd cell_6t
Xbit_r62_c83 bl[83] br[83] wl[62] vdd gnd cell_6t
Xbit_r63_c83 bl[83] br[83] wl[63] vdd gnd cell_6t
Xbit_r0_c84 bl[84] br[84] wl[0] vdd gnd cell_6t
Xbit_r1_c84 bl[84] br[84] wl[1] vdd gnd cell_6t
Xbit_r2_c84 bl[84] br[84] wl[2] vdd gnd cell_6t
Xbit_r3_c84 bl[84] br[84] wl[3] vdd gnd cell_6t
Xbit_r4_c84 bl[84] br[84] wl[4] vdd gnd cell_6t
Xbit_r5_c84 bl[84] br[84] wl[5] vdd gnd cell_6t
Xbit_r6_c84 bl[84] br[84] wl[6] vdd gnd cell_6t
Xbit_r7_c84 bl[84] br[84] wl[7] vdd gnd cell_6t
Xbit_r8_c84 bl[84] br[84] wl[8] vdd gnd cell_6t
Xbit_r9_c84 bl[84] br[84] wl[9] vdd gnd cell_6t
Xbit_r10_c84 bl[84] br[84] wl[10] vdd gnd cell_6t
Xbit_r11_c84 bl[84] br[84] wl[11] vdd gnd cell_6t
Xbit_r12_c84 bl[84] br[84] wl[12] vdd gnd cell_6t
Xbit_r13_c84 bl[84] br[84] wl[13] vdd gnd cell_6t
Xbit_r14_c84 bl[84] br[84] wl[14] vdd gnd cell_6t
Xbit_r15_c84 bl[84] br[84] wl[15] vdd gnd cell_6t
Xbit_r16_c84 bl[84] br[84] wl[16] vdd gnd cell_6t
Xbit_r17_c84 bl[84] br[84] wl[17] vdd gnd cell_6t
Xbit_r18_c84 bl[84] br[84] wl[18] vdd gnd cell_6t
Xbit_r19_c84 bl[84] br[84] wl[19] vdd gnd cell_6t
Xbit_r20_c84 bl[84] br[84] wl[20] vdd gnd cell_6t
Xbit_r21_c84 bl[84] br[84] wl[21] vdd gnd cell_6t
Xbit_r22_c84 bl[84] br[84] wl[22] vdd gnd cell_6t
Xbit_r23_c84 bl[84] br[84] wl[23] vdd gnd cell_6t
Xbit_r24_c84 bl[84] br[84] wl[24] vdd gnd cell_6t
Xbit_r25_c84 bl[84] br[84] wl[25] vdd gnd cell_6t
Xbit_r26_c84 bl[84] br[84] wl[26] vdd gnd cell_6t
Xbit_r27_c84 bl[84] br[84] wl[27] vdd gnd cell_6t
Xbit_r28_c84 bl[84] br[84] wl[28] vdd gnd cell_6t
Xbit_r29_c84 bl[84] br[84] wl[29] vdd gnd cell_6t
Xbit_r30_c84 bl[84] br[84] wl[30] vdd gnd cell_6t
Xbit_r31_c84 bl[84] br[84] wl[31] vdd gnd cell_6t
Xbit_r32_c84 bl[84] br[84] wl[32] vdd gnd cell_6t
Xbit_r33_c84 bl[84] br[84] wl[33] vdd gnd cell_6t
Xbit_r34_c84 bl[84] br[84] wl[34] vdd gnd cell_6t
Xbit_r35_c84 bl[84] br[84] wl[35] vdd gnd cell_6t
Xbit_r36_c84 bl[84] br[84] wl[36] vdd gnd cell_6t
Xbit_r37_c84 bl[84] br[84] wl[37] vdd gnd cell_6t
Xbit_r38_c84 bl[84] br[84] wl[38] vdd gnd cell_6t
Xbit_r39_c84 bl[84] br[84] wl[39] vdd gnd cell_6t
Xbit_r40_c84 bl[84] br[84] wl[40] vdd gnd cell_6t
Xbit_r41_c84 bl[84] br[84] wl[41] vdd gnd cell_6t
Xbit_r42_c84 bl[84] br[84] wl[42] vdd gnd cell_6t
Xbit_r43_c84 bl[84] br[84] wl[43] vdd gnd cell_6t
Xbit_r44_c84 bl[84] br[84] wl[44] vdd gnd cell_6t
Xbit_r45_c84 bl[84] br[84] wl[45] vdd gnd cell_6t
Xbit_r46_c84 bl[84] br[84] wl[46] vdd gnd cell_6t
Xbit_r47_c84 bl[84] br[84] wl[47] vdd gnd cell_6t
Xbit_r48_c84 bl[84] br[84] wl[48] vdd gnd cell_6t
Xbit_r49_c84 bl[84] br[84] wl[49] vdd gnd cell_6t
Xbit_r50_c84 bl[84] br[84] wl[50] vdd gnd cell_6t
Xbit_r51_c84 bl[84] br[84] wl[51] vdd gnd cell_6t
Xbit_r52_c84 bl[84] br[84] wl[52] vdd gnd cell_6t
Xbit_r53_c84 bl[84] br[84] wl[53] vdd gnd cell_6t
Xbit_r54_c84 bl[84] br[84] wl[54] vdd gnd cell_6t
Xbit_r55_c84 bl[84] br[84] wl[55] vdd gnd cell_6t
Xbit_r56_c84 bl[84] br[84] wl[56] vdd gnd cell_6t
Xbit_r57_c84 bl[84] br[84] wl[57] vdd gnd cell_6t
Xbit_r58_c84 bl[84] br[84] wl[58] vdd gnd cell_6t
Xbit_r59_c84 bl[84] br[84] wl[59] vdd gnd cell_6t
Xbit_r60_c84 bl[84] br[84] wl[60] vdd gnd cell_6t
Xbit_r61_c84 bl[84] br[84] wl[61] vdd gnd cell_6t
Xbit_r62_c84 bl[84] br[84] wl[62] vdd gnd cell_6t
Xbit_r63_c84 bl[84] br[84] wl[63] vdd gnd cell_6t
Xbit_r0_c85 bl[85] br[85] wl[0] vdd gnd cell_6t
Xbit_r1_c85 bl[85] br[85] wl[1] vdd gnd cell_6t
Xbit_r2_c85 bl[85] br[85] wl[2] vdd gnd cell_6t
Xbit_r3_c85 bl[85] br[85] wl[3] vdd gnd cell_6t
Xbit_r4_c85 bl[85] br[85] wl[4] vdd gnd cell_6t
Xbit_r5_c85 bl[85] br[85] wl[5] vdd gnd cell_6t
Xbit_r6_c85 bl[85] br[85] wl[6] vdd gnd cell_6t
Xbit_r7_c85 bl[85] br[85] wl[7] vdd gnd cell_6t
Xbit_r8_c85 bl[85] br[85] wl[8] vdd gnd cell_6t
Xbit_r9_c85 bl[85] br[85] wl[9] vdd gnd cell_6t
Xbit_r10_c85 bl[85] br[85] wl[10] vdd gnd cell_6t
Xbit_r11_c85 bl[85] br[85] wl[11] vdd gnd cell_6t
Xbit_r12_c85 bl[85] br[85] wl[12] vdd gnd cell_6t
Xbit_r13_c85 bl[85] br[85] wl[13] vdd gnd cell_6t
Xbit_r14_c85 bl[85] br[85] wl[14] vdd gnd cell_6t
Xbit_r15_c85 bl[85] br[85] wl[15] vdd gnd cell_6t
Xbit_r16_c85 bl[85] br[85] wl[16] vdd gnd cell_6t
Xbit_r17_c85 bl[85] br[85] wl[17] vdd gnd cell_6t
Xbit_r18_c85 bl[85] br[85] wl[18] vdd gnd cell_6t
Xbit_r19_c85 bl[85] br[85] wl[19] vdd gnd cell_6t
Xbit_r20_c85 bl[85] br[85] wl[20] vdd gnd cell_6t
Xbit_r21_c85 bl[85] br[85] wl[21] vdd gnd cell_6t
Xbit_r22_c85 bl[85] br[85] wl[22] vdd gnd cell_6t
Xbit_r23_c85 bl[85] br[85] wl[23] vdd gnd cell_6t
Xbit_r24_c85 bl[85] br[85] wl[24] vdd gnd cell_6t
Xbit_r25_c85 bl[85] br[85] wl[25] vdd gnd cell_6t
Xbit_r26_c85 bl[85] br[85] wl[26] vdd gnd cell_6t
Xbit_r27_c85 bl[85] br[85] wl[27] vdd gnd cell_6t
Xbit_r28_c85 bl[85] br[85] wl[28] vdd gnd cell_6t
Xbit_r29_c85 bl[85] br[85] wl[29] vdd gnd cell_6t
Xbit_r30_c85 bl[85] br[85] wl[30] vdd gnd cell_6t
Xbit_r31_c85 bl[85] br[85] wl[31] vdd gnd cell_6t
Xbit_r32_c85 bl[85] br[85] wl[32] vdd gnd cell_6t
Xbit_r33_c85 bl[85] br[85] wl[33] vdd gnd cell_6t
Xbit_r34_c85 bl[85] br[85] wl[34] vdd gnd cell_6t
Xbit_r35_c85 bl[85] br[85] wl[35] vdd gnd cell_6t
Xbit_r36_c85 bl[85] br[85] wl[36] vdd gnd cell_6t
Xbit_r37_c85 bl[85] br[85] wl[37] vdd gnd cell_6t
Xbit_r38_c85 bl[85] br[85] wl[38] vdd gnd cell_6t
Xbit_r39_c85 bl[85] br[85] wl[39] vdd gnd cell_6t
Xbit_r40_c85 bl[85] br[85] wl[40] vdd gnd cell_6t
Xbit_r41_c85 bl[85] br[85] wl[41] vdd gnd cell_6t
Xbit_r42_c85 bl[85] br[85] wl[42] vdd gnd cell_6t
Xbit_r43_c85 bl[85] br[85] wl[43] vdd gnd cell_6t
Xbit_r44_c85 bl[85] br[85] wl[44] vdd gnd cell_6t
Xbit_r45_c85 bl[85] br[85] wl[45] vdd gnd cell_6t
Xbit_r46_c85 bl[85] br[85] wl[46] vdd gnd cell_6t
Xbit_r47_c85 bl[85] br[85] wl[47] vdd gnd cell_6t
Xbit_r48_c85 bl[85] br[85] wl[48] vdd gnd cell_6t
Xbit_r49_c85 bl[85] br[85] wl[49] vdd gnd cell_6t
Xbit_r50_c85 bl[85] br[85] wl[50] vdd gnd cell_6t
Xbit_r51_c85 bl[85] br[85] wl[51] vdd gnd cell_6t
Xbit_r52_c85 bl[85] br[85] wl[52] vdd gnd cell_6t
Xbit_r53_c85 bl[85] br[85] wl[53] vdd gnd cell_6t
Xbit_r54_c85 bl[85] br[85] wl[54] vdd gnd cell_6t
Xbit_r55_c85 bl[85] br[85] wl[55] vdd gnd cell_6t
Xbit_r56_c85 bl[85] br[85] wl[56] vdd gnd cell_6t
Xbit_r57_c85 bl[85] br[85] wl[57] vdd gnd cell_6t
Xbit_r58_c85 bl[85] br[85] wl[58] vdd gnd cell_6t
Xbit_r59_c85 bl[85] br[85] wl[59] vdd gnd cell_6t
Xbit_r60_c85 bl[85] br[85] wl[60] vdd gnd cell_6t
Xbit_r61_c85 bl[85] br[85] wl[61] vdd gnd cell_6t
Xbit_r62_c85 bl[85] br[85] wl[62] vdd gnd cell_6t
Xbit_r63_c85 bl[85] br[85] wl[63] vdd gnd cell_6t
Xbit_r0_c86 bl[86] br[86] wl[0] vdd gnd cell_6t
Xbit_r1_c86 bl[86] br[86] wl[1] vdd gnd cell_6t
Xbit_r2_c86 bl[86] br[86] wl[2] vdd gnd cell_6t
Xbit_r3_c86 bl[86] br[86] wl[3] vdd gnd cell_6t
Xbit_r4_c86 bl[86] br[86] wl[4] vdd gnd cell_6t
Xbit_r5_c86 bl[86] br[86] wl[5] vdd gnd cell_6t
Xbit_r6_c86 bl[86] br[86] wl[6] vdd gnd cell_6t
Xbit_r7_c86 bl[86] br[86] wl[7] vdd gnd cell_6t
Xbit_r8_c86 bl[86] br[86] wl[8] vdd gnd cell_6t
Xbit_r9_c86 bl[86] br[86] wl[9] vdd gnd cell_6t
Xbit_r10_c86 bl[86] br[86] wl[10] vdd gnd cell_6t
Xbit_r11_c86 bl[86] br[86] wl[11] vdd gnd cell_6t
Xbit_r12_c86 bl[86] br[86] wl[12] vdd gnd cell_6t
Xbit_r13_c86 bl[86] br[86] wl[13] vdd gnd cell_6t
Xbit_r14_c86 bl[86] br[86] wl[14] vdd gnd cell_6t
Xbit_r15_c86 bl[86] br[86] wl[15] vdd gnd cell_6t
Xbit_r16_c86 bl[86] br[86] wl[16] vdd gnd cell_6t
Xbit_r17_c86 bl[86] br[86] wl[17] vdd gnd cell_6t
Xbit_r18_c86 bl[86] br[86] wl[18] vdd gnd cell_6t
Xbit_r19_c86 bl[86] br[86] wl[19] vdd gnd cell_6t
Xbit_r20_c86 bl[86] br[86] wl[20] vdd gnd cell_6t
Xbit_r21_c86 bl[86] br[86] wl[21] vdd gnd cell_6t
Xbit_r22_c86 bl[86] br[86] wl[22] vdd gnd cell_6t
Xbit_r23_c86 bl[86] br[86] wl[23] vdd gnd cell_6t
Xbit_r24_c86 bl[86] br[86] wl[24] vdd gnd cell_6t
Xbit_r25_c86 bl[86] br[86] wl[25] vdd gnd cell_6t
Xbit_r26_c86 bl[86] br[86] wl[26] vdd gnd cell_6t
Xbit_r27_c86 bl[86] br[86] wl[27] vdd gnd cell_6t
Xbit_r28_c86 bl[86] br[86] wl[28] vdd gnd cell_6t
Xbit_r29_c86 bl[86] br[86] wl[29] vdd gnd cell_6t
Xbit_r30_c86 bl[86] br[86] wl[30] vdd gnd cell_6t
Xbit_r31_c86 bl[86] br[86] wl[31] vdd gnd cell_6t
Xbit_r32_c86 bl[86] br[86] wl[32] vdd gnd cell_6t
Xbit_r33_c86 bl[86] br[86] wl[33] vdd gnd cell_6t
Xbit_r34_c86 bl[86] br[86] wl[34] vdd gnd cell_6t
Xbit_r35_c86 bl[86] br[86] wl[35] vdd gnd cell_6t
Xbit_r36_c86 bl[86] br[86] wl[36] vdd gnd cell_6t
Xbit_r37_c86 bl[86] br[86] wl[37] vdd gnd cell_6t
Xbit_r38_c86 bl[86] br[86] wl[38] vdd gnd cell_6t
Xbit_r39_c86 bl[86] br[86] wl[39] vdd gnd cell_6t
Xbit_r40_c86 bl[86] br[86] wl[40] vdd gnd cell_6t
Xbit_r41_c86 bl[86] br[86] wl[41] vdd gnd cell_6t
Xbit_r42_c86 bl[86] br[86] wl[42] vdd gnd cell_6t
Xbit_r43_c86 bl[86] br[86] wl[43] vdd gnd cell_6t
Xbit_r44_c86 bl[86] br[86] wl[44] vdd gnd cell_6t
Xbit_r45_c86 bl[86] br[86] wl[45] vdd gnd cell_6t
Xbit_r46_c86 bl[86] br[86] wl[46] vdd gnd cell_6t
Xbit_r47_c86 bl[86] br[86] wl[47] vdd gnd cell_6t
Xbit_r48_c86 bl[86] br[86] wl[48] vdd gnd cell_6t
Xbit_r49_c86 bl[86] br[86] wl[49] vdd gnd cell_6t
Xbit_r50_c86 bl[86] br[86] wl[50] vdd gnd cell_6t
Xbit_r51_c86 bl[86] br[86] wl[51] vdd gnd cell_6t
Xbit_r52_c86 bl[86] br[86] wl[52] vdd gnd cell_6t
Xbit_r53_c86 bl[86] br[86] wl[53] vdd gnd cell_6t
Xbit_r54_c86 bl[86] br[86] wl[54] vdd gnd cell_6t
Xbit_r55_c86 bl[86] br[86] wl[55] vdd gnd cell_6t
Xbit_r56_c86 bl[86] br[86] wl[56] vdd gnd cell_6t
Xbit_r57_c86 bl[86] br[86] wl[57] vdd gnd cell_6t
Xbit_r58_c86 bl[86] br[86] wl[58] vdd gnd cell_6t
Xbit_r59_c86 bl[86] br[86] wl[59] vdd gnd cell_6t
Xbit_r60_c86 bl[86] br[86] wl[60] vdd gnd cell_6t
Xbit_r61_c86 bl[86] br[86] wl[61] vdd gnd cell_6t
Xbit_r62_c86 bl[86] br[86] wl[62] vdd gnd cell_6t
Xbit_r63_c86 bl[86] br[86] wl[63] vdd gnd cell_6t
Xbit_r0_c87 bl[87] br[87] wl[0] vdd gnd cell_6t
Xbit_r1_c87 bl[87] br[87] wl[1] vdd gnd cell_6t
Xbit_r2_c87 bl[87] br[87] wl[2] vdd gnd cell_6t
Xbit_r3_c87 bl[87] br[87] wl[3] vdd gnd cell_6t
Xbit_r4_c87 bl[87] br[87] wl[4] vdd gnd cell_6t
Xbit_r5_c87 bl[87] br[87] wl[5] vdd gnd cell_6t
Xbit_r6_c87 bl[87] br[87] wl[6] vdd gnd cell_6t
Xbit_r7_c87 bl[87] br[87] wl[7] vdd gnd cell_6t
Xbit_r8_c87 bl[87] br[87] wl[8] vdd gnd cell_6t
Xbit_r9_c87 bl[87] br[87] wl[9] vdd gnd cell_6t
Xbit_r10_c87 bl[87] br[87] wl[10] vdd gnd cell_6t
Xbit_r11_c87 bl[87] br[87] wl[11] vdd gnd cell_6t
Xbit_r12_c87 bl[87] br[87] wl[12] vdd gnd cell_6t
Xbit_r13_c87 bl[87] br[87] wl[13] vdd gnd cell_6t
Xbit_r14_c87 bl[87] br[87] wl[14] vdd gnd cell_6t
Xbit_r15_c87 bl[87] br[87] wl[15] vdd gnd cell_6t
Xbit_r16_c87 bl[87] br[87] wl[16] vdd gnd cell_6t
Xbit_r17_c87 bl[87] br[87] wl[17] vdd gnd cell_6t
Xbit_r18_c87 bl[87] br[87] wl[18] vdd gnd cell_6t
Xbit_r19_c87 bl[87] br[87] wl[19] vdd gnd cell_6t
Xbit_r20_c87 bl[87] br[87] wl[20] vdd gnd cell_6t
Xbit_r21_c87 bl[87] br[87] wl[21] vdd gnd cell_6t
Xbit_r22_c87 bl[87] br[87] wl[22] vdd gnd cell_6t
Xbit_r23_c87 bl[87] br[87] wl[23] vdd gnd cell_6t
Xbit_r24_c87 bl[87] br[87] wl[24] vdd gnd cell_6t
Xbit_r25_c87 bl[87] br[87] wl[25] vdd gnd cell_6t
Xbit_r26_c87 bl[87] br[87] wl[26] vdd gnd cell_6t
Xbit_r27_c87 bl[87] br[87] wl[27] vdd gnd cell_6t
Xbit_r28_c87 bl[87] br[87] wl[28] vdd gnd cell_6t
Xbit_r29_c87 bl[87] br[87] wl[29] vdd gnd cell_6t
Xbit_r30_c87 bl[87] br[87] wl[30] vdd gnd cell_6t
Xbit_r31_c87 bl[87] br[87] wl[31] vdd gnd cell_6t
Xbit_r32_c87 bl[87] br[87] wl[32] vdd gnd cell_6t
Xbit_r33_c87 bl[87] br[87] wl[33] vdd gnd cell_6t
Xbit_r34_c87 bl[87] br[87] wl[34] vdd gnd cell_6t
Xbit_r35_c87 bl[87] br[87] wl[35] vdd gnd cell_6t
Xbit_r36_c87 bl[87] br[87] wl[36] vdd gnd cell_6t
Xbit_r37_c87 bl[87] br[87] wl[37] vdd gnd cell_6t
Xbit_r38_c87 bl[87] br[87] wl[38] vdd gnd cell_6t
Xbit_r39_c87 bl[87] br[87] wl[39] vdd gnd cell_6t
Xbit_r40_c87 bl[87] br[87] wl[40] vdd gnd cell_6t
Xbit_r41_c87 bl[87] br[87] wl[41] vdd gnd cell_6t
Xbit_r42_c87 bl[87] br[87] wl[42] vdd gnd cell_6t
Xbit_r43_c87 bl[87] br[87] wl[43] vdd gnd cell_6t
Xbit_r44_c87 bl[87] br[87] wl[44] vdd gnd cell_6t
Xbit_r45_c87 bl[87] br[87] wl[45] vdd gnd cell_6t
Xbit_r46_c87 bl[87] br[87] wl[46] vdd gnd cell_6t
Xbit_r47_c87 bl[87] br[87] wl[47] vdd gnd cell_6t
Xbit_r48_c87 bl[87] br[87] wl[48] vdd gnd cell_6t
Xbit_r49_c87 bl[87] br[87] wl[49] vdd gnd cell_6t
Xbit_r50_c87 bl[87] br[87] wl[50] vdd gnd cell_6t
Xbit_r51_c87 bl[87] br[87] wl[51] vdd gnd cell_6t
Xbit_r52_c87 bl[87] br[87] wl[52] vdd gnd cell_6t
Xbit_r53_c87 bl[87] br[87] wl[53] vdd gnd cell_6t
Xbit_r54_c87 bl[87] br[87] wl[54] vdd gnd cell_6t
Xbit_r55_c87 bl[87] br[87] wl[55] vdd gnd cell_6t
Xbit_r56_c87 bl[87] br[87] wl[56] vdd gnd cell_6t
Xbit_r57_c87 bl[87] br[87] wl[57] vdd gnd cell_6t
Xbit_r58_c87 bl[87] br[87] wl[58] vdd gnd cell_6t
Xbit_r59_c87 bl[87] br[87] wl[59] vdd gnd cell_6t
Xbit_r60_c87 bl[87] br[87] wl[60] vdd gnd cell_6t
Xbit_r61_c87 bl[87] br[87] wl[61] vdd gnd cell_6t
Xbit_r62_c87 bl[87] br[87] wl[62] vdd gnd cell_6t
Xbit_r63_c87 bl[87] br[87] wl[63] vdd gnd cell_6t
Xbit_r0_c88 bl[88] br[88] wl[0] vdd gnd cell_6t
Xbit_r1_c88 bl[88] br[88] wl[1] vdd gnd cell_6t
Xbit_r2_c88 bl[88] br[88] wl[2] vdd gnd cell_6t
Xbit_r3_c88 bl[88] br[88] wl[3] vdd gnd cell_6t
Xbit_r4_c88 bl[88] br[88] wl[4] vdd gnd cell_6t
Xbit_r5_c88 bl[88] br[88] wl[5] vdd gnd cell_6t
Xbit_r6_c88 bl[88] br[88] wl[6] vdd gnd cell_6t
Xbit_r7_c88 bl[88] br[88] wl[7] vdd gnd cell_6t
Xbit_r8_c88 bl[88] br[88] wl[8] vdd gnd cell_6t
Xbit_r9_c88 bl[88] br[88] wl[9] vdd gnd cell_6t
Xbit_r10_c88 bl[88] br[88] wl[10] vdd gnd cell_6t
Xbit_r11_c88 bl[88] br[88] wl[11] vdd gnd cell_6t
Xbit_r12_c88 bl[88] br[88] wl[12] vdd gnd cell_6t
Xbit_r13_c88 bl[88] br[88] wl[13] vdd gnd cell_6t
Xbit_r14_c88 bl[88] br[88] wl[14] vdd gnd cell_6t
Xbit_r15_c88 bl[88] br[88] wl[15] vdd gnd cell_6t
Xbit_r16_c88 bl[88] br[88] wl[16] vdd gnd cell_6t
Xbit_r17_c88 bl[88] br[88] wl[17] vdd gnd cell_6t
Xbit_r18_c88 bl[88] br[88] wl[18] vdd gnd cell_6t
Xbit_r19_c88 bl[88] br[88] wl[19] vdd gnd cell_6t
Xbit_r20_c88 bl[88] br[88] wl[20] vdd gnd cell_6t
Xbit_r21_c88 bl[88] br[88] wl[21] vdd gnd cell_6t
Xbit_r22_c88 bl[88] br[88] wl[22] vdd gnd cell_6t
Xbit_r23_c88 bl[88] br[88] wl[23] vdd gnd cell_6t
Xbit_r24_c88 bl[88] br[88] wl[24] vdd gnd cell_6t
Xbit_r25_c88 bl[88] br[88] wl[25] vdd gnd cell_6t
Xbit_r26_c88 bl[88] br[88] wl[26] vdd gnd cell_6t
Xbit_r27_c88 bl[88] br[88] wl[27] vdd gnd cell_6t
Xbit_r28_c88 bl[88] br[88] wl[28] vdd gnd cell_6t
Xbit_r29_c88 bl[88] br[88] wl[29] vdd gnd cell_6t
Xbit_r30_c88 bl[88] br[88] wl[30] vdd gnd cell_6t
Xbit_r31_c88 bl[88] br[88] wl[31] vdd gnd cell_6t
Xbit_r32_c88 bl[88] br[88] wl[32] vdd gnd cell_6t
Xbit_r33_c88 bl[88] br[88] wl[33] vdd gnd cell_6t
Xbit_r34_c88 bl[88] br[88] wl[34] vdd gnd cell_6t
Xbit_r35_c88 bl[88] br[88] wl[35] vdd gnd cell_6t
Xbit_r36_c88 bl[88] br[88] wl[36] vdd gnd cell_6t
Xbit_r37_c88 bl[88] br[88] wl[37] vdd gnd cell_6t
Xbit_r38_c88 bl[88] br[88] wl[38] vdd gnd cell_6t
Xbit_r39_c88 bl[88] br[88] wl[39] vdd gnd cell_6t
Xbit_r40_c88 bl[88] br[88] wl[40] vdd gnd cell_6t
Xbit_r41_c88 bl[88] br[88] wl[41] vdd gnd cell_6t
Xbit_r42_c88 bl[88] br[88] wl[42] vdd gnd cell_6t
Xbit_r43_c88 bl[88] br[88] wl[43] vdd gnd cell_6t
Xbit_r44_c88 bl[88] br[88] wl[44] vdd gnd cell_6t
Xbit_r45_c88 bl[88] br[88] wl[45] vdd gnd cell_6t
Xbit_r46_c88 bl[88] br[88] wl[46] vdd gnd cell_6t
Xbit_r47_c88 bl[88] br[88] wl[47] vdd gnd cell_6t
Xbit_r48_c88 bl[88] br[88] wl[48] vdd gnd cell_6t
Xbit_r49_c88 bl[88] br[88] wl[49] vdd gnd cell_6t
Xbit_r50_c88 bl[88] br[88] wl[50] vdd gnd cell_6t
Xbit_r51_c88 bl[88] br[88] wl[51] vdd gnd cell_6t
Xbit_r52_c88 bl[88] br[88] wl[52] vdd gnd cell_6t
Xbit_r53_c88 bl[88] br[88] wl[53] vdd gnd cell_6t
Xbit_r54_c88 bl[88] br[88] wl[54] vdd gnd cell_6t
Xbit_r55_c88 bl[88] br[88] wl[55] vdd gnd cell_6t
Xbit_r56_c88 bl[88] br[88] wl[56] vdd gnd cell_6t
Xbit_r57_c88 bl[88] br[88] wl[57] vdd gnd cell_6t
Xbit_r58_c88 bl[88] br[88] wl[58] vdd gnd cell_6t
Xbit_r59_c88 bl[88] br[88] wl[59] vdd gnd cell_6t
Xbit_r60_c88 bl[88] br[88] wl[60] vdd gnd cell_6t
Xbit_r61_c88 bl[88] br[88] wl[61] vdd gnd cell_6t
Xbit_r62_c88 bl[88] br[88] wl[62] vdd gnd cell_6t
Xbit_r63_c88 bl[88] br[88] wl[63] vdd gnd cell_6t
Xbit_r0_c89 bl[89] br[89] wl[0] vdd gnd cell_6t
Xbit_r1_c89 bl[89] br[89] wl[1] vdd gnd cell_6t
Xbit_r2_c89 bl[89] br[89] wl[2] vdd gnd cell_6t
Xbit_r3_c89 bl[89] br[89] wl[3] vdd gnd cell_6t
Xbit_r4_c89 bl[89] br[89] wl[4] vdd gnd cell_6t
Xbit_r5_c89 bl[89] br[89] wl[5] vdd gnd cell_6t
Xbit_r6_c89 bl[89] br[89] wl[6] vdd gnd cell_6t
Xbit_r7_c89 bl[89] br[89] wl[7] vdd gnd cell_6t
Xbit_r8_c89 bl[89] br[89] wl[8] vdd gnd cell_6t
Xbit_r9_c89 bl[89] br[89] wl[9] vdd gnd cell_6t
Xbit_r10_c89 bl[89] br[89] wl[10] vdd gnd cell_6t
Xbit_r11_c89 bl[89] br[89] wl[11] vdd gnd cell_6t
Xbit_r12_c89 bl[89] br[89] wl[12] vdd gnd cell_6t
Xbit_r13_c89 bl[89] br[89] wl[13] vdd gnd cell_6t
Xbit_r14_c89 bl[89] br[89] wl[14] vdd gnd cell_6t
Xbit_r15_c89 bl[89] br[89] wl[15] vdd gnd cell_6t
Xbit_r16_c89 bl[89] br[89] wl[16] vdd gnd cell_6t
Xbit_r17_c89 bl[89] br[89] wl[17] vdd gnd cell_6t
Xbit_r18_c89 bl[89] br[89] wl[18] vdd gnd cell_6t
Xbit_r19_c89 bl[89] br[89] wl[19] vdd gnd cell_6t
Xbit_r20_c89 bl[89] br[89] wl[20] vdd gnd cell_6t
Xbit_r21_c89 bl[89] br[89] wl[21] vdd gnd cell_6t
Xbit_r22_c89 bl[89] br[89] wl[22] vdd gnd cell_6t
Xbit_r23_c89 bl[89] br[89] wl[23] vdd gnd cell_6t
Xbit_r24_c89 bl[89] br[89] wl[24] vdd gnd cell_6t
Xbit_r25_c89 bl[89] br[89] wl[25] vdd gnd cell_6t
Xbit_r26_c89 bl[89] br[89] wl[26] vdd gnd cell_6t
Xbit_r27_c89 bl[89] br[89] wl[27] vdd gnd cell_6t
Xbit_r28_c89 bl[89] br[89] wl[28] vdd gnd cell_6t
Xbit_r29_c89 bl[89] br[89] wl[29] vdd gnd cell_6t
Xbit_r30_c89 bl[89] br[89] wl[30] vdd gnd cell_6t
Xbit_r31_c89 bl[89] br[89] wl[31] vdd gnd cell_6t
Xbit_r32_c89 bl[89] br[89] wl[32] vdd gnd cell_6t
Xbit_r33_c89 bl[89] br[89] wl[33] vdd gnd cell_6t
Xbit_r34_c89 bl[89] br[89] wl[34] vdd gnd cell_6t
Xbit_r35_c89 bl[89] br[89] wl[35] vdd gnd cell_6t
Xbit_r36_c89 bl[89] br[89] wl[36] vdd gnd cell_6t
Xbit_r37_c89 bl[89] br[89] wl[37] vdd gnd cell_6t
Xbit_r38_c89 bl[89] br[89] wl[38] vdd gnd cell_6t
Xbit_r39_c89 bl[89] br[89] wl[39] vdd gnd cell_6t
Xbit_r40_c89 bl[89] br[89] wl[40] vdd gnd cell_6t
Xbit_r41_c89 bl[89] br[89] wl[41] vdd gnd cell_6t
Xbit_r42_c89 bl[89] br[89] wl[42] vdd gnd cell_6t
Xbit_r43_c89 bl[89] br[89] wl[43] vdd gnd cell_6t
Xbit_r44_c89 bl[89] br[89] wl[44] vdd gnd cell_6t
Xbit_r45_c89 bl[89] br[89] wl[45] vdd gnd cell_6t
Xbit_r46_c89 bl[89] br[89] wl[46] vdd gnd cell_6t
Xbit_r47_c89 bl[89] br[89] wl[47] vdd gnd cell_6t
Xbit_r48_c89 bl[89] br[89] wl[48] vdd gnd cell_6t
Xbit_r49_c89 bl[89] br[89] wl[49] vdd gnd cell_6t
Xbit_r50_c89 bl[89] br[89] wl[50] vdd gnd cell_6t
Xbit_r51_c89 bl[89] br[89] wl[51] vdd gnd cell_6t
Xbit_r52_c89 bl[89] br[89] wl[52] vdd gnd cell_6t
Xbit_r53_c89 bl[89] br[89] wl[53] vdd gnd cell_6t
Xbit_r54_c89 bl[89] br[89] wl[54] vdd gnd cell_6t
Xbit_r55_c89 bl[89] br[89] wl[55] vdd gnd cell_6t
Xbit_r56_c89 bl[89] br[89] wl[56] vdd gnd cell_6t
Xbit_r57_c89 bl[89] br[89] wl[57] vdd gnd cell_6t
Xbit_r58_c89 bl[89] br[89] wl[58] vdd gnd cell_6t
Xbit_r59_c89 bl[89] br[89] wl[59] vdd gnd cell_6t
Xbit_r60_c89 bl[89] br[89] wl[60] vdd gnd cell_6t
Xbit_r61_c89 bl[89] br[89] wl[61] vdd gnd cell_6t
Xbit_r62_c89 bl[89] br[89] wl[62] vdd gnd cell_6t
Xbit_r63_c89 bl[89] br[89] wl[63] vdd gnd cell_6t
Xbit_r0_c90 bl[90] br[90] wl[0] vdd gnd cell_6t
Xbit_r1_c90 bl[90] br[90] wl[1] vdd gnd cell_6t
Xbit_r2_c90 bl[90] br[90] wl[2] vdd gnd cell_6t
Xbit_r3_c90 bl[90] br[90] wl[3] vdd gnd cell_6t
Xbit_r4_c90 bl[90] br[90] wl[4] vdd gnd cell_6t
Xbit_r5_c90 bl[90] br[90] wl[5] vdd gnd cell_6t
Xbit_r6_c90 bl[90] br[90] wl[6] vdd gnd cell_6t
Xbit_r7_c90 bl[90] br[90] wl[7] vdd gnd cell_6t
Xbit_r8_c90 bl[90] br[90] wl[8] vdd gnd cell_6t
Xbit_r9_c90 bl[90] br[90] wl[9] vdd gnd cell_6t
Xbit_r10_c90 bl[90] br[90] wl[10] vdd gnd cell_6t
Xbit_r11_c90 bl[90] br[90] wl[11] vdd gnd cell_6t
Xbit_r12_c90 bl[90] br[90] wl[12] vdd gnd cell_6t
Xbit_r13_c90 bl[90] br[90] wl[13] vdd gnd cell_6t
Xbit_r14_c90 bl[90] br[90] wl[14] vdd gnd cell_6t
Xbit_r15_c90 bl[90] br[90] wl[15] vdd gnd cell_6t
Xbit_r16_c90 bl[90] br[90] wl[16] vdd gnd cell_6t
Xbit_r17_c90 bl[90] br[90] wl[17] vdd gnd cell_6t
Xbit_r18_c90 bl[90] br[90] wl[18] vdd gnd cell_6t
Xbit_r19_c90 bl[90] br[90] wl[19] vdd gnd cell_6t
Xbit_r20_c90 bl[90] br[90] wl[20] vdd gnd cell_6t
Xbit_r21_c90 bl[90] br[90] wl[21] vdd gnd cell_6t
Xbit_r22_c90 bl[90] br[90] wl[22] vdd gnd cell_6t
Xbit_r23_c90 bl[90] br[90] wl[23] vdd gnd cell_6t
Xbit_r24_c90 bl[90] br[90] wl[24] vdd gnd cell_6t
Xbit_r25_c90 bl[90] br[90] wl[25] vdd gnd cell_6t
Xbit_r26_c90 bl[90] br[90] wl[26] vdd gnd cell_6t
Xbit_r27_c90 bl[90] br[90] wl[27] vdd gnd cell_6t
Xbit_r28_c90 bl[90] br[90] wl[28] vdd gnd cell_6t
Xbit_r29_c90 bl[90] br[90] wl[29] vdd gnd cell_6t
Xbit_r30_c90 bl[90] br[90] wl[30] vdd gnd cell_6t
Xbit_r31_c90 bl[90] br[90] wl[31] vdd gnd cell_6t
Xbit_r32_c90 bl[90] br[90] wl[32] vdd gnd cell_6t
Xbit_r33_c90 bl[90] br[90] wl[33] vdd gnd cell_6t
Xbit_r34_c90 bl[90] br[90] wl[34] vdd gnd cell_6t
Xbit_r35_c90 bl[90] br[90] wl[35] vdd gnd cell_6t
Xbit_r36_c90 bl[90] br[90] wl[36] vdd gnd cell_6t
Xbit_r37_c90 bl[90] br[90] wl[37] vdd gnd cell_6t
Xbit_r38_c90 bl[90] br[90] wl[38] vdd gnd cell_6t
Xbit_r39_c90 bl[90] br[90] wl[39] vdd gnd cell_6t
Xbit_r40_c90 bl[90] br[90] wl[40] vdd gnd cell_6t
Xbit_r41_c90 bl[90] br[90] wl[41] vdd gnd cell_6t
Xbit_r42_c90 bl[90] br[90] wl[42] vdd gnd cell_6t
Xbit_r43_c90 bl[90] br[90] wl[43] vdd gnd cell_6t
Xbit_r44_c90 bl[90] br[90] wl[44] vdd gnd cell_6t
Xbit_r45_c90 bl[90] br[90] wl[45] vdd gnd cell_6t
Xbit_r46_c90 bl[90] br[90] wl[46] vdd gnd cell_6t
Xbit_r47_c90 bl[90] br[90] wl[47] vdd gnd cell_6t
Xbit_r48_c90 bl[90] br[90] wl[48] vdd gnd cell_6t
Xbit_r49_c90 bl[90] br[90] wl[49] vdd gnd cell_6t
Xbit_r50_c90 bl[90] br[90] wl[50] vdd gnd cell_6t
Xbit_r51_c90 bl[90] br[90] wl[51] vdd gnd cell_6t
Xbit_r52_c90 bl[90] br[90] wl[52] vdd gnd cell_6t
Xbit_r53_c90 bl[90] br[90] wl[53] vdd gnd cell_6t
Xbit_r54_c90 bl[90] br[90] wl[54] vdd gnd cell_6t
Xbit_r55_c90 bl[90] br[90] wl[55] vdd gnd cell_6t
Xbit_r56_c90 bl[90] br[90] wl[56] vdd gnd cell_6t
Xbit_r57_c90 bl[90] br[90] wl[57] vdd gnd cell_6t
Xbit_r58_c90 bl[90] br[90] wl[58] vdd gnd cell_6t
Xbit_r59_c90 bl[90] br[90] wl[59] vdd gnd cell_6t
Xbit_r60_c90 bl[90] br[90] wl[60] vdd gnd cell_6t
Xbit_r61_c90 bl[90] br[90] wl[61] vdd gnd cell_6t
Xbit_r62_c90 bl[90] br[90] wl[62] vdd gnd cell_6t
Xbit_r63_c90 bl[90] br[90] wl[63] vdd gnd cell_6t
Xbit_r0_c91 bl[91] br[91] wl[0] vdd gnd cell_6t
Xbit_r1_c91 bl[91] br[91] wl[1] vdd gnd cell_6t
Xbit_r2_c91 bl[91] br[91] wl[2] vdd gnd cell_6t
Xbit_r3_c91 bl[91] br[91] wl[3] vdd gnd cell_6t
Xbit_r4_c91 bl[91] br[91] wl[4] vdd gnd cell_6t
Xbit_r5_c91 bl[91] br[91] wl[5] vdd gnd cell_6t
Xbit_r6_c91 bl[91] br[91] wl[6] vdd gnd cell_6t
Xbit_r7_c91 bl[91] br[91] wl[7] vdd gnd cell_6t
Xbit_r8_c91 bl[91] br[91] wl[8] vdd gnd cell_6t
Xbit_r9_c91 bl[91] br[91] wl[9] vdd gnd cell_6t
Xbit_r10_c91 bl[91] br[91] wl[10] vdd gnd cell_6t
Xbit_r11_c91 bl[91] br[91] wl[11] vdd gnd cell_6t
Xbit_r12_c91 bl[91] br[91] wl[12] vdd gnd cell_6t
Xbit_r13_c91 bl[91] br[91] wl[13] vdd gnd cell_6t
Xbit_r14_c91 bl[91] br[91] wl[14] vdd gnd cell_6t
Xbit_r15_c91 bl[91] br[91] wl[15] vdd gnd cell_6t
Xbit_r16_c91 bl[91] br[91] wl[16] vdd gnd cell_6t
Xbit_r17_c91 bl[91] br[91] wl[17] vdd gnd cell_6t
Xbit_r18_c91 bl[91] br[91] wl[18] vdd gnd cell_6t
Xbit_r19_c91 bl[91] br[91] wl[19] vdd gnd cell_6t
Xbit_r20_c91 bl[91] br[91] wl[20] vdd gnd cell_6t
Xbit_r21_c91 bl[91] br[91] wl[21] vdd gnd cell_6t
Xbit_r22_c91 bl[91] br[91] wl[22] vdd gnd cell_6t
Xbit_r23_c91 bl[91] br[91] wl[23] vdd gnd cell_6t
Xbit_r24_c91 bl[91] br[91] wl[24] vdd gnd cell_6t
Xbit_r25_c91 bl[91] br[91] wl[25] vdd gnd cell_6t
Xbit_r26_c91 bl[91] br[91] wl[26] vdd gnd cell_6t
Xbit_r27_c91 bl[91] br[91] wl[27] vdd gnd cell_6t
Xbit_r28_c91 bl[91] br[91] wl[28] vdd gnd cell_6t
Xbit_r29_c91 bl[91] br[91] wl[29] vdd gnd cell_6t
Xbit_r30_c91 bl[91] br[91] wl[30] vdd gnd cell_6t
Xbit_r31_c91 bl[91] br[91] wl[31] vdd gnd cell_6t
Xbit_r32_c91 bl[91] br[91] wl[32] vdd gnd cell_6t
Xbit_r33_c91 bl[91] br[91] wl[33] vdd gnd cell_6t
Xbit_r34_c91 bl[91] br[91] wl[34] vdd gnd cell_6t
Xbit_r35_c91 bl[91] br[91] wl[35] vdd gnd cell_6t
Xbit_r36_c91 bl[91] br[91] wl[36] vdd gnd cell_6t
Xbit_r37_c91 bl[91] br[91] wl[37] vdd gnd cell_6t
Xbit_r38_c91 bl[91] br[91] wl[38] vdd gnd cell_6t
Xbit_r39_c91 bl[91] br[91] wl[39] vdd gnd cell_6t
Xbit_r40_c91 bl[91] br[91] wl[40] vdd gnd cell_6t
Xbit_r41_c91 bl[91] br[91] wl[41] vdd gnd cell_6t
Xbit_r42_c91 bl[91] br[91] wl[42] vdd gnd cell_6t
Xbit_r43_c91 bl[91] br[91] wl[43] vdd gnd cell_6t
Xbit_r44_c91 bl[91] br[91] wl[44] vdd gnd cell_6t
Xbit_r45_c91 bl[91] br[91] wl[45] vdd gnd cell_6t
Xbit_r46_c91 bl[91] br[91] wl[46] vdd gnd cell_6t
Xbit_r47_c91 bl[91] br[91] wl[47] vdd gnd cell_6t
Xbit_r48_c91 bl[91] br[91] wl[48] vdd gnd cell_6t
Xbit_r49_c91 bl[91] br[91] wl[49] vdd gnd cell_6t
Xbit_r50_c91 bl[91] br[91] wl[50] vdd gnd cell_6t
Xbit_r51_c91 bl[91] br[91] wl[51] vdd gnd cell_6t
Xbit_r52_c91 bl[91] br[91] wl[52] vdd gnd cell_6t
Xbit_r53_c91 bl[91] br[91] wl[53] vdd gnd cell_6t
Xbit_r54_c91 bl[91] br[91] wl[54] vdd gnd cell_6t
Xbit_r55_c91 bl[91] br[91] wl[55] vdd gnd cell_6t
Xbit_r56_c91 bl[91] br[91] wl[56] vdd gnd cell_6t
Xbit_r57_c91 bl[91] br[91] wl[57] vdd gnd cell_6t
Xbit_r58_c91 bl[91] br[91] wl[58] vdd gnd cell_6t
Xbit_r59_c91 bl[91] br[91] wl[59] vdd gnd cell_6t
Xbit_r60_c91 bl[91] br[91] wl[60] vdd gnd cell_6t
Xbit_r61_c91 bl[91] br[91] wl[61] vdd gnd cell_6t
Xbit_r62_c91 bl[91] br[91] wl[62] vdd gnd cell_6t
Xbit_r63_c91 bl[91] br[91] wl[63] vdd gnd cell_6t
Xbit_r0_c92 bl[92] br[92] wl[0] vdd gnd cell_6t
Xbit_r1_c92 bl[92] br[92] wl[1] vdd gnd cell_6t
Xbit_r2_c92 bl[92] br[92] wl[2] vdd gnd cell_6t
Xbit_r3_c92 bl[92] br[92] wl[3] vdd gnd cell_6t
Xbit_r4_c92 bl[92] br[92] wl[4] vdd gnd cell_6t
Xbit_r5_c92 bl[92] br[92] wl[5] vdd gnd cell_6t
Xbit_r6_c92 bl[92] br[92] wl[6] vdd gnd cell_6t
Xbit_r7_c92 bl[92] br[92] wl[7] vdd gnd cell_6t
Xbit_r8_c92 bl[92] br[92] wl[8] vdd gnd cell_6t
Xbit_r9_c92 bl[92] br[92] wl[9] vdd gnd cell_6t
Xbit_r10_c92 bl[92] br[92] wl[10] vdd gnd cell_6t
Xbit_r11_c92 bl[92] br[92] wl[11] vdd gnd cell_6t
Xbit_r12_c92 bl[92] br[92] wl[12] vdd gnd cell_6t
Xbit_r13_c92 bl[92] br[92] wl[13] vdd gnd cell_6t
Xbit_r14_c92 bl[92] br[92] wl[14] vdd gnd cell_6t
Xbit_r15_c92 bl[92] br[92] wl[15] vdd gnd cell_6t
Xbit_r16_c92 bl[92] br[92] wl[16] vdd gnd cell_6t
Xbit_r17_c92 bl[92] br[92] wl[17] vdd gnd cell_6t
Xbit_r18_c92 bl[92] br[92] wl[18] vdd gnd cell_6t
Xbit_r19_c92 bl[92] br[92] wl[19] vdd gnd cell_6t
Xbit_r20_c92 bl[92] br[92] wl[20] vdd gnd cell_6t
Xbit_r21_c92 bl[92] br[92] wl[21] vdd gnd cell_6t
Xbit_r22_c92 bl[92] br[92] wl[22] vdd gnd cell_6t
Xbit_r23_c92 bl[92] br[92] wl[23] vdd gnd cell_6t
Xbit_r24_c92 bl[92] br[92] wl[24] vdd gnd cell_6t
Xbit_r25_c92 bl[92] br[92] wl[25] vdd gnd cell_6t
Xbit_r26_c92 bl[92] br[92] wl[26] vdd gnd cell_6t
Xbit_r27_c92 bl[92] br[92] wl[27] vdd gnd cell_6t
Xbit_r28_c92 bl[92] br[92] wl[28] vdd gnd cell_6t
Xbit_r29_c92 bl[92] br[92] wl[29] vdd gnd cell_6t
Xbit_r30_c92 bl[92] br[92] wl[30] vdd gnd cell_6t
Xbit_r31_c92 bl[92] br[92] wl[31] vdd gnd cell_6t
Xbit_r32_c92 bl[92] br[92] wl[32] vdd gnd cell_6t
Xbit_r33_c92 bl[92] br[92] wl[33] vdd gnd cell_6t
Xbit_r34_c92 bl[92] br[92] wl[34] vdd gnd cell_6t
Xbit_r35_c92 bl[92] br[92] wl[35] vdd gnd cell_6t
Xbit_r36_c92 bl[92] br[92] wl[36] vdd gnd cell_6t
Xbit_r37_c92 bl[92] br[92] wl[37] vdd gnd cell_6t
Xbit_r38_c92 bl[92] br[92] wl[38] vdd gnd cell_6t
Xbit_r39_c92 bl[92] br[92] wl[39] vdd gnd cell_6t
Xbit_r40_c92 bl[92] br[92] wl[40] vdd gnd cell_6t
Xbit_r41_c92 bl[92] br[92] wl[41] vdd gnd cell_6t
Xbit_r42_c92 bl[92] br[92] wl[42] vdd gnd cell_6t
Xbit_r43_c92 bl[92] br[92] wl[43] vdd gnd cell_6t
Xbit_r44_c92 bl[92] br[92] wl[44] vdd gnd cell_6t
Xbit_r45_c92 bl[92] br[92] wl[45] vdd gnd cell_6t
Xbit_r46_c92 bl[92] br[92] wl[46] vdd gnd cell_6t
Xbit_r47_c92 bl[92] br[92] wl[47] vdd gnd cell_6t
Xbit_r48_c92 bl[92] br[92] wl[48] vdd gnd cell_6t
Xbit_r49_c92 bl[92] br[92] wl[49] vdd gnd cell_6t
Xbit_r50_c92 bl[92] br[92] wl[50] vdd gnd cell_6t
Xbit_r51_c92 bl[92] br[92] wl[51] vdd gnd cell_6t
Xbit_r52_c92 bl[92] br[92] wl[52] vdd gnd cell_6t
Xbit_r53_c92 bl[92] br[92] wl[53] vdd gnd cell_6t
Xbit_r54_c92 bl[92] br[92] wl[54] vdd gnd cell_6t
Xbit_r55_c92 bl[92] br[92] wl[55] vdd gnd cell_6t
Xbit_r56_c92 bl[92] br[92] wl[56] vdd gnd cell_6t
Xbit_r57_c92 bl[92] br[92] wl[57] vdd gnd cell_6t
Xbit_r58_c92 bl[92] br[92] wl[58] vdd gnd cell_6t
Xbit_r59_c92 bl[92] br[92] wl[59] vdd gnd cell_6t
Xbit_r60_c92 bl[92] br[92] wl[60] vdd gnd cell_6t
Xbit_r61_c92 bl[92] br[92] wl[61] vdd gnd cell_6t
Xbit_r62_c92 bl[92] br[92] wl[62] vdd gnd cell_6t
Xbit_r63_c92 bl[92] br[92] wl[63] vdd gnd cell_6t
Xbit_r0_c93 bl[93] br[93] wl[0] vdd gnd cell_6t
Xbit_r1_c93 bl[93] br[93] wl[1] vdd gnd cell_6t
Xbit_r2_c93 bl[93] br[93] wl[2] vdd gnd cell_6t
Xbit_r3_c93 bl[93] br[93] wl[3] vdd gnd cell_6t
Xbit_r4_c93 bl[93] br[93] wl[4] vdd gnd cell_6t
Xbit_r5_c93 bl[93] br[93] wl[5] vdd gnd cell_6t
Xbit_r6_c93 bl[93] br[93] wl[6] vdd gnd cell_6t
Xbit_r7_c93 bl[93] br[93] wl[7] vdd gnd cell_6t
Xbit_r8_c93 bl[93] br[93] wl[8] vdd gnd cell_6t
Xbit_r9_c93 bl[93] br[93] wl[9] vdd gnd cell_6t
Xbit_r10_c93 bl[93] br[93] wl[10] vdd gnd cell_6t
Xbit_r11_c93 bl[93] br[93] wl[11] vdd gnd cell_6t
Xbit_r12_c93 bl[93] br[93] wl[12] vdd gnd cell_6t
Xbit_r13_c93 bl[93] br[93] wl[13] vdd gnd cell_6t
Xbit_r14_c93 bl[93] br[93] wl[14] vdd gnd cell_6t
Xbit_r15_c93 bl[93] br[93] wl[15] vdd gnd cell_6t
Xbit_r16_c93 bl[93] br[93] wl[16] vdd gnd cell_6t
Xbit_r17_c93 bl[93] br[93] wl[17] vdd gnd cell_6t
Xbit_r18_c93 bl[93] br[93] wl[18] vdd gnd cell_6t
Xbit_r19_c93 bl[93] br[93] wl[19] vdd gnd cell_6t
Xbit_r20_c93 bl[93] br[93] wl[20] vdd gnd cell_6t
Xbit_r21_c93 bl[93] br[93] wl[21] vdd gnd cell_6t
Xbit_r22_c93 bl[93] br[93] wl[22] vdd gnd cell_6t
Xbit_r23_c93 bl[93] br[93] wl[23] vdd gnd cell_6t
Xbit_r24_c93 bl[93] br[93] wl[24] vdd gnd cell_6t
Xbit_r25_c93 bl[93] br[93] wl[25] vdd gnd cell_6t
Xbit_r26_c93 bl[93] br[93] wl[26] vdd gnd cell_6t
Xbit_r27_c93 bl[93] br[93] wl[27] vdd gnd cell_6t
Xbit_r28_c93 bl[93] br[93] wl[28] vdd gnd cell_6t
Xbit_r29_c93 bl[93] br[93] wl[29] vdd gnd cell_6t
Xbit_r30_c93 bl[93] br[93] wl[30] vdd gnd cell_6t
Xbit_r31_c93 bl[93] br[93] wl[31] vdd gnd cell_6t
Xbit_r32_c93 bl[93] br[93] wl[32] vdd gnd cell_6t
Xbit_r33_c93 bl[93] br[93] wl[33] vdd gnd cell_6t
Xbit_r34_c93 bl[93] br[93] wl[34] vdd gnd cell_6t
Xbit_r35_c93 bl[93] br[93] wl[35] vdd gnd cell_6t
Xbit_r36_c93 bl[93] br[93] wl[36] vdd gnd cell_6t
Xbit_r37_c93 bl[93] br[93] wl[37] vdd gnd cell_6t
Xbit_r38_c93 bl[93] br[93] wl[38] vdd gnd cell_6t
Xbit_r39_c93 bl[93] br[93] wl[39] vdd gnd cell_6t
Xbit_r40_c93 bl[93] br[93] wl[40] vdd gnd cell_6t
Xbit_r41_c93 bl[93] br[93] wl[41] vdd gnd cell_6t
Xbit_r42_c93 bl[93] br[93] wl[42] vdd gnd cell_6t
Xbit_r43_c93 bl[93] br[93] wl[43] vdd gnd cell_6t
Xbit_r44_c93 bl[93] br[93] wl[44] vdd gnd cell_6t
Xbit_r45_c93 bl[93] br[93] wl[45] vdd gnd cell_6t
Xbit_r46_c93 bl[93] br[93] wl[46] vdd gnd cell_6t
Xbit_r47_c93 bl[93] br[93] wl[47] vdd gnd cell_6t
Xbit_r48_c93 bl[93] br[93] wl[48] vdd gnd cell_6t
Xbit_r49_c93 bl[93] br[93] wl[49] vdd gnd cell_6t
Xbit_r50_c93 bl[93] br[93] wl[50] vdd gnd cell_6t
Xbit_r51_c93 bl[93] br[93] wl[51] vdd gnd cell_6t
Xbit_r52_c93 bl[93] br[93] wl[52] vdd gnd cell_6t
Xbit_r53_c93 bl[93] br[93] wl[53] vdd gnd cell_6t
Xbit_r54_c93 bl[93] br[93] wl[54] vdd gnd cell_6t
Xbit_r55_c93 bl[93] br[93] wl[55] vdd gnd cell_6t
Xbit_r56_c93 bl[93] br[93] wl[56] vdd gnd cell_6t
Xbit_r57_c93 bl[93] br[93] wl[57] vdd gnd cell_6t
Xbit_r58_c93 bl[93] br[93] wl[58] vdd gnd cell_6t
Xbit_r59_c93 bl[93] br[93] wl[59] vdd gnd cell_6t
Xbit_r60_c93 bl[93] br[93] wl[60] vdd gnd cell_6t
Xbit_r61_c93 bl[93] br[93] wl[61] vdd gnd cell_6t
Xbit_r62_c93 bl[93] br[93] wl[62] vdd gnd cell_6t
Xbit_r63_c93 bl[93] br[93] wl[63] vdd gnd cell_6t
Xbit_r0_c94 bl[94] br[94] wl[0] vdd gnd cell_6t
Xbit_r1_c94 bl[94] br[94] wl[1] vdd gnd cell_6t
Xbit_r2_c94 bl[94] br[94] wl[2] vdd gnd cell_6t
Xbit_r3_c94 bl[94] br[94] wl[3] vdd gnd cell_6t
Xbit_r4_c94 bl[94] br[94] wl[4] vdd gnd cell_6t
Xbit_r5_c94 bl[94] br[94] wl[5] vdd gnd cell_6t
Xbit_r6_c94 bl[94] br[94] wl[6] vdd gnd cell_6t
Xbit_r7_c94 bl[94] br[94] wl[7] vdd gnd cell_6t
Xbit_r8_c94 bl[94] br[94] wl[8] vdd gnd cell_6t
Xbit_r9_c94 bl[94] br[94] wl[9] vdd gnd cell_6t
Xbit_r10_c94 bl[94] br[94] wl[10] vdd gnd cell_6t
Xbit_r11_c94 bl[94] br[94] wl[11] vdd gnd cell_6t
Xbit_r12_c94 bl[94] br[94] wl[12] vdd gnd cell_6t
Xbit_r13_c94 bl[94] br[94] wl[13] vdd gnd cell_6t
Xbit_r14_c94 bl[94] br[94] wl[14] vdd gnd cell_6t
Xbit_r15_c94 bl[94] br[94] wl[15] vdd gnd cell_6t
Xbit_r16_c94 bl[94] br[94] wl[16] vdd gnd cell_6t
Xbit_r17_c94 bl[94] br[94] wl[17] vdd gnd cell_6t
Xbit_r18_c94 bl[94] br[94] wl[18] vdd gnd cell_6t
Xbit_r19_c94 bl[94] br[94] wl[19] vdd gnd cell_6t
Xbit_r20_c94 bl[94] br[94] wl[20] vdd gnd cell_6t
Xbit_r21_c94 bl[94] br[94] wl[21] vdd gnd cell_6t
Xbit_r22_c94 bl[94] br[94] wl[22] vdd gnd cell_6t
Xbit_r23_c94 bl[94] br[94] wl[23] vdd gnd cell_6t
Xbit_r24_c94 bl[94] br[94] wl[24] vdd gnd cell_6t
Xbit_r25_c94 bl[94] br[94] wl[25] vdd gnd cell_6t
Xbit_r26_c94 bl[94] br[94] wl[26] vdd gnd cell_6t
Xbit_r27_c94 bl[94] br[94] wl[27] vdd gnd cell_6t
Xbit_r28_c94 bl[94] br[94] wl[28] vdd gnd cell_6t
Xbit_r29_c94 bl[94] br[94] wl[29] vdd gnd cell_6t
Xbit_r30_c94 bl[94] br[94] wl[30] vdd gnd cell_6t
Xbit_r31_c94 bl[94] br[94] wl[31] vdd gnd cell_6t
Xbit_r32_c94 bl[94] br[94] wl[32] vdd gnd cell_6t
Xbit_r33_c94 bl[94] br[94] wl[33] vdd gnd cell_6t
Xbit_r34_c94 bl[94] br[94] wl[34] vdd gnd cell_6t
Xbit_r35_c94 bl[94] br[94] wl[35] vdd gnd cell_6t
Xbit_r36_c94 bl[94] br[94] wl[36] vdd gnd cell_6t
Xbit_r37_c94 bl[94] br[94] wl[37] vdd gnd cell_6t
Xbit_r38_c94 bl[94] br[94] wl[38] vdd gnd cell_6t
Xbit_r39_c94 bl[94] br[94] wl[39] vdd gnd cell_6t
Xbit_r40_c94 bl[94] br[94] wl[40] vdd gnd cell_6t
Xbit_r41_c94 bl[94] br[94] wl[41] vdd gnd cell_6t
Xbit_r42_c94 bl[94] br[94] wl[42] vdd gnd cell_6t
Xbit_r43_c94 bl[94] br[94] wl[43] vdd gnd cell_6t
Xbit_r44_c94 bl[94] br[94] wl[44] vdd gnd cell_6t
Xbit_r45_c94 bl[94] br[94] wl[45] vdd gnd cell_6t
Xbit_r46_c94 bl[94] br[94] wl[46] vdd gnd cell_6t
Xbit_r47_c94 bl[94] br[94] wl[47] vdd gnd cell_6t
Xbit_r48_c94 bl[94] br[94] wl[48] vdd gnd cell_6t
Xbit_r49_c94 bl[94] br[94] wl[49] vdd gnd cell_6t
Xbit_r50_c94 bl[94] br[94] wl[50] vdd gnd cell_6t
Xbit_r51_c94 bl[94] br[94] wl[51] vdd gnd cell_6t
Xbit_r52_c94 bl[94] br[94] wl[52] vdd gnd cell_6t
Xbit_r53_c94 bl[94] br[94] wl[53] vdd gnd cell_6t
Xbit_r54_c94 bl[94] br[94] wl[54] vdd gnd cell_6t
Xbit_r55_c94 bl[94] br[94] wl[55] vdd gnd cell_6t
Xbit_r56_c94 bl[94] br[94] wl[56] vdd gnd cell_6t
Xbit_r57_c94 bl[94] br[94] wl[57] vdd gnd cell_6t
Xbit_r58_c94 bl[94] br[94] wl[58] vdd gnd cell_6t
Xbit_r59_c94 bl[94] br[94] wl[59] vdd gnd cell_6t
Xbit_r60_c94 bl[94] br[94] wl[60] vdd gnd cell_6t
Xbit_r61_c94 bl[94] br[94] wl[61] vdd gnd cell_6t
Xbit_r62_c94 bl[94] br[94] wl[62] vdd gnd cell_6t
Xbit_r63_c94 bl[94] br[94] wl[63] vdd gnd cell_6t
Xbit_r0_c95 bl[95] br[95] wl[0] vdd gnd cell_6t
Xbit_r1_c95 bl[95] br[95] wl[1] vdd gnd cell_6t
Xbit_r2_c95 bl[95] br[95] wl[2] vdd gnd cell_6t
Xbit_r3_c95 bl[95] br[95] wl[3] vdd gnd cell_6t
Xbit_r4_c95 bl[95] br[95] wl[4] vdd gnd cell_6t
Xbit_r5_c95 bl[95] br[95] wl[5] vdd gnd cell_6t
Xbit_r6_c95 bl[95] br[95] wl[6] vdd gnd cell_6t
Xbit_r7_c95 bl[95] br[95] wl[7] vdd gnd cell_6t
Xbit_r8_c95 bl[95] br[95] wl[8] vdd gnd cell_6t
Xbit_r9_c95 bl[95] br[95] wl[9] vdd gnd cell_6t
Xbit_r10_c95 bl[95] br[95] wl[10] vdd gnd cell_6t
Xbit_r11_c95 bl[95] br[95] wl[11] vdd gnd cell_6t
Xbit_r12_c95 bl[95] br[95] wl[12] vdd gnd cell_6t
Xbit_r13_c95 bl[95] br[95] wl[13] vdd gnd cell_6t
Xbit_r14_c95 bl[95] br[95] wl[14] vdd gnd cell_6t
Xbit_r15_c95 bl[95] br[95] wl[15] vdd gnd cell_6t
Xbit_r16_c95 bl[95] br[95] wl[16] vdd gnd cell_6t
Xbit_r17_c95 bl[95] br[95] wl[17] vdd gnd cell_6t
Xbit_r18_c95 bl[95] br[95] wl[18] vdd gnd cell_6t
Xbit_r19_c95 bl[95] br[95] wl[19] vdd gnd cell_6t
Xbit_r20_c95 bl[95] br[95] wl[20] vdd gnd cell_6t
Xbit_r21_c95 bl[95] br[95] wl[21] vdd gnd cell_6t
Xbit_r22_c95 bl[95] br[95] wl[22] vdd gnd cell_6t
Xbit_r23_c95 bl[95] br[95] wl[23] vdd gnd cell_6t
Xbit_r24_c95 bl[95] br[95] wl[24] vdd gnd cell_6t
Xbit_r25_c95 bl[95] br[95] wl[25] vdd gnd cell_6t
Xbit_r26_c95 bl[95] br[95] wl[26] vdd gnd cell_6t
Xbit_r27_c95 bl[95] br[95] wl[27] vdd gnd cell_6t
Xbit_r28_c95 bl[95] br[95] wl[28] vdd gnd cell_6t
Xbit_r29_c95 bl[95] br[95] wl[29] vdd gnd cell_6t
Xbit_r30_c95 bl[95] br[95] wl[30] vdd gnd cell_6t
Xbit_r31_c95 bl[95] br[95] wl[31] vdd gnd cell_6t
Xbit_r32_c95 bl[95] br[95] wl[32] vdd gnd cell_6t
Xbit_r33_c95 bl[95] br[95] wl[33] vdd gnd cell_6t
Xbit_r34_c95 bl[95] br[95] wl[34] vdd gnd cell_6t
Xbit_r35_c95 bl[95] br[95] wl[35] vdd gnd cell_6t
Xbit_r36_c95 bl[95] br[95] wl[36] vdd gnd cell_6t
Xbit_r37_c95 bl[95] br[95] wl[37] vdd gnd cell_6t
Xbit_r38_c95 bl[95] br[95] wl[38] vdd gnd cell_6t
Xbit_r39_c95 bl[95] br[95] wl[39] vdd gnd cell_6t
Xbit_r40_c95 bl[95] br[95] wl[40] vdd gnd cell_6t
Xbit_r41_c95 bl[95] br[95] wl[41] vdd gnd cell_6t
Xbit_r42_c95 bl[95] br[95] wl[42] vdd gnd cell_6t
Xbit_r43_c95 bl[95] br[95] wl[43] vdd gnd cell_6t
Xbit_r44_c95 bl[95] br[95] wl[44] vdd gnd cell_6t
Xbit_r45_c95 bl[95] br[95] wl[45] vdd gnd cell_6t
Xbit_r46_c95 bl[95] br[95] wl[46] vdd gnd cell_6t
Xbit_r47_c95 bl[95] br[95] wl[47] vdd gnd cell_6t
Xbit_r48_c95 bl[95] br[95] wl[48] vdd gnd cell_6t
Xbit_r49_c95 bl[95] br[95] wl[49] vdd gnd cell_6t
Xbit_r50_c95 bl[95] br[95] wl[50] vdd gnd cell_6t
Xbit_r51_c95 bl[95] br[95] wl[51] vdd gnd cell_6t
Xbit_r52_c95 bl[95] br[95] wl[52] vdd gnd cell_6t
Xbit_r53_c95 bl[95] br[95] wl[53] vdd gnd cell_6t
Xbit_r54_c95 bl[95] br[95] wl[54] vdd gnd cell_6t
Xbit_r55_c95 bl[95] br[95] wl[55] vdd gnd cell_6t
Xbit_r56_c95 bl[95] br[95] wl[56] vdd gnd cell_6t
Xbit_r57_c95 bl[95] br[95] wl[57] vdd gnd cell_6t
Xbit_r58_c95 bl[95] br[95] wl[58] vdd gnd cell_6t
Xbit_r59_c95 bl[95] br[95] wl[59] vdd gnd cell_6t
Xbit_r60_c95 bl[95] br[95] wl[60] vdd gnd cell_6t
Xbit_r61_c95 bl[95] br[95] wl[61] vdd gnd cell_6t
Xbit_r62_c95 bl[95] br[95] wl[62] vdd gnd cell_6t
Xbit_r63_c95 bl[95] br[95] wl[63] vdd gnd cell_6t
Xbit_r0_c96 bl[96] br[96] wl[0] vdd gnd cell_6t
Xbit_r1_c96 bl[96] br[96] wl[1] vdd gnd cell_6t
Xbit_r2_c96 bl[96] br[96] wl[2] vdd gnd cell_6t
Xbit_r3_c96 bl[96] br[96] wl[3] vdd gnd cell_6t
Xbit_r4_c96 bl[96] br[96] wl[4] vdd gnd cell_6t
Xbit_r5_c96 bl[96] br[96] wl[5] vdd gnd cell_6t
Xbit_r6_c96 bl[96] br[96] wl[6] vdd gnd cell_6t
Xbit_r7_c96 bl[96] br[96] wl[7] vdd gnd cell_6t
Xbit_r8_c96 bl[96] br[96] wl[8] vdd gnd cell_6t
Xbit_r9_c96 bl[96] br[96] wl[9] vdd gnd cell_6t
Xbit_r10_c96 bl[96] br[96] wl[10] vdd gnd cell_6t
Xbit_r11_c96 bl[96] br[96] wl[11] vdd gnd cell_6t
Xbit_r12_c96 bl[96] br[96] wl[12] vdd gnd cell_6t
Xbit_r13_c96 bl[96] br[96] wl[13] vdd gnd cell_6t
Xbit_r14_c96 bl[96] br[96] wl[14] vdd gnd cell_6t
Xbit_r15_c96 bl[96] br[96] wl[15] vdd gnd cell_6t
Xbit_r16_c96 bl[96] br[96] wl[16] vdd gnd cell_6t
Xbit_r17_c96 bl[96] br[96] wl[17] vdd gnd cell_6t
Xbit_r18_c96 bl[96] br[96] wl[18] vdd gnd cell_6t
Xbit_r19_c96 bl[96] br[96] wl[19] vdd gnd cell_6t
Xbit_r20_c96 bl[96] br[96] wl[20] vdd gnd cell_6t
Xbit_r21_c96 bl[96] br[96] wl[21] vdd gnd cell_6t
Xbit_r22_c96 bl[96] br[96] wl[22] vdd gnd cell_6t
Xbit_r23_c96 bl[96] br[96] wl[23] vdd gnd cell_6t
Xbit_r24_c96 bl[96] br[96] wl[24] vdd gnd cell_6t
Xbit_r25_c96 bl[96] br[96] wl[25] vdd gnd cell_6t
Xbit_r26_c96 bl[96] br[96] wl[26] vdd gnd cell_6t
Xbit_r27_c96 bl[96] br[96] wl[27] vdd gnd cell_6t
Xbit_r28_c96 bl[96] br[96] wl[28] vdd gnd cell_6t
Xbit_r29_c96 bl[96] br[96] wl[29] vdd gnd cell_6t
Xbit_r30_c96 bl[96] br[96] wl[30] vdd gnd cell_6t
Xbit_r31_c96 bl[96] br[96] wl[31] vdd gnd cell_6t
Xbit_r32_c96 bl[96] br[96] wl[32] vdd gnd cell_6t
Xbit_r33_c96 bl[96] br[96] wl[33] vdd gnd cell_6t
Xbit_r34_c96 bl[96] br[96] wl[34] vdd gnd cell_6t
Xbit_r35_c96 bl[96] br[96] wl[35] vdd gnd cell_6t
Xbit_r36_c96 bl[96] br[96] wl[36] vdd gnd cell_6t
Xbit_r37_c96 bl[96] br[96] wl[37] vdd gnd cell_6t
Xbit_r38_c96 bl[96] br[96] wl[38] vdd gnd cell_6t
Xbit_r39_c96 bl[96] br[96] wl[39] vdd gnd cell_6t
Xbit_r40_c96 bl[96] br[96] wl[40] vdd gnd cell_6t
Xbit_r41_c96 bl[96] br[96] wl[41] vdd gnd cell_6t
Xbit_r42_c96 bl[96] br[96] wl[42] vdd gnd cell_6t
Xbit_r43_c96 bl[96] br[96] wl[43] vdd gnd cell_6t
Xbit_r44_c96 bl[96] br[96] wl[44] vdd gnd cell_6t
Xbit_r45_c96 bl[96] br[96] wl[45] vdd gnd cell_6t
Xbit_r46_c96 bl[96] br[96] wl[46] vdd gnd cell_6t
Xbit_r47_c96 bl[96] br[96] wl[47] vdd gnd cell_6t
Xbit_r48_c96 bl[96] br[96] wl[48] vdd gnd cell_6t
Xbit_r49_c96 bl[96] br[96] wl[49] vdd gnd cell_6t
Xbit_r50_c96 bl[96] br[96] wl[50] vdd gnd cell_6t
Xbit_r51_c96 bl[96] br[96] wl[51] vdd gnd cell_6t
Xbit_r52_c96 bl[96] br[96] wl[52] vdd gnd cell_6t
Xbit_r53_c96 bl[96] br[96] wl[53] vdd gnd cell_6t
Xbit_r54_c96 bl[96] br[96] wl[54] vdd gnd cell_6t
Xbit_r55_c96 bl[96] br[96] wl[55] vdd gnd cell_6t
Xbit_r56_c96 bl[96] br[96] wl[56] vdd gnd cell_6t
Xbit_r57_c96 bl[96] br[96] wl[57] vdd gnd cell_6t
Xbit_r58_c96 bl[96] br[96] wl[58] vdd gnd cell_6t
Xbit_r59_c96 bl[96] br[96] wl[59] vdd gnd cell_6t
Xbit_r60_c96 bl[96] br[96] wl[60] vdd gnd cell_6t
Xbit_r61_c96 bl[96] br[96] wl[61] vdd gnd cell_6t
Xbit_r62_c96 bl[96] br[96] wl[62] vdd gnd cell_6t
Xbit_r63_c96 bl[96] br[96] wl[63] vdd gnd cell_6t
Xbit_r0_c97 bl[97] br[97] wl[0] vdd gnd cell_6t
Xbit_r1_c97 bl[97] br[97] wl[1] vdd gnd cell_6t
Xbit_r2_c97 bl[97] br[97] wl[2] vdd gnd cell_6t
Xbit_r3_c97 bl[97] br[97] wl[3] vdd gnd cell_6t
Xbit_r4_c97 bl[97] br[97] wl[4] vdd gnd cell_6t
Xbit_r5_c97 bl[97] br[97] wl[5] vdd gnd cell_6t
Xbit_r6_c97 bl[97] br[97] wl[6] vdd gnd cell_6t
Xbit_r7_c97 bl[97] br[97] wl[7] vdd gnd cell_6t
Xbit_r8_c97 bl[97] br[97] wl[8] vdd gnd cell_6t
Xbit_r9_c97 bl[97] br[97] wl[9] vdd gnd cell_6t
Xbit_r10_c97 bl[97] br[97] wl[10] vdd gnd cell_6t
Xbit_r11_c97 bl[97] br[97] wl[11] vdd gnd cell_6t
Xbit_r12_c97 bl[97] br[97] wl[12] vdd gnd cell_6t
Xbit_r13_c97 bl[97] br[97] wl[13] vdd gnd cell_6t
Xbit_r14_c97 bl[97] br[97] wl[14] vdd gnd cell_6t
Xbit_r15_c97 bl[97] br[97] wl[15] vdd gnd cell_6t
Xbit_r16_c97 bl[97] br[97] wl[16] vdd gnd cell_6t
Xbit_r17_c97 bl[97] br[97] wl[17] vdd gnd cell_6t
Xbit_r18_c97 bl[97] br[97] wl[18] vdd gnd cell_6t
Xbit_r19_c97 bl[97] br[97] wl[19] vdd gnd cell_6t
Xbit_r20_c97 bl[97] br[97] wl[20] vdd gnd cell_6t
Xbit_r21_c97 bl[97] br[97] wl[21] vdd gnd cell_6t
Xbit_r22_c97 bl[97] br[97] wl[22] vdd gnd cell_6t
Xbit_r23_c97 bl[97] br[97] wl[23] vdd gnd cell_6t
Xbit_r24_c97 bl[97] br[97] wl[24] vdd gnd cell_6t
Xbit_r25_c97 bl[97] br[97] wl[25] vdd gnd cell_6t
Xbit_r26_c97 bl[97] br[97] wl[26] vdd gnd cell_6t
Xbit_r27_c97 bl[97] br[97] wl[27] vdd gnd cell_6t
Xbit_r28_c97 bl[97] br[97] wl[28] vdd gnd cell_6t
Xbit_r29_c97 bl[97] br[97] wl[29] vdd gnd cell_6t
Xbit_r30_c97 bl[97] br[97] wl[30] vdd gnd cell_6t
Xbit_r31_c97 bl[97] br[97] wl[31] vdd gnd cell_6t
Xbit_r32_c97 bl[97] br[97] wl[32] vdd gnd cell_6t
Xbit_r33_c97 bl[97] br[97] wl[33] vdd gnd cell_6t
Xbit_r34_c97 bl[97] br[97] wl[34] vdd gnd cell_6t
Xbit_r35_c97 bl[97] br[97] wl[35] vdd gnd cell_6t
Xbit_r36_c97 bl[97] br[97] wl[36] vdd gnd cell_6t
Xbit_r37_c97 bl[97] br[97] wl[37] vdd gnd cell_6t
Xbit_r38_c97 bl[97] br[97] wl[38] vdd gnd cell_6t
Xbit_r39_c97 bl[97] br[97] wl[39] vdd gnd cell_6t
Xbit_r40_c97 bl[97] br[97] wl[40] vdd gnd cell_6t
Xbit_r41_c97 bl[97] br[97] wl[41] vdd gnd cell_6t
Xbit_r42_c97 bl[97] br[97] wl[42] vdd gnd cell_6t
Xbit_r43_c97 bl[97] br[97] wl[43] vdd gnd cell_6t
Xbit_r44_c97 bl[97] br[97] wl[44] vdd gnd cell_6t
Xbit_r45_c97 bl[97] br[97] wl[45] vdd gnd cell_6t
Xbit_r46_c97 bl[97] br[97] wl[46] vdd gnd cell_6t
Xbit_r47_c97 bl[97] br[97] wl[47] vdd gnd cell_6t
Xbit_r48_c97 bl[97] br[97] wl[48] vdd gnd cell_6t
Xbit_r49_c97 bl[97] br[97] wl[49] vdd gnd cell_6t
Xbit_r50_c97 bl[97] br[97] wl[50] vdd gnd cell_6t
Xbit_r51_c97 bl[97] br[97] wl[51] vdd gnd cell_6t
Xbit_r52_c97 bl[97] br[97] wl[52] vdd gnd cell_6t
Xbit_r53_c97 bl[97] br[97] wl[53] vdd gnd cell_6t
Xbit_r54_c97 bl[97] br[97] wl[54] vdd gnd cell_6t
Xbit_r55_c97 bl[97] br[97] wl[55] vdd gnd cell_6t
Xbit_r56_c97 bl[97] br[97] wl[56] vdd gnd cell_6t
Xbit_r57_c97 bl[97] br[97] wl[57] vdd gnd cell_6t
Xbit_r58_c97 bl[97] br[97] wl[58] vdd gnd cell_6t
Xbit_r59_c97 bl[97] br[97] wl[59] vdd gnd cell_6t
Xbit_r60_c97 bl[97] br[97] wl[60] vdd gnd cell_6t
Xbit_r61_c97 bl[97] br[97] wl[61] vdd gnd cell_6t
Xbit_r62_c97 bl[97] br[97] wl[62] vdd gnd cell_6t
Xbit_r63_c97 bl[97] br[97] wl[63] vdd gnd cell_6t
Xbit_r0_c98 bl[98] br[98] wl[0] vdd gnd cell_6t
Xbit_r1_c98 bl[98] br[98] wl[1] vdd gnd cell_6t
Xbit_r2_c98 bl[98] br[98] wl[2] vdd gnd cell_6t
Xbit_r3_c98 bl[98] br[98] wl[3] vdd gnd cell_6t
Xbit_r4_c98 bl[98] br[98] wl[4] vdd gnd cell_6t
Xbit_r5_c98 bl[98] br[98] wl[5] vdd gnd cell_6t
Xbit_r6_c98 bl[98] br[98] wl[6] vdd gnd cell_6t
Xbit_r7_c98 bl[98] br[98] wl[7] vdd gnd cell_6t
Xbit_r8_c98 bl[98] br[98] wl[8] vdd gnd cell_6t
Xbit_r9_c98 bl[98] br[98] wl[9] vdd gnd cell_6t
Xbit_r10_c98 bl[98] br[98] wl[10] vdd gnd cell_6t
Xbit_r11_c98 bl[98] br[98] wl[11] vdd gnd cell_6t
Xbit_r12_c98 bl[98] br[98] wl[12] vdd gnd cell_6t
Xbit_r13_c98 bl[98] br[98] wl[13] vdd gnd cell_6t
Xbit_r14_c98 bl[98] br[98] wl[14] vdd gnd cell_6t
Xbit_r15_c98 bl[98] br[98] wl[15] vdd gnd cell_6t
Xbit_r16_c98 bl[98] br[98] wl[16] vdd gnd cell_6t
Xbit_r17_c98 bl[98] br[98] wl[17] vdd gnd cell_6t
Xbit_r18_c98 bl[98] br[98] wl[18] vdd gnd cell_6t
Xbit_r19_c98 bl[98] br[98] wl[19] vdd gnd cell_6t
Xbit_r20_c98 bl[98] br[98] wl[20] vdd gnd cell_6t
Xbit_r21_c98 bl[98] br[98] wl[21] vdd gnd cell_6t
Xbit_r22_c98 bl[98] br[98] wl[22] vdd gnd cell_6t
Xbit_r23_c98 bl[98] br[98] wl[23] vdd gnd cell_6t
Xbit_r24_c98 bl[98] br[98] wl[24] vdd gnd cell_6t
Xbit_r25_c98 bl[98] br[98] wl[25] vdd gnd cell_6t
Xbit_r26_c98 bl[98] br[98] wl[26] vdd gnd cell_6t
Xbit_r27_c98 bl[98] br[98] wl[27] vdd gnd cell_6t
Xbit_r28_c98 bl[98] br[98] wl[28] vdd gnd cell_6t
Xbit_r29_c98 bl[98] br[98] wl[29] vdd gnd cell_6t
Xbit_r30_c98 bl[98] br[98] wl[30] vdd gnd cell_6t
Xbit_r31_c98 bl[98] br[98] wl[31] vdd gnd cell_6t
Xbit_r32_c98 bl[98] br[98] wl[32] vdd gnd cell_6t
Xbit_r33_c98 bl[98] br[98] wl[33] vdd gnd cell_6t
Xbit_r34_c98 bl[98] br[98] wl[34] vdd gnd cell_6t
Xbit_r35_c98 bl[98] br[98] wl[35] vdd gnd cell_6t
Xbit_r36_c98 bl[98] br[98] wl[36] vdd gnd cell_6t
Xbit_r37_c98 bl[98] br[98] wl[37] vdd gnd cell_6t
Xbit_r38_c98 bl[98] br[98] wl[38] vdd gnd cell_6t
Xbit_r39_c98 bl[98] br[98] wl[39] vdd gnd cell_6t
Xbit_r40_c98 bl[98] br[98] wl[40] vdd gnd cell_6t
Xbit_r41_c98 bl[98] br[98] wl[41] vdd gnd cell_6t
Xbit_r42_c98 bl[98] br[98] wl[42] vdd gnd cell_6t
Xbit_r43_c98 bl[98] br[98] wl[43] vdd gnd cell_6t
Xbit_r44_c98 bl[98] br[98] wl[44] vdd gnd cell_6t
Xbit_r45_c98 bl[98] br[98] wl[45] vdd gnd cell_6t
Xbit_r46_c98 bl[98] br[98] wl[46] vdd gnd cell_6t
Xbit_r47_c98 bl[98] br[98] wl[47] vdd gnd cell_6t
Xbit_r48_c98 bl[98] br[98] wl[48] vdd gnd cell_6t
Xbit_r49_c98 bl[98] br[98] wl[49] vdd gnd cell_6t
Xbit_r50_c98 bl[98] br[98] wl[50] vdd gnd cell_6t
Xbit_r51_c98 bl[98] br[98] wl[51] vdd gnd cell_6t
Xbit_r52_c98 bl[98] br[98] wl[52] vdd gnd cell_6t
Xbit_r53_c98 bl[98] br[98] wl[53] vdd gnd cell_6t
Xbit_r54_c98 bl[98] br[98] wl[54] vdd gnd cell_6t
Xbit_r55_c98 bl[98] br[98] wl[55] vdd gnd cell_6t
Xbit_r56_c98 bl[98] br[98] wl[56] vdd gnd cell_6t
Xbit_r57_c98 bl[98] br[98] wl[57] vdd gnd cell_6t
Xbit_r58_c98 bl[98] br[98] wl[58] vdd gnd cell_6t
Xbit_r59_c98 bl[98] br[98] wl[59] vdd gnd cell_6t
Xbit_r60_c98 bl[98] br[98] wl[60] vdd gnd cell_6t
Xbit_r61_c98 bl[98] br[98] wl[61] vdd gnd cell_6t
Xbit_r62_c98 bl[98] br[98] wl[62] vdd gnd cell_6t
Xbit_r63_c98 bl[98] br[98] wl[63] vdd gnd cell_6t
Xbit_r0_c99 bl[99] br[99] wl[0] vdd gnd cell_6t
Xbit_r1_c99 bl[99] br[99] wl[1] vdd gnd cell_6t
Xbit_r2_c99 bl[99] br[99] wl[2] vdd gnd cell_6t
Xbit_r3_c99 bl[99] br[99] wl[3] vdd gnd cell_6t
Xbit_r4_c99 bl[99] br[99] wl[4] vdd gnd cell_6t
Xbit_r5_c99 bl[99] br[99] wl[5] vdd gnd cell_6t
Xbit_r6_c99 bl[99] br[99] wl[6] vdd gnd cell_6t
Xbit_r7_c99 bl[99] br[99] wl[7] vdd gnd cell_6t
Xbit_r8_c99 bl[99] br[99] wl[8] vdd gnd cell_6t
Xbit_r9_c99 bl[99] br[99] wl[9] vdd gnd cell_6t
Xbit_r10_c99 bl[99] br[99] wl[10] vdd gnd cell_6t
Xbit_r11_c99 bl[99] br[99] wl[11] vdd gnd cell_6t
Xbit_r12_c99 bl[99] br[99] wl[12] vdd gnd cell_6t
Xbit_r13_c99 bl[99] br[99] wl[13] vdd gnd cell_6t
Xbit_r14_c99 bl[99] br[99] wl[14] vdd gnd cell_6t
Xbit_r15_c99 bl[99] br[99] wl[15] vdd gnd cell_6t
Xbit_r16_c99 bl[99] br[99] wl[16] vdd gnd cell_6t
Xbit_r17_c99 bl[99] br[99] wl[17] vdd gnd cell_6t
Xbit_r18_c99 bl[99] br[99] wl[18] vdd gnd cell_6t
Xbit_r19_c99 bl[99] br[99] wl[19] vdd gnd cell_6t
Xbit_r20_c99 bl[99] br[99] wl[20] vdd gnd cell_6t
Xbit_r21_c99 bl[99] br[99] wl[21] vdd gnd cell_6t
Xbit_r22_c99 bl[99] br[99] wl[22] vdd gnd cell_6t
Xbit_r23_c99 bl[99] br[99] wl[23] vdd gnd cell_6t
Xbit_r24_c99 bl[99] br[99] wl[24] vdd gnd cell_6t
Xbit_r25_c99 bl[99] br[99] wl[25] vdd gnd cell_6t
Xbit_r26_c99 bl[99] br[99] wl[26] vdd gnd cell_6t
Xbit_r27_c99 bl[99] br[99] wl[27] vdd gnd cell_6t
Xbit_r28_c99 bl[99] br[99] wl[28] vdd gnd cell_6t
Xbit_r29_c99 bl[99] br[99] wl[29] vdd gnd cell_6t
Xbit_r30_c99 bl[99] br[99] wl[30] vdd gnd cell_6t
Xbit_r31_c99 bl[99] br[99] wl[31] vdd gnd cell_6t
Xbit_r32_c99 bl[99] br[99] wl[32] vdd gnd cell_6t
Xbit_r33_c99 bl[99] br[99] wl[33] vdd gnd cell_6t
Xbit_r34_c99 bl[99] br[99] wl[34] vdd gnd cell_6t
Xbit_r35_c99 bl[99] br[99] wl[35] vdd gnd cell_6t
Xbit_r36_c99 bl[99] br[99] wl[36] vdd gnd cell_6t
Xbit_r37_c99 bl[99] br[99] wl[37] vdd gnd cell_6t
Xbit_r38_c99 bl[99] br[99] wl[38] vdd gnd cell_6t
Xbit_r39_c99 bl[99] br[99] wl[39] vdd gnd cell_6t
Xbit_r40_c99 bl[99] br[99] wl[40] vdd gnd cell_6t
Xbit_r41_c99 bl[99] br[99] wl[41] vdd gnd cell_6t
Xbit_r42_c99 bl[99] br[99] wl[42] vdd gnd cell_6t
Xbit_r43_c99 bl[99] br[99] wl[43] vdd gnd cell_6t
Xbit_r44_c99 bl[99] br[99] wl[44] vdd gnd cell_6t
Xbit_r45_c99 bl[99] br[99] wl[45] vdd gnd cell_6t
Xbit_r46_c99 bl[99] br[99] wl[46] vdd gnd cell_6t
Xbit_r47_c99 bl[99] br[99] wl[47] vdd gnd cell_6t
Xbit_r48_c99 bl[99] br[99] wl[48] vdd gnd cell_6t
Xbit_r49_c99 bl[99] br[99] wl[49] vdd gnd cell_6t
Xbit_r50_c99 bl[99] br[99] wl[50] vdd gnd cell_6t
Xbit_r51_c99 bl[99] br[99] wl[51] vdd gnd cell_6t
Xbit_r52_c99 bl[99] br[99] wl[52] vdd gnd cell_6t
Xbit_r53_c99 bl[99] br[99] wl[53] vdd gnd cell_6t
Xbit_r54_c99 bl[99] br[99] wl[54] vdd gnd cell_6t
Xbit_r55_c99 bl[99] br[99] wl[55] vdd gnd cell_6t
Xbit_r56_c99 bl[99] br[99] wl[56] vdd gnd cell_6t
Xbit_r57_c99 bl[99] br[99] wl[57] vdd gnd cell_6t
Xbit_r58_c99 bl[99] br[99] wl[58] vdd gnd cell_6t
Xbit_r59_c99 bl[99] br[99] wl[59] vdd gnd cell_6t
Xbit_r60_c99 bl[99] br[99] wl[60] vdd gnd cell_6t
Xbit_r61_c99 bl[99] br[99] wl[61] vdd gnd cell_6t
Xbit_r62_c99 bl[99] br[99] wl[62] vdd gnd cell_6t
Xbit_r63_c99 bl[99] br[99] wl[63] vdd gnd cell_6t
Xbit_r0_c100 bl[100] br[100] wl[0] vdd gnd cell_6t
Xbit_r1_c100 bl[100] br[100] wl[1] vdd gnd cell_6t
Xbit_r2_c100 bl[100] br[100] wl[2] vdd gnd cell_6t
Xbit_r3_c100 bl[100] br[100] wl[3] vdd gnd cell_6t
Xbit_r4_c100 bl[100] br[100] wl[4] vdd gnd cell_6t
Xbit_r5_c100 bl[100] br[100] wl[5] vdd gnd cell_6t
Xbit_r6_c100 bl[100] br[100] wl[6] vdd gnd cell_6t
Xbit_r7_c100 bl[100] br[100] wl[7] vdd gnd cell_6t
Xbit_r8_c100 bl[100] br[100] wl[8] vdd gnd cell_6t
Xbit_r9_c100 bl[100] br[100] wl[9] vdd gnd cell_6t
Xbit_r10_c100 bl[100] br[100] wl[10] vdd gnd cell_6t
Xbit_r11_c100 bl[100] br[100] wl[11] vdd gnd cell_6t
Xbit_r12_c100 bl[100] br[100] wl[12] vdd gnd cell_6t
Xbit_r13_c100 bl[100] br[100] wl[13] vdd gnd cell_6t
Xbit_r14_c100 bl[100] br[100] wl[14] vdd gnd cell_6t
Xbit_r15_c100 bl[100] br[100] wl[15] vdd gnd cell_6t
Xbit_r16_c100 bl[100] br[100] wl[16] vdd gnd cell_6t
Xbit_r17_c100 bl[100] br[100] wl[17] vdd gnd cell_6t
Xbit_r18_c100 bl[100] br[100] wl[18] vdd gnd cell_6t
Xbit_r19_c100 bl[100] br[100] wl[19] vdd gnd cell_6t
Xbit_r20_c100 bl[100] br[100] wl[20] vdd gnd cell_6t
Xbit_r21_c100 bl[100] br[100] wl[21] vdd gnd cell_6t
Xbit_r22_c100 bl[100] br[100] wl[22] vdd gnd cell_6t
Xbit_r23_c100 bl[100] br[100] wl[23] vdd gnd cell_6t
Xbit_r24_c100 bl[100] br[100] wl[24] vdd gnd cell_6t
Xbit_r25_c100 bl[100] br[100] wl[25] vdd gnd cell_6t
Xbit_r26_c100 bl[100] br[100] wl[26] vdd gnd cell_6t
Xbit_r27_c100 bl[100] br[100] wl[27] vdd gnd cell_6t
Xbit_r28_c100 bl[100] br[100] wl[28] vdd gnd cell_6t
Xbit_r29_c100 bl[100] br[100] wl[29] vdd gnd cell_6t
Xbit_r30_c100 bl[100] br[100] wl[30] vdd gnd cell_6t
Xbit_r31_c100 bl[100] br[100] wl[31] vdd gnd cell_6t
Xbit_r32_c100 bl[100] br[100] wl[32] vdd gnd cell_6t
Xbit_r33_c100 bl[100] br[100] wl[33] vdd gnd cell_6t
Xbit_r34_c100 bl[100] br[100] wl[34] vdd gnd cell_6t
Xbit_r35_c100 bl[100] br[100] wl[35] vdd gnd cell_6t
Xbit_r36_c100 bl[100] br[100] wl[36] vdd gnd cell_6t
Xbit_r37_c100 bl[100] br[100] wl[37] vdd gnd cell_6t
Xbit_r38_c100 bl[100] br[100] wl[38] vdd gnd cell_6t
Xbit_r39_c100 bl[100] br[100] wl[39] vdd gnd cell_6t
Xbit_r40_c100 bl[100] br[100] wl[40] vdd gnd cell_6t
Xbit_r41_c100 bl[100] br[100] wl[41] vdd gnd cell_6t
Xbit_r42_c100 bl[100] br[100] wl[42] vdd gnd cell_6t
Xbit_r43_c100 bl[100] br[100] wl[43] vdd gnd cell_6t
Xbit_r44_c100 bl[100] br[100] wl[44] vdd gnd cell_6t
Xbit_r45_c100 bl[100] br[100] wl[45] vdd gnd cell_6t
Xbit_r46_c100 bl[100] br[100] wl[46] vdd gnd cell_6t
Xbit_r47_c100 bl[100] br[100] wl[47] vdd gnd cell_6t
Xbit_r48_c100 bl[100] br[100] wl[48] vdd gnd cell_6t
Xbit_r49_c100 bl[100] br[100] wl[49] vdd gnd cell_6t
Xbit_r50_c100 bl[100] br[100] wl[50] vdd gnd cell_6t
Xbit_r51_c100 bl[100] br[100] wl[51] vdd gnd cell_6t
Xbit_r52_c100 bl[100] br[100] wl[52] vdd gnd cell_6t
Xbit_r53_c100 bl[100] br[100] wl[53] vdd gnd cell_6t
Xbit_r54_c100 bl[100] br[100] wl[54] vdd gnd cell_6t
Xbit_r55_c100 bl[100] br[100] wl[55] vdd gnd cell_6t
Xbit_r56_c100 bl[100] br[100] wl[56] vdd gnd cell_6t
Xbit_r57_c100 bl[100] br[100] wl[57] vdd gnd cell_6t
Xbit_r58_c100 bl[100] br[100] wl[58] vdd gnd cell_6t
Xbit_r59_c100 bl[100] br[100] wl[59] vdd gnd cell_6t
Xbit_r60_c100 bl[100] br[100] wl[60] vdd gnd cell_6t
Xbit_r61_c100 bl[100] br[100] wl[61] vdd gnd cell_6t
Xbit_r62_c100 bl[100] br[100] wl[62] vdd gnd cell_6t
Xbit_r63_c100 bl[100] br[100] wl[63] vdd gnd cell_6t
Xbit_r0_c101 bl[101] br[101] wl[0] vdd gnd cell_6t
Xbit_r1_c101 bl[101] br[101] wl[1] vdd gnd cell_6t
Xbit_r2_c101 bl[101] br[101] wl[2] vdd gnd cell_6t
Xbit_r3_c101 bl[101] br[101] wl[3] vdd gnd cell_6t
Xbit_r4_c101 bl[101] br[101] wl[4] vdd gnd cell_6t
Xbit_r5_c101 bl[101] br[101] wl[5] vdd gnd cell_6t
Xbit_r6_c101 bl[101] br[101] wl[6] vdd gnd cell_6t
Xbit_r7_c101 bl[101] br[101] wl[7] vdd gnd cell_6t
Xbit_r8_c101 bl[101] br[101] wl[8] vdd gnd cell_6t
Xbit_r9_c101 bl[101] br[101] wl[9] vdd gnd cell_6t
Xbit_r10_c101 bl[101] br[101] wl[10] vdd gnd cell_6t
Xbit_r11_c101 bl[101] br[101] wl[11] vdd gnd cell_6t
Xbit_r12_c101 bl[101] br[101] wl[12] vdd gnd cell_6t
Xbit_r13_c101 bl[101] br[101] wl[13] vdd gnd cell_6t
Xbit_r14_c101 bl[101] br[101] wl[14] vdd gnd cell_6t
Xbit_r15_c101 bl[101] br[101] wl[15] vdd gnd cell_6t
Xbit_r16_c101 bl[101] br[101] wl[16] vdd gnd cell_6t
Xbit_r17_c101 bl[101] br[101] wl[17] vdd gnd cell_6t
Xbit_r18_c101 bl[101] br[101] wl[18] vdd gnd cell_6t
Xbit_r19_c101 bl[101] br[101] wl[19] vdd gnd cell_6t
Xbit_r20_c101 bl[101] br[101] wl[20] vdd gnd cell_6t
Xbit_r21_c101 bl[101] br[101] wl[21] vdd gnd cell_6t
Xbit_r22_c101 bl[101] br[101] wl[22] vdd gnd cell_6t
Xbit_r23_c101 bl[101] br[101] wl[23] vdd gnd cell_6t
Xbit_r24_c101 bl[101] br[101] wl[24] vdd gnd cell_6t
Xbit_r25_c101 bl[101] br[101] wl[25] vdd gnd cell_6t
Xbit_r26_c101 bl[101] br[101] wl[26] vdd gnd cell_6t
Xbit_r27_c101 bl[101] br[101] wl[27] vdd gnd cell_6t
Xbit_r28_c101 bl[101] br[101] wl[28] vdd gnd cell_6t
Xbit_r29_c101 bl[101] br[101] wl[29] vdd gnd cell_6t
Xbit_r30_c101 bl[101] br[101] wl[30] vdd gnd cell_6t
Xbit_r31_c101 bl[101] br[101] wl[31] vdd gnd cell_6t
Xbit_r32_c101 bl[101] br[101] wl[32] vdd gnd cell_6t
Xbit_r33_c101 bl[101] br[101] wl[33] vdd gnd cell_6t
Xbit_r34_c101 bl[101] br[101] wl[34] vdd gnd cell_6t
Xbit_r35_c101 bl[101] br[101] wl[35] vdd gnd cell_6t
Xbit_r36_c101 bl[101] br[101] wl[36] vdd gnd cell_6t
Xbit_r37_c101 bl[101] br[101] wl[37] vdd gnd cell_6t
Xbit_r38_c101 bl[101] br[101] wl[38] vdd gnd cell_6t
Xbit_r39_c101 bl[101] br[101] wl[39] vdd gnd cell_6t
Xbit_r40_c101 bl[101] br[101] wl[40] vdd gnd cell_6t
Xbit_r41_c101 bl[101] br[101] wl[41] vdd gnd cell_6t
Xbit_r42_c101 bl[101] br[101] wl[42] vdd gnd cell_6t
Xbit_r43_c101 bl[101] br[101] wl[43] vdd gnd cell_6t
Xbit_r44_c101 bl[101] br[101] wl[44] vdd gnd cell_6t
Xbit_r45_c101 bl[101] br[101] wl[45] vdd gnd cell_6t
Xbit_r46_c101 bl[101] br[101] wl[46] vdd gnd cell_6t
Xbit_r47_c101 bl[101] br[101] wl[47] vdd gnd cell_6t
Xbit_r48_c101 bl[101] br[101] wl[48] vdd gnd cell_6t
Xbit_r49_c101 bl[101] br[101] wl[49] vdd gnd cell_6t
Xbit_r50_c101 bl[101] br[101] wl[50] vdd gnd cell_6t
Xbit_r51_c101 bl[101] br[101] wl[51] vdd gnd cell_6t
Xbit_r52_c101 bl[101] br[101] wl[52] vdd gnd cell_6t
Xbit_r53_c101 bl[101] br[101] wl[53] vdd gnd cell_6t
Xbit_r54_c101 bl[101] br[101] wl[54] vdd gnd cell_6t
Xbit_r55_c101 bl[101] br[101] wl[55] vdd gnd cell_6t
Xbit_r56_c101 bl[101] br[101] wl[56] vdd gnd cell_6t
Xbit_r57_c101 bl[101] br[101] wl[57] vdd gnd cell_6t
Xbit_r58_c101 bl[101] br[101] wl[58] vdd gnd cell_6t
Xbit_r59_c101 bl[101] br[101] wl[59] vdd gnd cell_6t
Xbit_r60_c101 bl[101] br[101] wl[60] vdd gnd cell_6t
Xbit_r61_c101 bl[101] br[101] wl[61] vdd gnd cell_6t
Xbit_r62_c101 bl[101] br[101] wl[62] vdd gnd cell_6t
Xbit_r63_c101 bl[101] br[101] wl[63] vdd gnd cell_6t
Xbit_r0_c102 bl[102] br[102] wl[0] vdd gnd cell_6t
Xbit_r1_c102 bl[102] br[102] wl[1] vdd gnd cell_6t
Xbit_r2_c102 bl[102] br[102] wl[2] vdd gnd cell_6t
Xbit_r3_c102 bl[102] br[102] wl[3] vdd gnd cell_6t
Xbit_r4_c102 bl[102] br[102] wl[4] vdd gnd cell_6t
Xbit_r5_c102 bl[102] br[102] wl[5] vdd gnd cell_6t
Xbit_r6_c102 bl[102] br[102] wl[6] vdd gnd cell_6t
Xbit_r7_c102 bl[102] br[102] wl[7] vdd gnd cell_6t
Xbit_r8_c102 bl[102] br[102] wl[8] vdd gnd cell_6t
Xbit_r9_c102 bl[102] br[102] wl[9] vdd gnd cell_6t
Xbit_r10_c102 bl[102] br[102] wl[10] vdd gnd cell_6t
Xbit_r11_c102 bl[102] br[102] wl[11] vdd gnd cell_6t
Xbit_r12_c102 bl[102] br[102] wl[12] vdd gnd cell_6t
Xbit_r13_c102 bl[102] br[102] wl[13] vdd gnd cell_6t
Xbit_r14_c102 bl[102] br[102] wl[14] vdd gnd cell_6t
Xbit_r15_c102 bl[102] br[102] wl[15] vdd gnd cell_6t
Xbit_r16_c102 bl[102] br[102] wl[16] vdd gnd cell_6t
Xbit_r17_c102 bl[102] br[102] wl[17] vdd gnd cell_6t
Xbit_r18_c102 bl[102] br[102] wl[18] vdd gnd cell_6t
Xbit_r19_c102 bl[102] br[102] wl[19] vdd gnd cell_6t
Xbit_r20_c102 bl[102] br[102] wl[20] vdd gnd cell_6t
Xbit_r21_c102 bl[102] br[102] wl[21] vdd gnd cell_6t
Xbit_r22_c102 bl[102] br[102] wl[22] vdd gnd cell_6t
Xbit_r23_c102 bl[102] br[102] wl[23] vdd gnd cell_6t
Xbit_r24_c102 bl[102] br[102] wl[24] vdd gnd cell_6t
Xbit_r25_c102 bl[102] br[102] wl[25] vdd gnd cell_6t
Xbit_r26_c102 bl[102] br[102] wl[26] vdd gnd cell_6t
Xbit_r27_c102 bl[102] br[102] wl[27] vdd gnd cell_6t
Xbit_r28_c102 bl[102] br[102] wl[28] vdd gnd cell_6t
Xbit_r29_c102 bl[102] br[102] wl[29] vdd gnd cell_6t
Xbit_r30_c102 bl[102] br[102] wl[30] vdd gnd cell_6t
Xbit_r31_c102 bl[102] br[102] wl[31] vdd gnd cell_6t
Xbit_r32_c102 bl[102] br[102] wl[32] vdd gnd cell_6t
Xbit_r33_c102 bl[102] br[102] wl[33] vdd gnd cell_6t
Xbit_r34_c102 bl[102] br[102] wl[34] vdd gnd cell_6t
Xbit_r35_c102 bl[102] br[102] wl[35] vdd gnd cell_6t
Xbit_r36_c102 bl[102] br[102] wl[36] vdd gnd cell_6t
Xbit_r37_c102 bl[102] br[102] wl[37] vdd gnd cell_6t
Xbit_r38_c102 bl[102] br[102] wl[38] vdd gnd cell_6t
Xbit_r39_c102 bl[102] br[102] wl[39] vdd gnd cell_6t
Xbit_r40_c102 bl[102] br[102] wl[40] vdd gnd cell_6t
Xbit_r41_c102 bl[102] br[102] wl[41] vdd gnd cell_6t
Xbit_r42_c102 bl[102] br[102] wl[42] vdd gnd cell_6t
Xbit_r43_c102 bl[102] br[102] wl[43] vdd gnd cell_6t
Xbit_r44_c102 bl[102] br[102] wl[44] vdd gnd cell_6t
Xbit_r45_c102 bl[102] br[102] wl[45] vdd gnd cell_6t
Xbit_r46_c102 bl[102] br[102] wl[46] vdd gnd cell_6t
Xbit_r47_c102 bl[102] br[102] wl[47] vdd gnd cell_6t
Xbit_r48_c102 bl[102] br[102] wl[48] vdd gnd cell_6t
Xbit_r49_c102 bl[102] br[102] wl[49] vdd gnd cell_6t
Xbit_r50_c102 bl[102] br[102] wl[50] vdd gnd cell_6t
Xbit_r51_c102 bl[102] br[102] wl[51] vdd gnd cell_6t
Xbit_r52_c102 bl[102] br[102] wl[52] vdd gnd cell_6t
Xbit_r53_c102 bl[102] br[102] wl[53] vdd gnd cell_6t
Xbit_r54_c102 bl[102] br[102] wl[54] vdd gnd cell_6t
Xbit_r55_c102 bl[102] br[102] wl[55] vdd gnd cell_6t
Xbit_r56_c102 bl[102] br[102] wl[56] vdd gnd cell_6t
Xbit_r57_c102 bl[102] br[102] wl[57] vdd gnd cell_6t
Xbit_r58_c102 bl[102] br[102] wl[58] vdd gnd cell_6t
Xbit_r59_c102 bl[102] br[102] wl[59] vdd gnd cell_6t
Xbit_r60_c102 bl[102] br[102] wl[60] vdd gnd cell_6t
Xbit_r61_c102 bl[102] br[102] wl[61] vdd gnd cell_6t
Xbit_r62_c102 bl[102] br[102] wl[62] vdd gnd cell_6t
Xbit_r63_c102 bl[102] br[102] wl[63] vdd gnd cell_6t
Xbit_r0_c103 bl[103] br[103] wl[0] vdd gnd cell_6t
Xbit_r1_c103 bl[103] br[103] wl[1] vdd gnd cell_6t
Xbit_r2_c103 bl[103] br[103] wl[2] vdd gnd cell_6t
Xbit_r3_c103 bl[103] br[103] wl[3] vdd gnd cell_6t
Xbit_r4_c103 bl[103] br[103] wl[4] vdd gnd cell_6t
Xbit_r5_c103 bl[103] br[103] wl[5] vdd gnd cell_6t
Xbit_r6_c103 bl[103] br[103] wl[6] vdd gnd cell_6t
Xbit_r7_c103 bl[103] br[103] wl[7] vdd gnd cell_6t
Xbit_r8_c103 bl[103] br[103] wl[8] vdd gnd cell_6t
Xbit_r9_c103 bl[103] br[103] wl[9] vdd gnd cell_6t
Xbit_r10_c103 bl[103] br[103] wl[10] vdd gnd cell_6t
Xbit_r11_c103 bl[103] br[103] wl[11] vdd gnd cell_6t
Xbit_r12_c103 bl[103] br[103] wl[12] vdd gnd cell_6t
Xbit_r13_c103 bl[103] br[103] wl[13] vdd gnd cell_6t
Xbit_r14_c103 bl[103] br[103] wl[14] vdd gnd cell_6t
Xbit_r15_c103 bl[103] br[103] wl[15] vdd gnd cell_6t
Xbit_r16_c103 bl[103] br[103] wl[16] vdd gnd cell_6t
Xbit_r17_c103 bl[103] br[103] wl[17] vdd gnd cell_6t
Xbit_r18_c103 bl[103] br[103] wl[18] vdd gnd cell_6t
Xbit_r19_c103 bl[103] br[103] wl[19] vdd gnd cell_6t
Xbit_r20_c103 bl[103] br[103] wl[20] vdd gnd cell_6t
Xbit_r21_c103 bl[103] br[103] wl[21] vdd gnd cell_6t
Xbit_r22_c103 bl[103] br[103] wl[22] vdd gnd cell_6t
Xbit_r23_c103 bl[103] br[103] wl[23] vdd gnd cell_6t
Xbit_r24_c103 bl[103] br[103] wl[24] vdd gnd cell_6t
Xbit_r25_c103 bl[103] br[103] wl[25] vdd gnd cell_6t
Xbit_r26_c103 bl[103] br[103] wl[26] vdd gnd cell_6t
Xbit_r27_c103 bl[103] br[103] wl[27] vdd gnd cell_6t
Xbit_r28_c103 bl[103] br[103] wl[28] vdd gnd cell_6t
Xbit_r29_c103 bl[103] br[103] wl[29] vdd gnd cell_6t
Xbit_r30_c103 bl[103] br[103] wl[30] vdd gnd cell_6t
Xbit_r31_c103 bl[103] br[103] wl[31] vdd gnd cell_6t
Xbit_r32_c103 bl[103] br[103] wl[32] vdd gnd cell_6t
Xbit_r33_c103 bl[103] br[103] wl[33] vdd gnd cell_6t
Xbit_r34_c103 bl[103] br[103] wl[34] vdd gnd cell_6t
Xbit_r35_c103 bl[103] br[103] wl[35] vdd gnd cell_6t
Xbit_r36_c103 bl[103] br[103] wl[36] vdd gnd cell_6t
Xbit_r37_c103 bl[103] br[103] wl[37] vdd gnd cell_6t
Xbit_r38_c103 bl[103] br[103] wl[38] vdd gnd cell_6t
Xbit_r39_c103 bl[103] br[103] wl[39] vdd gnd cell_6t
Xbit_r40_c103 bl[103] br[103] wl[40] vdd gnd cell_6t
Xbit_r41_c103 bl[103] br[103] wl[41] vdd gnd cell_6t
Xbit_r42_c103 bl[103] br[103] wl[42] vdd gnd cell_6t
Xbit_r43_c103 bl[103] br[103] wl[43] vdd gnd cell_6t
Xbit_r44_c103 bl[103] br[103] wl[44] vdd gnd cell_6t
Xbit_r45_c103 bl[103] br[103] wl[45] vdd gnd cell_6t
Xbit_r46_c103 bl[103] br[103] wl[46] vdd gnd cell_6t
Xbit_r47_c103 bl[103] br[103] wl[47] vdd gnd cell_6t
Xbit_r48_c103 bl[103] br[103] wl[48] vdd gnd cell_6t
Xbit_r49_c103 bl[103] br[103] wl[49] vdd gnd cell_6t
Xbit_r50_c103 bl[103] br[103] wl[50] vdd gnd cell_6t
Xbit_r51_c103 bl[103] br[103] wl[51] vdd gnd cell_6t
Xbit_r52_c103 bl[103] br[103] wl[52] vdd gnd cell_6t
Xbit_r53_c103 bl[103] br[103] wl[53] vdd gnd cell_6t
Xbit_r54_c103 bl[103] br[103] wl[54] vdd gnd cell_6t
Xbit_r55_c103 bl[103] br[103] wl[55] vdd gnd cell_6t
Xbit_r56_c103 bl[103] br[103] wl[56] vdd gnd cell_6t
Xbit_r57_c103 bl[103] br[103] wl[57] vdd gnd cell_6t
Xbit_r58_c103 bl[103] br[103] wl[58] vdd gnd cell_6t
Xbit_r59_c103 bl[103] br[103] wl[59] vdd gnd cell_6t
Xbit_r60_c103 bl[103] br[103] wl[60] vdd gnd cell_6t
Xbit_r61_c103 bl[103] br[103] wl[61] vdd gnd cell_6t
Xbit_r62_c103 bl[103] br[103] wl[62] vdd gnd cell_6t
Xbit_r63_c103 bl[103] br[103] wl[63] vdd gnd cell_6t
Xbit_r0_c104 bl[104] br[104] wl[0] vdd gnd cell_6t
Xbit_r1_c104 bl[104] br[104] wl[1] vdd gnd cell_6t
Xbit_r2_c104 bl[104] br[104] wl[2] vdd gnd cell_6t
Xbit_r3_c104 bl[104] br[104] wl[3] vdd gnd cell_6t
Xbit_r4_c104 bl[104] br[104] wl[4] vdd gnd cell_6t
Xbit_r5_c104 bl[104] br[104] wl[5] vdd gnd cell_6t
Xbit_r6_c104 bl[104] br[104] wl[6] vdd gnd cell_6t
Xbit_r7_c104 bl[104] br[104] wl[7] vdd gnd cell_6t
Xbit_r8_c104 bl[104] br[104] wl[8] vdd gnd cell_6t
Xbit_r9_c104 bl[104] br[104] wl[9] vdd gnd cell_6t
Xbit_r10_c104 bl[104] br[104] wl[10] vdd gnd cell_6t
Xbit_r11_c104 bl[104] br[104] wl[11] vdd gnd cell_6t
Xbit_r12_c104 bl[104] br[104] wl[12] vdd gnd cell_6t
Xbit_r13_c104 bl[104] br[104] wl[13] vdd gnd cell_6t
Xbit_r14_c104 bl[104] br[104] wl[14] vdd gnd cell_6t
Xbit_r15_c104 bl[104] br[104] wl[15] vdd gnd cell_6t
Xbit_r16_c104 bl[104] br[104] wl[16] vdd gnd cell_6t
Xbit_r17_c104 bl[104] br[104] wl[17] vdd gnd cell_6t
Xbit_r18_c104 bl[104] br[104] wl[18] vdd gnd cell_6t
Xbit_r19_c104 bl[104] br[104] wl[19] vdd gnd cell_6t
Xbit_r20_c104 bl[104] br[104] wl[20] vdd gnd cell_6t
Xbit_r21_c104 bl[104] br[104] wl[21] vdd gnd cell_6t
Xbit_r22_c104 bl[104] br[104] wl[22] vdd gnd cell_6t
Xbit_r23_c104 bl[104] br[104] wl[23] vdd gnd cell_6t
Xbit_r24_c104 bl[104] br[104] wl[24] vdd gnd cell_6t
Xbit_r25_c104 bl[104] br[104] wl[25] vdd gnd cell_6t
Xbit_r26_c104 bl[104] br[104] wl[26] vdd gnd cell_6t
Xbit_r27_c104 bl[104] br[104] wl[27] vdd gnd cell_6t
Xbit_r28_c104 bl[104] br[104] wl[28] vdd gnd cell_6t
Xbit_r29_c104 bl[104] br[104] wl[29] vdd gnd cell_6t
Xbit_r30_c104 bl[104] br[104] wl[30] vdd gnd cell_6t
Xbit_r31_c104 bl[104] br[104] wl[31] vdd gnd cell_6t
Xbit_r32_c104 bl[104] br[104] wl[32] vdd gnd cell_6t
Xbit_r33_c104 bl[104] br[104] wl[33] vdd gnd cell_6t
Xbit_r34_c104 bl[104] br[104] wl[34] vdd gnd cell_6t
Xbit_r35_c104 bl[104] br[104] wl[35] vdd gnd cell_6t
Xbit_r36_c104 bl[104] br[104] wl[36] vdd gnd cell_6t
Xbit_r37_c104 bl[104] br[104] wl[37] vdd gnd cell_6t
Xbit_r38_c104 bl[104] br[104] wl[38] vdd gnd cell_6t
Xbit_r39_c104 bl[104] br[104] wl[39] vdd gnd cell_6t
Xbit_r40_c104 bl[104] br[104] wl[40] vdd gnd cell_6t
Xbit_r41_c104 bl[104] br[104] wl[41] vdd gnd cell_6t
Xbit_r42_c104 bl[104] br[104] wl[42] vdd gnd cell_6t
Xbit_r43_c104 bl[104] br[104] wl[43] vdd gnd cell_6t
Xbit_r44_c104 bl[104] br[104] wl[44] vdd gnd cell_6t
Xbit_r45_c104 bl[104] br[104] wl[45] vdd gnd cell_6t
Xbit_r46_c104 bl[104] br[104] wl[46] vdd gnd cell_6t
Xbit_r47_c104 bl[104] br[104] wl[47] vdd gnd cell_6t
Xbit_r48_c104 bl[104] br[104] wl[48] vdd gnd cell_6t
Xbit_r49_c104 bl[104] br[104] wl[49] vdd gnd cell_6t
Xbit_r50_c104 bl[104] br[104] wl[50] vdd gnd cell_6t
Xbit_r51_c104 bl[104] br[104] wl[51] vdd gnd cell_6t
Xbit_r52_c104 bl[104] br[104] wl[52] vdd gnd cell_6t
Xbit_r53_c104 bl[104] br[104] wl[53] vdd gnd cell_6t
Xbit_r54_c104 bl[104] br[104] wl[54] vdd gnd cell_6t
Xbit_r55_c104 bl[104] br[104] wl[55] vdd gnd cell_6t
Xbit_r56_c104 bl[104] br[104] wl[56] vdd gnd cell_6t
Xbit_r57_c104 bl[104] br[104] wl[57] vdd gnd cell_6t
Xbit_r58_c104 bl[104] br[104] wl[58] vdd gnd cell_6t
Xbit_r59_c104 bl[104] br[104] wl[59] vdd gnd cell_6t
Xbit_r60_c104 bl[104] br[104] wl[60] vdd gnd cell_6t
Xbit_r61_c104 bl[104] br[104] wl[61] vdd gnd cell_6t
Xbit_r62_c104 bl[104] br[104] wl[62] vdd gnd cell_6t
Xbit_r63_c104 bl[104] br[104] wl[63] vdd gnd cell_6t
Xbit_r0_c105 bl[105] br[105] wl[0] vdd gnd cell_6t
Xbit_r1_c105 bl[105] br[105] wl[1] vdd gnd cell_6t
Xbit_r2_c105 bl[105] br[105] wl[2] vdd gnd cell_6t
Xbit_r3_c105 bl[105] br[105] wl[3] vdd gnd cell_6t
Xbit_r4_c105 bl[105] br[105] wl[4] vdd gnd cell_6t
Xbit_r5_c105 bl[105] br[105] wl[5] vdd gnd cell_6t
Xbit_r6_c105 bl[105] br[105] wl[6] vdd gnd cell_6t
Xbit_r7_c105 bl[105] br[105] wl[7] vdd gnd cell_6t
Xbit_r8_c105 bl[105] br[105] wl[8] vdd gnd cell_6t
Xbit_r9_c105 bl[105] br[105] wl[9] vdd gnd cell_6t
Xbit_r10_c105 bl[105] br[105] wl[10] vdd gnd cell_6t
Xbit_r11_c105 bl[105] br[105] wl[11] vdd gnd cell_6t
Xbit_r12_c105 bl[105] br[105] wl[12] vdd gnd cell_6t
Xbit_r13_c105 bl[105] br[105] wl[13] vdd gnd cell_6t
Xbit_r14_c105 bl[105] br[105] wl[14] vdd gnd cell_6t
Xbit_r15_c105 bl[105] br[105] wl[15] vdd gnd cell_6t
Xbit_r16_c105 bl[105] br[105] wl[16] vdd gnd cell_6t
Xbit_r17_c105 bl[105] br[105] wl[17] vdd gnd cell_6t
Xbit_r18_c105 bl[105] br[105] wl[18] vdd gnd cell_6t
Xbit_r19_c105 bl[105] br[105] wl[19] vdd gnd cell_6t
Xbit_r20_c105 bl[105] br[105] wl[20] vdd gnd cell_6t
Xbit_r21_c105 bl[105] br[105] wl[21] vdd gnd cell_6t
Xbit_r22_c105 bl[105] br[105] wl[22] vdd gnd cell_6t
Xbit_r23_c105 bl[105] br[105] wl[23] vdd gnd cell_6t
Xbit_r24_c105 bl[105] br[105] wl[24] vdd gnd cell_6t
Xbit_r25_c105 bl[105] br[105] wl[25] vdd gnd cell_6t
Xbit_r26_c105 bl[105] br[105] wl[26] vdd gnd cell_6t
Xbit_r27_c105 bl[105] br[105] wl[27] vdd gnd cell_6t
Xbit_r28_c105 bl[105] br[105] wl[28] vdd gnd cell_6t
Xbit_r29_c105 bl[105] br[105] wl[29] vdd gnd cell_6t
Xbit_r30_c105 bl[105] br[105] wl[30] vdd gnd cell_6t
Xbit_r31_c105 bl[105] br[105] wl[31] vdd gnd cell_6t
Xbit_r32_c105 bl[105] br[105] wl[32] vdd gnd cell_6t
Xbit_r33_c105 bl[105] br[105] wl[33] vdd gnd cell_6t
Xbit_r34_c105 bl[105] br[105] wl[34] vdd gnd cell_6t
Xbit_r35_c105 bl[105] br[105] wl[35] vdd gnd cell_6t
Xbit_r36_c105 bl[105] br[105] wl[36] vdd gnd cell_6t
Xbit_r37_c105 bl[105] br[105] wl[37] vdd gnd cell_6t
Xbit_r38_c105 bl[105] br[105] wl[38] vdd gnd cell_6t
Xbit_r39_c105 bl[105] br[105] wl[39] vdd gnd cell_6t
Xbit_r40_c105 bl[105] br[105] wl[40] vdd gnd cell_6t
Xbit_r41_c105 bl[105] br[105] wl[41] vdd gnd cell_6t
Xbit_r42_c105 bl[105] br[105] wl[42] vdd gnd cell_6t
Xbit_r43_c105 bl[105] br[105] wl[43] vdd gnd cell_6t
Xbit_r44_c105 bl[105] br[105] wl[44] vdd gnd cell_6t
Xbit_r45_c105 bl[105] br[105] wl[45] vdd gnd cell_6t
Xbit_r46_c105 bl[105] br[105] wl[46] vdd gnd cell_6t
Xbit_r47_c105 bl[105] br[105] wl[47] vdd gnd cell_6t
Xbit_r48_c105 bl[105] br[105] wl[48] vdd gnd cell_6t
Xbit_r49_c105 bl[105] br[105] wl[49] vdd gnd cell_6t
Xbit_r50_c105 bl[105] br[105] wl[50] vdd gnd cell_6t
Xbit_r51_c105 bl[105] br[105] wl[51] vdd gnd cell_6t
Xbit_r52_c105 bl[105] br[105] wl[52] vdd gnd cell_6t
Xbit_r53_c105 bl[105] br[105] wl[53] vdd gnd cell_6t
Xbit_r54_c105 bl[105] br[105] wl[54] vdd gnd cell_6t
Xbit_r55_c105 bl[105] br[105] wl[55] vdd gnd cell_6t
Xbit_r56_c105 bl[105] br[105] wl[56] vdd gnd cell_6t
Xbit_r57_c105 bl[105] br[105] wl[57] vdd gnd cell_6t
Xbit_r58_c105 bl[105] br[105] wl[58] vdd gnd cell_6t
Xbit_r59_c105 bl[105] br[105] wl[59] vdd gnd cell_6t
Xbit_r60_c105 bl[105] br[105] wl[60] vdd gnd cell_6t
Xbit_r61_c105 bl[105] br[105] wl[61] vdd gnd cell_6t
Xbit_r62_c105 bl[105] br[105] wl[62] vdd gnd cell_6t
Xbit_r63_c105 bl[105] br[105] wl[63] vdd gnd cell_6t
Xbit_r0_c106 bl[106] br[106] wl[0] vdd gnd cell_6t
Xbit_r1_c106 bl[106] br[106] wl[1] vdd gnd cell_6t
Xbit_r2_c106 bl[106] br[106] wl[2] vdd gnd cell_6t
Xbit_r3_c106 bl[106] br[106] wl[3] vdd gnd cell_6t
Xbit_r4_c106 bl[106] br[106] wl[4] vdd gnd cell_6t
Xbit_r5_c106 bl[106] br[106] wl[5] vdd gnd cell_6t
Xbit_r6_c106 bl[106] br[106] wl[6] vdd gnd cell_6t
Xbit_r7_c106 bl[106] br[106] wl[7] vdd gnd cell_6t
Xbit_r8_c106 bl[106] br[106] wl[8] vdd gnd cell_6t
Xbit_r9_c106 bl[106] br[106] wl[9] vdd gnd cell_6t
Xbit_r10_c106 bl[106] br[106] wl[10] vdd gnd cell_6t
Xbit_r11_c106 bl[106] br[106] wl[11] vdd gnd cell_6t
Xbit_r12_c106 bl[106] br[106] wl[12] vdd gnd cell_6t
Xbit_r13_c106 bl[106] br[106] wl[13] vdd gnd cell_6t
Xbit_r14_c106 bl[106] br[106] wl[14] vdd gnd cell_6t
Xbit_r15_c106 bl[106] br[106] wl[15] vdd gnd cell_6t
Xbit_r16_c106 bl[106] br[106] wl[16] vdd gnd cell_6t
Xbit_r17_c106 bl[106] br[106] wl[17] vdd gnd cell_6t
Xbit_r18_c106 bl[106] br[106] wl[18] vdd gnd cell_6t
Xbit_r19_c106 bl[106] br[106] wl[19] vdd gnd cell_6t
Xbit_r20_c106 bl[106] br[106] wl[20] vdd gnd cell_6t
Xbit_r21_c106 bl[106] br[106] wl[21] vdd gnd cell_6t
Xbit_r22_c106 bl[106] br[106] wl[22] vdd gnd cell_6t
Xbit_r23_c106 bl[106] br[106] wl[23] vdd gnd cell_6t
Xbit_r24_c106 bl[106] br[106] wl[24] vdd gnd cell_6t
Xbit_r25_c106 bl[106] br[106] wl[25] vdd gnd cell_6t
Xbit_r26_c106 bl[106] br[106] wl[26] vdd gnd cell_6t
Xbit_r27_c106 bl[106] br[106] wl[27] vdd gnd cell_6t
Xbit_r28_c106 bl[106] br[106] wl[28] vdd gnd cell_6t
Xbit_r29_c106 bl[106] br[106] wl[29] vdd gnd cell_6t
Xbit_r30_c106 bl[106] br[106] wl[30] vdd gnd cell_6t
Xbit_r31_c106 bl[106] br[106] wl[31] vdd gnd cell_6t
Xbit_r32_c106 bl[106] br[106] wl[32] vdd gnd cell_6t
Xbit_r33_c106 bl[106] br[106] wl[33] vdd gnd cell_6t
Xbit_r34_c106 bl[106] br[106] wl[34] vdd gnd cell_6t
Xbit_r35_c106 bl[106] br[106] wl[35] vdd gnd cell_6t
Xbit_r36_c106 bl[106] br[106] wl[36] vdd gnd cell_6t
Xbit_r37_c106 bl[106] br[106] wl[37] vdd gnd cell_6t
Xbit_r38_c106 bl[106] br[106] wl[38] vdd gnd cell_6t
Xbit_r39_c106 bl[106] br[106] wl[39] vdd gnd cell_6t
Xbit_r40_c106 bl[106] br[106] wl[40] vdd gnd cell_6t
Xbit_r41_c106 bl[106] br[106] wl[41] vdd gnd cell_6t
Xbit_r42_c106 bl[106] br[106] wl[42] vdd gnd cell_6t
Xbit_r43_c106 bl[106] br[106] wl[43] vdd gnd cell_6t
Xbit_r44_c106 bl[106] br[106] wl[44] vdd gnd cell_6t
Xbit_r45_c106 bl[106] br[106] wl[45] vdd gnd cell_6t
Xbit_r46_c106 bl[106] br[106] wl[46] vdd gnd cell_6t
Xbit_r47_c106 bl[106] br[106] wl[47] vdd gnd cell_6t
Xbit_r48_c106 bl[106] br[106] wl[48] vdd gnd cell_6t
Xbit_r49_c106 bl[106] br[106] wl[49] vdd gnd cell_6t
Xbit_r50_c106 bl[106] br[106] wl[50] vdd gnd cell_6t
Xbit_r51_c106 bl[106] br[106] wl[51] vdd gnd cell_6t
Xbit_r52_c106 bl[106] br[106] wl[52] vdd gnd cell_6t
Xbit_r53_c106 bl[106] br[106] wl[53] vdd gnd cell_6t
Xbit_r54_c106 bl[106] br[106] wl[54] vdd gnd cell_6t
Xbit_r55_c106 bl[106] br[106] wl[55] vdd gnd cell_6t
Xbit_r56_c106 bl[106] br[106] wl[56] vdd gnd cell_6t
Xbit_r57_c106 bl[106] br[106] wl[57] vdd gnd cell_6t
Xbit_r58_c106 bl[106] br[106] wl[58] vdd gnd cell_6t
Xbit_r59_c106 bl[106] br[106] wl[59] vdd gnd cell_6t
Xbit_r60_c106 bl[106] br[106] wl[60] vdd gnd cell_6t
Xbit_r61_c106 bl[106] br[106] wl[61] vdd gnd cell_6t
Xbit_r62_c106 bl[106] br[106] wl[62] vdd gnd cell_6t
Xbit_r63_c106 bl[106] br[106] wl[63] vdd gnd cell_6t
Xbit_r0_c107 bl[107] br[107] wl[0] vdd gnd cell_6t
Xbit_r1_c107 bl[107] br[107] wl[1] vdd gnd cell_6t
Xbit_r2_c107 bl[107] br[107] wl[2] vdd gnd cell_6t
Xbit_r3_c107 bl[107] br[107] wl[3] vdd gnd cell_6t
Xbit_r4_c107 bl[107] br[107] wl[4] vdd gnd cell_6t
Xbit_r5_c107 bl[107] br[107] wl[5] vdd gnd cell_6t
Xbit_r6_c107 bl[107] br[107] wl[6] vdd gnd cell_6t
Xbit_r7_c107 bl[107] br[107] wl[7] vdd gnd cell_6t
Xbit_r8_c107 bl[107] br[107] wl[8] vdd gnd cell_6t
Xbit_r9_c107 bl[107] br[107] wl[9] vdd gnd cell_6t
Xbit_r10_c107 bl[107] br[107] wl[10] vdd gnd cell_6t
Xbit_r11_c107 bl[107] br[107] wl[11] vdd gnd cell_6t
Xbit_r12_c107 bl[107] br[107] wl[12] vdd gnd cell_6t
Xbit_r13_c107 bl[107] br[107] wl[13] vdd gnd cell_6t
Xbit_r14_c107 bl[107] br[107] wl[14] vdd gnd cell_6t
Xbit_r15_c107 bl[107] br[107] wl[15] vdd gnd cell_6t
Xbit_r16_c107 bl[107] br[107] wl[16] vdd gnd cell_6t
Xbit_r17_c107 bl[107] br[107] wl[17] vdd gnd cell_6t
Xbit_r18_c107 bl[107] br[107] wl[18] vdd gnd cell_6t
Xbit_r19_c107 bl[107] br[107] wl[19] vdd gnd cell_6t
Xbit_r20_c107 bl[107] br[107] wl[20] vdd gnd cell_6t
Xbit_r21_c107 bl[107] br[107] wl[21] vdd gnd cell_6t
Xbit_r22_c107 bl[107] br[107] wl[22] vdd gnd cell_6t
Xbit_r23_c107 bl[107] br[107] wl[23] vdd gnd cell_6t
Xbit_r24_c107 bl[107] br[107] wl[24] vdd gnd cell_6t
Xbit_r25_c107 bl[107] br[107] wl[25] vdd gnd cell_6t
Xbit_r26_c107 bl[107] br[107] wl[26] vdd gnd cell_6t
Xbit_r27_c107 bl[107] br[107] wl[27] vdd gnd cell_6t
Xbit_r28_c107 bl[107] br[107] wl[28] vdd gnd cell_6t
Xbit_r29_c107 bl[107] br[107] wl[29] vdd gnd cell_6t
Xbit_r30_c107 bl[107] br[107] wl[30] vdd gnd cell_6t
Xbit_r31_c107 bl[107] br[107] wl[31] vdd gnd cell_6t
Xbit_r32_c107 bl[107] br[107] wl[32] vdd gnd cell_6t
Xbit_r33_c107 bl[107] br[107] wl[33] vdd gnd cell_6t
Xbit_r34_c107 bl[107] br[107] wl[34] vdd gnd cell_6t
Xbit_r35_c107 bl[107] br[107] wl[35] vdd gnd cell_6t
Xbit_r36_c107 bl[107] br[107] wl[36] vdd gnd cell_6t
Xbit_r37_c107 bl[107] br[107] wl[37] vdd gnd cell_6t
Xbit_r38_c107 bl[107] br[107] wl[38] vdd gnd cell_6t
Xbit_r39_c107 bl[107] br[107] wl[39] vdd gnd cell_6t
Xbit_r40_c107 bl[107] br[107] wl[40] vdd gnd cell_6t
Xbit_r41_c107 bl[107] br[107] wl[41] vdd gnd cell_6t
Xbit_r42_c107 bl[107] br[107] wl[42] vdd gnd cell_6t
Xbit_r43_c107 bl[107] br[107] wl[43] vdd gnd cell_6t
Xbit_r44_c107 bl[107] br[107] wl[44] vdd gnd cell_6t
Xbit_r45_c107 bl[107] br[107] wl[45] vdd gnd cell_6t
Xbit_r46_c107 bl[107] br[107] wl[46] vdd gnd cell_6t
Xbit_r47_c107 bl[107] br[107] wl[47] vdd gnd cell_6t
Xbit_r48_c107 bl[107] br[107] wl[48] vdd gnd cell_6t
Xbit_r49_c107 bl[107] br[107] wl[49] vdd gnd cell_6t
Xbit_r50_c107 bl[107] br[107] wl[50] vdd gnd cell_6t
Xbit_r51_c107 bl[107] br[107] wl[51] vdd gnd cell_6t
Xbit_r52_c107 bl[107] br[107] wl[52] vdd gnd cell_6t
Xbit_r53_c107 bl[107] br[107] wl[53] vdd gnd cell_6t
Xbit_r54_c107 bl[107] br[107] wl[54] vdd gnd cell_6t
Xbit_r55_c107 bl[107] br[107] wl[55] vdd gnd cell_6t
Xbit_r56_c107 bl[107] br[107] wl[56] vdd gnd cell_6t
Xbit_r57_c107 bl[107] br[107] wl[57] vdd gnd cell_6t
Xbit_r58_c107 bl[107] br[107] wl[58] vdd gnd cell_6t
Xbit_r59_c107 bl[107] br[107] wl[59] vdd gnd cell_6t
Xbit_r60_c107 bl[107] br[107] wl[60] vdd gnd cell_6t
Xbit_r61_c107 bl[107] br[107] wl[61] vdd gnd cell_6t
Xbit_r62_c107 bl[107] br[107] wl[62] vdd gnd cell_6t
Xbit_r63_c107 bl[107] br[107] wl[63] vdd gnd cell_6t
Xbit_r0_c108 bl[108] br[108] wl[0] vdd gnd cell_6t
Xbit_r1_c108 bl[108] br[108] wl[1] vdd gnd cell_6t
Xbit_r2_c108 bl[108] br[108] wl[2] vdd gnd cell_6t
Xbit_r3_c108 bl[108] br[108] wl[3] vdd gnd cell_6t
Xbit_r4_c108 bl[108] br[108] wl[4] vdd gnd cell_6t
Xbit_r5_c108 bl[108] br[108] wl[5] vdd gnd cell_6t
Xbit_r6_c108 bl[108] br[108] wl[6] vdd gnd cell_6t
Xbit_r7_c108 bl[108] br[108] wl[7] vdd gnd cell_6t
Xbit_r8_c108 bl[108] br[108] wl[8] vdd gnd cell_6t
Xbit_r9_c108 bl[108] br[108] wl[9] vdd gnd cell_6t
Xbit_r10_c108 bl[108] br[108] wl[10] vdd gnd cell_6t
Xbit_r11_c108 bl[108] br[108] wl[11] vdd gnd cell_6t
Xbit_r12_c108 bl[108] br[108] wl[12] vdd gnd cell_6t
Xbit_r13_c108 bl[108] br[108] wl[13] vdd gnd cell_6t
Xbit_r14_c108 bl[108] br[108] wl[14] vdd gnd cell_6t
Xbit_r15_c108 bl[108] br[108] wl[15] vdd gnd cell_6t
Xbit_r16_c108 bl[108] br[108] wl[16] vdd gnd cell_6t
Xbit_r17_c108 bl[108] br[108] wl[17] vdd gnd cell_6t
Xbit_r18_c108 bl[108] br[108] wl[18] vdd gnd cell_6t
Xbit_r19_c108 bl[108] br[108] wl[19] vdd gnd cell_6t
Xbit_r20_c108 bl[108] br[108] wl[20] vdd gnd cell_6t
Xbit_r21_c108 bl[108] br[108] wl[21] vdd gnd cell_6t
Xbit_r22_c108 bl[108] br[108] wl[22] vdd gnd cell_6t
Xbit_r23_c108 bl[108] br[108] wl[23] vdd gnd cell_6t
Xbit_r24_c108 bl[108] br[108] wl[24] vdd gnd cell_6t
Xbit_r25_c108 bl[108] br[108] wl[25] vdd gnd cell_6t
Xbit_r26_c108 bl[108] br[108] wl[26] vdd gnd cell_6t
Xbit_r27_c108 bl[108] br[108] wl[27] vdd gnd cell_6t
Xbit_r28_c108 bl[108] br[108] wl[28] vdd gnd cell_6t
Xbit_r29_c108 bl[108] br[108] wl[29] vdd gnd cell_6t
Xbit_r30_c108 bl[108] br[108] wl[30] vdd gnd cell_6t
Xbit_r31_c108 bl[108] br[108] wl[31] vdd gnd cell_6t
Xbit_r32_c108 bl[108] br[108] wl[32] vdd gnd cell_6t
Xbit_r33_c108 bl[108] br[108] wl[33] vdd gnd cell_6t
Xbit_r34_c108 bl[108] br[108] wl[34] vdd gnd cell_6t
Xbit_r35_c108 bl[108] br[108] wl[35] vdd gnd cell_6t
Xbit_r36_c108 bl[108] br[108] wl[36] vdd gnd cell_6t
Xbit_r37_c108 bl[108] br[108] wl[37] vdd gnd cell_6t
Xbit_r38_c108 bl[108] br[108] wl[38] vdd gnd cell_6t
Xbit_r39_c108 bl[108] br[108] wl[39] vdd gnd cell_6t
Xbit_r40_c108 bl[108] br[108] wl[40] vdd gnd cell_6t
Xbit_r41_c108 bl[108] br[108] wl[41] vdd gnd cell_6t
Xbit_r42_c108 bl[108] br[108] wl[42] vdd gnd cell_6t
Xbit_r43_c108 bl[108] br[108] wl[43] vdd gnd cell_6t
Xbit_r44_c108 bl[108] br[108] wl[44] vdd gnd cell_6t
Xbit_r45_c108 bl[108] br[108] wl[45] vdd gnd cell_6t
Xbit_r46_c108 bl[108] br[108] wl[46] vdd gnd cell_6t
Xbit_r47_c108 bl[108] br[108] wl[47] vdd gnd cell_6t
Xbit_r48_c108 bl[108] br[108] wl[48] vdd gnd cell_6t
Xbit_r49_c108 bl[108] br[108] wl[49] vdd gnd cell_6t
Xbit_r50_c108 bl[108] br[108] wl[50] vdd gnd cell_6t
Xbit_r51_c108 bl[108] br[108] wl[51] vdd gnd cell_6t
Xbit_r52_c108 bl[108] br[108] wl[52] vdd gnd cell_6t
Xbit_r53_c108 bl[108] br[108] wl[53] vdd gnd cell_6t
Xbit_r54_c108 bl[108] br[108] wl[54] vdd gnd cell_6t
Xbit_r55_c108 bl[108] br[108] wl[55] vdd gnd cell_6t
Xbit_r56_c108 bl[108] br[108] wl[56] vdd gnd cell_6t
Xbit_r57_c108 bl[108] br[108] wl[57] vdd gnd cell_6t
Xbit_r58_c108 bl[108] br[108] wl[58] vdd gnd cell_6t
Xbit_r59_c108 bl[108] br[108] wl[59] vdd gnd cell_6t
Xbit_r60_c108 bl[108] br[108] wl[60] vdd gnd cell_6t
Xbit_r61_c108 bl[108] br[108] wl[61] vdd gnd cell_6t
Xbit_r62_c108 bl[108] br[108] wl[62] vdd gnd cell_6t
Xbit_r63_c108 bl[108] br[108] wl[63] vdd gnd cell_6t
Xbit_r0_c109 bl[109] br[109] wl[0] vdd gnd cell_6t
Xbit_r1_c109 bl[109] br[109] wl[1] vdd gnd cell_6t
Xbit_r2_c109 bl[109] br[109] wl[2] vdd gnd cell_6t
Xbit_r3_c109 bl[109] br[109] wl[3] vdd gnd cell_6t
Xbit_r4_c109 bl[109] br[109] wl[4] vdd gnd cell_6t
Xbit_r5_c109 bl[109] br[109] wl[5] vdd gnd cell_6t
Xbit_r6_c109 bl[109] br[109] wl[6] vdd gnd cell_6t
Xbit_r7_c109 bl[109] br[109] wl[7] vdd gnd cell_6t
Xbit_r8_c109 bl[109] br[109] wl[8] vdd gnd cell_6t
Xbit_r9_c109 bl[109] br[109] wl[9] vdd gnd cell_6t
Xbit_r10_c109 bl[109] br[109] wl[10] vdd gnd cell_6t
Xbit_r11_c109 bl[109] br[109] wl[11] vdd gnd cell_6t
Xbit_r12_c109 bl[109] br[109] wl[12] vdd gnd cell_6t
Xbit_r13_c109 bl[109] br[109] wl[13] vdd gnd cell_6t
Xbit_r14_c109 bl[109] br[109] wl[14] vdd gnd cell_6t
Xbit_r15_c109 bl[109] br[109] wl[15] vdd gnd cell_6t
Xbit_r16_c109 bl[109] br[109] wl[16] vdd gnd cell_6t
Xbit_r17_c109 bl[109] br[109] wl[17] vdd gnd cell_6t
Xbit_r18_c109 bl[109] br[109] wl[18] vdd gnd cell_6t
Xbit_r19_c109 bl[109] br[109] wl[19] vdd gnd cell_6t
Xbit_r20_c109 bl[109] br[109] wl[20] vdd gnd cell_6t
Xbit_r21_c109 bl[109] br[109] wl[21] vdd gnd cell_6t
Xbit_r22_c109 bl[109] br[109] wl[22] vdd gnd cell_6t
Xbit_r23_c109 bl[109] br[109] wl[23] vdd gnd cell_6t
Xbit_r24_c109 bl[109] br[109] wl[24] vdd gnd cell_6t
Xbit_r25_c109 bl[109] br[109] wl[25] vdd gnd cell_6t
Xbit_r26_c109 bl[109] br[109] wl[26] vdd gnd cell_6t
Xbit_r27_c109 bl[109] br[109] wl[27] vdd gnd cell_6t
Xbit_r28_c109 bl[109] br[109] wl[28] vdd gnd cell_6t
Xbit_r29_c109 bl[109] br[109] wl[29] vdd gnd cell_6t
Xbit_r30_c109 bl[109] br[109] wl[30] vdd gnd cell_6t
Xbit_r31_c109 bl[109] br[109] wl[31] vdd gnd cell_6t
Xbit_r32_c109 bl[109] br[109] wl[32] vdd gnd cell_6t
Xbit_r33_c109 bl[109] br[109] wl[33] vdd gnd cell_6t
Xbit_r34_c109 bl[109] br[109] wl[34] vdd gnd cell_6t
Xbit_r35_c109 bl[109] br[109] wl[35] vdd gnd cell_6t
Xbit_r36_c109 bl[109] br[109] wl[36] vdd gnd cell_6t
Xbit_r37_c109 bl[109] br[109] wl[37] vdd gnd cell_6t
Xbit_r38_c109 bl[109] br[109] wl[38] vdd gnd cell_6t
Xbit_r39_c109 bl[109] br[109] wl[39] vdd gnd cell_6t
Xbit_r40_c109 bl[109] br[109] wl[40] vdd gnd cell_6t
Xbit_r41_c109 bl[109] br[109] wl[41] vdd gnd cell_6t
Xbit_r42_c109 bl[109] br[109] wl[42] vdd gnd cell_6t
Xbit_r43_c109 bl[109] br[109] wl[43] vdd gnd cell_6t
Xbit_r44_c109 bl[109] br[109] wl[44] vdd gnd cell_6t
Xbit_r45_c109 bl[109] br[109] wl[45] vdd gnd cell_6t
Xbit_r46_c109 bl[109] br[109] wl[46] vdd gnd cell_6t
Xbit_r47_c109 bl[109] br[109] wl[47] vdd gnd cell_6t
Xbit_r48_c109 bl[109] br[109] wl[48] vdd gnd cell_6t
Xbit_r49_c109 bl[109] br[109] wl[49] vdd gnd cell_6t
Xbit_r50_c109 bl[109] br[109] wl[50] vdd gnd cell_6t
Xbit_r51_c109 bl[109] br[109] wl[51] vdd gnd cell_6t
Xbit_r52_c109 bl[109] br[109] wl[52] vdd gnd cell_6t
Xbit_r53_c109 bl[109] br[109] wl[53] vdd gnd cell_6t
Xbit_r54_c109 bl[109] br[109] wl[54] vdd gnd cell_6t
Xbit_r55_c109 bl[109] br[109] wl[55] vdd gnd cell_6t
Xbit_r56_c109 bl[109] br[109] wl[56] vdd gnd cell_6t
Xbit_r57_c109 bl[109] br[109] wl[57] vdd gnd cell_6t
Xbit_r58_c109 bl[109] br[109] wl[58] vdd gnd cell_6t
Xbit_r59_c109 bl[109] br[109] wl[59] vdd gnd cell_6t
Xbit_r60_c109 bl[109] br[109] wl[60] vdd gnd cell_6t
Xbit_r61_c109 bl[109] br[109] wl[61] vdd gnd cell_6t
Xbit_r62_c109 bl[109] br[109] wl[62] vdd gnd cell_6t
Xbit_r63_c109 bl[109] br[109] wl[63] vdd gnd cell_6t
Xbit_r0_c110 bl[110] br[110] wl[0] vdd gnd cell_6t
Xbit_r1_c110 bl[110] br[110] wl[1] vdd gnd cell_6t
Xbit_r2_c110 bl[110] br[110] wl[2] vdd gnd cell_6t
Xbit_r3_c110 bl[110] br[110] wl[3] vdd gnd cell_6t
Xbit_r4_c110 bl[110] br[110] wl[4] vdd gnd cell_6t
Xbit_r5_c110 bl[110] br[110] wl[5] vdd gnd cell_6t
Xbit_r6_c110 bl[110] br[110] wl[6] vdd gnd cell_6t
Xbit_r7_c110 bl[110] br[110] wl[7] vdd gnd cell_6t
Xbit_r8_c110 bl[110] br[110] wl[8] vdd gnd cell_6t
Xbit_r9_c110 bl[110] br[110] wl[9] vdd gnd cell_6t
Xbit_r10_c110 bl[110] br[110] wl[10] vdd gnd cell_6t
Xbit_r11_c110 bl[110] br[110] wl[11] vdd gnd cell_6t
Xbit_r12_c110 bl[110] br[110] wl[12] vdd gnd cell_6t
Xbit_r13_c110 bl[110] br[110] wl[13] vdd gnd cell_6t
Xbit_r14_c110 bl[110] br[110] wl[14] vdd gnd cell_6t
Xbit_r15_c110 bl[110] br[110] wl[15] vdd gnd cell_6t
Xbit_r16_c110 bl[110] br[110] wl[16] vdd gnd cell_6t
Xbit_r17_c110 bl[110] br[110] wl[17] vdd gnd cell_6t
Xbit_r18_c110 bl[110] br[110] wl[18] vdd gnd cell_6t
Xbit_r19_c110 bl[110] br[110] wl[19] vdd gnd cell_6t
Xbit_r20_c110 bl[110] br[110] wl[20] vdd gnd cell_6t
Xbit_r21_c110 bl[110] br[110] wl[21] vdd gnd cell_6t
Xbit_r22_c110 bl[110] br[110] wl[22] vdd gnd cell_6t
Xbit_r23_c110 bl[110] br[110] wl[23] vdd gnd cell_6t
Xbit_r24_c110 bl[110] br[110] wl[24] vdd gnd cell_6t
Xbit_r25_c110 bl[110] br[110] wl[25] vdd gnd cell_6t
Xbit_r26_c110 bl[110] br[110] wl[26] vdd gnd cell_6t
Xbit_r27_c110 bl[110] br[110] wl[27] vdd gnd cell_6t
Xbit_r28_c110 bl[110] br[110] wl[28] vdd gnd cell_6t
Xbit_r29_c110 bl[110] br[110] wl[29] vdd gnd cell_6t
Xbit_r30_c110 bl[110] br[110] wl[30] vdd gnd cell_6t
Xbit_r31_c110 bl[110] br[110] wl[31] vdd gnd cell_6t
Xbit_r32_c110 bl[110] br[110] wl[32] vdd gnd cell_6t
Xbit_r33_c110 bl[110] br[110] wl[33] vdd gnd cell_6t
Xbit_r34_c110 bl[110] br[110] wl[34] vdd gnd cell_6t
Xbit_r35_c110 bl[110] br[110] wl[35] vdd gnd cell_6t
Xbit_r36_c110 bl[110] br[110] wl[36] vdd gnd cell_6t
Xbit_r37_c110 bl[110] br[110] wl[37] vdd gnd cell_6t
Xbit_r38_c110 bl[110] br[110] wl[38] vdd gnd cell_6t
Xbit_r39_c110 bl[110] br[110] wl[39] vdd gnd cell_6t
Xbit_r40_c110 bl[110] br[110] wl[40] vdd gnd cell_6t
Xbit_r41_c110 bl[110] br[110] wl[41] vdd gnd cell_6t
Xbit_r42_c110 bl[110] br[110] wl[42] vdd gnd cell_6t
Xbit_r43_c110 bl[110] br[110] wl[43] vdd gnd cell_6t
Xbit_r44_c110 bl[110] br[110] wl[44] vdd gnd cell_6t
Xbit_r45_c110 bl[110] br[110] wl[45] vdd gnd cell_6t
Xbit_r46_c110 bl[110] br[110] wl[46] vdd gnd cell_6t
Xbit_r47_c110 bl[110] br[110] wl[47] vdd gnd cell_6t
Xbit_r48_c110 bl[110] br[110] wl[48] vdd gnd cell_6t
Xbit_r49_c110 bl[110] br[110] wl[49] vdd gnd cell_6t
Xbit_r50_c110 bl[110] br[110] wl[50] vdd gnd cell_6t
Xbit_r51_c110 bl[110] br[110] wl[51] vdd gnd cell_6t
Xbit_r52_c110 bl[110] br[110] wl[52] vdd gnd cell_6t
Xbit_r53_c110 bl[110] br[110] wl[53] vdd gnd cell_6t
Xbit_r54_c110 bl[110] br[110] wl[54] vdd gnd cell_6t
Xbit_r55_c110 bl[110] br[110] wl[55] vdd gnd cell_6t
Xbit_r56_c110 bl[110] br[110] wl[56] vdd gnd cell_6t
Xbit_r57_c110 bl[110] br[110] wl[57] vdd gnd cell_6t
Xbit_r58_c110 bl[110] br[110] wl[58] vdd gnd cell_6t
Xbit_r59_c110 bl[110] br[110] wl[59] vdd gnd cell_6t
Xbit_r60_c110 bl[110] br[110] wl[60] vdd gnd cell_6t
Xbit_r61_c110 bl[110] br[110] wl[61] vdd gnd cell_6t
Xbit_r62_c110 bl[110] br[110] wl[62] vdd gnd cell_6t
Xbit_r63_c110 bl[110] br[110] wl[63] vdd gnd cell_6t
Xbit_r0_c111 bl[111] br[111] wl[0] vdd gnd cell_6t
Xbit_r1_c111 bl[111] br[111] wl[1] vdd gnd cell_6t
Xbit_r2_c111 bl[111] br[111] wl[2] vdd gnd cell_6t
Xbit_r3_c111 bl[111] br[111] wl[3] vdd gnd cell_6t
Xbit_r4_c111 bl[111] br[111] wl[4] vdd gnd cell_6t
Xbit_r5_c111 bl[111] br[111] wl[5] vdd gnd cell_6t
Xbit_r6_c111 bl[111] br[111] wl[6] vdd gnd cell_6t
Xbit_r7_c111 bl[111] br[111] wl[7] vdd gnd cell_6t
Xbit_r8_c111 bl[111] br[111] wl[8] vdd gnd cell_6t
Xbit_r9_c111 bl[111] br[111] wl[9] vdd gnd cell_6t
Xbit_r10_c111 bl[111] br[111] wl[10] vdd gnd cell_6t
Xbit_r11_c111 bl[111] br[111] wl[11] vdd gnd cell_6t
Xbit_r12_c111 bl[111] br[111] wl[12] vdd gnd cell_6t
Xbit_r13_c111 bl[111] br[111] wl[13] vdd gnd cell_6t
Xbit_r14_c111 bl[111] br[111] wl[14] vdd gnd cell_6t
Xbit_r15_c111 bl[111] br[111] wl[15] vdd gnd cell_6t
Xbit_r16_c111 bl[111] br[111] wl[16] vdd gnd cell_6t
Xbit_r17_c111 bl[111] br[111] wl[17] vdd gnd cell_6t
Xbit_r18_c111 bl[111] br[111] wl[18] vdd gnd cell_6t
Xbit_r19_c111 bl[111] br[111] wl[19] vdd gnd cell_6t
Xbit_r20_c111 bl[111] br[111] wl[20] vdd gnd cell_6t
Xbit_r21_c111 bl[111] br[111] wl[21] vdd gnd cell_6t
Xbit_r22_c111 bl[111] br[111] wl[22] vdd gnd cell_6t
Xbit_r23_c111 bl[111] br[111] wl[23] vdd gnd cell_6t
Xbit_r24_c111 bl[111] br[111] wl[24] vdd gnd cell_6t
Xbit_r25_c111 bl[111] br[111] wl[25] vdd gnd cell_6t
Xbit_r26_c111 bl[111] br[111] wl[26] vdd gnd cell_6t
Xbit_r27_c111 bl[111] br[111] wl[27] vdd gnd cell_6t
Xbit_r28_c111 bl[111] br[111] wl[28] vdd gnd cell_6t
Xbit_r29_c111 bl[111] br[111] wl[29] vdd gnd cell_6t
Xbit_r30_c111 bl[111] br[111] wl[30] vdd gnd cell_6t
Xbit_r31_c111 bl[111] br[111] wl[31] vdd gnd cell_6t
Xbit_r32_c111 bl[111] br[111] wl[32] vdd gnd cell_6t
Xbit_r33_c111 bl[111] br[111] wl[33] vdd gnd cell_6t
Xbit_r34_c111 bl[111] br[111] wl[34] vdd gnd cell_6t
Xbit_r35_c111 bl[111] br[111] wl[35] vdd gnd cell_6t
Xbit_r36_c111 bl[111] br[111] wl[36] vdd gnd cell_6t
Xbit_r37_c111 bl[111] br[111] wl[37] vdd gnd cell_6t
Xbit_r38_c111 bl[111] br[111] wl[38] vdd gnd cell_6t
Xbit_r39_c111 bl[111] br[111] wl[39] vdd gnd cell_6t
Xbit_r40_c111 bl[111] br[111] wl[40] vdd gnd cell_6t
Xbit_r41_c111 bl[111] br[111] wl[41] vdd gnd cell_6t
Xbit_r42_c111 bl[111] br[111] wl[42] vdd gnd cell_6t
Xbit_r43_c111 bl[111] br[111] wl[43] vdd gnd cell_6t
Xbit_r44_c111 bl[111] br[111] wl[44] vdd gnd cell_6t
Xbit_r45_c111 bl[111] br[111] wl[45] vdd gnd cell_6t
Xbit_r46_c111 bl[111] br[111] wl[46] vdd gnd cell_6t
Xbit_r47_c111 bl[111] br[111] wl[47] vdd gnd cell_6t
Xbit_r48_c111 bl[111] br[111] wl[48] vdd gnd cell_6t
Xbit_r49_c111 bl[111] br[111] wl[49] vdd gnd cell_6t
Xbit_r50_c111 bl[111] br[111] wl[50] vdd gnd cell_6t
Xbit_r51_c111 bl[111] br[111] wl[51] vdd gnd cell_6t
Xbit_r52_c111 bl[111] br[111] wl[52] vdd gnd cell_6t
Xbit_r53_c111 bl[111] br[111] wl[53] vdd gnd cell_6t
Xbit_r54_c111 bl[111] br[111] wl[54] vdd gnd cell_6t
Xbit_r55_c111 bl[111] br[111] wl[55] vdd gnd cell_6t
Xbit_r56_c111 bl[111] br[111] wl[56] vdd gnd cell_6t
Xbit_r57_c111 bl[111] br[111] wl[57] vdd gnd cell_6t
Xbit_r58_c111 bl[111] br[111] wl[58] vdd gnd cell_6t
Xbit_r59_c111 bl[111] br[111] wl[59] vdd gnd cell_6t
Xbit_r60_c111 bl[111] br[111] wl[60] vdd gnd cell_6t
Xbit_r61_c111 bl[111] br[111] wl[61] vdd gnd cell_6t
Xbit_r62_c111 bl[111] br[111] wl[62] vdd gnd cell_6t
Xbit_r63_c111 bl[111] br[111] wl[63] vdd gnd cell_6t
Xbit_r0_c112 bl[112] br[112] wl[0] vdd gnd cell_6t
Xbit_r1_c112 bl[112] br[112] wl[1] vdd gnd cell_6t
Xbit_r2_c112 bl[112] br[112] wl[2] vdd gnd cell_6t
Xbit_r3_c112 bl[112] br[112] wl[3] vdd gnd cell_6t
Xbit_r4_c112 bl[112] br[112] wl[4] vdd gnd cell_6t
Xbit_r5_c112 bl[112] br[112] wl[5] vdd gnd cell_6t
Xbit_r6_c112 bl[112] br[112] wl[6] vdd gnd cell_6t
Xbit_r7_c112 bl[112] br[112] wl[7] vdd gnd cell_6t
Xbit_r8_c112 bl[112] br[112] wl[8] vdd gnd cell_6t
Xbit_r9_c112 bl[112] br[112] wl[9] vdd gnd cell_6t
Xbit_r10_c112 bl[112] br[112] wl[10] vdd gnd cell_6t
Xbit_r11_c112 bl[112] br[112] wl[11] vdd gnd cell_6t
Xbit_r12_c112 bl[112] br[112] wl[12] vdd gnd cell_6t
Xbit_r13_c112 bl[112] br[112] wl[13] vdd gnd cell_6t
Xbit_r14_c112 bl[112] br[112] wl[14] vdd gnd cell_6t
Xbit_r15_c112 bl[112] br[112] wl[15] vdd gnd cell_6t
Xbit_r16_c112 bl[112] br[112] wl[16] vdd gnd cell_6t
Xbit_r17_c112 bl[112] br[112] wl[17] vdd gnd cell_6t
Xbit_r18_c112 bl[112] br[112] wl[18] vdd gnd cell_6t
Xbit_r19_c112 bl[112] br[112] wl[19] vdd gnd cell_6t
Xbit_r20_c112 bl[112] br[112] wl[20] vdd gnd cell_6t
Xbit_r21_c112 bl[112] br[112] wl[21] vdd gnd cell_6t
Xbit_r22_c112 bl[112] br[112] wl[22] vdd gnd cell_6t
Xbit_r23_c112 bl[112] br[112] wl[23] vdd gnd cell_6t
Xbit_r24_c112 bl[112] br[112] wl[24] vdd gnd cell_6t
Xbit_r25_c112 bl[112] br[112] wl[25] vdd gnd cell_6t
Xbit_r26_c112 bl[112] br[112] wl[26] vdd gnd cell_6t
Xbit_r27_c112 bl[112] br[112] wl[27] vdd gnd cell_6t
Xbit_r28_c112 bl[112] br[112] wl[28] vdd gnd cell_6t
Xbit_r29_c112 bl[112] br[112] wl[29] vdd gnd cell_6t
Xbit_r30_c112 bl[112] br[112] wl[30] vdd gnd cell_6t
Xbit_r31_c112 bl[112] br[112] wl[31] vdd gnd cell_6t
Xbit_r32_c112 bl[112] br[112] wl[32] vdd gnd cell_6t
Xbit_r33_c112 bl[112] br[112] wl[33] vdd gnd cell_6t
Xbit_r34_c112 bl[112] br[112] wl[34] vdd gnd cell_6t
Xbit_r35_c112 bl[112] br[112] wl[35] vdd gnd cell_6t
Xbit_r36_c112 bl[112] br[112] wl[36] vdd gnd cell_6t
Xbit_r37_c112 bl[112] br[112] wl[37] vdd gnd cell_6t
Xbit_r38_c112 bl[112] br[112] wl[38] vdd gnd cell_6t
Xbit_r39_c112 bl[112] br[112] wl[39] vdd gnd cell_6t
Xbit_r40_c112 bl[112] br[112] wl[40] vdd gnd cell_6t
Xbit_r41_c112 bl[112] br[112] wl[41] vdd gnd cell_6t
Xbit_r42_c112 bl[112] br[112] wl[42] vdd gnd cell_6t
Xbit_r43_c112 bl[112] br[112] wl[43] vdd gnd cell_6t
Xbit_r44_c112 bl[112] br[112] wl[44] vdd gnd cell_6t
Xbit_r45_c112 bl[112] br[112] wl[45] vdd gnd cell_6t
Xbit_r46_c112 bl[112] br[112] wl[46] vdd gnd cell_6t
Xbit_r47_c112 bl[112] br[112] wl[47] vdd gnd cell_6t
Xbit_r48_c112 bl[112] br[112] wl[48] vdd gnd cell_6t
Xbit_r49_c112 bl[112] br[112] wl[49] vdd gnd cell_6t
Xbit_r50_c112 bl[112] br[112] wl[50] vdd gnd cell_6t
Xbit_r51_c112 bl[112] br[112] wl[51] vdd gnd cell_6t
Xbit_r52_c112 bl[112] br[112] wl[52] vdd gnd cell_6t
Xbit_r53_c112 bl[112] br[112] wl[53] vdd gnd cell_6t
Xbit_r54_c112 bl[112] br[112] wl[54] vdd gnd cell_6t
Xbit_r55_c112 bl[112] br[112] wl[55] vdd gnd cell_6t
Xbit_r56_c112 bl[112] br[112] wl[56] vdd gnd cell_6t
Xbit_r57_c112 bl[112] br[112] wl[57] vdd gnd cell_6t
Xbit_r58_c112 bl[112] br[112] wl[58] vdd gnd cell_6t
Xbit_r59_c112 bl[112] br[112] wl[59] vdd gnd cell_6t
Xbit_r60_c112 bl[112] br[112] wl[60] vdd gnd cell_6t
Xbit_r61_c112 bl[112] br[112] wl[61] vdd gnd cell_6t
Xbit_r62_c112 bl[112] br[112] wl[62] vdd gnd cell_6t
Xbit_r63_c112 bl[112] br[112] wl[63] vdd gnd cell_6t
Xbit_r0_c113 bl[113] br[113] wl[0] vdd gnd cell_6t
Xbit_r1_c113 bl[113] br[113] wl[1] vdd gnd cell_6t
Xbit_r2_c113 bl[113] br[113] wl[2] vdd gnd cell_6t
Xbit_r3_c113 bl[113] br[113] wl[3] vdd gnd cell_6t
Xbit_r4_c113 bl[113] br[113] wl[4] vdd gnd cell_6t
Xbit_r5_c113 bl[113] br[113] wl[5] vdd gnd cell_6t
Xbit_r6_c113 bl[113] br[113] wl[6] vdd gnd cell_6t
Xbit_r7_c113 bl[113] br[113] wl[7] vdd gnd cell_6t
Xbit_r8_c113 bl[113] br[113] wl[8] vdd gnd cell_6t
Xbit_r9_c113 bl[113] br[113] wl[9] vdd gnd cell_6t
Xbit_r10_c113 bl[113] br[113] wl[10] vdd gnd cell_6t
Xbit_r11_c113 bl[113] br[113] wl[11] vdd gnd cell_6t
Xbit_r12_c113 bl[113] br[113] wl[12] vdd gnd cell_6t
Xbit_r13_c113 bl[113] br[113] wl[13] vdd gnd cell_6t
Xbit_r14_c113 bl[113] br[113] wl[14] vdd gnd cell_6t
Xbit_r15_c113 bl[113] br[113] wl[15] vdd gnd cell_6t
Xbit_r16_c113 bl[113] br[113] wl[16] vdd gnd cell_6t
Xbit_r17_c113 bl[113] br[113] wl[17] vdd gnd cell_6t
Xbit_r18_c113 bl[113] br[113] wl[18] vdd gnd cell_6t
Xbit_r19_c113 bl[113] br[113] wl[19] vdd gnd cell_6t
Xbit_r20_c113 bl[113] br[113] wl[20] vdd gnd cell_6t
Xbit_r21_c113 bl[113] br[113] wl[21] vdd gnd cell_6t
Xbit_r22_c113 bl[113] br[113] wl[22] vdd gnd cell_6t
Xbit_r23_c113 bl[113] br[113] wl[23] vdd gnd cell_6t
Xbit_r24_c113 bl[113] br[113] wl[24] vdd gnd cell_6t
Xbit_r25_c113 bl[113] br[113] wl[25] vdd gnd cell_6t
Xbit_r26_c113 bl[113] br[113] wl[26] vdd gnd cell_6t
Xbit_r27_c113 bl[113] br[113] wl[27] vdd gnd cell_6t
Xbit_r28_c113 bl[113] br[113] wl[28] vdd gnd cell_6t
Xbit_r29_c113 bl[113] br[113] wl[29] vdd gnd cell_6t
Xbit_r30_c113 bl[113] br[113] wl[30] vdd gnd cell_6t
Xbit_r31_c113 bl[113] br[113] wl[31] vdd gnd cell_6t
Xbit_r32_c113 bl[113] br[113] wl[32] vdd gnd cell_6t
Xbit_r33_c113 bl[113] br[113] wl[33] vdd gnd cell_6t
Xbit_r34_c113 bl[113] br[113] wl[34] vdd gnd cell_6t
Xbit_r35_c113 bl[113] br[113] wl[35] vdd gnd cell_6t
Xbit_r36_c113 bl[113] br[113] wl[36] vdd gnd cell_6t
Xbit_r37_c113 bl[113] br[113] wl[37] vdd gnd cell_6t
Xbit_r38_c113 bl[113] br[113] wl[38] vdd gnd cell_6t
Xbit_r39_c113 bl[113] br[113] wl[39] vdd gnd cell_6t
Xbit_r40_c113 bl[113] br[113] wl[40] vdd gnd cell_6t
Xbit_r41_c113 bl[113] br[113] wl[41] vdd gnd cell_6t
Xbit_r42_c113 bl[113] br[113] wl[42] vdd gnd cell_6t
Xbit_r43_c113 bl[113] br[113] wl[43] vdd gnd cell_6t
Xbit_r44_c113 bl[113] br[113] wl[44] vdd gnd cell_6t
Xbit_r45_c113 bl[113] br[113] wl[45] vdd gnd cell_6t
Xbit_r46_c113 bl[113] br[113] wl[46] vdd gnd cell_6t
Xbit_r47_c113 bl[113] br[113] wl[47] vdd gnd cell_6t
Xbit_r48_c113 bl[113] br[113] wl[48] vdd gnd cell_6t
Xbit_r49_c113 bl[113] br[113] wl[49] vdd gnd cell_6t
Xbit_r50_c113 bl[113] br[113] wl[50] vdd gnd cell_6t
Xbit_r51_c113 bl[113] br[113] wl[51] vdd gnd cell_6t
Xbit_r52_c113 bl[113] br[113] wl[52] vdd gnd cell_6t
Xbit_r53_c113 bl[113] br[113] wl[53] vdd gnd cell_6t
Xbit_r54_c113 bl[113] br[113] wl[54] vdd gnd cell_6t
Xbit_r55_c113 bl[113] br[113] wl[55] vdd gnd cell_6t
Xbit_r56_c113 bl[113] br[113] wl[56] vdd gnd cell_6t
Xbit_r57_c113 bl[113] br[113] wl[57] vdd gnd cell_6t
Xbit_r58_c113 bl[113] br[113] wl[58] vdd gnd cell_6t
Xbit_r59_c113 bl[113] br[113] wl[59] vdd gnd cell_6t
Xbit_r60_c113 bl[113] br[113] wl[60] vdd gnd cell_6t
Xbit_r61_c113 bl[113] br[113] wl[61] vdd gnd cell_6t
Xbit_r62_c113 bl[113] br[113] wl[62] vdd gnd cell_6t
Xbit_r63_c113 bl[113] br[113] wl[63] vdd gnd cell_6t
Xbit_r0_c114 bl[114] br[114] wl[0] vdd gnd cell_6t
Xbit_r1_c114 bl[114] br[114] wl[1] vdd gnd cell_6t
Xbit_r2_c114 bl[114] br[114] wl[2] vdd gnd cell_6t
Xbit_r3_c114 bl[114] br[114] wl[3] vdd gnd cell_6t
Xbit_r4_c114 bl[114] br[114] wl[4] vdd gnd cell_6t
Xbit_r5_c114 bl[114] br[114] wl[5] vdd gnd cell_6t
Xbit_r6_c114 bl[114] br[114] wl[6] vdd gnd cell_6t
Xbit_r7_c114 bl[114] br[114] wl[7] vdd gnd cell_6t
Xbit_r8_c114 bl[114] br[114] wl[8] vdd gnd cell_6t
Xbit_r9_c114 bl[114] br[114] wl[9] vdd gnd cell_6t
Xbit_r10_c114 bl[114] br[114] wl[10] vdd gnd cell_6t
Xbit_r11_c114 bl[114] br[114] wl[11] vdd gnd cell_6t
Xbit_r12_c114 bl[114] br[114] wl[12] vdd gnd cell_6t
Xbit_r13_c114 bl[114] br[114] wl[13] vdd gnd cell_6t
Xbit_r14_c114 bl[114] br[114] wl[14] vdd gnd cell_6t
Xbit_r15_c114 bl[114] br[114] wl[15] vdd gnd cell_6t
Xbit_r16_c114 bl[114] br[114] wl[16] vdd gnd cell_6t
Xbit_r17_c114 bl[114] br[114] wl[17] vdd gnd cell_6t
Xbit_r18_c114 bl[114] br[114] wl[18] vdd gnd cell_6t
Xbit_r19_c114 bl[114] br[114] wl[19] vdd gnd cell_6t
Xbit_r20_c114 bl[114] br[114] wl[20] vdd gnd cell_6t
Xbit_r21_c114 bl[114] br[114] wl[21] vdd gnd cell_6t
Xbit_r22_c114 bl[114] br[114] wl[22] vdd gnd cell_6t
Xbit_r23_c114 bl[114] br[114] wl[23] vdd gnd cell_6t
Xbit_r24_c114 bl[114] br[114] wl[24] vdd gnd cell_6t
Xbit_r25_c114 bl[114] br[114] wl[25] vdd gnd cell_6t
Xbit_r26_c114 bl[114] br[114] wl[26] vdd gnd cell_6t
Xbit_r27_c114 bl[114] br[114] wl[27] vdd gnd cell_6t
Xbit_r28_c114 bl[114] br[114] wl[28] vdd gnd cell_6t
Xbit_r29_c114 bl[114] br[114] wl[29] vdd gnd cell_6t
Xbit_r30_c114 bl[114] br[114] wl[30] vdd gnd cell_6t
Xbit_r31_c114 bl[114] br[114] wl[31] vdd gnd cell_6t
Xbit_r32_c114 bl[114] br[114] wl[32] vdd gnd cell_6t
Xbit_r33_c114 bl[114] br[114] wl[33] vdd gnd cell_6t
Xbit_r34_c114 bl[114] br[114] wl[34] vdd gnd cell_6t
Xbit_r35_c114 bl[114] br[114] wl[35] vdd gnd cell_6t
Xbit_r36_c114 bl[114] br[114] wl[36] vdd gnd cell_6t
Xbit_r37_c114 bl[114] br[114] wl[37] vdd gnd cell_6t
Xbit_r38_c114 bl[114] br[114] wl[38] vdd gnd cell_6t
Xbit_r39_c114 bl[114] br[114] wl[39] vdd gnd cell_6t
Xbit_r40_c114 bl[114] br[114] wl[40] vdd gnd cell_6t
Xbit_r41_c114 bl[114] br[114] wl[41] vdd gnd cell_6t
Xbit_r42_c114 bl[114] br[114] wl[42] vdd gnd cell_6t
Xbit_r43_c114 bl[114] br[114] wl[43] vdd gnd cell_6t
Xbit_r44_c114 bl[114] br[114] wl[44] vdd gnd cell_6t
Xbit_r45_c114 bl[114] br[114] wl[45] vdd gnd cell_6t
Xbit_r46_c114 bl[114] br[114] wl[46] vdd gnd cell_6t
Xbit_r47_c114 bl[114] br[114] wl[47] vdd gnd cell_6t
Xbit_r48_c114 bl[114] br[114] wl[48] vdd gnd cell_6t
Xbit_r49_c114 bl[114] br[114] wl[49] vdd gnd cell_6t
Xbit_r50_c114 bl[114] br[114] wl[50] vdd gnd cell_6t
Xbit_r51_c114 bl[114] br[114] wl[51] vdd gnd cell_6t
Xbit_r52_c114 bl[114] br[114] wl[52] vdd gnd cell_6t
Xbit_r53_c114 bl[114] br[114] wl[53] vdd gnd cell_6t
Xbit_r54_c114 bl[114] br[114] wl[54] vdd gnd cell_6t
Xbit_r55_c114 bl[114] br[114] wl[55] vdd gnd cell_6t
Xbit_r56_c114 bl[114] br[114] wl[56] vdd gnd cell_6t
Xbit_r57_c114 bl[114] br[114] wl[57] vdd gnd cell_6t
Xbit_r58_c114 bl[114] br[114] wl[58] vdd gnd cell_6t
Xbit_r59_c114 bl[114] br[114] wl[59] vdd gnd cell_6t
Xbit_r60_c114 bl[114] br[114] wl[60] vdd gnd cell_6t
Xbit_r61_c114 bl[114] br[114] wl[61] vdd gnd cell_6t
Xbit_r62_c114 bl[114] br[114] wl[62] vdd gnd cell_6t
Xbit_r63_c114 bl[114] br[114] wl[63] vdd gnd cell_6t
Xbit_r0_c115 bl[115] br[115] wl[0] vdd gnd cell_6t
Xbit_r1_c115 bl[115] br[115] wl[1] vdd gnd cell_6t
Xbit_r2_c115 bl[115] br[115] wl[2] vdd gnd cell_6t
Xbit_r3_c115 bl[115] br[115] wl[3] vdd gnd cell_6t
Xbit_r4_c115 bl[115] br[115] wl[4] vdd gnd cell_6t
Xbit_r5_c115 bl[115] br[115] wl[5] vdd gnd cell_6t
Xbit_r6_c115 bl[115] br[115] wl[6] vdd gnd cell_6t
Xbit_r7_c115 bl[115] br[115] wl[7] vdd gnd cell_6t
Xbit_r8_c115 bl[115] br[115] wl[8] vdd gnd cell_6t
Xbit_r9_c115 bl[115] br[115] wl[9] vdd gnd cell_6t
Xbit_r10_c115 bl[115] br[115] wl[10] vdd gnd cell_6t
Xbit_r11_c115 bl[115] br[115] wl[11] vdd gnd cell_6t
Xbit_r12_c115 bl[115] br[115] wl[12] vdd gnd cell_6t
Xbit_r13_c115 bl[115] br[115] wl[13] vdd gnd cell_6t
Xbit_r14_c115 bl[115] br[115] wl[14] vdd gnd cell_6t
Xbit_r15_c115 bl[115] br[115] wl[15] vdd gnd cell_6t
Xbit_r16_c115 bl[115] br[115] wl[16] vdd gnd cell_6t
Xbit_r17_c115 bl[115] br[115] wl[17] vdd gnd cell_6t
Xbit_r18_c115 bl[115] br[115] wl[18] vdd gnd cell_6t
Xbit_r19_c115 bl[115] br[115] wl[19] vdd gnd cell_6t
Xbit_r20_c115 bl[115] br[115] wl[20] vdd gnd cell_6t
Xbit_r21_c115 bl[115] br[115] wl[21] vdd gnd cell_6t
Xbit_r22_c115 bl[115] br[115] wl[22] vdd gnd cell_6t
Xbit_r23_c115 bl[115] br[115] wl[23] vdd gnd cell_6t
Xbit_r24_c115 bl[115] br[115] wl[24] vdd gnd cell_6t
Xbit_r25_c115 bl[115] br[115] wl[25] vdd gnd cell_6t
Xbit_r26_c115 bl[115] br[115] wl[26] vdd gnd cell_6t
Xbit_r27_c115 bl[115] br[115] wl[27] vdd gnd cell_6t
Xbit_r28_c115 bl[115] br[115] wl[28] vdd gnd cell_6t
Xbit_r29_c115 bl[115] br[115] wl[29] vdd gnd cell_6t
Xbit_r30_c115 bl[115] br[115] wl[30] vdd gnd cell_6t
Xbit_r31_c115 bl[115] br[115] wl[31] vdd gnd cell_6t
Xbit_r32_c115 bl[115] br[115] wl[32] vdd gnd cell_6t
Xbit_r33_c115 bl[115] br[115] wl[33] vdd gnd cell_6t
Xbit_r34_c115 bl[115] br[115] wl[34] vdd gnd cell_6t
Xbit_r35_c115 bl[115] br[115] wl[35] vdd gnd cell_6t
Xbit_r36_c115 bl[115] br[115] wl[36] vdd gnd cell_6t
Xbit_r37_c115 bl[115] br[115] wl[37] vdd gnd cell_6t
Xbit_r38_c115 bl[115] br[115] wl[38] vdd gnd cell_6t
Xbit_r39_c115 bl[115] br[115] wl[39] vdd gnd cell_6t
Xbit_r40_c115 bl[115] br[115] wl[40] vdd gnd cell_6t
Xbit_r41_c115 bl[115] br[115] wl[41] vdd gnd cell_6t
Xbit_r42_c115 bl[115] br[115] wl[42] vdd gnd cell_6t
Xbit_r43_c115 bl[115] br[115] wl[43] vdd gnd cell_6t
Xbit_r44_c115 bl[115] br[115] wl[44] vdd gnd cell_6t
Xbit_r45_c115 bl[115] br[115] wl[45] vdd gnd cell_6t
Xbit_r46_c115 bl[115] br[115] wl[46] vdd gnd cell_6t
Xbit_r47_c115 bl[115] br[115] wl[47] vdd gnd cell_6t
Xbit_r48_c115 bl[115] br[115] wl[48] vdd gnd cell_6t
Xbit_r49_c115 bl[115] br[115] wl[49] vdd gnd cell_6t
Xbit_r50_c115 bl[115] br[115] wl[50] vdd gnd cell_6t
Xbit_r51_c115 bl[115] br[115] wl[51] vdd gnd cell_6t
Xbit_r52_c115 bl[115] br[115] wl[52] vdd gnd cell_6t
Xbit_r53_c115 bl[115] br[115] wl[53] vdd gnd cell_6t
Xbit_r54_c115 bl[115] br[115] wl[54] vdd gnd cell_6t
Xbit_r55_c115 bl[115] br[115] wl[55] vdd gnd cell_6t
Xbit_r56_c115 bl[115] br[115] wl[56] vdd gnd cell_6t
Xbit_r57_c115 bl[115] br[115] wl[57] vdd gnd cell_6t
Xbit_r58_c115 bl[115] br[115] wl[58] vdd gnd cell_6t
Xbit_r59_c115 bl[115] br[115] wl[59] vdd gnd cell_6t
Xbit_r60_c115 bl[115] br[115] wl[60] vdd gnd cell_6t
Xbit_r61_c115 bl[115] br[115] wl[61] vdd gnd cell_6t
Xbit_r62_c115 bl[115] br[115] wl[62] vdd gnd cell_6t
Xbit_r63_c115 bl[115] br[115] wl[63] vdd gnd cell_6t
Xbit_r0_c116 bl[116] br[116] wl[0] vdd gnd cell_6t
Xbit_r1_c116 bl[116] br[116] wl[1] vdd gnd cell_6t
Xbit_r2_c116 bl[116] br[116] wl[2] vdd gnd cell_6t
Xbit_r3_c116 bl[116] br[116] wl[3] vdd gnd cell_6t
Xbit_r4_c116 bl[116] br[116] wl[4] vdd gnd cell_6t
Xbit_r5_c116 bl[116] br[116] wl[5] vdd gnd cell_6t
Xbit_r6_c116 bl[116] br[116] wl[6] vdd gnd cell_6t
Xbit_r7_c116 bl[116] br[116] wl[7] vdd gnd cell_6t
Xbit_r8_c116 bl[116] br[116] wl[8] vdd gnd cell_6t
Xbit_r9_c116 bl[116] br[116] wl[9] vdd gnd cell_6t
Xbit_r10_c116 bl[116] br[116] wl[10] vdd gnd cell_6t
Xbit_r11_c116 bl[116] br[116] wl[11] vdd gnd cell_6t
Xbit_r12_c116 bl[116] br[116] wl[12] vdd gnd cell_6t
Xbit_r13_c116 bl[116] br[116] wl[13] vdd gnd cell_6t
Xbit_r14_c116 bl[116] br[116] wl[14] vdd gnd cell_6t
Xbit_r15_c116 bl[116] br[116] wl[15] vdd gnd cell_6t
Xbit_r16_c116 bl[116] br[116] wl[16] vdd gnd cell_6t
Xbit_r17_c116 bl[116] br[116] wl[17] vdd gnd cell_6t
Xbit_r18_c116 bl[116] br[116] wl[18] vdd gnd cell_6t
Xbit_r19_c116 bl[116] br[116] wl[19] vdd gnd cell_6t
Xbit_r20_c116 bl[116] br[116] wl[20] vdd gnd cell_6t
Xbit_r21_c116 bl[116] br[116] wl[21] vdd gnd cell_6t
Xbit_r22_c116 bl[116] br[116] wl[22] vdd gnd cell_6t
Xbit_r23_c116 bl[116] br[116] wl[23] vdd gnd cell_6t
Xbit_r24_c116 bl[116] br[116] wl[24] vdd gnd cell_6t
Xbit_r25_c116 bl[116] br[116] wl[25] vdd gnd cell_6t
Xbit_r26_c116 bl[116] br[116] wl[26] vdd gnd cell_6t
Xbit_r27_c116 bl[116] br[116] wl[27] vdd gnd cell_6t
Xbit_r28_c116 bl[116] br[116] wl[28] vdd gnd cell_6t
Xbit_r29_c116 bl[116] br[116] wl[29] vdd gnd cell_6t
Xbit_r30_c116 bl[116] br[116] wl[30] vdd gnd cell_6t
Xbit_r31_c116 bl[116] br[116] wl[31] vdd gnd cell_6t
Xbit_r32_c116 bl[116] br[116] wl[32] vdd gnd cell_6t
Xbit_r33_c116 bl[116] br[116] wl[33] vdd gnd cell_6t
Xbit_r34_c116 bl[116] br[116] wl[34] vdd gnd cell_6t
Xbit_r35_c116 bl[116] br[116] wl[35] vdd gnd cell_6t
Xbit_r36_c116 bl[116] br[116] wl[36] vdd gnd cell_6t
Xbit_r37_c116 bl[116] br[116] wl[37] vdd gnd cell_6t
Xbit_r38_c116 bl[116] br[116] wl[38] vdd gnd cell_6t
Xbit_r39_c116 bl[116] br[116] wl[39] vdd gnd cell_6t
Xbit_r40_c116 bl[116] br[116] wl[40] vdd gnd cell_6t
Xbit_r41_c116 bl[116] br[116] wl[41] vdd gnd cell_6t
Xbit_r42_c116 bl[116] br[116] wl[42] vdd gnd cell_6t
Xbit_r43_c116 bl[116] br[116] wl[43] vdd gnd cell_6t
Xbit_r44_c116 bl[116] br[116] wl[44] vdd gnd cell_6t
Xbit_r45_c116 bl[116] br[116] wl[45] vdd gnd cell_6t
Xbit_r46_c116 bl[116] br[116] wl[46] vdd gnd cell_6t
Xbit_r47_c116 bl[116] br[116] wl[47] vdd gnd cell_6t
Xbit_r48_c116 bl[116] br[116] wl[48] vdd gnd cell_6t
Xbit_r49_c116 bl[116] br[116] wl[49] vdd gnd cell_6t
Xbit_r50_c116 bl[116] br[116] wl[50] vdd gnd cell_6t
Xbit_r51_c116 bl[116] br[116] wl[51] vdd gnd cell_6t
Xbit_r52_c116 bl[116] br[116] wl[52] vdd gnd cell_6t
Xbit_r53_c116 bl[116] br[116] wl[53] vdd gnd cell_6t
Xbit_r54_c116 bl[116] br[116] wl[54] vdd gnd cell_6t
Xbit_r55_c116 bl[116] br[116] wl[55] vdd gnd cell_6t
Xbit_r56_c116 bl[116] br[116] wl[56] vdd gnd cell_6t
Xbit_r57_c116 bl[116] br[116] wl[57] vdd gnd cell_6t
Xbit_r58_c116 bl[116] br[116] wl[58] vdd gnd cell_6t
Xbit_r59_c116 bl[116] br[116] wl[59] vdd gnd cell_6t
Xbit_r60_c116 bl[116] br[116] wl[60] vdd gnd cell_6t
Xbit_r61_c116 bl[116] br[116] wl[61] vdd gnd cell_6t
Xbit_r62_c116 bl[116] br[116] wl[62] vdd gnd cell_6t
Xbit_r63_c116 bl[116] br[116] wl[63] vdd gnd cell_6t
Xbit_r0_c117 bl[117] br[117] wl[0] vdd gnd cell_6t
Xbit_r1_c117 bl[117] br[117] wl[1] vdd gnd cell_6t
Xbit_r2_c117 bl[117] br[117] wl[2] vdd gnd cell_6t
Xbit_r3_c117 bl[117] br[117] wl[3] vdd gnd cell_6t
Xbit_r4_c117 bl[117] br[117] wl[4] vdd gnd cell_6t
Xbit_r5_c117 bl[117] br[117] wl[5] vdd gnd cell_6t
Xbit_r6_c117 bl[117] br[117] wl[6] vdd gnd cell_6t
Xbit_r7_c117 bl[117] br[117] wl[7] vdd gnd cell_6t
Xbit_r8_c117 bl[117] br[117] wl[8] vdd gnd cell_6t
Xbit_r9_c117 bl[117] br[117] wl[9] vdd gnd cell_6t
Xbit_r10_c117 bl[117] br[117] wl[10] vdd gnd cell_6t
Xbit_r11_c117 bl[117] br[117] wl[11] vdd gnd cell_6t
Xbit_r12_c117 bl[117] br[117] wl[12] vdd gnd cell_6t
Xbit_r13_c117 bl[117] br[117] wl[13] vdd gnd cell_6t
Xbit_r14_c117 bl[117] br[117] wl[14] vdd gnd cell_6t
Xbit_r15_c117 bl[117] br[117] wl[15] vdd gnd cell_6t
Xbit_r16_c117 bl[117] br[117] wl[16] vdd gnd cell_6t
Xbit_r17_c117 bl[117] br[117] wl[17] vdd gnd cell_6t
Xbit_r18_c117 bl[117] br[117] wl[18] vdd gnd cell_6t
Xbit_r19_c117 bl[117] br[117] wl[19] vdd gnd cell_6t
Xbit_r20_c117 bl[117] br[117] wl[20] vdd gnd cell_6t
Xbit_r21_c117 bl[117] br[117] wl[21] vdd gnd cell_6t
Xbit_r22_c117 bl[117] br[117] wl[22] vdd gnd cell_6t
Xbit_r23_c117 bl[117] br[117] wl[23] vdd gnd cell_6t
Xbit_r24_c117 bl[117] br[117] wl[24] vdd gnd cell_6t
Xbit_r25_c117 bl[117] br[117] wl[25] vdd gnd cell_6t
Xbit_r26_c117 bl[117] br[117] wl[26] vdd gnd cell_6t
Xbit_r27_c117 bl[117] br[117] wl[27] vdd gnd cell_6t
Xbit_r28_c117 bl[117] br[117] wl[28] vdd gnd cell_6t
Xbit_r29_c117 bl[117] br[117] wl[29] vdd gnd cell_6t
Xbit_r30_c117 bl[117] br[117] wl[30] vdd gnd cell_6t
Xbit_r31_c117 bl[117] br[117] wl[31] vdd gnd cell_6t
Xbit_r32_c117 bl[117] br[117] wl[32] vdd gnd cell_6t
Xbit_r33_c117 bl[117] br[117] wl[33] vdd gnd cell_6t
Xbit_r34_c117 bl[117] br[117] wl[34] vdd gnd cell_6t
Xbit_r35_c117 bl[117] br[117] wl[35] vdd gnd cell_6t
Xbit_r36_c117 bl[117] br[117] wl[36] vdd gnd cell_6t
Xbit_r37_c117 bl[117] br[117] wl[37] vdd gnd cell_6t
Xbit_r38_c117 bl[117] br[117] wl[38] vdd gnd cell_6t
Xbit_r39_c117 bl[117] br[117] wl[39] vdd gnd cell_6t
Xbit_r40_c117 bl[117] br[117] wl[40] vdd gnd cell_6t
Xbit_r41_c117 bl[117] br[117] wl[41] vdd gnd cell_6t
Xbit_r42_c117 bl[117] br[117] wl[42] vdd gnd cell_6t
Xbit_r43_c117 bl[117] br[117] wl[43] vdd gnd cell_6t
Xbit_r44_c117 bl[117] br[117] wl[44] vdd gnd cell_6t
Xbit_r45_c117 bl[117] br[117] wl[45] vdd gnd cell_6t
Xbit_r46_c117 bl[117] br[117] wl[46] vdd gnd cell_6t
Xbit_r47_c117 bl[117] br[117] wl[47] vdd gnd cell_6t
Xbit_r48_c117 bl[117] br[117] wl[48] vdd gnd cell_6t
Xbit_r49_c117 bl[117] br[117] wl[49] vdd gnd cell_6t
Xbit_r50_c117 bl[117] br[117] wl[50] vdd gnd cell_6t
Xbit_r51_c117 bl[117] br[117] wl[51] vdd gnd cell_6t
Xbit_r52_c117 bl[117] br[117] wl[52] vdd gnd cell_6t
Xbit_r53_c117 bl[117] br[117] wl[53] vdd gnd cell_6t
Xbit_r54_c117 bl[117] br[117] wl[54] vdd gnd cell_6t
Xbit_r55_c117 bl[117] br[117] wl[55] vdd gnd cell_6t
Xbit_r56_c117 bl[117] br[117] wl[56] vdd gnd cell_6t
Xbit_r57_c117 bl[117] br[117] wl[57] vdd gnd cell_6t
Xbit_r58_c117 bl[117] br[117] wl[58] vdd gnd cell_6t
Xbit_r59_c117 bl[117] br[117] wl[59] vdd gnd cell_6t
Xbit_r60_c117 bl[117] br[117] wl[60] vdd gnd cell_6t
Xbit_r61_c117 bl[117] br[117] wl[61] vdd gnd cell_6t
Xbit_r62_c117 bl[117] br[117] wl[62] vdd gnd cell_6t
Xbit_r63_c117 bl[117] br[117] wl[63] vdd gnd cell_6t
Xbit_r0_c118 bl[118] br[118] wl[0] vdd gnd cell_6t
Xbit_r1_c118 bl[118] br[118] wl[1] vdd gnd cell_6t
Xbit_r2_c118 bl[118] br[118] wl[2] vdd gnd cell_6t
Xbit_r3_c118 bl[118] br[118] wl[3] vdd gnd cell_6t
Xbit_r4_c118 bl[118] br[118] wl[4] vdd gnd cell_6t
Xbit_r5_c118 bl[118] br[118] wl[5] vdd gnd cell_6t
Xbit_r6_c118 bl[118] br[118] wl[6] vdd gnd cell_6t
Xbit_r7_c118 bl[118] br[118] wl[7] vdd gnd cell_6t
Xbit_r8_c118 bl[118] br[118] wl[8] vdd gnd cell_6t
Xbit_r9_c118 bl[118] br[118] wl[9] vdd gnd cell_6t
Xbit_r10_c118 bl[118] br[118] wl[10] vdd gnd cell_6t
Xbit_r11_c118 bl[118] br[118] wl[11] vdd gnd cell_6t
Xbit_r12_c118 bl[118] br[118] wl[12] vdd gnd cell_6t
Xbit_r13_c118 bl[118] br[118] wl[13] vdd gnd cell_6t
Xbit_r14_c118 bl[118] br[118] wl[14] vdd gnd cell_6t
Xbit_r15_c118 bl[118] br[118] wl[15] vdd gnd cell_6t
Xbit_r16_c118 bl[118] br[118] wl[16] vdd gnd cell_6t
Xbit_r17_c118 bl[118] br[118] wl[17] vdd gnd cell_6t
Xbit_r18_c118 bl[118] br[118] wl[18] vdd gnd cell_6t
Xbit_r19_c118 bl[118] br[118] wl[19] vdd gnd cell_6t
Xbit_r20_c118 bl[118] br[118] wl[20] vdd gnd cell_6t
Xbit_r21_c118 bl[118] br[118] wl[21] vdd gnd cell_6t
Xbit_r22_c118 bl[118] br[118] wl[22] vdd gnd cell_6t
Xbit_r23_c118 bl[118] br[118] wl[23] vdd gnd cell_6t
Xbit_r24_c118 bl[118] br[118] wl[24] vdd gnd cell_6t
Xbit_r25_c118 bl[118] br[118] wl[25] vdd gnd cell_6t
Xbit_r26_c118 bl[118] br[118] wl[26] vdd gnd cell_6t
Xbit_r27_c118 bl[118] br[118] wl[27] vdd gnd cell_6t
Xbit_r28_c118 bl[118] br[118] wl[28] vdd gnd cell_6t
Xbit_r29_c118 bl[118] br[118] wl[29] vdd gnd cell_6t
Xbit_r30_c118 bl[118] br[118] wl[30] vdd gnd cell_6t
Xbit_r31_c118 bl[118] br[118] wl[31] vdd gnd cell_6t
Xbit_r32_c118 bl[118] br[118] wl[32] vdd gnd cell_6t
Xbit_r33_c118 bl[118] br[118] wl[33] vdd gnd cell_6t
Xbit_r34_c118 bl[118] br[118] wl[34] vdd gnd cell_6t
Xbit_r35_c118 bl[118] br[118] wl[35] vdd gnd cell_6t
Xbit_r36_c118 bl[118] br[118] wl[36] vdd gnd cell_6t
Xbit_r37_c118 bl[118] br[118] wl[37] vdd gnd cell_6t
Xbit_r38_c118 bl[118] br[118] wl[38] vdd gnd cell_6t
Xbit_r39_c118 bl[118] br[118] wl[39] vdd gnd cell_6t
Xbit_r40_c118 bl[118] br[118] wl[40] vdd gnd cell_6t
Xbit_r41_c118 bl[118] br[118] wl[41] vdd gnd cell_6t
Xbit_r42_c118 bl[118] br[118] wl[42] vdd gnd cell_6t
Xbit_r43_c118 bl[118] br[118] wl[43] vdd gnd cell_6t
Xbit_r44_c118 bl[118] br[118] wl[44] vdd gnd cell_6t
Xbit_r45_c118 bl[118] br[118] wl[45] vdd gnd cell_6t
Xbit_r46_c118 bl[118] br[118] wl[46] vdd gnd cell_6t
Xbit_r47_c118 bl[118] br[118] wl[47] vdd gnd cell_6t
Xbit_r48_c118 bl[118] br[118] wl[48] vdd gnd cell_6t
Xbit_r49_c118 bl[118] br[118] wl[49] vdd gnd cell_6t
Xbit_r50_c118 bl[118] br[118] wl[50] vdd gnd cell_6t
Xbit_r51_c118 bl[118] br[118] wl[51] vdd gnd cell_6t
Xbit_r52_c118 bl[118] br[118] wl[52] vdd gnd cell_6t
Xbit_r53_c118 bl[118] br[118] wl[53] vdd gnd cell_6t
Xbit_r54_c118 bl[118] br[118] wl[54] vdd gnd cell_6t
Xbit_r55_c118 bl[118] br[118] wl[55] vdd gnd cell_6t
Xbit_r56_c118 bl[118] br[118] wl[56] vdd gnd cell_6t
Xbit_r57_c118 bl[118] br[118] wl[57] vdd gnd cell_6t
Xbit_r58_c118 bl[118] br[118] wl[58] vdd gnd cell_6t
Xbit_r59_c118 bl[118] br[118] wl[59] vdd gnd cell_6t
Xbit_r60_c118 bl[118] br[118] wl[60] vdd gnd cell_6t
Xbit_r61_c118 bl[118] br[118] wl[61] vdd gnd cell_6t
Xbit_r62_c118 bl[118] br[118] wl[62] vdd gnd cell_6t
Xbit_r63_c118 bl[118] br[118] wl[63] vdd gnd cell_6t
Xbit_r0_c119 bl[119] br[119] wl[0] vdd gnd cell_6t
Xbit_r1_c119 bl[119] br[119] wl[1] vdd gnd cell_6t
Xbit_r2_c119 bl[119] br[119] wl[2] vdd gnd cell_6t
Xbit_r3_c119 bl[119] br[119] wl[3] vdd gnd cell_6t
Xbit_r4_c119 bl[119] br[119] wl[4] vdd gnd cell_6t
Xbit_r5_c119 bl[119] br[119] wl[5] vdd gnd cell_6t
Xbit_r6_c119 bl[119] br[119] wl[6] vdd gnd cell_6t
Xbit_r7_c119 bl[119] br[119] wl[7] vdd gnd cell_6t
Xbit_r8_c119 bl[119] br[119] wl[8] vdd gnd cell_6t
Xbit_r9_c119 bl[119] br[119] wl[9] vdd gnd cell_6t
Xbit_r10_c119 bl[119] br[119] wl[10] vdd gnd cell_6t
Xbit_r11_c119 bl[119] br[119] wl[11] vdd gnd cell_6t
Xbit_r12_c119 bl[119] br[119] wl[12] vdd gnd cell_6t
Xbit_r13_c119 bl[119] br[119] wl[13] vdd gnd cell_6t
Xbit_r14_c119 bl[119] br[119] wl[14] vdd gnd cell_6t
Xbit_r15_c119 bl[119] br[119] wl[15] vdd gnd cell_6t
Xbit_r16_c119 bl[119] br[119] wl[16] vdd gnd cell_6t
Xbit_r17_c119 bl[119] br[119] wl[17] vdd gnd cell_6t
Xbit_r18_c119 bl[119] br[119] wl[18] vdd gnd cell_6t
Xbit_r19_c119 bl[119] br[119] wl[19] vdd gnd cell_6t
Xbit_r20_c119 bl[119] br[119] wl[20] vdd gnd cell_6t
Xbit_r21_c119 bl[119] br[119] wl[21] vdd gnd cell_6t
Xbit_r22_c119 bl[119] br[119] wl[22] vdd gnd cell_6t
Xbit_r23_c119 bl[119] br[119] wl[23] vdd gnd cell_6t
Xbit_r24_c119 bl[119] br[119] wl[24] vdd gnd cell_6t
Xbit_r25_c119 bl[119] br[119] wl[25] vdd gnd cell_6t
Xbit_r26_c119 bl[119] br[119] wl[26] vdd gnd cell_6t
Xbit_r27_c119 bl[119] br[119] wl[27] vdd gnd cell_6t
Xbit_r28_c119 bl[119] br[119] wl[28] vdd gnd cell_6t
Xbit_r29_c119 bl[119] br[119] wl[29] vdd gnd cell_6t
Xbit_r30_c119 bl[119] br[119] wl[30] vdd gnd cell_6t
Xbit_r31_c119 bl[119] br[119] wl[31] vdd gnd cell_6t
Xbit_r32_c119 bl[119] br[119] wl[32] vdd gnd cell_6t
Xbit_r33_c119 bl[119] br[119] wl[33] vdd gnd cell_6t
Xbit_r34_c119 bl[119] br[119] wl[34] vdd gnd cell_6t
Xbit_r35_c119 bl[119] br[119] wl[35] vdd gnd cell_6t
Xbit_r36_c119 bl[119] br[119] wl[36] vdd gnd cell_6t
Xbit_r37_c119 bl[119] br[119] wl[37] vdd gnd cell_6t
Xbit_r38_c119 bl[119] br[119] wl[38] vdd gnd cell_6t
Xbit_r39_c119 bl[119] br[119] wl[39] vdd gnd cell_6t
Xbit_r40_c119 bl[119] br[119] wl[40] vdd gnd cell_6t
Xbit_r41_c119 bl[119] br[119] wl[41] vdd gnd cell_6t
Xbit_r42_c119 bl[119] br[119] wl[42] vdd gnd cell_6t
Xbit_r43_c119 bl[119] br[119] wl[43] vdd gnd cell_6t
Xbit_r44_c119 bl[119] br[119] wl[44] vdd gnd cell_6t
Xbit_r45_c119 bl[119] br[119] wl[45] vdd gnd cell_6t
Xbit_r46_c119 bl[119] br[119] wl[46] vdd gnd cell_6t
Xbit_r47_c119 bl[119] br[119] wl[47] vdd gnd cell_6t
Xbit_r48_c119 bl[119] br[119] wl[48] vdd gnd cell_6t
Xbit_r49_c119 bl[119] br[119] wl[49] vdd gnd cell_6t
Xbit_r50_c119 bl[119] br[119] wl[50] vdd gnd cell_6t
Xbit_r51_c119 bl[119] br[119] wl[51] vdd gnd cell_6t
Xbit_r52_c119 bl[119] br[119] wl[52] vdd gnd cell_6t
Xbit_r53_c119 bl[119] br[119] wl[53] vdd gnd cell_6t
Xbit_r54_c119 bl[119] br[119] wl[54] vdd gnd cell_6t
Xbit_r55_c119 bl[119] br[119] wl[55] vdd gnd cell_6t
Xbit_r56_c119 bl[119] br[119] wl[56] vdd gnd cell_6t
Xbit_r57_c119 bl[119] br[119] wl[57] vdd gnd cell_6t
Xbit_r58_c119 bl[119] br[119] wl[58] vdd gnd cell_6t
Xbit_r59_c119 bl[119] br[119] wl[59] vdd gnd cell_6t
Xbit_r60_c119 bl[119] br[119] wl[60] vdd gnd cell_6t
Xbit_r61_c119 bl[119] br[119] wl[61] vdd gnd cell_6t
Xbit_r62_c119 bl[119] br[119] wl[62] vdd gnd cell_6t
Xbit_r63_c119 bl[119] br[119] wl[63] vdd gnd cell_6t
Xbit_r0_c120 bl[120] br[120] wl[0] vdd gnd cell_6t
Xbit_r1_c120 bl[120] br[120] wl[1] vdd gnd cell_6t
Xbit_r2_c120 bl[120] br[120] wl[2] vdd gnd cell_6t
Xbit_r3_c120 bl[120] br[120] wl[3] vdd gnd cell_6t
Xbit_r4_c120 bl[120] br[120] wl[4] vdd gnd cell_6t
Xbit_r5_c120 bl[120] br[120] wl[5] vdd gnd cell_6t
Xbit_r6_c120 bl[120] br[120] wl[6] vdd gnd cell_6t
Xbit_r7_c120 bl[120] br[120] wl[7] vdd gnd cell_6t
Xbit_r8_c120 bl[120] br[120] wl[8] vdd gnd cell_6t
Xbit_r9_c120 bl[120] br[120] wl[9] vdd gnd cell_6t
Xbit_r10_c120 bl[120] br[120] wl[10] vdd gnd cell_6t
Xbit_r11_c120 bl[120] br[120] wl[11] vdd gnd cell_6t
Xbit_r12_c120 bl[120] br[120] wl[12] vdd gnd cell_6t
Xbit_r13_c120 bl[120] br[120] wl[13] vdd gnd cell_6t
Xbit_r14_c120 bl[120] br[120] wl[14] vdd gnd cell_6t
Xbit_r15_c120 bl[120] br[120] wl[15] vdd gnd cell_6t
Xbit_r16_c120 bl[120] br[120] wl[16] vdd gnd cell_6t
Xbit_r17_c120 bl[120] br[120] wl[17] vdd gnd cell_6t
Xbit_r18_c120 bl[120] br[120] wl[18] vdd gnd cell_6t
Xbit_r19_c120 bl[120] br[120] wl[19] vdd gnd cell_6t
Xbit_r20_c120 bl[120] br[120] wl[20] vdd gnd cell_6t
Xbit_r21_c120 bl[120] br[120] wl[21] vdd gnd cell_6t
Xbit_r22_c120 bl[120] br[120] wl[22] vdd gnd cell_6t
Xbit_r23_c120 bl[120] br[120] wl[23] vdd gnd cell_6t
Xbit_r24_c120 bl[120] br[120] wl[24] vdd gnd cell_6t
Xbit_r25_c120 bl[120] br[120] wl[25] vdd gnd cell_6t
Xbit_r26_c120 bl[120] br[120] wl[26] vdd gnd cell_6t
Xbit_r27_c120 bl[120] br[120] wl[27] vdd gnd cell_6t
Xbit_r28_c120 bl[120] br[120] wl[28] vdd gnd cell_6t
Xbit_r29_c120 bl[120] br[120] wl[29] vdd gnd cell_6t
Xbit_r30_c120 bl[120] br[120] wl[30] vdd gnd cell_6t
Xbit_r31_c120 bl[120] br[120] wl[31] vdd gnd cell_6t
Xbit_r32_c120 bl[120] br[120] wl[32] vdd gnd cell_6t
Xbit_r33_c120 bl[120] br[120] wl[33] vdd gnd cell_6t
Xbit_r34_c120 bl[120] br[120] wl[34] vdd gnd cell_6t
Xbit_r35_c120 bl[120] br[120] wl[35] vdd gnd cell_6t
Xbit_r36_c120 bl[120] br[120] wl[36] vdd gnd cell_6t
Xbit_r37_c120 bl[120] br[120] wl[37] vdd gnd cell_6t
Xbit_r38_c120 bl[120] br[120] wl[38] vdd gnd cell_6t
Xbit_r39_c120 bl[120] br[120] wl[39] vdd gnd cell_6t
Xbit_r40_c120 bl[120] br[120] wl[40] vdd gnd cell_6t
Xbit_r41_c120 bl[120] br[120] wl[41] vdd gnd cell_6t
Xbit_r42_c120 bl[120] br[120] wl[42] vdd gnd cell_6t
Xbit_r43_c120 bl[120] br[120] wl[43] vdd gnd cell_6t
Xbit_r44_c120 bl[120] br[120] wl[44] vdd gnd cell_6t
Xbit_r45_c120 bl[120] br[120] wl[45] vdd gnd cell_6t
Xbit_r46_c120 bl[120] br[120] wl[46] vdd gnd cell_6t
Xbit_r47_c120 bl[120] br[120] wl[47] vdd gnd cell_6t
Xbit_r48_c120 bl[120] br[120] wl[48] vdd gnd cell_6t
Xbit_r49_c120 bl[120] br[120] wl[49] vdd gnd cell_6t
Xbit_r50_c120 bl[120] br[120] wl[50] vdd gnd cell_6t
Xbit_r51_c120 bl[120] br[120] wl[51] vdd gnd cell_6t
Xbit_r52_c120 bl[120] br[120] wl[52] vdd gnd cell_6t
Xbit_r53_c120 bl[120] br[120] wl[53] vdd gnd cell_6t
Xbit_r54_c120 bl[120] br[120] wl[54] vdd gnd cell_6t
Xbit_r55_c120 bl[120] br[120] wl[55] vdd gnd cell_6t
Xbit_r56_c120 bl[120] br[120] wl[56] vdd gnd cell_6t
Xbit_r57_c120 bl[120] br[120] wl[57] vdd gnd cell_6t
Xbit_r58_c120 bl[120] br[120] wl[58] vdd gnd cell_6t
Xbit_r59_c120 bl[120] br[120] wl[59] vdd gnd cell_6t
Xbit_r60_c120 bl[120] br[120] wl[60] vdd gnd cell_6t
Xbit_r61_c120 bl[120] br[120] wl[61] vdd gnd cell_6t
Xbit_r62_c120 bl[120] br[120] wl[62] vdd gnd cell_6t
Xbit_r63_c120 bl[120] br[120] wl[63] vdd gnd cell_6t
Xbit_r0_c121 bl[121] br[121] wl[0] vdd gnd cell_6t
Xbit_r1_c121 bl[121] br[121] wl[1] vdd gnd cell_6t
Xbit_r2_c121 bl[121] br[121] wl[2] vdd gnd cell_6t
Xbit_r3_c121 bl[121] br[121] wl[3] vdd gnd cell_6t
Xbit_r4_c121 bl[121] br[121] wl[4] vdd gnd cell_6t
Xbit_r5_c121 bl[121] br[121] wl[5] vdd gnd cell_6t
Xbit_r6_c121 bl[121] br[121] wl[6] vdd gnd cell_6t
Xbit_r7_c121 bl[121] br[121] wl[7] vdd gnd cell_6t
Xbit_r8_c121 bl[121] br[121] wl[8] vdd gnd cell_6t
Xbit_r9_c121 bl[121] br[121] wl[9] vdd gnd cell_6t
Xbit_r10_c121 bl[121] br[121] wl[10] vdd gnd cell_6t
Xbit_r11_c121 bl[121] br[121] wl[11] vdd gnd cell_6t
Xbit_r12_c121 bl[121] br[121] wl[12] vdd gnd cell_6t
Xbit_r13_c121 bl[121] br[121] wl[13] vdd gnd cell_6t
Xbit_r14_c121 bl[121] br[121] wl[14] vdd gnd cell_6t
Xbit_r15_c121 bl[121] br[121] wl[15] vdd gnd cell_6t
Xbit_r16_c121 bl[121] br[121] wl[16] vdd gnd cell_6t
Xbit_r17_c121 bl[121] br[121] wl[17] vdd gnd cell_6t
Xbit_r18_c121 bl[121] br[121] wl[18] vdd gnd cell_6t
Xbit_r19_c121 bl[121] br[121] wl[19] vdd gnd cell_6t
Xbit_r20_c121 bl[121] br[121] wl[20] vdd gnd cell_6t
Xbit_r21_c121 bl[121] br[121] wl[21] vdd gnd cell_6t
Xbit_r22_c121 bl[121] br[121] wl[22] vdd gnd cell_6t
Xbit_r23_c121 bl[121] br[121] wl[23] vdd gnd cell_6t
Xbit_r24_c121 bl[121] br[121] wl[24] vdd gnd cell_6t
Xbit_r25_c121 bl[121] br[121] wl[25] vdd gnd cell_6t
Xbit_r26_c121 bl[121] br[121] wl[26] vdd gnd cell_6t
Xbit_r27_c121 bl[121] br[121] wl[27] vdd gnd cell_6t
Xbit_r28_c121 bl[121] br[121] wl[28] vdd gnd cell_6t
Xbit_r29_c121 bl[121] br[121] wl[29] vdd gnd cell_6t
Xbit_r30_c121 bl[121] br[121] wl[30] vdd gnd cell_6t
Xbit_r31_c121 bl[121] br[121] wl[31] vdd gnd cell_6t
Xbit_r32_c121 bl[121] br[121] wl[32] vdd gnd cell_6t
Xbit_r33_c121 bl[121] br[121] wl[33] vdd gnd cell_6t
Xbit_r34_c121 bl[121] br[121] wl[34] vdd gnd cell_6t
Xbit_r35_c121 bl[121] br[121] wl[35] vdd gnd cell_6t
Xbit_r36_c121 bl[121] br[121] wl[36] vdd gnd cell_6t
Xbit_r37_c121 bl[121] br[121] wl[37] vdd gnd cell_6t
Xbit_r38_c121 bl[121] br[121] wl[38] vdd gnd cell_6t
Xbit_r39_c121 bl[121] br[121] wl[39] vdd gnd cell_6t
Xbit_r40_c121 bl[121] br[121] wl[40] vdd gnd cell_6t
Xbit_r41_c121 bl[121] br[121] wl[41] vdd gnd cell_6t
Xbit_r42_c121 bl[121] br[121] wl[42] vdd gnd cell_6t
Xbit_r43_c121 bl[121] br[121] wl[43] vdd gnd cell_6t
Xbit_r44_c121 bl[121] br[121] wl[44] vdd gnd cell_6t
Xbit_r45_c121 bl[121] br[121] wl[45] vdd gnd cell_6t
Xbit_r46_c121 bl[121] br[121] wl[46] vdd gnd cell_6t
Xbit_r47_c121 bl[121] br[121] wl[47] vdd gnd cell_6t
Xbit_r48_c121 bl[121] br[121] wl[48] vdd gnd cell_6t
Xbit_r49_c121 bl[121] br[121] wl[49] vdd gnd cell_6t
Xbit_r50_c121 bl[121] br[121] wl[50] vdd gnd cell_6t
Xbit_r51_c121 bl[121] br[121] wl[51] vdd gnd cell_6t
Xbit_r52_c121 bl[121] br[121] wl[52] vdd gnd cell_6t
Xbit_r53_c121 bl[121] br[121] wl[53] vdd gnd cell_6t
Xbit_r54_c121 bl[121] br[121] wl[54] vdd gnd cell_6t
Xbit_r55_c121 bl[121] br[121] wl[55] vdd gnd cell_6t
Xbit_r56_c121 bl[121] br[121] wl[56] vdd gnd cell_6t
Xbit_r57_c121 bl[121] br[121] wl[57] vdd gnd cell_6t
Xbit_r58_c121 bl[121] br[121] wl[58] vdd gnd cell_6t
Xbit_r59_c121 bl[121] br[121] wl[59] vdd gnd cell_6t
Xbit_r60_c121 bl[121] br[121] wl[60] vdd gnd cell_6t
Xbit_r61_c121 bl[121] br[121] wl[61] vdd gnd cell_6t
Xbit_r62_c121 bl[121] br[121] wl[62] vdd gnd cell_6t
Xbit_r63_c121 bl[121] br[121] wl[63] vdd gnd cell_6t
Xbit_r0_c122 bl[122] br[122] wl[0] vdd gnd cell_6t
Xbit_r1_c122 bl[122] br[122] wl[1] vdd gnd cell_6t
Xbit_r2_c122 bl[122] br[122] wl[2] vdd gnd cell_6t
Xbit_r3_c122 bl[122] br[122] wl[3] vdd gnd cell_6t
Xbit_r4_c122 bl[122] br[122] wl[4] vdd gnd cell_6t
Xbit_r5_c122 bl[122] br[122] wl[5] vdd gnd cell_6t
Xbit_r6_c122 bl[122] br[122] wl[6] vdd gnd cell_6t
Xbit_r7_c122 bl[122] br[122] wl[7] vdd gnd cell_6t
Xbit_r8_c122 bl[122] br[122] wl[8] vdd gnd cell_6t
Xbit_r9_c122 bl[122] br[122] wl[9] vdd gnd cell_6t
Xbit_r10_c122 bl[122] br[122] wl[10] vdd gnd cell_6t
Xbit_r11_c122 bl[122] br[122] wl[11] vdd gnd cell_6t
Xbit_r12_c122 bl[122] br[122] wl[12] vdd gnd cell_6t
Xbit_r13_c122 bl[122] br[122] wl[13] vdd gnd cell_6t
Xbit_r14_c122 bl[122] br[122] wl[14] vdd gnd cell_6t
Xbit_r15_c122 bl[122] br[122] wl[15] vdd gnd cell_6t
Xbit_r16_c122 bl[122] br[122] wl[16] vdd gnd cell_6t
Xbit_r17_c122 bl[122] br[122] wl[17] vdd gnd cell_6t
Xbit_r18_c122 bl[122] br[122] wl[18] vdd gnd cell_6t
Xbit_r19_c122 bl[122] br[122] wl[19] vdd gnd cell_6t
Xbit_r20_c122 bl[122] br[122] wl[20] vdd gnd cell_6t
Xbit_r21_c122 bl[122] br[122] wl[21] vdd gnd cell_6t
Xbit_r22_c122 bl[122] br[122] wl[22] vdd gnd cell_6t
Xbit_r23_c122 bl[122] br[122] wl[23] vdd gnd cell_6t
Xbit_r24_c122 bl[122] br[122] wl[24] vdd gnd cell_6t
Xbit_r25_c122 bl[122] br[122] wl[25] vdd gnd cell_6t
Xbit_r26_c122 bl[122] br[122] wl[26] vdd gnd cell_6t
Xbit_r27_c122 bl[122] br[122] wl[27] vdd gnd cell_6t
Xbit_r28_c122 bl[122] br[122] wl[28] vdd gnd cell_6t
Xbit_r29_c122 bl[122] br[122] wl[29] vdd gnd cell_6t
Xbit_r30_c122 bl[122] br[122] wl[30] vdd gnd cell_6t
Xbit_r31_c122 bl[122] br[122] wl[31] vdd gnd cell_6t
Xbit_r32_c122 bl[122] br[122] wl[32] vdd gnd cell_6t
Xbit_r33_c122 bl[122] br[122] wl[33] vdd gnd cell_6t
Xbit_r34_c122 bl[122] br[122] wl[34] vdd gnd cell_6t
Xbit_r35_c122 bl[122] br[122] wl[35] vdd gnd cell_6t
Xbit_r36_c122 bl[122] br[122] wl[36] vdd gnd cell_6t
Xbit_r37_c122 bl[122] br[122] wl[37] vdd gnd cell_6t
Xbit_r38_c122 bl[122] br[122] wl[38] vdd gnd cell_6t
Xbit_r39_c122 bl[122] br[122] wl[39] vdd gnd cell_6t
Xbit_r40_c122 bl[122] br[122] wl[40] vdd gnd cell_6t
Xbit_r41_c122 bl[122] br[122] wl[41] vdd gnd cell_6t
Xbit_r42_c122 bl[122] br[122] wl[42] vdd gnd cell_6t
Xbit_r43_c122 bl[122] br[122] wl[43] vdd gnd cell_6t
Xbit_r44_c122 bl[122] br[122] wl[44] vdd gnd cell_6t
Xbit_r45_c122 bl[122] br[122] wl[45] vdd gnd cell_6t
Xbit_r46_c122 bl[122] br[122] wl[46] vdd gnd cell_6t
Xbit_r47_c122 bl[122] br[122] wl[47] vdd gnd cell_6t
Xbit_r48_c122 bl[122] br[122] wl[48] vdd gnd cell_6t
Xbit_r49_c122 bl[122] br[122] wl[49] vdd gnd cell_6t
Xbit_r50_c122 bl[122] br[122] wl[50] vdd gnd cell_6t
Xbit_r51_c122 bl[122] br[122] wl[51] vdd gnd cell_6t
Xbit_r52_c122 bl[122] br[122] wl[52] vdd gnd cell_6t
Xbit_r53_c122 bl[122] br[122] wl[53] vdd gnd cell_6t
Xbit_r54_c122 bl[122] br[122] wl[54] vdd gnd cell_6t
Xbit_r55_c122 bl[122] br[122] wl[55] vdd gnd cell_6t
Xbit_r56_c122 bl[122] br[122] wl[56] vdd gnd cell_6t
Xbit_r57_c122 bl[122] br[122] wl[57] vdd gnd cell_6t
Xbit_r58_c122 bl[122] br[122] wl[58] vdd gnd cell_6t
Xbit_r59_c122 bl[122] br[122] wl[59] vdd gnd cell_6t
Xbit_r60_c122 bl[122] br[122] wl[60] vdd gnd cell_6t
Xbit_r61_c122 bl[122] br[122] wl[61] vdd gnd cell_6t
Xbit_r62_c122 bl[122] br[122] wl[62] vdd gnd cell_6t
Xbit_r63_c122 bl[122] br[122] wl[63] vdd gnd cell_6t
Xbit_r0_c123 bl[123] br[123] wl[0] vdd gnd cell_6t
Xbit_r1_c123 bl[123] br[123] wl[1] vdd gnd cell_6t
Xbit_r2_c123 bl[123] br[123] wl[2] vdd gnd cell_6t
Xbit_r3_c123 bl[123] br[123] wl[3] vdd gnd cell_6t
Xbit_r4_c123 bl[123] br[123] wl[4] vdd gnd cell_6t
Xbit_r5_c123 bl[123] br[123] wl[5] vdd gnd cell_6t
Xbit_r6_c123 bl[123] br[123] wl[6] vdd gnd cell_6t
Xbit_r7_c123 bl[123] br[123] wl[7] vdd gnd cell_6t
Xbit_r8_c123 bl[123] br[123] wl[8] vdd gnd cell_6t
Xbit_r9_c123 bl[123] br[123] wl[9] vdd gnd cell_6t
Xbit_r10_c123 bl[123] br[123] wl[10] vdd gnd cell_6t
Xbit_r11_c123 bl[123] br[123] wl[11] vdd gnd cell_6t
Xbit_r12_c123 bl[123] br[123] wl[12] vdd gnd cell_6t
Xbit_r13_c123 bl[123] br[123] wl[13] vdd gnd cell_6t
Xbit_r14_c123 bl[123] br[123] wl[14] vdd gnd cell_6t
Xbit_r15_c123 bl[123] br[123] wl[15] vdd gnd cell_6t
Xbit_r16_c123 bl[123] br[123] wl[16] vdd gnd cell_6t
Xbit_r17_c123 bl[123] br[123] wl[17] vdd gnd cell_6t
Xbit_r18_c123 bl[123] br[123] wl[18] vdd gnd cell_6t
Xbit_r19_c123 bl[123] br[123] wl[19] vdd gnd cell_6t
Xbit_r20_c123 bl[123] br[123] wl[20] vdd gnd cell_6t
Xbit_r21_c123 bl[123] br[123] wl[21] vdd gnd cell_6t
Xbit_r22_c123 bl[123] br[123] wl[22] vdd gnd cell_6t
Xbit_r23_c123 bl[123] br[123] wl[23] vdd gnd cell_6t
Xbit_r24_c123 bl[123] br[123] wl[24] vdd gnd cell_6t
Xbit_r25_c123 bl[123] br[123] wl[25] vdd gnd cell_6t
Xbit_r26_c123 bl[123] br[123] wl[26] vdd gnd cell_6t
Xbit_r27_c123 bl[123] br[123] wl[27] vdd gnd cell_6t
Xbit_r28_c123 bl[123] br[123] wl[28] vdd gnd cell_6t
Xbit_r29_c123 bl[123] br[123] wl[29] vdd gnd cell_6t
Xbit_r30_c123 bl[123] br[123] wl[30] vdd gnd cell_6t
Xbit_r31_c123 bl[123] br[123] wl[31] vdd gnd cell_6t
Xbit_r32_c123 bl[123] br[123] wl[32] vdd gnd cell_6t
Xbit_r33_c123 bl[123] br[123] wl[33] vdd gnd cell_6t
Xbit_r34_c123 bl[123] br[123] wl[34] vdd gnd cell_6t
Xbit_r35_c123 bl[123] br[123] wl[35] vdd gnd cell_6t
Xbit_r36_c123 bl[123] br[123] wl[36] vdd gnd cell_6t
Xbit_r37_c123 bl[123] br[123] wl[37] vdd gnd cell_6t
Xbit_r38_c123 bl[123] br[123] wl[38] vdd gnd cell_6t
Xbit_r39_c123 bl[123] br[123] wl[39] vdd gnd cell_6t
Xbit_r40_c123 bl[123] br[123] wl[40] vdd gnd cell_6t
Xbit_r41_c123 bl[123] br[123] wl[41] vdd gnd cell_6t
Xbit_r42_c123 bl[123] br[123] wl[42] vdd gnd cell_6t
Xbit_r43_c123 bl[123] br[123] wl[43] vdd gnd cell_6t
Xbit_r44_c123 bl[123] br[123] wl[44] vdd gnd cell_6t
Xbit_r45_c123 bl[123] br[123] wl[45] vdd gnd cell_6t
Xbit_r46_c123 bl[123] br[123] wl[46] vdd gnd cell_6t
Xbit_r47_c123 bl[123] br[123] wl[47] vdd gnd cell_6t
Xbit_r48_c123 bl[123] br[123] wl[48] vdd gnd cell_6t
Xbit_r49_c123 bl[123] br[123] wl[49] vdd gnd cell_6t
Xbit_r50_c123 bl[123] br[123] wl[50] vdd gnd cell_6t
Xbit_r51_c123 bl[123] br[123] wl[51] vdd gnd cell_6t
Xbit_r52_c123 bl[123] br[123] wl[52] vdd gnd cell_6t
Xbit_r53_c123 bl[123] br[123] wl[53] vdd gnd cell_6t
Xbit_r54_c123 bl[123] br[123] wl[54] vdd gnd cell_6t
Xbit_r55_c123 bl[123] br[123] wl[55] vdd gnd cell_6t
Xbit_r56_c123 bl[123] br[123] wl[56] vdd gnd cell_6t
Xbit_r57_c123 bl[123] br[123] wl[57] vdd gnd cell_6t
Xbit_r58_c123 bl[123] br[123] wl[58] vdd gnd cell_6t
Xbit_r59_c123 bl[123] br[123] wl[59] vdd gnd cell_6t
Xbit_r60_c123 bl[123] br[123] wl[60] vdd gnd cell_6t
Xbit_r61_c123 bl[123] br[123] wl[61] vdd gnd cell_6t
Xbit_r62_c123 bl[123] br[123] wl[62] vdd gnd cell_6t
Xbit_r63_c123 bl[123] br[123] wl[63] vdd gnd cell_6t
Xbit_r0_c124 bl[124] br[124] wl[0] vdd gnd cell_6t
Xbit_r1_c124 bl[124] br[124] wl[1] vdd gnd cell_6t
Xbit_r2_c124 bl[124] br[124] wl[2] vdd gnd cell_6t
Xbit_r3_c124 bl[124] br[124] wl[3] vdd gnd cell_6t
Xbit_r4_c124 bl[124] br[124] wl[4] vdd gnd cell_6t
Xbit_r5_c124 bl[124] br[124] wl[5] vdd gnd cell_6t
Xbit_r6_c124 bl[124] br[124] wl[6] vdd gnd cell_6t
Xbit_r7_c124 bl[124] br[124] wl[7] vdd gnd cell_6t
Xbit_r8_c124 bl[124] br[124] wl[8] vdd gnd cell_6t
Xbit_r9_c124 bl[124] br[124] wl[9] vdd gnd cell_6t
Xbit_r10_c124 bl[124] br[124] wl[10] vdd gnd cell_6t
Xbit_r11_c124 bl[124] br[124] wl[11] vdd gnd cell_6t
Xbit_r12_c124 bl[124] br[124] wl[12] vdd gnd cell_6t
Xbit_r13_c124 bl[124] br[124] wl[13] vdd gnd cell_6t
Xbit_r14_c124 bl[124] br[124] wl[14] vdd gnd cell_6t
Xbit_r15_c124 bl[124] br[124] wl[15] vdd gnd cell_6t
Xbit_r16_c124 bl[124] br[124] wl[16] vdd gnd cell_6t
Xbit_r17_c124 bl[124] br[124] wl[17] vdd gnd cell_6t
Xbit_r18_c124 bl[124] br[124] wl[18] vdd gnd cell_6t
Xbit_r19_c124 bl[124] br[124] wl[19] vdd gnd cell_6t
Xbit_r20_c124 bl[124] br[124] wl[20] vdd gnd cell_6t
Xbit_r21_c124 bl[124] br[124] wl[21] vdd gnd cell_6t
Xbit_r22_c124 bl[124] br[124] wl[22] vdd gnd cell_6t
Xbit_r23_c124 bl[124] br[124] wl[23] vdd gnd cell_6t
Xbit_r24_c124 bl[124] br[124] wl[24] vdd gnd cell_6t
Xbit_r25_c124 bl[124] br[124] wl[25] vdd gnd cell_6t
Xbit_r26_c124 bl[124] br[124] wl[26] vdd gnd cell_6t
Xbit_r27_c124 bl[124] br[124] wl[27] vdd gnd cell_6t
Xbit_r28_c124 bl[124] br[124] wl[28] vdd gnd cell_6t
Xbit_r29_c124 bl[124] br[124] wl[29] vdd gnd cell_6t
Xbit_r30_c124 bl[124] br[124] wl[30] vdd gnd cell_6t
Xbit_r31_c124 bl[124] br[124] wl[31] vdd gnd cell_6t
Xbit_r32_c124 bl[124] br[124] wl[32] vdd gnd cell_6t
Xbit_r33_c124 bl[124] br[124] wl[33] vdd gnd cell_6t
Xbit_r34_c124 bl[124] br[124] wl[34] vdd gnd cell_6t
Xbit_r35_c124 bl[124] br[124] wl[35] vdd gnd cell_6t
Xbit_r36_c124 bl[124] br[124] wl[36] vdd gnd cell_6t
Xbit_r37_c124 bl[124] br[124] wl[37] vdd gnd cell_6t
Xbit_r38_c124 bl[124] br[124] wl[38] vdd gnd cell_6t
Xbit_r39_c124 bl[124] br[124] wl[39] vdd gnd cell_6t
Xbit_r40_c124 bl[124] br[124] wl[40] vdd gnd cell_6t
Xbit_r41_c124 bl[124] br[124] wl[41] vdd gnd cell_6t
Xbit_r42_c124 bl[124] br[124] wl[42] vdd gnd cell_6t
Xbit_r43_c124 bl[124] br[124] wl[43] vdd gnd cell_6t
Xbit_r44_c124 bl[124] br[124] wl[44] vdd gnd cell_6t
Xbit_r45_c124 bl[124] br[124] wl[45] vdd gnd cell_6t
Xbit_r46_c124 bl[124] br[124] wl[46] vdd gnd cell_6t
Xbit_r47_c124 bl[124] br[124] wl[47] vdd gnd cell_6t
Xbit_r48_c124 bl[124] br[124] wl[48] vdd gnd cell_6t
Xbit_r49_c124 bl[124] br[124] wl[49] vdd gnd cell_6t
Xbit_r50_c124 bl[124] br[124] wl[50] vdd gnd cell_6t
Xbit_r51_c124 bl[124] br[124] wl[51] vdd gnd cell_6t
Xbit_r52_c124 bl[124] br[124] wl[52] vdd gnd cell_6t
Xbit_r53_c124 bl[124] br[124] wl[53] vdd gnd cell_6t
Xbit_r54_c124 bl[124] br[124] wl[54] vdd gnd cell_6t
Xbit_r55_c124 bl[124] br[124] wl[55] vdd gnd cell_6t
Xbit_r56_c124 bl[124] br[124] wl[56] vdd gnd cell_6t
Xbit_r57_c124 bl[124] br[124] wl[57] vdd gnd cell_6t
Xbit_r58_c124 bl[124] br[124] wl[58] vdd gnd cell_6t
Xbit_r59_c124 bl[124] br[124] wl[59] vdd gnd cell_6t
Xbit_r60_c124 bl[124] br[124] wl[60] vdd gnd cell_6t
Xbit_r61_c124 bl[124] br[124] wl[61] vdd gnd cell_6t
Xbit_r62_c124 bl[124] br[124] wl[62] vdd gnd cell_6t
Xbit_r63_c124 bl[124] br[124] wl[63] vdd gnd cell_6t
Xbit_r0_c125 bl[125] br[125] wl[0] vdd gnd cell_6t
Xbit_r1_c125 bl[125] br[125] wl[1] vdd gnd cell_6t
Xbit_r2_c125 bl[125] br[125] wl[2] vdd gnd cell_6t
Xbit_r3_c125 bl[125] br[125] wl[3] vdd gnd cell_6t
Xbit_r4_c125 bl[125] br[125] wl[4] vdd gnd cell_6t
Xbit_r5_c125 bl[125] br[125] wl[5] vdd gnd cell_6t
Xbit_r6_c125 bl[125] br[125] wl[6] vdd gnd cell_6t
Xbit_r7_c125 bl[125] br[125] wl[7] vdd gnd cell_6t
Xbit_r8_c125 bl[125] br[125] wl[8] vdd gnd cell_6t
Xbit_r9_c125 bl[125] br[125] wl[9] vdd gnd cell_6t
Xbit_r10_c125 bl[125] br[125] wl[10] vdd gnd cell_6t
Xbit_r11_c125 bl[125] br[125] wl[11] vdd gnd cell_6t
Xbit_r12_c125 bl[125] br[125] wl[12] vdd gnd cell_6t
Xbit_r13_c125 bl[125] br[125] wl[13] vdd gnd cell_6t
Xbit_r14_c125 bl[125] br[125] wl[14] vdd gnd cell_6t
Xbit_r15_c125 bl[125] br[125] wl[15] vdd gnd cell_6t
Xbit_r16_c125 bl[125] br[125] wl[16] vdd gnd cell_6t
Xbit_r17_c125 bl[125] br[125] wl[17] vdd gnd cell_6t
Xbit_r18_c125 bl[125] br[125] wl[18] vdd gnd cell_6t
Xbit_r19_c125 bl[125] br[125] wl[19] vdd gnd cell_6t
Xbit_r20_c125 bl[125] br[125] wl[20] vdd gnd cell_6t
Xbit_r21_c125 bl[125] br[125] wl[21] vdd gnd cell_6t
Xbit_r22_c125 bl[125] br[125] wl[22] vdd gnd cell_6t
Xbit_r23_c125 bl[125] br[125] wl[23] vdd gnd cell_6t
Xbit_r24_c125 bl[125] br[125] wl[24] vdd gnd cell_6t
Xbit_r25_c125 bl[125] br[125] wl[25] vdd gnd cell_6t
Xbit_r26_c125 bl[125] br[125] wl[26] vdd gnd cell_6t
Xbit_r27_c125 bl[125] br[125] wl[27] vdd gnd cell_6t
Xbit_r28_c125 bl[125] br[125] wl[28] vdd gnd cell_6t
Xbit_r29_c125 bl[125] br[125] wl[29] vdd gnd cell_6t
Xbit_r30_c125 bl[125] br[125] wl[30] vdd gnd cell_6t
Xbit_r31_c125 bl[125] br[125] wl[31] vdd gnd cell_6t
Xbit_r32_c125 bl[125] br[125] wl[32] vdd gnd cell_6t
Xbit_r33_c125 bl[125] br[125] wl[33] vdd gnd cell_6t
Xbit_r34_c125 bl[125] br[125] wl[34] vdd gnd cell_6t
Xbit_r35_c125 bl[125] br[125] wl[35] vdd gnd cell_6t
Xbit_r36_c125 bl[125] br[125] wl[36] vdd gnd cell_6t
Xbit_r37_c125 bl[125] br[125] wl[37] vdd gnd cell_6t
Xbit_r38_c125 bl[125] br[125] wl[38] vdd gnd cell_6t
Xbit_r39_c125 bl[125] br[125] wl[39] vdd gnd cell_6t
Xbit_r40_c125 bl[125] br[125] wl[40] vdd gnd cell_6t
Xbit_r41_c125 bl[125] br[125] wl[41] vdd gnd cell_6t
Xbit_r42_c125 bl[125] br[125] wl[42] vdd gnd cell_6t
Xbit_r43_c125 bl[125] br[125] wl[43] vdd gnd cell_6t
Xbit_r44_c125 bl[125] br[125] wl[44] vdd gnd cell_6t
Xbit_r45_c125 bl[125] br[125] wl[45] vdd gnd cell_6t
Xbit_r46_c125 bl[125] br[125] wl[46] vdd gnd cell_6t
Xbit_r47_c125 bl[125] br[125] wl[47] vdd gnd cell_6t
Xbit_r48_c125 bl[125] br[125] wl[48] vdd gnd cell_6t
Xbit_r49_c125 bl[125] br[125] wl[49] vdd gnd cell_6t
Xbit_r50_c125 bl[125] br[125] wl[50] vdd gnd cell_6t
Xbit_r51_c125 bl[125] br[125] wl[51] vdd gnd cell_6t
Xbit_r52_c125 bl[125] br[125] wl[52] vdd gnd cell_6t
Xbit_r53_c125 bl[125] br[125] wl[53] vdd gnd cell_6t
Xbit_r54_c125 bl[125] br[125] wl[54] vdd gnd cell_6t
Xbit_r55_c125 bl[125] br[125] wl[55] vdd gnd cell_6t
Xbit_r56_c125 bl[125] br[125] wl[56] vdd gnd cell_6t
Xbit_r57_c125 bl[125] br[125] wl[57] vdd gnd cell_6t
Xbit_r58_c125 bl[125] br[125] wl[58] vdd gnd cell_6t
Xbit_r59_c125 bl[125] br[125] wl[59] vdd gnd cell_6t
Xbit_r60_c125 bl[125] br[125] wl[60] vdd gnd cell_6t
Xbit_r61_c125 bl[125] br[125] wl[61] vdd gnd cell_6t
Xbit_r62_c125 bl[125] br[125] wl[62] vdd gnd cell_6t
Xbit_r63_c125 bl[125] br[125] wl[63] vdd gnd cell_6t
Xbit_r0_c126 bl[126] br[126] wl[0] vdd gnd cell_6t
Xbit_r1_c126 bl[126] br[126] wl[1] vdd gnd cell_6t
Xbit_r2_c126 bl[126] br[126] wl[2] vdd gnd cell_6t
Xbit_r3_c126 bl[126] br[126] wl[3] vdd gnd cell_6t
Xbit_r4_c126 bl[126] br[126] wl[4] vdd gnd cell_6t
Xbit_r5_c126 bl[126] br[126] wl[5] vdd gnd cell_6t
Xbit_r6_c126 bl[126] br[126] wl[6] vdd gnd cell_6t
Xbit_r7_c126 bl[126] br[126] wl[7] vdd gnd cell_6t
Xbit_r8_c126 bl[126] br[126] wl[8] vdd gnd cell_6t
Xbit_r9_c126 bl[126] br[126] wl[9] vdd gnd cell_6t
Xbit_r10_c126 bl[126] br[126] wl[10] vdd gnd cell_6t
Xbit_r11_c126 bl[126] br[126] wl[11] vdd gnd cell_6t
Xbit_r12_c126 bl[126] br[126] wl[12] vdd gnd cell_6t
Xbit_r13_c126 bl[126] br[126] wl[13] vdd gnd cell_6t
Xbit_r14_c126 bl[126] br[126] wl[14] vdd gnd cell_6t
Xbit_r15_c126 bl[126] br[126] wl[15] vdd gnd cell_6t
Xbit_r16_c126 bl[126] br[126] wl[16] vdd gnd cell_6t
Xbit_r17_c126 bl[126] br[126] wl[17] vdd gnd cell_6t
Xbit_r18_c126 bl[126] br[126] wl[18] vdd gnd cell_6t
Xbit_r19_c126 bl[126] br[126] wl[19] vdd gnd cell_6t
Xbit_r20_c126 bl[126] br[126] wl[20] vdd gnd cell_6t
Xbit_r21_c126 bl[126] br[126] wl[21] vdd gnd cell_6t
Xbit_r22_c126 bl[126] br[126] wl[22] vdd gnd cell_6t
Xbit_r23_c126 bl[126] br[126] wl[23] vdd gnd cell_6t
Xbit_r24_c126 bl[126] br[126] wl[24] vdd gnd cell_6t
Xbit_r25_c126 bl[126] br[126] wl[25] vdd gnd cell_6t
Xbit_r26_c126 bl[126] br[126] wl[26] vdd gnd cell_6t
Xbit_r27_c126 bl[126] br[126] wl[27] vdd gnd cell_6t
Xbit_r28_c126 bl[126] br[126] wl[28] vdd gnd cell_6t
Xbit_r29_c126 bl[126] br[126] wl[29] vdd gnd cell_6t
Xbit_r30_c126 bl[126] br[126] wl[30] vdd gnd cell_6t
Xbit_r31_c126 bl[126] br[126] wl[31] vdd gnd cell_6t
Xbit_r32_c126 bl[126] br[126] wl[32] vdd gnd cell_6t
Xbit_r33_c126 bl[126] br[126] wl[33] vdd gnd cell_6t
Xbit_r34_c126 bl[126] br[126] wl[34] vdd gnd cell_6t
Xbit_r35_c126 bl[126] br[126] wl[35] vdd gnd cell_6t
Xbit_r36_c126 bl[126] br[126] wl[36] vdd gnd cell_6t
Xbit_r37_c126 bl[126] br[126] wl[37] vdd gnd cell_6t
Xbit_r38_c126 bl[126] br[126] wl[38] vdd gnd cell_6t
Xbit_r39_c126 bl[126] br[126] wl[39] vdd gnd cell_6t
Xbit_r40_c126 bl[126] br[126] wl[40] vdd gnd cell_6t
Xbit_r41_c126 bl[126] br[126] wl[41] vdd gnd cell_6t
Xbit_r42_c126 bl[126] br[126] wl[42] vdd gnd cell_6t
Xbit_r43_c126 bl[126] br[126] wl[43] vdd gnd cell_6t
Xbit_r44_c126 bl[126] br[126] wl[44] vdd gnd cell_6t
Xbit_r45_c126 bl[126] br[126] wl[45] vdd gnd cell_6t
Xbit_r46_c126 bl[126] br[126] wl[46] vdd gnd cell_6t
Xbit_r47_c126 bl[126] br[126] wl[47] vdd gnd cell_6t
Xbit_r48_c126 bl[126] br[126] wl[48] vdd gnd cell_6t
Xbit_r49_c126 bl[126] br[126] wl[49] vdd gnd cell_6t
Xbit_r50_c126 bl[126] br[126] wl[50] vdd gnd cell_6t
Xbit_r51_c126 bl[126] br[126] wl[51] vdd gnd cell_6t
Xbit_r52_c126 bl[126] br[126] wl[52] vdd gnd cell_6t
Xbit_r53_c126 bl[126] br[126] wl[53] vdd gnd cell_6t
Xbit_r54_c126 bl[126] br[126] wl[54] vdd gnd cell_6t
Xbit_r55_c126 bl[126] br[126] wl[55] vdd gnd cell_6t
Xbit_r56_c126 bl[126] br[126] wl[56] vdd gnd cell_6t
Xbit_r57_c126 bl[126] br[126] wl[57] vdd gnd cell_6t
Xbit_r58_c126 bl[126] br[126] wl[58] vdd gnd cell_6t
Xbit_r59_c126 bl[126] br[126] wl[59] vdd gnd cell_6t
Xbit_r60_c126 bl[126] br[126] wl[60] vdd gnd cell_6t
Xbit_r61_c126 bl[126] br[126] wl[61] vdd gnd cell_6t
Xbit_r62_c126 bl[126] br[126] wl[62] vdd gnd cell_6t
Xbit_r63_c126 bl[126] br[126] wl[63] vdd gnd cell_6t
Xbit_r0_c127 bl[127] br[127] wl[0] vdd gnd cell_6t
Xbit_r1_c127 bl[127] br[127] wl[1] vdd gnd cell_6t
Xbit_r2_c127 bl[127] br[127] wl[2] vdd gnd cell_6t
Xbit_r3_c127 bl[127] br[127] wl[3] vdd gnd cell_6t
Xbit_r4_c127 bl[127] br[127] wl[4] vdd gnd cell_6t
Xbit_r5_c127 bl[127] br[127] wl[5] vdd gnd cell_6t
Xbit_r6_c127 bl[127] br[127] wl[6] vdd gnd cell_6t
Xbit_r7_c127 bl[127] br[127] wl[7] vdd gnd cell_6t
Xbit_r8_c127 bl[127] br[127] wl[8] vdd gnd cell_6t
Xbit_r9_c127 bl[127] br[127] wl[9] vdd gnd cell_6t
Xbit_r10_c127 bl[127] br[127] wl[10] vdd gnd cell_6t
Xbit_r11_c127 bl[127] br[127] wl[11] vdd gnd cell_6t
Xbit_r12_c127 bl[127] br[127] wl[12] vdd gnd cell_6t
Xbit_r13_c127 bl[127] br[127] wl[13] vdd gnd cell_6t
Xbit_r14_c127 bl[127] br[127] wl[14] vdd gnd cell_6t
Xbit_r15_c127 bl[127] br[127] wl[15] vdd gnd cell_6t
Xbit_r16_c127 bl[127] br[127] wl[16] vdd gnd cell_6t
Xbit_r17_c127 bl[127] br[127] wl[17] vdd gnd cell_6t
Xbit_r18_c127 bl[127] br[127] wl[18] vdd gnd cell_6t
Xbit_r19_c127 bl[127] br[127] wl[19] vdd gnd cell_6t
Xbit_r20_c127 bl[127] br[127] wl[20] vdd gnd cell_6t
Xbit_r21_c127 bl[127] br[127] wl[21] vdd gnd cell_6t
Xbit_r22_c127 bl[127] br[127] wl[22] vdd gnd cell_6t
Xbit_r23_c127 bl[127] br[127] wl[23] vdd gnd cell_6t
Xbit_r24_c127 bl[127] br[127] wl[24] vdd gnd cell_6t
Xbit_r25_c127 bl[127] br[127] wl[25] vdd gnd cell_6t
Xbit_r26_c127 bl[127] br[127] wl[26] vdd gnd cell_6t
Xbit_r27_c127 bl[127] br[127] wl[27] vdd gnd cell_6t
Xbit_r28_c127 bl[127] br[127] wl[28] vdd gnd cell_6t
Xbit_r29_c127 bl[127] br[127] wl[29] vdd gnd cell_6t
Xbit_r30_c127 bl[127] br[127] wl[30] vdd gnd cell_6t
Xbit_r31_c127 bl[127] br[127] wl[31] vdd gnd cell_6t
Xbit_r32_c127 bl[127] br[127] wl[32] vdd gnd cell_6t
Xbit_r33_c127 bl[127] br[127] wl[33] vdd gnd cell_6t
Xbit_r34_c127 bl[127] br[127] wl[34] vdd gnd cell_6t
Xbit_r35_c127 bl[127] br[127] wl[35] vdd gnd cell_6t
Xbit_r36_c127 bl[127] br[127] wl[36] vdd gnd cell_6t
Xbit_r37_c127 bl[127] br[127] wl[37] vdd gnd cell_6t
Xbit_r38_c127 bl[127] br[127] wl[38] vdd gnd cell_6t
Xbit_r39_c127 bl[127] br[127] wl[39] vdd gnd cell_6t
Xbit_r40_c127 bl[127] br[127] wl[40] vdd gnd cell_6t
Xbit_r41_c127 bl[127] br[127] wl[41] vdd gnd cell_6t
Xbit_r42_c127 bl[127] br[127] wl[42] vdd gnd cell_6t
Xbit_r43_c127 bl[127] br[127] wl[43] vdd gnd cell_6t
Xbit_r44_c127 bl[127] br[127] wl[44] vdd gnd cell_6t
Xbit_r45_c127 bl[127] br[127] wl[45] vdd gnd cell_6t
Xbit_r46_c127 bl[127] br[127] wl[46] vdd gnd cell_6t
Xbit_r47_c127 bl[127] br[127] wl[47] vdd gnd cell_6t
Xbit_r48_c127 bl[127] br[127] wl[48] vdd gnd cell_6t
Xbit_r49_c127 bl[127] br[127] wl[49] vdd gnd cell_6t
Xbit_r50_c127 bl[127] br[127] wl[50] vdd gnd cell_6t
Xbit_r51_c127 bl[127] br[127] wl[51] vdd gnd cell_6t
Xbit_r52_c127 bl[127] br[127] wl[52] vdd gnd cell_6t
Xbit_r53_c127 bl[127] br[127] wl[53] vdd gnd cell_6t
Xbit_r54_c127 bl[127] br[127] wl[54] vdd gnd cell_6t
Xbit_r55_c127 bl[127] br[127] wl[55] vdd gnd cell_6t
Xbit_r56_c127 bl[127] br[127] wl[56] vdd gnd cell_6t
Xbit_r57_c127 bl[127] br[127] wl[57] vdd gnd cell_6t
Xbit_r58_c127 bl[127] br[127] wl[58] vdd gnd cell_6t
Xbit_r59_c127 bl[127] br[127] wl[59] vdd gnd cell_6t
Xbit_r60_c127 bl[127] br[127] wl[60] vdd gnd cell_6t
Xbit_r61_c127 bl[127] br[127] wl[61] vdd gnd cell_6t
Xbit_r62_c127 bl[127] br[127] wl[62] vdd gnd cell_6t
Xbit_r63_c127 bl[127] br[127] wl[63] vdd gnd cell_6t
.ENDS bitcell_array

* ptx M{0} {1} p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p

.SUBCKT precharge bl br en vdd
Mlower_pmos bl en BR vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mupper_pmos1 bl en vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mupper_pmos2 br en vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
.ENDS precharge

.SUBCKT precharge_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] bl[8] br[8] bl[9] br[9] bl[10] br[10] bl[11] br[11] bl[12] br[12] bl[13] br[13] bl[14] br[14] bl[15] br[15] bl[16] br[16] bl[17] br[17] bl[18] br[18] bl[19] br[19] bl[20] br[20] bl[21] br[21] bl[22] br[22] bl[23] br[23] bl[24] br[24] bl[25] br[25] bl[26] br[26] bl[27] br[27] bl[28] br[28] bl[29] br[29] bl[30] br[30] bl[31] br[31] bl[32] br[32] bl[33] br[33] bl[34] br[34] bl[35] br[35] bl[36] br[36] bl[37] br[37] bl[38] br[38] bl[39] br[39] bl[40] br[40] bl[41] br[41] bl[42] br[42] bl[43] br[43] bl[44] br[44] bl[45] br[45] bl[46] br[46] bl[47] br[47] bl[48] br[48] bl[49] br[49] bl[50] br[50] bl[51] br[51] bl[52] br[52] bl[53] br[53] bl[54] br[54] bl[55] br[55] bl[56] br[56] bl[57] br[57] bl[58] br[58] bl[59] br[59] bl[60] br[60] bl[61] br[61] bl[62] br[62] bl[63] br[63] bl[64] br[64] bl[65] br[65] bl[66] br[66] bl[67] br[67] bl[68] br[68] bl[69] br[69] bl[70] br[70] bl[71] br[71] bl[72] br[72] bl[73] br[73] bl[74] br[74] bl[75] br[75] bl[76] br[76] bl[77] br[77] bl[78] br[78] bl[79] br[79] bl[80] br[80] bl[81] br[81] bl[82] br[82] bl[83] br[83] bl[84] br[84] bl[85] br[85] bl[86] br[86] bl[87] br[87] bl[88] br[88] bl[89] br[89] bl[90] br[90] bl[91] br[91] bl[92] br[92] bl[93] br[93] bl[94] br[94] bl[95] br[95] bl[96] br[96] bl[97] br[97] bl[98] br[98] bl[99] br[99] bl[100] br[100] bl[101] br[101] bl[102] br[102] bl[103] br[103] bl[104] br[104] bl[105] br[105] bl[106] br[106] bl[107] br[107] bl[108] br[108] bl[109] br[109] bl[110] br[110] bl[111] br[111] bl[112] br[112] bl[113] br[113] bl[114] br[114] bl[115] br[115] bl[116] br[116] bl[117] br[117] bl[118] br[118] bl[119] br[119] bl[120] br[120] bl[121] br[121] bl[122] br[122] bl[123] br[123] bl[124] br[124] bl[125] br[125] bl[126] br[126] bl[127] br[127] en vdd
Xpre_column_0 bl[0] br[0] en vdd precharge
Xpre_column_1 bl[1] br[1] en vdd precharge
Xpre_column_2 bl[2] br[2] en vdd precharge
Xpre_column_3 bl[3] br[3] en vdd precharge
Xpre_column_4 bl[4] br[4] en vdd precharge
Xpre_column_5 bl[5] br[5] en vdd precharge
Xpre_column_6 bl[6] br[6] en vdd precharge
Xpre_column_7 bl[7] br[7] en vdd precharge
Xpre_column_8 bl[8] br[8] en vdd precharge
Xpre_column_9 bl[9] br[9] en vdd precharge
Xpre_column_10 bl[10] br[10] en vdd precharge
Xpre_column_11 bl[11] br[11] en vdd precharge
Xpre_column_12 bl[12] br[12] en vdd precharge
Xpre_column_13 bl[13] br[13] en vdd precharge
Xpre_column_14 bl[14] br[14] en vdd precharge
Xpre_column_15 bl[15] br[15] en vdd precharge
Xpre_column_16 bl[16] br[16] en vdd precharge
Xpre_column_17 bl[17] br[17] en vdd precharge
Xpre_column_18 bl[18] br[18] en vdd precharge
Xpre_column_19 bl[19] br[19] en vdd precharge
Xpre_column_20 bl[20] br[20] en vdd precharge
Xpre_column_21 bl[21] br[21] en vdd precharge
Xpre_column_22 bl[22] br[22] en vdd precharge
Xpre_column_23 bl[23] br[23] en vdd precharge
Xpre_column_24 bl[24] br[24] en vdd precharge
Xpre_column_25 bl[25] br[25] en vdd precharge
Xpre_column_26 bl[26] br[26] en vdd precharge
Xpre_column_27 bl[27] br[27] en vdd precharge
Xpre_column_28 bl[28] br[28] en vdd precharge
Xpre_column_29 bl[29] br[29] en vdd precharge
Xpre_column_30 bl[30] br[30] en vdd precharge
Xpre_column_31 bl[31] br[31] en vdd precharge
Xpre_column_32 bl[32] br[32] en vdd precharge
Xpre_column_33 bl[33] br[33] en vdd precharge
Xpre_column_34 bl[34] br[34] en vdd precharge
Xpre_column_35 bl[35] br[35] en vdd precharge
Xpre_column_36 bl[36] br[36] en vdd precharge
Xpre_column_37 bl[37] br[37] en vdd precharge
Xpre_column_38 bl[38] br[38] en vdd precharge
Xpre_column_39 bl[39] br[39] en vdd precharge
Xpre_column_40 bl[40] br[40] en vdd precharge
Xpre_column_41 bl[41] br[41] en vdd precharge
Xpre_column_42 bl[42] br[42] en vdd precharge
Xpre_column_43 bl[43] br[43] en vdd precharge
Xpre_column_44 bl[44] br[44] en vdd precharge
Xpre_column_45 bl[45] br[45] en vdd precharge
Xpre_column_46 bl[46] br[46] en vdd precharge
Xpre_column_47 bl[47] br[47] en vdd precharge
Xpre_column_48 bl[48] br[48] en vdd precharge
Xpre_column_49 bl[49] br[49] en vdd precharge
Xpre_column_50 bl[50] br[50] en vdd precharge
Xpre_column_51 bl[51] br[51] en vdd precharge
Xpre_column_52 bl[52] br[52] en vdd precharge
Xpre_column_53 bl[53] br[53] en vdd precharge
Xpre_column_54 bl[54] br[54] en vdd precharge
Xpre_column_55 bl[55] br[55] en vdd precharge
Xpre_column_56 bl[56] br[56] en vdd precharge
Xpre_column_57 bl[57] br[57] en vdd precharge
Xpre_column_58 bl[58] br[58] en vdd precharge
Xpre_column_59 bl[59] br[59] en vdd precharge
Xpre_column_60 bl[60] br[60] en vdd precharge
Xpre_column_61 bl[61] br[61] en vdd precharge
Xpre_column_62 bl[62] br[62] en vdd precharge
Xpre_column_63 bl[63] br[63] en vdd precharge
Xpre_column_64 bl[64] br[64] en vdd precharge
Xpre_column_65 bl[65] br[65] en vdd precharge
Xpre_column_66 bl[66] br[66] en vdd precharge
Xpre_column_67 bl[67] br[67] en vdd precharge
Xpre_column_68 bl[68] br[68] en vdd precharge
Xpre_column_69 bl[69] br[69] en vdd precharge
Xpre_column_70 bl[70] br[70] en vdd precharge
Xpre_column_71 bl[71] br[71] en vdd precharge
Xpre_column_72 bl[72] br[72] en vdd precharge
Xpre_column_73 bl[73] br[73] en vdd precharge
Xpre_column_74 bl[74] br[74] en vdd precharge
Xpre_column_75 bl[75] br[75] en vdd precharge
Xpre_column_76 bl[76] br[76] en vdd precharge
Xpre_column_77 bl[77] br[77] en vdd precharge
Xpre_column_78 bl[78] br[78] en vdd precharge
Xpre_column_79 bl[79] br[79] en vdd precharge
Xpre_column_80 bl[80] br[80] en vdd precharge
Xpre_column_81 bl[81] br[81] en vdd precharge
Xpre_column_82 bl[82] br[82] en vdd precharge
Xpre_column_83 bl[83] br[83] en vdd precharge
Xpre_column_84 bl[84] br[84] en vdd precharge
Xpre_column_85 bl[85] br[85] en vdd precharge
Xpre_column_86 bl[86] br[86] en vdd precharge
Xpre_column_87 bl[87] br[87] en vdd precharge
Xpre_column_88 bl[88] br[88] en vdd precharge
Xpre_column_89 bl[89] br[89] en vdd precharge
Xpre_column_90 bl[90] br[90] en vdd precharge
Xpre_column_91 bl[91] br[91] en vdd precharge
Xpre_column_92 bl[92] br[92] en vdd precharge
Xpre_column_93 bl[93] br[93] en vdd precharge
Xpre_column_94 bl[94] br[94] en vdd precharge
Xpre_column_95 bl[95] br[95] en vdd precharge
Xpre_column_96 bl[96] br[96] en vdd precharge
Xpre_column_97 bl[97] br[97] en vdd precharge
Xpre_column_98 bl[98] br[98] en vdd precharge
Xpre_column_99 bl[99] br[99] en vdd precharge
Xpre_column_100 bl[100] br[100] en vdd precharge
Xpre_column_101 bl[101] br[101] en vdd precharge
Xpre_column_102 bl[102] br[102] en vdd precharge
Xpre_column_103 bl[103] br[103] en vdd precharge
Xpre_column_104 bl[104] br[104] en vdd precharge
Xpre_column_105 bl[105] br[105] en vdd precharge
Xpre_column_106 bl[106] br[106] en vdd precharge
Xpre_column_107 bl[107] br[107] en vdd precharge
Xpre_column_108 bl[108] br[108] en vdd precharge
Xpre_column_109 bl[109] br[109] en vdd precharge
Xpre_column_110 bl[110] br[110] en vdd precharge
Xpre_column_111 bl[111] br[111] en vdd precharge
Xpre_column_112 bl[112] br[112] en vdd precharge
Xpre_column_113 bl[113] br[113] en vdd precharge
Xpre_column_114 bl[114] br[114] en vdd precharge
Xpre_column_115 bl[115] br[115] en vdd precharge
Xpre_column_116 bl[116] br[116] en vdd precharge
Xpre_column_117 bl[117] br[117] en vdd precharge
Xpre_column_118 bl[118] br[118] en vdd precharge
Xpre_column_119 bl[119] br[119] en vdd precharge
Xpre_column_120 bl[120] br[120] en vdd precharge
Xpre_column_121 bl[121] br[121] en vdd precharge
Xpre_column_122 bl[122] br[122] en vdd precharge
Xpre_column_123 bl[123] br[123] en vdd precharge
Xpre_column_124 bl[124] br[124] en vdd precharge
Xpre_column_125 bl[125] br[125] en vdd precharge
Xpre_column_126 bl[126] br[126] en vdd precharge
Xpre_column_127 bl[127] br[127] en vdd precharge
.ENDS precharge_array

* ptx M{0} {1} n m=1 w=9.6u l=0.6u pd=20.4u ps=20.4u as=14.4p ad=14.4p

.SUBCKT single_level_column_mux_8 bl br bl_out br_out sel gnd
Mmux_tx1 bl sel bl_out gnd n m=1 w=9.6u l=0.6u pd=20.4u ps=20.4u as=14.4p ad=14.4p
Mmux_tx2 br sel br_out gnd n m=1 w=9.6u l=0.6u pd=20.4u ps=20.4u as=14.4p ad=14.4p
.ENDS single_level_column_mux_8

.SUBCKT columnmux_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] bl[8] br[8] bl[9] br[9] bl[10] br[10] bl[11] br[11] bl[12] br[12] bl[13] br[13] bl[14] br[14] bl[15] br[15] bl[16] br[16] bl[17] br[17] bl[18] br[18] bl[19] br[19] bl[20] br[20] bl[21] br[21] bl[22] br[22] bl[23] br[23] bl[24] br[24] bl[25] br[25] bl[26] br[26] bl[27] br[27] bl[28] br[28] bl[29] br[29] bl[30] br[30] bl[31] br[31] bl[32] br[32] bl[33] br[33] bl[34] br[34] bl[35] br[35] bl[36] br[36] bl[37] br[37] bl[38] br[38] bl[39] br[39] bl[40] br[40] bl[41] br[41] bl[42] br[42] bl[43] br[43] bl[44] br[44] bl[45] br[45] bl[46] br[46] bl[47] br[47] bl[48] br[48] bl[49] br[49] bl[50] br[50] bl[51] br[51] bl[52] br[52] bl[53] br[53] bl[54] br[54] bl[55] br[55] bl[56] br[56] bl[57] br[57] bl[58] br[58] bl[59] br[59] bl[60] br[60] bl[61] br[61] bl[62] br[62] bl[63] br[63] bl[64] br[64] bl[65] br[65] bl[66] br[66] bl[67] br[67] bl[68] br[68] bl[69] br[69] bl[70] br[70] bl[71] br[71] bl[72] br[72] bl[73] br[73] bl[74] br[74] bl[75] br[75] bl[76] br[76] bl[77] br[77] bl[78] br[78] bl[79] br[79] bl[80] br[80] bl[81] br[81] bl[82] br[82] bl[83] br[83] bl[84] br[84] bl[85] br[85] bl[86] br[86] bl[87] br[87] bl[88] br[88] bl[89] br[89] bl[90] br[90] bl[91] br[91] bl[92] br[92] bl[93] br[93] bl[94] br[94] bl[95] br[95] bl[96] br[96] bl[97] br[97] bl[98] br[98] bl[99] br[99] bl[100] br[100] bl[101] br[101] bl[102] br[102] bl[103] br[103] bl[104] br[104] bl[105] br[105] bl[106] br[106] bl[107] br[107] bl[108] br[108] bl[109] br[109] bl[110] br[110] bl[111] br[111] bl[112] br[112] bl[113] br[113] bl[114] br[114] bl[115] br[115] bl[116] br[116] bl[117] br[117] bl[118] br[118] bl[119] br[119] bl[120] br[120] bl[121] br[121] bl[122] br[122] bl[123] br[123] bl[124] br[124] bl[125] br[125] bl[126] br[126] bl[127] br[127] sel[0] sel[1] sel[2] sel[3] bl_out[0] br_out[0] bl_out[1] br_out[1] bl_out[2] br_out[2] bl_out[3] br_out[3] bl_out[4] br_out[4] bl_out[5] br_out[5] bl_out[6] br_out[6] bl_out[7] br_out[7] bl_out[8] br_out[8] bl_out[9] br_out[9] bl_out[10] br_out[10] bl_out[11] br_out[11] bl_out[12] br_out[12] bl_out[13] br_out[13] bl_out[14] br_out[14] bl_out[15] br_out[15] bl_out[16] br_out[16] bl_out[17] br_out[17] bl_out[18] br_out[18] bl_out[19] br_out[19] bl_out[20] br_out[20] bl_out[21] br_out[21] bl_out[22] br_out[22] bl_out[23] br_out[23] bl_out[24] br_out[24] bl_out[25] br_out[25] bl_out[26] br_out[26] bl_out[27] br_out[27] bl_out[28] br_out[28] bl_out[29] br_out[29] bl_out[30] br_out[30] bl_out[31] br_out[31] gnd
XXMUX0 bl[0] br[0] bl_out[0] br_out[0] sel[0] gnd single_level_column_mux_8
XXMUX1 bl[1] br[1] bl_out[0] br_out[0] sel[1] gnd single_level_column_mux_8
XXMUX2 bl[2] br[2] bl_out[0] br_out[0] sel[2] gnd single_level_column_mux_8
XXMUX3 bl[3] br[3] bl_out[0] br_out[0] sel[3] gnd single_level_column_mux_8
XXMUX4 bl[4] br[4] bl_out[1] br_out[1] sel[0] gnd single_level_column_mux_8
XXMUX5 bl[5] br[5] bl_out[1] br_out[1] sel[1] gnd single_level_column_mux_8
XXMUX6 bl[6] br[6] bl_out[1] br_out[1] sel[2] gnd single_level_column_mux_8
XXMUX7 bl[7] br[7] bl_out[1] br_out[1] sel[3] gnd single_level_column_mux_8
XXMUX8 bl[8] br[8] bl_out[2] br_out[2] sel[0] gnd single_level_column_mux_8
XXMUX9 bl[9] br[9] bl_out[2] br_out[2] sel[1] gnd single_level_column_mux_8
XXMUX10 bl[10] br[10] bl_out[2] br_out[2] sel[2] gnd single_level_column_mux_8
XXMUX11 bl[11] br[11] bl_out[2] br_out[2] sel[3] gnd single_level_column_mux_8
XXMUX12 bl[12] br[12] bl_out[3] br_out[3] sel[0] gnd single_level_column_mux_8
XXMUX13 bl[13] br[13] bl_out[3] br_out[3] sel[1] gnd single_level_column_mux_8
XXMUX14 bl[14] br[14] bl_out[3] br_out[3] sel[2] gnd single_level_column_mux_8
XXMUX15 bl[15] br[15] bl_out[3] br_out[3] sel[3] gnd single_level_column_mux_8
XXMUX16 bl[16] br[16] bl_out[4] br_out[4] sel[0] gnd single_level_column_mux_8
XXMUX17 bl[17] br[17] bl_out[4] br_out[4] sel[1] gnd single_level_column_mux_8
XXMUX18 bl[18] br[18] bl_out[4] br_out[4] sel[2] gnd single_level_column_mux_8
XXMUX19 bl[19] br[19] bl_out[4] br_out[4] sel[3] gnd single_level_column_mux_8
XXMUX20 bl[20] br[20] bl_out[5] br_out[5] sel[0] gnd single_level_column_mux_8
XXMUX21 bl[21] br[21] bl_out[5] br_out[5] sel[1] gnd single_level_column_mux_8
XXMUX22 bl[22] br[22] bl_out[5] br_out[5] sel[2] gnd single_level_column_mux_8
XXMUX23 bl[23] br[23] bl_out[5] br_out[5] sel[3] gnd single_level_column_mux_8
XXMUX24 bl[24] br[24] bl_out[6] br_out[6] sel[0] gnd single_level_column_mux_8
XXMUX25 bl[25] br[25] bl_out[6] br_out[6] sel[1] gnd single_level_column_mux_8
XXMUX26 bl[26] br[26] bl_out[6] br_out[6] sel[2] gnd single_level_column_mux_8
XXMUX27 bl[27] br[27] bl_out[6] br_out[6] sel[3] gnd single_level_column_mux_8
XXMUX28 bl[28] br[28] bl_out[7] br_out[7] sel[0] gnd single_level_column_mux_8
XXMUX29 bl[29] br[29] bl_out[7] br_out[7] sel[1] gnd single_level_column_mux_8
XXMUX30 bl[30] br[30] bl_out[7] br_out[7] sel[2] gnd single_level_column_mux_8
XXMUX31 bl[31] br[31] bl_out[7] br_out[7] sel[3] gnd single_level_column_mux_8
XXMUX32 bl[32] br[32] bl_out[8] br_out[8] sel[0] gnd single_level_column_mux_8
XXMUX33 bl[33] br[33] bl_out[8] br_out[8] sel[1] gnd single_level_column_mux_8
XXMUX34 bl[34] br[34] bl_out[8] br_out[8] sel[2] gnd single_level_column_mux_8
XXMUX35 bl[35] br[35] bl_out[8] br_out[8] sel[3] gnd single_level_column_mux_8
XXMUX36 bl[36] br[36] bl_out[9] br_out[9] sel[0] gnd single_level_column_mux_8
XXMUX37 bl[37] br[37] bl_out[9] br_out[9] sel[1] gnd single_level_column_mux_8
XXMUX38 bl[38] br[38] bl_out[9] br_out[9] sel[2] gnd single_level_column_mux_8
XXMUX39 bl[39] br[39] bl_out[9] br_out[9] sel[3] gnd single_level_column_mux_8
XXMUX40 bl[40] br[40] bl_out[10] br_out[10] sel[0] gnd single_level_column_mux_8
XXMUX41 bl[41] br[41] bl_out[10] br_out[10] sel[1] gnd single_level_column_mux_8
XXMUX42 bl[42] br[42] bl_out[10] br_out[10] sel[2] gnd single_level_column_mux_8
XXMUX43 bl[43] br[43] bl_out[10] br_out[10] sel[3] gnd single_level_column_mux_8
XXMUX44 bl[44] br[44] bl_out[11] br_out[11] sel[0] gnd single_level_column_mux_8
XXMUX45 bl[45] br[45] bl_out[11] br_out[11] sel[1] gnd single_level_column_mux_8
XXMUX46 bl[46] br[46] bl_out[11] br_out[11] sel[2] gnd single_level_column_mux_8
XXMUX47 bl[47] br[47] bl_out[11] br_out[11] sel[3] gnd single_level_column_mux_8
XXMUX48 bl[48] br[48] bl_out[12] br_out[12] sel[0] gnd single_level_column_mux_8
XXMUX49 bl[49] br[49] bl_out[12] br_out[12] sel[1] gnd single_level_column_mux_8
XXMUX50 bl[50] br[50] bl_out[12] br_out[12] sel[2] gnd single_level_column_mux_8
XXMUX51 bl[51] br[51] bl_out[12] br_out[12] sel[3] gnd single_level_column_mux_8
XXMUX52 bl[52] br[52] bl_out[13] br_out[13] sel[0] gnd single_level_column_mux_8
XXMUX53 bl[53] br[53] bl_out[13] br_out[13] sel[1] gnd single_level_column_mux_8
XXMUX54 bl[54] br[54] bl_out[13] br_out[13] sel[2] gnd single_level_column_mux_8
XXMUX55 bl[55] br[55] bl_out[13] br_out[13] sel[3] gnd single_level_column_mux_8
XXMUX56 bl[56] br[56] bl_out[14] br_out[14] sel[0] gnd single_level_column_mux_8
XXMUX57 bl[57] br[57] bl_out[14] br_out[14] sel[1] gnd single_level_column_mux_8
XXMUX58 bl[58] br[58] bl_out[14] br_out[14] sel[2] gnd single_level_column_mux_8
XXMUX59 bl[59] br[59] bl_out[14] br_out[14] sel[3] gnd single_level_column_mux_8
XXMUX60 bl[60] br[60] bl_out[15] br_out[15] sel[0] gnd single_level_column_mux_8
XXMUX61 bl[61] br[61] bl_out[15] br_out[15] sel[1] gnd single_level_column_mux_8
XXMUX62 bl[62] br[62] bl_out[15] br_out[15] sel[2] gnd single_level_column_mux_8
XXMUX63 bl[63] br[63] bl_out[15] br_out[15] sel[3] gnd single_level_column_mux_8
XXMUX64 bl[64] br[64] bl_out[16] br_out[16] sel[0] gnd single_level_column_mux_8
XXMUX65 bl[65] br[65] bl_out[16] br_out[16] sel[1] gnd single_level_column_mux_8
XXMUX66 bl[66] br[66] bl_out[16] br_out[16] sel[2] gnd single_level_column_mux_8
XXMUX67 bl[67] br[67] bl_out[16] br_out[16] sel[3] gnd single_level_column_mux_8
XXMUX68 bl[68] br[68] bl_out[17] br_out[17] sel[0] gnd single_level_column_mux_8
XXMUX69 bl[69] br[69] bl_out[17] br_out[17] sel[1] gnd single_level_column_mux_8
XXMUX70 bl[70] br[70] bl_out[17] br_out[17] sel[2] gnd single_level_column_mux_8
XXMUX71 bl[71] br[71] bl_out[17] br_out[17] sel[3] gnd single_level_column_mux_8
XXMUX72 bl[72] br[72] bl_out[18] br_out[18] sel[0] gnd single_level_column_mux_8
XXMUX73 bl[73] br[73] bl_out[18] br_out[18] sel[1] gnd single_level_column_mux_8
XXMUX74 bl[74] br[74] bl_out[18] br_out[18] sel[2] gnd single_level_column_mux_8
XXMUX75 bl[75] br[75] bl_out[18] br_out[18] sel[3] gnd single_level_column_mux_8
XXMUX76 bl[76] br[76] bl_out[19] br_out[19] sel[0] gnd single_level_column_mux_8
XXMUX77 bl[77] br[77] bl_out[19] br_out[19] sel[1] gnd single_level_column_mux_8
XXMUX78 bl[78] br[78] bl_out[19] br_out[19] sel[2] gnd single_level_column_mux_8
XXMUX79 bl[79] br[79] bl_out[19] br_out[19] sel[3] gnd single_level_column_mux_8
XXMUX80 bl[80] br[80] bl_out[20] br_out[20] sel[0] gnd single_level_column_mux_8
XXMUX81 bl[81] br[81] bl_out[20] br_out[20] sel[1] gnd single_level_column_mux_8
XXMUX82 bl[82] br[82] bl_out[20] br_out[20] sel[2] gnd single_level_column_mux_8
XXMUX83 bl[83] br[83] bl_out[20] br_out[20] sel[3] gnd single_level_column_mux_8
XXMUX84 bl[84] br[84] bl_out[21] br_out[21] sel[0] gnd single_level_column_mux_8
XXMUX85 bl[85] br[85] bl_out[21] br_out[21] sel[1] gnd single_level_column_mux_8
XXMUX86 bl[86] br[86] bl_out[21] br_out[21] sel[2] gnd single_level_column_mux_8
XXMUX87 bl[87] br[87] bl_out[21] br_out[21] sel[3] gnd single_level_column_mux_8
XXMUX88 bl[88] br[88] bl_out[22] br_out[22] sel[0] gnd single_level_column_mux_8
XXMUX89 bl[89] br[89] bl_out[22] br_out[22] sel[1] gnd single_level_column_mux_8
XXMUX90 bl[90] br[90] bl_out[22] br_out[22] sel[2] gnd single_level_column_mux_8
XXMUX91 bl[91] br[91] bl_out[22] br_out[22] sel[3] gnd single_level_column_mux_8
XXMUX92 bl[92] br[92] bl_out[23] br_out[23] sel[0] gnd single_level_column_mux_8
XXMUX93 bl[93] br[93] bl_out[23] br_out[23] sel[1] gnd single_level_column_mux_8
XXMUX94 bl[94] br[94] bl_out[23] br_out[23] sel[2] gnd single_level_column_mux_8
XXMUX95 bl[95] br[95] bl_out[23] br_out[23] sel[3] gnd single_level_column_mux_8
XXMUX96 bl[96] br[96] bl_out[24] br_out[24] sel[0] gnd single_level_column_mux_8
XXMUX97 bl[97] br[97] bl_out[24] br_out[24] sel[1] gnd single_level_column_mux_8
XXMUX98 bl[98] br[98] bl_out[24] br_out[24] sel[2] gnd single_level_column_mux_8
XXMUX99 bl[99] br[99] bl_out[24] br_out[24] sel[3] gnd single_level_column_mux_8
XXMUX100 bl[100] br[100] bl_out[25] br_out[25] sel[0] gnd single_level_column_mux_8
XXMUX101 bl[101] br[101] bl_out[25] br_out[25] sel[1] gnd single_level_column_mux_8
XXMUX102 bl[102] br[102] bl_out[25] br_out[25] sel[2] gnd single_level_column_mux_8
XXMUX103 bl[103] br[103] bl_out[25] br_out[25] sel[3] gnd single_level_column_mux_8
XXMUX104 bl[104] br[104] bl_out[26] br_out[26] sel[0] gnd single_level_column_mux_8
XXMUX105 bl[105] br[105] bl_out[26] br_out[26] sel[1] gnd single_level_column_mux_8
XXMUX106 bl[106] br[106] bl_out[26] br_out[26] sel[2] gnd single_level_column_mux_8
XXMUX107 bl[107] br[107] bl_out[26] br_out[26] sel[3] gnd single_level_column_mux_8
XXMUX108 bl[108] br[108] bl_out[27] br_out[27] sel[0] gnd single_level_column_mux_8
XXMUX109 bl[109] br[109] bl_out[27] br_out[27] sel[1] gnd single_level_column_mux_8
XXMUX110 bl[110] br[110] bl_out[27] br_out[27] sel[2] gnd single_level_column_mux_8
XXMUX111 bl[111] br[111] bl_out[27] br_out[27] sel[3] gnd single_level_column_mux_8
XXMUX112 bl[112] br[112] bl_out[28] br_out[28] sel[0] gnd single_level_column_mux_8
XXMUX113 bl[113] br[113] bl_out[28] br_out[28] sel[1] gnd single_level_column_mux_8
XXMUX114 bl[114] br[114] bl_out[28] br_out[28] sel[2] gnd single_level_column_mux_8
XXMUX115 bl[115] br[115] bl_out[28] br_out[28] sel[3] gnd single_level_column_mux_8
XXMUX116 bl[116] br[116] bl_out[29] br_out[29] sel[0] gnd single_level_column_mux_8
XXMUX117 bl[117] br[117] bl_out[29] br_out[29] sel[1] gnd single_level_column_mux_8
XXMUX118 bl[118] br[118] bl_out[29] br_out[29] sel[2] gnd single_level_column_mux_8
XXMUX119 bl[119] br[119] bl_out[29] br_out[29] sel[3] gnd single_level_column_mux_8
XXMUX120 bl[120] br[120] bl_out[30] br_out[30] sel[0] gnd single_level_column_mux_8
XXMUX121 bl[121] br[121] bl_out[30] br_out[30] sel[1] gnd single_level_column_mux_8
XXMUX122 bl[122] br[122] bl_out[30] br_out[30] sel[2] gnd single_level_column_mux_8
XXMUX123 bl[123] br[123] bl_out[30] br_out[30] sel[3] gnd single_level_column_mux_8
XXMUX124 bl[124] br[124] bl_out[31] br_out[31] sel[0] gnd single_level_column_mux_8
XXMUX125 bl[125] br[125] bl_out[31] br_out[31] sel[1] gnd single_level_column_mux_8
XXMUX126 bl[126] br[126] bl_out[31] br_out[31] sel[2] gnd single_level_column_mux_8
XXMUX127 bl[127] br[127] bl_out[31] br_out[31] sel[3] gnd single_level_column_mux_8
.ENDS columnmux_array
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


.SUBCKT sense_amp_array data[0] bl[0] br[0] data[1] bl[4] br[4] data[2] bl[8] br[8] data[3] bl[12] br[12] data[4] bl[16] br[16] data[5] bl[20] br[20] data[6] bl[24] br[24] data[7] bl[28] br[28] data[8] bl[32] br[32] data[9] bl[36] br[36] data[10] bl[40] br[40] data[11] bl[44] br[44] data[12] bl[48] br[48] data[13] bl[52] br[52] data[14] bl[56] br[56] data[15] bl[60] br[60] data[16] bl[64] br[64] data[17] bl[68] br[68] data[18] bl[72] br[72] data[19] bl[76] br[76] data[20] bl[80] br[80] data[21] bl[84] br[84] data[22] bl[88] br[88] data[23] bl[92] br[92] data[24] bl[96] br[96] data[25] bl[100] br[100] data[26] bl[104] br[104] data[27] bl[108] br[108] data[28] bl[112] br[112] data[29] bl[116] br[116] data[30] bl[120] br[120] data[31] bl[124] br[124] en vdd gnd
Xsa_d0 bl[0] br[0] data[0] en vdd gnd sense_amp
Xsa_d4 bl[4] br[4] data[1] en vdd gnd sense_amp
Xsa_d8 bl[8] br[8] data[2] en vdd gnd sense_amp
Xsa_d12 bl[12] br[12] data[3] en vdd gnd sense_amp
Xsa_d16 bl[16] br[16] data[4] en vdd gnd sense_amp
Xsa_d20 bl[20] br[20] data[5] en vdd gnd sense_amp
Xsa_d24 bl[24] br[24] data[6] en vdd gnd sense_amp
Xsa_d28 bl[28] br[28] data[7] en vdd gnd sense_amp
Xsa_d32 bl[32] br[32] data[8] en vdd gnd sense_amp
Xsa_d36 bl[36] br[36] data[9] en vdd gnd sense_amp
Xsa_d40 bl[40] br[40] data[10] en vdd gnd sense_amp
Xsa_d44 bl[44] br[44] data[11] en vdd gnd sense_amp
Xsa_d48 bl[48] br[48] data[12] en vdd gnd sense_amp
Xsa_d52 bl[52] br[52] data[13] en vdd gnd sense_amp
Xsa_d56 bl[56] br[56] data[14] en vdd gnd sense_amp
Xsa_d60 bl[60] br[60] data[15] en vdd gnd sense_amp
Xsa_d64 bl[64] br[64] data[16] en vdd gnd sense_amp
Xsa_d68 bl[68] br[68] data[17] en vdd gnd sense_amp
Xsa_d72 bl[72] br[72] data[18] en vdd gnd sense_amp
Xsa_d76 bl[76] br[76] data[19] en vdd gnd sense_amp
Xsa_d80 bl[80] br[80] data[20] en vdd gnd sense_amp
Xsa_d84 bl[84] br[84] data[21] en vdd gnd sense_amp
Xsa_d88 bl[88] br[88] data[22] en vdd gnd sense_amp
Xsa_d92 bl[92] br[92] data[23] en vdd gnd sense_amp
Xsa_d96 bl[96] br[96] data[24] en vdd gnd sense_amp
Xsa_d100 bl[100] br[100] data[25] en vdd gnd sense_amp
Xsa_d104 bl[104] br[104] data[26] en vdd gnd sense_amp
Xsa_d108 bl[108] br[108] data[27] en vdd gnd sense_amp
Xsa_d112 bl[112] br[112] data[28] en vdd gnd sense_amp
Xsa_d116 bl[116] br[116] data[29] en vdd gnd sense_amp
Xsa_d120 bl[120] br[120] data[30] en vdd gnd sense_amp
Xsa_d124 bl[124] br[124] data[31] en vdd gnd sense_amp
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


.SUBCKT write_driver_array data[0] data[1] data[2] data[3] data[4] data[5] data[6] data[7] data[8] data[9] data[10] data[11] data[12] data[13] data[14] data[15] data[16] data[17] data[18] data[19] data[20] data[21] data[22] data[23] data[24] data[25] data[26] data[27] data[28] data[29] data[30] data[31] bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] bl[8] br[8] bl[9] br[9] bl[10] br[10] bl[11] br[11] bl[12] br[12] bl[13] br[13] bl[14] br[14] bl[15] br[15] bl[16] br[16] bl[17] br[17] bl[18] br[18] bl[19] br[19] bl[20] br[20] bl[21] br[21] bl[22] br[22] bl[23] br[23] bl[24] br[24] bl[25] br[25] bl[26] br[26] bl[27] br[27] bl[28] br[28] bl[29] br[29] bl[30] br[30] bl[31] br[31] en vdd gnd
XXwrite_driver0 data[0] bl[0] br[0] en vdd gnd write_driver
XXwrite_driver4 data[1] bl[1] br[1] en vdd gnd write_driver
XXwrite_driver8 data[2] bl[2] br[2] en vdd gnd write_driver
XXwrite_driver12 data[3] bl[3] br[3] en vdd gnd write_driver
XXwrite_driver16 data[4] bl[4] br[4] en vdd gnd write_driver
XXwrite_driver20 data[5] bl[5] br[5] en vdd gnd write_driver
XXwrite_driver24 data[6] bl[6] br[6] en vdd gnd write_driver
XXwrite_driver28 data[7] bl[7] br[7] en vdd gnd write_driver
XXwrite_driver32 data[8] bl[8] br[8] en vdd gnd write_driver
XXwrite_driver36 data[9] bl[9] br[9] en vdd gnd write_driver
XXwrite_driver40 data[10] bl[10] br[10] en vdd gnd write_driver
XXwrite_driver44 data[11] bl[11] br[11] en vdd gnd write_driver
XXwrite_driver48 data[12] bl[12] br[12] en vdd gnd write_driver
XXwrite_driver52 data[13] bl[13] br[13] en vdd gnd write_driver
XXwrite_driver56 data[14] bl[14] br[14] en vdd gnd write_driver
XXwrite_driver60 data[15] bl[15] br[15] en vdd gnd write_driver
XXwrite_driver64 data[16] bl[16] br[16] en vdd gnd write_driver
XXwrite_driver68 data[17] bl[17] br[17] en vdd gnd write_driver
XXwrite_driver72 data[18] bl[18] br[18] en vdd gnd write_driver
XXwrite_driver76 data[19] bl[19] br[19] en vdd gnd write_driver
XXwrite_driver80 data[20] bl[20] br[20] en vdd gnd write_driver
XXwrite_driver84 data[21] bl[21] br[21] en vdd gnd write_driver
XXwrite_driver88 data[22] bl[22] br[22] en vdd gnd write_driver
XXwrite_driver92 data[23] bl[23] br[23] en vdd gnd write_driver
XXwrite_driver96 data[24] bl[24] br[24] en vdd gnd write_driver
XXwrite_driver100 data[25] bl[25] br[25] en vdd gnd write_driver
XXwrite_driver104 data[26] bl[26] br[26] en vdd gnd write_driver
XXwrite_driver108 data[27] bl[27] br[27] en vdd gnd write_driver
XXwrite_driver112 data[28] bl[28] br[28] en vdd gnd write_driver
XXwrite_driver116 data[29] bl[29] br[29] en vdd gnd write_driver
XXwrite_driver120 data[30] bl[30] br[30] en vdd gnd write_driver
XXwrite_driver124 data[31] bl[31] br[31] en vdd gnd write_driver
.ENDS write_driver_array

.SUBCKT pinv_8 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.6u ps=3.6u as=1.8p ad=1.8p
.ENDS pinv_8

.SUBCKT pnand2_2 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
.ENDS pnand2_2

.SUBCKT pnand3_2 A B C Z vdd gnd
Mpnand3_pmos1 vdd A Z vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand3_pmos2 Z B vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand3_pmos3 Z C vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand3_nmos1 Z C net1 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand3_nmos2 net1 B net2 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand3_nmos3 net2 A gnd gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
.ENDS pnand3_2

.SUBCKT pinv_9 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.6u ps=3.6u as=1.8p ad=1.8p
.ENDS pinv_9

.SUBCKT pnand2_3 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
.ENDS pnand2_3

.SUBCKT pre2x4 in[0] in[1] out[0] out[1] out[2] out[3] vdd gnd
XXpre_inv[0] in[0] inbar[0] vdd gnd pinv_9
XXpre_inv[1] in[1] inbar[1] vdd gnd pinv_9
XXpre_nand_inv[0] Z[0] out[0] vdd gnd pinv_9
XXpre_nand_inv[1] Z[1] out[1] vdd gnd pinv_9
XXpre_nand_inv[2] Z[2] out[2] vdd gnd pinv_9
XXpre_nand_inv[3] Z[3] out[3] vdd gnd pinv_9
XXpre2x4_nand[0] inbar[0] inbar[1] Z[0] vdd gnd pnand2_3
XXpre2x4_nand[1] in[0] inbar[1] Z[1] vdd gnd pnand2_3
XXpre2x4_nand[2] inbar[0] in[1] Z[2] vdd gnd pnand2_3
XXpre2x4_nand[3] in[0] in[1] Z[3] vdd gnd pnand2_3
.ENDS pre2x4

.SUBCKT pinv_10 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.6u ps=3.6u as=1.8p ad=1.8p
.ENDS pinv_10

.SUBCKT pnand3_3 A B C Z vdd gnd
Mpnand3_pmos1 vdd A Z vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand3_pmos2 Z B vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand3_pmos3 Z C vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand3_nmos1 Z C net1 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand3_nmos2 net1 B net2 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand3_nmos3 net2 A gnd gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
.ENDS pnand3_3

.SUBCKT pre3x8 in[0] in[1] in[2] out[0] out[1] out[2] out[3] out[4] out[5] out[6] out[7] vdd gnd
XXpre_inv[0] in[0] inbar[0] vdd gnd pinv_10
XXpre_inv[1] in[1] inbar[1] vdd gnd pinv_10
XXpre_inv[2] in[2] inbar[2] vdd gnd pinv_10
XXpre_nand_inv[0] Z[0] out[0] vdd gnd pinv_10
XXpre_nand_inv[1] Z[1] out[1] vdd gnd pinv_10
XXpre_nand_inv[2] Z[2] out[2] vdd gnd pinv_10
XXpre_nand_inv[3] Z[3] out[3] vdd gnd pinv_10
XXpre_nand_inv[4] Z[4] out[4] vdd gnd pinv_10
XXpre_nand_inv[5] Z[5] out[5] vdd gnd pinv_10
XXpre_nand_inv[6] Z[6] out[6] vdd gnd pinv_10
XXpre_nand_inv[7] Z[7] out[7] vdd gnd pinv_10
XXpre3x8_nand[0] inbar[0] inbar[1] inbar[2] Z[0] vdd gnd pnand3_3
XXpre3x8_nand[1] in[0] inbar[1] inbar[2] Z[1] vdd gnd pnand3_3
XXpre3x8_nand[2] inbar[0] in[1] inbar[2] Z[2] vdd gnd pnand3_3
XXpre3x8_nand[3] in[0] in[1] inbar[2] Z[3] vdd gnd pnand3_3
XXpre3x8_nand[4] inbar[0] inbar[1] in[2] Z[4] vdd gnd pnand3_3
XXpre3x8_nand[5] in[0] inbar[1] in[2] Z[5] vdd gnd pnand3_3
XXpre3x8_nand[6] inbar[0] in[1] in[2] Z[6] vdd gnd pnand3_3
XXpre3x8_nand[7] in[0] in[1] in[2] Z[7] vdd gnd pnand3_3
.ENDS pre3x8

.SUBCKT hierarchical_decoder_64rows A[0] A[1] A[2] A[3] A[4] A[5] decode[0] decode[1] decode[2] decode[3] decode[4] decode[5] decode[6] decode[7] decode[8] decode[9] decode[10] decode[11] decode[12] decode[13] decode[14] decode[15] decode[16] decode[17] decode[18] decode[19] decode[20] decode[21] decode[22] decode[23] decode[24] decode[25] decode[26] decode[27] decode[28] decode[29] decode[30] decode[31] decode[32] decode[33] decode[34] decode[35] decode[36] decode[37] decode[38] decode[39] decode[40] decode[41] decode[42] decode[43] decode[44] decode[45] decode[46] decode[47] decode[48] decode[49] decode[50] decode[51] decode[52] decode[53] decode[54] decode[55] decode[56] decode[57] decode[58] decode[59] decode[60] decode[61] decode[62] decode[63] vdd gnd
Xpre[0] A[0] A[1] out[0] out[1] out[2] out[3] vdd gnd pre2x4
Xpre[1] A[2] A[3] out[4] out[5] out[6] out[7] vdd gnd pre2x4
Xpre[2] A[4] A[5] out[8] out[9] out[10] out[11] vdd gnd pre2x4
XDEC_NAND[0] out[0] out[4] out[8] Z[0] vdd gnd pnand3_2
XDEC_NAND[1] out[0] out[4] out[9] Z[1] vdd gnd pnand3_2
XDEC_NAND[2] out[0] out[4] out[10] Z[2] vdd gnd pnand3_2
XDEC_NAND[3] out[0] out[4] out[11] Z[3] vdd gnd pnand3_2
XDEC_NAND[4] out[0] out[5] out[8] Z[4] vdd gnd pnand3_2
XDEC_NAND[5] out[0] out[5] out[9] Z[5] vdd gnd pnand3_2
XDEC_NAND[6] out[0] out[5] out[10] Z[6] vdd gnd pnand3_2
XDEC_NAND[7] out[0] out[5] out[11] Z[7] vdd gnd pnand3_2
XDEC_NAND[8] out[0] out[6] out[8] Z[8] vdd gnd pnand3_2
XDEC_NAND[9] out[0] out[6] out[9] Z[9] vdd gnd pnand3_2
XDEC_NAND[10] out[0] out[6] out[10] Z[10] vdd gnd pnand3_2
XDEC_NAND[11] out[0] out[6] out[11] Z[11] vdd gnd pnand3_2
XDEC_NAND[12] out[0] out[7] out[8] Z[12] vdd gnd pnand3_2
XDEC_NAND[13] out[0] out[7] out[9] Z[13] vdd gnd pnand3_2
XDEC_NAND[14] out[0] out[7] out[10] Z[14] vdd gnd pnand3_2
XDEC_NAND[15] out[0] out[7] out[11] Z[15] vdd gnd pnand3_2
XDEC_NAND[16] out[1] out[4] out[8] Z[16] vdd gnd pnand3_2
XDEC_NAND[17] out[1] out[4] out[9] Z[17] vdd gnd pnand3_2
XDEC_NAND[18] out[1] out[4] out[10] Z[18] vdd gnd pnand3_2
XDEC_NAND[19] out[1] out[4] out[11] Z[19] vdd gnd pnand3_2
XDEC_NAND[20] out[1] out[5] out[8] Z[20] vdd gnd pnand3_2
XDEC_NAND[21] out[1] out[5] out[9] Z[21] vdd gnd pnand3_2
XDEC_NAND[22] out[1] out[5] out[10] Z[22] vdd gnd pnand3_2
XDEC_NAND[23] out[1] out[5] out[11] Z[23] vdd gnd pnand3_2
XDEC_NAND[24] out[1] out[6] out[8] Z[24] vdd gnd pnand3_2
XDEC_NAND[25] out[1] out[6] out[9] Z[25] vdd gnd pnand3_2
XDEC_NAND[26] out[1] out[6] out[10] Z[26] vdd gnd pnand3_2
XDEC_NAND[27] out[1] out[6] out[11] Z[27] vdd gnd pnand3_2
XDEC_NAND[28] out[1] out[7] out[8] Z[28] vdd gnd pnand3_2
XDEC_NAND[29] out[1] out[7] out[9] Z[29] vdd gnd pnand3_2
XDEC_NAND[30] out[1] out[7] out[10] Z[30] vdd gnd pnand3_2
XDEC_NAND[31] out[1] out[7] out[11] Z[31] vdd gnd pnand3_2
XDEC_NAND[32] out[2] out[4] out[8] Z[32] vdd gnd pnand3_2
XDEC_NAND[33] out[2] out[4] out[9] Z[33] vdd gnd pnand3_2
XDEC_NAND[34] out[2] out[4] out[10] Z[34] vdd gnd pnand3_2
XDEC_NAND[35] out[2] out[4] out[11] Z[35] vdd gnd pnand3_2
XDEC_NAND[36] out[2] out[5] out[8] Z[36] vdd gnd pnand3_2
XDEC_NAND[37] out[2] out[5] out[9] Z[37] vdd gnd pnand3_2
XDEC_NAND[38] out[2] out[5] out[10] Z[38] vdd gnd pnand3_2
XDEC_NAND[39] out[2] out[5] out[11] Z[39] vdd gnd pnand3_2
XDEC_NAND[40] out[2] out[6] out[8] Z[40] vdd gnd pnand3_2
XDEC_NAND[41] out[2] out[6] out[9] Z[41] vdd gnd pnand3_2
XDEC_NAND[42] out[2] out[6] out[10] Z[42] vdd gnd pnand3_2
XDEC_NAND[43] out[2] out[6] out[11] Z[43] vdd gnd pnand3_2
XDEC_NAND[44] out[2] out[7] out[8] Z[44] vdd gnd pnand3_2
XDEC_NAND[45] out[2] out[7] out[9] Z[45] vdd gnd pnand3_2
XDEC_NAND[46] out[2] out[7] out[10] Z[46] vdd gnd pnand3_2
XDEC_NAND[47] out[2] out[7] out[11] Z[47] vdd gnd pnand3_2
XDEC_NAND[48] out[3] out[4] out[8] Z[48] vdd gnd pnand3_2
XDEC_NAND[49] out[3] out[4] out[9] Z[49] vdd gnd pnand3_2
XDEC_NAND[50] out[3] out[4] out[10] Z[50] vdd gnd pnand3_2
XDEC_NAND[51] out[3] out[4] out[11] Z[51] vdd gnd pnand3_2
XDEC_NAND[52] out[3] out[5] out[8] Z[52] vdd gnd pnand3_2
XDEC_NAND[53] out[3] out[5] out[9] Z[53] vdd gnd pnand3_2
XDEC_NAND[54] out[3] out[5] out[10] Z[54] vdd gnd pnand3_2
XDEC_NAND[55] out[3] out[5] out[11] Z[55] vdd gnd pnand3_2
XDEC_NAND[56] out[3] out[6] out[8] Z[56] vdd gnd pnand3_2
XDEC_NAND[57] out[3] out[6] out[9] Z[57] vdd gnd pnand3_2
XDEC_NAND[58] out[3] out[6] out[10] Z[58] vdd gnd pnand3_2
XDEC_NAND[59] out[3] out[6] out[11] Z[59] vdd gnd pnand3_2
XDEC_NAND[60] out[3] out[7] out[8] Z[60] vdd gnd pnand3_2
XDEC_NAND[61] out[3] out[7] out[9] Z[61] vdd gnd pnand3_2
XDEC_NAND[62] out[3] out[7] out[10] Z[62] vdd gnd pnand3_2
XDEC_NAND[63] out[3] out[7] out[11] Z[63] vdd gnd pnand3_2
XDEC_INV_[0] Z[0] decode[0] vdd gnd pinv_8
XDEC_INV_[1] Z[1] decode[1] vdd gnd pinv_8
XDEC_INV_[2] Z[2] decode[2] vdd gnd pinv_8
XDEC_INV_[3] Z[3] decode[3] vdd gnd pinv_8
XDEC_INV_[4] Z[4] decode[4] vdd gnd pinv_8
XDEC_INV_[5] Z[5] decode[5] vdd gnd pinv_8
XDEC_INV_[6] Z[6] decode[6] vdd gnd pinv_8
XDEC_INV_[7] Z[7] decode[7] vdd gnd pinv_8
XDEC_INV_[8] Z[8] decode[8] vdd gnd pinv_8
XDEC_INV_[9] Z[9] decode[9] vdd gnd pinv_8
XDEC_INV_[10] Z[10] decode[10] vdd gnd pinv_8
XDEC_INV_[11] Z[11] decode[11] vdd gnd pinv_8
XDEC_INV_[12] Z[12] decode[12] vdd gnd pinv_8
XDEC_INV_[13] Z[13] decode[13] vdd gnd pinv_8
XDEC_INV_[14] Z[14] decode[14] vdd gnd pinv_8
XDEC_INV_[15] Z[15] decode[15] vdd gnd pinv_8
XDEC_INV_[16] Z[16] decode[16] vdd gnd pinv_8
XDEC_INV_[17] Z[17] decode[17] vdd gnd pinv_8
XDEC_INV_[18] Z[18] decode[18] vdd gnd pinv_8
XDEC_INV_[19] Z[19] decode[19] vdd gnd pinv_8
XDEC_INV_[20] Z[20] decode[20] vdd gnd pinv_8
XDEC_INV_[21] Z[21] decode[21] vdd gnd pinv_8
XDEC_INV_[22] Z[22] decode[22] vdd gnd pinv_8
XDEC_INV_[23] Z[23] decode[23] vdd gnd pinv_8
XDEC_INV_[24] Z[24] decode[24] vdd gnd pinv_8
XDEC_INV_[25] Z[25] decode[25] vdd gnd pinv_8
XDEC_INV_[26] Z[26] decode[26] vdd gnd pinv_8
XDEC_INV_[27] Z[27] decode[27] vdd gnd pinv_8
XDEC_INV_[28] Z[28] decode[28] vdd gnd pinv_8
XDEC_INV_[29] Z[29] decode[29] vdd gnd pinv_8
XDEC_INV_[30] Z[30] decode[30] vdd gnd pinv_8
XDEC_INV_[31] Z[31] decode[31] vdd gnd pinv_8
XDEC_INV_[32] Z[32] decode[32] vdd gnd pinv_8
XDEC_INV_[33] Z[33] decode[33] vdd gnd pinv_8
XDEC_INV_[34] Z[34] decode[34] vdd gnd pinv_8
XDEC_INV_[35] Z[35] decode[35] vdd gnd pinv_8
XDEC_INV_[36] Z[36] decode[36] vdd gnd pinv_8
XDEC_INV_[37] Z[37] decode[37] vdd gnd pinv_8
XDEC_INV_[38] Z[38] decode[38] vdd gnd pinv_8
XDEC_INV_[39] Z[39] decode[39] vdd gnd pinv_8
XDEC_INV_[40] Z[40] decode[40] vdd gnd pinv_8
XDEC_INV_[41] Z[41] decode[41] vdd gnd pinv_8
XDEC_INV_[42] Z[42] decode[42] vdd gnd pinv_8
XDEC_INV_[43] Z[43] decode[43] vdd gnd pinv_8
XDEC_INV_[44] Z[44] decode[44] vdd gnd pinv_8
XDEC_INV_[45] Z[45] decode[45] vdd gnd pinv_8
XDEC_INV_[46] Z[46] decode[46] vdd gnd pinv_8
XDEC_INV_[47] Z[47] decode[47] vdd gnd pinv_8
XDEC_INV_[48] Z[48] decode[48] vdd gnd pinv_8
XDEC_INV_[49] Z[49] decode[49] vdd gnd pinv_8
XDEC_INV_[50] Z[50] decode[50] vdd gnd pinv_8
XDEC_INV_[51] Z[51] decode[51] vdd gnd pinv_8
XDEC_INV_[52] Z[52] decode[52] vdd gnd pinv_8
XDEC_INV_[53] Z[53] decode[53] vdd gnd pinv_8
XDEC_INV_[54] Z[54] decode[54] vdd gnd pinv_8
XDEC_INV_[55] Z[55] decode[55] vdd gnd pinv_8
XDEC_INV_[56] Z[56] decode[56] vdd gnd pinv_8
XDEC_INV_[57] Z[57] decode[57] vdd gnd pinv_8
XDEC_INV_[58] Z[58] decode[58] vdd gnd pinv_8
XDEC_INV_[59] Z[59] decode[59] vdd gnd pinv_8
XDEC_INV_[60] Z[60] decode[60] vdd gnd pinv_8
XDEC_INV_[61] Z[61] decode[61] vdd gnd pinv_8
XDEC_INV_[62] Z[62] decode[62] vdd gnd pinv_8
XDEC_INV_[63] Z[63] decode[63] vdd gnd pinv_8
.ENDS hierarchical_decoder_64rows

.SUBCKT msf_address din[0] din[1] din[2] din[3] din[4] din[5] din[6] din[7] dout[0] dout_bar[0] dout[1] dout_bar[1] dout[2] dout_bar[2] dout[3] dout_bar[3] dout[4] dout_bar[4] dout[5] dout_bar[5] dout[6] dout_bar[6] dout[7] dout_bar[7] clk vdd gnd
XXdff0 din[0] dout[0] dout_bar[0] clk vdd gnd ms_flop
XXdff1 din[1] dout[1] dout_bar[1] clk vdd gnd ms_flop
XXdff2 din[2] dout[2] dout_bar[2] clk vdd gnd ms_flop
XXdff3 din[3] dout[3] dout_bar[3] clk vdd gnd ms_flop
XXdff4 din[4] dout[4] dout_bar[4] clk vdd gnd ms_flop
XXdff5 din[5] dout[5] dout_bar[5] clk vdd gnd ms_flop
XXdff6 din[6] dout[6] dout_bar[6] clk vdd gnd ms_flop
XXdff7 din[7] dout[7] dout_bar[7] clk vdd gnd ms_flop
.ENDS msf_address

.SUBCKT msf_data_in din[0] din[1] din[2] din[3] din[4] din[5] din[6] din[7] din[8] din[9] din[10] din[11] din[12] din[13] din[14] din[15] din[16] din[17] din[18] din[19] din[20] din[21] din[22] din[23] din[24] din[25] din[26] din[27] din[28] din[29] din[30] din[31] dout[0] dout_bar[0] dout[1] dout_bar[1] dout[2] dout_bar[2] dout[3] dout_bar[3] dout[4] dout_bar[4] dout[5] dout_bar[5] dout[6] dout_bar[6] dout[7] dout_bar[7] dout[8] dout_bar[8] dout[9] dout_bar[9] dout[10] dout_bar[10] dout[11] dout_bar[11] dout[12] dout_bar[12] dout[13] dout_bar[13] dout[14] dout_bar[14] dout[15] dout_bar[15] dout[16] dout_bar[16] dout[17] dout_bar[17] dout[18] dout_bar[18] dout[19] dout_bar[19] dout[20] dout_bar[20] dout[21] dout_bar[21] dout[22] dout_bar[22] dout[23] dout_bar[23] dout[24] dout_bar[24] dout[25] dout_bar[25] dout[26] dout_bar[26] dout[27] dout_bar[27] dout[28] dout_bar[28] dout[29] dout_bar[29] dout[30] dout_bar[30] dout[31] dout_bar[31] clk vdd gnd
XXdff0 din[0] dout[0] dout_bar[0] clk vdd gnd ms_flop
XXdff4 din[1] dout[1] dout_bar[1] clk vdd gnd ms_flop
XXdff8 din[2] dout[2] dout_bar[2] clk vdd gnd ms_flop
XXdff12 din[3] dout[3] dout_bar[3] clk vdd gnd ms_flop
XXdff16 din[4] dout[4] dout_bar[4] clk vdd gnd ms_flop
XXdff20 din[5] dout[5] dout_bar[5] clk vdd gnd ms_flop
XXdff24 din[6] dout[6] dout_bar[6] clk vdd gnd ms_flop
XXdff28 din[7] dout[7] dout_bar[7] clk vdd gnd ms_flop
XXdff32 din[8] dout[8] dout_bar[8] clk vdd gnd ms_flop
XXdff36 din[9] dout[9] dout_bar[9] clk vdd gnd ms_flop
XXdff40 din[10] dout[10] dout_bar[10] clk vdd gnd ms_flop
XXdff44 din[11] dout[11] dout_bar[11] clk vdd gnd ms_flop
XXdff48 din[12] dout[12] dout_bar[12] clk vdd gnd ms_flop
XXdff52 din[13] dout[13] dout_bar[13] clk vdd gnd ms_flop
XXdff56 din[14] dout[14] dout_bar[14] clk vdd gnd ms_flop
XXdff60 din[15] dout[15] dout_bar[15] clk vdd gnd ms_flop
XXdff64 din[16] dout[16] dout_bar[16] clk vdd gnd ms_flop
XXdff68 din[17] dout[17] dout_bar[17] clk vdd gnd ms_flop
XXdff72 din[18] dout[18] dout_bar[18] clk vdd gnd ms_flop
XXdff76 din[19] dout[19] dout_bar[19] clk vdd gnd ms_flop
XXdff80 din[20] dout[20] dout_bar[20] clk vdd gnd ms_flop
XXdff84 din[21] dout[21] dout_bar[21] clk vdd gnd ms_flop
XXdff88 din[22] dout[22] dout_bar[22] clk vdd gnd ms_flop
XXdff92 din[23] dout[23] dout_bar[23] clk vdd gnd ms_flop
XXdff96 din[24] dout[24] dout_bar[24] clk vdd gnd ms_flop
XXdff100 din[25] dout[25] dout_bar[25] clk vdd gnd ms_flop
XXdff104 din[26] dout[26] dout_bar[26] clk vdd gnd ms_flop
XXdff108 din[27] dout[27] dout_bar[27] clk vdd gnd ms_flop
XXdff112 din[28] dout[28] dout_bar[28] clk vdd gnd ms_flop
XXdff116 din[29] dout[29] dout_bar[29] clk vdd gnd ms_flop
XXdff120 din[30] dout[30] dout_bar[30] clk vdd gnd ms_flop
XXdff124 din[31] dout[31] dout_bar[31] clk vdd gnd ms_flop
.ENDS msf_data_in
*********************** tri_gate ******************************

.SUBCKT tri_gate in out en en_bar vdd gnd

M_1 net_2 in_inv gnd gnd n W='1.2*1u' L=0.6u
M_2 net_3 in_inv vdd vdd p W='2.4*1u' L=0.6u
M_3 out en_bar net_3 vdd p W='2.4*1u' L=0.6u
M_4 out en net_2 gnd n W='1.2*1u' L=0.6u
M_5 in_inv in vdd vdd p W='2.4*1u' L=0.6u
M_6 in_inv in gnd gnd n W='1.2*1u' L=0.6u


.ENDS	

.SUBCKT tri_gate_array in[0] in[1] in[2] in[3] in[4] in[5] in[6] in[7] in[8] in[9] in[10] in[11] in[12] in[13] in[14] in[15] in[16] in[17] in[18] in[19] in[20] in[21] in[22] in[23] in[24] in[25] in[26] in[27] in[28] in[29] in[30] in[31] out[0] out[1] out[2] out[3] out[4] out[5] out[6] out[7] out[8] out[9] out[10] out[11] out[12] out[13] out[14] out[15] out[16] out[17] out[18] out[19] out[20] out[21] out[22] out[23] out[24] out[25] out[26] out[27] out[28] out[29] out[30] out[31] en en_bar vdd gnd
XXtri_gate0 in[0] out[0] en en_bar vdd gnd tri_gate
XXtri_gate4 in[1] out[1] en en_bar vdd gnd tri_gate
XXtri_gate8 in[2] out[2] en en_bar vdd gnd tri_gate
XXtri_gate12 in[3] out[3] en en_bar vdd gnd tri_gate
XXtri_gate16 in[4] out[4] en en_bar vdd gnd tri_gate
XXtri_gate20 in[5] out[5] en en_bar vdd gnd tri_gate
XXtri_gate24 in[6] out[6] en en_bar vdd gnd tri_gate
XXtri_gate28 in[7] out[7] en en_bar vdd gnd tri_gate
XXtri_gate32 in[8] out[8] en en_bar vdd gnd tri_gate
XXtri_gate36 in[9] out[9] en en_bar vdd gnd tri_gate
XXtri_gate40 in[10] out[10] en en_bar vdd gnd tri_gate
XXtri_gate44 in[11] out[11] en en_bar vdd gnd tri_gate
XXtri_gate48 in[12] out[12] en en_bar vdd gnd tri_gate
XXtri_gate52 in[13] out[13] en en_bar vdd gnd tri_gate
XXtri_gate56 in[14] out[14] en en_bar vdd gnd tri_gate
XXtri_gate60 in[15] out[15] en en_bar vdd gnd tri_gate
XXtri_gate64 in[16] out[16] en en_bar vdd gnd tri_gate
XXtri_gate68 in[17] out[17] en en_bar vdd gnd tri_gate
XXtri_gate72 in[18] out[18] en en_bar vdd gnd tri_gate
XXtri_gate76 in[19] out[19] en en_bar vdd gnd tri_gate
XXtri_gate80 in[20] out[20] en en_bar vdd gnd tri_gate
XXtri_gate84 in[21] out[21] en en_bar vdd gnd tri_gate
XXtri_gate88 in[22] out[22] en en_bar vdd gnd tri_gate
XXtri_gate92 in[23] out[23] en en_bar vdd gnd tri_gate
XXtri_gate96 in[24] out[24] en en_bar vdd gnd tri_gate
XXtri_gate100 in[25] out[25] en en_bar vdd gnd tri_gate
XXtri_gate104 in[26] out[26] en en_bar vdd gnd tri_gate
XXtri_gate108 in[27] out[27] en en_bar vdd gnd tri_gate
XXtri_gate112 in[28] out[28] en en_bar vdd gnd tri_gate
XXtri_gate116 in[29] out[29] en en_bar vdd gnd tri_gate
XXtri_gate120 in[30] out[30] en en_bar vdd gnd tri_gate
XXtri_gate124 in[31] out[31] en en_bar vdd gnd tri_gate
.ENDS tri_gate_array

.SUBCKT pinv_11 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.6u ps=3.6u as=1.8p ad=1.8p
.ENDS pinv_11

.SUBCKT pinv_12 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.6u ps=3.6u as=1.8p ad=1.8p
.ENDS pinv_12

.SUBCKT pnand2_4 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
.ENDS pnand2_4

.SUBCKT wordline_driver in[0] in[1] in[2] in[3] in[4] in[5] in[6] in[7] in[8] in[9] in[10] in[11] in[12] in[13] in[14] in[15] in[16] in[17] in[18] in[19] in[20] in[21] in[22] in[23] in[24] in[25] in[26] in[27] in[28] in[29] in[30] in[31] in[32] in[33] in[34] in[35] in[36] in[37] in[38] in[39] in[40] in[41] in[42] in[43] in[44] in[45] in[46] in[47] in[48] in[49] in[50] in[51] in[52] in[53] in[54] in[55] in[56] in[57] in[58] in[59] in[60] in[61] in[62] in[63] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] wl[16] wl[17] wl[18] wl[19] wl[20] wl[21] wl[22] wl[23] wl[24] wl[25] wl[26] wl[27] wl[28] wl[29] wl[30] wl[31] wl[32] wl[33] wl[34] wl[35] wl[36] wl[37] wl[38] wl[39] wl[40] wl[41] wl[42] wl[43] wl[44] wl[45] wl[46] wl[47] wl[48] wl[49] wl[50] wl[51] wl[52] wl[53] wl[54] wl[55] wl[56] wl[57] wl[58] wl[59] wl[60] wl[61] wl[62] wl[63] en vdd gnd
Xwl_driver_inv_en0 en en_bar[0] vdd gnd pinv_12
Xwl_driver_nand0 en_bar[0] in[0] net[0] vdd gnd pnand2_4
Xwl_driver_inv0 net[0] wl[0] vdd gnd pinv_11
Xwl_driver_inv_en1 en en_bar[1] vdd gnd pinv_12
Xwl_driver_nand1 en_bar[1] in[1] net[1] vdd gnd pnand2_4
Xwl_driver_inv1 net[1] wl[1] vdd gnd pinv_11
Xwl_driver_inv_en2 en en_bar[2] vdd gnd pinv_12
Xwl_driver_nand2 en_bar[2] in[2] net[2] vdd gnd pnand2_4
Xwl_driver_inv2 net[2] wl[2] vdd gnd pinv_11
Xwl_driver_inv_en3 en en_bar[3] vdd gnd pinv_12
Xwl_driver_nand3 en_bar[3] in[3] net[3] vdd gnd pnand2_4
Xwl_driver_inv3 net[3] wl[3] vdd gnd pinv_11
Xwl_driver_inv_en4 en en_bar[4] vdd gnd pinv_12
Xwl_driver_nand4 en_bar[4] in[4] net[4] vdd gnd pnand2_4
Xwl_driver_inv4 net[4] wl[4] vdd gnd pinv_11
Xwl_driver_inv_en5 en en_bar[5] vdd gnd pinv_12
Xwl_driver_nand5 en_bar[5] in[5] net[5] vdd gnd pnand2_4
Xwl_driver_inv5 net[5] wl[5] vdd gnd pinv_11
Xwl_driver_inv_en6 en en_bar[6] vdd gnd pinv_12
Xwl_driver_nand6 en_bar[6] in[6] net[6] vdd gnd pnand2_4
Xwl_driver_inv6 net[6] wl[6] vdd gnd pinv_11
Xwl_driver_inv_en7 en en_bar[7] vdd gnd pinv_12
Xwl_driver_nand7 en_bar[7] in[7] net[7] vdd gnd pnand2_4
Xwl_driver_inv7 net[7] wl[7] vdd gnd pinv_11
Xwl_driver_inv_en8 en en_bar[8] vdd gnd pinv_12
Xwl_driver_nand8 en_bar[8] in[8] net[8] vdd gnd pnand2_4
Xwl_driver_inv8 net[8] wl[8] vdd gnd pinv_11
Xwl_driver_inv_en9 en en_bar[9] vdd gnd pinv_12
Xwl_driver_nand9 en_bar[9] in[9] net[9] vdd gnd pnand2_4
Xwl_driver_inv9 net[9] wl[9] vdd gnd pinv_11
Xwl_driver_inv_en10 en en_bar[10] vdd gnd pinv_12
Xwl_driver_nand10 en_bar[10] in[10] net[10] vdd gnd pnand2_4
Xwl_driver_inv10 net[10] wl[10] vdd gnd pinv_11
Xwl_driver_inv_en11 en en_bar[11] vdd gnd pinv_12
Xwl_driver_nand11 en_bar[11] in[11] net[11] vdd gnd pnand2_4
Xwl_driver_inv11 net[11] wl[11] vdd gnd pinv_11
Xwl_driver_inv_en12 en en_bar[12] vdd gnd pinv_12
Xwl_driver_nand12 en_bar[12] in[12] net[12] vdd gnd pnand2_4
Xwl_driver_inv12 net[12] wl[12] vdd gnd pinv_11
Xwl_driver_inv_en13 en en_bar[13] vdd gnd pinv_12
Xwl_driver_nand13 en_bar[13] in[13] net[13] vdd gnd pnand2_4
Xwl_driver_inv13 net[13] wl[13] vdd gnd pinv_11
Xwl_driver_inv_en14 en en_bar[14] vdd gnd pinv_12
Xwl_driver_nand14 en_bar[14] in[14] net[14] vdd gnd pnand2_4
Xwl_driver_inv14 net[14] wl[14] vdd gnd pinv_11
Xwl_driver_inv_en15 en en_bar[15] vdd gnd pinv_12
Xwl_driver_nand15 en_bar[15] in[15] net[15] vdd gnd pnand2_4
Xwl_driver_inv15 net[15] wl[15] vdd gnd pinv_11
Xwl_driver_inv_en16 en en_bar[16] vdd gnd pinv_12
Xwl_driver_nand16 en_bar[16] in[16] net[16] vdd gnd pnand2_4
Xwl_driver_inv16 net[16] wl[16] vdd gnd pinv_11
Xwl_driver_inv_en17 en en_bar[17] vdd gnd pinv_12
Xwl_driver_nand17 en_bar[17] in[17] net[17] vdd gnd pnand2_4
Xwl_driver_inv17 net[17] wl[17] vdd gnd pinv_11
Xwl_driver_inv_en18 en en_bar[18] vdd gnd pinv_12
Xwl_driver_nand18 en_bar[18] in[18] net[18] vdd gnd pnand2_4
Xwl_driver_inv18 net[18] wl[18] vdd gnd pinv_11
Xwl_driver_inv_en19 en en_bar[19] vdd gnd pinv_12
Xwl_driver_nand19 en_bar[19] in[19] net[19] vdd gnd pnand2_4
Xwl_driver_inv19 net[19] wl[19] vdd gnd pinv_11
Xwl_driver_inv_en20 en en_bar[20] vdd gnd pinv_12
Xwl_driver_nand20 en_bar[20] in[20] net[20] vdd gnd pnand2_4
Xwl_driver_inv20 net[20] wl[20] vdd gnd pinv_11
Xwl_driver_inv_en21 en en_bar[21] vdd gnd pinv_12
Xwl_driver_nand21 en_bar[21] in[21] net[21] vdd gnd pnand2_4
Xwl_driver_inv21 net[21] wl[21] vdd gnd pinv_11
Xwl_driver_inv_en22 en en_bar[22] vdd gnd pinv_12
Xwl_driver_nand22 en_bar[22] in[22] net[22] vdd gnd pnand2_4
Xwl_driver_inv22 net[22] wl[22] vdd gnd pinv_11
Xwl_driver_inv_en23 en en_bar[23] vdd gnd pinv_12
Xwl_driver_nand23 en_bar[23] in[23] net[23] vdd gnd pnand2_4
Xwl_driver_inv23 net[23] wl[23] vdd gnd pinv_11
Xwl_driver_inv_en24 en en_bar[24] vdd gnd pinv_12
Xwl_driver_nand24 en_bar[24] in[24] net[24] vdd gnd pnand2_4
Xwl_driver_inv24 net[24] wl[24] vdd gnd pinv_11
Xwl_driver_inv_en25 en en_bar[25] vdd gnd pinv_12
Xwl_driver_nand25 en_bar[25] in[25] net[25] vdd gnd pnand2_4
Xwl_driver_inv25 net[25] wl[25] vdd gnd pinv_11
Xwl_driver_inv_en26 en en_bar[26] vdd gnd pinv_12
Xwl_driver_nand26 en_bar[26] in[26] net[26] vdd gnd pnand2_4
Xwl_driver_inv26 net[26] wl[26] vdd gnd pinv_11
Xwl_driver_inv_en27 en en_bar[27] vdd gnd pinv_12
Xwl_driver_nand27 en_bar[27] in[27] net[27] vdd gnd pnand2_4
Xwl_driver_inv27 net[27] wl[27] vdd gnd pinv_11
Xwl_driver_inv_en28 en en_bar[28] vdd gnd pinv_12
Xwl_driver_nand28 en_bar[28] in[28] net[28] vdd gnd pnand2_4
Xwl_driver_inv28 net[28] wl[28] vdd gnd pinv_11
Xwl_driver_inv_en29 en en_bar[29] vdd gnd pinv_12
Xwl_driver_nand29 en_bar[29] in[29] net[29] vdd gnd pnand2_4
Xwl_driver_inv29 net[29] wl[29] vdd gnd pinv_11
Xwl_driver_inv_en30 en en_bar[30] vdd gnd pinv_12
Xwl_driver_nand30 en_bar[30] in[30] net[30] vdd gnd pnand2_4
Xwl_driver_inv30 net[30] wl[30] vdd gnd pinv_11
Xwl_driver_inv_en31 en en_bar[31] vdd gnd pinv_12
Xwl_driver_nand31 en_bar[31] in[31] net[31] vdd gnd pnand2_4
Xwl_driver_inv31 net[31] wl[31] vdd gnd pinv_11
Xwl_driver_inv_en32 en en_bar[32] vdd gnd pinv_12
Xwl_driver_nand32 en_bar[32] in[32] net[32] vdd gnd pnand2_4
Xwl_driver_inv32 net[32] wl[32] vdd gnd pinv_11
Xwl_driver_inv_en33 en en_bar[33] vdd gnd pinv_12
Xwl_driver_nand33 en_bar[33] in[33] net[33] vdd gnd pnand2_4
Xwl_driver_inv33 net[33] wl[33] vdd gnd pinv_11
Xwl_driver_inv_en34 en en_bar[34] vdd gnd pinv_12
Xwl_driver_nand34 en_bar[34] in[34] net[34] vdd gnd pnand2_4
Xwl_driver_inv34 net[34] wl[34] vdd gnd pinv_11
Xwl_driver_inv_en35 en en_bar[35] vdd gnd pinv_12
Xwl_driver_nand35 en_bar[35] in[35] net[35] vdd gnd pnand2_4
Xwl_driver_inv35 net[35] wl[35] vdd gnd pinv_11
Xwl_driver_inv_en36 en en_bar[36] vdd gnd pinv_12
Xwl_driver_nand36 en_bar[36] in[36] net[36] vdd gnd pnand2_4
Xwl_driver_inv36 net[36] wl[36] vdd gnd pinv_11
Xwl_driver_inv_en37 en en_bar[37] vdd gnd pinv_12
Xwl_driver_nand37 en_bar[37] in[37] net[37] vdd gnd pnand2_4
Xwl_driver_inv37 net[37] wl[37] vdd gnd pinv_11
Xwl_driver_inv_en38 en en_bar[38] vdd gnd pinv_12
Xwl_driver_nand38 en_bar[38] in[38] net[38] vdd gnd pnand2_4
Xwl_driver_inv38 net[38] wl[38] vdd gnd pinv_11
Xwl_driver_inv_en39 en en_bar[39] vdd gnd pinv_12
Xwl_driver_nand39 en_bar[39] in[39] net[39] vdd gnd pnand2_4
Xwl_driver_inv39 net[39] wl[39] vdd gnd pinv_11
Xwl_driver_inv_en40 en en_bar[40] vdd gnd pinv_12
Xwl_driver_nand40 en_bar[40] in[40] net[40] vdd gnd pnand2_4
Xwl_driver_inv40 net[40] wl[40] vdd gnd pinv_11
Xwl_driver_inv_en41 en en_bar[41] vdd gnd pinv_12
Xwl_driver_nand41 en_bar[41] in[41] net[41] vdd gnd pnand2_4
Xwl_driver_inv41 net[41] wl[41] vdd gnd pinv_11
Xwl_driver_inv_en42 en en_bar[42] vdd gnd pinv_12
Xwl_driver_nand42 en_bar[42] in[42] net[42] vdd gnd pnand2_4
Xwl_driver_inv42 net[42] wl[42] vdd gnd pinv_11
Xwl_driver_inv_en43 en en_bar[43] vdd gnd pinv_12
Xwl_driver_nand43 en_bar[43] in[43] net[43] vdd gnd pnand2_4
Xwl_driver_inv43 net[43] wl[43] vdd gnd pinv_11
Xwl_driver_inv_en44 en en_bar[44] vdd gnd pinv_12
Xwl_driver_nand44 en_bar[44] in[44] net[44] vdd gnd pnand2_4
Xwl_driver_inv44 net[44] wl[44] vdd gnd pinv_11
Xwl_driver_inv_en45 en en_bar[45] vdd gnd pinv_12
Xwl_driver_nand45 en_bar[45] in[45] net[45] vdd gnd pnand2_4
Xwl_driver_inv45 net[45] wl[45] vdd gnd pinv_11
Xwl_driver_inv_en46 en en_bar[46] vdd gnd pinv_12
Xwl_driver_nand46 en_bar[46] in[46] net[46] vdd gnd pnand2_4
Xwl_driver_inv46 net[46] wl[46] vdd gnd pinv_11
Xwl_driver_inv_en47 en en_bar[47] vdd gnd pinv_12
Xwl_driver_nand47 en_bar[47] in[47] net[47] vdd gnd pnand2_4
Xwl_driver_inv47 net[47] wl[47] vdd gnd pinv_11
Xwl_driver_inv_en48 en en_bar[48] vdd gnd pinv_12
Xwl_driver_nand48 en_bar[48] in[48] net[48] vdd gnd pnand2_4
Xwl_driver_inv48 net[48] wl[48] vdd gnd pinv_11
Xwl_driver_inv_en49 en en_bar[49] vdd gnd pinv_12
Xwl_driver_nand49 en_bar[49] in[49] net[49] vdd gnd pnand2_4
Xwl_driver_inv49 net[49] wl[49] vdd gnd pinv_11
Xwl_driver_inv_en50 en en_bar[50] vdd gnd pinv_12
Xwl_driver_nand50 en_bar[50] in[50] net[50] vdd gnd pnand2_4
Xwl_driver_inv50 net[50] wl[50] vdd gnd pinv_11
Xwl_driver_inv_en51 en en_bar[51] vdd gnd pinv_12
Xwl_driver_nand51 en_bar[51] in[51] net[51] vdd gnd pnand2_4
Xwl_driver_inv51 net[51] wl[51] vdd gnd pinv_11
Xwl_driver_inv_en52 en en_bar[52] vdd gnd pinv_12
Xwl_driver_nand52 en_bar[52] in[52] net[52] vdd gnd pnand2_4
Xwl_driver_inv52 net[52] wl[52] vdd gnd pinv_11
Xwl_driver_inv_en53 en en_bar[53] vdd gnd pinv_12
Xwl_driver_nand53 en_bar[53] in[53] net[53] vdd gnd pnand2_4
Xwl_driver_inv53 net[53] wl[53] vdd gnd pinv_11
Xwl_driver_inv_en54 en en_bar[54] vdd gnd pinv_12
Xwl_driver_nand54 en_bar[54] in[54] net[54] vdd gnd pnand2_4
Xwl_driver_inv54 net[54] wl[54] vdd gnd pinv_11
Xwl_driver_inv_en55 en en_bar[55] vdd gnd pinv_12
Xwl_driver_nand55 en_bar[55] in[55] net[55] vdd gnd pnand2_4
Xwl_driver_inv55 net[55] wl[55] vdd gnd pinv_11
Xwl_driver_inv_en56 en en_bar[56] vdd gnd pinv_12
Xwl_driver_nand56 en_bar[56] in[56] net[56] vdd gnd pnand2_4
Xwl_driver_inv56 net[56] wl[56] vdd gnd pinv_11
Xwl_driver_inv_en57 en en_bar[57] vdd gnd pinv_12
Xwl_driver_nand57 en_bar[57] in[57] net[57] vdd gnd pnand2_4
Xwl_driver_inv57 net[57] wl[57] vdd gnd pinv_11
Xwl_driver_inv_en58 en en_bar[58] vdd gnd pinv_12
Xwl_driver_nand58 en_bar[58] in[58] net[58] vdd gnd pnand2_4
Xwl_driver_inv58 net[58] wl[58] vdd gnd pinv_11
Xwl_driver_inv_en59 en en_bar[59] vdd gnd pinv_12
Xwl_driver_nand59 en_bar[59] in[59] net[59] vdd gnd pnand2_4
Xwl_driver_inv59 net[59] wl[59] vdd gnd pinv_11
Xwl_driver_inv_en60 en en_bar[60] vdd gnd pinv_12
Xwl_driver_nand60 en_bar[60] in[60] net[60] vdd gnd pnand2_4
Xwl_driver_inv60 net[60] wl[60] vdd gnd pinv_11
Xwl_driver_inv_en61 en en_bar[61] vdd gnd pinv_12
Xwl_driver_nand61 en_bar[61] in[61] net[61] vdd gnd pnand2_4
Xwl_driver_inv61 net[61] wl[61] vdd gnd pinv_11
Xwl_driver_inv_en62 en en_bar[62] vdd gnd pinv_12
Xwl_driver_nand62 en_bar[62] in[62] net[62] vdd gnd pnand2_4
Xwl_driver_inv62 net[62] wl[62] vdd gnd pinv_11
Xwl_driver_inv_en63 en en_bar[63] vdd gnd pinv_12
Xwl_driver_nand63 en_bar[63] in[63] net[63] vdd gnd pnand2_4
Xwl_driver_inv63 net[63] wl[63] vdd gnd pinv_11
.ENDS wordline_driver

.SUBCKT pinv_13 A Z vdd gnd
Mpinv_pmos Z A vdd vdd p m=1 w=2.4u l=0.6u pd=6.0u ps=6.0u as=3.6p ad=3.6p
Mpinv_nmos Z A gnd gnd n m=1 w=1.2u l=0.6u pd=3.6u ps=3.6u as=1.8p ad=1.8p
.ENDS pinv_13

.SUBCKT bank DATA[0] DATA[1] DATA[2] DATA[3] DATA[4] DATA[5] DATA[6] DATA[7] DATA[8] DATA[9] DATA[10] DATA[11] DATA[12] DATA[13] DATA[14] DATA[15] DATA[16] DATA[17] DATA[18] DATA[19] DATA[20] DATA[21] DATA[22] DATA[23] DATA[24] DATA[25] DATA[26] DATA[27] DATA[28] DATA[29] DATA[30] DATA[31] ADDR[0] ADDR[1] ADDR[2] ADDR[3] ADDR[4] ADDR[5] ADDR[6] ADDR[7] s_en w_en tri_en_bar tri_en clk_bar clk_buf vdd gnd
Xbitcell_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] bl[8] br[8] bl[9] br[9] bl[10] br[10] bl[11] br[11] bl[12] br[12] bl[13] br[13] bl[14] br[14] bl[15] br[15] bl[16] br[16] bl[17] br[17] bl[18] br[18] bl[19] br[19] bl[20] br[20] bl[21] br[21] bl[22] br[22] bl[23] br[23] bl[24] br[24] bl[25] br[25] bl[26] br[26] bl[27] br[27] bl[28] br[28] bl[29] br[29] bl[30] br[30] bl[31] br[31] bl[32] br[32] bl[33] br[33] bl[34] br[34] bl[35] br[35] bl[36] br[36] bl[37] br[37] bl[38] br[38] bl[39] br[39] bl[40] br[40] bl[41] br[41] bl[42] br[42] bl[43] br[43] bl[44] br[44] bl[45] br[45] bl[46] br[46] bl[47] br[47] bl[48] br[48] bl[49] br[49] bl[50] br[50] bl[51] br[51] bl[52] br[52] bl[53] br[53] bl[54] br[54] bl[55] br[55] bl[56] br[56] bl[57] br[57] bl[58] br[58] bl[59] br[59] bl[60] br[60] bl[61] br[61] bl[62] br[62] bl[63] br[63] bl[64] br[64] bl[65] br[65] bl[66] br[66] bl[67] br[67] bl[68] br[68] bl[69] br[69] bl[70] br[70] bl[71] br[71] bl[72] br[72] bl[73] br[73] bl[74] br[74] bl[75] br[75] bl[76] br[76] bl[77] br[77] bl[78] br[78] bl[79] br[79] bl[80] br[80] bl[81] br[81] bl[82] br[82] bl[83] br[83] bl[84] br[84] bl[85] br[85] bl[86] br[86] bl[87] br[87] bl[88] br[88] bl[89] br[89] bl[90] br[90] bl[91] br[91] bl[92] br[92] bl[93] br[93] bl[94] br[94] bl[95] br[95] bl[96] br[96] bl[97] br[97] bl[98] br[98] bl[99] br[99] bl[100] br[100] bl[101] br[101] bl[102] br[102] bl[103] br[103] bl[104] br[104] bl[105] br[105] bl[106] br[106] bl[107] br[107] bl[108] br[108] bl[109] br[109] bl[110] br[110] bl[111] br[111] bl[112] br[112] bl[113] br[113] bl[114] br[114] bl[115] br[115] bl[116] br[116] bl[117] br[117] bl[118] br[118] bl[119] br[119] bl[120] br[120] bl[121] br[121] bl[122] br[122] bl[123] br[123] bl[124] br[124] bl[125] br[125] bl[126] br[126] bl[127] br[127] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] wl[16] wl[17] wl[18] wl[19] wl[20] wl[21] wl[22] wl[23] wl[24] wl[25] wl[26] wl[27] wl[28] wl[29] wl[30] wl[31] wl[32] wl[33] wl[34] wl[35] wl[36] wl[37] wl[38] wl[39] wl[40] wl[41] wl[42] wl[43] wl[44] wl[45] wl[46] wl[47] wl[48] wl[49] wl[50] wl[51] wl[52] wl[53] wl[54] wl[55] wl[56] wl[57] wl[58] wl[59] wl[60] wl[61] wl[62] wl[63] vdd gnd bitcell_array
Xprecharge_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] bl[8] br[8] bl[9] br[9] bl[10] br[10] bl[11] br[11] bl[12] br[12] bl[13] br[13] bl[14] br[14] bl[15] br[15] bl[16] br[16] bl[17] br[17] bl[18] br[18] bl[19] br[19] bl[20] br[20] bl[21] br[21] bl[22] br[22] bl[23] br[23] bl[24] br[24] bl[25] br[25] bl[26] br[26] bl[27] br[27] bl[28] br[28] bl[29] br[29] bl[30] br[30] bl[31] br[31] bl[32] br[32] bl[33] br[33] bl[34] br[34] bl[35] br[35] bl[36] br[36] bl[37] br[37] bl[38] br[38] bl[39] br[39] bl[40] br[40] bl[41] br[41] bl[42] br[42] bl[43] br[43] bl[44] br[44] bl[45] br[45] bl[46] br[46] bl[47] br[47] bl[48] br[48] bl[49] br[49] bl[50] br[50] bl[51] br[51] bl[52] br[52] bl[53] br[53] bl[54] br[54] bl[55] br[55] bl[56] br[56] bl[57] br[57] bl[58] br[58] bl[59] br[59] bl[60] br[60] bl[61] br[61] bl[62] br[62] bl[63] br[63] bl[64] br[64] bl[65] br[65] bl[66] br[66] bl[67] br[67] bl[68] br[68] bl[69] br[69] bl[70] br[70] bl[71] br[71] bl[72] br[72] bl[73] br[73] bl[74] br[74] bl[75] br[75] bl[76] br[76] bl[77] br[77] bl[78] br[78] bl[79] br[79] bl[80] br[80] bl[81] br[81] bl[82] br[82] bl[83] br[83] bl[84] br[84] bl[85] br[85] bl[86] br[86] bl[87] br[87] bl[88] br[88] bl[89] br[89] bl[90] br[90] bl[91] br[91] bl[92] br[92] bl[93] br[93] bl[94] br[94] bl[95] br[95] bl[96] br[96] bl[97] br[97] bl[98] br[98] bl[99] br[99] bl[100] br[100] bl[101] br[101] bl[102] br[102] bl[103] br[103] bl[104] br[104] bl[105] br[105] bl[106] br[106] bl[107] br[107] bl[108] br[108] bl[109] br[109] bl[110] br[110] bl[111] br[111] bl[112] br[112] bl[113] br[113] bl[114] br[114] bl[115] br[115] bl[116] br[116] bl[117] br[117] bl[118] br[118] bl[119] br[119] bl[120] br[120] bl[121] br[121] bl[122] br[122] bl[123] br[123] bl[124] br[124] bl[125] br[125] bl[126] br[126] bl[127] br[127] clk_bar vdd precharge_array
Xcolumn_mux_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] bl[8] br[8] bl[9] br[9] bl[10] br[10] bl[11] br[11] bl[12] br[12] bl[13] br[13] bl[14] br[14] bl[15] br[15] bl[16] br[16] bl[17] br[17] bl[18] br[18] bl[19] br[19] bl[20] br[20] bl[21] br[21] bl[22] br[22] bl[23] br[23] bl[24] br[24] bl[25] br[25] bl[26] br[26] bl[27] br[27] bl[28] br[28] bl[29] br[29] bl[30] br[30] bl[31] br[31] bl[32] br[32] bl[33] br[33] bl[34] br[34] bl[35] br[35] bl[36] br[36] bl[37] br[37] bl[38] br[38] bl[39] br[39] bl[40] br[40] bl[41] br[41] bl[42] br[42] bl[43] br[43] bl[44] br[44] bl[45] br[45] bl[46] br[46] bl[47] br[47] bl[48] br[48] bl[49] br[49] bl[50] br[50] bl[51] br[51] bl[52] br[52] bl[53] br[53] bl[54] br[54] bl[55] br[55] bl[56] br[56] bl[57] br[57] bl[58] br[58] bl[59] br[59] bl[60] br[60] bl[61] br[61] bl[62] br[62] bl[63] br[63] bl[64] br[64] bl[65] br[65] bl[66] br[66] bl[67] br[67] bl[68] br[68] bl[69] br[69] bl[70] br[70] bl[71] br[71] bl[72] br[72] bl[73] br[73] bl[74] br[74] bl[75] br[75] bl[76] br[76] bl[77] br[77] bl[78] br[78] bl[79] br[79] bl[80] br[80] bl[81] br[81] bl[82] br[82] bl[83] br[83] bl[84] br[84] bl[85] br[85] bl[86] br[86] bl[87] br[87] bl[88] br[88] bl[89] br[89] bl[90] br[90] bl[91] br[91] bl[92] br[92] bl[93] br[93] bl[94] br[94] bl[95] br[95] bl[96] br[96] bl[97] br[97] bl[98] br[98] bl[99] br[99] bl[100] br[100] bl[101] br[101] bl[102] br[102] bl[103] br[103] bl[104] br[104] bl[105] br[105] bl[106] br[106] bl[107] br[107] bl[108] br[108] bl[109] br[109] bl[110] br[110] bl[111] br[111] bl[112] br[112] bl[113] br[113] bl[114] br[114] bl[115] br[115] bl[116] br[116] bl[117] br[117] bl[118] br[118] bl[119] br[119] bl[120] br[120] bl[121] br[121] bl[122] br[122] bl[123] br[123] bl[124] br[124] bl[125] br[125] bl[126] br[126] bl[127] br[127] sel[0] sel[1] sel[2] sel[3] bl_out[0] br_out[0] bl_out[1] br_out[1] bl_out[2] br_out[2] bl_out[3] br_out[3] bl_out[4] br_out[4] bl_out[5] br_out[5] bl_out[6] br_out[6] bl_out[7] br_out[7] bl_out[8] br_out[8] bl_out[9] br_out[9] bl_out[10] br_out[10] bl_out[11] br_out[11] bl_out[12] br_out[12] bl_out[13] br_out[13] bl_out[14] br_out[14] bl_out[15] br_out[15] bl_out[16] br_out[16] bl_out[17] br_out[17] bl_out[18] br_out[18] bl_out[19] br_out[19] bl_out[20] br_out[20] bl_out[21] br_out[21] bl_out[22] br_out[22] bl_out[23] br_out[23] bl_out[24] br_out[24] bl_out[25] br_out[25] bl_out[26] br_out[26] bl_out[27] br_out[27] bl_out[28] br_out[28] bl_out[29] br_out[29] bl_out[30] br_out[30] bl_out[31] br_out[31] gnd columnmux_array
Xcol_address_decoder A[6] A[7] sel[0] sel[1] sel[2] sel[3] vdd gnd pre2x4
Xsense_amp_array data_out[0] bl_out[0] br_out[0] data_out[1] bl_out[1] br_out[1] data_out[2] bl_out[2] br_out[2] data_out[3] bl_out[3] br_out[3] data_out[4] bl_out[4] br_out[4] data_out[5] bl_out[5] br_out[5] data_out[6] bl_out[6] br_out[6] data_out[7] bl_out[7] br_out[7] data_out[8] bl_out[8] br_out[8] data_out[9] bl_out[9] br_out[9] data_out[10] bl_out[10] br_out[10] data_out[11] bl_out[11] br_out[11] data_out[12] bl_out[12] br_out[12] data_out[13] bl_out[13] br_out[13] data_out[14] bl_out[14] br_out[14] data_out[15] bl_out[15] br_out[15] data_out[16] bl_out[16] br_out[16] data_out[17] bl_out[17] br_out[17] data_out[18] bl_out[18] br_out[18] data_out[19] bl_out[19] br_out[19] data_out[20] bl_out[20] br_out[20] data_out[21] bl_out[21] br_out[21] data_out[22] bl_out[22] br_out[22] data_out[23] bl_out[23] br_out[23] data_out[24] bl_out[24] br_out[24] data_out[25] bl_out[25] br_out[25] data_out[26] bl_out[26] br_out[26] data_out[27] bl_out[27] br_out[27] data_out[28] bl_out[28] br_out[28] data_out[29] bl_out[29] br_out[29] data_out[30] bl_out[30] br_out[30] data_out[31] bl_out[31] br_out[31] s_en vdd gnd sense_amp_array
Xwrite_driver_array data_in[0] data_in[1] data_in[2] data_in[3] data_in[4] data_in[5] data_in[6] data_in[7] data_in[8] data_in[9] data_in[10] data_in[11] data_in[12] data_in[13] data_in[14] data_in[15] data_in[16] data_in[17] data_in[18] data_in[19] data_in[20] data_in[21] data_in[22] data_in[23] data_in[24] data_in[25] data_in[26] data_in[27] data_in[28] data_in[29] data_in[30] data_in[31] bl_out[0] br_out[0] bl_out[1] br_out[1] bl_out[2] br_out[2] bl_out[3] br_out[3] bl_out[4] br_out[4] bl_out[5] br_out[5] bl_out[6] br_out[6] bl_out[7] br_out[7] bl_out[8] br_out[8] bl_out[9] br_out[9] bl_out[10] br_out[10] bl_out[11] br_out[11] bl_out[12] br_out[12] bl_out[13] br_out[13] bl_out[14] br_out[14] bl_out[15] br_out[15] bl_out[16] br_out[16] bl_out[17] br_out[17] bl_out[18] br_out[18] bl_out[19] br_out[19] bl_out[20] br_out[20] bl_out[21] br_out[21] bl_out[22] br_out[22] bl_out[23] br_out[23] bl_out[24] br_out[24] bl_out[25] br_out[25] bl_out[26] br_out[26] bl_out[27] br_out[27] bl_out[28] br_out[28] bl_out[29] br_out[29] bl_out[30] br_out[30] bl_out[31] br_out[31] w_en vdd gnd write_driver_array
Xdata_in_flop_array DATA[0] DATA[1] DATA[2] DATA[3] DATA[4] DATA[5] DATA[6] DATA[7] DATA[8] DATA[9] DATA[10] DATA[11] DATA[12] DATA[13] DATA[14] DATA[15] DATA[16] DATA[17] DATA[18] DATA[19] DATA[20] DATA[21] DATA[22] DATA[23] DATA[24] DATA[25] DATA[26] DATA[27] DATA[28] DATA[29] DATA[30] DATA[31] data_in[0] data_in_bar[0] data_in[1] data_in_bar[1] data_in[2] data_in_bar[2] data_in[3] data_in_bar[3] data_in[4] data_in_bar[4] data_in[5] data_in_bar[5] data_in[6] data_in_bar[6] data_in[7] data_in_bar[7] data_in[8] data_in_bar[8] data_in[9] data_in_bar[9] data_in[10] data_in_bar[10] data_in[11] data_in_bar[11] data_in[12] data_in_bar[12] data_in[13] data_in_bar[13] data_in[14] data_in_bar[14] data_in[15] data_in_bar[15] data_in[16] data_in_bar[16] data_in[17] data_in_bar[17] data_in[18] data_in_bar[18] data_in[19] data_in_bar[19] data_in[20] data_in_bar[20] data_in[21] data_in_bar[21] data_in[22] data_in_bar[22] data_in[23] data_in_bar[23] data_in[24] data_in_bar[24] data_in[25] data_in_bar[25] data_in[26] data_in_bar[26] data_in[27] data_in_bar[27] data_in[28] data_in_bar[28] data_in[29] data_in_bar[29] data_in[30] data_in_bar[30] data_in[31] data_in_bar[31] clk_bar vdd gnd msf_data_in
Xtri_gate_array data_out[0] data_out[1] data_out[2] data_out[3] data_out[4] data_out[5] data_out[6] data_out[7] data_out[8] data_out[9] data_out[10] data_out[11] data_out[12] data_out[13] data_out[14] data_out[15] data_out[16] data_out[17] data_out[18] data_out[19] data_out[20] data_out[21] data_out[22] data_out[23] data_out[24] data_out[25] data_out[26] data_out[27] data_out[28] data_out[29] data_out[30] data_out[31] DATA[0] DATA[1] DATA[2] DATA[3] DATA[4] DATA[5] DATA[6] DATA[7] DATA[8] DATA[9] DATA[10] DATA[11] DATA[12] DATA[13] DATA[14] DATA[15] DATA[16] DATA[17] DATA[18] DATA[19] DATA[20] DATA[21] DATA[22] DATA[23] DATA[24] DATA[25] DATA[26] DATA[27] DATA[28] DATA[29] DATA[30] DATA[31] tri_en tri_en_bar vdd gnd tri_gate_array
Xrow_decoder A[0] A[1] A[2] A[3] A[4] A[5] dec_out[0] dec_out[1] dec_out[2] dec_out[3] dec_out[4] dec_out[5] dec_out[6] dec_out[7] dec_out[8] dec_out[9] dec_out[10] dec_out[11] dec_out[12] dec_out[13] dec_out[14] dec_out[15] dec_out[16] dec_out[17] dec_out[18] dec_out[19] dec_out[20] dec_out[21] dec_out[22] dec_out[23] dec_out[24] dec_out[25] dec_out[26] dec_out[27] dec_out[28] dec_out[29] dec_out[30] dec_out[31] dec_out[32] dec_out[33] dec_out[34] dec_out[35] dec_out[36] dec_out[37] dec_out[38] dec_out[39] dec_out[40] dec_out[41] dec_out[42] dec_out[43] dec_out[44] dec_out[45] dec_out[46] dec_out[47] dec_out[48] dec_out[49] dec_out[50] dec_out[51] dec_out[52] dec_out[53] dec_out[54] dec_out[55] dec_out[56] dec_out[57] dec_out[58] dec_out[59] dec_out[60] dec_out[61] dec_out[62] dec_out[63] vdd gnd hierarchical_decoder_64rows
Xwordline_driver dec_out[0] dec_out[1] dec_out[2] dec_out[3] dec_out[4] dec_out[5] dec_out[6] dec_out[7] dec_out[8] dec_out[9] dec_out[10] dec_out[11] dec_out[12] dec_out[13] dec_out[14] dec_out[15] dec_out[16] dec_out[17] dec_out[18] dec_out[19] dec_out[20] dec_out[21] dec_out[22] dec_out[23] dec_out[24] dec_out[25] dec_out[26] dec_out[27] dec_out[28] dec_out[29] dec_out[30] dec_out[31] dec_out[32] dec_out[33] dec_out[34] dec_out[35] dec_out[36] dec_out[37] dec_out[38] dec_out[39] dec_out[40] dec_out[41] dec_out[42] dec_out[43] dec_out[44] dec_out[45] dec_out[46] dec_out[47] dec_out[48] dec_out[49] dec_out[50] dec_out[51] dec_out[52] dec_out[53] dec_out[54] dec_out[55] dec_out[56] dec_out[57] dec_out[58] dec_out[59] dec_out[60] dec_out[61] dec_out[62] dec_out[63] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] wl[16] wl[17] wl[18] wl[19] wl[20] wl[21] wl[22] wl[23] wl[24] wl[25] wl[26] wl[27] wl[28] wl[29] wl[30] wl[31] wl[32] wl[33] wl[34] wl[35] wl[36] wl[37] wl[38] wl[39] wl[40] wl[41] wl[42] wl[43] wl[44] wl[45] wl[46] wl[47] wl[48] wl[49] wl[50] wl[51] wl[52] wl[53] wl[54] wl[55] wl[56] wl[57] wl[58] wl[59] wl[60] wl[61] wl[62] wl[63] clk_buf vdd gnd wordline_driver
Xaddress_flop_array ADDR[0] ADDR[1] ADDR[2] ADDR[3] ADDR[4] ADDR[5] ADDR[6] ADDR[7] A[0] A_bar[0] A[1] A_bar[1] A[2] A_bar[2] A[3] A_bar[3] A[4] A_bar[4] A[5] A_bar[5] A[6] A_bar[6] A[7] A_bar[7] clk_buf vdd gnd msf_address
.ENDS bank

.SUBCKT sram_1rw_32b_256w_1bank_scn3me_subm DATA[0] DATA[1] DATA[2] DATA[3] DATA[4] DATA[5] DATA[6] DATA[7] DATA[8] DATA[9] DATA[10] DATA[11] DATA[12] DATA[13] DATA[14] DATA[15] DATA[16] DATA[17] DATA[18] DATA[19] DATA[20] DATA[21] DATA[22] DATA[23] DATA[24] DATA[25] DATA[26] DATA[27] DATA[28] DATA[29] DATA[30] DATA[31] ADDR[0] ADDR[1] ADDR[2] ADDR[3] ADDR[4] ADDR[5] ADDR[6] ADDR[7] CSb WEb OEb clk vdd gnd
Xbank0 DATA[0] DATA[1] DATA[2] DATA[3] DATA[4] DATA[5] DATA[6] DATA[7] DATA[8] DATA[9] DATA[10] DATA[11] DATA[12] DATA[13] DATA[14] DATA[15] DATA[16] DATA[17] DATA[18] DATA[19] DATA[20] DATA[21] DATA[22] DATA[23] DATA[24] DATA[25] DATA[26] DATA[27] DATA[28] DATA[29] DATA[30] DATA[31] ADDR[0] ADDR[1] ADDR[2] ADDR[3] ADDR[4] ADDR[5] ADDR[6] ADDR[7] s_en w_en tri_en_bar tri_en clk_bar clk_buf vdd gnd bank
Xcontrol CSb WEb OEb clk s_en w_en tri_en tri_en_bar clk_bar clk_buf vdd gnd control_logic
.ENDS sram_1rw_32b_256w_1bank_scn3me_subm
