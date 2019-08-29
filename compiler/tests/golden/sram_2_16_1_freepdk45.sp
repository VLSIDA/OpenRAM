* OpenRAM generated memory.
* User: mrg
.global vdd gnd
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


.SUBCKT inv_nmos11 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.09u l=0.05u
.ENDS inv_nmos11

.SUBCKT inv_pmos12 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.27u l=0.05u
.ENDS inv_pmos12

.SUBCKT pinv A Z vdd gnd
Xpinv_nmos Z A gnd gnd inv_nmos11
Xpinv_pmos Z A vdd vdd inv_pmos12
.ENDS pinv

.SUBCKT nand_2_nmos13 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_2_nmos13

.SUBCKT nand_2_nmos24 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_2_nmos24

.SUBCKT nand_2_pmos15 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_2_pmos15

.SUBCKT nand_2_pmos26 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_2_pmos26

.SUBCKT nand2 A B Z vdd gnd
Xnmos1 Z A net1 gnd nand_2_nmos13
Xnmos2 net1 B gnd gnd nand_2_nmos24
Xpmos1 vdd A Z vdd nand_2_pmos15
Xpmos2 Z B vdd vdd nand_2_pmos26
.ENDS nand2

.SUBCKT nand_3_nmos17 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.27u l=0.05u
.ENDS nand_3_nmos17

.SUBCKT nand_3_nmos28 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.27u l=0.05u
.ENDS nand_3_nmos28

.SUBCKT nand_3_nmos39 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.27u l=0.05u
.ENDS nand_3_nmos39

.SUBCKT nand_3_pmos110 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_3_pmos110

.SUBCKT nand_3_pmos211 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_3_pmos211

.SUBCKT nand_3_pmos312 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_3_pmos312

.SUBCKT NAND3 A B C Z vdd gnd
Xnmos1 net2 A gnd gnd nand_3_nmos17
Xnmos2 net1 B net2 gnd nand_3_nmos28
Xnmos3 Z C net1 gnd nand_3_nmos39
Xpmos1 Z A vdd vdd nand_3_pmos110
Xpmos2 vdd B Z vdd nand_3_pmos211
Xpmos3 Z C vdd vdd nand_3_pmos312
.ENDS NAND3

.SUBCKT inv_nmos113 D G S B
Mnmos D G S B nmos_vtg m=4 w=0.09u l=0.05u
.ENDS inv_nmos113

.SUBCKT inv_pmos114 D G S B
Mpmos D G S B pmos_vtg m=4 w=0.27u l=0.05u
.ENDS inv_pmos114

.SUBCKT pinv4 A Z vdd gnd
Xpinv_nmos Z A gnd gnd inv_nmos113
Xpinv_pmos Z A vdd vdd inv_pmos114
.ENDS pinv4

.SUBCKT nor_2_nmos119 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.09u l=0.05u
.ENDS nor_2_nmos119

.SUBCKT nor_2_nmos220 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.09u l=0.05u
.ENDS nor_2_nmos220

.SUBCKT nor_2_pmos121 D G S B
Mpmos D G S B pmos_vtg m=2 w=0.18u l=0.05u
.ENDS nor_2_pmos121

.SUBCKT nor_2_pmos222 D G S B
Mpmos D G S B pmos_vtg m=2 w=0.18u l=0.05u
.ENDS nor_2_pmos222

.SUBCKT nor2 A B Z vdd gnd
Xnmos1 Z A gnd gnd nor_2_nmos119
Xnmos2 Z B gnd gnd nor_2_nmos220
Xpmos1 vdd A net1 vdd nor_2_pmos121
Xpmos2 net1 B Z vdd nor_2_pmos222
.ENDS nor2

.SUBCKT msf_control data[0] data[1] data[2] data_in[0] data_in_bar[0] data_in[1] data_in_bar[1] data_in[2] data_in_bar[2] clk vdd gnd
XXdff0 data[0] data_in[0] data_in_bar[0] clk vdd gnd ms_flop
XXdff1 data[1] data_in[1] data_in_bar[1] clk vdd gnd ms_flop
XXdff2 data[2] data_in[2] data_in_bar[2] clk vdd gnd ms_flop
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


