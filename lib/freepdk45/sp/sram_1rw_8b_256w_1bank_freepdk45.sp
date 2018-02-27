**************************************************
* OpenRAM generated memory.
* Words: 256
* Data bits: 8
* Banks: 1
* Column mux: 4:1
**************************************************

* ptx M{0} {1} nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p

* ptx M{0} {1} pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p

.SUBCKT pnand2_1 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand2_pmos2 Z B vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand2_nmos1 Z B net1 gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
Mpnand2_nmos2 net1 A gnd gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
.ENDS pnand2_1

.SUBCKT pnand3_1 A B C Z vdd gnd
Mpnand3_pmos1 vdd A Z vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand3_pmos2 Z B vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand3_pmos3 Z C vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand3_nmos1 Z C net1 gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
Mpnand3_nmos2 net1 B net2 gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
Mpnand3_nmos3 net2 A gnd gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
.ENDS pnand3_1

* ptx M{0} {1} nmos_vtg m=1 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p

* ptx M{0} {1} pmos_vtg m=1 w=0.405u l=0.05u pd=0.91u ps=0.91u as=0.050625p ad=0.050625p

.SUBCKT pnor2_1 A B Z vdd gnd
Mpnor2_pmos1 vdd A net1 vdd pmos_vtg m=1 w=0.405u l=0.05u pd=0.91u ps=0.91u as=0.050625p ad=0.050625p
Mpnor2_pmos2 net1 B Z vdd pmos_vtg m=1 w=0.405u l=0.05u pd=0.91u ps=0.91u as=0.050625p ad=0.050625p
Mpnor2_nmos1 Z A gnd gnd nmos_vtg m=1 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p
Mpnor2_nmos2 Z B gnd gnd nmos_vtg m=1 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p
.ENDS pnor2_1

.SUBCKT pinv_1 A Z vdd gnd
Mpinv_pmos Z A vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpinv_nmos Z A gnd gnd nmos_vtg m=1 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p
.ENDS pinv_1

* ptx M{0} {1} nmos_vtg m=2 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p

* ptx M{0} {1} pmos_vtg m=2 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p

.SUBCKT pinv_2 A Z vdd gnd
Mpinv_pmos Z A vdd vdd pmos_vtg m=2 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpinv_nmos Z A gnd gnd nmos_vtg m=2 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p
.ENDS pinv_2

* ptx M{0} {1} nmos_vtg m=3 w=0.12u l=0.05u pd=0.34u ps=0.34u as=0.015p ad=0.015p

* ptx M{0} {1} pmos_vtg m=3 w=0.36u l=0.05u pd=0.82u ps=0.82u as=0.045p ad=0.045p

.SUBCKT pinv_3 A Z vdd gnd
Mpinv_pmos Z A vdd vdd pmos_vtg m=3 w=0.36u l=0.05u pd=0.82u ps=0.82u as=0.045p ad=0.045p
Mpinv_nmos Z A gnd gnd nmos_vtg m=3 w=0.12u l=0.05u pd=0.34u ps=0.34u as=0.015p ad=0.015p
.ENDS pinv_3

* ptx M{0} {1} nmos_vtg m=6 w=0.12u l=0.05u pd=0.34u ps=0.34u as=0.015p ad=0.015p

* ptx M{0} {1} pmos_vtg m=6 w=0.36u l=0.05u pd=0.82u ps=0.82u as=0.045p ad=0.045p

.SUBCKT pinv_4 A Z vdd gnd
Mpinv_pmos Z A vdd vdd pmos_vtg m=6 w=0.36u l=0.05u pd=0.82u ps=0.82u as=0.045p ad=0.045p
Mpinv_nmos Z A gnd gnd nmos_vtg m=6 w=0.12u l=0.05u pd=0.34u ps=0.34u as=0.015p ad=0.015p
.ENDS pinv_4

* ptx M{0} {1} nmos_vtg m=12 w=0.12u l=0.05u pd=0.34u ps=0.34u as=0.015p ad=0.015p

* ptx M{0} {1} pmos_vtg m=12 w=0.36u l=0.05u pd=0.82u ps=0.82u as=0.045p ad=0.045p

