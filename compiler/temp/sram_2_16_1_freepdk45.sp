**************************************************
* OpenRAM generated memory.
* Words: 128
* Data bits: 2
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


.SUBCKT bitline_load bl[0] br[0] wl[0] wl[1] wl[2] wl[3] vdd gnd
Xbit_r0_c0 bl[0] br[0] wl[0] vdd gnd cell_6t
Xbit_r1_c0 bl[0] br[0] wl[1] vdd gnd cell_6t
Xbit_r2_c0 bl[0] br[0] wl[2] vdd gnd cell_6t
Xbit_r3_c0 bl[0] br[0] wl[3] vdd gnd cell_6t
.ENDS bitline_load

.SUBCKT pinv_6 A Z vdd gnd
Mpinv_pmos Z A vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpinv_nmos Z A gnd gnd nmos_vtg m=1 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p
.ENDS pinv_6

.SUBCKT delay_chain in out vdd gnd
Xdinv0 in s1 vdd gnd pinv_6
Xdinv1 s1 s2n1 vdd gnd pinv_6
Xdinv2 s1 s2n2 vdd gnd pinv_6
Xdinv3 s1 s2n3 vdd gnd pinv_6
Xdinv4 s1 s2 vdd gnd pinv_6
Xdinv5 s2 s3n1 vdd gnd pinv_6
Xdinv6 s2 s3n2 vdd gnd pinv_6
Xdinv7 s2 s3n3 vdd gnd pinv_6
Xdinv8 s2 s3 vdd gnd pinv_6
Xdinv9 s3 s4n1 vdd gnd pinv_6
Xdinv10 s3 s4n2 vdd gnd pinv_6
Xdinv11 s3 s4n3 vdd gnd pinv_6
Xdinv12 s3 s4 vdd gnd pinv_6
Xdinv13 s4 s5n1 vdd gnd pinv_6
Xdinv14 s4 s5n2 vdd gnd pinv_6
Xdinv15 s4 s5n3 vdd gnd pinv_6
Xdinv16 s4 s5 vdd gnd pinv_6
Xdinv17 s5 s6n1 vdd gnd pinv_6
Xdinv18 s5 s6n2 vdd gnd pinv_6
Xdinv19 s5 s6n3 vdd gnd pinv_6
Xdinv20 s5 s6 vdd gnd pinv_6
Xdinv21 s6 s7n1 vdd gnd pinv_6
Xdinv22 s6 s7n2 vdd gnd pinv_6
Xdinv23 s6 s7n3 vdd gnd pinv_6
Xdinv24 s6 s7 vdd gnd pinv_6
Xdinv25 s7 s8n1 vdd gnd pinv_6
Xdinv26 s7 s8n2 vdd gnd pinv_6
Xdinv27 s7 s8n3 vdd gnd pinv_6
Xdinv28 s7 s8 vdd gnd pinv_6
Xdinv29 s8 s9n1 vdd gnd pinv_6
Xdinv30 s8 s9n2 vdd gnd pinv_6
Xdinv31 s8 s9n3 vdd gnd pinv_6
Xdinv32 s8 out vdd gnd pinv_6
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
Xload bl[0] br[0] gnd gnd gnd gnd vdd gnd bitline_load
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

.SUBCKT bitcell_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] wl[16] wl[17] wl[18] wl[19] wl[20] wl[21] wl[22] wl[23] wl[24] wl[25] wl[26] wl[27] wl[28] wl[29] wl[30] wl[31] vdd gnd
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
.ENDS bitcell_array

* ptx M{0} {1} pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p

.SUBCKT precharge bl br en vdd
Mlower_pmos bl en BR vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mupper_pmos1 bl en vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mupper_pmos2 br en vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
.ENDS precharge

.SUBCKT precharge_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] en vdd
Xpre_column_0 bl[0] br[0] en vdd precharge
Xpre_column_1 bl[1] br[1] en vdd precharge
Xpre_column_2 bl[2] br[2] en vdd precharge
Xpre_column_3 bl[3] br[3] en vdd precharge
Xpre_column_4 bl[4] br[4] en vdd precharge
Xpre_column_5 bl[5] br[5] en vdd precharge
Xpre_column_6 bl[6] br[6] en vdd precharge
Xpre_column_7 bl[7] br[7] en vdd precharge
.ENDS precharge_array

* ptx M{0} {1} nmos_vtg m=1 w=0.72u l=0.05u pd=1.54u ps=1.54u as=0.09p ad=0.09p