.SUBCKT bitline_load bl[0] br[0] wl[0] wl[1] vdd gnd
Xbit_r0_c0 bl[0] br[0] wl[0] vdd gnd cell_6t
Xbit_r1_c0 bl[0] br[0] wl[1] vdd gnd cell_6t
.ENDS bitline_load

.SUBCKT inv_nmos123 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.09u l=0.05u
.ENDS inv_nmos123

.SUBCKT inv_pmos124 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.27u l=0.05u
.ENDS inv_pmos124

.SUBCKT delay_chain_inv A Z vdd gnd
Xpinv_nmos Z A gnd gnd inv_nmos123
Xpinv_pmos Z A vdd vdd inv_pmos124
.ENDS delay_chain_inv

.SUBCKT delay_chain clk_in clk_out vdd gnd
Xinv_chain0 clk_in s1 vdd gnd delay_chain_inv
Xinv_chain1 s1 s2 vdd gnd delay_chain_inv
Xinv_chain2 s2 s3 vdd gnd delay_chain_inv
Xinv_chain3 s3 clk_out vdd gnd delay_chain_inv
.ENDS delay_chain

.SUBCKT inv_nmos125 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.09u l=0.05u
.ENDS inv_nmos125

.SUBCKT inv_pmos126 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.27u l=0.05u
.ENDS inv_pmos126

.SUBCKT RBL_inv A Z vdd gnd
Xpinv_nmos Z A gnd gnd inv_nmos125
Xpinv_pmos Z A vdd vdd inv_pmos126
.ENDS RBL_inv

.SUBCKT nor_2_nmos131 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.09u l=0.05u
.ENDS nor_2_nmos131

.SUBCKT nor_2_nmos232 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.09u l=0.05u
.ENDS nor_2_nmos232

.SUBCKT nor_2_pmos133 D G S B
Mpmos D G S B pmos_vtg m=2 w=0.18u l=0.05u
.ENDS nor_2_pmos133

.SUBCKT nor_2_pmos234 D G S B
Mpmos D G S B pmos_vtg m=2 w=0.18u l=0.05u
.ENDS nor_2_pmos234

.SUBCKT replica_bitline_nor2 A B Z vdd gnd
Xnmos1 Z A gnd gnd nor_2_nmos131
Xnmos2 Z B gnd gnd nor_2_nmos232
Xpmos1 vdd A net1 vdd nor_2_pmos133
Xpmos2 net1 B Z vdd nor_2_pmos234
.ENDS replica_bitline_nor2

.SUBCKT access_tx35 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.09u l=0.05u
.ENDS access_tx35

.SUBCKT replica_bitline en out vdd gnd
XBL_inv bl[0] out vdd gnd RBL_inv
XBL_access_tx vdd delayed_en bl[0] vdd access_tx35
Xdelay_chain en delayed_en vdd gnd delay_chain
Xbitcell bl[0] br[0] delayed_en vdd gnd replica_cell_6t
Xload bl[0] br[0] gnd gnd vdd gnd bitline_load
.ENDS replica_bitline

.SUBCKT control_logic CSb WEb OEb s_en w_en tri_en tri_en_bar clk_bar clk vdd gnd
Xmsf_control CSb WEb OEb CS_bar CS WE_bar WE OE_bar OE clk vdd gnd msf_control
Xclk_inverter clk clk_bar vdd gnd pinv4
Xnor2 clk OE_bar tri_en vdd gnd nor2
Xnand2_tri_en OE clk_bar tri_en_bar vdd gnd nand2
Xreplica_bitline rblk pre_s_en vdd gnd replica_bitline
Xinv_s_en1 pre_s_en_bar s_en vdd gnd pinv
Xinv_s_en2 pre_s_en pre_s_en_bar vdd gnd pinv
XNAND3_rblk_bar clk_bar OE CS rblk_bar vdd gnd NAND3
XNAND3_w_en_bar clk_bar WE CS w_en_bar vdd gnd NAND3
Xinv_rblk rblk_bar rblk vdd gnd pinv
Xinv_w_en w_en_bar pre_w_en vdd gnd pinv
Xinv_w_en1 pre_w_en pre_w_en1 vdd gnd pinv
Xinv_w_en2 pre_w_en1 w_en vdd gnd pinv
.ENDS control_logic

