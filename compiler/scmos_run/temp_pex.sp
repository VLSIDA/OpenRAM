* NGSPICE file created from sram_2_16_scn4m_subm.ext - technology: scmos

.SUBCKT sram_2_16_scn4m_subm din0[0] din0[1] addr0[0] addr0[1] addr0[2] addr0[3] csb0 web0 clk0 dout0[0] dout0[1] vdd gnd
+ bitcell_Q_b0_r0_c0 bitcell_Q_bar_b0_r0_c0 bitcell_Q_b0_r0_c1 bitcell_Q_bar_b0_r0_c1 bitcell_Q_b0_r1_c0 bitcell_Q_bar_b0_r1_c0 bitcell_Q_b0_r1_c1 bitcell_Q_bar_b0_r1_c1 bitcell_Q_b0_r2_c0 bitcell_Q_bar_b0_r2_c0 bitcell_Q_b0_r2_c1 bitcell_Q_bar_b0_r2_c1 bitcell_Q_b0_r3_c0 bitcell_Q_bar_b0_r3_c0 bitcell_Q_b0_r3_c1 bitcell_Q_bar_b0_r3_c1 bitcell_Q_b0_r4_c0 bitcell_Q_bar_b0_r4_c0 bitcell_Q_b0_r4_c1 bitcell_Q_bar_b0_r4_c1 bitcell_Q_b0_r5_c0 bitcell_Q_bar_b0_r5_c0 bitcell_Q_b0_r5_c1 bitcell_Q_bar_b0_r5_c1 bitcell_Q_b0_r6_c0 bitcell_Q_bar_b0_r6_c0 bitcell_Q_b0_r6_c1 bitcell_Q_bar_b0_r6_c1 bitcell_Q_b0_r7_c0 bitcell_Q_bar_b0_r7_c0 bitcell_Q_b0_r7_c1 bitcell_Q_bar_b0_r7_c1 bitcell_Q_b0_r8_c0 bitcell_Q_bar_b0_r8_c0 bitcell_Q_b0_r8_c1 bitcell_Q_bar_b0_r8_c1 bitcell_Q_b0_r9_c0 bitcell_Q_bar_b0_r9_c0 bitcell_Q_b0_r9_c1 bitcell_Q_bar_b0_r9_c1 bitcell_Q_b0_r10_c0 bitcell_Q_bar_b0_r10_c0 bitcell_Q_b0_r10_c1 bitcell_Q_bar_b0_r10_c1 bitcell_Q_b0_r11_c0 bitcell_Q_bar_b0_r11_c0 bitcell_Q_b0_r11_c1 bitcell_Q_bar_b0_r11_c1 bitcell_Q_b0_r12_c0 bitcell_Q_bar_b0_r12_c0 bitcell_Q_b0_r12_c1 bitcell_Q_bar_b0_r12_c1 bitcell_Q_b0_r13_c0 bitcell_Q_bar_b0_r13_c0 bitcell_Q_b0_r13_c1 bitcell_Q_bar_b0_r13_c1 bitcell_Q_b0_r14_c0 bitcell_Q_bar_b0_r14_c0 bitcell_Q_b0_r14_c1 bitcell_Q_bar_b0_r14_c1 bitcell_Q_b0_r15_c0 bitcell_Q_bar_b0_r15_c0 bitcell_Q_b0_r15_c1 bitcell_Q_bar_b0_r15_c1 bl0_0 br0_0 bl0_1 br0_1 
+ s_en0
M1000 vdd clk_buf0 data_dff_0/dff_0/a_24_24# vdd p w=8u l=0.4u
+  ad=790.427p pd=2402.65u as=8p ps=18u
M1001 data_dff_0/dff_0/a_280_24# data_dff_0/dff_0/a_24_24# data_dff_0/dff_0/a_260_296# vdd p w=4u l=0.4u
+  ad=6p pd=11.2u as=2.4p ps=9.2u
M1002 bank_0/din0_1 data_dff_0/dff_0/a_280_24# vdd vdd p w=8u l=0.4u
+  ad=8p pd=18u as=0p ps=0u
M1003 data_dff_0/dff_0/a_260_24# data_dff_0/dff_0/a_152_16# gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=682.328p ps=1855.75u
M1004 data_dff_0/dff_0/a_84_296# din0[1] vdd vdd p w=4u l=0.4u
+  ad=3.2p pd=9.6u as=0p ps=0u
M1005 data_dff_0/dff_0/a_84_24# din0[1] gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1006 gnd bank_0/din0_1 data_dff_0/dff_0/a_320_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1007 gnd data_dff_0/dff_0/a_152_16# data_dff_0/dff_0/a_140_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1008 data_dff_0/dff_0/a_320_336# clk_buf0 data_dff_0/dff_0/a_280_24# vdd p w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1009 data_dff_0/dff_0/a_152_16# data_dff_0/dff_0/a_104_24# vdd vdd p w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1010 data_dff_0/dff_0/a_140_296# data_dff_0/dff_0/a_24_24# data_dff_0/dff_0/a_104_24# vdd p w=4u l=0.4u
+  ad=3.2p pd=9.6u as=4.8p ps=10.4u
M1011 data_dff_0/dff_0/a_280_24# clk_buf0 data_dff_0/dff_0/a_260_24# gnd n w=2u l=0.4u
+  ad=3.2p pd=7.2u as=0p ps=0u
M1012 gnd clk_buf0 data_dff_0/dff_0/a_24_24# gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4p ps=10u
M1013 data_dff_0/dff_0/a_260_296# data_dff_0/dff_0/a_152_16# vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1014 data_dff_0/dff_0/a_152_16# data_dff_0/dff_0/a_104_24# gnd gnd n w=2u l=0.4u
+  ad=2p pd=6u as=0p ps=0u
M1015 data_dff_0/dff_0/a_104_24# data_dff_0/dff_0/a_24_24# data_dff_0/dff_0/a_84_24# gnd n w=2u l=0.4u
+  ad=2.8p pd=6.8u as=0p ps=0u
M1016 data_dff_0/dff_0/a_320_24# data_dff_0/dff_0/a_24_24# data_dff_0/dff_0/a_280_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1017 vdd bank_0/din0_1 data_dff_0/dff_0/a_320_336# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1018 bank_0/din0_1 data_dff_0/dff_0/a_280_24# gnd gnd n w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1019 vdd data_dff_0/dff_0/a_152_16# data_dff_0/dff_0/a_140_296# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1020 data_dff_0/dff_0/a_140_24# clk_buf0 data_dff_0/dff_0/a_104_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1021 data_dff_0/dff_0/a_104_24# clk_buf0 data_dff_0/dff_0/a_84_296# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1022 vdd clk_buf0 data_dff_0/dff_1/a_24_24# vdd p w=8u l=0.4u
+  ad=0p pd=0u as=8p ps=18u
M1023 data_dff_0/dff_1/a_280_24# data_dff_0/dff_1/a_24_24# data_dff_0/dff_1/a_260_296# vdd p w=4u l=0.4u
+  ad=6p pd=11.2u as=2.4p ps=9.2u
M1024 bank_0/din0_0 data_dff_0/dff_1/a_280_24# vdd vdd p w=8u l=0.4u
+  ad=8p pd=18u as=0p ps=0u
M1025 data_dff_0/dff_1/a_260_24# data_dff_0/dff_1/a_152_16# gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1026 data_dff_0/dff_1/a_84_296# din0[0] vdd vdd p w=4u l=0.4u
+  ad=3.2p pd=9.6u as=0p ps=0u
M1027 data_dff_0/dff_1/a_84_24# din0[0] gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1028 gnd bank_0/din0_0 data_dff_0/dff_1/a_320_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1029 gnd data_dff_0/dff_1/a_152_16# data_dff_0/dff_1/a_140_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1030 data_dff_0/dff_1/a_320_336# clk_buf0 data_dff_0/dff_1/a_280_24# vdd p w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1031 data_dff_0/dff_1/a_152_16# data_dff_0/dff_1/a_104_24# vdd vdd p w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1032 data_dff_0/dff_1/a_140_296# data_dff_0/dff_1/a_24_24# data_dff_0/dff_1/a_104_24# vdd p w=4u l=0.4u
+  ad=3.2p pd=9.6u as=4.8p ps=10.4u
M1033 data_dff_0/dff_1/a_280_24# clk_buf0 data_dff_0/dff_1/a_260_24# gnd n w=2u l=0.4u
+  ad=3.2p pd=7.2u as=0p ps=0u
M1034 gnd clk_buf0 data_dff_0/dff_1/a_24_24# gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4p ps=10u
M1035 data_dff_0/dff_1/a_260_296# data_dff_0/dff_1/a_152_16# vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1036 data_dff_0/dff_1/a_152_16# data_dff_0/dff_1/a_104_24# gnd gnd n w=2u l=0.4u
+  ad=2p pd=6u as=0p ps=0u
M1037 data_dff_0/dff_1/a_104_24# data_dff_0/dff_1/a_24_24# data_dff_0/dff_1/a_84_24# gnd n w=2u l=0.4u
+  ad=2.8p pd=6.8u as=0p ps=0u
M1038 data_dff_0/dff_1/a_320_24# data_dff_0/dff_1/a_24_24# data_dff_0/dff_1/a_280_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1039 vdd bank_0/din0_0 data_dff_0/dff_1/a_320_336# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1040 bank_0/din0_0 data_dff_0/dff_1/a_280_24# gnd gnd n w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1041 vdd data_dff_0/dff_1/a_152_16# data_dff_0/dff_1/a_140_296# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1042 data_dff_0/dff_1/a_140_24# clk_buf0 data_dff_0/dff_1/a_104_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1043 data_dff_0/dff_1/a_104_24# clk_buf0 data_dff_0/dff_1/a_84_296# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1044 control_logic_rw_0/pand3_0_0/pinv_8_0/A control_logic_rw_0/pand3_1_0/B vdd vdd p w=1.6u l=0.4u
+  ad=4.8075p pd=11u as=0p ps=0u
M1045 vdd control_logic_rw_0/pinv_5_0/Z control_logic_rw_0/pand3_0_0/pinv_8_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1046 control_logic_rw_0/pand3_0_0/pinv_8_0/A control_logic_rw_0/pand3_0_0/A vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1047 control_logic_rw_0/pand3_0_0/pinv_8_0/A control_logic_rw_0/pand3_1_0/B control_logic_rw_0/pand3_0_0/pnand3_1_0/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M1048 control_logic_rw_0/pand3_0_0/pnand3_1_0/nmos_m1_w1_600_a_p_1/D control_logic_rw_0/pinv_5_0/Z control_logic_rw_0/pand3_0_0/pnand3_1_0/nmos_m1_w1_600_a_p_2/D gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M1049 control_logic_rw_0/pand3_0_0/pnand3_1_0/nmos_m1_w1_600_a_p_2/D control_logic_rw_0/pand3_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1050 w_en0 control_logic_rw_0/pand3_0_0/pinv_8_0/A vdd vdd p w=8u l=0.4u
+  ad=9.6025p pd=18.45u as=0p ps=0u
M1051 vdd control_logic_rw_0/pand3_0_0/pinv_8_0/A w_en0 vdd p w=8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1052 gnd control_logic_rw_0/pand3_0_0/pinv_8_0/A w_en0 gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4.8025p ps=10.45u
M1053 w_en0 control_logic_rw_0/pand3_0_0/pinv_8_0/A gnd gnd n w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1054 control_logic_rw_0/pinv_5_0/Z control_logic_rw_0/pinv_5_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1055 control_logic_rw_0/pinv_5_0/Z control_logic_rw_0/pinv_5_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1056 control_logic_rw_0/pinv_5_1/Z clk_buf0 vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1057 control_logic_rw_0/pinv_5_1/Z clk_buf0 gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1058 control_logic_rw_0/pdriver_3_0/pinv_3_0/A control_logic_rw_0/pdriver_3_0/pinv_5_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1059 control_logic_rw_0/pdriver_3_0/pinv_3_0/A control_logic_rw_0/pdriver_3_0/pinv_5_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1060 control_logic_rw_0/pdriver_3_0/pinv_5_0/A control_logic_rw_0/pand3_1_0/B vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1061 control_logic_rw_0/pdriver_3_0/pinv_5_0/A control_logic_rw_0/pand3_1_0/B gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1062 control_logic_rw_0/pdriver_3_0/pinv_6_0/A control_logic_rw_0/pdriver_3_0/pinv_3_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.2025p pd=8.45u as=0p ps=0u
M1063 control_logic_rw_0/pdriver_3_0/pinv_6_0/A control_logic_rw_0/pdriver_3_0/pinv_3_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1064 wl_en0 control_logic_rw_0/pdriver_3_0/pinv_6_0/A vdd vdd p w=8u l=0.4u
+  ad=8.0025p pd=18.05u as=0p ps=0u
M1065 wl_en0 control_logic_rw_0/pdriver_3_0/pinv_6_0/A gnd gnd n w=4u l=0.4u
+  ad=4.0025p pd=10.05u as=0p ps=0u
M1066 control_logic_rw_0/pand2_0_0/pdriver_1_0/pinv_4_0/A control_logic_rw_0/pand2_0_0/pdriver_1_0/pinv_5_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1067 control_logic_rw_0/pand2_0_0/pdriver_1_0/pinv_4_0/A control_logic_rw_0/pand2_0_0/pdriver_1_0/pinv_5_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1068 control_logic_rw_0/pand2_0_0/pdriver_1_0/pinv_5_0/A control_logic_rw_0/pand2_0_0/pnand2_1_0/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1069 control_logic_rw_0/pand2_0_0/pdriver_1_0/pinv_5_0/A control_logic_rw_0/pand2_0_0/pnand2_1_0/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1070 control_logic_rw_0/pand2_0_0/Z control_logic_rw_0/pand2_0_0/pdriver_1_0/pinv_4_0/A gnd gnd n w=3.2u l=0.4u
+  ad=3.2025p pd=8.45u as=0p ps=0u
M1071 control_logic_rw_0/pand2_0_0/Z control_logic_rw_0/pand2_0_0/pdriver_1_0/pinv_4_0/A vdd vdd p w=6.4u l=0.4u
+  ad=6.4025p pd=14.85u as=0p ps=0u
M1072 vdd control_logic_rw_0/pand2_0_0/B control_logic_rw_0/pand2_0_0/pnand2_1_0/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=3.205p ps=5.75u
M1073 control_logic_rw_0/pand2_0_0/pnand2_1_0/Z clk_buf0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1074 control_logic_rw_0/pand2_0_0/pnand2_1_0/Z control_logic_rw_0/pand2_0_0/B control_logic_rw_0/pand2_0_0/pnand2_1_0/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M1075 control_logic_rw_0/pand2_0_0/pnand2_1_0/nmos_m1_w1_600_a_p_1/D clk_buf0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1076 control_logic_rw_0/pand2_0_1/pdriver_1_0/pinv_4_0/A control_logic_rw_0/pand2_0_1/pdriver_1_0/pinv_5_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1077 control_logic_rw_0/pand2_0_1/pdriver_1_0/pinv_4_0/A control_logic_rw_0/pand2_0_1/pdriver_1_0/pinv_5_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1078 control_logic_rw_0/pand2_0_1/pdriver_1_0/pinv_5_0/A control_logic_rw_0/pand2_0_1/pnand2_1_0/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1079 control_logic_rw_0/pand2_0_1/pdriver_1_0/pinv_5_0/A control_logic_rw_0/pand2_0_1/pnand2_1_0/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1080 control_logic_rw_0/pand3_1_0/B control_logic_rw_0/pand2_0_1/pdriver_1_0/pinv_4_0/A gnd gnd n w=3.2u l=0.4u
+  ad=3.2025p pd=8.45u as=0p ps=0u
M1081 control_logic_rw_0/pand3_1_0/B control_logic_rw_0/pand2_0_1/pdriver_1_0/pinv_4_0/A vdd vdd p w=6.4u l=0.4u
+  ad=6.4025p pd=14.85u as=0p ps=0u
M1082 vdd control_logic_rw_0/pinv_5_1/Z control_logic_rw_0/pand2_0_1/pnand2_1_0/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=3.205p ps=5.75u
M1083 control_logic_rw_0/pand2_0_1/pnand2_1_0/Z control_logic_rw_0/pand2_0_0/B vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1084 control_logic_rw_0/pand2_0_1/pnand2_1_0/Z control_logic_rw_0/pinv_5_1/Z control_logic_rw_0/pand2_0_1/pnand2_1_0/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M1085 control_logic_rw_0/pand2_0_1/pnand2_1_0/nmos_m1_w1_600_a_p_1/D control_logic_rw_0/pand2_0_0/B gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1086 s_en0 control_logic_rw_0/pand3_1_0/pinv_3_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.2025p pd=8.45u as=0p ps=0u
M1087 s_en0 control_logic_rw_0/pand3_1_0/pinv_3_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1088 control_logic_rw_0/pand3_1_0/pinv_3_0/A control_logic_rw_0/pand3_1_0/C vdd vdd p w=1.6u l=0.4u
+  ad=4.8075p pd=11u as=0p ps=0u
M1089 vdd control_logic_rw_0/pand3_1_0/B control_logic_rw_0/pand3_1_0/pinv_3_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1090 control_logic_rw_0/pand3_1_0/pinv_3_0/A control_logic_rw_0/pinv_5_0/A vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1091 control_logic_rw_0/pand3_1_0/pinv_3_0/A control_logic_rw_0/pand3_1_0/C control_logic_rw_0/pand3_1_0/pnand3_1_0/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M1092 control_logic_rw_0/pand3_1_0/pnand3_1_0/nmos_m1_w1_600_a_p_1/D control_logic_rw_0/pand3_1_0/B control_logic_rw_0/pand3_1_0/pnand3_1_0/nmos_m1_w1_600_a_p_2/D gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M1093 control_logic_rw_0/pand3_1_0/pnand3_1_0/nmos_m1_w1_600_a_p_2/D control_logic_rw_0/pinv_5_0/A gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1094 p_en_bar0 control_logic_rw_0/pdriver_4_0/pinv_5_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1095 p_en_bar0 control_logic_rw_0/pdriver_4_0/pinv_5_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1096 control_logic_rw_0/pdriver_4_0/pinv_5_0/A control_logic_rw_0/pnand2_1_0/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1097 control_logic_rw_0/pdriver_4_0/pinv_5_0/A control_logic_rw_0/pnand2_1_0/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1098 vdd clk_buf0 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_24_24# vdd p w=8u l=0.4u
+  ad=0p pd=0u as=8p ps=18u
M1099 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_280_24# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_24_24# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_260_296# vdd p w=4u l=0.4u
+  ad=6p pd=11.2u as=2.4p ps=9.2u
M1100 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/Q control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_280_24# vdd vdd p w=8u l=0.4u
+  ad=8p pd=18u as=0p ps=0u
M1101 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_260_24# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_152_16# gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1102 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_84_296# csb0 vdd vdd p w=4u l=0.4u
+  ad=3.2p pd=9.6u as=0p ps=0u
M1103 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_84_24# csb0 gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1104 gnd control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/Q control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_320_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1105 gnd control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_152_16# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_140_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1106 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_320_336# clk_buf0 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_280_24# vdd p w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1107 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_152_16# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_104_24# vdd vdd p w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1108 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_140_296# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_24_24# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_104_24# vdd p w=4u l=0.4u
+  ad=3.2p pd=9.6u as=4.8p ps=10.4u
M1109 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_280_24# clk_buf0 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_260_24# gnd n w=2u l=0.4u
+  ad=3.2p pd=7.2u as=0p ps=0u
M1110 gnd clk_buf0 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_24_24# gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4p ps=10u
M1111 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_260_296# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_152_16# vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1112 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_152_16# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_104_24# gnd gnd n w=2u l=0.4u
+  ad=2p pd=6u as=0p ps=0u
M1113 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_104_24# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_24_24# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_84_24# gnd n w=2u l=0.4u
+  ad=2.8p pd=6.8u as=0p ps=0u
M1114 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_320_24# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_24_24# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_280_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1115 vdd control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/Q control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_320_336# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1116 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/Q control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_280_24# gnd gnd n w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1117 vdd control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_152_16# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_140_296# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1118 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_140_24# clk_buf0 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_104_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1119 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_104_24# clk_buf0 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_84_296# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1120 control_logic_rw_0/pand2_0_0/B control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/Q vdd vdd p w=3.2u l=0.4u
+  ad=3.2025p pd=8.45u as=0p ps=0u
M1121 control_logic_rw_0/pand2_0_0/B control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/Q gnd gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1122 control_logic_rw_0/dff_buf_array_0_0/dout_0 control_logic_rw_0/pand2_0_0/B gnd gnd n w=3.2u l=0.4u
+  ad=3.2025p pd=8.45u as=0p ps=0u
M1123 control_logic_rw_0/dff_buf_array_0_0/dout_0 control_logic_rw_0/pand2_0_0/B vdd vdd p w=6.4u l=0.4u
+  ad=6.4025p pd=14.85u as=0p ps=0u
M1124 vdd clk_buf0 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_24_24# vdd p w=8u l=0.4u
+  ad=0p pd=0u as=8p ps=18u
M1125 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_280_24# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_24_24# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_260_296# vdd p w=4u l=0.4u
+  ad=6p pd=11.2u as=2.4p ps=9.2u
M1126 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/Q control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_280_24# vdd vdd p w=8u l=0.4u
+  ad=8p pd=18u as=0p ps=0u
M1127 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_260_24# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_152_16# gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1128 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_84_296# web0 vdd vdd p w=4u l=0.4u
+  ad=3.2p pd=9.6u as=0p ps=0u
M1129 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_84_24# web0 gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1130 gnd control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/Q control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_320_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1131 gnd control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_152_16# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_140_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1132 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_320_336# clk_buf0 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_280_24# vdd p w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1133 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_152_16# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_104_24# vdd vdd p w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1134 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_140_296# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_24_24# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_104_24# vdd p w=4u l=0.4u
+  ad=3.2p pd=9.6u as=4.8p ps=10.4u
M1135 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_280_24# clk_buf0 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_260_24# gnd n w=2u l=0.4u
+  ad=3.2p pd=7.2u as=0p ps=0u
M1136 gnd clk_buf0 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_24_24# gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4p ps=10u
M1137 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_260_296# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_152_16# vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1138 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_152_16# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_104_24# gnd gnd n w=2u l=0.4u
+  ad=2p pd=6u as=0p ps=0u
M1139 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_104_24# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_24_24# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_84_24# gnd n w=2u l=0.4u
+  ad=2.8p pd=6.8u as=0p ps=0u
M1140 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_320_24# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_24_24# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_280_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1141 vdd control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/Q control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_320_336# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1142 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/Q control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_280_24# gnd gnd n w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1143 vdd control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_152_16# control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_140_296# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1144 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_140_24# clk_buf0 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_104_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1145 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_104_24# clk_buf0 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_84_296# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1146 control_logic_rw_0/pand3_0_0/A control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/Q vdd vdd p w=3.2u l=0.4u
+  ad=3.2025p pd=8.45u as=0p ps=0u
M1147 control_logic_rw_0/pand3_0_0/A control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/Q gnd gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1148 control_logic_rw_0/pand3_1_0/C control_logic_rw_0/pand3_0_0/A gnd gnd n w=3.2u l=0.4u
+  ad=3.2025p pd=8.45u as=0p ps=0u
M1149 control_logic_rw_0/pand3_1_0/C control_logic_rw_0/pand3_0_0/A vdd vdd p w=6.4u l=0.4u
+  ad=6.4025p pd=14.85u as=0p ps=0u
M1150 vdd control_logic_rw_0/pinv_5_0/A control_logic_rw_0/pnand2_1_0/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=3.205p ps=5.75u
M1151 control_logic_rw_0/pnand2_1_0/Z control_logic_rw_0/pand2_0_0/Z vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1152 control_logic_rw_0/pnand2_1_0/Z control_logic_rw_0/pinv_5_0/A control_logic_rw_0/pnand2_1_0/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M1153 control_logic_rw_0/pnand2_1_0/nmos_m1_w1_600_a_p_1/D control_logic_rw_0/pand2_0_0/Z gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1154 clk_buf0 control_logic_rw_0/pdriver_2_0/pinv_7_0/A vdd vdd p w=8u l=0.4u
+  ad=17.6025p pd=36.45u as=0p ps=0u
M1155 clk_buf0 control_logic_rw_0/pdriver_2_0/pinv_7_0/A vdd vdd p w=8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1156 vdd control_logic_rw_0/pdriver_2_0/pinv_7_0/A clk_buf0 vdd p w=8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1157 gnd control_logic_rw_0/pdriver_2_0/pinv_7_0/A clk_buf0 gnd n w=4u l=0.4u
+  ad=0p pd=0u as=8.8025p ps=20.45u
M1158 clk_buf0 control_logic_rw_0/pdriver_2_0/pinv_7_0/A gnd gnd n w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1159 clk_buf0 control_logic_rw_0/pdriver_2_0/pinv_7_0/A gnd gnd n w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1160 control_logic_rw_0/pdriver_2_0/pinv_3_0/A clk0 vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1161 control_logic_rw_0/pdriver_2_0/pinv_3_0/A clk0 gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1162 control_logic_rw_0/pdriver_2_0/pinv_6_0/A control_logic_rw_0/pdriver_2_0/pinv_3_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.2025p pd=8.45u as=0p ps=0u
M1163 control_logic_rw_0/pdriver_2_0/pinv_6_0/A control_logic_rw_0/pdriver_2_0/pinv_3_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1164 control_logic_rw_0/pdriver_2_0/pinv_7_0/A control_logic_rw_0/pdriver_2_0/pinv_6_0/A vdd vdd p w=8u l=0.4u
+  ad=8.0025p pd=18.05u as=0p ps=0u
M1165 control_logic_rw_0/pdriver_2_0/pinv_7_0/A control_logic_rw_0/pdriver_2_0/pinv_6_0/A gnd gnd n w=4u l=0.4u
+  ad=4.0025p pd=10.05u as=0p ps=0u
M1166 control_logic_rw_0/delay_chain_0_0/pinv_2_6/Z control_logic_rw_0/delay_chain_0_0/pinv_2_4/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1167 control_logic_rw_0/delay_chain_0_0/pinv_2_6/Z control_logic_rw_0/delay_chain_0_0/pinv_2_4/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1168 control_logic_rw_0/delay_chain_0_0/pinv_2_16/Z control_logic_rw_0/delay_chain_0_0/pinv_2_14/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1169 control_logic_rw_0/delay_chain_0_0/pinv_2_16/Z control_logic_rw_0/delay_chain_0_0/pinv_2_14/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1170 control_logic_rw_0/delay_chain_0_0/pinv_2_38/Z control_logic_rw_0/delay_chain_0_0/pinv_2_34/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1171 control_logic_rw_0/delay_chain_0_0/pinv_2_38/Z control_logic_rw_0/delay_chain_0_0/pinv_2_34/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1172 control_logic_rw_0/delay_chain_0_0/pinv_2_27/Z control_logic_rw_0/delay_chain_0_0/pinv_2_24/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1173 control_logic_rw_0/delay_chain_0_0/pinv_2_27/Z control_logic_rw_0/delay_chain_0_0/pinv_2_24/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1174 control_logic_rw_0/delay_chain_0_0/pinv_2_7/Z control_logic_rw_0/delay_chain_0_0/pinv_2_4/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1175 control_logic_rw_0/delay_chain_0_0/pinv_2_7/Z control_logic_rw_0/delay_chain_0_0/pinv_2_4/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1176 control_logic_rw_0/delay_chain_0_0/pinv_2_17/Z control_logic_rw_0/delay_chain_0_0/pinv_2_14/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1177 control_logic_rw_0/delay_chain_0_0/pinv_2_17/Z control_logic_rw_0/delay_chain_0_0/pinv_2_14/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1178 control_logic_rw_0/delay_chain_0_0/pinv_2_34/A control_logic_rw_0/delay_chain_0_0/pinv_2_40/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1179 control_logic_rw_0/delay_chain_0_0/pinv_2_34/A control_logic_rw_0/delay_chain_0_0/pinv_2_40/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1180 control_logic_rw_0/delay_chain_0_0/pinv_2_28/Z control_logic_rw_0/delay_chain_0_0/pinv_2_24/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1181 control_logic_rw_0/delay_chain_0_0/pinv_2_28/Z control_logic_rw_0/delay_chain_0_0/pinv_2_24/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1182 control_logic_rw_0/delay_chain_0_0/pinv_2_8/Z control_logic_rw_0/delay_chain_0_0/pinv_2_4/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1183 control_logic_rw_0/delay_chain_0_0/pinv_2_8/Z control_logic_rw_0/delay_chain_0_0/pinv_2_4/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1184 control_logic_rw_0/delay_chain_0_0/pinv_2_18/Z control_logic_rw_0/delay_chain_0_0/pinv_2_14/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1185 control_logic_rw_0/delay_chain_0_0/pinv_2_18/Z control_logic_rw_0/delay_chain_0_0/pinv_2_14/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1186 control_logic_rw_0/delay_chain_0_0/pinv_2_24/A control_logic_rw_0/delay_chain_0_0/pinv_2_30/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1187 control_logic_rw_0/delay_chain_0_0/pinv_2_24/A control_logic_rw_0/delay_chain_0_0/pinv_2_30/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1188 control_logic_rw_0/delay_chain_0_0/pinv_2_4/A control_logic_rw_0/delay_chain_0_0/pinv_2_9/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1189 control_logic_rw_0/delay_chain_0_0/pinv_2_4/A control_logic_rw_0/delay_chain_0_0/pinv_2_9/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1190 control_logic_rw_0/delay_chain_0_0/pinv_2_14/A control_logic_rw_0/delay_chain_0_0/pinv_2_20/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1191 control_logic_rw_0/delay_chain_0_0/pinv_2_14/A control_logic_rw_0/delay_chain_0_0/pinv_2_20/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1192 control_logic_rw_0/delay_chain_0_0/pinv_2_40/Z control_logic_rw_0/delay_chain_0_0/pinv_2_40/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1193 control_logic_rw_0/delay_chain_0_0/pinv_2_40/Z control_logic_rw_0/delay_chain_0_0/pinv_2_40/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1194 control_logic_rw_0/delay_chain_0_0/pinv_2_41/Z control_logic_rw_0/delay_chain_0_0/pinv_2_40/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1195 control_logic_rw_0/delay_chain_0_0/pinv_2_41/Z control_logic_rw_0/delay_chain_0_0/pinv_2_40/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1196 control_logic_rw_0/delay_chain_0_0/pinv_2_30/Z control_logic_rw_0/delay_chain_0_0/pinv_2_30/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1197 control_logic_rw_0/delay_chain_0_0/pinv_2_30/Z control_logic_rw_0/delay_chain_0_0/pinv_2_30/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1198 control_logic_rw_0/delay_chain_0_0/pinv_2_20/Z control_logic_rw_0/delay_chain_0_0/pinv_2_20/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1199 control_logic_rw_0/delay_chain_0_0/pinv_2_20/Z control_logic_rw_0/delay_chain_0_0/pinv_2_20/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1200 control_logic_rw_0/delay_chain_0_0/pinv_2_42/Z control_logic_rw_0/delay_chain_0_0/pinv_2_40/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1201 control_logic_rw_0/delay_chain_0_0/pinv_2_42/Z control_logic_rw_0/delay_chain_0_0/pinv_2_40/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1202 control_logic_rw_0/delay_chain_0_0/pinv_2_31/Z control_logic_rw_0/delay_chain_0_0/pinv_2_30/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1203 control_logic_rw_0/delay_chain_0_0/pinv_2_31/Z control_logic_rw_0/delay_chain_0_0/pinv_2_30/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1204 control_logic_rw_0/delay_chain_0_0/pinv_2_0/Z control_logic_rw_0/pinv_5_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1205 control_logic_rw_0/delay_chain_0_0/pinv_2_0/Z control_logic_rw_0/pinv_5_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1206 control_logic_rw_0/delay_chain_0_0/pinv_2_10/Z control_logic_rw_0/delay_chain_0_0/pinv_2_9/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1207 control_logic_rw_0/delay_chain_0_0/pinv_2_10/Z control_logic_rw_0/delay_chain_0_0/pinv_2_9/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1208 control_logic_rw_0/delay_chain_0_0/pinv_2_43/Z control_logic_rw_0/delay_chain_0_0/pinv_2_40/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1209 control_logic_rw_0/delay_chain_0_0/pinv_2_43/Z control_logic_rw_0/delay_chain_0_0/pinv_2_40/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1210 control_logic_rw_0/delay_chain_0_0/pinv_2_32/Z control_logic_rw_0/delay_chain_0_0/pinv_2_30/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1211 control_logic_rw_0/delay_chain_0_0/pinv_2_32/Z control_logic_rw_0/delay_chain_0_0/pinv_2_30/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1212 control_logic_rw_0/delay_chain_0_0/pinv_2_21/Z control_logic_rw_0/delay_chain_0_0/pinv_2_20/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1213 control_logic_rw_0/delay_chain_0_0/pinv_2_21/Z control_logic_rw_0/delay_chain_0_0/pinv_2_20/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1214 control_logic_rw_0/delay_chain_0_0/pinv_2_1/Z control_logic_rw_0/pinv_5_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1215 control_logic_rw_0/delay_chain_0_0/pinv_2_1/Z control_logic_rw_0/pinv_5_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1216 control_logic_rw_0/delay_chain_0_0/pinv_2_11/Z control_logic_rw_0/delay_chain_0_0/pinv_2_9/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1217 control_logic_rw_0/delay_chain_0_0/pinv_2_11/Z control_logic_rw_0/delay_chain_0_0/pinv_2_9/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1218 control_logic_rw_0/delay_chain_0_0/pinv_2_40/A rbl_bl0 vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1219 control_logic_rw_0/delay_chain_0_0/pinv_2_40/A rbl_bl0 gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1220 control_logic_rw_0/delay_chain_0_0/pinv_2_33/Z control_logic_rw_0/delay_chain_0_0/pinv_2_30/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1221 control_logic_rw_0/delay_chain_0_0/pinv_2_33/Z control_logic_rw_0/delay_chain_0_0/pinv_2_30/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1222 control_logic_rw_0/delay_chain_0_0/pinv_2_22/Z control_logic_rw_0/delay_chain_0_0/pinv_2_20/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1223 control_logic_rw_0/delay_chain_0_0/pinv_2_22/Z control_logic_rw_0/delay_chain_0_0/pinv_2_20/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1224 control_logic_rw_0/delay_chain_0_0/pinv_2_2/Z control_logic_rw_0/pinv_5_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1225 control_logic_rw_0/delay_chain_0_0/pinv_2_2/Z control_logic_rw_0/pinv_5_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1226 control_logic_rw_0/delay_chain_0_0/pinv_2_12/Z control_logic_rw_0/delay_chain_0_0/pinv_2_9/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1227 control_logic_rw_0/delay_chain_0_0/pinv_2_12/Z control_logic_rw_0/delay_chain_0_0/pinv_2_9/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1228 control_logic_rw_0/delay_chain_0_0/pinv_2_30/A control_logic_rw_0/delay_chain_0_0/pinv_2_34/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1229 control_logic_rw_0/delay_chain_0_0/pinv_2_30/A control_logic_rw_0/delay_chain_0_0/pinv_2_34/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1230 control_logic_rw_0/delay_chain_0_0/pinv_2_23/Z control_logic_rw_0/delay_chain_0_0/pinv_2_20/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1231 control_logic_rw_0/delay_chain_0_0/pinv_2_23/Z control_logic_rw_0/delay_chain_0_0/pinv_2_20/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1232 control_logic_rw_0/delay_chain_0_0/pinv_2_3/Z control_logic_rw_0/pinv_5_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1233 control_logic_rw_0/delay_chain_0_0/pinv_2_3/Z control_logic_rw_0/pinv_5_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1234 control_logic_rw_0/delay_chain_0_0/pinv_2_13/Z control_logic_rw_0/delay_chain_0_0/pinv_2_9/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1235 control_logic_rw_0/delay_chain_0_0/pinv_2_13/Z control_logic_rw_0/delay_chain_0_0/pinv_2_9/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1236 control_logic_rw_0/delay_chain_0_0/pinv_2_35/Z control_logic_rw_0/delay_chain_0_0/pinv_2_34/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1237 control_logic_rw_0/delay_chain_0_0/pinv_2_35/Z control_logic_rw_0/delay_chain_0_0/pinv_2_34/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1238 control_logic_rw_0/delay_chain_0_0/pinv_2_20/A control_logic_rw_0/delay_chain_0_0/pinv_2_24/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1239 control_logic_rw_0/delay_chain_0_0/pinv_2_20/A control_logic_rw_0/delay_chain_0_0/pinv_2_24/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1240 control_logic_rw_0/pinv_5_0/A control_logic_rw_0/delay_chain_0_0/pinv_2_4/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1241 control_logic_rw_0/pinv_5_0/A control_logic_rw_0/delay_chain_0_0/pinv_2_4/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1242 control_logic_rw_0/delay_chain_0_0/pinv_2_9/A control_logic_rw_0/delay_chain_0_0/pinv_2_14/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1243 control_logic_rw_0/delay_chain_0_0/pinv_2_9/A control_logic_rw_0/delay_chain_0_0/pinv_2_14/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1244 control_logic_rw_0/delay_chain_0_0/pinv_2_36/Z control_logic_rw_0/delay_chain_0_0/pinv_2_34/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1245 control_logic_rw_0/delay_chain_0_0/pinv_2_36/Z control_logic_rw_0/delay_chain_0_0/pinv_2_34/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1246 control_logic_rw_0/delay_chain_0_0/pinv_2_25/Z control_logic_rw_0/delay_chain_0_0/pinv_2_24/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1247 control_logic_rw_0/delay_chain_0_0/pinv_2_25/Z control_logic_rw_0/delay_chain_0_0/pinv_2_24/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1248 control_logic_rw_0/delay_chain_0_0/pinv_2_5/Z control_logic_rw_0/delay_chain_0_0/pinv_2_4/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1249 control_logic_rw_0/delay_chain_0_0/pinv_2_5/Z control_logic_rw_0/delay_chain_0_0/pinv_2_4/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1250 control_logic_rw_0/delay_chain_0_0/pinv_2_15/Z control_logic_rw_0/delay_chain_0_0/pinv_2_14/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1251 control_logic_rw_0/delay_chain_0_0/pinv_2_15/Z control_logic_rw_0/delay_chain_0_0/pinv_2_14/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1252 control_logic_rw_0/delay_chain_0_0/pinv_2_37/Z control_logic_rw_0/delay_chain_0_0/pinv_2_34/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1253 control_logic_rw_0/delay_chain_0_0/pinv_2_37/Z control_logic_rw_0/delay_chain_0_0/pinv_2_34/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1254 control_logic_rw_0/delay_chain_0_0/pinv_2_26/Z control_logic_rw_0/delay_chain_0_0/pinv_2_24/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1255 control_logic_rw_0/delay_chain_0_0/pinv_2_26/Z control_logic_rw_0/delay_chain_0_0/pinv_2_24/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1256 vdd clk_buf0 row_addr_dff_0/dff_0/a_24_24# vdd p w=8u l=0.4u
+  ad=0p pd=0u as=8p ps=18u
M1257 row_addr_dff_0/dff_0/a_280_24# row_addr_dff_0/dff_0/a_24_24# row_addr_dff_0/dff_0/a_260_296# vdd p w=4u l=0.4u
+  ad=6p pd=11.2u as=2.4p ps=9.2u
M1258 bank_0/addr0_3 row_addr_dff_0/dff_0/a_280_24# vdd vdd p w=8u l=0.4u
+  ad=8p pd=18u as=0p ps=0u
M1259 row_addr_dff_0/dff_0/a_260_24# row_addr_dff_0/dff_0/a_152_16# gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1260 row_addr_dff_0/dff_0/a_84_296# addr0[3] vdd vdd p w=4u l=0.4u
+  ad=3.2p pd=9.6u as=0p ps=0u
M1261 row_addr_dff_0/dff_0/a_84_24# addr0[3] gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1262 gnd bank_0/addr0_3 row_addr_dff_0/dff_0/a_320_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1263 gnd row_addr_dff_0/dff_0/a_152_16# row_addr_dff_0/dff_0/a_140_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1264 row_addr_dff_0/dff_0/a_320_336# clk_buf0 row_addr_dff_0/dff_0/a_280_24# vdd p w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1265 row_addr_dff_0/dff_0/a_152_16# row_addr_dff_0/dff_0/a_104_24# vdd vdd p w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1266 row_addr_dff_0/dff_0/a_140_296# row_addr_dff_0/dff_0/a_24_24# row_addr_dff_0/dff_0/a_104_24# vdd p w=4u l=0.4u
+  ad=3.2p pd=9.6u as=4.8p ps=10.4u
M1267 row_addr_dff_0/dff_0/a_280_24# clk_buf0 row_addr_dff_0/dff_0/a_260_24# gnd n w=2u l=0.4u
+  ad=3.2p pd=7.2u as=0p ps=0u
M1268 gnd clk_buf0 row_addr_dff_0/dff_0/a_24_24# gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4p ps=10u
M1269 row_addr_dff_0/dff_0/a_260_296# row_addr_dff_0/dff_0/a_152_16# vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1270 row_addr_dff_0/dff_0/a_152_16# row_addr_dff_0/dff_0/a_104_24# gnd gnd n w=2u l=0.4u
+  ad=2p pd=6u as=0p ps=0u
M1271 row_addr_dff_0/dff_0/a_104_24# row_addr_dff_0/dff_0/a_24_24# row_addr_dff_0/dff_0/a_84_24# gnd n w=2u l=0.4u
+  ad=2.8p pd=6.8u as=0p ps=0u
M1272 row_addr_dff_0/dff_0/a_320_24# row_addr_dff_0/dff_0/a_24_24# row_addr_dff_0/dff_0/a_280_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1273 vdd bank_0/addr0_3 row_addr_dff_0/dff_0/a_320_336# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1274 bank_0/addr0_3 row_addr_dff_0/dff_0/a_280_24# gnd gnd n w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1275 vdd row_addr_dff_0/dff_0/a_152_16# row_addr_dff_0/dff_0/a_140_296# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1276 row_addr_dff_0/dff_0/a_140_24# clk_buf0 row_addr_dff_0/dff_0/a_104_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1277 row_addr_dff_0/dff_0/a_104_24# clk_buf0 row_addr_dff_0/dff_0/a_84_296# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1278 vdd clk_buf0 row_addr_dff_0/dff_1/a_24_24# vdd p w=8u l=0.4u
+  ad=0p pd=0u as=8p ps=18u
M1279 row_addr_dff_0/dff_1/a_280_24# row_addr_dff_0/dff_1/a_24_24# row_addr_dff_0/dff_1/a_260_296# vdd p w=4u l=0.4u
+  ad=6p pd=11.2u as=2.4p ps=9.2u
M1280 bank_0/addr0_2 row_addr_dff_0/dff_1/a_280_24# vdd vdd p w=8u l=0.4u
+  ad=8p pd=18u as=0p ps=0u
M1281 row_addr_dff_0/dff_1/a_260_24# row_addr_dff_0/dff_1/a_152_16# gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1282 row_addr_dff_0/dff_1/a_84_296# addr0[2] vdd vdd p w=4u l=0.4u
+  ad=3.2p pd=9.6u as=0p ps=0u
M1283 row_addr_dff_0/dff_1/a_84_24# addr0[2] gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1284 gnd bank_0/addr0_2 row_addr_dff_0/dff_1/a_320_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1285 gnd row_addr_dff_0/dff_1/a_152_16# row_addr_dff_0/dff_1/a_140_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1286 row_addr_dff_0/dff_1/a_320_336# clk_buf0 row_addr_dff_0/dff_1/a_280_24# vdd p w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1287 row_addr_dff_0/dff_1/a_152_16# row_addr_dff_0/dff_1/a_104_24# vdd vdd p w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1288 row_addr_dff_0/dff_1/a_140_296# row_addr_dff_0/dff_1/a_24_24# row_addr_dff_0/dff_1/a_104_24# vdd p w=4u l=0.4u
+  ad=3.2p pd=9.6u as=4.8p ps=10.4u
M1289 row_addr_dff_0/dff_1/a_280_24# clk_buf0 row_addr_dff_0/dff_1/a_260_24# gnd n w=2u l=0.4u
+  ad=3.2p pd=7.2u as=0p ps=0u
M1290 gnd clk_buf0 row_addr_dff_0/dff_1/a_24_24# gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4p ps=10u
M1291 row_addr_dff_0/dff_1/a_260_296# row_addr_dff_0/dff_1/a_152_16# vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1292 row_addr_dff_0/dff_1/a_152_16# row_addr_dff_0/dff_1/a_104_24# gnd gnd n w=2u l=0.4u
+  ad=2p pd=6u as=0p ps=0u
M1293 row_addr_dff_0/dff_1/a_104_24# row_addr_dff_0/dff_1/a_24_24# row_addr_dff_0/dff_1/a_84_24# gnd n w=2u l=0.4u
+  ad=2.8p pd=6.8u as=0p ps=0u
M1294 row_addr_dff_0/dff_1/a_320_24# row_addr_dff_0/dff_1/a_24_24# row_addr_dff_0/dff_1/a_280_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1295 vdd bank_0/addr0_2 row_addr_dff_0/dff_1/a_320_336# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1296 bank_0/addr0_2 row_addr_dff_0/dff_1/a_280_24# gnd gnd n w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1297 vdd row_addr_dff_0/dff_1/a_152_16# row_addr_dff_0/dff_1/a_140_296# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1298 row_addr_dff_0/dff_1/a_140_24# clk_buf0 row_addr_dff_0/dff_1/a_104_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1299 row_addr_dff_0/dff_1/a_104_24# clk_buf0 row_addr_dff_0/dff_1/a_84_296# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1300 vdd clk_buf0 row_addr_dff_0/dff_2/a_24_24# vdd p w=8u l=0.4u
+  ad=0p pd=0u as=8p ps=18u
M1301 row_addr_dff_0/dff_2/a_280_24# row_addr_dff_0/dff_2/a_24_24# row_addr_dff_0/dff_2/a_260_296# vdd p w=4u l=0.4u
+  ad=6p pd=11.2u as=2.4p ps=9.2u
M1302 bank_0/addr0_1 row_addr_dff_0/dff_2/a_280_24# vdd vdd p w=8u l=0.4u
+  ad=8p pd=18u as=0p ps=0u
M1303 row_addr_dff_0/dff_2/a_260_24# row_addr_dff_0/dff_2/a_152_16# gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1304 row_addr_dff_0/dff_2/a_84_296# addr0[1] vdd vdd p w=4u l=0.4u
+  ad=3.2p pd=9.6u as=0p ps=0u
M1305 row_addr_dff_0/dff_2/a_84_24# addr0[1] gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1306 gnd bank_0/addr0_1 row_addr_dff_0/dff_2/a_320_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1307 gnd row_addr_dff_0/dff_2/a_152_16# row_addr_dff_0/dff_2/a_140_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1308 row_addr_dff_0/dff_2/a_320_336# clk_buf0 row_addr_dff_0/dff_2/a_280_24# vdd p w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1309 row_addr_dff_0/dff_2/a_152_16# row_addr_dff_0/dff_2/a_104_24# vdd vdd p w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1310 row_addr_dff_0/dff_2/a_140_296# row_addr_dff_0/dff_2/a_24_24# row_addr_dff_0/dff_2/a_104_24# vdd p w=4u l=0.4u
+  ad=3.2p pd=9.6u as=4.8p ps=10.4u
M1311 row_addr_dff_0/dff_2/a_280_24# clk_buf0 row_addr_dff_0/dff_2/a_260_24# gnd n w=2u l=0.4u
+  ad=3.2p pd=7.2u as=0p ps=0u
M1312 gnd clk_buf0 row_addr_dff_0/dff_2/a_24_24# gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4p ps=10u
M1313 row_addr_dff_0/dff_2/a_260_296# row_addr_dff_0/dff_2/a_152_16# vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1314 row_addr_dff_0/dff_2/a_152_16# row_addr_dff_0/dff_2/a_104_24# gnd gnd n w=2u l=0.4u
+  ad=2p pd=6u as=0p ps=0u
M1315 row_addr_dff_0/dff_2/a_104_24# row_addr_dff_0/dff_2/a_24_24# row_addr_dff_0/dff_2/a_84_24# gnd n w=2u l=0.4u
+  ad=2.8p pd=6.8u as=0p ps=0u
M1316 row_addr_dff_0/dff_2/a_320_24# row_addr_dff_0/dff_2/a_24_24# row_addr_dff_0/dff_2/a_280_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1317 vdd bank_0/addr0_1 row_addr_dff_0/dff_2/a_320_336# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1318 bank_0/addr0_1 row_addr_dff_0/dff_2/a_280_24# gnd gnd n w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1319 vdd row_addr_dff_0/dff_2/a_152_16# row_addr_dff_0/dff_2/a_140_296# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1320 row_addr_dff_0/dff_2/a_140_24# clk_buf0 row_addr_dff_0/dff_2/a_104_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1321 row_addr_dff_0/dff_2/a_104_24# clk_buf0 row_addr_dff_0/dff_2/a_84_296# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1322 vdd clk_buf0 row_addr_dff_0/dff_3/a_24_24# vdd p w=8u l=0.4u
+  ad=0p pd=0u as=8p ps=18u
M1323 row_addr_dff_0/dff_3/a_280_24# row_addr_dff_0/dff_3/a_24_24# row_addr_dff_0/dff_3/a_260_296# vdd p w=4u l=0.4u
+  ad=6p pd=11.2u as=2.4p ps=9.2u
M1324 bank_0/addr0_0 row_addr_dff_0/dff_3/a_280_24# vdd vdd p w=8u l=0.4u
+  ad=8p pd=18u as=0p ps=0u
M1325 row_addr_dff_0/dff_3/a_260_24# row_addr_dff_0/dff_3/a_152_16# gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1326 row_addr_dff_0/dff_3/a_84_296# addr0[0] vdd vdd p w=4u l=0.4u
+  ad=3.2p pd=9.6u as=0p ps=0u
M1327 row_addr_dff_0/dff_3/a_84_24# addr0[0] gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1328 gnd bank_0/addr0_0 row_addr_dff_0/dff_3/a_320_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1329 gnd row_addr_dff_0/dff_3/a_152_16# row_addr_dff_0/dff_3/a_140_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1330 row_addr_dff_0/dff_3/a_320_336# clk_buf0 row_addr_dff_0/dff_3/a_280_24# vdd p w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1331 row_addr_dff_0/dff_3/a_152_16# row_addr_dff_0/dff_3/a_104_24# vdd vdd p w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1332 row_addr_dff_0/dff_3/a_140_296# row_addr_dff_0/dff_3/a_24_24# row_addr_dff_0/dff_3/a_104_24# vdd p w=4u l=0.4u
+  ad=3.2p pd=9.6u as=4.8p ps=10.4u
M1333 row_addr_dff_0/dff_3/a_280_24# clk_buf0 row_addr_dff_0/dff_3/a_260_24# gnd n w=2u l=0.4u
+  ad=3.2p pd=7.2u as=0p ps=0u
M1334 gnd clk_buf0 row_addr_dff_0/dff_3/a_24_24# gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4p ps=10u
M1335 row_addr_dff_0/dff_3/a_260_296# row_addr_dff_0/dff_3/a_152_16# vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1336 row_addr_dff_0/dff_3/a_152_16# row_addr_dff_0/dff_3/a_104_24# gnd gnd n w=2u l=0.4u
+  ad=2p pd=6u as=0p ps=0u
M1337 row_addr_dff_0/dff_3/a_104_24# row_addr_dff_0/dff_3/a_24_24# row_addr_dff_0/dff_3/a_84_24# gnd n w=2u l=0.4u
+  ad=2.8p pd=6.8u as=0p ps=0u
M1338 row_addr_dff_0/dff_3/a_320_24# row_addr_dff_0/dff_3/a_24_24# row_addr_dff_0/dff_3/a_280_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1339 vdd bank_0/addr0_0 row_addr_dff_0/dff_3/a_320_336# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1340 bank_0/addr0_0 row_addr_dff_0/dff_3/a_280_24# gnd gnd n w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1341 vdd row_addr_dff_0/dff_3/a_152_16# row_addr_dff_0/dff_3/a_140_296# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1342 row_addr_dff_0/dff_3/a_140_24# clk_buf0 row_addr_dff_0/dff_3/a_104_24# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1343 row_addr_dff_0/dff_3/a_104_24# clk_buf0 row_addr_dff_0/dff_3/a_84_296# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1344 vdd w_en0 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_20_328# vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=2.8p ps=9.6u
M1345 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_64_360# bank_0/din0_1 vdd vdd p w=1.4u l=0.4u
+  ad=1.4p pd=4.8u as=0p ps=0u
M1346 gnd bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_36_704# bl0_1 gnd n w=2.4u l=0.4u
+  ad=0p pd=0u as=15.2p ps=64.4u
M1347 gnd bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_8_284# bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_16_500# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1348 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_40_228# w_en0 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_8_284# gnd n w=1.4u l=0.4u
+  ad=1.68p pd=5.2u as=1.4p ps=4.8u
M1349 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_64_360# bank_0/din0_1 gnd gnd n w=0.8u l=0.4u
+  ad=0.8p pd=3.6u as=0p ps=0u
M1350 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_48_328# w_en0 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_20_328# gnd n w=1.4u l=0.4u
+  ad=1.68p pd=5.2u as=1.4p ps=4.8u
M1351 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_36_704# bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_20_328# vdd vdd p w=1.4u l=0.4u
+  ad=1.4p pd=4.8u as=0p ps=0u
M1352 vdd bank_0/din0_1 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_8_284# vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=1.68p ps=5.2u
M1353 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_20_328# bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_64_360# vdd vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1354 br0_1 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_16_500# gnd gnd n w=2.4u l=0.4u
+  ad=15.2p pd=64.4u as=0p ps=0u
M1355 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_36_704# bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_20_328# gnd gnd n w=0.8u l=0.4u
+  ad=0.8p pd=3.6u as=0p ps=0u
M1356 gnd bank_0/din0_1 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_40_228# gnd n w=1.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1357 vdd bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_8_284# bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_16_500# vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=1.4p ps=4.8u
M1358 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_8_284# w_en0 vdd vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1359 gnd bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_64_360# bank_0/port_data_0_0/write_driver_array_0_0/write_driver_0/a_48_328# gnd n w=1.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1360 vdd w_en0 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_20_328# vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=2.8p ps=9.6u
M1361 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_64_360# bank_0/din0_0 vdd vdd p w=1.4u l=0.4u
+  ad=1.4p pd=4.8u as=0p ps=0u
M1362 gnd bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_36_704# bl0_0 gnd n w=2.4u l=0.4u
+  ad=0p pd=0u as=15.2p ps=64.4u
M1363 gnd bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_8_284# bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_16_500# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1364 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_40_228# w_en0 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_8_284# gnd n w=1.4u l=0.4u
+  ad=1.68p pd=5.2u as=1.4p ps=4.8u
M1365 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_64_360# bank_0/din0_0 gnd gnd n w=0.8u l=0.4u
+  ad=0.8p pd=3.6u as=0p ps=0u
M1366 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_48_328# w_en0 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_20_328# gnd n w=1.4u l=0.4u
+  ad=1.68p pd=5.2u as=1.4p ps=4.8u
M1367 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_36_704# bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_20_328# vdd vdd p w=1.4u l=0.4u
+  ad=1.4p pd=4.8u as=0p ps=0u
M1368 vdd bank_0/din0_0 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_8_284# vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=1.68p ps=5.2u
M1369 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_20_328# bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_64_360# vdd vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1370 br0_0 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_16_500# gnd gnd n w=2.4u l=0.4u
+  ad=15.2p pd=64.4u as=0p ps=0u
M1371 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_36_704# bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_20_328# gnd gnd n w=0.8u l=0.4u
+  ad=0.8p pd=3.6u as=0p ps=0u
M1372 gnd bank_0/din0_0 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_40_228# gnd n w=1.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1373 vdd bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_8_284# bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_16_500# vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=1.4p ps=4.8u
M1374 bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_8_284# w_en0 vdd vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1375 gnd bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_64_360# bank_0/port_data_0_0/write_driver_array_0_0/write_driver_1/a_48_328# gnd n w=1.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1376 br0_1 p_en_bar0 vdd vdd p w=1.6u l=0.4u
+  ad=8.005p pd=22.1u as=0p ps=0u
M1377 vdd p_en_bar0 bl0_1 vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=8.005p ps=22.1u
M1378 br0_1 p_en_bar0 bl0_1 vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1379 br0_0 p_en_bar0 vdd vdd p w=1.6u l=0.4u
+  ad=8.005p pd=22.1u as=0p ps=0u
M1380 vdd p_en_bar0 bl0_0 vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=8.005p ps=22.1u
M1381 br0_0 p_en_bar0 bl0_0 vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1382 bank_0/port_data_0_0/rbl_br p_en_bar0 vdd vdd p w=1.6u l=0.4u
+  ad=3.205p pd=10.5u as=0p ps=0u
M1383 vdd p_en_bar0 rbl_bl0 vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=3.205p ps=10.5u
M1384 bank_0/port_data_0_0/rbl_br p_en_bar0 rbl_bl0 vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1385 bank_0/port_data_0_0/sense_amp_array_0_0/sense_amp_0/a_48_304# dout0[1] vdd vdd p w=3.6u l=0.4u
+  ad=8.4p pd=20.8u as=0p ps=0u
M1386 vdd bank_0/port_data_0_0/sense_amp_array_0_0/sense_amp_0/a_48_304# dout0[1] vdd p w=3.6u l=0.4u
+  ad=0p pd=0u as=8.4p ps=20.8u
M1387 gnd s_en0 bank_0/port_data_0_0/sense_amp_array_0_0/sense_amp_0/a_56_432# gnd n w=1.8u l=0.4u
+  ad=0p pd=0u as=3.96p ps=11.6u
M1388 bl0_1 s_en0 dout0[1] vdd p w=4.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1389 bank_0/port_data_0_0/sense_amp_array_0_0/sense_amp_0/a_48_304# dout0[1] bank_0/port_data_0_0/sense_amp_array_0_0/sense_amp_0/a_56_432# gnd n w=1.8u l=0.4u
+  ad=1.8p pd=5.6u as=0p ps=0u
M1390 bank_0/port_data_0_0/sense_amp_array_0_0/sense_amp_0/a_48_304# s_en0 br0_1 vdd p w=4.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1391 bank_0/port_data_0_0/sense_amp_array_0_0/sense_amp_0/a_56_432# bank_0/port_data_0_0/sense_amp_array_0_0/sense_amp_0/a_48_304# dout0[1] gnd n w=1.8u l=0.4u
+  ad=0p pd=0u as=1.8p ps=5.6u
M1392 bank_0/port_data_0_0/sense_amp_array_0_0/sense_amp_1/a_48_304# dout0[0] vdd vdd p w=3.6u l=0.4u
+  ad=8.4p pd=20.8u as=0p ps=0u
M1393 vdd bank_0/port_data_0_0/sense_amp_array_0_0/sense_amp_1/a_48_304# dout0[0] vdd p w=3.6u l=0.4u
+  ad=0p pd=0u as=8.4p ps=20.8u
M1394 gnd s_en0 bank_0/port_data_0_0/sense_amp_array_0_0/sense_amp_1/a_56_432# gnd n w=1.8u l=0.4u
+  ad=0p pd=0u as=3.96p ps=11.6u
M1395 bl0_0 s_en0 dout0[0] vdd p w=4.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1396 bank_0/port_data_0_0/sense_amp_array_0_0/sense_amp_1/a_48_304# dout0[0] bank_0/port_data_0_0/sense_amp_array_0_0/sense_amp_1/a_56_432# gnd n w=1.8u l=0.4u
+  ad=1.8p pd=5.6u as=0p ps=0u
M1397 bank_0/port_data_0_0/sense_amp_array_0_0/sense_amp_1/a_48_304# s_en0 br0_0 vdd p w=4.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1398 bank_0/port_data_0_0/sense_amp_array_0_0/sense_amp_1/a_56_432# bank_0/port_data_0_0/sense_amp_array_0_0/sense_amp_1/a_48_304# dout0[0] gnd n w=1.8u l=0.4u
+  ad=0p pd=0u as=1.8p ps=5.6u
M1399 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_1/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1400 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_1/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1401 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_1/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1402 vdd bank_0/port_address_0_0/wl_14 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=186.09p pd=842.65u as=13.6p ps=61.2u
M1403 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_1/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1404 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_1/Q bank_0/port_address_0_0/wl_14 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=13.6p ps=61.2u
M1405 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_0/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1406 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_0/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1407 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_0/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1408 vdd bank_0/port_address_0_0/wl_15 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1409 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_0/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1410 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_0/Q bank_0/port_address_0_0/wl_15 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1411 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_2/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1412 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_2/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1413 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_2/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1414 vdd bank_0/port_address_0_0/wl_13 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1415 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_2/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1416 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_2/Q bank_0/port_address_0_0/wl_13 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1417 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_3/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1418 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_3/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1419 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_3/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1420 vdd bank_0/port_address_0_0/wl_12 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1421 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_3/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1422 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_3/Q bank_0/port_address_0_0/wl_12 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1423 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_10/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1424 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_10/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1425 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_10/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1426 vdd bank_0/port_address_0_0/wl_5 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1427 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_10/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1428 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_10/Q bank_0/port_address_0_0/wl_5 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1429 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_4/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1430 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_4/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1431 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_4/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1432 vdd bank_0/port_address_0_0/wl_11 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1433 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_4/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1434 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_4/Q bank_0/port_address_0_0/wl_11 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1435 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_11/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1436 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_11/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1437 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_11/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1438 vdd bank_0/port_address_0_0/wl_4 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1439 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_11/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1440 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_11/Q bank_0/port_address_0_0/wl_4 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1441 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_12/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1442 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_12/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1443 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_12/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1444 vdd bank_0/port_address_0_0/wl_3 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1445 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_12/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1446 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_12/Q bank_0/port_address_0_0/wl_3 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1447 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_5/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1448 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_5/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1449 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_5/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1450 vdd bank_0/port_address_0_0/wl_10 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1451 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_5/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1452 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_5/Q bank_0/port_address_0_0/wl_10 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1453 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_13/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1454 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_13/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1455 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_13/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1456 vdd bank_0/port_address_0_0/wl_2 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1457 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_13/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1458 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_13/Q bank_0/port_address_0_0/wl_2 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1459 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_6/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1460 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_6/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1461 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_6/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1462 vdd bank_0/port_address_0_0/wl_9 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1463 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_6/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1464 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_6/Q bank_0/port_address_0_0/wl_9 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1465 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_14/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1466 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_14/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1467 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_14/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1468 vdd bank_0/port_address_0_0/wl_1 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1469 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_14/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1470 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_14/Q bank_0/port_address_0_0/wl_1 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1471 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_7/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1472 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_7/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1473 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_7/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1474 vdd bank_0/port_address_0_0/wl_8 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1475 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_7/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1476 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_7/Q bank_0/port_address_0_0/wl_8 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1477 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_15/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1478 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_15/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1479 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_15/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1480 vdd bank_0/port_address_0_0/wl_0 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1481 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_15/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1482 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_15/Q bank_0/port_address_0_0/wl_0 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1483 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_8/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1484 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_8/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1485 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_8/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1486 vdd bank_0/port_address_0_0/wl_7 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1487 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_8/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1488 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_8/Q bank_0/port_address_0_0/wl_7 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1489 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_16/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1490 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_16/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1491 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_16/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1492 vdd wl_en0 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1493 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_16/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1494 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_16/Q wl_en0 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1495 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_9/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1496 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_9/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1497 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_9/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1498 vdd bank_0/port_address_0_0/wl_6 bank_0/port_data_0_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1499 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_9/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1500 bank_0/replica_bitcell_array_0_0/replica_column_0_0/replica_cell_6t_9/Q bank_0/port_address_0_0/wl_6 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1501 bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_0/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1502 bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_0/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1503 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_0/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1504 bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_0/a_28_56# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/wl_0 bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_0/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1505 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_0/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1506 bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/wl_0 bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_0/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1507 bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_1/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1508 bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_1/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1509 vdd bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_1/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1510 bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_1/a_28_56# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/wl_0 bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_1/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1511 gnd bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_1/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1512 bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/wl_0 bank_0/replica_bitcell_array_0_0/replica_column_0_0/dummy_cell_6t_1/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1513 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_2/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_2/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1514 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_2/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_2/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1515 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_2/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_2/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1516 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_2/a_28_56# bank_0/port_address_0_0/wl_14 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_2/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1517 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_2/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_2/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1518 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_2/a_36_64# bank_0/port_address_0_0/wl_14 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_2/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1519 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_3/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_3/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1520 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_3/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_3/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1521 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_3/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_3/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1522 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_3/a_28_56# bank_0/port_address_0_0/wl_13 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_3/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1523 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_3/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_3/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1524 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_3/a_36_64# bank_0/port_address_0_0/wl_13 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_3/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1525 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_4/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_4/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1526 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_4/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_4/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1527 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_4/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_4/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1528 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_4/a_28_56# bank_0/port_address_0_0/wl_12 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_4/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1529 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_4/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_4/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1530 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_4/a_36_64# bank_0/port_address_0_0/wl_12 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_4/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1531 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_5/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_5/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1532 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_5/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_5/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1533 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_5/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_5/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1534 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_5/a_28_56# bank_0/port_address_0_0/wl_11 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_5/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1535 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_5/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_5/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1536 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_5/a_36_64# bank_0/port_address_0_0/wl_11 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_5/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1537 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_6/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_6/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1538 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_6/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_6/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1539 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_6/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_6/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1540 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_6/a_28_56# bank_0/port_address_0_0/wl_10 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_6/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1541 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_6/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_6/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1542 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_6/a_36_64# bank_0/port_address_0_0/wl_10 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_6/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1543 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_7/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_7/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1544 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_7/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_7/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1545 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_7/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_7/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1546 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_7/a_28_56# bank_0/port_address_0_0/wl_9 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_7/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1547 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_7/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_7/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1548 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_7/a_36_64# bank_0/port_address_0_0/wl_9 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_7/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1549 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_8/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_8/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1550 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_8/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_8/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1551 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_8/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_8/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1552 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_8/a_28_56# bank_0/port_address_0_0/wl_8 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_8/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1553 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_8/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_8/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1554 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_8/a_36_64# bank_0/port_address_0_0/wl_8 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_8/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1555 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_9/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_9/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1556 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_9/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_9/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1557 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_9/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_9/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1558 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_9/a_28_56# bank_0/port_address_0_0/wl_7 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_9/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1559 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_9/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_9/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1560 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_9/a_36_64# bank_0/port_address_0_0/wl_7 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_9/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1561 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_10/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_10/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1562 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_10/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_10/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1563 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_10/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_10/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1564 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_10/a_28_56# bank_0/port_address_0_0/wl_6 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_10/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1565 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_10/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_10/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1566 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_10/a_36_64# bank_0/port_address_0_0/wl_6 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_10/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1567 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_11/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_11/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1568 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_11/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_11/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1569 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_11/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_11/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1570 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_11/a_28_56# bank_0/port_address_0_0/wl_5 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_11/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1571 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_11/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_11/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1572 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_11/a_36_64# bank_0/port_address_0_0/wl_5 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_11/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1573 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_12/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_12/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1574 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_12/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_12/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1575 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_12/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_12/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1576 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_12/a_28_56# bank_0/port_address_0_0/wl_4 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_12/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1577 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_12/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_12/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1578 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_12/a_36_64# bank_0/port_address_0_0/wl_4 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_12/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1579 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_13/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_13/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1580 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_13/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_13/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1581 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_13/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_13/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1582 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_13/a_28_56# bank_0/port_address_0_0/wl_3 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_13/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1583 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_13/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_13/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1584 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_13/a_36_64# bank_0/port_address_0_0/wl_3 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_13/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1585 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_14/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_14/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1586 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_14/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_14/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1587 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_14/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_14/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1588 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_14/a_28_56# bank_0/port_address_0_0/wl_2 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_14/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1589 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_14/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_14/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1590 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_14/a_36_64# bank_0/port_address_0_0/wl_2 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_14/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1591 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_15/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_15/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1592 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_15/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_15/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1593 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_15/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_15/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1594 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_15/a_28_56# bank_0/port_address_0_0/wl_1 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_15/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1595 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_15/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_15/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1596 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_15/a_36_64# bank_0/port_address_0_0/wl_1 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_15/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1597 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_16/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_16/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1598 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_16/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_16/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1599 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_16/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_16/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1600 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_16/a_28_56# bank_0/port_address_0_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_16/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1601 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_16/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_16/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1602 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_16/a_36_64# bank_0/port_address_0_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_16/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1603 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_17/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_17/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1604 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_17/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_17/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1605 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_17/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_17/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1606 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_17/a_28_56# wl_en0 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_17/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1607 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_17/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_17/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1608 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_17/a_36_64# wl_en0 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_17/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1609 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_18/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_18/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1610 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_18/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_18/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1611 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_18/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_18/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1612 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_18/a_28_56# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_18/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1613 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_18/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_18/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1614 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_18/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_18/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1615 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_0/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1616 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_0/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1617 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_0/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1618 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_0/a_28_56# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_0/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1619 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_0/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1620 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_0/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1621 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_1/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1622 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_1/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1623 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_1/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1624 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_1/a_28_56# bank_0/port_address_0_0/wl_15 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_1/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1625 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_1/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1626 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_1/a_36_64# bank_0/port_address_0_0/wl_15 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/dummy_cell_6t_1/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1627 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_2/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_2/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1628 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_2/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_2/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1629 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_2/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_2/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1630 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_2/a_28_56# bank_0/port_address_0_0/wl_14 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_2/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1631 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_2/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_2/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1632 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_2/a_36_64# bank_0/port_address_0_0/wl_14 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_2/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1633 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_3/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_3/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1634 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_3/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_3/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1635 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_3/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_3/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1636 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_3/a_28_56# bank_0/port_address_0_0/wl_13 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_3/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1637 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_3/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_3/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1638 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_3/a_36_64# bank_0/port_address_0_0/wl_13 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_3/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1639 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_4/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_4/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1640 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_4/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_4/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1641 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_4/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_4/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1642 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_4/a_28_56# bank_0/port_address_0_0/wl_12 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_4/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1643 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_4/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_4/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1644 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_4/a_36_64# bank_0/port_address_0_0/wl_12 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_4/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1645 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_5/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_5/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1646 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_5/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_5/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1647 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_5/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_5/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1648 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_5/a_28_56# bank_0/port_address_0_0/wl_11 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_5/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1649 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_5/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_5/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1650 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_5/a_36_64# bank_0/port_address_0_0/wl_11 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_5/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1651 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_6/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_6/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1652 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_6/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_6/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1653 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_6/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_6/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1654 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_6/a_28_56# bank_0/port_address_0_0/wl_10 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_6/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1655 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_6/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_6/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1656 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_6/a_36_64# bank_0/port_address_0_0/wl_10 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_6/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1657 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_7/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_7/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1658 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_7/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_7/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1659 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_7/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_7/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1660 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_7/a_28_56# bank_0/port_address_0_0/wl_9 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_7/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1661 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_7/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_7/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1662 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_7/a_36_64# bank_0/port_address_0_0/wl_9 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_7/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1663 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_8/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_8/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1664 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_8/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_8/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1665 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_8/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_8/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1666 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_8/a_28_56# bank_0/port_address_0_0/wl_8 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_8/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1667 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_8/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_8/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1668 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_8/a_36_64# bank_0/port_address_0_0/wl_8 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_8/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1669 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_9/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_9/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1670 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_9/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_9/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1671 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_9/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_9/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1672 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_9/a_28_56# bank_0/port_address_0_0/wl_7 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_9/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1673 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_9/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_9/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1674 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_9/a_36_64# bank_0/port_address_0_0/wl_7 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_9/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1675 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_10/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_10/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1676 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_10/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_10/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1677 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_10/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_10/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1678 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_10/a_28_56# bank_0/port_address_0_0/wl_6 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_10/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1679 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_10/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_10/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1680 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_10/a_36_64# bank_0/port_address_0_0/wl_6 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_10/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1681 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_11/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_11/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1682 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_11/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_11/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1683 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_11/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_11/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1684 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_11/a_28_56# bank_0/port_address_0_0/wl_5 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_11/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1685 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_11/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_11/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1686 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_11/a_36_64# bank_0/port_address_0_0/wl_5 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_11/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1687 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_12/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_12/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1688 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_12/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_12/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1689 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_12/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_12/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1690 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_12/a_28_56# bank_0/port_address_0_0/wl_4 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_12/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1691 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_12/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_12/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1692 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_12/a_36_64# bank_0/port_address_0_0/wl_4 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_12/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1693 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_13/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_13/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1694 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_13/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_13/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1695 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_13/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_13/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1696 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_13/a_28_56# bank_0/port_address_0_0/wl_3 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_13/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1697 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_13/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_13/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1698 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_13/a_36_64# bank_0/port_address_0_0/wl_3 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_13/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1699 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_14/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_14/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1700 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_14/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_14/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1701 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_14/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_14/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1702 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_14/a_28_56# bank_0/port_address_0_0/wl_2 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_14/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1703 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_14/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_14/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1704 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_14/a_36_64# bank_0/port_address_0_0/wl_2 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_14/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1705 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_15/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_15/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1706 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_15/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_15/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1707 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_15/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_15/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1708 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_15/a_28_56# bank_0/port_address_0_0/wl_1 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_15/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1709 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_15/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_15/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1710 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_15/a_36_64# bank_0/port_address_0_0/wl_1 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_15/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1711 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_16/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_16/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1712 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_16/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_16/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1713 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_16/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_16/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1714 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_16/a_28_56# bank_0/port_address_0_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_16/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1715 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_16/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_16/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1716 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_16/a_36_64# bank_0/port_address_0_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_16/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1717 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_17/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_17/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1718 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_17/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_17/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1719 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_17/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_17/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1720 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_17/a_28_56# wl_en0 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_17/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1721 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_17/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_17/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1722 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_17/a_36_64# wl_en0 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_17/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1723 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_18/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_18/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1724 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_18/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_18/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1725 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_18/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_18/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1726 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_18/a_28_56# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_18/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1727 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_18/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_18/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1728 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_18/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_18/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1729 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_0/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1730 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_0/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1731 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_0/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1732 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_0/a_28_56# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_0/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1733 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_0/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1734 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_0/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1735 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_1/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1736 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_1/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1737 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_1/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1738 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_1/a_28_56# bank_0/port_address_0_0/wl_15 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_1/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1739 gnd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_1/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1740 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_1/a_36_64# bank_0/port_address_0_0/wl_15 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/dummy_cell_6t_1/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1741 bitcell_Q_b0_r15_c1 bitcell_Q_bar_b0_r15_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1742 bitcell_Q_b0_r15_c1 bitcell_Q_bar_b0_r15_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1743 vdd bitcell_Q_b0_r15_c1 bitcell_Q_bar_b0_r15_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1744 bitcell_Q_bar_b0_r15_c1 bank_0/port_address_0_0/wl_15 br0_1 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1745 gnd bitcell_Q_b0_r15_c1 bitcell_Q_bar_b0_r15_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1746 bitcell_Q_b0_r15_c1 bank_0/port_address_0_0/wl_15 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1747 bitcell_Q_b0_r14_c1 bitcell_Q_bar_b0_r14_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1748 bitcell_Q_b0_r14_c1 bitcell_Q_bar_b0_r14_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1749 vdd bitcell_Q_b0_r14_c1 bitcell_Q_bar_b0_r14_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1750 bitcell_Q_bar_b0_r14_c1 bank_0/port_address_0_0/wl_14 br0_1 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1751 gnd bitcell_Q_b0_r14_c1 bitcell_Q_bar_b0_r14_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1752 bitcell_Q_b0_r14_c1 bank_0/port_address_0_0/wl_14 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1753 bitcell_Q_b0_r13_c1 bitcell_Q_bar_b0_r13_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1754 bitcell_Q_b0_r13_c1 bitcell_Q_bar_b0_r13_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1755 vdd bitcell_Q_b0_r13_c1 bitcell_Q_bar_b0_r13_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1756 bitcell_Q_bar_b0_r13_c1 bank_0/port_address_0_0/wl_13 br0_1 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1757 gnd bitcell_Q_b0_r13_c1 bitcell_Q_bar_b0_r13_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1758 bitcell_Q_b0_r13_c1 bank_0/port_address_0_0/wl_13 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1759 bitcell_Q_b0_r12_c1 bitcell_Q_bar_b0_r12_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1760 bitcell_Q_b0_r12_c1 bitcell_Q_bar_b0_r12_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1761 vdd bitcell_Q_b0_r12_c1 bitcell_Q_bar_b0_r12_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1762 bitcell_Q_bar_b0_r12_c1 bank_0/port_address_0_0/wl_12 br0_1 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1763 gnd bitcell_Q_b0_r12_c1 bitcell_Q_bar_b0_r12_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1764 bitcell_Q_b0_r12_c1 bank_0/port_address_0_0/wl_12 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1765 bitcell_Q_b0_r11_c1 bitcell_Q_bar_b0_r11_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1766 bitcell_Q_b0_r11_c1 bitcell_Q_bar_b0_r11_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1767 vdd bitcell_Q_b0_r11_c1 bitcell_Q_bar_b0_r11_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1768 bitcell_Q_bar_b0_r11_c1 bank_0/port_address_0_0/wl_11 br0_1 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1769 gnd bitcell_Q_b0_r11_c1 bitcell_Q_bar_b0_r11_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1770 bitcell_Q_b0_r11_c1 bank_0/port_address_0_0/wl_11 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1771 bitcell_Q_b0_r10_c1 bitcell_Q_bar_b0_r10_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1772 bitcell_Q_b0_r10_c1 bitcell_Q_bar_b0_r10_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1773 vdd bitcell_Q_b0_r10_c1 bitcell_Q_bar_b0_r10_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1774 bitcell_Q_bar_b0_r10_c1 bank_0/port_address_0_0/wl_10 br0_1 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1775 gnd bitcell_Q_b0_r10_c1 bitcell_Q_bar_b0_r10_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1776 bitcell_Q_b0_r10_c1 bank_0/port_address_0_0/wl_10 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1777 bitcell_Q_b0_r9_c1 bitcell_Q_bar_b0_r9_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1778 bitcell_Q_b0_r9_c1 bitcell_Q_bar_b0_r9_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1779 vdd bitcell_Q_b0_r9_c1 bitcell_Q_bar_b0_r9_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1780 bitcell_Q_bar_b0_r9_c1 bank_0/port_address_0_0/wl_9 br0_1 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1781 gnd bitcell_Q_b0_r9_c1 bitcell_Q_bar_b0_r9_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1782 bitcell_Q_b0_r9_c1 bank_0/port_address_0_0/wl_9 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1783 bitcell_Q_b0_r8_c1 bitcell_Q_bar_b0_r8_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1784 bitcell_Q_b0_r8_c1 bitcell_Q_bar_b0_r8_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1785 vdd bitcell_Q_b0_r8_c1 bitcell_Q_bar_b0_r8_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1786 bitcell_Q_bar_b0_r8_c1 bank_0/port_address_0_0/wl_8 br0_1 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1787 gnd bitcell_Q_b0_r8_c1 bitcell_Q_bar_b0_r8_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1788 bitcell_Q_b0_r8_c1 bank_0/port_address_0_0/wl_8 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1789 bitcell_Q_b0_r7_c1 bitcell_Q_bar_b0_r7_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1790 bitcell_Q_b0_r7_c1 bitcell_Q_bar_b0_r7_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1791 vdd bitcell_Q_b0_r7_c1 bitcell_Q_bar_b0_r7_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1792 bitcell_Q_bar_b0_r7_c1 bank_0/port_address_0_0/wl_7 br0_1 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1793 gnd bitcell_Q_b0_r7_c1 bitcell_Q_bar_b0_r7_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1794 bitcell_Q_b0_r7_c1 bank_0/port_address_0_0/wl_7 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1795 bitcell_Q_b0_r6_c1 bitcell_Q_bar_b0_r6_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1796 bitcell_Q_b0_r6_c1 bitcell_Q_bar_b0_r6_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1797 vdd bitcell_Q_b0_r6_c1 bitcell_Q_bar_b0_r6_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1798 bitcell_Q_bar_b0_r6_c1 bank_0/port_address_0_0/wl_6 br0_1 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1799 gnd bitcell_Q_b0_r6_c1 bitcell_Q_bar_b0_r6_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1800 bitcell_Q_b0_r6_c1 bank_0/port_address_0_0/wl_6 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1801 bitcell_Q_b0_r1_c0 bitcell_Q_bar_b0_r1_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1802 bitcell_Q_b0_r1_c0 bitcell_Q_bar_b0_r1_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1803 vdd bitcell_Q_b0_r1_c0 bitcell_Q_bar_b0_r1_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1804 bitcell_Q_bar_b0_r1_c0 bank_0/port_address_0_0/wl_1 br0_0 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1805 gnd bitcell_Q_b0_r1_c0 bitcell_Q_bar_b0_r1_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1806 bitcell_Q_b0_r1_c0 bank_0/port_address_0_0/wl_1 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1807 bitcell_Q_b0_r0_c0 bitcell_Q_bar_b0_r0_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1808 bitcell_Q_b0_r0_c0 bitcell_Q_bar_b0_r0_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1809 vdd bitcell_Q_b0_r0_c0 bitcell_Q_bar_b0_r0_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1810 bitcell_Q_bar_b0_r0_c0 bank_0/port_address_0_0/wl_0 br0_0 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1811 gnd bitcell_Q_b0_r0_c0 bitcell_Q_bar_b0_r0_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1812 bitcell_Q_b0_r0_c0 bank_0/port_address_0_0/wl_0 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1813 bitcell_Q_b0_r11_c0 bitcell_Q_bar_b0_r11_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1814 bitcell_Q_b0_r11_c0 bitcell_Q_bar_b0_r11_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1815 vdd bitcell_Q_b0_r11_c0 bitcell_Q_bar_b0_r11_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1816 bitcell_Q_bar_b0_r11_c0 bank_0/port_address_0_0/wl_11 br0_0 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1817 gnd bitcell_Q_b0_r11_c0 bitcell_Q_bar_b0_r11_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1818 bitcell_Q_b0_r11_c0 bank_0/port_address_0_0/wl_11 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1819 bitcell_Q_b0_r5_c1 bitcell_Q_bar_b0_r5_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1820 bitcell_Q_b0_r5_c1 bitcell_Q_bar_b0_r5_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1821 vdd bitcell_Q_b0_r5_c1 bitcell_Q_bar_b0_r5_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1822 bitcell_Q_bar_b0_r5_c1 bank_0/port_address_0_0/wl_5 br0_1 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1823 gnd bitcell_Q_b0_r5_c1 bitcell_Q_bar_b0_r5_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1824 bitcell_Q_b0_r5_c1 bank_0/port_address_0_0/wl_5 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1825 bitcell_Q_b0_r10_c0 bitcell_Q_bar_b0_r10_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1826 bitcell_Q_b0_r10_c0 bitcell_Q_bar_b0_r10_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1827 vdd bitcell_Q_b0_r10_c0 bitcell_Q_bar_b0_r10_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1828 bitcell_Q_bar_b0_r10_c0 bank_0/port_address_0_0/wl_10 br0_0 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1829 gnd bitcell_Q_b0_r10_c0 bitcell_Q_bar_b0_r10_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1830 bitcell_Q_b0_r10_c0 bank_0/port_address_0_0/wl_10 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1831 bitcell_Q_b0_r4_c1 bitcell_Q_bar_b0_r4_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1832 bitcell_Q_b0_r4_c1 bitcell_Q_bar_b0_r4_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1833 vdd bitcell_Q_b0_r4_c1 bitcell_Q_bar_b0_r4_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1834 bitcell_Q_bar_b0_r4_c1 bank_0/port_address_0_0/wl_4 br0_1 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1835 gnd bitcell_Q_b0_r4_c1 bitcell_Q_bar_b0_r4_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1836 bitcell_Q_b0_r4_c1 bank_0/port_address_0_0/wl_4 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1837 bitcell_Q_b0_r9_c0 bitcell_Q_bar_b0_r9_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1838 bitcell_Q_b0_r9_c0 bitcell_Q_bar_b0_r9_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1839 vdd bitcell_Q_b0_r9_c0 bitcell_Q_bar_b0_r9_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1840 bitcell_Q_bar_b0_r9_c0 bank_0/port_address_0_0/wl_9 br0_0 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1841 gnd bitcell_Q_b0_r9_c0 bitcell_Q_bar_b0_r9_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1842 bitcell_Q_b0_r9_c0 bank_0/port_address_0_0/wl_9 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1843 bitcell_Q_b0_r3_c1 bitcell_Q_bar_b0_r3_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1844 bitcell_Q_b0_r3_c1 bitcell_Q_bar_b0_r3_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1845 vdd bitcell_Q_b0_r3_c1 bitcell_Q_bar_b0_r3_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1846 bitcell_Q_bar_b0_r3_c1 bank_0/port_address_0_0/wl_3 br0_1 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1847 gnd bitcell_Q_b0_r3_c1 bitcell_Q_bar_b0_r3_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1848 bitcell_Q_b0_r3_c1 bank_0/port_address_0_0/wl_3 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1849 bitcell_Q_b0_r8_c0 bitcell_Q_bar_b0_r8_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1850 bitcell_Q_b0_r8_c0 bitcell_Q_bar_b0_r8_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1851 vdd bitcell_Q_b0_r8_c0 bitcell_Q_bar_b0_r8_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1852 bitcell_Q_bar_b0_r8_c0 bank_0/port_address_0_0/wl_8 br0_0 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1853 gnd bitcell_Q_b0_r8_c0 bitcell_Q_bar_b0_r8_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1854 bitcell_Q_b0_r8_c0 bank_0/port_address_0_0/wl_8 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1855 bitcell_Q_b0_r2_c1 bitcell_Q_bar_b0_r2_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1856 bitcell_Q_b0_r2_c1 bitcell_Q_bar_b0_r2_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1857 vdd bitcell_Q_b0_r2_c1 bitcell_Q_bar_b0_r2_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1858 bitcell_Q_bar_b0_r2_c1 bank_0/port_address_0_0/wl_2 br0_1 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1859 gnd bitcell_Q_b0_r2_c1 bitcell_Q_bar_b0_r2_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1860 bitcell_Q_b0_r2_c1 bank_0/port_address_0_0/wl_2 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1861 bitcell_Q_b0_r7_c0 bitcell_Q_bar_b0_r7_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1862 bitcell_Q_b0_r7_c0 bitcell_Q_bar_b0_r7_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1863 vdd bitcell_Q_b0_r7_c0 bitcell_Q_bar_b0_r7_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1864 bitcell_Q_bar_b0_r7_c0 bank_0/port_address_0_0/wl_7 br0_0 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1865 gnd bitcell_Q_b0_r7_c0 bitcell_Q_bar_b0_r7_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1866 bitcell_Q_b0_r7_c0 bank_0/port_address_0_0/wl_7 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1867 bitcell_Q_b0_r1_c1 bitcell_Q_bar_b0_r1_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1868 bitcell_Q_b0_r1_c1 bitcell_Q_bar_b0_r1_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1869 vdd bitcell_Q_b0_r1_c1 bitcell_Q_bar_b0_r1_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1870 bitcell_Q_bar_b0_r1_c1 bank_0/port_address_0_0/wl_1 br0_1 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1871 gnd bitcell_Q_b0_r1_c1 bitcell_Q_bar_b0_r1_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1872 bitcell_Q_b0_r1_c1 bank_0/port_address_0_0/wl_1 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1873 bitcell_Q_b0_r6_c0 bitcell_Q_bar_b0_r6_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1874 bitcell_Q_b0_r6_c0 bitcell_Q_bar_b0_r6_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1875 vdd bitcell_Q_b0_r6_c0 bitcell_Q_bar_b0_r6_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1876 bitcell_Q_bar_b0_r6_c0 bank_0/port_address_0_0/wl_6 br0_0 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1877 gnd bitcell_Q_b0_r6_c0 bitcell_Q_bar_b0_r6_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1878 bitcell_Q_b0_r6_c0 bank_0/port_address_0_0/wl_6 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1879 bitcell_Q_b0_r0_c1 bitcell_Q_bar_b0_r0_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1880 bitcell_Q_b0_r0_c1 bitcell_Q_bar_b0_r0_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1881 vdd bitcell_Q_b0_r0_c1 bitcell_Q_bar_b0_r0_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1882 bitcell_Q_bar_b0_r0_c1 bank_0/port_address_0_0/wl_0 br0_1 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1883 gnd bitcell_Q_b0_r0_c1 bitcell_Q_bar_b0_r0_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1884 bitcell_Q_b0_r0_c1 bank_0/port_address_0_0/wl_0 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1885 bitcell_Q_b0_r5_c0 bitcell_Q_bar_b0_r5_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1886 bitcell_Q_b0_r5_c0 bitcell_Q_bar_b0_r5_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1887 vdd bitcell_Q_b0_r5_c0 bitcell_Q_bar_b0_r5_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1888 bitcell_Q_bar_b0_r5_c0 bank_0/port_address_0_0/wl_5 br0_0 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1889 gnd bitcell_Q_b0_r5_c0 bitcell_Q_bar_b0_r5_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1890 bitcell_Q_b0_r5_c0 bank_0/port_address_0_0/wl_5 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1891 bitcell_Q_b0_r15_c0 bitcell_Q_bar_b0_r15_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1892 bitcell_Q_b0_r15_c0 bitcell_Q_bar_b0_r15_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1893 vdd bitcell_Q_b0_r15_c0 bitcell_Q_bar_b0_r15_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1894 bitcell_Q_bar_b0_r15_c0 bank_0/port_address_0_0/wl_15 br0_0 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1895 gnd bitcell_Q_b0_r15_c0 bitcell_Q_bar_b0_r15_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1896 bitcell_Q_b0_r15_c0 bank_0/port_address_0_0/wl_15 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1897 bitcell_Q_b0_r4_c0 bitcell_Q_bar_b0_r4_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1898 bitcell_Q_b0_r4_c0 bitcell_Q_bar_b0_r4_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1899 vdd bitcell_Q_b0_r4_c0 bitcell_Q_bar_b0_r4_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1900 bitcell_Q_bar_b0_r4_c0 bank_0/port_address_0_0/wl_4 br0_0 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1901 gnd bitcell_Q_b0_r4_c0 bitcell_Q_bar_b0_r4_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1902 bitcell_Q_b0_r4_c0 bank_0/port_address_0_0/wl_4 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1903 bitcell_Q_b0_r14_c0 bitcell_Q_bar_b0_r14_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1904 bitcell_Q_b0_r14_c0 bitcell_Q_bar_b0_r14_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1905 vdd bitcell_Q_b0_r14_c0 bitcell_Q_bar_b0_r14_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1906 bitcell_Q_bar_b0_r14_c0 bank_0/port_address_0_0/wl_14 br0_0 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1907 gnd bitcell_Q_b0_r14_c0 bitcell_Q_bar_b0_r14_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1908 bitcell_Q_b0_r14_c0 bank_0/port_address_0_0/wl_14 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1909 bitcell_Q_b0_r3_c0 bitcell_Q_bar_b0_r3_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1910 bitcell_Q_b0_r3_c0 bitcell_Q_bar_b0_r3_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1911 vdd bitcell_Q_b0_r3_c0 bitcell_Q_bar_b0_r3_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1912 bitcell_Q_bar_b0_r3_c0 bank_0/port_address_0_0/wl_3 br0_0 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1913 gnd bitcell_Q_b0_r3_c0 bitcell_Q_bar_b0_r3_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1914 bitcell_Q_b0_r3_c0 bank_0/port_address_0_0/wl_3 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1915 bitcell_Q_b0_r13_c0 bitcell_Q_bar_b0_r13_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1916 bitcell_Q_b0_r13_c0 bitcell_Q_bar_b0_r13_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1917 vdd bitcell_Q_b0_r13_c0 bitcell_Q_bar_b0_r13_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1918 bitcell_Q_bar_b0_r13_c0 bank_0/port_address_0_0/wl_13 br0_0 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1919 gnd bitcell_Q_b0_r13_c0 bitcell_Q_bar_b0_r13_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1920 bitcell_Q_b0_r13_c0 bank_0/port_address_0_0/wl_13 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1921 bitcell_Q_b0_r2_c0 bitcell_Q_bar_b0_r2_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1922 bitcell_Q_b0_r2_c0 bitcell_Q_bar_b0_r2_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1923 vdd bitcell_Q_b0_r2_c0 bitcell_Q_bar_b0_r2_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1924 bitcell_Q_bar_b0_r2_c0 bank_0/port_address_0_0/wl_2 br0_0 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1925 gnd bitcell_Q_b0_r2_c0 bitcell_Q_bar_b0_r2_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1926 bitcell_Q_b0_r2_c0 bank_0/port_address_0_0/wl_2 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1927 bitcell_Q_b0_r12_c0 bitcell_Q_bar_b0_r12_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1928 bitcell_Q_b0_r12_c0 bitcell_Q_bar_b0_r12_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1929 vdd bitcell_Q_b0_r12_c0 bitcell_Q_bar_b0_r12_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1930 bitcell_Q_bar_b0_r12_c0 bank_0/port_address_0_0/wl_12 br0_0 gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1931 gnd bitcell_Q_b0_r12_c0 bitcell_Q_bar_b0_r12_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1932 bitcell_Q_b0_r12_c0 bank_0/port_address_0_0/wl_12 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1933 bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_0/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1934 bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_0/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1935 vdd bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_0/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1936 bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_0/a_28_56# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_0/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1937 gnd bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_0/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1938 bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_0/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1939 bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_1/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1940 bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_1/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1941 vdd bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_1/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1942 bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_1/a_28_56# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_1/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1943 gnd bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_1/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1944 bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_0_0/dummy_cell_6t_1/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1945 bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_0/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1946 bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_0/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1947 vdd bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_0/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1948 bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_0/a_28_56# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_0/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1949 gnd bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_0/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1950 bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_0/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1951 bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_1/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1952 bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_1/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1953 vdd bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_1/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1954 bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_1/a_28_56# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_1/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1955 gnd bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_1/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1956 bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_1_0/wl_0 bank_0/replica_bitcell_array_0_0/dummy_array_0_1/dummy_cell_6t_1/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1957 bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_0/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1958 bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_0/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1959 vdd bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_0/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1960 bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_0/a_28_56# wl_en0 bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_0/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1961 gnd bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_0/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_0/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1962 bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_0/a_36_64# wl_en0 bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_0/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1963 bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_1/a_28_56# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1964 bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_1/a_28_56# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1965 vdd bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_1/a_28_56# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1966 bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_1/a_28_56# wl_en0 bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_1/a_96_16# gnd n w=0.8u l=0.4u
+  ad=2.4p pd=7.2u as=0.8p ps=3.6u
M1967 gnd bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_1/a_36_64# bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_1/a_28_56# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1968 bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_1/a_36_64# wl_en0 bank_0/replica_bitcell_array_0_0/dummy_array_0_2/dummy_cell_6t_1/a_40_16# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1969 bank_0/port_address_0_0/wl_12 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_3/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1970 bank_0/port_address_0_0/wl_12 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_3/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1971 vdd bank_0/port_address_0_0/wordline_driver_0_0/in_8 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_7/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M1972 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_7/Z wl_en0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1973 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_7/Z bank_0/port_address_0_0/wordline_driver_0_0/in_8 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_7/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M1974 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_7/nmos_m1_w1_600_a_p_1/D wl_en0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1975 bank_0/port_address_0_0/wl_11 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_4/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1976 bank_0/port_address_0_0/wl_11 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_4/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1977 vdd bank_0/port_address_0_0/wordline_driver_0_0/in_7 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_8/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M1978 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_8/Z wl_en0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1979 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_8/Z bank_0/port_address_0_0/wordline_driver_0_0/in_7 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_8/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M1980 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_8/nmos_m1_w1_600_a_p_1/D wl_en0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1981 bank_0/port_address_0_0/wl_10 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_5/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1982 bank_0/port_address_0_0/wl_10 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_5/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1983 vdd bank_0/port_address_0_0/wordline_driver_0_0/in_6 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_9/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M1984 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_9/Z wl_en0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1985 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_9/Z bank_0/port_address_0_0/wordline_driver_0_0/in_6 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_9/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M1986 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_9/nmos_m1_w1_600_a_p_1/D wl_en0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1987 bank_0/port_address_0_0/wl_9 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_6/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1988 bank_0/port_address_0_0/wl_9 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_6/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1989 bank_0/port_address_0_0/wl_8 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_7/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1990 bank_0/port_address_0_0/wl_8 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_7/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1991 vdd bank_0/port_address_0_0/wordline_driver_0_0/in_5 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_10/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M1992 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_10/Z wl_en0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1993 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_10/Z bank_0/port_address_0_0/wordline_driver_0_0/in_5 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_10/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M1994 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_10/nmos_m1_w1_600_a_p_1/D wl_en0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1995 bank_0/port_address_0_0/wl_7 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_8/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M1996 bank_0/port_address_0_0/wl_7 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_8/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M1997 vdd bank_0/port_address_0_0/wordline_driver_0_0/in_4 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_11/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M1998 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_11/Z wl_en0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1999 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_11/Z bank_0/port_address_0_0/wordline_driver_0_0/in_4 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_11/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M2000 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_11/nmos_m1_w1_600_a_p_1/D wl_en0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2001 bank_0/port_address_0_0/wl_6 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_9/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2002 bank_0/port_address_0_0/wl_6 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_9/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2003 vdd bank_0/port_address_0_0/wordline_driver_0_0/in_3 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_12/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2004 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_12/Z wl_en0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2005 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_12/Z bank_0/port_address_0_0/wordline_driver_0_0/in_3 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_12/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M2006 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_12/nmos_m1_w1_600_a_p_1/D wl_en0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2007 vdd bank_0/port_address_0_0/wordline_driver_0_0/in_2 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_13/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2008 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_13/Z wl_en0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2009 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_13/Z bank_0/port_address_0_0/wordline_driver_0_0/in_2 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_13/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M2010 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_13/nmos_m1_w1_600_a_p_1/D wl_en0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2011 bank_0/port_address_0_0/wl_5 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_10/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2012 bank_0/port_address_0_0/wl_5 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_10/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2013 vdd bank_0/port_address_0_0/wordline_driver_0_0/in_1 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_14/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2014 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_14/Z wl_en0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2015 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_14/Z bank_0/port_address_0_0/wordline_driver_0_0/in_1 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_14/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M2016 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_14/nmos_m1_w1_600_a_p_1/D wl_en0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2017 bank_0/port_address_0_0/wl_4 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_11/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2018 bank_0/port_address_0_0/wl_4 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_11/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2019 vdd bank_0/port_address_0_0/wordline_driver_0_0/in_0 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_15/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2020 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_15/Z wl_en0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2021 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_15/Z bank_0/port_address_0_0/wordline_driver_0_0/in_0 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_15/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M2022 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_15/nmos_m1_w1_600_a_p_1/D wl_en0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2023 bank_0/port_address_0_0/wl_3 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_12/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2024 bank_0/port_address_0_0/wl_3 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_12/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2025 bank_0/port_address_0_0/wl_2 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_13/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2026 bank_0/port_address_0_0/wl_2 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_13/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2027 bank_0/port_address_0_0/wl_1 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_14/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2028 bank_0/port_address_0_0/wl_1 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_14/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2029 bank_0/port_address_0_0/wl_0 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_15/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2030 bank_0/port_address_0_0/wl_0 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_15/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2031 vdd bank_0/port_address_0_0/wordline_driver_0_0/in_15 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_0/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2032 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_0/Z wl_en0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2033 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_0/Z bank_0/port_address_0_0/wordline_driver_0_0/in_15 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_0/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M2034 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_0/nmos_m1_w1_600_a_p_1/D wl_en0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2035 vdd bank_0/port_address_0_0/wordline_driver_0_0/in_14 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_1/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2036 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_1/Z wl_en0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2037 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_1/Z bank_0/port_address_0_0/wordline_driver_0_0/in_14 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_1/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M2038 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_1/nmos_m1_w1_600_a_p_1/D wl_en0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2039 vdd bank_0/port_address_0_0/wordline_driver_0_0/in_13 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_2/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2040 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_2/Z wl_en0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2041 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_2/Z bank_0/port_address_0_0/wordline_driver_0_0/in_13 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_2/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M2042 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_2/nmos_m1_w1_600_a_p_1/D wl_en0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2043 vdd bank_0/port_address_0_0/wordline_driver_0_0/in_12 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_3/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2044 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_3/Z wl_en0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2045 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_3/Z bank_0/port_address_0_0/wordline_driver_0_0/in_12 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_3/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M2046 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_3/nmos_m1_w1_600_a_p_1/D wl_en0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2047 bank_0/port_address_0_0/wl_15 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_0/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2048 bank_0/port_address_0_0/wl_15 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_0/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2049 vdd bank_0/port_address_0_0/wordline_driver_0_0/in_11 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_4/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2050 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_4/Z wl_en0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2051 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_4/Z bank_0/port_address_0_0/wordline_driver_0_0/in_11 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_4/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M2052 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_4/nmos_m1_w1_600_a_p_1/D wl_en0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2053 bank_0/port_address_0_0/wl_14 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_1/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2054 bank_0/port_address_0_0/wl_14 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_1/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2055 vdd bank_0/port_address_0_0/wordline_driver_0_0/in_10 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_5/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2056 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_5/Z wl_en0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2057 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_5/Z bank_0/port_address_0_0/wordline_driver_0_0/in_10 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_5/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M2058 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_5/nmos_m1_w1_600_a_p_1/D wl_en0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2059 bank_0/port_address_0_0/wl_13 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_2/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2060 bank_0/port_address_0_0/wl_13 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_2/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2061 vdd bank_0/port_address_0_0/wordline_driver_0_0/in_9 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_6/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2062 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_6/Z wl_en0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2063 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_6/Z bank_0/port_address_0_0/wordline_driver_0_0/in_9 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_6/nmos_m1_w1_600_a_p_1/D gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=1.9275p ps=5.75u
M2064 bank_0/port_address_0_0/wordline_driver_0_0/pnand2_6/nmos_m1_w1_600_a_p_1/D wl_en0 gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2065 bank_0/port_address_0_0/wordline_driver_0_0/in_12 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_3/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2066 bank_0/port_address_0_0/wordline_driver_0_0/in_12 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_3/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2067 bank_0/port_address_0_0/wordline_driver_0_0/in_11 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_4/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2068 bank_0/port_address_0_0/wordline_driver_0_0/in_11 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_4/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2069 bank_0/port_address_0_0/wordline_driver_0_0/in_10 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_5/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2070 bank_0/port_address_0_0/wordline_driver_0_0/in_10 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_5/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2071 bank_0/port_address_0_0/wordline_driver_0_0/in_9 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_6/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2072 bank_0/port_address_0_0/wordline_driver_0_0/in_9 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_6/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2073 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_5 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_10/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2074 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_10/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_1 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2075 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_10/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_1 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2076 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_10/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_5 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_10/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2077 bank_0/port_address_0_0/wordline_driver_0_0/in_8 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_7/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2078 bank_0/port_address_0_0/wordline_driver_0_0/in_8 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_7/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2079 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_5 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_11/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2080 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_11/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2081 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_11/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_0 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2082 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_11/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_5 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_11/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2083 bank_0/port_address_0_0/wordline_driver_0_0/in_7 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_8/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2084 bank_0/port_address_0_0/wordline_driver_0_0/in_7 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_8/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2085 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_4 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_12/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2086 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_12/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_3 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2087 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_12/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_3 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2088 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_12/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_4 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_12/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2089 bank_0/port_address_0_0/wordline_driver_0_0/in_5 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_10/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2090 bank_0/port_address_0_0/wordline_driver_0_0/in_5 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_10/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2091 bank_0/port_address_0_0/wordline_driver_0_0/in_6 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_9/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2092 bank_0/port_address_0_0/wordline_driver_0_0/in_6 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_9/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2093 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_4 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_13/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2094 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_13/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_2 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2095 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_13/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_2 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2096 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_13/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_4 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_13/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2097 bank_0/port_address_0_0/wordline_driver_0_0/in_4 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_11/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2098 bank_0/port_address_0_0/wordline_driver_0_0/in_4 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_11/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2099 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_4 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_14/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2100 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_14/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_1 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2101 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_14/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_1 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2102 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_14/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_4 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_14/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2103 bank_0/port_address_0_0/wordline_driver_0_0/in_3 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_12/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2104 bank_0/port_address_0_0/wordline_driver_0_0/in_3 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_12/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2105 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_4 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_15/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2106 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_15/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2107 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_15/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_0 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2108 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_15/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_4 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_15/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2109 bank_0/port_address_0_0/wordline_driver_0_0/in_2 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_13/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2110 bank_0/port_address_0_0/wordline_driver_0_0/in_2 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_13/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2111 bank_0/port_address_0_0/wordline_driver_0_0/in_1 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_14/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2112 bank_0/port_address_0_0/wordline_driver_0_0/in_1 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_14/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2113 bank_0/port_address_0_0/wordline_driver_0_0/in_0 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_15/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2114 bank_0/port_address_0_0/wordline_driver_0_0/in_0 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_15/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2115 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_7 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2116 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_0/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_3 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2117 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_0/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_3 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2118 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_0/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_7 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_0/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2119 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_7 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_1/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2120 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_1/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_2 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2121 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_1/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_2 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2122 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_1/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_7 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_1/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2123 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_7 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_2/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2124 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_2/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_1 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2125 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_2/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_1 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2126 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_2/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_7 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_2/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2127 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_7 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_3/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2128 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_3/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2129 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_3/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_0 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2130 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_3/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_7 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_3/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2131 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_6 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_4/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2132 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_4/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_3 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2133 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_4/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_3 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2134 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_4/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_6 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_4/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2135 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_6 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_5/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2136 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_5/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_2 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2137 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_5/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_2 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2138 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_5/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_6 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_5/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2139 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_4 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_3/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2140 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_4 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_3/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2141 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_4/Z bank_0/addr0_3 vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2142 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_4/Z bank_0/addr0_3 gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2143 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_5/Z bank_0/addr0_2 vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2144 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_5/Z bank_0/addr0_2 gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2145 vdd bank_0/addr0_3 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2146 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_0/A bank_0/addr0_2 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2147 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pnand2_0_0/nmos_m1_w1_600_a_p_0/S bank_0/addr0_2 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2148 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_0/A bank_0/addr0_3 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pnand2_0_0/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2149 vdd bank_0/addr0_3 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_1/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2150 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_1/A bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_5/Z vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2151 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pnand2_0_1/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_5/Z gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2152 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_1/A bank_0/addr0_3 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pnand2_0_1/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2153 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_4/Z bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_2/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2154 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_2/A bank_0/addr0_2 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2155 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pnand2_0_2/nmos_m1_w1_600_a_p_0/S bank_0/addr0_2 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2156 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_2/A bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_4/Z bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pnand2_0_2/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2157 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_4/Z bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_3/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2158 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_3/A bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_5/Z vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2159 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pnand2_0_3/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_5/Z gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2160 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_3/A bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_4/Z bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pnand2_0_3/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2161 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_7 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2162 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_7 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2163 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_6 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_1/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2164 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_6 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_1/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2165 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_5 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_2/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2166 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_5 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_2/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2167 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_6 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_6/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2168 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_6/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_1 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2169 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_6/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_1 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2170 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_6/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_6 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_6/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2171 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_0 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_3/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2172 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_0 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_3/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2173 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_4/Z bank_0/addr0_1 vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2174 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_4/Z bank_0/addr0_1 gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2175 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_5/Z bank_0/addr0_0 vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2176 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_5/Z bank_0/addr0_0 gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2177 vdd bank_0/addr0_1 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2178 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_0/A bank_0/addr0_0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2179 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pnand2_0_0/nmos_m1_w1_600_a_p_0/S bank_0/addr0_0 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2180 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_0/A bank_0/addr0_1 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pnand2_0_0/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2181 vdd bank_0/addr0_1 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_1/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2182 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_1/A bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_5/Z vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2183 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pnand2_0_1/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_5/Z gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2184 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_1/A bank_0/addr0_1 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pnand2_0_1/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2185 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_4/Z bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_2/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2186 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_2/A bank_0/addr0_0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2187 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pnand2_0_2/nmos_m1_w1_600_a_p_0/S bank_0/addr0_0 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2188 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_2/A bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_4/Z bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pnand2_0_2/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2189 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_4/Z bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_3/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2190 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_3/A bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_5/Z vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2191 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pnand2_0_3/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_5/Z gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2192 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_3/A bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_4/Z bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pnand2_0_3/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2193 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_3 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2194 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_3 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2195 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_2 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_1/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2196 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_2 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_1/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2197 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_1 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_2/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2198 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_1 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_2/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2199 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_6 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_7/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2200 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_7/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2201 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_7/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_0 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2202 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_7/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_6 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_7/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2203 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_5 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_8/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2204 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_8/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_3 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2205 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_8/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_3 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2206 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_8/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_5 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_8/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2207 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_5 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_9/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=1.9275p ps=5.75u
M2208 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_9/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_2 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M2209 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_9/nmos_m1_w1_600_a_p_0/S bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_2 gnd gnd n w=1.6u l=0.4u
+  ad=1.9275p pd=5.75u as=0p ps=0u
M2210 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_9/A bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_5 bank_0/port_address_0_0/hierarchical_decoder_0_0/pnand2_0_9/nmos_m1_w1_600_a_p_0/S gnd n w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2211 bank_0/port_address_0_0/wordline_driver_0_0/in_15 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2212 bank_0/port_address_0_0/wordline_driver_0_0/in_15 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2213 bank_0/port_address_0_0/wordline_driver_0_0/in_14 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_1/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2214 bank_0/port_address_0_0/wordline_driver_0_0/in_14 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_1/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
M2215 bank_0/port_address_0_0/wordline_driver_0_0/in_13 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_2/A vdd vdd p w=1.6u l=0.4u
+  ad=1.6025p pd=5.25u as=0p ps=0u
M2216 bank_0/port_address_0_0/wordline_driver_0_0/in_13 bank_0/port_address_0_0/hierarchical_decoder_0_0/pinv_0_2/A gnd gnd n w=0.8u l=0.4u
+  ad=0.8025p pd=3.65u as=0p ps=0u
C0 control_logic_rw_0/pand2_0_0/B control_logic_rw_0/pand3_1_0/C 9.62fF
C1 control_logic_rw_0/pinv_5_0/Z vdd 5.68fF
C2 control_logic_rw_0/pand3_1_0/B vdd 9.01fF
C3 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_4 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_5 10.09fF
C4 bank_0/addr0_0 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_4/Z 2.97fF
C5 data_dff_0/dff_0/a_24_24# vdd 2.75fF
C6 vdd bank_0/port_data_0_0/rbl_br 13.34fF
C7 control_logic_rw_0/pand3_0_0/pinv_8_0/A vdd 3.19fF
C8 vdd dout0[1] 2.06fF
C9 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_7 6.95fF
C10 vdd bank_0/addr0_0 8.65fF
C11 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_5 4.99fF
C12 vdd row_addr_dff_0/dff_1/a_24_24# 2.85fF
C13 s_en0 p_en_bar0 6.97fF
C14 vdd control_logic_rw_0/delay_chain_0_0/pinv_2_14/A 4.57fF
C15 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_2 5.20fF
C16 vdd bank_0/addr0_1 10.26fF
C17 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_5/Z 2.62fF
C18 data_dff_0/dff_0/a_152_16# vdd 2.21fF
C19 data_dff_0/dff_1/a_24_24# vdd 3.02fF
C20 vdd bank_0/addr0_3 8.31fF
C21 vdd br0_1 9.35fF
C22 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/br_0 3.43fF
C23 control_logic_rw_0/pdriver_2_0/pinv_3_0/A vdd 2.70fF
C24 vdd row_addr_dff_0/dff_1/a_152_16# 2.28fF
C25 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_4 5.14fF
C26 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_4/Z 2.61fF
C27 control_logic_rw_0/pdriver_2_0/pinv_7_0/A vdd 2.11fF
C28 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_7 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_6 10.09fF
C29 control_logic_rw_0/pand2_0_0/B vdd 8.18fF
C30 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_0 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_1 10.12fF
C31 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_6 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_5 10.09fF
C32 vdd row_addr_dff_0/dff_0/a_24_24# 2.76fF
C33 control_logic_rw_0/pinv_5_0/Z control_logic_rw_0/pinv_5_0/A 9.85fF
C34 bank_0/din0_1 vdd 3.56fF
C35 control_logic_rw_0/pand3_1_0/B control_logic_rw_0/pinv_5_0/A 10.79fF
C36 data_dff_0/dff_1/a_152_16# vdd 2.22fF
C37 vdd control_logic_rw_0/delay_chain_0_0/pinv_2_30/A 4.79fF
C38 vdd row_addr_dff_0/dff_3/a_24_24# 2.72fF
C39 bank_0/addr0_2 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_4/Z 2.97fF
C40 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_5/Z bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_4/Z 3.04fF
C41 vdd bl0_0 6.40fF
C42 vdd wl_en0 19.04fF
C43 vdd row_addr_dff_0/dff_2/a_24_24# 2.71fF
C44 vdd row_addr_dff_0/dff_0/a_152_16# 2.31fF
C45 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_5/Z 2.78fF
C46 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_24_24# vdd 2.90fF
C47 control_logic_rw_0/pinv_5_1/Z vdd 2.87fF
C48 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_6 7.36fF
C49 control_logic_rw_0/pand2_0_0/Z control_logic_rw_0/pand3_0_0/A 9.67fF
C50 control_logic_rw_0/pnand2_1_0/Z vdd 2.86fF
C51 control_logic_rw_0/pand2_0_1/pnand2_1_0/Z vdd 3.11fF
C52 vdd control_logic_rw_0/delay_chain_0_0/pinv_2_20/A 5.89fF
C53 vdd br0_0 7.06fF
C54 vdd row_addr_dff_0/dff_2/a_152_16# 2.38fF
C55 control_logic_rw_0/pand2_0_1/pdriver_1_0/pinv_5_0/A vdd 2.56fF
C56 control_logic_rw_0/pand3_0_0/A clk_buf0 9.63fF
C57 w_en0 vdd 9.23fF
C58 control_logic_rw_0/pdriver_4_0/pinv_5_0/A vdd 2.86fF
C59 s_en0 vdd 8.60fF
C60 vdd row_addr_dff_0/dff_3/a_152_16# 2.32fF
C61 control_logic_rw_0/pdriver_3_0/pinv_5_0/A vdd 2.83fF
C62 control_logic_rw_0/pand2_0_0/pnand2_1_0/Z vdd 2.95fF
C63 vdd control_logic_rw_0/pinv_5_0/A 18.27fF
C64 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_3 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_2 10.12fF
C65 vdd control_logic_rw_0/delay_chain_0_0/pinv_2_9/A 4.87fF
C66 control_logic_rw_0/pand3_1_0/C clk_buf0 9.72fF
C67 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_24_24# vdd 2.90fF
C68 bl0_0 br0_0 2.36fF
C69 control_logic_rw_0/pand2_0_0/Z control_logic_rw_0/pand3_1_0/B 9.72fF
C70 control_logic_rw_0/pand2_0_0/pdriver_1_0/pinv_5_0/A vdd 2.82fF
C71 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_0 7.66fF
C72 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/bl_0 6.54fF
C73 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_0/bl_0 4.78fF
C74 bank_0/din0_0 vdd 3.52fF
C75 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/Q vdd 3.32fF
C76 bank_0/addr0_2 bank_0/addr0_1 7.64fF
C77 bank_0/addr0_3 bank_0/addr0_2 14.29fF
C78 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_4 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_3 10.65fF
C79 control_logic_rw_0/delay_chain_0_0/pinv_2_24/A vdd 4.60fF
C80 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_152_16# vdd 2.25fF
C81 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_4/Z bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_5/Z 3.04fF
C82 vdd bank_0/replica_bitcell_array_0_0/dummy_array_1_1/br_0 3.98fF
C83 clk_buf0 bank_0/addr0_0 4.33fF
C84 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_3 7.86fF
C85 control_logic_rw_0/pdriver_3_0/pinv_3_0/A vdd 2.38fF
C86 vdd control_logic_rw_0/delay_chain_0_0/pinv_2_40/A 4.83fF
C87 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_2 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_1 10.12fF
C88 vdd bank_0/addr0_2 10.43fF
C89 w_en0 s_en0 6.97fF
C90 vdd p_en_bar0 8.18fF
C91 vdd control_logic_rw_0/delay_chain_0_0/pinv_2_4/A 4.59fF
C92 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_152_16# vdd 2.25fF
C93 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_4/Z 2.66fF
C94 vdd rbl_bl0 11.46fF
C95 control_logic_rw_0/pand2_0_0/Z vdd 5.38fF
C96 bl0_1 br0_1 2.36fF
C97 control_logic_rw_0/pand3_0_0/A vdd 8.23fF
C98 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/Q vdd 3.32fF
C99 control_logic_rw_0/delay_chain_0_0/pinv_2_34/A vdd 4.59fF
C100 control_logic_rw_0/pand3_1_0/pinv_3_0/A vdd 3.42fF
C101 clk_buf0 vdd 51.88fF
C102 vdd bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_1 5.11fF
C103 bank_0/addr0_1 bank_0/addr0_0 11.94fF
C104 p_en_bar0 wl_en0 6.96fF
C105 control_logic_rw_0/pand3_1_0/C vdd 4.89fF
C106 vdd bl0_1 7.88fF
C107 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_1 gnd 7.22fF
C108 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_2 gnd 7.07fF
C109 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_3 gnd 4.50fF
C110 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_1/pinv_0_5/Z gnd 3.32fF
C111 bank_0/addr0_0 gnd 8.67fF
C112 bank_0/addr0_1 gnd 6.36fF
C113 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_5 gnd 8.17fF
C114 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_6 gnd 4.36fF
C115 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_7 gnd 5.03fF
C116 bank_0/port_address_0_0/hierarchical_decoder_0_0/hierarchical_predecode2x4_0_0/pinv_0_5/Z gnd 3.43fF
C117 bank_0/addr0_2 gnd 7.15fF
C118 bank_0/addr0_3 gnd 10.28fF
C119 bank_0/port_address_0_0/hierarchical_decoder_0_0/predecode_4 gnd 6.41fF
C120 bank_0/port_address_0_0/wl_13 gnd 5.20fF
C121 bank_0/port_address_0_0/wl_15 gnd 4.57fF
C122 wl_en0 gnd 23.16fF
C123 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/wl_0 gnd 5.00fF
C124 bank_0/replica_bitcell_array_0_0/dummy_array_0_0/wl_0 gnd 5.00fF
C125 br0_1 gnd 19.14fF
C126 bl0_1 gnd 20.42fF
C127 br0_0 gnd 19.38fF
C128 bl0_0 gnd 13.80fF
C129 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/br_0 gnd 18.13fF ; **FLOATING
C130 bank_0/replica_bitcell_array_0_0/dummy_array_1_1/bl_0 gnd 19.08fF ; **FLOATING
C131 bank_0/port_address_0_0/wl_0 gnd 6.06fF
C132 bank_0/port_address_0_0/wl_2 gnd 6.02fF
C133 bank_0/port_address_0_0/wl_4 gnd 5.72fF
C134 bank_0/port_address_0_0/wl_6 gnd 6.06fF
C135 bank_0/port_address_0_0/wl_8 gnd 6.05fF
C136 bank_0/port_address_0_0/wl_9 gnd 2.83fF
C137 bank_0/port_address_0_0/wl_10 gnd 5.72fF
C138 bank_0/port_address_0_0/wl_11 gnd 4.35fF
C139 bank_0/port_address_0_0/wl_12 gnd 6.06fF
C140 bank_0/port_address_0_0/wl_14 gnd 6.02fF
C141 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/br_0 gnd 19.31fF ; **FLOATING
C142 bank_0/replica_bitcell_array_0_0/dummy_array_1_0/bl_0 gnd 20.82fF ; **FLOATING
C143 bank_0/port_data_0_0/rbl_br gnd 20.49fF
C144 rbl_bl0 gnd 21.08fF
C145 p_en_bar0 gnd 6.45fF
C146 row_addr_dff_0/dff_3/a_24_24# gnd 2.49fF
C147 row_addr_dff_0/dff_2/a_24_24# gnd 2.61fF
C148 row_addr_dff_0/dff_1/a_24_24# gnd 2.42fF
C149 row_addr_dff_0/dff_0/a_24_24# gnd 2.51fF
C150 control_logic_rw_0/pinv_5_0/A gnd 5.59fF
C151 vdd gnd 8001.06fF
C152 clk_buf0 gnd 41.42fF
C153 control_logic_rw_0/pand3_1_0/C gnd 6.50fF
C154 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_0/dff_0/a_24_24# gnd 2.25fF
C155 control_logic_rw_0/pand2_0_0/B gnd 4.32fF
C156 control_logic_rw_0/dff_buf_array_0_0/dff_buf_0_1/dff_0/a_24_24# gnd 2.25fF
C157 s_en0 gnd 10.69fF
C158 control_logic_rw_0/pand3_1_0/B gnd 7.31fF
C159 control_logic_rw_0/pand2_0_0/Z gnd 7.46fF
C160 w_en0 gnd 7.60fF
C161 control_logic_rw_0/pinv_5_0/Z gnd 4.15fF
C162 data_dff_0/dff_1/a_24_24# gnd 2.39fF
C163 data_dff_0/dff_0/a_24_24# gnd 2.59fF
.ends