.SUBCKT single_level_column_mux_8 bl br bl_out br_out sel gnd
Mmux_tx1 bl sel bl_out gnd nmos_vtg m=1 w=0.72u l=0.05u pd=1.54u ps=1.54u as=0.09p ad=0.09p
Mmux_tx2 br sel br_out gnd nmos_vtg m=1 w=0.72u l=0.05u pd=1.54u ps=1.54u as=0.09p ad=0.09p
.ENDS single_level_column_mux_8

.SUBCKT columnmux_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] sel[0] sel[1] sel[2] sel[3] bl_out[0] br_out[0] bl_out[1] br_out[1] gnd
XXMUX0 bl[0] br[0] bl_out[0] br_out[0] sel[0] gnd single_level_column_mux_8
XXMUX1 bl[1] br[1] bl_out[0] br_out[0] sel[1] gnd single_level_column_mux_8
XXMUX2 bl[2] br[2] bl_out[0] br_out[0] sel[2] gnd single_level_column_mux_8
XXMUX3 bl[3] br[3] bl_out[0] br_out[0] sel[3] gnd single_level_column_mux_8
XXMUX4 bl[4] br[4] bl_out[1] br_out[1] sel[0] gnd single_level_column_mux_8
XXMUX5 bl[5] br[5] bl_out[1] br_out[1] sel[1] gnd single_level_column_mux_8
XXMUX6 bl[6] br[6] bl_out[1] br_out[1] sel[2] gnd single_level_column_mux_8
XXMUX7 bl[7] br[7] bl_out[1] br_out[1] sel[3] gnd single_level_column_mux_8
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


.SUBCKT sense_amp_array data[0] bl[0] br[0] data[1] bl[4] br[4] en vdd gnd
Xsa_d0 bl[0] br[0] data[0] en vdd gnd sense_amp
Xsa_d4 bl[4] br[4] data[1] en vdd gnd sense_amp
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


.SUBCKT write_driver_array data[0] data[1] bl[0] br[0] bl[1] br[1] en vdd gnd
XXwrite_driver0 data[0] bl[0] br[0] en vdd gnd write_driver
XXwrite_driver4 data[1] bl[1] br[1] en vdd gnd write_driver
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

.SUBCKT hierarchical_decoder_32rows A[0] A[1] A[2] A[3] A[4] decode[0] decode[1] decode[2] decode[3] decode[4] decode[5] decode[6] decode[7] decode[8] decode[9] decode[10] decode[11] decode[12] decode[13] decode[14] decode[15] decode[16] decode[17] decode[18] decode[19] decode[20] decode[21] decode[22] decode[23] decode[24] decode[25] decode[26] decode[27] decode[28] decode[29] decode[30] decode[31] vdd gnd
Xpre[0] A[0] A[1] out[0] out[1] out[2] out[3] vdd gnd pre2x4
Xpre3x8[0] A[2] A[3] A[4] out[4] out[5] out[6] out[7] out[8] out[9] out[10] out[11] vdd gnd pre3x8
XDEC_NAND[0] out[0] out[4] Z[0] vdd gnd pnand2_2
XDEC_NAND[1] out[0] out[5] Z[1] vdd gnd pnand2_2
XDEC_NAND[2] out[0] out[6] Z[2] vdd gnd pnand2_2
XDEC_NAND[3] out[0] out[7] Z[3] vdd gnd pnand2_2
XDEC_NAND[4] out[0] out[8] Z[4] vdd gnd pnand2_2
XDEC_NAND[5] out[0] out[9] Z[5] vdd gnd pnand2_2
XDEC_NAND[6] out[0] out[10] Z[6] vdd gnd pnand2_2
XDEC_NAND[7] out[0] out[11] Z[7] vdd gnd pnand2_2
XDEC_NAND[8] out[1] out[4] Z[8] vdd gnd pnand2_2
XDEC_NAND[9] out[1] out[5] Z[9] vdd gnd pnand2_2
XDEC_NAND[10] out[1] out[6] Z[10] vdd gnd pnand2_2
XDEC_NAND[11] out[1] out[7] Z[11] vdd gnd pnand2_2
XDEC_NAND[12] out[1] out[8] Z[12] vdd gnd pnand2_2
XDEC_NAND[13] out[1] out[9] Z[13] vdd gnd pnand2_2
XDEC_NAND[14] out[1] out[10] Z[14] vdd gnd pnand2_2
XDEC_NAND[15] out[1] out[11] Z[15] vdd gnd pnand2_2
XDEC_NAND[16] out[2] out[4] Z[16] vdd gnd pnand2_2
XDEC_NAND[17] out[2] out[5] Z[17] vdd gnd pnand2_2
XDEC_NAND[18] out[2] out[6] Z[18] vdd gnd pnand2_2
XDEC_NAND[19] out[2] out[7] Z[19] vdd gnd pnand2_2
XDEC_NAND[20] out[2] out[8] Z[20] vdd gnd pnand2_2
XDEC_NAND[21] out[2] out[9] Z[21] vdd gnd pnand2_2
XDEC_NAND[22] out[2] out[10] Z[22] vdd gnd pnand2_2
XDEC_NAND[23] out[2] out[11] Z[23] vdd gnd pnand2_2
XDEC_NAND[24] out[3] out[4] Z[24] vdd gnd pnand2_2
XDEC_NAND[25] out[3] out[5] Z[25] vdd gnd pnand2_2
XDEC_NAND[26] out[3] out[6] Z[26] vdd gnd pnand2_2
XDEC_NAND[27] out[3] out[7] Z[27] vdd gnd pnand2_2
XDEC_NAND[28] out[3] out[8] Z[28] vdd gnd pnand2_2
XDEC_NAND[29] out[3] out[9] Z[29] vdd gnd pnand2_2
XDEC_NAND[30] out[3] out[10] Z[30] vdd gnd pnand2_2
XDEC_NAND[31] out[3] out[11] Z[31] vdd gnd pnand2_2
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
.ENDS hierarchical_decoder_32rows