.SUBCKT bitcell_array bl[0] br[0] bl[1] br[1] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] vdd gnd
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
.ENDS bitcell_array

.SUBCKT lower_pmos36 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.09u l=0.05u
.ENDS lower_pmos36

.SUBCKT upper_pmos37 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.18u l=0.05u
.ENDS upper_pmos37

.SUBCKT precharge_cell bl br clk vdd
Xlower_pmos bl clk br vdd lower_pmos36
Xupper_pmos1 bl clk vdd vdd upper_pmos37
Xupper_pmos2 br clk vdd vdd upper_pmos37
.ENDS precharge_cell

.SUBCKT precharge_array bl[0] br[0] bl[1] br[1] clk vdd
Xpre_column_0 bl[0] br[0] clk vdd precharge_cell
Xpre_column_1 bl[1] br[1] clk vdd precharge_cell
.ENDS precharge_array

.SUBCKT sense_amp bl br dout sclk vdd gnd
M_1 dout net_1 vdd vdd pmos_vtg w=540.0n l=50.0n
M_3 net_1 dout vdd vdd pmos_vtg w=540.0n l=50.0n
M_2 dout net_1 net_2 gnd nmos_vtg w=270.0n l=50.0n
M_8 net_1 dout net_2 gnd nmos_vtg w=270.0n l=50.0n
M_5 bl sclk dout vdd pmos_vtg w=720.0n l=50.0n
M_6 br sclk net_1 vdd pmos_vtg w=720.0n l=50.0n
M_7 net_2 sclk gnd gnd nmos_vtg w=270.0n l=50.0n
.ENDS sense_amp


.SUBCKT sense_amp_array bl[0] br[0] bl[1] br[1] data_out[0] data_out[1] sclk vdd gnd
Xsa_d0 bl[0] br[0] data_out[0] sclk vdd gnd sense_amp
Xsa_d1 bl[1] br[1] data_out[1] sclk vdd gnd sense_amp
.ENDS sense_amp_array

.SUBCKT write_driver din bl br wen vdd gnd
*inverters for enable and data input
minP bl_bar din vdd vdd pmos_vtg w=360.000000n l=50.000000n
minN bl_bar din gnd gnd nmos_vtg w=180.000000n l=50.000000n
moutP wen_bar wen vdd vdd pmos_vtg w=360.000000n l=50.000000n
moutN wen_bar wen gnd gnd nmos_vtg w=180.000000n l=50.000000n

*tristate for BL
mout0P int1 bl_bar vdd vdd pmos_vtg w=360.000000n l=50.000000n
mout0P2 bl wen_bar int1 vdd pmos_vtg w=360.000000n l=50.000000n
mout0N bl wen int2 gnd nmos_vtg w=180.000000n l=50.000000n
mout0N2 int2 bl_bar gnd gnd nmos_vtg w=180.000000n l=50.000000n

*tristate for BR
mout1P int3 din vdd vdd pmos_vtg w=360.000000n l=50.000000n
mout1P2 br wen_bar int3 vdd pmos_vtg w=360.000000n l=50.000000n
mout1N br wen int4 gnd nmos_vtg w=180.000000n l=50.000000n
mout1N2 int4 din gnd gnd nmos_vtg w=180.000000n l=50.000000n
.ENDS write_driver


.SUBCKT write_driver_array data_in[0] data_in[1] bl[0] br[0] bl[1] br[1] wen vdd gnd
XXwrite_driver0 data_in[0] bl[0] br[0] wen vdd gnd write_driver
XXwrite_driver1 data_in[1] bl[1] br[1] wen vdd gnd write_driver
.ENDS write_driver_array

.SUBCKT inv_nmos139 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.09u l=0.05u
.ENDS inv_nmos139

.SUBCKT inv_pmos140 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.18u l=0.05u
.ENDS inv_pmos140