.SUBCKT pinv_5 A Z vdd gnd
Mpinv_pmos Z A vdd vdd pmos_vtg m=12 w=0.36u l=0.05u pd=0.82u ps=0.82u as=0.045p ad=0.045p
Mpinv_nmos Z A gnd gnd nmos_vtg m=12 w=0.12u l=0.05u pd=0.34u ps=0.34u as=0.015p ad=0.015p
.ENDS pinv_5
*master-slave flip-flop with both output and inverted ouput

.SUBCKT ms_flop din dout dout_bar clk vdd gnd
xmaster din mout mout_bar clk clk_bar vdd gnd dlatch
xslave mout_bar dout_bar dout clk_bar clk_nn vdd gnd dlatch
.ENDS flop

.SUBCKT dlatch din dout dout_bar clk clk_bar vdd gnd
*clk inverter
mPff1 clk_bar clk vdd vdd PMOS_VTG W=180.0n L=50n m=1
mNff1 clk_bar clk gnd gnd NMOS_VTG W=90n L=50n m=1

*transmission gate 1
mtmP1 din clk int1 vdd PMOS_VTG W=180.0n L=50n m=1
mtmN1 din clk_bar int1 gnd NMOS_VTG W=90n L=50n m=1

*foward inverter
mPff3 dout_bar int1 vdd vdd PMOS_VTG W=180.0n L=50n m=1
mNff3 dout_bar int1 gnd gnd NMOS_VTG W=90n L=50n m=1

*backward inverter
mPff4 dout dout_bar vdd vdd PMOS_VTG W=180.0n L=50n m=1
mNf4 dout dout_bar gnd gnd NMOS_VTG W=90n L=50n m=1

*transmission gate 2
mtmP2 int1 clk_bar dout vdd PMOS_VTG W=180.0n L=50n m=1
mtmN2 int1 clk dout gnd NMOS_VTG W=90n L=50n m=1
.ENDS dlatch


.SUBCKT msf_control din[0] din[1] din[2] dout[0] dout_bar[0] dout[1] dout_bar[1] dout[2] dout_bar[2] clk vdd gnd
XXdff0 din[0] dout[0] dout_bar[0] clk vdd gnd ms_flop
XXdff1 din[1] dout[1] dout_bar[1] clk vdd gnd ms_flop
XXdff2 din[2] dout[2] dout_bar[2] clk vdd gnd ms_flop
.ENDS msf_control

.SUBCKT replica_cell_6t bl br wl vdd gnd
MM3 bl wl gnd gnd NMOS_VTG W=135.00n L=50n
MM2 br wl net4 gnd NMOS_VTG W=135.00n L=50n
MM1 gnd net4 gnd gnd NMOS_VTG W=205.00n L=50n
MM0 net4 gnd gnd gnd NMOS_VTG W=205.00n L=50n
MM5 gnd net4 vdd vdd PMOS_VTG W=90n L=50n
MM4 net4 gnd vdd vdd PMOS_VTG W=90n L=50n
.ENDS replica_cell_6t


.SUBCKT cell_6t bl br wl vdd gnd
MM3 bl wl net10 gnd NMOS_VTG W=135.00n L=50n
MM2 br wl net4 gnd NMOS_VTG W=135.00n L=50n
MM1 net10 net4 gnd gnd NMOS_VTG W=205.00n L=50n
MM0 net4 net10 gnd gnd NMOS_VTG W=205.00n L=50n
MM5 net10 net4 vdd vdd PMOS_VTG W=90n L=50n
MM4 net4 net10 vdd vdd PMOS_VTG W=90n L=50n
.ENDS cell_6t


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
Mpinv_pmos Z A vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpinv_nmos Z A gnd gnd nmos_vtg m=1 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p
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
Mpinv_pmos Z A vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpinv_nmos Z A gnd gnd nmos_vtg m=1 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p
.ENDS pinv_7

* ptx M{0} {1} pmos_vtg m=1 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p

.SUBCKT replica_bitline en out vdd gnd
Xrbl_inv bl[0] out vdd gnd pinv_7
Mrbl_access_tx vdd delayed_en bl[0] vdd pmos_vtg m=1 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p
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