.SUBCKT msf_address din[0] din[1] din[2] din[3] din[4] din[5] din[6] dout[0] dout_bar[0] dout[1] dout_bar[1] dout[2] dout_bar[2] dout[3] dout_bar[3] dout[4] dout_bar[4] dout[5] dout_bar[5] dout[6] dout_bar[6] clk vdd gnd
XXdff0 din[0] dout[0] dout_bar[0] clk vdd gnd ms_flop
XXdff1 din[1] dout[1] dout_bar[1] clk vdd gnd ms_flop
XXdff2 din[2] dout[2] dout_bar[2] clk vdd gnd ms_flop
XXdff3 din[3] dout[3] dout_bar[3] clk vdd gnd ms_flop
XXdff4 din[4] dout[4] dout_bar[4] clk vdd gnd ms_flop
XXdff5 din[5] dout[5] dout_bar[5] clk vdd gnd ms_flop
XXdff6 din[6] dout[6] dout_bar[6] clk vdd gnd ms_flop
.ENDS msf_address

.SUBCKT msf_data_in din[0] din[1] dout[0] dout_bar[0] dout[1] dout_bar[1] clk vdd gnd
XXdff0 din[0] dout[0] dout_bar[0] clk vdd gnd ms_flop
XXdff4 din[1] dout[1] dout_bar[1] clk vdd gnd ms_flop
.ENDS msf_data_in

.SUBCKT tri_gate in out en en_bar vdd gnd
M_1 net_2 in_inv gnd gnd NMOS_VTG W=180.000000n L=50.000000n
M_2 out en net_2 gnd NMOS_VTG W=180.000000n L=50.000000n
M_3 net_3 in_inv vdd vdd PMOS_VTG W=360.000000n L=50.000000n
M_4 out en_bar net_3 vdd PMOS_VTG W=360.000000n L=50.000000n
M_5 in_inv in vdd vdd PMOS_VTG W=180.000000n L=50.000000n
M_6 in_inv in gnd gnd NMOS_VTG W=90.000000n L=50.000000n
.ENDS


.SUBCKT tri_gate_array in[0] in[1] out[0] out[1] en en_bar vdd gnd
XXtri_gate0 in[0] out[0] en en_bar vdd gnd tri_gate
XXtri_gate4 in[1] out[1] en en_bar vdd gnd tri_gate
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

.SUBCKT wordline_driver in[0] in[1] in[2] in[3] in[4] in[5] in[6] in[7] in[8] in[9] in[10] in[11] in[12] in[13] in[14] in[15] in[16] in[17] in[18] in[19] in[20] in[21] in[22] in[23] in[24] in[25] in[26] in[27] in[28] in[29] in[30] in[31] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] wl[16] wl[17] wl[18] wl[19] wl[20] wl[21] wl[22] wl[23] wl[24] wl[25] wl[26] wl[27] wl[28] wl[29] wl[30] wl[31] en vdd gnd
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
.ENDS wordline_driver