.SUBCKT INVERTER A Z vdd gnd
Xpinv_nmos Z A gnd gnd inv_nmos139
Xpinv_pmos Z A vdd vdd inv_pmos140
.ENDS INVERTER

.SUBCKT nand_2_nmos141 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_2_nmos141

.SUBCKT nand_2_nmos242 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_2_nmos242

.SUBCKT nand_2_pmos143 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_2_pmos143

.SUBCKT nand_2_pmos244 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_2_pmos244

.SUBCKT NAND2 A B Z vdd gnd
Xnmos1 Z A net1 gnd nand_2_nmos141
Xnmos2 net1 B gnd gnd nand_2_nmos242
Xpmos1 vdd A Z vdd nand_2_pmos143
Xpmos2 Z B vdd vdd nand_2_pmos244
.ENDS NAND2

.SUBCKT nand_2_nmos151 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_2_nmos151

.SUBCKT nand_2_nmos252 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_2_nmos252

.SUBCKT nand_2_pmos153 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_2_pmos153

.SUBCKT nand_2_pmos254 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_2_pmos254

.SUBCKT a_nand_2 A B Z vdd gnd
Xnmos1 Z A net1 gnd nand_2_nmos151
Xnmos2 net1 B gnd gnd nand_2_nmos252
Xpmos1 vdd A Z vdd nand_2_pmos153
Xpmos2 Z B vdd vdd nand_2_pmos254
.ENDS a_nand_2

.SUBCKT inv_nmos155 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.09u l=0.05u
.ENDS inv_nmos155

.SUBCKT inv_pmos156 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.18u l=0.05u
.ENDS inv_pmos156

.SUBCKT a_inv_1 A Z vdd gnd
Xpinv_nmos Z A gnd gnd inv_nmos155
Xpinv_pmos Z A vdd vdd inv_pmos156
.ENDS a_inv_1

.SUBCKT pre2x4 A[0] A[1] out[0] out[1] out[2] out[3] vdd gnd
XXpre2x4_inv[0] A[0] B[0] vdd gnd a_inv_1
XXpre2x4_inv[1] A[1] B[1] vdd gnd a_inv_1
XXpre2x4_nand_inv[0] Z[0] out[0] vdd gnd a_inv_1
XXpre2x4_nand_inv[1] Z[1] out[1] vdd gnd a_inv_1
XXpre2x4_nand_inv[2] Z[2] out[2] vdd gnd a_inv_1
XXpre2x4_nand_inv[3] Z[3] out[3] vdd gnd a_inv_1
XXpre2x4_nand[0] A[0] A[1] Z[3] vdd gnd a_nand_2
XXpre2x4_nand[1] B[0] A[1] Z[2] vdd gnd a_nand_2
XXpre2x4_nand[2] A[0] B[1] Z[1] vdd gnd a_nand_2
XXpre2x4_nand[3] B[0] B[1] Z[0] vdd gnd a_nand_2
.ENDS pre2x4

.SUBCKT nand_3_nmos157 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.27u l=0.05u
.ENDS nand_3_nmos157

.SUBCKT nand_3_nmos258 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.27u l=0.05u
.ENDS nand_3_nmos258

.SUBCKT nand_3_nmos359 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.27u l=0.05u
.ENDS nand_3_nmos359

.SUBCKT nand_3_pmos160 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_3_pmos160

.SUBCKT nand_3_pmos261 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_3_pmos261

.SUBCKT nand_3_pmos362 D G S B
Mpmos D G S B pmos_vtg m=1 w=0.18u l=0.05u
.ENDS nand_3_pmos362

.SUBCKT a_nand_3 A B C Z vdd gnd
Xnmos1 net2 A gnd gnd nand_3_nmos157
Xnmos2 net1 B net2 gnd nand_3_nmos258
Xnmos3 Z C net1 gnd nand_3_nmos359
Xpmos1 Z A vdd vdd nand_3_pmos160
Xpmos2 vdd B Z vdd nand_3_pmos261
Xpmos3 Z C vdd vdd nand_3_pmos362
.ENDS a_nand_3