.SUBCKT bitcell_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] bl[8] br[8] bl[9] br[9] bl[10] br[10] bl[11] br[11] bl[12] br[12] bl[13] br[13] bl[14] br[14] bl[15] br[15] bl[16] br[16] bl[17] br[17] bl[18] br[18] bl[19] br[19] bl[20] br[20] bl[21] br[21] bl[22] br[22] bl[23] br[23] bl[24] br[24] bl[25] br[25] bl[26] br[26] bl[27] br[27] bl[28] br[28] bl[29] br[29] bl[30] br[30] bl[31] br[31] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] wl[16] wl[17] wl[18] wl[19] wl[20] wl[21] wl[22] wl[23] wl[24] wl[25] wl[26] wl[27] wl[28] wl[29] wl[30] wl[31] wl[32] wl[33] wl[34] wl[35] wl[36] wl[37] wl[38] wl[39] wl[40] wl[41] wl[42] wl[43] wl[44] wl[45] wl[46] wl[47] wl[48] wl[49] wl[50] wl[51] wl[52] wl[53] wl[54] wl[55] wl[56] wl[57] wl[58] wl[59] wl[60] wl[61] wl[62] wl[63] vdd gnd
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
.ENDS bitcell_array

* ptx M{0} {1} pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p

.SUBCKT precharge bl br en vdd
Mlower_pmos bl en BR vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mupper_pmos1 bl en vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mupper_pmos2 br en vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
.ENDS precharge

.SUBCKT precharge_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] bl[8] br[8] bl[9] br[9] bl[10] br[10] bl[11] br[11] bl[12] br[12] bl[13] br[13] bl[14] br[14] bl[15] br[15] bl[16] br[16] bl[17] br[17] bl[18] br[18] bl[19] br[19] bl[20] br[20] bl[21] br[21] bl[22] br[22] bl[23] br[23] bl[24] br[24] bl[25] br[25] bl[26] br[26] bl[27] br[27] bl[28] br[28] bl[29] br[29] bl[30] br[30] bl[31] br[31] en vdd
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
.ENDS precharge_array

* ptx M{0} {1} nmos_vtg m=1 w=0.72u l=0.05u pd=1.54u ps=1.54u as=0.09p ad=0.09p

.SUBCKT single_level_column_mux_8 bl br bl_out br_out sel gnd
Mmux_tx1 bl sel bl_out gnd nmos_vtg m=1 w=0.72u l=0.05u pd=1.54u ps=1.54u as=0.09p ad=0.09p
Mmux_tx2 br sel br_out gnd nmos_vtg m=1 w=0.72u l=0.05u pd=1.54u ps=1.54u as=0.09p ad=0.09p
.ENDS single_level_column_mux_8

.SUBCKT columnmux_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] bl[8] br[8] bl[9] br[9] bl[10] br[10] bl[11] br[11] bl[12] br[12] bl[13] br[13] bl[14] br[14] bl[15] br[15] bl[16] br[16] bl[17] br[17] bl[18] br[18] bl[19] br[19] bl[20] br[20] bl[21] br[21] bl[22] br[22] bl[23] br[23] bl[24] br[24] bl[25] br[25] bl[26] br[26] bl[27] br[27] bl[28] br[28] bl[29] br[29] bl[30] br[30] bl[31] br[31] sel[0] sel[1] sel[2] sel[3] bl_out[0] br_out[0] bl_out[1] br_out[1] bl_out[2] br_out[2] bl_out[3] br_out[3] bl_out[4] br_out[4] bl_out[5] br_out[5] bl_out[6] br_out[6] bl_out[7] br_out[7] gnd
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
.ENDS columnmux_array

.SUBCKT sense_amp bl br dout en vdd gnd
M_1 dout net_1 vdd vdd pmos_vtg w=540.0n l=50.0n
M_3 net_1 dout vdd vdd pmos_vtg w=540.0n l=50.0n
M_2 dout net_1 net_2 gnd nmos_vtg w=270.0n l=50.0n
M_8 net_1 dout net_2 gnd nmos_vtg w=270.0n l=50.0n
M_5 bl en dout vdd pmos_vtg w=720.0n l=50.0n
M_6 br en net_1 vdd pmos_vtg w=720.0n l=50.0n
M_7 net_2 en gnd gnd nmos_vtg w=270.0n l=50.0n
.ENDS sense_amp