.SUBCKT pinv_13 A Z vdd gnd
Mpinv_pmos Z A vdd vdd pmos_vtg m=1 w=0.27u l=0.05u pd=0.64u ps=0.64u as=0.03375p ad=0.03375p
Mpinv_nmos Z A gnd gnd nmos_vtg m=1 w=0.09u l=0.05u pd=0.28u ps=0.28u as=0.01125p ad=0.01125p
.ENDS pinv_13

.SUBCKT bank DATA[0] DATA[1] ADDR[0] ADDR[1] ADDR[2] ADDR[3] ADDR[4] ADDR[5] ADDR[6] s_en w_en tri_en_bar tri_en clk_bar clk_buf vdd gnd
Xbitcell_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] wl[16] wl[17] wl[18] wl[19] wl[20] wl[21] wl[22] wl[23] wl[24] wl[25] wl[26] wl[27] wl[28] wl[29] wl[30] wl[31] vdd gnd bitcell_array
Xprecharge_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] clk_bar vdd precharge_array
Xcolumn_mux_array bl[0] br[0] bl[1] br[1] bl[2] br[2] bl[3] br[3] bl[4] br[4] bl[5] br[5] bl[6] br[6] bl[7] br[7] sel[0] sel[1] sel[2] sel[3] bl_out[0] br_out[0] bl_out[1] br_out[1] gnd columnmux_array
Xcol_address_decoder A[5] A[6] sel[0] sel[1] sel[2] sel[3] vdd gnd pre2x4
Xsense_amp_array data_out[0] bl_out[0] br_out[0] data_out[1] bl_out[1] br_out[1] s_en vdd gnd sense_amp_array
Xwrite_driver_array data_in[0] data_in[1] bl_out[0] br_out[0] bl_out[1] br_out[1] w_en vdd gnd write_driver_array
Xdata_in_flop_array DATA[0] DATA[1] data_in[0] data_in_bar[0] data_in[1] data_in_bar[1] clk_bar vdd gnd msf_data_in
Xtri_gate_array data_out[0] data_out[1] DATA[0] DATA[1] tri_en tri_en_bar vdd gnd tri_gate_array
Xrow_decoder A[0] A[1] A[2] A[3] A[4] dec_out[0] dec_out[1] dec_out[2] dec_out[3] dec_out[4] dec_out[5] dec_out[6] dec_out[7] dec_out[8] dec_out[9] dec_out[10] dec_out[11] dec_out[12] dec_out[13] dec_out[14] dec_out[15] dec_out[16] dec_out[17] dec_out[18] dec_out[19] dec_out[20] dec_out[21] dec_out[22] dec_out[23] dec_out[24] dec_out[25] dec_out[26] dec_out[27] dec_out[28] dec_out[29] dec_out[30] dec_out[31] vdd gnd hierarchical_decoder_32rows
Xwordline_driver dec_out[0] dec_out[1] dec_out[2] dec_out[3] dec_out[4] dec_out[5] dec_out[6] dec_out[7] dec_out[8] dec_out[9] dec_out[10] dec_out[11] dec_out[12] dec_out[13] dec_out[14] dec_out[15] dec_out[16] dec_out[17] dec_out[18] dec_out[19] dec_out[20] dec_out[21] dec_out[22] dec_out[23] dec_out[24] dec_out[25] dec_out[26] dec_out[27] dec_out[28] dec_out[29] dec_out[30] dec_out[31] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] wl[16] wl[17] wl[18] wl[19] wl[20] wl[21] wl[22] wl[23] wl[24] wl[25] wl[26] wl[27] wl[28] wl[29] wl[30] wl[31] clk_buf vdd gnd wordline_driver
Xaddress_flop_array ADDR[0] ADDR[1] ADDR[2] ADDR[3] ADDR[4] ADDR[5] ADDR[6] A[0] A_bar[0] A[1] A_bar[1] A[2] A_bar[2] A[3] A_bar[3] A[4] A_bar[4] A[5] A_bar[5] A[6] A_bar[6] clk_buf vdd gnd msf_address
.ENDS bank

.SUBCKT sram_2_16_1_freepdk45 DATA[0] DATA[1] ADDR[0] ADDR[1] ADDR[2] ADDR[3] ADDR[4] ADDR[5] ADDR[6] CSb WEb OEb clk vdd gnd
Xbank0 DATA[0] DATA[1] ADDR[0] ADDR[1] ADDR[2] ADDR[3] ADDR[4] ADDR[5] ADDR[6] s_en w_en tri_en_bar tri_en clk_bar clk_buf vdd gnd bank
Xcontrol CSb WEb OEb clk s_en w_en tri_en tri_en_bar clk_bar clk_buf vdd gnd control_logic
.ENDS sram_2_16_1_freepdk45