.SUBCKT pre3x8 A[0] A[1] A[2] out[0] out[1] out[2] out[3] out[4] out[5] out[6] out[7] vdd gnd
XXpre2x4_inv[0] A[0] B[0] vdd gnd a_inv_1
XXpre2x4_inv[1] A[1] B[1] vdd gnd a_inv_1
XXpre2x4_inv[2] A[2] B[2] vdd gnd a_inv_1
XXpre2x4_nand_inv[0] Z[0] out[0] vdd gnd a_inv_1
XXpre2x4_nand_inv[1] Z[1] out[1] vdd gnd a_inv_1
XXpre2x4_nand_inv[2] Z[2] out[2] vdd gnd a_inv_1
XXpre2x4_nand_inv[3] Z[3] out[3] vdd gnd a_inv_1
XXpre2x4_nand_inv[4] Z[4] out[4] vdd gnd a_inv_1
XXpre2x4_nand_inv[5] Z[5] out[5] vdd gnd a_inv_1
XXpre2x4_nand_inv[6] Z[6] out[6] vdd gnd a_inv_1
XXpre2x4_nand_inv[7] Z[7] out[7] vdd gnd a_inv_1
XXpre3x8_nand[0] A[0] A[1] A[2] Z[7] vdd gnd a_nand_3
XXpre3x8_nand[1] A[0] A[1] B[2] Z[6] vdd gnd a_nand_3
XXpre3x8_nand[2] A[0] B[1] A[2] Z[5] vdd gnd a_nand_3
XXpre3x8_nand[3] A[0] B[1] B[2] Z[4] vdd gnd a_nand_3
XXpre3x8_nand[4] B[0] A[1] A[2] Z[3] vdd gnd a_nand_3
XXpre3x8_nand[5] B[0] A[1] B[2] Z[2] vdd gnd a_nand_3
XXpre3x8_nand[6] B[0] B[1] A[2] Z[1] vdd gnd a_nand_3
XXpre3x8_nand[7] B[0] B[1] B[2] Z[0] vdd gnd a_nand_3
.ENDS pre3x8

.SUBCKT hierarchical_decoder A[0] A[1] A[2] A[3] decode_out[0] decode_out[1] decode_out[2] decode_out[3] decode_out[4] decode_out[5] decode_out[6] decode_out[7] decode_out[8] decode_out[9] decode_out[10] decode_out[11] decode_out[12] decode_out[13] decode_out[14] decode_out[15] vdd gnd
Xpre[0] A[0] A[1] out[0] out[1] out[2] out[3] vdd gnd pre2x4
Xpre[1] A[2] A[3] out[4] out[5] out[6] out[7] vdd gnd pre2x4
XNAND2_[0] out[0] out[4] Z[0] vdd gnd NAND2
XNAND2_[1] out[0] out[5] Z[1] vdd gnd NAND2
XNAND2_[2] out[0] out[6] Z[2] vdd gnd NAND2
XNAND2_[3] out[0] out[7] Z[3] vdd gnd NAND2
XNAND2_[4] out[1] out[4] Z[4] vdd gnd NAND2
XNAND2_[5] out[1] out[5] Z[5] vdd gnd NAND2
XNAND2_[6] out[1] out[6] Z[6] vdd gnd NAND2
XNAND2_[7] out[1] out[7] Z[7] vdd gnd NAND2
XNAND2_[8] out[2] out[4] Z[8] vdd gnd NAND2
XNAND2_[9] out[2] out[5] Z[9] vdd gnd NAND2
XNAND2_[10] out[2] out[6] Z[10] vdd gnd NAND2
XNAND2_[11] out[2] out[7] Z[11] vdd gnd NAND2
XNAND2_[12] out[3] out[4] Z[12] vdd gnd NAND2
XNAND2_[13] out[3] out[5] Z[13] vdd gnd NAND2
XNAND2_[14] out[3] out[6] Z[14] vdd gnd NAND2
XNAND2_[15] out[3] out[7] Z[15] vdd gnd NAND2
XINVERTER_[0] Z[0] decode_out[0] vdd gnd INVERTER
XINVERTER_[1] Z[1] decode_out[1] vdd gnd INVERTER
XINVERTER_[2] Z[2] decode_out[2] vdd gnd INVERTER
XINVERTER_[3] Z[3] decode_out[3] vdd gnd INVERTER
XINVERTER_[4] Z[4] decode_out[4] vdd gnd INVERTER
XINVERTER_[5] Z[5] decode_out[5] vdd gnd INVERTER
XINVERTER_[6] Z[6] decode_out[6] vdd gnd INVERTER
XINVERTER_[7] Z[7] decode_out[7] vdd gnd INVERTER
XINVERTER_[8] Z[8] decode_out[8] vdd gnd INVERTER
XINVERTER_[9] Z[9] decode_out[9] vdd gnd INVERTER
XINVERTER_[10] Z[10] decode_out[10] vdd gnd INVERTER
XINVERTER_[11] Z[11] decode_out[11] vdd gnd INVERTER
XINVERTER_[12] Z[12] decode_out[12] vdd gnd INVERTER
XINVERTER_[13] Z[13] decode_out[13] vdd gnd INVERTER
XINVERTER_[14] Z[14] decode_out[14] vdd gnd INVERTER
XINVERTER_[15] Z[15] decode_out[15] vdd gnd INVERTER
.ENDS hierarchical_decoder