.SUBCKT sense_amp_array data[0] bl[0] br[0] data[1] bl[4] br[4] data[2] bl[8] br[8] data[3] bl[12] br[12] data[4] bl[16] br[16] data[5] bl[20] br[20] data[6] bl[24] br[24] data[7] bl[28] br[28] en vdd gnd
Xsa_d0 bl[0] br[0] data[0] en vdd gnd sense_amp
Xsa_d4 bl[4] br[4] data[1] en vdd gnd sense_amp
Xsa_d8 bl[8] br[8] data[2] en vdd gnd sense_amp
Xsa_d12 bl[12] br[12] data[3] en vdd gnd sense_amp
Xsa_d16 bl[16] br[16] data[4] en vdd gnd sense_amp
Xsa_d20 bl[20] br[20] data[5] en vdd gnd sense_amp
Xsa_d24 bl[24] br[24] data[6] en vdd gnd sense_amp
Xsa_d28 bl[28] br[28] data[7] en vdd gnd sense_amp
.ENDS sense_amp_array

.SUBCKT write_driver din bl br en vdd gnd
*inverters for enable and data input
minP bl_bar din vdd vdd pmos_vtg w=360.000000n l=50.000000n
minN bl_bar din gnd gnd nmos_vtg w=180.000000n l=50.000000n
moutP en_bar en vdd vdd pmos_vtg w=360.000000n l=50.000000n
moutN en_bar en gnd gnd nmos_vtg w=180.000000n l=50.000000n

*tristate for BL
mout0P int1 bl_bar vdd vdd pmos_vtg w=360.000000n l=50.000000n
mout0P2 bl en_bar int1 vdd pmos_vtg w=360.000000n l=50.000000n
mout0N bl en int2 gnd nmos_vtg w=180.000000n l=50.000000n
mout0N2 int2 bl_bar gnd gnd nmos_vtg w=180.000000n l=50.000000n

*tristate for BR
mout1P int3 din vdd vdd pmos_vtg w=360.000000n l=50.000000n
mout1P2 br en_bar int3 vdd pmos_vtg w=360.000000n l=50.000000n
mout1N br en int4 gnd nmos_vtg w=180.000000n l=50.000000n
mout1N2 int4 din gnd gnd nmos_vtg w=180.000000n l=50.000000n
.ENDS write_driver


.SUBCKT write_driver_array data[0] data[1] data[2] data[3] data[4] data[5] data[6] data[7] bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] en vdd gnd
XXwrite_driver0 data[0] bl[0] br[0] en vdd gnd write_driver
XXwrite_driver4 data[1] bl[1] br[1] en vdd gnd write_driver
XXwrite_driver8 data[2] bl[2] br[2] en vdd gnd write_driver
XXwrite_driver12 data[3] bl[3] br[3] en vdd gnd write_driver
XXwrite_driver16 data[4] bl[4] br[4] en vdd gnd write_driver
XXwrite_driver20 data[5] bl[5] br[5] en vdd gnd write_driver
XXwrite_driver24 data[6] bl[6] br[6] en vdd gnd write_driver
XXwrite_driver28 data[7] bl[7] br[7] en vdd gnd write_driver
.ENDS write_driver_array

.SUBCKT pinv_8 A Z vdd gnd
Mpinv_pmos Z A vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpinv_nmos Z A gnd gnd nmos_vtg m=1 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p
.ENDS pinv_8

.SUBCKT pnand2_2 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand2_pmos2 Z B vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand2_nmos1 Z B net1 gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
Mpnand2_nmos2 net1 A gnd gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
.ENDS pnand2_2

.SUBCKT pnand3_2 A B C Z vdd gnd
Mpnand3_pmos1 vdd A Z vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand3_pmos2 Z B vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand3_pmos3 Z C vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand3_nmos1 Z C net1 gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
Mpnand3_nmos2 net1 B net2 gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
Mpnand3_nmos3 net2 A gnd gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
.ENDS pnand3_2

.SUBCKT pinv_9 A Z vdd gnd
Mpinv_pmos Z A vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpinv_nmos Z A gnd gnd nmos_vtg m=1 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p
.ENDS pinv_9

.SUBCKT pnand2_3 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand2_pmos2 Z B vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand2_nmos1 Z B net1 gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
Mpnand2_nmos2 net1 A gnd gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
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
Mpinv_pmos Z A vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpinv_nmos Z A gnd gnd nmos_vtg m=1 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p
.ENDS pinv_10

.SUBCKT pnand3_3 A B C Z vdd gnd
Mpnand3_pmos1 vdd A Z vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand3_pmos2 Z B vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand3_pmos3 Z C vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand3_nmos1 Z C net1 gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
Mpnand3_nmos2 net1 B net2 gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
Mpnand3_nmos3 net2 A gnd gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
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