.SUBCKT msf_address addr[0] addr[1] addr[2] addr[3] A[0] A_bar[0] A[1] A_bar[1] A[2] A_bar[2] A[3] A_bar[3] addr_clk vdd gnd
XXdff0 addr[0] A[0] A_bar[0] addr_clk vdd gnd ms_flop
XXdff1 addr[1] A[1] A_bar[1] addr_clk vdd gnd ms_flop
XXdff2 addr[2] A[2] A_bar[2] addr_clk vdd gnd ms_flop
XXdff3 addr[3] A[3] A_bar[3] addr_clk vdd gnd ms_flop
.ENDS msf_address

.SUBCKT msf_data_in data[0] data[1] data_in[0] data_in_bar[0] data_in[1] data_in_bar[1] clk vdd gnd
XXdff0 data[0] data_in[0] data_in_bar[0] clk vdd gnd ms_flop
XXdff1 data[1] data_in[1] data_in_bar[1] clk vdd gnd ms_flop
.ENDS msf_data_in

.SUBCKT msf_data_out data_out[0] data_out[1] tri_in[0] tri_in_bar[0] tri_in[1] tri_in_bar[1] sclk vdd gnd
XXdff0 data_out[0] tri_in[0] tri_in_bar[0] sclk vdd gnd ms_flop
XXdff1 data_out[1] tri_in[1] tri_in_bar[1] sclk vdd gnd ms_flop
.ENDS msf_data_out

.SUBCKT tri_gate in out en en_bar vdd gnd
M_1 net_2 in_inv gnd gnd NMOS_VTG W=180.000000n L=50.000000n
M_2 out en net_2 gnd NMOS_VTG W=180.000000n L=50.000000n
M_3 net_3 in_inv vdd vdd PMOS_VTG W=360.000000n L=50.000000n
M_4 out en_bar net_3 vdd PMOS_VTG W=360.000000n L=50.000000n
M_5 in_inv in vdd vdd PMOS_VTG W=180.000000n L=50.000000n
M_6 in_inv in gnd gnd NMOS_VTG W=90.000000n L=50.000000n
.ENDS


.SUBCKT tri_gate_array tri_in[0] tri_in[1] data[0] data[1] en en_bar vdd gnd
XXtri_gate0 tri_in[0] data[0] en en_bar vdd gnd tri_gate
XXtri_gate1 tri_in[1] data[1] en en_bar vdd gnd tri_gate
.ENDS tri_gate_array