.SUBCKT msf_data_in din[0] din[1] din[2] din[3] din[4] din[5] din[6] din[7] dout[0] dout_bar[0] dout[1] dout_bar[1] dout[2] dout_bar[2] dout[3] dout_bar[3] dout[4] dout_bar[4] dout[5] dout_bar[5] dout[6] dout_bar[6] dout[7] dout_bar[7] clk vdd gnd
XXdff0 din[0] dout[0] dout_bar[0] clk vdd gnd ms_flop
XXdff4 din[1] dout[1] dout_bar[1] clk vdd gnd ms_flop
XXdff8 din[2] dout[2] dout_bar[2] clk vdd gnd ms_flop
XXdff12 din[3] dout[3] dout_bar[3] clk vdd gnd ms_flop
XXdff16 din[4] dout[4] dout_bar[4] clk vdd gnd ms_flop
XXdff20 din[5] dout[5] dout_bar[5] clk vdd gnd ms_flop
XXdff24 din[6] dout[6] dout_bar[6] clk vdd gnd ms_flop
XXdff28 din[7] dout[7] dout_bar[7] clk vdd gnd ms_flop
.ENDS msf_data_in

.SUBCKT tri_gate in out en en_bar vdd gnd
M_1 net_2 in_inv gnd gnd NMOS_VTG W=180.000000n L=50.000000n
M_2 out en net_2 gnd NMOS_VTG W=180.000000n L=50.000000n
M_3 net_3 in_inv vdd vdd PMOS_VTG W=360.000000n L=50.000000n
M_4 out en_bar net_3 vdd PMOS_VTG W=360.000000n L=50.000000n
M_5 in_inv in vdd vdd PMOS_VTG W=180.000000n L=50.000000n
M_6 in_inv in gnd gnd NMOS_VTG W=90.000000n L=50.000000n
.ENDS


.SUBCKT tri_gate_array in[0] in[1] in[2] in[3] in[4] in[5] in[6] in[7] out[0] out[1] out[2] out[3] out[4] out[5] out[6] out[7] en en_bar vdd gnd
XXtri_gate0 in[0] out[0] en en_bar vdd gnd tri_gate
XXtri_gate4 in[1] out[1] en en_bar vdd gnd tri_gate
XXtri_gate8 in[2] out[2] en en_bar vdd gnd tri_gate
XXtri_gate12 in[3] out[3] en en_bar vdd gnd tri_gate
XXtri_gate16 in[4] out[4] en en_bar vdd gnd tri_gate
XXtri_gate20 in[5] out[5] en en_bar vdd gnd tri_gate
XXtri_gate24 in[6] out[6] en en_bar vdd gnd tri_gate
XXtri_gate28 in[7] out[7] en en_bar vdd gnd tri_gate
.ENDS tri_gate_array

.SUBCKT pinv_11 A Z vdd gnd
Mpinv_pmos Z A vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpinv_nmos Z A gnd gnd nmos_vtg m=1 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p
.ENDS pinv_11

.SUBCKT pinv_12 A Z vdd gnd
Mpinv_pmos Z A vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpinv_nmos Z A gnd gnd nmos_vtg m=1 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p
.ENDS pinv_12

.SUBCKT pnand2_4 A B Z vdd gnd
Mpnand2_pmos1 vdd A Z vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand2_pmos2 Z B vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpnand2_nmos1 Z B net1 gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
Mpnand2_nmos2 net1 A gnd gnd nmos_vtg m=1 w=0.18u l=0.05u pd=0.46u ps=0.46u as=0.0225p ad=0.0225p
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
Mpinv_pmos Z A vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpinv_nmos Z A gnd gnd nmos_vtg m=1 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p
.ENDS pinv_13