.SUBCKT wordline_driver decode_out[0] decode_out[1] decode_out[2] decode_out[3] decode_out[4] decode_out[5] decode_out[6] decode_out[7] decode_out[8] decode_out[9] decode_out[10] decode_out[11] decode_out[12] decode_out[13] decode_out[14] decode_out[15] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] clk vdd gnd
XWordline_driver_inv_clk0 clk clk_bar[0] vdd gnd INVERTER
XWordline_driver_nand0 decode_out[0] clk_bar[0] net[0] vdd gnd NAND2
XWordline_driver_inv0 net[0] wl[0] vdd gnd INVERTER
XWordline_driver_inv_clk1 clk clk_bar[1] vdd gnd INVERTER
XWordline_driver_nand1 decode_out[1] clk_bar[1] net[1] vdd gnd NAND2
XWordline_driver_inv1 net[1] wl[1] vdd gnd INVERTER
XWordline_driver_inv_clk2 clk clk_bar[2] vdd gnd INVERTER
XWordline_driver_nand2 decode_out[2] clk_bar[2] net[2] vdd gnd NAND2
XWordline_driver_inv2 net[2] wl[2] vdd gnd INVERTER
XWordline_driver_inv_clk3 clk clk_bar[3] vdd gnd INVERTER
XWordline_driver_nand3 decode_out[3] clk_bar[3] net[3] vdd gnd NAND2
XWordline_driver_inv3 net[3] wl[3] vdd gnd INVERTER
XWordline_driver_inv_clk4 clk clk_bar[4] vdd gnd INVERTER
XWordline_driver_nand4 decode_out[4] clk_bar[4] net[4] vdd gnd NAND2
XWordline_driver_inv4 net[4] wl[4] vdd gnd INVERTER
XWordline_driver_inv_clk5 clk clk_bar[5] vdd gnd INVERTER
XWordline_driver_nand5 decode_out[5] clk_bar[5] net[5] vdd gnd NAND2
XWordline_driver_inv5 net[5] wl[5] vdd gnd INVERTER
XWordline_driver_inv_clk6 clk clk_bar[6] vdd gnd INVERTER
XWordline_driver_nand6 decode_out[6] clk_bar[6] net[6] vdd gnd NAND2
XWordline_driver_inv6 net[6] wl[6] vdd gnd INVERTER
XWordline_driver_inv_clk7 clk clk_bar[7] vdd gnd INVERTER
XWordline_driver_nand7 decode_out[7] clk_bar[7] net[7] vdd gnd NAND2
XWordline_driver_inv7 net[7] wl[7] vdd gnd INVERTER
XWordline_driver_inv_clk8 clk clk_bar[8] vdd gnd INVERTER
XWordline_driver_nand8 decode_out[8] clk_bar[8] net[8] vdd gnd NAND2
XWordline_driver_inv8 net[8] wl[8] vdd gnd INVERTER
XWordline_driver_inv_clk9 clk clk_bar[9] vdd gnd INVERTER
XWordline_driver_nand9 decode_out[9] clk_bar[9] net[9] vdd gnd NAND2
XWordline_driver_inv9 net[9] wl[9] vdd gnd INVERTER
XWordline_driver_inv_clk10 clk clk_bar[10] vdd gnd INVERTER
XWordline_driver_nand10 decode_out[10] clk_bar[10] net[10] vdd gnd NAND2
XWordline_driver_inv10 net[10] wl[10] vdd gnd INVERTER
XWordline_driver_inv_clk11 clk clk_bar[11] vdd gnd INVERTER
XWordline_driver_nand11 decode_out[11] clk_bar[11] net[11] vdd gnd NAND2
XWordline_driver_inv11 net[11] wl[11] vdd gnd INVERTER
XWordline_driver_inv_clk12 clk clk_bar[12] vdd gnd INVERTER
XWordline_driver_nand12 decode_out[12] clk_bar[12] net[12] vdd gnd NAND2
XWordline_driver_inv12 net[12] wl[12] vdd gnd INVERTER
XWordline_driver_inv_clk13 clk clk_bar[13] vdd gnd INVERTER
XWordline_driver_nand13 decode_out[13] clk_bar[13] net[13] vdd gnd NAND2
XWordline_driver_inv13 net[13] wl[13] vdd gnd INVERTER
XWordline_driver_inv_clk14 clk clk_bar[14] vdd gnd INVERTER
XWordline_driver_nand14 decode_out[14] clk_bar[14] net[14] vdd gnd NAND2
XWordline_driver_inv14 net[14] wl[14] vdd gnd INVERTER
XWordline_driver_inv_clk15 clk clk_bar[15] vdd gnd INVERTER
XWordline_driver_nand15 decode_out[15] clk_bar[15] net[15] vdd gnd NAND2
XWordline_driver_inv15 net[15] wl[15] vdd gnd INVERTER
.ENDS wordline_driver