.SUBCKT bank DATA[0] DATA[1] DATA[2] DATA[3] DATA[4] DATA[5] DATA[6] DATA[7] ADDR[0] ADDR[1] ADDR[2] ADDR[3] ADDR[4] ADDR[5] ADDR[6] ADDR[7] s_en w_en tri_en_bar tri_en clk_bar clk_buf vdd gnd
Xbitcell_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] bl[8] br[8] bl[9] br[9] bl[10] br[10] bl[11] br[11] bl[12] br[12] bl[13] br[13] bl[14] br[14] bl[15] br[15] bl[16] br[16] bl[17] br[17] bl[18] br[18] bl[19] br[19] bl[20] br[20] bl[21] br[21] bl[22] br[22] bl[23] br[23] bl[24] br[24] bl[25] br[25] bl[26] br[26] bl[27] br[27] bl[28] br[28] bl[29] br[29] bl[30] br[30] bl[31] br[31] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] wl[16] wl[17] wl[18] wl[19] wl[20] wl[21] wl[22] wl[23] wl[24] wl[25] wl[26] wl[27] wl[28] wl[29] wl[30] wl[31] wl[32] wl[33] wl[34] wl[35] wl[36] wl[37] wl[38] wl[39] wl[40] wl[41] wl[42] wl[43] wl[44] wl[45] wl[46] wl[47] wl[48] wl[49] wl[50] wl[51] wl[52] wl[53] wl[54] wl[55] wl[56] wl[57] wl[58] wl[59] wl[60] wl[61] wl[62] wl[63] vdd gnd bitcell_array
Xprecharge_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] bl[8] br[8] bl[9] br[9] bl[10] br[10] bl[11] br[11] bl[12] br[12] bl[13] br[13] bl[14] br[14] bl[15] br[15] bl[16] br[16] bl[17] br[17] bl[18] br[18] bl[19] br[19] bl[20] br[20] bl[21] br[21] bl[22] br[22] bl[23] br[23] bl[24] br[24] bl[25] br[25] bl[26] br[26] bl[27] br[27] bl[28] br[28] bl[29] br[29] bl[30] br[30] bl[31] br[31] clk_bar vdd precharge_array
Xcolumn_mux_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] bl[8] br[8] bl[9] br[9] bl[10] br[10] bl[11] br[11] bl[12] br[12] bl[13] br[13] bl[14] br[14] bl[15] br[15] bl[16] br[16] bl[17] br[17] bl[18] br[18] bl[19] br[19] bl[20] br[20] bl[21] br[21] bl[22] br[22] bl[23] br[23] bl[24] br[24] bl[25] br[25] bl[26] br[26] bl[27] br[27] bl[28] br[28] bl[29] br[29] bl[30] br[30] bl[31] br[31] sel[0] sel[1] sel[2] sel[3] bl_out[0] br_out[0] bl_out[1] br_out[1] bl_out[2] br_out[2] bl_out[3] br_out[3] bl_out[4] br_out[4] bl_out[5] br_out[5] bl_out[6] br_out[6] bl_out[7] br_out[7] gnd columnmux_array
Xcol_address_decoder A[6] A[7] sel[0] sel[1] sel[2] sel[3] vdd gnd pre2x4
Xsense_amp_array data_out[0] bl_out[0] br_out[0] data_out[1] bl_out[1] br_out[1] data_out[2] bl_out[2] br_out[2] data_out[3] bl_out[3] br_out[3] data_out[4] bl_out[4] br_out[4] data_out[5] bl_out[5] br_out[5] data_out[6] bl_out[6] br_out[6] data_out[7] bl_out[7] br_out[7] s_en vdd gnd sense_amp_array
Xwrite_driver_array data_in[0] data_in[1] data_in[2] data_in[3] data_in[4] data_in[5] data_in[6] data_in[7] bl_out[0] br_out[0] bl_out[1] br_out[1] bl_out[2] br_out[2] bl_out[3] br_out[3] bl_out[4] br_out[4] bl_out[5] br_out[5] bl_out[6] br_out[6] bl_out[7] br_out[7] w_en vdd gnd write_driver_array
Xdata_in_flop_array DATA[0] DATA[1] DATA[2] DATA[3] DATA[4] DATA[5] DATA[6] DATA[7] data_in[0] data_in_bar[0] data_in[1] data_in_bar[1] data_in[2] data_in_bar[2] data_in[3] data_in_bar[3] data_in[4] data_in_bar[4] data_in[5] data_in_bar[5] data_in[6] data_in_bar[6] data_in[7] data_in_bar[7] clk_bar vdd gnd msf_data_in
Xtri_gate_array data_out[0] data_out[1] data_out[2] data_out[3] data_out[4] data_out[5] data_out[6] data_out[7] DATA[0] DATA[1] DATA[2] DATA[3] DATA[4] DATA[5] DATA[6] DATA[7] tri_en tri_en_bar vdd gnd tri_gate_array
Xrow_decoder A[0] A[1] A[2] A[3] A[4] A[5] dec_out[0] dec_out[1] dec_out[2] dec_out[3] dec_out[4] dec_out[5] dec_out[6] dec_out[7] dec_out[8] dec_out[9] dec_out[10] dec_out[11] dec_out[12] dec_out[13] dec_out[14] dec_out[15] dec_out[16] dec_out[17] dec_out[18] dec_out[19] dec_out[20] dec_out[21] dec_out[22] dec_out[23] dec_out[24] dec_out[25] dec_out[26] dec_out[27] dec_out[28] dec_out[29] dec_out[30] dec_out[31] dec_out[32] dec_out[33] dec_out[34] dec_out[35] dec_out[36] dec_out[37] dec_out[38] dec_out[39] dec_out[40] dec_out[41] dec_out[42] dec_out[43] dec_out[44] dec_out[45] dec_out[46] dec_out[47] dec_out[48] dec_out[49] dec_out[50] dec_out[51] dec_out[52] dec_out[53] dec_out[54] dec_out[55] dec_out[56] dec_out[57] dec_out[58] dec_out[59] dec_out[60] dec_out[61] dec_out[62] dec_out[63] vdd gnd hierarchical_decoder_64rows
Xwordline_driver dec_out[0] dec_out[1] dec_out[2] dec_out[3] dec_out[4] dec_out[5] dec_out[6] dec_out[7] dec_out[8] dec_out[9] dec_out[10] dec_out[11] dec_out[12] dec_out[13] dec_out[14] dec_out[15] dec_out[16] dec_out[17] dec_out[18] dec_out[19] dec_out[20] dec_out[21] dec_out[22] dec_out[23] dec_out[24] dec_out[25] dec_out[26] dec_out[27] dec_out[28] dec_out[29] dec_out[30] dec_out[31] dec_out[32] dec_out[33] dec_out[34] dec_out[35] dec_out[36] dec_out[37] dec_out[38] dec_out[39] dec_out[40] dec_out[41] dec_out[42] dec_out[43] dec_out[44] dec_out[45] dec_out[46] dec_out[47] dec_out[48] dec_out[49] dec_out[50] dec_out[51] dec_out[52] dec_out[53] dec_out[54] dec_out[55] dec_out[56] dec_out[57] dec_out[58] dec_out[59] dec_out[60] dec_out[61] dec_out[62] dec_out[63] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] wl[16] wl[17] wl[18] wl[19] wl[20] wl[21] wl[22] wl[23] wl[24] wl[25] wl[26] wl[27] wl[28] wl[29] wl[30] wl[31] wl[32] wl[33] wl[34] wl[35] wl[36] wl[37] wl[38] wl[39] wl[40] wl[41] wl[42] wl[43] wl[44] wl[45] wl[46] wl[47] wl[48] wl[49] wl[50] wl[51] wl[52] wl[53] wl[54] wl[55] wl[56] wl[57] wl[58] wl[59] wl[60] wl[61] wl[62] wl[63] clk_buf vdd gnd wordline_driver
Xaddress_flop_array ADDR[0] ADDR[1] ADDR[2] ADDR[3] ADDR[4] ADDR[5] ADDR[6] ADDR[7] A[0] A_bar[0] A[1] A_bar[1] A[2] A_bar[2] A[3] A_bar[3] A[4] A_bar[4] A[5] A_bar[5] A[6] A_bar[6] A[7] A_bar[7] clk_buf vdd gnd msf_address
.ENDS bank

.SUBCKT sram_1rw_8b_256w_1bank_freepdk45 DATA[0] DATA[1] DATA[2] DATA[3] DATA[4] DATA[5] DATA[6] DATA[7] ADDR[0] ADDR[1] ADDR[2] ADDR[3] ADDR[4] ADDR[5] ADDR[6] ADDR[7] CSb WEb OEb clk vdd gnd
Xbank0 DATA[0] DATA[1] DATA[2] DATA[3] DATA[4] DATA[5] DATA[6] DATA[7] ADDR[0] ADDR[1] ADDR[2] ADDR[3] ADDR[4] ADDR[5] ADDR[6] ADDR[7] s_en w_en tri_en_bar tri_en clk_bar clk_buf vdd gnd bank
Xcontrol CSb WEb OEb clk s_en w_en tri_en tri_en_bar clk_bar clk_buf vdd gnd control_logic
.ENDS sram_1rw_8b_256w_1bank_freepdk45