.SUBCKT inv_nmos173 D G S B
Mnmos D G S B nmos_vtg m=4 w=0.09u l=0.05u
.ENDS inv_nmos173

.SUBCKT inv_pmos174 D G S B
Mpmos D G S B pmos_vtg m=4 w=0.27u l=0.05u
.ENDS inv_pmos174

.SUBCKT pinv4x A Z vdd gnd
Xpinv_nmos Z A gnd gnd inv_nmos173
Xpinv_pmos Z A vdd vdd inv_pmos174
.ENDS pinv4x

.SUBCKT nor_2_nmos183 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.09u l=0.05u
.ENDS nor_2_nmos183

.SUBCKT nor_2_nmos284 D G S B
Mnmos D G S B nmos_vtg m=1 w=0.09u l=0.05u
.ENDS nor_2_nmos284

.SUBCKT nor_2_pmos185 D G S B
Mpmos D G S B pmos_vtg m=2 w=0.18u l=0.05u
.ENDS nor_2_pmos185

.SUBCKT nor_2_pmos286 D G S B
Mpmos D G S B pmos_vtg m=2 w=0.18u l=0.05u
.ENDS nor_2_pmos286

.SUBCKT NOR2 A B Z vdd gnd
Xnmos1 Z A gnd gnd nor_2_nmos183
Xnmos2 Z B gnd gnd nor_2_nmos284
Xpmos1 vdd A net1 vdd nor_2_pmos185
Xpmos2 net1 B Z vdd nor_2_pmos286
.ENDS NOR2

.SUBCKT test_bank1 data[0] data[1] addr[0] addr[1] addr[2] addr[3] s_en w_en tri_en_bar tri_en clk_bar clk vdd gnd
Xbitcell_array bl[0] br[0] bl[1] br[1] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] vdd gnd bitcell_array
Xprecharge_array bl[0] br[0] bl[1] br[1] clk_bar vdd precharge_array
Xsense_amp_array bl[0] br[0] bl[1] br[1] data_out[0] data_out[1] s_en vdd gnd sense_amp_array
Xwrite_driver_array data_in[0] data_in[1] bl[0] br[0] bl[1] br[1] w_en vdd gnd write_driver_array
Xdata_in_flop_array data[0] data[1] data_in[0] data_in_bar[0] data_in[1] data_in_bar[1] clk_bar vdd gnd msf_data_in
Xtrigate_data_array data_out[0] data_out[1] data[0] data[1] tri_en tri_en_bar vdd gnd tri_gate_array
Xaddress_decoder A[0] A[1] A[2] A[3] decode_out[0] decode_out[1] decode_out[2] decode_out[3] decode_out[4] decode_out[5] decode_out[6] decode_out[7] decode_out[8] decode_out[9] decode_out[10] decode_out[11] decode_out[12] decode_out[13] decode_out[14] decode_out[15] vdd gnd hierarchical_decoder
Xwordline_driver decode_out[0] decode_out[1] decode_out[2] decode_out[3] decode_out[4] decode_out[5] decode_out[6] decode_out[7] decode_out[8] decode_out[9] decode_out[10] decode_out[11] decode_out[12] decode_out[13] decode_out[14] decode_out[15] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] clk vdd gnd wordline_driver
Xaddress_flop_array addr[0] addr[1] addr[2] addr[3] A[0] A_bar[0] A[1] A_bar[1] A[2] A_bar[2] A[3] A_bar[3] clk vdd gnd msf_address
.ENDS test_bank1

.SUBCKT testsram data[0] data[1] addr[0] addr[1] addr[2] addr[3] CSb WEb OEb clk vdd gnd
Xbank0 data[0] data[1] addr[0] addr[1] addr[2] addr[3] s_en w_en tri_en_bar tri_en clk_bar clk vdd gnd test_bank1
Xcontrol CSb WEb OEb s_en w_en tri_en tri_en_bar clk_bar clk vdd gnd control_logic
.ENDS testsram
