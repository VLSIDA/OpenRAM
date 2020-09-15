* NGSPICE file created from sram_2_16_scn4m_subm.ext - technology: scmos

.SUBCKT sram_2_16_scn4m_subm din0[0] din0[1] addr0[0] addr0[1] addr0[2] addr0[3] csb0 web0 clk0 dout0[0] dout0[1] vdd gnd
+ bitcell_Q_b0_r15_c1 bitcell_Q_bar_b0_r15_c1 bl0_0 br0_0 bl0_1 br0_1 
+ bank_0/s_en0
M1000 data_dff_0/dff_0/a_304_32# data_dff_0/dff_0/a_208_48# gnd gnd n w=2u l=0.4u
+  ad=2p pd=6u as=739.779p ps=1942.38u
M1001 data_dff_0/dff_0/a_640_48# data_dff_0/dff_0/a_48_48# data_dff_0/dff_0/a_560_48# gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=3.2p ps=7.2u
M1002 gnd bank_0/din0_1 data_dff_0/dff_0/a_640_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1003 data_dff_0/dff_0/a_280_48# data_dff_0/clk data_dff_0/dff_0/a_208_48# gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=2.8p ps=6.8u
M1004 vdd data_dff_0/clk data_dff_0/dff_0/a_48_48# vdd p w=8u l=0.4u
+  ad=942.654p pd=2713.82u as=8p ps=18u
M1005 gnd data_dff_0/clk data_dff_0/dff_0/a_48_48# gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4p ps=10u
M1006 data_dff_0/dff_0/a_168_48# din0[1] gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1007 data_dff_0/dff_0/a_208_48# data_dff_0/dff_0/a_48_48# data_dff_0/dff_0/a_168_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1008 gnd data_dff_0/dff_0/a_304_32# data_dff_0/dff_0/a_280_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1009 bank_0/din0_1 data_dff_0/dff_0/a_560_48# gnd gnd n w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1010 vdd bank_0/din0_1 data_dff_0/dff_0/a_640_672# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1011 vdd data_dff_0/dff_0/a_304_32# data_dff_0/dff_0/a_280_592# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=3.2p ps=9.6u
M1012 data_dff_0/dff_0/a_208_48# data_dff_0/clk data_dff_0/dff_0/a_168_592# vdd p w=4u l=0.4u
+  ad=4.8p pd=10.4u as=3.2p ps=9.6u
M1013 data_dff_0/dff_0/a_640_672# data_dff_0/clk data_dff_0/dff_0/a_560_48# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=6p ps=11.2u
M1014 bank_0/din0_1 data_dff_0/dff_0/a_560_48# vdd vdd p w=8u l=0.4u
+  ad=8p pd=18u as=0p ps=0u
M1015 data_dff_0/dff_0/a_560_48# data_dff_0/dff_0/a_48_48# data_dff_0/dff_0/a_520_592# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=2.4p ps=9.2u
M1016 data_dff_0/dff_0/a_304_32# data_dff_0/dff_0/a_208_48# vdd vdd p w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1017 data_dff_0/dff_0/a_520_48# data_dff_0/dff_0/a_304_32# gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1018 data_dff_0/dff_0/a_560_48# data_dff_0/clk data_dff_0/dff_0/a_520_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1019 data_dff_0/dff_0/a_280_592# data_dff_0/dff_0/a_48_48# data_dff_0/dff_0/a_208_48# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1020 data_dff_0/dff_0/a_168_592# din0[1] vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1021 data_dff_0/dff_0/a_520_592# data_dff_0/dff_0/a_304_32# vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1022 data_dff_0/dff_1/a_304_32# data_dff_0/dff_1/a_208_48# gnd gnd n w=2u l=0.4u
+  ad=2p pd=6u as=0p ps=0u
M1023 data_dff_0/dff_1/a_640_48# data_dff_0/dff_1/a_48_48# data_dff_0/dff_1/a_560_48# gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=3.2p ps=7.2u
M1024 gnd bank_0/din0_0 data_dff_0/dff_1/a_640_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1025 data_dff_0/dff_1/a_280_48# data_dff_0/clk data_dff_0/dff_1/a_208_48# gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=2.8p ps=6.8u
M1026 vdd data_dff_0/clk data_dff_0/dff_1/a_48_48# vdd p w=8u l=0.4u
+  ad=0p pd=0u as=8p ps=18u
M1027 gnd data_dff_0/clk data_dff_0/dff_1/a_48_48# gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4p ps=10u
M1028 data_dff_0/dff_1/a_168_48# din0[0] gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1029 data_dff_0/dff_1/a_208_48# data_dff_0/dff_1/a_48_48# data_dff_0/dff_1/a_168_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1030 gnd data_dff_0/dff_1/a_304_32# data_dff_0/dff_1/a_280_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1031 bank_0/din0_0 data_dff_0/dff_1/a_560_48# gnd gnd n w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1032 vdd bank_0/din0_0 data_dff_0/dff_1/a_640_672# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1033 vdd data_dff_0/dff_1/a_304_32# data_dff_0/dff_1/a_280_592# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=3.2p ps=9.6u
M1034 data_dff_0/dff_1/a_208_48# data_dff_0/clk data_dff_0/dff_1/a_168_592# vdd p w=4u l=0.4u
+  ad=4.8p pd=10.4u as=3.2p ps=9.6u
M1035 data_dff_0/dff_1/a_640_672# data_dff_0/clk data_dff_0/dff_1/a_560_48# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=6p ps=11.2u
M1036 bank_0/din0_0 data_dff_0/dff_1/a_560_48# vdd vdd p w=8u l=0.4u
+  ad=8p pd=18u as=0p ps=0u
M1037 data_dff_0/dff_1/a_560_48# data_dff_0/dff_1/a_48_48# data_dff_0/dff_1/a_520_592# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=2.4p ps=9.2u
M1038 data_dff_0/dff_1/a_304_32# data_dff_0/dff_1/a_208_48# vdd vdd p w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1039 data_dff_0/dff_1/a_520_48# data_dff_0/dff_1/a_304_32# gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1040 data_dff_0/dff_1/a_560_48# data_dff_0/clk data_dff_0/dff_1/a_520_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1041 data_dff_0/dff_1/a_280_592# data_dff_0/dff_1/a_48_48# data_dff_0/dff_1/a_208_48# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1042 data_dff_0/dff_1/a_168_592# din0[0] vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1043 data_dff_0/dff_1/a_520_592# data_dff_0/dff_1/a_304_32# vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1044 control_logic_rw_0/pand3_0_0/pnand3_0_0/nmos_m1_w1_600_sactive_dm1_0/S control_logic_rw_0/pand2_1/Z control_logic_rw_0/pand3_0_0/pnand3_0_0/nmos_m1_w1_600_sm1_dactive_0/D gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=2.56063p ps=6.425u
M1045 control_logic_rw_0/pand3_0_0/pnand3_0_0/nmos_m1_w1_600_sm1_dactive_0/D control_logic_rw_0/pinv_4_0/A gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1046 control_logic_rw_0/pand3_0_0/pnand3_0_0/Z control_logic_rw_0/pand3_0_0/C control_logic_rw_0/pand3_0_0/pnand3_0_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1047 vdd control_logic_rw_0/pand2_1/Z control_logic_rw_0/pand3_0_0/pnand3_0_0/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=5.76188p ps=12.1u
M1048 control_logic_rw_0/pand3_0_0/pnand3_0_0/Z control_logic_rw_0/pand3_0_0/C vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1049 control_logic_rw_0/pand3_0_0/pnand3_0_0/Z control_logic_rw_0/pinv_4_0/A vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1050 bank_0/s_en0 control_logic_rw_0/pand3_0_0/pnand3_0_0/Z vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1051 bank_0/s_en0 control_logic_rw_0/pand3_0_0/pnand3_0_0/Z gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1052 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_304_32# control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_208_48# gnd gnd n w=2u l=0.4u
+  ad=2p pd=6u as=0p ps=0u
M1053 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_640_48# control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_48_48# control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_560_48# gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=3.2p ps=7.2u
M1054 gnd control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/Q control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_640_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1055 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_280_48# data_dff_0/clk control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_208_48# gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=2.8p ps=6.8u
M1056 vdd data_dff_0/clk control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_48_48# vdd p w=8u l=0.4u
+  ad=0p pd=0u as=8p ps=18u
M1057 gnd data_dff_0/clk control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_48_48# gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4p ps=10u
M1058 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_168_48# csb0 gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1059 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_208_48# control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_48_48# control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_168_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1060 gnd control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_304_32# control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_280_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1061 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/Q control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_560_48# gnd gnd n w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1062 vdd control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/Q control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_640_672# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1063 vdd control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_304_32# control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_280_592# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=3.2p ps=9.6u
M1064 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_208_48# data_dff_0/clk control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_168_592# vdd p w=4u l=0.4u
+  ad=4.8p pd=10.4u as=3.2p ps=9.6u
M1065 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_640_672# data_dff_0/clk control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_560_48# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=6p ps=11.2u
M1066 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/Q control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_560_48# vdd vdd p w=8u l=0.4u
+  ad=8p pd=18u as=0p ps=0u
M1067 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_560_48# control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_48_48# control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_520_592# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=2.4p ps=9.2u
M1068 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_304_32# control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_208_48# vdd vdd p w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1069 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_520_48# control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_304_32# gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1070 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_560_48# data_dff_0/clk control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_520_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1071 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_280_592# control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_48_48# control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_208_48# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1072 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_168_592# csb0 vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1073 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_520_592# control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_304_32# vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1074 control_logic_rw_0/pand2_0/B control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/Q vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1075 control_logic_rw_0/pand2_0/B control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/Q gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1076 control_logic_rw_0/dff_buf_array_0/dout_0 control_logic_rw_0/pand2_0/B gnd gnd n w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1077 control_logic_rw_0/dff_buf_array_0/dout_0 control_logic_rw_0/pand2_0/B vdd vdd p w=6.4u l=0.4u
+  ad=7.68063p pd=15.225u as=0p ps=0u
M1078 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_304_32# control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_208_48# gnd gnd n w=2u l=0.4u
+  ad=2p pd=6u as=0p ps=0u
M1079 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_640_48# control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_48_48# control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_560_48# gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=3.2p ps=7.2u
M1080 gnd control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/Q control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_640_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1081 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_280_48# data_dff_0/clk control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_208_48# gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=2.8p ps=6.8u
M1082 vdd data_dff_0/clk control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_48_48# vdd p w=8u l=0.4u
+  ad=0p pd=0u as=8p ps=18u
M1083 gnd data_dff_0/clk control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_48_48# gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4p ps=10u
M1084 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_168_48# web0 gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1085 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_208_48# control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_48_48# control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_168_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1086 gnd control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_304_32# control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_280_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1087 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/Q control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_560_48# gnd gnd n w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1088 vdd control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/Q control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_640_672# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1089 vdd control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_304_32# control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_280_592# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=3.2p ps=9.6u
M1090 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_208_48# data_dff_0/clk control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_168_592# vdd p w=4u l=0.4u
+  ad=4.8p pd=10.4u as=3.2p ps=9.6u
M1091 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_640_672# data_dff_0/clk control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_560_48# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=6p ps=11.2u
M1092 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/Q control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_560_48# vdd vdd p w=8u l=0.4u
+  ad=8p pd=18u as=0p ps=0u
M1093 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_560_48# control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_48_48# control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_520_592# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=2.4p ps=9.2u
M1094 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_304_32# control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_208_48# vdd vdd p w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1095 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_520_48# control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_304_32# gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1096 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_560_48# data_dff_0/clk control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_520_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1097 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_280_592# control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_48_48# control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_208_48# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1098 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_168_592# web0 vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1099 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_520_592# control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_304_32# vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1100 control_logic_rw_0/pand3_0/A control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/Q vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1101 control_logic_rw_0/pand3_0/A control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/Q gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1102 control_logic_rw_0/pand3_0_0/C control_logic_rw_0/pand3_0/A gnd gnd n w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1103 control_logic_rw_0/pand3_0_0/C control_logic_rw_0/pand3_0/A vdd vdd p w=6.4u l=0.4u
+  ad=7.68063p pd=15.225u as=0p ps=0u
M1104 control_logic_rw_0/pand3_0/pnand3_0_0/nmos_m1_w1_600_sactive_dm1_0/S control_logic_rw_0/pand3_0/B control_logic_rw_0/pand3_0/pnand3_0_0/nmos_m1_w1_600_sm1_dactive_0/D gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=2.56063p ps=6.425u
M1105 control_logic_rw_0/pand3_0/pnand3_0_0/nmos_m1_w1_600_sm1_dactive_0/D control_logic_rw_0/pand3_0/A gnd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1106 control_logic_rw_0/pand3_0/pnand3_0_0/Z control_logic_rw_0/pand2_1/Z control_logic_rw_0/pand3_0/pnand3_0_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1107 vdd control_logic_rw_0/pand3_0/B control_logic_rw_0/pand3_0/pnand3_0_0/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=5.76188p ps=12.1u
M1108 control_logic_rw_0/pand3_0/pnand3_0_0/Z control_logic_rw_0/pand2_1/Z vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1109 control_logic_rw_0/pand3_0/pnand3_0_0/Z control_logic_rw_0/pand3_0/A vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1110 bank_0/w_en0 control_logic_rw_0/pand3_0/pnand3_0_0/Z vdd vdd p w=8u l=0.4u
+  ad=9.60063p pd=18.425u as=0p ps=0u
M1111 vdd control_logic_rw_0/pand3_0/pnand3_0_0/Z bank_0/w_en0 vdd p w=8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1112 bank_0/w_en0 control_logic_rw_0/pand3_0/pnand3_0_0/Z gnd gnd n w=4u l=0.4u
+  ad=4.80063p pd=10.425u as=0p ps=0u
M1113 gnd control_logic_rw_0/pand3_0/pnand3_0_0/Z bank_0/w_en0 gnd n w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1114 control_logic_rw_0/pdriver_1_0/pinv_5_0/A control_logic_rw_0/pdriver_1_0/pinv_9_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1115 control_logic_rw_0/pdriver_1_0/pinv_5_0/A control_logic_rw_0/pdriver_1_0/pinv_9_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1116 bank_0/wl_en0 control_logic_rw_0/pdriver_1_0/pinv_7_0/A gnd gnd n w=4u l=0.4u
+  ad=4.80063p pd=10.425u as=0p ps=0u
M1117 bank_0/wl_en0 control_logic_rw_0/pdriver_1_0/pinv_7_0/A vdd vdd p w=8u l=0.4u
+  ad=9.60063p pd=18.425u as=0p ps=0u
M1118 control_logic_rw_0/pdriver_1_0/pinv_7_0/A control_logic_rw_0/pdriver_1_0/pinv_5_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1119 control_logic_rw_0/pdriver_1_0/pinv_7_0/A control_logic_rw_0/pdriver_1_0/pinv_5_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1120 control_logic_rw_0/pdriver_1_0/pinv_9_0/A control_logic_rw_0/pand2_1/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1121 control_logic_rw_0/pdriver_1_0/pinv_9_0/A control_logic_rw_0/pand2_1/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1122 control_logic_rw_0/delay_chain_0/pinv_12_12/Z control_logic_rw_0/delay_chain_0/pinv_12_9/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1123 control_logic_rw_0/delay_chain_0/pinv_12_12/Z control_logic_rw_0/delay_chain_0/pinv_12_9/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1124 control_logic_rw_0/delay_chain_0/pinv_12_29/A control_logic_rw_0/delay_chain_0/pinv_12_34/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1125 control_logic_rw_0/delay_chain_0/pinv_12_29/A control_logic_rw_0/delay_chain_0/pinv_12_34/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1126 control_logic_rw_0/delay_chain_0/pinv_12_23/Z control_logic_rw_0/delay_chain_0/pinv_12_19/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1127 control_logic_rw_0/delay_chain_0/pinv_12_23/Z control_logic_rw_0/delay_chain_0/pinv_12_19/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1128 control_logic_rw_0/delay_chain_0/pinv_12_13/Z control_logic_rw_0/delay_chain_0/pinv_12_9/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1129 control_logic_rw_0/delay_chain_0/pinv_12_13/Z control_logic_rw_0/delay_chain_0/pinv_12_9/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1130 control_logic_rw_0/delay_chain_0/pinv_12_35/Z control_logic_rw_0/delay_chain_0/pinv_12_34/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1131 control_logic_rw_0/delay_chain_0/pinv_12_35/Z control_logic_rw_0/delay_chain_0/pinv_12_34/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1132 control_logic_rw_0/delay_chain_0/pinv_12_19/A control_logic_rw_0/delay_chain_0/pinv_12_24/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1133 control_logic_rw_0/delay_chain_0/pinv_12_19/A control_logic_rw_0/delay_chain_0/pinv_12_24/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1134 control_logic_rw_0/delay_chain_0/pinv_12_9/A control_logic_rw_0/delay_chain_0/pinv_12_14/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1135 control_logic_rw_0/delay_chain_0/pinv_12_9/A control_logic_rw_0/delay_chain_0/pinv_12_14/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1136 control_logic_rw_0/delay_chain_0/pinv_12_36/Z control_logic_rw_0/delay_chain_0/pinv_12_34/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1137 control_logic_rw_0/delay_chain_0/pinv_12_36/Z control_logic_rw_0/delay_chain_0/pinv_12_34/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1138 control_logic_rw_0/delay_chain_0/pinv_12_25/Z control_logic_rw_0/delay_chain_0/pinv_12_24/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1139 control_logic_rw_0/delay_chain_0/pinv_12_25/Z control_logic_rw_0/delay_chain_0/pinv_12_24/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1140 control_logic_rw_0/delay_chain_0/pinv_12_15/Z control_logic_rw_0/delay_chain_0/pinv_12_14/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1141 control_logic_rw_0/delay_chain_0/pinv_12_15/Z control_logic_rw_0/delay_chain_0/pinv_12_14/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1142 control_logic_rw_0/delay_chain_0/pinv_12_37/Z control_logic_rw_0/delay_chain_0/pinv_12_34/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1143 control_logic_rw_0/delay_chain_0/pinv_12_37/Z control_logic_rw_0/delay_chain_0/pinv_12_34/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1144 control_logic_rw_0/delay_chain_0/pinv_12_26/Z control_logic_rw_0/delay_chain_0/pinv_12_24/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1145 control_logic_rw_0/delay_chain_0/pinv_12_26/Z control_logic_rw_0/delay_chain_0/pinv_12_24/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1146 control_logic_rw_0/delay_chain_0/pinv_12_16/Z control_logic_rw_0/delay_chain_0/pinv_12_14/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1147 control_logic_rw_0/delay_chain_0/pinv_12_16/Z control_logic_rw_0/delay_chain_0/pinv_12_14/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1148 control_logic_rw_0/delay_chain_0/pinv_12_38/Z control_logic_rw_0/delay_chain_0/pinv_12_34/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1149 control_logic_rw_0/delay_chain_0/pinv_12_38/Z control_logic_rw_0/delay_chain_0/pinv_12_34/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1150 control_logic_rw_0/delay_chain_0/pinv_12_27/Z control_logic_rw_0/delay_chain_0/pinv_12_24/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1151 control_logic_rw_0/delay_chain_0/pinv_12_27/Z control_logic_rw_0/delay_chain_0/pinv_12_24/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1152 control_logic_rw_0/delay_chain_0/pinv_12_17/Z control_logic_rw_0/delay_chain_0/pinv_12_14/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1153 control_logic_rw_0/delay_chain_0/pinv_12_17/Z control_logic_rw_0/delay_chain_0/pinv_12_14/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1154 control_logic_rw_0/delay_chain_0/pinv_12_34/A control_logic_rw_0/delay_chain_0/pinv_12_39/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1155 control_logic_rw_0/delay_chain_0/pinv_12_34/A control_logic_rw_0/delay_chain_0/pinv_12_39/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1156 control_logic_rw_0/delay_chain_0/pinv_12_28/Z control_logic_rw_0/delay_chain_0/pinv_12_24/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1157 control_logic_rw_0/delay_chain_0/pinv_12_28/Z control_logic_rw_0/delay_chain_0/pinv_12_24/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1158 control_logic_rw_0/delay_chain_0/pinv_12_18/Z control_logic_rw_0/delay_chain_0/pinv_12_14/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1159 control_logic_rw_0/delay_chain_0/pinv_12_18/Z control_logic_rw_0/delay_chain_0/pinv_12_14/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1160 control_logic_rw_0/delay_chain_0/pinv_12_24/A control_logic_rw_0/delay_chain_0/pinv_12_29/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1161 control_logic_rw_0/delay_chain_0/pinv_12_24/A control_logic_rw_0/delay_chain_0/pinv_12_29/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1162 control_logic_rw_0/delay_chain_0/pinv_12_14/A control_logic_rw_0/delay_chain_0/pinv_12_19/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1163 control_logic_rw_0/delay_chain_0/pinv_12_14/A control_logic_rw_0/delay_chain_0/pinv_12_19/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1164 control_logic_rw_0/delay_chain_0/pinv_12_0/Z control_logic_rw_0/pinv_4_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1165 control_logic_rw_0/delay_chain_0/pinv_12_0/Z control_logic_rw_0/pinv_4_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1166 control_logic_rw_0/delay_chain_0/pinv_12_1/Z control_logic_rw_0/pinv_4_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1167 control_logic_rw_0/delay_chain_0/pinv_12_1/Z control_logic_rw_0/pinv_4_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1168 control_logic_rw_0/delay_chain_0/pinv_12_2/Z control_logic_rw_0/pinv_4_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1169 control_logic_rw_0/delay_chain_0/pinv_12_2/Z control_logic_rw_0/pinv_4_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1170 control_logic_rw_0/delay_chain_0/pinv_12_3/Z control_logic_rw_0/pinv_4_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1171 control_logic_rw_0/delay_chain_0/pinv_12_3/Z control_logic_rw_0/pinv_4_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1172 control_logic_rw_0/pinv_4_0/A control_logic_rw_0/delay_chain_0/pinv_12_4/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1173 control_logic_rw_0/pinv_4_0/A control_logic_rw_0/delay_chain_0/pinv_12_4/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1174 control_logic_rw_0/delay_chain_0/pinv_12_5/Z control_logic_rw_0/delay_chain_0/pinv_12_4/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1175 control_logic_rw_0/delay_chain_0/pinv_12_5/Z control_logic_rw_0/delay_chain_0/pinv_12_4/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1176 control_logic_rw_0/delay_chain_0/pinv_12_40/Z control_logic_rw_0/delay_chain_0/pinv_12_39/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1177 control_logic_rw_0/delay_chain_0/pinv_12_40/Z control_logic_rw_0/delay_chain_0/pinv_12_39/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1178 control_logic_rw_0/delay_chain_0/pinv_12_6/Z control_logic_rw_0/delay_chain_0/pinv_12_4/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1179 control_logic_rw_0/delay_chain_0/pinv_12_6/Z control_logic_rw_0/delay_chain_0/pinv_12_4/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1180 control_logic_rw_0/delay_chain_0/pinv_12_41/Z control_logic_rw_0/delay_chain_0/pinv_12_39/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1181 control_logic_rw_0/delay_chain_0/pinv_12_41/Z control_logic_rw_0/delay_chain_0/pinv_12_39/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1182 control_logic_rw_0/delay_chain_0/pinv_12_30/Z control_logic_rw_0/delay_chain_0/pinv_12_29/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1183 control_logic_rw_0/delay_chain_0/pinv_12_30/Z control_logic_rw_0/delay_chain_0/pinv_12_29/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1184 control_logic_rw_0/delay_chain_0/pinv_12_7/Z control_logic_rw_0/delay_chain_0/pinv_12_4/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1185 control_logic_rw_0/delay_chain_0/pinv_12_7/Z control_logic_rw_0/delay_chain_0/pinv_12_4/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1186 control_logic_rw_0/delay_chain_0/pinv_12_20/Z control_logic_rw_0/delay_chain_0/pinv_12_19/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1187 control_logic_rw_0/delay_chain_0/pinv_12_20/Z control_logic_rw_0/delay_chain_0/pinv_12_19/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1188 control_logic_rw_0/delay_chain_0/pinv_12_42/Z control_logic_rw_0/delay_chain_0/pinv_12_39/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1189 control_logic_rw_0/delay_chain_0/pinv_12_42/Z control_logic_rw_0/delay_chain_0/pinv_12_39/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1190 control_logic_rw_0/delay_chain_0/pinv_12_31/Z control_logic_rw_0/delay_chain_0/pinv_12_29/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1191 control_logic_rw_0/delay_chain_0/pinv_12_31/Z control_logic_rw_0/delay_chain_0/pinv_12_29/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1192 control_logic_rw_0/delay_chain_0/pinv_12_8/Z control_logic_rw_0/delay_chain_0/pinv_12_4/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1193 control_logic_rw_0/delay_chain_0/pinv_12_8/Z control_logic_rw_0/delay_chain_0/pinv_12_4/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1194 control_logic_rw_0/delay_chain_0/pinv_12_10/Z control_logic_rw_0/delay_chain_0/pinv_12_9/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1195 control_logic_rw_0/delay_chain_0/pinv_12_10/Z control_logic_rw_0/delay_chain_0/pinv_12_9/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1196 control_logic_rw_0/delay_chain_0/pinv_12_21/Z control_logic_rw_0/delay_chain_0/pinv_12_19/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1197 control_logic_rw_0/delay_chain_0/pinv_12_21/Z control_logic_rw_0/delay_chain_0/pinv_12_19/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1198 control_logic_rw_0/delay_chain_0/pinv_12_43/Z control_logic_rw_0/delay_chain_0/pinv_12_39/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1199 control_logic_rw_0/delay_chain_0/pinv_12_43/Z control_logic_rw_0/delay_chain_0/pinv_12_39/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1200 control_logic_rw_0/delay_chain_0/pinv_12_32/Z control_logic_rw_0/delay_chain_0/pinv_12_29/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1201 control_logic_rw_0/delay_chain_0/pinv_12_32/Z control_logic_rw_0/delay_chain_0/pinv_12_29/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1202 control_logic_rw_0/delay_chain_0/pinv_12_4/A control_logic_rw_0/delay_chain_0/pinv_12_9/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1203 control_logic_rw_0/delay_chain_0/pinv_12_4/A control_logic_rw_0/delay_chain_0/pinv_12_9/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1204 control_logic_rw_0/delay_chain_0/pinv_12_11/Z control_logic_rw_0/delay_chain_0/pinv_12_9/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1205 control_logic_rw_0/delay_chain_0/pinv_12_11/Z control_logic_rw_0/delay_chain_0/pinv_12_9/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1206 control_logic_rw_0/delay_chain_0/pinv_12_39/A rbl_bl0 vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1207 control_logic_rw_0/delay_chain_0/pinv_12_39/A rbl_bl0 gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1208 control_logic_rw_0/delay_chain_0/pinv_12_33/Z control_logic_rw_0/delay_chain_0/pinv_12_29/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1209 control_logic_rw_0/delay_chain_0/pinv_12_33/Z control_logic_rw_0/delay_chain_0/pinv_12_29/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1210 control_logic_rw_0/delay_chain_0/pinv_12_22/Z control_logic_rw_0/delay_chain_0/pinv_12_19/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1211 control_logic_rw_0/delay_chain_0/pinv_12_22/Z control_logic_rw_0/delay_chain_0/pinv_12_19/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1212 bank_0/p_en_bar0 control_logic_rw_0/pdriver_4_0/pinv_9_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1213 bank_0/p_en_bar0 control_logic_rw_0/pdriver_4_0/pinv_9_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1214 control_logic_rw_0/pdriver_4_0/pinv_9_0/A control_logic_rw_0/pnand2_1_0/Z vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1215 control_logic_rw_0/pdriver_4_0/pinv_9_0/A control_logic_rw_0/pnand2_1_0/Z gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1216 control_logic_rw_0/pand3_0/B control_logic_rw_0/pinv_4_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1217 control_logic_rw_0/pand3_0/B control_logic_rw_0/pinv_4_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1218 control_logic_rw_0/pand2_0/pnand2_0_0/nmos_m1_w1_600_sactive_dm1_0/S data_dff_0/clk gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1219 control_logic_rw_0/pand2_0/pdriver_0/A control_logic_rw_0/pand2_0/B control_logic_rw_0/pand2_0/pnand2_0_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1220 control_logic_rw_0/pand2_0/pdriver_0/A data_dff_0/clk vdd vdd p w=1.6u l=0.4u
+  ad=3.84125p pd=6.475u as=0p ps=0u
M1221 vdd control_logic_rw_0/pand2_0/B control_logic_rw_0/pand2_0/pdriver_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1222 control_logic_rw_0/pand2_0/Z control_logic_rw_0/pand2_0/pdriver_0/A vdd vdd p w=6.4u l=0.4u
+  ad=15.3606p pd=30.425u as=0p ps=0u
M1223 control_logic_rw_0/pand2_0/Z control_logic_rw_0/pand2_0/pdriver_0/A vdd vdd p w=6.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1224 vdd control_logic_rw_0/pand2_0/pdriver_0/A control_logic_rw_0/pand2_0/Z vdd p w=6.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1225 control_logic_rw_0/pand2_0/Z control_logic_rw_0/pand2_0/pdriver_0/A gnd gnd n w=3.2u l=0.4u
+  ad=7.68063p pd=17.625u as=0p ps=0u
M1226 control_logic_rw_0/pand2_0/Z control_logic_rw_0/pand2_0/pdriver_0/A gnd gnd n w=3.2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1227 gnd control_logic_rw_0/pand2_0/pdriver_0/A control_logic_rw_0/pand2_0/Z gnd n w=3.2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1228 control_logic_rw_0/pand2_1/pnand2_0_0/nmos_m1_w1_600_sactive_dm1_0/S control_logic_rw_0/pand2_1/A gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1229 control_logic_rw_0/pand2_1/pdriver_0/A control_logic_rw_0/pand2_0/B control_logic_rw_0/pand2_1/pnand2_0_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1230 control_logic_rw_0/pand2_1/pdriver_0/A control_logic_rw_0/pand2_1/A vdd vdd p w=1.6u l=0.4u
+  ad=3.84125p pd=6.475u as=0p ps=0u
M1231 vdd control_logic_rw_0/pand2_0/B control_logic_rw_0/pand2_1/pdriver_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1232 control_logic_rw_0/pand2_1/Z control_logic_rw_0/pand2_1/pdriver_0/A vdd vdd p w=6.4u l=0.4u
+  ad=15.3606p pd=30.425u as=0p ps=0u
M1233 control_logic_rw_0/pand2_1/Z control_logic_rw_0/pand2_1/pdriver_0/A vdd vdd p w=6.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1234 vdd control_logic_rw_0/pand2_1/pdriver_0/A control_logic_rw_0/pand2_1/Z vdd p w=6.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1235 control_logic_rw_0/pand2_1/Z control_logic_rw_0/pand2_1/pdriver_0/A gnd gnd n w=3.2u l=0.4u
+  ad=7.68063p pd=17.625u as=0p ps=0u
M1236 control_logic_rw_0/pand2_1/Z control_logic_rw_0/pand2_1/pdriver_0/A gnd gnd n w=3.2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1237 gnd control_logic_rw_0/pand2_1/pdriver_0/A control_logic_rw_0/pand2_1/Z gnd n w=3.2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1238 control_logic_rw_0/pand2_1/A data_dff_0/clk vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1239 control_logic_rw_0/pand2_1/A data_dff_0/clk gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1240 control_logic_rw_0/pnand2_1_0/nmos_m1_w1_600_sactive_dm1_0/S control_logic_rw_0/pand2_0/Z gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1241 control_logic_rw_0/pnand2_1_0/Z control_logic_rw_0/pinv_4_0/A control_logic_rw_0/pnand2_1_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1242 control_logic_rw_0/pnand2_1_0/Z control_logic_rw_0/pand2_0/Z vdd vdd p w=1.6u l=0.4u
+  ad=3.84125p pd=6.475u as=0p ps=0u
M1243 vdd control_logic_rw_0/pinv_4_0/A control_logic_rw_0/pnand2_1_0/Z vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1244 control_logic_rw_0/pdriver_0_0/pinv_8_0/A control_logic_rw_0/pdriver_0_0/pinv_7_0/A gnd gnd n w=4u l=0.4u
+  ad=4.80063p pd=10.425u as=0p ps=0u
M1245 control_logic_rw_0/pdriver_0_0/pinv_8_0/A control_logic_rw_0/pdriver_0_0/pinv_7_0/A vdd vdd p w=8u l=0.4u
+  ad=9.60063p pd=18.425u as=0p ps=0u
M1246 control_logic_rw_0/pdriver_0_0/pinv_7_0/A control_logic_rw_0/pdriver_0_0/pinv_5_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1247 control_logic_rw_0/pdriver_0_0/pinv_7_0/A control_logic_rw_0/pdriver_0_0/pinv_5_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1248 data_dff_0/clk control_logic_rw_0/pdriver_0_0/pinv_8_0/A vdd vdd p w=8u l=0.4u
+  ad=19.2006p pd=36.825u as=0p ps=0u
M1249 data_dff_0/clk control_logic_rw_0/pdriver_0_0/pinv_8_0/A vdd vdd p w=8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1250 vdd control_logic_rw_0/pdriver_0_0/pinv_8_0/A data_dff_0/clk vdd p w=8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1251 data_dff_0/clk control_logic_rw_0/pdriver_0_0/pinv_8_0/A gnd gnd n w=4u l=0.4u
+  ad=9.60063p pd=20.825u as=0p ps=0u
M1252 data_dff_0/clk control_logic_rw_0/pdriver_0_0/pinv_8_0/A gnd gnd n w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1253 gnd control_logic_rw_0/pdriver_0_0/pinv_8_0/A data_dff_0/clk gnd n w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1254 control_logic_rw_0/pdriver_0_0/pinv_5_0/A clk0 vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1255 control_logic_rw_0/pdriver_0_0/pinv_5_0/A clk0 gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1256 row_addr_dff_0/dff_0/a_304_32# row_addr_dff_0/dff_0/a_208_48# gnd gnd n w=2u l=0.4u
+  ad=2p pd=6u as=0p ps=0u
M1257 row_addr_dff_0/dff_0/a_640_48# row_addr_dff_0/dff_0/a_48_48# row_addr_dff_0/dff_0/a_560_48# gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=3.2p ps=7.2u
M1258 gnd bank_0/addr0_3 row_addr_dff_0/dff_0/a_640_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1259 row_addr_dff_0/dff_0/a_280_48# data_dff_0/clk row_addr_dff_0/dff_0/a_208_48# gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=2.8p ps=6.8u
M1260 vdd data_dff_0/clk row_addr_dff_0/dff_0/a_48_48# vdd p w=8u l=0.4u
+  ad=0p pd=0u as=8p ps=18u
M1261 gnd data_dff_0/clk row_addr_dff_0/dff_0/a_48_48# gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4p ps=10u
M1262 row_addr_dff_0/dff_0/a_168_48# addr0[3] gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1263 row_addr_dff_0/dff_0/a_208_48# row_addr_dff_0/dff_0/a_48_48# row_addr_dff_0/dff_0/a_168_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1264 gnd row_addr_dff_0/dff_0/a_304_32# row_addr_dff_0/dff_0/a_280_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1265 bank_0/addr0_3 row_addr_dff_0/dff_0/a_560_48# gnd gnd n w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1266 vdd bank_0/addr0_3 row_addr_dff_0/dff_0/a_640_672# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1267 vdd row_addr_dff_0/dff_0/a_304_32# row_addr_dff_0/dff_0/a_280_592# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=3.2p ps=9.6u
M1268 row_addr_dff_0/dff_0/a_208_48# data_dff_0/clk row_addr_dff_0/dff_0/a_168_592# vdd p w=4u l=0.4u
+  ad=4.8p pd=10.4u as=3.2p ps=9.6u
M1269 row_addr_dff_0/dff_0/a_640_672# data_dff_0/clk row_addr_dff_0/dff_0/a_560_48# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=6p ps=11.2u
M1270 bank_0/addr0_3 row_addr_dff_0/dff_0/a_560_48# vdd vdd p w=8u l=0.4u
+  ad=8p pd=18u as=0p ps=0u
M1271 row_addr_dff_0/dff_0/a_560_48# row_addr_dff_0/dff_0/a_48_48# row_addr_dff_0/dff_0/a_520_592# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=2.4p ps=9.2u
M1272 row_addr_dff_0/dff_0/a_304_32# row_addr_dff_0/dff_0/a_208_48# vdd vdd p w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1273 row_addr_dff_0/dff_0/a_520_48# row_addr_dff_0/dff_0/a_304_32# gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1274 row_addr_dff_0/dff_0/a_560_48# data_dff_0/clk row_addr_dff_0/dff_0/a_520_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1275 row_addr_dff_0/dff_0/a_280_592# row_addr_dff_0/dff_0/a_48_48# row_addr_dff_0/dff_0/a_208_48# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1276 row_addr_dff_0/dff_0/a_168_592# addr0[3] vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1277 row_addr_dff_0/dff_0/a_520_592# row_addr_dff_0/dff_0/a_304_32# vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1278 row_addr_dff_0/dff_1/a_304_32# row_addr_dff_0/dff_1/a_208_48# gnd gnd n w=2u l=0.4u
+  ad=2p pd=6u as=0p ps=0u
M1279 row_addr_dff_0/dff_1/a_640_48# row_addr_dff_0/dff_1/a_48_48# row_addr_dff_0/dff_1/a_560_48# gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=3.2p ps=7.2u
M1280 gnd bank_0/addr0_2 row_addr_dff_0/dff_1/a_640_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1281 row_addr_dff_0/dff_1/a_280_48# data_dff_0/clk row_addr_dff_0/dff_1/a_208_48# gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=2.8p ps=6.8u
M1282 vdd data_dff_0/clk row_addr_dff_0/dff_1/a_48_48# vdd p w=8u l=0.4u
+  ad=0p pd=0u as=8p ps=18u
M1283 gnd data_dff_0/clk row_addr_dff_0/dff_1/a_48_48# gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4p ps=10u
M1284 row_addr_dff_0/dff_1/a_168_48# addr0[2] gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1285 row_addr_dff_0/dff_1/a_208_48# row_addr_dff_0/dff_1/a_48_48# row_addr_dff_0/dff_1/a_168_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1286 gnd row_addr_dff_0/dff_1/a_304_32# row_addr_dff_0/dff_1/a_280_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1287 bank_0/addr0_2 row_addr_dff_0/dff_1/a_560_48# gnd gnd n w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1288 vdd bank_0/addr0_2 row_addr_dff_0/dff_1/a_640_672# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1289 vdd row_addr_dff_0/dff_1/a_304_32# row_addr_dff_0/dff_1/a_280_592# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=3.2p ps=9.6u
M1290 row_addr_dff_0/dff_1/a_208_48# data_dff_0/clk row_addr_dff_0/dff_1/a_168_592# vdd p w=4u l=0.4u
+  ad=4.8p pd=10.4u as=3.2p ps=9.6u
M1291 row_addr_dff_0/dff_1/a_640_672# data_dff_0/clk row_addr_dff_0/dff_1/a_560_48# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=6p ps=11.2u
M1292 bank_0/addr0_2 row_addr_dff_0/dff_1/a_560_48# vdd vdd p w=8u l=0.4u
+  ad=8p pd=18u as=0p ps=0u
M1293 row_addr_dff_0/dff_1/a_560_48# row_addr_dff_0/dff_1/a_48_48# row_addr_dff_0/dff_1/a_520_592# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=2.4p ps=9.2u
M1294 row_addr_dff_0/dff_1/a_304_32# row_addr_dff_0/dff_1/a_208_48# vdd vdd p w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1295 row_addr_dff_0/dff_1/a_520_48# row_addr_dff_0/dff_1/a_304_32# gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1296 row_addr_dff_0/dff_1/a_560_48# data_dff_0/clk row_addr_dff_0/dff_1/a_520_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1297 row_addr_dff_0/dff_1/a_280_592# row_addr_dff_0/dff_1/a_48_48# row_addr_dff_0/dff_1/a_208_48# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1298 row_addr_dff_0/dff_1/a_168_592# addr0[2] vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1299 row_addr_dff_0/dff_1/a_520_592# row_addr_dff_0/dff_1/a_304_32# vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1300 row_addr_dff_0/dff_2/a_304_32# row_addr_dff_0/dff_2/a_208_48# gnd gnd n w=2u l=0.4u
+  ad=2p pd=6u as=0p ps=0u
M1301 row_addr_dff_0/dff_2/a_640_48# row_addr_dff_0/dff_2/a_48_48# row_addr_dff_0/dff_2/a_560_48# gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=3.2p ps=7.2u
M1302 gnd bank_0/addr0_1 row_addr_dff_0/dff_2/a_640_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1303 row_addr_dff_0/dff_2/a_280_48# data_dff_0/clk row_addr_dff_0/dff_2/a_208_48# gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=2.8p ps=6.8u
M1304 vdd data_dff_0/clk row_addr_dff_0/dff_2/a_48_48# vdd p w=8u l=0.4u
+  ad=0p pd=0u as=8p ps=18u
M1305 gnd data_dff_0/clk row_addr_dff_0/dff_2/a_48_48# gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4p ps=10u
M1306 row_addr_dff_0/dff_2/a_168_48# addr0[1] gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1307 row_addr_dff_0/dff_2/a_208_48# row_addr_dff_0/dff_2/a_48_48# row_addr_dff_0/dff_2/a_168_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1308 gnd row_addr_dff_0/dff_2/a_304_32# row_addr_dff_0/dff_2/a_280_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1309 bank_0/addr0_1 row_addr_dff_0/dff_2/a_560_48# gnd gnd n w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1310 vdd bank_0/addr0_1 row_addr_dff_0/dff_2/a_640_672# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1311 vdd row_addr_dff_0/dff_2/a_304_32# row_addr_dff_0/dff_2/a_280_592# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=3.2p ps=9.6u
M1312 row_addr_dff_0/dff_2/a_208_48# data_dff_0/clk row_addr_dff_0/dff_2/a_168_592# vdd p w=4u l=0.4u
+  ad=4.8p pd=10.4u as=3.2p ps=9.6u
M1313 row_addr_dff_0/dff_2/a_640_672# data_dff_0/clk row_addr_dff_0/dff_2/a_560_48# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=6p ps=11.2u
M1314 bank_0/addr0_1 row_addr_dff_0/dff_2/a_560_48# vdd vdd p w=8u l=0.4u
+  ad=8p pd=18u as=0p ps=0u
M1315 row_addr_dff_0/dff_2/a_560_48# row_addr_dff_0/dff_2/a_48_48# row_addr_dff_0/dff_2/a_520_592# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=2.4p ps=9.2u
M1316 row_addr_dff_0/dff_2/a_304_32# row_addr_dff_0/dff_2/a_208_48# vdd vdd p w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1317 row_addr_dff_0/dff_2/a_520_48# row_addr_dff_0/dff_2/a_304_32# gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1318 row_addr_dff_0/dff_2/a_560_48# data_dff_0/clk row_addr_dff_0/dff_2/a_520_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1319 row_addr_dff_0/dff_2/a_280_592# row_addr_dff_0/dff_2/a_48_48# row_addr_dff_0/dff_2/a_208_48# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1320 row_addr_dff_0/dff_2/a_168_592# addr0[1] vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1321 row_addr_dff_0/dff_2/a_520_592# row_addr_dff_0/dff_2/a_304_32# vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1322 row_addr_dff_0/dff_3/a_304_32# row_addr_dff_0/dff_3/a_208_48# gnd gnd n w=2u l=0.4u
+  ad=2p pd=6u as=0p ps=0u
M1323 row_addr_dff_0/dff_3/a_640_48# row_addr_dff_0/dff_3/a_48_48# row_addr_dff_0/dff_3/a_560_48# gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=3.2p ps=7.2u
M1324 gnd bank_0/addr0_0 row_addr_dff_0/dff_3/a_640_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1325 row_addr_dff_0/dff_3/a_280_48# data_dff_0/clk row_addr_dff_0/dff_3/a_208_48# gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=2.8p ps=6.8u
M1326 vdd data_dff_0/clk row_addr_dff_0/dff_3/a_48_48# vdd p w=8u l=0.4u
+  ad=0p pd=0u as=8p ps=18u
M1327 gnd data_dff_0/clk row_addr_dff_0/dff_3/a_48_48# gnd n w=4u l=0.4u
+  ad=0p pd=0u as=4p ps=10u
M1328 row_addr_dff_0/dff_3/a_168_48# addr0[0] gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1329 row_addr_dff_0/dff_3/a_208_48# row_addr_dff_0/dff_3/a_48_48# row_addr_dff_0/dff_3/a_168_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1330 gnd row_addr_dff_0/dff_3/a_304_32# row_addr_dff_0/dff_3/a_280_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1331 bank_0/addr0_0 row_addr_dff_0/dff_3/a_560_48# gnd gnd n w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1332 vdd bank_0/addr0_0 row_addr_dff_0/dff_3/a_640_672# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=1.2p ps=5.2u
M1333 vdd row_addr_dff_0/dff_3/a_304_32# row_addr_dff_0/dff_3/a_280_592# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=3.2p ps=9.6u
M1334 row_addr_dff_0/dff_3/a_208_48# data_dff_0/clk row_addr_dff_0/dff_3/a_168_592# vdd p w=4u l=0.4u
+  ad=4.8p pd=10.4u as=3.2p ps=9.6u
M1335 row_addr_dff_0/dff_3/a_640_672# data_dff_0/clk row_addr_dff_0/dff_3/a_560_48# vdd p w=2u l=0.4u
+  ad=0p pd=0u as=6p ps=11.2u
M1336 bank_0/addr0_0 row_addr_dff_0/dff_3/a_560_48# vdd vdd p w=8u l=0.4u
+  ad=8p pd=18u as=0p ps=0u
M1337 row_addr_dff_0/dff_3/a_560_48# row_addr_dff_0/dff_3/a_48_48# row_addr_dff_0/dff_3/a_520_592# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=2.4p ps=9.2u
M1338 row_addr_dff_0/dff_3/a_304_32# row_addr_dff_0/dff_3/a_208_48# vdd vdd p w=4u l=0.4u
+  ad=4p pd=10u as=0p ps=0u
M1339 row_addr_dff_0/dff_3/a_520_48# row_addr_dff_0/dff_3/a_304_32# gnd gnd n w=2u l=0.4u
+  ad=1.2p pd=5.2u as=0p ps=0u
M1340 row_addr_dff_0/dff_3/a_560_48# data_dff_0/clk row_addr_dff_0/dff_3/a_520_48# gnd n w=2u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1341 row_addr_dff_0/dff_3/a_280_592# row_addr_dff_0/dff_3/a_48_48# row_addr_dff_0/dff_3/a_208_48# vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1342 row_addr_dff_0/dff_3/a_168_592# addr0[0] vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1343 row_addr_dff_0/dff_3/a_520_592# row_addr_dff_0/dff_3/a_304_32# vdd vdd p w=4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1344 bl0_1 bank_0/s_en0 dout0[1] vdd p w=4.8u l=0.4u
+  ad=8.64125p pd=22.85u as=8.4p ps=20.8u
M1345 vdd bank_0/port_data_0/sense_amp_array_0/sense_amp_0/a_96_608# dout0[1] vdd p w=3.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1346 bank_0/port_data_0/sense_amp_array_0/sense_amp_0/a_112_864# bank_0/port_data_0/sense_amp_array_0/sense_amp_0/a_96_608# dout0[1] gnd n w=1.8u l=0.4u
+  ad=3.96p pd=11.6u as=1.8p ps=5.6u
M1347 gnd bank_0/s_en0 bank_0/port_data_0/sense_amp_array_0/sense_amp_0/a_112_864# gnd n w=1.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1348 bank_0/port_data_0/sense_amp_array_0/sense_amp_0/a_96_608# bank_0/s_en0 br0_1 vdd p w=4.8u l=0.4u
+  ad=8.4p pd=20.8u as=8.64125p ps=22.85u
M1349 bank_0/port_data_0/sense_amp_array_0/sense_amp_0/a_96_608# dout0[1] bank_0/port_data_0/sense_amp_array_0/sense_amp_0/a_112_864# gnd n w=1.8u l=0.4u
+  ad=1.8p pd=5.6u as=0p ps=0u
M1350 bank_0/port_data_0/sense_amp_array_0/sense_amp_0/a_96_608# dout0[1] vdd vdd p w=3.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1351 bl0_0 bank_0/s_en0 dout0[0] vdd p w=4.8u l=0.4u
+  ad=8.64125p pd=22.85u as=8.4p ps=20.8u
M1352 vdd bank_0/port_data_0/sense_amp_array_0/sense_amp_1/a_96_608# dout0[0] vdd p w=3.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1353 bank_0/port_data_0/sense_amp_array_0/sense_amp_1/a_112_864# bank_0/port_data_0/sense_amp_array_0/sense_amp_1/a_96_608# dout0[0] gnd n w=1.8u l=0.4u
+  ad=3.96p pd=11.6u as=1.8p ps=5.6u
M1354 gnd bank_0/s_en0 bank_0/port_data_0/sense_amp_array_0/sense_amp_1/a_112_864# gnd n w=1.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1355 bank_0/port_data_0/sense_amp_array_0/sense_amp_1/a_96_608# bank_0/s_en0 br0_0 vdd p w=4.8u l=0.4u
+  ad=8.4p pd=20.8u as=8.64125p ps=22.85u
M1356 bank_0/port_data_0/sense_amp_array_0/sense_amp_1/a_96_608# dout0[0] bank_0/port_data_0/sense_amp_array_0/sense_amp_1/a_112_864# gnd n w=1.8u l=0.4u
+  ad=1.8p pd=5.6u as=0p ps=0u
M1357 bank_0/port_data_0/sense_amp_array_0/sense_amp_1/a_96_608# dout0[0] vdd vdd p w=3.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1358 bank_0/port_data_0/write_driver_array_0/write_driver_0/a_128_720# bank_0/din0_1 vdd vdd p w=1.4u l=0.4u
+  ad=1.4p pd=4.8u as=0p ps=0u
M1359 br0_1 bank_0/port_data_0/write_driver_array_0/write_driver_0/a_32_1000# gnd gnd n w=2.4u l=0.4u
+  ad=15.2p pd=64.4u as=0p ps=0u
M1360 gnd bank_0/port_data_0/write_driver_array_0/write_driver_0/a_128_720# bank_0/port_data_0/write_driver_array_0/write_driver_0/a_96_656# gnd n w=1.4u l=0.4u
+  ad=0p pd=0u as=1.68p ps=5.2u
M1361 bank_0/port_data_0/write_driver_array_0/write_driver_0/a_128_720# bank_0/din0_1 gnd gnd n w=0.8u l=0.4u
+  ad=0.8p pd=3.6u as=0p ps=0u
M1362 bank_0/port_data_0/write_driver_array_0/write_driver_0/a_16_568# bank_0/w_en0 vdd vdd p w=1.4u l=0.4u
+  ad=1.68p pd=5.2u as=0p ps=0u
M1363 vdd bank_0/w_en0 bank_0/port_data_0/write_driver_array_0/write_driver_0/a_40_656# vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=2.8p ps=9.6u
M1364 vdd bank_0/port_data_0/write_driver_array_0/write_driver_0/a_16_568# bank_0/port_data_0/write_driver_array_0/write_driver_0/a_32_1000# vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=1.4p ps=4.8u
M1365 bank_0/port_data_0/write_driver_array_0/write_driver_0/a_80_456# bank_0/w_en0 bank_0/port_data_0/write_driver_array_0/write_driver_0/a_16_568# gnd n w=1.4u l=0.4u
+  ad=1.68p pd=5.2u as=1.4p ps=4.8u
M1366 gnd bank_0/port_data_0/write_driver_array_0/write_driver_0/a_16_568# bank_0/port_data_0/write_driver_array_0/write_driver_0/a_32_1000# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1367 vdd bank_0/din0_1 bank_0/port_data_0/write_driver_array_0/write_driver_0/a_16_568# vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1368 bank_0/port_data_0/write_driver_array_0/write_driver_0/a_40_656# bank_0/port_data_0/write_driver_array_0/write_driver_0/a_128_720# vdd vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1369 gnd bank_0/din0_1 bank_0/port_data_0/write_driver_array_0/write_driver_0/a_80_456# gnd n w=1.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1370 gnd bank_0/port_data_0/write_driver_array_0/write_driver_0/a_72_1408# bl0_1 gnd n w=2.4u l=0.4u
+  ad=0p pd=0u as=15.2p ps=64.4u
M1371 bank_0/port_data_0/write_driver_array_0/write_driver_0/a_72_1408# bank_0/port_data_0/write_driver_array_0/write_driver_0/a_40_656# vdd vdd p w=1.4u l=0.4u
+  ad=1.4p pd=4.8u as=0p ps=0u
M1372 bank_0/port_data_0/write_driver_array_0/write_driver_0/a_96_656# bank_0/w_en0 bank_0/port_data_0/write_driver_array_0/write_driver_0/a_40_656# gnd n w=1.4u l=0.4u
+  ad=0p pd=0u as=1.4p ps=4.8u
M1373 bank_0/port_data_0/write_driver_array_0/write_driver_0/a_72_1408# bank_0/port_data_0/write_driver_array_0/write_driver_0/a_40_656# gnd gnd n w=0.8u l=0.4u
+  ad=0.8p pd=3.6u as=0p ps=0u
M1374 bank_0/port_data_0/write_driver_array_0/write_driver_1/a_128_720# bank_0/din0_0 vdd vdd p w=1.4u l=0.4u
+  ad=1.4p pd=4.8u as=0p ps=0u
M1375 br0_0 bank_0/port_data_0/write_driver_array_0/write_driver_1/a_32_1000# gnd gnd n w=2.4u l=0.4u
+  ad=15.2p pd=64.4u as=0p ps=0u
M1376 gnd bank_0/port_data_0/write_driver_array_0/write_driver_1/a_128_720# bank_0/port_data_0/write_driver_array_0/write_driver_1/a_96_656# gnd n w=1.4u l=0.4u
+  ad=0p pd=0u as=1.68p ps=5.2u
M1377 bank_0/port_data_0/write_driver_array_0/write_driver_1/a_128_720# bank_0/din0_0 gnd gnd n w=0.8u l=0.4u
+  ad=0.8p pd=3.6u as=0p ps=0u
M1378 bank_0/port_data_0/write_driver_array_0/write_driver_1/a_16_568# bank_0/w_en0 vdd vdd p w=1.4u l=0.4u
+  ad=1.68p pd=5.2u as=0p ps=0u
M1379 vdd bank_0/w_en0 bank_0/port_data_0/write_driver_array_0/write_driver_1/a_40_656# vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=2.8p ps=9.6u
M1380 vdd bank_0/port_data_0/write_driver_array_0/write_driver_1/a_16_568# bank_0/port_data_0/write_driver_array_0/write_driver_1/a_32_1000# vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=1.4p ps=4.8u
M1381 bank_0/port_data_0/write_driver_array_0/write_driver_1/a_80_456# bank_0/w_en0 bank_0/port_data_0/write_driver_array_0/write_driver_1/a_16_568# gnd n w=1.4u l=0.4u
+  ad=1.68p pd=5.2u as=1.4p ps=4.8u
M1382 gnd bank_0/port_data_0/write_driver_array_0/write_driver_1/a_16_568# bank_0/port_data_0/write_driver_array_0/write_driver_1/a_32_1000# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1383 vdd bank_0/din0_0 bank_0/port_data_0/write_driver_array_0/write_driver_1/a_16_568# vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1384 bank_0/port_data_0/write_driver_array_0/write_driver_1/a_40_656# bank_0/port_data_0/write_driver_array_0/write_driver_1/a_128_720# vdd vdd p w=1.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1385 gnd bank_0/din0_0 bank_0/port_data_0/write_driver_array_0/write_driver_1/a_80_456# gnd n w=1.4u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1386 gnd bank_0/port_data_0/write_driver_array_0/write_driver_1/a_72_1408# bl0_0 gnd n w=2.4u l=0.4u
+  ad=0p pd=0u as=15.2p ps=64.4u
M1387 bank_0/port_data_0/write_driver_array_0/write_driver_1/a_72_1408# bank_0/port_data_0/write_driver_array_0/write_driver_1/a_40_656# vdd vdd p w=1.4u l=0.4u
+  ad=1.4p pd=4.8u as=0p ps=0u
M1388 bank_0/port_data_0/write_driver_array_0/write_driver_1/a_96_656# bank_0/w_en0 bank_0/port_data_0/write_driver_array_0/write_driver_1/a_40_656# gnd n w=1.4u l=0.4u
+  ad=0p pd=0u as=1.4p ps=4.8u
M1389 bank_0/port_data_0/write_driver_array_0/write_driver_1/a_72_1408# bank_0/port_data_0/write_driver_array_0/write_driver_1/a_40_656# gnd gnd n w=0.8u l=0.4u
+  ad=0.8p pd=3.6u as=0p ps=0u
M1390 vdd bank_0/p_en_bar0 bl0_1 vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1391 br0_1 bank_0/p_en_bar0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1392 br0_1 bank_0/p_en_bar0 bl0_1 vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1393 vdd bank_0/p_en_bar0 bl0_0 vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1394 br0_0 bank_0/p_en_bar0 vdd vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1395 br0_0 bank_0/p_en_bar0 bl0_0 vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1396 vdd bank_0/p_en_bar0 rbl_bl0 vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=3.84125p ps=11.25u
M1397 bank_0/port_data_0/rbl_br bank_0/p_en_bar0 vdd vdd p w=1.6u l=0.4u
+  ad=3.84125p pd=11.25u as=0p ps=0u
M1398 bank_0/port_data_0/rbl_br bank_0/p_en_bar0 rbl_bl0 vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1399 bank_0/port_address_0/wordline_driver_array_0/in_15 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_0/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1400 bank_0/port_address_0/wordline_driver_array_0/in_15 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_0/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1401 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_0/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/predecode_3 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1402 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_0/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_7 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_0/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1403 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_0/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_3 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1404 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_7 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_0/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1405 bank_0/port_address_0/wordline_driver_array_0/in_14 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_1/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1406 bank_0/port_address_0/wordline_driver_array_0/in_14 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_1/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1407 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_1/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/predecode_2 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1408 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_1/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_7 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_1/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1409 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_1/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_2 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1410 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_7 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_1/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1411 bank_0/port_address_0/wordline_driver_array_0/in_13 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_2/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1412 bank_0/port_address_0/wordline_driver_array_0/in_13 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_2/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1413 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_2/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/predecode_1 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1414 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_2/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_7 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_2/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1415 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_2/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_1 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1416 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_7 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_2/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1417 bank_0/port_address_0/wordline_driver_array_0/in_12 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_3/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1418 bank_0/port_address_0/wordline_driver_array_0/in_12 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_3/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1419 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_3/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/predecode_0 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1420 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_3/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_7 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_3/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1421 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_3/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_0 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1422 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_7 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_3/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1423 bank_0/port_address_0/wordline_driver_array_0/in_11 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_4/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1424 bank_0/port_address_0/wordline_driver_array_0/in_11 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_4/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1425 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_4/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/predecode_3 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1426 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_4/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_6 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_4/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1427 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_4/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_3 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1428 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_6 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_4/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1429 bank_0/port_address_0/wordline_driver_array_0/in_10 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_5/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1430 bank_0/port_address_0/wordline_driver_array_0/in_10 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_5/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1431 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_5/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/predecode_2 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1432 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_5/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_6 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_5/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1433 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_5/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_2 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1434 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_6 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_5/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1435 bank_0/port_address_0/wordline_driver_array_0/in_9 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_6/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1436 bank_0/port_address_0/wordline_driver_array_0/in_9 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_6/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1437 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_6/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/predecode_1 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1438 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_6/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_6 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_6/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1439 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_6/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_1 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1440 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_6 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_6/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1441 bank_0/port_address_0/wordline_driver_array_0/in_8 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_7/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1442 bank_0/port_address_0/wordline_driver_array_0/in_8 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_7/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1443 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_7/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/predecode_0 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1444 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_7/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_6 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_7/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1445 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_7/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_0 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1446 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_6 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_7/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1447 bank_0/port_address_0/wordline_driver_array_0/in_7 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_8/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1448 bank_0/port_address_0/wordline_driver_array_0/in_7 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_8/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1449 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_8/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/predecode_3 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1450 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_8/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_5 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_8/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1451 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_8/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_3 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1452 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_5 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_8/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1453 bank_0/port_address_0/hierarchical_decoder_0/predecode_7 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_0/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1454 bank_0/port_address_0/hierarchical_decoder_0/predecode_7 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_0/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1455 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_0/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/addr0_2 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1456 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_0/pinv_0/A bank_0/addr0_3 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_0/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1457 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_0/pinv_0/A bank_0/addr0_2 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1458 vdd bank_0/addr0_3 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_0/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1459 bank_0/port_address_0/hierarchical_decoder_0/predecode_6 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_1/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1460 bank_0/port_address_0/hierarchical_decoder_0/predecode_6 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_1/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1461 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_1/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_1/Z gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1462 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_1/pinv_0/A bank_0/addr0_3 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_1/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1463 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_1/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_1/Z vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1464 vdd bank_0/addr0_3 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_1/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1465 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_0/Z bank_0/addr0_3 vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1466 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_0/Z bank_0/addr0_3 gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1467 bank_0/port_address_0/hierarchical_decoder_0/predecode_5 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_2/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1468 bank_0/port_address_0/hierarchical_decoder_0/predecode_5 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_2/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1469 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_2/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/addr0_2 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1470 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_2/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_0/Z bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_2/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1471 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_2/pinv_0/A bank_0/addr0_2 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1472 vdd bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_0/Z bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_2/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1473 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_1/Z bank_0/addr0_2 vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1474 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_1/Z bank_0/addr0_2 gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1475 bank_0/port_address_0/hierarchical_decoder_0/predecode_4 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_3/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1476 bank_0/port_address_0/hierarchical_decoder_0/predecode_4 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_3/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1477 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_3/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_1/Z gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1478 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_3/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_0/Z bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_3/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1479 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_3/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_1/Z vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1480 vdd bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_0/Z bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/and2_dec_3/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1481 bank_0/port_address_0/hierarchical_decoder_0/predecode_3 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_0/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1482 bank_0/port_address_0/hierarchical_decoder_0/predecode_3 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_0/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1483 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_0/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/addr0_0 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1484 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_0/pinv_0/A bank_0/addr0_1 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_0/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1485 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_0/pinv_0/A bank_0/addr0_0 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1486 vdd bank_0/addr0_1 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_0/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1487 bank_0/port_address_0/hierarchical_decoder_0/predecode_2 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_1/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1488 bank_0/port_address_0/hierarchical_decoder_0/predecode_2 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_1/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1489 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_1/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_1/Z gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1490 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_1/pinv_0/A bank_0/addr0_1 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_1/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1491 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_1/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_1/Z vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1492 vdd bank_0/addr0_1 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_1/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1493 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_0/Z bank_0/addr0_1 vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1494 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_0/Z bank_0/addr0_1 gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1495 bank_0/port_address_0/hierarchical_decoder_0/predecode_1 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_2/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1496 bank_0/port_address_0/hierarchical_decoder_0/predecode_1 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_2/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1497 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_2/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/addr0_0 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1498 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_2/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_0/Z bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_2/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1499 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_2/pinv_0/A bank_0/addr0_0 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1500 vdd bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_0/Z bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_2/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1501 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_1/Z bank_0/addr0_0 vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1502 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_1/Z bank_0/addr0_0 gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1503 bank_0/port_address_0/hierarchical_decoder_0/predecode_0 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_3/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1504 bank_0/port_address_0/hierarchical_decoder_0/predecode_0 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_3/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1505 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_3/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_1/Z gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1506 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_3/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_0/Z bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_3/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1507 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_3/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_1/Z vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1508 vdd bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_0/Z bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/and2_dec_3/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1509 bank_0/port_address_0/wordline_driver_array_0/in_6 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_9/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1510 bank_0/port_address_0/wordline_driver_array_0/in_6 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_9/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1511 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_9/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/predecode_2 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1512 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_9/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_5 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_9/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1513 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_9/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_2 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1514 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_5 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_9/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1515 bank_0/port_address_0/wordline_driver_array_0/in_5 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_10/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1516 bank_0/port_address_0/wordline_driver_array_0/in_5 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_10/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1517 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_10/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/predecode_1 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1518 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_10/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_5 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_10/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1519 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_10/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_1 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1520 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_5 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_10/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1521 bank_0/port_address_0/wordline_driver_array_0/in_4 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_11/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1522 bank_0/port_address_0/wordline_driver_array_0/in_4 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_11/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1523 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_11/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/predecode_0 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1524 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_11/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_5 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_11/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1525 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_11/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_0 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1526 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_5 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_11/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1527 bank_0/port_address_0/wordline_driver_array_0/in_3 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_12/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1528 bank_0/port_address_0/wordline_driver_array_0/in_3 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_12/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1529 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_12/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/predecode_3 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1530 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_12/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_4 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_12/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1531 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_12/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_3 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1532 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_4 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_12/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1533 bank_0/port_address_0/wordline_driver_array_0/in_2 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_13/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1534 bank_0/port_address_0/wordline_driver_array_0/in_2 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_13/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1535 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_13/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/predecode_2 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1536 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_13/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_4 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_13/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1537 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_13/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_2 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1538 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_4 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_13/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1539 bank_0/port_address_0/wordline_driver_array_0/in_1 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_14/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1540 bank_0/port_address_0/wordline_driver_array_0/in_1 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_14/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1541 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_14/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/predecode_1 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1542 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_14/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_4 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_14/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1543 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_14/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_1 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1544 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_4 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_14/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1545 bank_0/port_address_0/wordline_driver_array_0/in_0 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_15/pinv_0/A vdd vdd p w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1546 bank_0/port_address_0/wordline_driver_array_0/in_0 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_15/pinv_0/A gnd gnd n w=0.8u l=0.4u
+  ad=0.960625p pd=4.025u as=0p ps=0u
M1547 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_15/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/hierarchical_decoder_0/predecode_0 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1548 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_15/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_4 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_15/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1549 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_15/pinv_0/A bank_0/port_address_0/hierarchical_decoder_0/predecode_0 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1550 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_4 bank_0/port_address_0/hierarchical_decoder_0/and2_dec_15/pinv_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1551 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_10/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/wordline_driver_array_0/in_5 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1552 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_10/pinv_0_0/A bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_10/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1553 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_10/pinv_0_0/A bank_0/port_address_0/wordline_driver_array_0/in_5 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1554 vdd bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_10/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1555 bank_0/port_address_0/wl_5 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_10/pinv_0_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1556 bank_0/port_address_0/wl_5 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_10/pinv_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1557 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_11/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/wordline_driver_array_0/in_4 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1558 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_11/pinv_0_0/A bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_11/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1559 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_11/pinv_0_0/A bank_0/port_address_0/wordline_driver_array_0/in_4 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1560 vdd bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_11/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1561 bank_0/port_address_0/wl_4 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_11/pinv_0_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1562 bank_0/port_address_0/wl_4 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_11/pinv_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1563 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_12/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/wordline_driver_array_0/in_3 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1564 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_12/pinv_0_0/A bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_12/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1565 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_12/pinv_0_0/A bank_0/port_address_0/wordline_driver_array_0/in_3 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1566 vdd bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_12/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1567 bank_0/port_address_0/wl_3 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_12/pinv_0_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1568 bank_0/port_address_0/wl_3 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_12/pinv_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1569 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_13/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/wordline_driver_array_0/in_2 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1570 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_13/pinv_0_0/A bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_13/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1571 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_13/pinv_0_0/A bank_0/port_address_0/wordline_driver_array_0/in_2 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1572 vdd bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_13/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1573 bank_0/port_address_0/wl_2 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_13/pinv_0_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1574 bank_0/port_address_0/wl_2 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_13/pinv_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1575 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_14/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/wordline_driver_array_0/in_1 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1576 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_14/pinv_0_0/A bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_14/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1577 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_14/pinv_0_0/A bank_0/port_address_0/wordline_driver_array_0/in_1 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1578 vdd bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_14/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1579 bank_0/port_address_0/wl_1 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_14/pinv_0_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1580 bank_0/port_address_0/wl_1 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_14/pinv_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1581 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_15/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/wordline_driver_array_0/in_0 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1582 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_15/pinv_0_0/A bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_15/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1583 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_15/pinv_0_0/A bank_0/port_address_0/wordline_driver_array_0/in_0 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1584 vdd bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_15/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1585 bank_0/port_address_0/wl_0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_15/pinv_0_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1586 bank_0/port_address_0/wl_0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_15/pinv_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1587 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_0/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/wordline_driver_array_0/in_15 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1588 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_0/pinv_0_0/A bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_0/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1589 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_0/pinv_0_0/A bank_0/port_address_0/wordline_driver_array_0/in_15 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1590 vdd bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_0/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1591 bank_0/port_address_0/wl_15 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_0/pinv_0_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1592 bank_0/port_address_0/wl_15 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_0/pinv_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1593 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_1/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/wordline_driver_array_0/in_14 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1594 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_1/pinv_0_0/A bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_1/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1595 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_1/pinv_0_0/A bank_0/port_address_0/wordline_driver_array_0/in_14 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1596 vdd bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_1/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1597 bank_0/port_address_0/wl_14 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_1/pinv_0_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1598 bank_0/port_address_0/wl_14 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_1/pinv_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1599 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_2/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/wordline_driver_array_0/in_13 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1600 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_2/pinv_0_0/A bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_2/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1601 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_2/pinv_0_0/A bank_0/port_address_0/wordline_driver_array_0/in_13 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1602 vdd bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_2/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1603 bank_0/port_address_0/wl_13 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_2/pinv_0_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1604 bank_0/port_address_0/wl_13 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_2/pinv_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1605 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_3/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/wordline_driver_array_0/in_12 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1606 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_3/pinv_0_0/A bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_3/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1607 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_3/pinv_0_0/A bank_0/port_address_0/wordline_driver_array_0/in_12 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1608 vdd bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_3/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1609 bank_0/port_address_0/wl_12 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_3/pinv_0_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1610 bank_0/port_address_0/wl_12 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_3/pinv_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1611 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_4/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/wordline_driver_array_0/in_11 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1612 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_4/pinv_0_0/A bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_4/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1613 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_4/pinv_0_0/A bank_0/port_address_0/wordline_driver_array_0/in_11 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1614 vdd bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_4/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1615 bank_0/port_address_0/wl_11 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_4/pinv_0_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1616 bank_0/port_address_0/wl_11 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_4/pinv_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1617 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_5/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/wordline_driver_array_0/in_10 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1618 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_5/pinv_0_0/A bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_5/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1619 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_5/pinv_0_0/A bank_0/port_address_0/wordline_driver_array_0/in_10 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1620 vdd bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_5/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1621 bank_0/port_address_0/wl_10 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_5/pinv_0_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1622 bank_0/port_address_0/wl_10 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_5/pinv_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1623 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_6/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/wordline_driver_array_0/in_9 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1624 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_6/pinv_0_0/A bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_6/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1625 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_6/pinv_0_0/A bank_0/port_address_0/wordline_driver_array_0/in_9 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1626 vdd bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_6/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1627 bank_0/port_address_0/wl_9 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_6/pinv_0_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1628 bank_0/port_address_0/wl_9 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_6/pinv_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1629 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_7/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/wordline_driver_array_0/in_8 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1630 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_7/pinv_0_0/A bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_7/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1631 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_7/pinv_0_0/A bank_0/port_address_0/wordline_driver_array_0/in_8 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1632 vdd bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_7/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1633 bank_0/port_address_0/wl_8 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_7/pinv_0_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1634 bank_0/port_address_0/wl_8 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_7/pinv_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1635 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_8/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/wordline_driver_array_0/in_7 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1636 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_8/pinv_0_0/A bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_8/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1637 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_8/pinv_0_0/A bank_0/port_address_0/wordline_driver_array_0/in_7 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1638 vdd bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_8/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1639 bank_0/port_address_0/wl_7 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_8/pinv_0_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1640 bank_0/port_address_0/wl_7 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_8/pinv_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1641 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_9/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S bank_0/port_address_0/wordline_driver_array_0/in_6 gnd gnd n w=1.6u l=0.4u
+  ad=2.56063p pd=6.425u as=0p ps=0u
M1642 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_9/pinv_0_0/A bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_9/pnand2_0/nmos_m1_w1_600_sactive_dm1_0/S gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1643 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_9/pinv_0_0/A bank_0/port_address_0/wordline_driver_array_0/in_6 vdd vdd p w=1.6u l=0.4u
+  ad=2.56188p pd=6.475u as=0p ps=0u
M1644 vdd bank_0/wl_en0 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_9/pinv_0_0/A vdd p w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1645 bank_0/port_address_0/wl_6 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_9/pinv_0_0/A vdd vdd p w=3.2u l=0.4u
+  ad=3.84063p pd=8.825u as=0p ps=0u
M1646 bank_0/port_address_0/wl_6 bank_0/port_address_0/wordline_driver_array_0/wordline_driver_9/pinv_0_0/A gnd gnd n w=1.6u l=0.4u
+  ad=1.92063p pd=5.625u as=0p ps=0u
M1647 gnd bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_0/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1648 bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_0/a_56_112# bank_0/replica_bitcell_array_0/dummy_array_0/wl_0 bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_0/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1649 bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_0/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1650 bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_0/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1651 vdd bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_0/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1652 bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0/wl_0 bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_0/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1653 gnd bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_1/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1654 bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_1/a_56_112# bank_0/replica_bitcell_array_0/dummy_array_0/wl_0 bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_1/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1655 bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_1/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1656 bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_1/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1657 vdd bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_1/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1658 bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0/wl_0 bank_0/replica_bitcell_array_0/dummy_array_0/dummy_cell_6t_1/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1659 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_1/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=176.483p ps=800.9u
M1660 vdd bank_0/port_address_0/wl_14 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=13.6p ps=61.2u
M1661 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_1/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1662 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_1/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1663 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_1/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1664 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_1/Q bank_0/port_address_0/wl_14 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=13.6p ps=61.2u
M1665 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_0/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1666 vdd bank_0/port_address_0/wl_15 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1667 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_0/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1668 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_0/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1669 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_0/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1670 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_0/Q bank_0/port_address_0/wl_15 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1671 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_2/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1672 vdd bank_0/port_address_0/wl_13 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1673 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_2/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1674 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_2/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1675 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_2/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1676 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_2/Q bank_0/port_address_0/wl_13 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1677 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_3/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1678 vdd bank_0/port_address_0/wl_12 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1679 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_3/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1680 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_3/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1681 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_3/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1682 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_3/Q bank_0/port_address_0/wl_12 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1683 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_10/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1684 vdd bank_0/port_address_0/wl_5 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1685 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_10/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1686 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_10/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1687 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_10/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1688 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_10/Q bank_0/port_address_0/wl_5 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1689 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_4/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1690 vdd bank_0/port_address_0/wl_11 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1691 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_4/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1692 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_4/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1693 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_4/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1694 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_4/Q bank_0/port_address_0/wl_11 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1695 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_11/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1696 vdd bank_0/port_address_0/wl_4 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1697 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_11/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1698 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_11/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1699 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_11/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1700 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_11/Q bank_0/port_address_0/wl_4 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1701 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_12/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1702 vdd bank_0/port_address_0/wl_3 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1703 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_12/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1704 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_12/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1705 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_12/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1706 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_12/Q bank_0/port_address_0/wl_3 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1707 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_5/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1708 vdd bank_0/port_address_0/wl_10 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1709 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_5/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1710 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_5/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1711 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_5/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1712 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_5/Q bank_0/port_address_0/wl_10 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1713 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_13/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1714 vdd bank_0/port_address_0/wl_2 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1715 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_13/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1716 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_13/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1717 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_13/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1718 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_13/Q bank_0/port_address_0/wl_2 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1719 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_6/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1720 vdd bank_0/port_address_0/wl_9 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1721 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_6/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1722 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_6/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1723 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_6/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1724 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_6/Q bank_0/port_address_0/wl_9 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1725 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_14/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1726 vdd bank_0/port_address_0/wl_1 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1727 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_14/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1728 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_14/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1729 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_14/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1730 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_14/Q bank_0/port_address_0/wl_1 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1731 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_7/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1732 vdd bank_0/port_address_0/wl_8 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1733 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_7/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1734 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_7/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1735 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_7/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1736 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_7/Q bank_0/port_address_0/wl_8 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1737 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_15/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1738 vdd bank_0/port_address_0/wl_0 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1739 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_15/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1740 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_15/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1741 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_15/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1742 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_15/Q bank_0/port_address_0/wl_0 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1743 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_8/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1744 vdd bank_0/port_address_0/wl_7 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1745 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_8/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1746 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_8/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1747 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_8/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1748 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_8/Q bank_0/port_address_0/wl_7 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1749 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_16/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1750 vdd bank_0/wl_en0 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1751 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_16/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1752 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_16/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1753 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_16/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1754 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_16/Q bank_0/wl_en0 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1755 gnd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_9/Q vdd gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1756 vdd bank_0/port_address_0/wl_6 bank_0/port_data_0/rbl_br gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1757 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_9/Q vdd gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1758 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_9/Q vdd vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1759 vdd bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_9/Q vdd vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0p ps=0u
M1760 bank_0/replica_bitcell_array_0/replica_column_0/replica_cell_6t_9/Q bank_0/port_address_0/wl_6 rbl_bl0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1761 gnd bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_0/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1762 bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_0/a_56_112# bank_0/replica_bitcell_array_0/dummy_array_0/wl_0 bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_0/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1763 bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_0/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1764 bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_0/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1765 vdd bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_0/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1766 bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0/wl_0 bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_0/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1767 gnd bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_1/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1768 bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_1/a_56_112# bank_0/replica_bitcell_array_0/dummy_array_1/wl_0 bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_1/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1769 bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_1/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1770 bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_1/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1771 vdd bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_1/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1772 bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1/wl_0 bank_0/replica_bitcell_array_0/replica_column_0/dummy_cell_6t_1/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1773 gnd bitcell_Q_b0_r15_c1 bitcell_Q_bar_b0_r15_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1774 bitcell_Q_bar_b0_r15_c1 bank_0/port_address_0/wl_15 br0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1775 bitcell_Q_b0_r15_c1 bitcell_Q_bar_b0_r15_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1776 bitcell_Q_b0_r15_c1 bitcell_Q_bar_b0_r15_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1777 vdd bitcell_Q_b0_r15_c1 bitcell_Q_bar_b0_r15_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1778 bitcell_Q_b0_r15_c1 bank_0/port_address_0/wl_15 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1779 gnd bitcell_Q_b0_r14_c1 bitcell_Q_bar_b0_r14_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1780 bitcell_Q_bar_b0_r14_c1 bank_0/port_address_0/wl_14 br0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1781 bitcell_Q_b0_r14_c1 bitcell_Q_bar_b0_r14_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1782 bitcell_Q_b0_r14_c1 bitcell_Q_bar_b0_r14_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1783 vdd bitcell_Q_b0_r14_c1 bitcell_Q_bar_b0_r14_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1784 bitcell_Q_b0_r14_c1 bank_0/port_address_0/wl_14 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1785 gnd bitcell_Q_b0_r13_c1 bitcell_Q_bar_b0_r13_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1786 bitcell_Q_bar_b0_r13_c1 bank_0/port_address_0/wl_13 br0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1787 bitcell_Q_b0_r13_c1 bitcell_Q_bar_b0_r13_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1788 bitcell_Q_b0_r13_c1 bitcell_Q_bar_b0_r13_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1789 vdd bitcell_Q_b0_r13_c1 bitcell_Q_bar_b0_r13_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1790 bitcell_Q_b0_r13_c1 bank_0/port_address_0/wl_13 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1791 gnd bitcell_Q_b0_r12_c1 bitcell_Q_bar_b0_r12_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1792 bitcell_Q_bar_b0_r12_c1 bank_0/port_address_0/wl_12 br0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1793 bitcell_Q_b0_r12_c1 bitcell_Q_bar_b0_r12_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1794 bitcell_Q_b0_r12_c1 bitcell_Q_bar_b0_r12_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1795 vdd bitcell_Q_b0_r12_c1 bitcell_Q_bar_b0_r12_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1796 bitcell_Q_b0_r12_c1 bank_0/port_address_0/wl_12 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1797 gnd bitcell_Q_b0_r11_c1 bitcell_Q_bar_b0_r11_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1798 bitcell_Q_bar_b0_r11_c1 bank_0/port_address_0/wl_11 br0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1799 bitcell_Q_b0_r11_c1 bitcell_Q_bar_b0_r11_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1800 bitcell_Q_b0_r11_c1 bitcell_Q_bar_b0_r11_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1801 vdd bitcell_Q_b0_r11_c1 bitcell_Q_bar_b0_r11_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1802 bitcell_Q_b0_r11_c1 bank_0/port_address_0/wl_11 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1803 gnd bitcell_Q_b0_r10_c1 bitcell_Q_bar_b0_r10_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1804 bitcell_Q_bar_b0_r10_c1 bank_0/port_address_0/wl_10 br0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1805 bitcell_Q_b0_r10_c1 bitcell_Q_bar_b0_r10_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1806 bitcell_Q_b0_r10_c1 bitcell_Q_bar_b0_r10_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1807 vdd bitcell_Q_b0_r10_c1 bitcell_Q_bar_b0_r10_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1808 bitcell_Q_b0_r10_c1 bank_0/port_address_0/wl_10 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1809 gnd bitcell_Q_b0_r9_c1 bitcell_Q_bar_b0_r9_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1810 bitcell_Q_bar_b0_r9_c1 bank_0/port_address_0/wl_9 br0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1811 bitcell_Q_b0_r9_c1 bitcell_Q_bar_b0_r9_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1812 bitcell_Q_b0_r9_c1 bitcell_Q_bar_b0_r9_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1813 vdd bitcell_Q_b0_r9_c1 bitcell_Q_bar_b0_r9_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1814 bitcell_Q_b0_r9_c1 bank_0/port_address_0/wl_9 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1815 gnd bitcell_Q_b0_r8_c1 bitcell_Q_bar_b0_r8_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1816 bitcell_Q_bar_b0_r8_c1 bank_0/port_address_0/wl_8 br0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1817 bitcell_Q_b0_r8_c1 bitcell_Q_bar_b0_r8_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1818 bitcell_Q_b0_r8_c1 bitcell_Q_bar_b0_r8_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1819 vdd bitcell_Q_b0_r8_c1 bitcell_Q_bar_b0_r8_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1820 bitcell_Q_b0_r8_c1 bank_0/port_address_0/wl_8 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1821 gnd bitcell_Q_b0_r7_c1 bitcell_Q_bar_b0_r7_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1822 bitcell_Q_bar_b0_r7_c1 bank_0/port_address_0/wl_7 br0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1823 bitcell_Q_b0_r7_c1 bitcell_Q_bar_b0_r7_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1824 bitcell_Q_b0_r7_c1 bitcell_Q_bar_b0_r7_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1825 vdd bitcell_Q_b0_r7_c1 bitcell_Q_bar_b0_r7_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1826 bitcell_Q_b0_r7_c1 bank_0/port_address_0/wl_7 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1827 gnd bitcell_Q_b0_r6_c1 bitcell_Q_bar_b0_r6_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1828 bitcell_Q_bar_b0_r6_c1 bank_0/port_address_0/wl_6 br0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1829 bitcell_Q_b0_r6_c1 bitcell_Q_bar_b0_r6_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1830 bitcell_Q_b0_r6_c1 bitcell_Q_bar_b0_r6_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1831 vdd bitcell_Q_b0_r6_c1 bitcell_Q_bar_b0_r6_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1832 bitcell_Q_b0_r6_c1 bank_0/port_address_0/wl_6 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1833 gnd bitcell_Q_b0_r1_c0 bitcell_Q_bar_b0_r1_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1834 bitcell_Q_bar_b0_r1_c0 bank_0/port_address_0/wl_1 br0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1835 bitcell_Q_b0_r1_c0 bitcell_Q_bar_b0_r1_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1836 bitcell_Q_b0_r1_c0 bitcell_Q_bar_b0_r1_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1837 vdd bitcell_Q_b0_r1_c0 bitcell_Q_bar_b0_r1_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1838 bitcell_Q_b0_r1_c0 bank_0/port_address_0/wl_1 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1839 gnd bitcell_Q_b0_r11_c0 bitcell_Q_bar_b0_r11_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1840 bitcell_Q_bar_b0_r11_c0 bank_0/port_address_0/wl_11 br0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1841 bitcell_Q_b0_r11_c0 bitcell_Q_bar_b0_r11_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1842 bitcell_Q_b0_r11_c0 bitcell_Q_bar_b0_r11_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1843 vdd bitcell_Q_b0_r11_c0 bitcell_Q_bar_b0_r11_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1844 bitcell_Q_b0_r11_c0 bank_0/port_address_0/wl_11 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1845 gnd bitcell_Q_b0_r0_c0 bitcell_Q_bar_b0_r0_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1846 bitcell_Q_bar_b0_r0_c0 bank_0/port_address_0/wl_0 br0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1847 bitcell_Q_b0_r0_c0 bitcell_Q_bar_b0_r0_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1848 bitcell_Q_b0_r0_c0 bitcell_Q_bar_b0_r0_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1849 vdd bitcell_Q_b0_r0_c0 bitcell_Q_bar_b0_r0_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1850 bitcell_Q_b0_r0_c0 bank_0/port_address_0/wl_0 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1851 gnd bitcell_Q_b0_r10_c0 bitcell_Q_bar_b0_r10_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1852 bitcell_Q_bar_b0_r10_c0 bank_0/port_address_0/wl_10 br0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1853 bitcell_Q_b0_r10_c0 bitcell_Q_bar_b0_r10_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1854 bitcell_Q_b0_r10_c0 bitcell_Q_bar_b0_r10_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1855 vdd bitcell_Q_b0_r10_c0 bitcell_Q_bar_b0_r10_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1856 bitcell_Q_b0_r10_c0 bank_0/port_address_0/wl_10 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1857 gnd bitcell_Q_b0_r5_c1 bitcell_Q_bar_b0_r5_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1858 bitcell_Q_bar_b0_r5_c1 bank_0/port_address_0/wl_5 br0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1859 bitcell_Q_b0_r5_c1 bitcell_Q_bar_b0_r5_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1860 bitcell_Q_b0_r5_c1 bitcell_Q_bar_b0_r5_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1861 vdd bitcell_Q_b0_r5_c1 bitcell_Q_bar_b0_r5_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1862 bitcell_Q_b0_r5_c1 bank_0/port_address_0/wl_5 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1863 gnd bitcell_Q_b0_r9_c0 bitcell_Q_bar_b0_r9_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1864 bitcell_Q_bar_b0_r9_c0 bank_0/port_address_0/wl_9 br0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1865 bitcell_Q_b0_r9_c0 bitcell_Q_bar_b0_r9_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1866 bitcell_Q_b0_r9_c0 bitcell_Q_bar_b0_r9_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1867 vdd bitcell_Q_b0_r9_c0 bitcell_Q_bar_b0_r9_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1868 bitcell_Q_b0_r9_c0 bank_0/port_address_0/wl_9 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1869 gnd bitcell_Q_b0_r4_c1 bitcell_Q_bar_b0_r4_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1870 bitcell_Q_bar_b0_r4_c1 bank_0/port_address_0/wl_4 br0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1871 bitcell_Q_b0_r4_c1 bitcell_Q_bar_b0_r4_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1872 bitcell_Q_b0_r4_c1 bitcell_Q_bar_b0_r4_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1873 vdd bitcell_Q_b0_r4_c1 bitcell_Q_bar_b0_r4_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1874 bitcell_Q_b0_r4_c1 bank_0/port_address_0/wl_4 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1875 gnd bitcell_Q_b0_r8_c0 bitcell_Q_bar_b0_r8_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1876 bitcell_Q_bar_b0_r8_c0 bank_0/port_address_0/wl_8 br0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1877 bitcell_Q_b0_r8_c0 bitcell_Q_bar_b0_r8_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1878 bitcell_Q_b0_r8_c0 bitcell_Q_bar_b0_r8_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1879 vdd bitcell_Q_b0_r8_c0 bitcell_Q_bar_b0_r8_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1880 bitcell_Q_b0_r8_c0 bank_0/port_address_0/wl_8 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1881 gnd bitcell_Q_b0_r3_c1 bitcell_Q_bar_b0_r3_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1882 bitcell_Q_bar_b0_r3_c1 bank_0/port_address_0/wl_3 br0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1883 bitcell_Q_b0_r3_c1 bitcell_Q_bar_b0_r3_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1884 bitcell_Q_b0_r3_c1 bitcell_Q_bar_b0_r3_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1885 vdd bitcell_Q_b0_r3_c1 bitcell_Q_bar_b0_r3_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1886 bitcell_Q_b0_r3_c1 bank_0/port_address_0/wl_3 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1887 gnd bitcell_Q_b0_r7_c0 bitcell_Q_bar_b0_r7_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1888 bitcell_Q_bar_b0_r7_c0 bank_0/port_address_0/wl_7 br0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1889 bitcell_Q_b0_r7_c0 bitcell_Q_bar_b0_r7_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1890 bitcell_Q_b0_r7_c0 bitcell_Q_bar_b0_r7_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1891 vdd bitcell_Q_b0_r7_c0 bitcell_Q_bar_b0_r7_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1892 bitcell_Q_b0_r7_c0 bank_0/port_address_0/wl_7 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1893 gnd bitcell_Q_b0_r2_c1 bitcell_Q_bar_b0_r2_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1894 bitcell_Q_bar_b0_r2_c1 bank_0/port_address_0/wl_2 br0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1895 bitcell_Q_b0_r2_c1 bitcell_Q_bar_b0_r2_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1896 bitcell_Q_b0_r2_c1 bitcell_Q_bar_b0_r2_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1897 vdd bitcell_Q_b0_r2_c1 bitcell_Q_bar_b0_r2_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1898 bitcell_Q_b0_r2_c1 bank_0/port_address_0/wl_2 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1899 gnd bitcell_Q_b0_r6_c0 bitcell_Q_bar_b0_r6_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1900 bitcell_Q_bar_b0_r6_c0 bank_0/port_address_0/wl_6 br0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1901 bitcell_Q_b0_r6_c0 bitcell_Q_bar_b0_r6_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1902 bitcell_Q_b0_r6_c0 bitcell_Q_bar_b0_r6_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1903 vdd bitcell_Q_b0_r6_c0 bitcell_Q_bar_b0_r6_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1904 bitcell_Q_b0_r6_c0 bank_0/port_address_0/wl_6 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1905 gnd bitcell_Q_b0_r1_c1 bitcell_Q_bar_b0_r1_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1906 bitcell_Q_bar_b0_r1_c1 bank_0/port_address_0/wl_1 br0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1907 bitcell_Q_b0_r1_c1 bitcell_Q_bar_b0_r1_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1908 bitcell_Q_b0_r1_c1 bitcell_Q_bar_b0_r1_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1909 vdd bitcell_Q_b0_r1_c1 bitcell_Q_bar_b0_r1_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1910 bitcell_Q_b0_r1_c1 bank_0/port_address_0/wl_1 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1911 gnd bitcell_Q_b0_r5_c0 bitcell_Q_bar_b0_r5_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1912 bitcell_Q_bar_b0_r5_c0 bank_0/port_address_0/wl_5 br0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1913 bitcell_Q_b0_r5_c0 bitcell_Q_bar_b0_r5_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1914 bitcell_Q_b0_r5_c0 bitcell_Q_bar_b0_r5_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1915 vdd bitcell_Q_b0_r5_c0 bitcell_Q_bar_b0_r5_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1916 bitcell_Q_b0_r5_c0 bank_0/port_address_0/wl_5 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1917 gnd bitcell_Q_b0_r0_c1 bitcell_Q_bar_b0_r0_c1 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1918 bitcell_Q_bar_b0_r0_c1 bank_0/port_address_0/wl_0 br0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1919 bitcell_Q_b0_r0_c1 bitcell_Q_bar_b0_r0_c1 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1920 bitcell_Q_b0_r0_c1 bitcell_Q_bar_b0_r0_c1 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1921 vdd bitcell_Q_b0_r0_c1 bitcell_Q_bar_b0_r0_c1 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1922 bitcell_Q_b0_r0_c1 bank_0/port_address_0/wl_0 bl0_1 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1923 gnd bitcell_Q_b0_r15_c0 bitcell_Q_bar_b0_r15_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1924 bitcell_Q_bar_b0_r15_c0 bank_0/port_address_0/wl_15 br0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1925 bitcell_Q_b0_r15_c0 bitcell_Q_bar_b0_r15_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1926 bitcell_Q_b0_r15_c0 bitcell_Q_bar_b0_r15_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1927 vdd bitcell_Q_b0_r15_c0 bitcell_Q_bar_b0_r15_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1928 bitcell_Q_b0_r15_c0 bank_0/port_address_0/wl_15 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1929 gnd bitcell_Q_b0_r14_c0 bitcell_Q_bar_b0_r14_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1930 bitcell_Q_bar_b0_r14_c0 bank_0/port_address_0/wl_14 br0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1931 bitcell_Q_b0_r14_c0 bitcell_Q_bar_b0_r14_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1932 bitcell_Q_b0_r14_c0 bitcell_Q_bar_b0_r14_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1933 vdd bitcell_Q_b0_r14_c0 bitcell_Q_bar_b0_r14_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1934 bitcell_Q_b0_r14_c0 bank_0/port_address_0/wl_14 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1935 gnd bitcell_Q_b0_r4_c0 bitcell_Q_bar_b0_r4_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1936 bitcell_Q_bar_b0_r4_c0 bank_0/port_address_0/wl_4 br0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1937 bitcell_Q_b0_r4_c0 bitcell_Q_bar_b0_r4_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1938 bitcell_Q_b0_r4_c0 bitcell_Q_bar_b0_r4_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1939 vdd bitcell_Q_b0_r4_c0 bitcell_Q_bar_b0_r4_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1940 bitcell_Q_b0_r4_c0 bank_0/port_address_0/wl_4 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1941 gnd bitcell_Q_b0_r3_c0 bitcell_Q_bar_b0_r3_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1942 bitcell_Q_bar_b0_r3_c0 bank_0/port_address_0/wl_3 br0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1943 bitcell_Q_b0_r3_c0 bitcell_Q_bar_b0_r3_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1944 bitcell_Q_b0_r3_c0 bitcell_Q_bar_b0_r3_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1945 vdd bitcell_Q_b0_r3_c0 bitcell_Q_bar_b0_r3_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1946 bitcell_Q_b0_r3_c0 bank_0/port_address_0/wl_3 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1947 gnd bitcell_Q_b0_r13_c0 bitcell_Q_bar_b0_r13_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1948 bitcell_Q_bar_b0_r13_c0 bank_0/port_address_0/wl_13 br0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1949 bitcell_Q_b0_r13_c0 bitcell_Q_bar_b0_r13_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1950 bitcell_Q_b0_r13_c0 bitcell_Q_bar_b0_r13_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1951 vdd bitcell_Q_b0_r13_c0 bitcell_Q_bar_b0_r13_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1952 bitcell_Q_b0_r13_c0 bank_0/port_address_0/wl_13 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1953 gnd bitcell_Q_b0_r2_c0 bitcell_Q_bar_b0_r2_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1954 bitcell_Q_bar_b0_r2_c0 bank_0/port_address_0/wl_2 br0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1955 bitcell_Q_b0_r2_c0 bitcell_Q_bar_b0_r2_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1956 bitcell_Q_b0_r2_c0 bitcell_Q_bar_b0_r2_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1957 vdd bitcell_Q_b0_r2_c0 bitcell_Q_bar_b0_r2_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1958 bitcell_Q_b0_r2_c0 bank_0/port_address_0/wl_2 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1959 gnd bitcell_Q_b0_r12_c0 bitcell_Q_bar_b0_r12_c0 gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1960 bitcell_Q_bar_b0_r12_c0 bank_0/port_address_0/wl_12 br0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1961 bitcell_Q_b0_r12_c0 bitcell_Q_bar_b0_r12_c0 gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1962 bitcell_Q_b0_r12_c0 bitcell_Q_bar_b0_r12_c0 vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1963 vdd bitcell_Q_b0_r12_c0 bitcell_Q_bar_b0_r12_c0 vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1964 bitcell_Q_b0_r12_c0 bank_0/port_address_0/wl_12 bl0_0 gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0p ps=0u
M1965 gnd bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_0/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1966 bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_0/a_56_112# bank_0/replica_bitcell_array_0/dummy_array_1/wl_0 bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_0/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1967 bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_0/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1968 bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_0/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1969 vdd bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_0/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1970 bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1/wl_0 bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_0/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1971 gnd bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_1/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1972 bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_1/a_56_112# bank_0/replica_bitcell_array_0/dummy_array_1/wl_0 bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_1/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1973 bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_1/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1974 bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_1/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1975 vdd bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_1/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1976 bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1/wl_0 bank_0/replica_bitcell_array_0/dummy_array_1/dummy_cell_6t_1/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1977 gnd bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_0/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1978 bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_0/a_56_112# bank_0/wl_en0 bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_0/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1979 bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_0/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1980 bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_0/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1981 vdd bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_0/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1982 bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_0/a_72_128# bank_0/wl_en0 bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_0/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1983 gnd bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_1/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1984 bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_1/a_56_112# bank_0/wl_en0 bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_1/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1985 bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_1/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1986 bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_1/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1987 vdd bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_1/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1988 bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_1/a_72_128# bank_0/wl_en0 bank_0/replica_bitcell_array_0/dummy_array_2/dummy_cell_6t_1/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1989 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_2/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_2/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1990 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_2/a_56_112# bank_0/port_address_0/wl_14 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_2/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1991 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_2/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_2/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1992 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_2/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_2/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1993 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_2/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_2/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M1994 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_2/a_72_128# bank_0/port_address_0/wl_14 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_2/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1995 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_3/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_3/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M1996 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_3/a_56_112# bank_0/port_address_0/wl_13 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_3/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M1997 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_3/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_3/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M1998 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_3/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_3/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M1999 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_3/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_3/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2000 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_3/a_72_128# bank_0/port_address_0/wl_13 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_3/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2001 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_4/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_4/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2002 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_4/a_56_112# bank_0/port_address_0/wl_12 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_4/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2003 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_4/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_4/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2004 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_4/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_4/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2005 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_4/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_4/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2006 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_4/a_72_128# bank_0/port_address_0/wl_12 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_4/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2007 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_5/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_5/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2008 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_5/a_56_112# bank_0/port_address_0/wl_11 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_5/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2009 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_5/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_5/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2010 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_5/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_5/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2011 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_5/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_5/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2012 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_5/a_72_128# bank_0/port_address_0/wl_11 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_5/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2013 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_6/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_6/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2014 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_6/a_56_112# bank_0/port_address_0/wl_10 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_6/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2015 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_6/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_6/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2016 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_6/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_6/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2017 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_6/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_6/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2018 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_6/a_72_128# bank_0/port_address_0/wl_10 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_6/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2019 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_7/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_7/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2020 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_7/a_56_112# bank_0/port_address_0/wl_9 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_7/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2021 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_7/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_7/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2022 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_7/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_7/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2023 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_7/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_7/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2024 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_7/a_72_128# bank_0/port_address_0/wl_9 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_7/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2025 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_8/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_8/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2026 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_8/a_56_112# bank_0/port_address_0/wl_8 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_8/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2027 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_8/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_8/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2028 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_8/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_8/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2029 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_8/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_8/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2030 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_8/a_72_128# bank_0/port_address_0/wl_8 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_8/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2031 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_9/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_9/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2032 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_9/a_56_112# bank_0/port_address_0/wl_7 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_9/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2033 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_9/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_9/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2034 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_9/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_9/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2035 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_9/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_9/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2036 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_9/a_72_128# bank_0/port_address_0/wl_7 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_9/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2037 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_10/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_10/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2038 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_10/a_56_112# bank_0/port_address_0/wl_6 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_10/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2039 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_10/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_10/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2040 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_10/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_10/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2041 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_10/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_10/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2042 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_10/a_72_128# bank_0/port_address_0/wl_6 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_10/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2043 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_11/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_11/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2044 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_11/a_56_112# bank_0/port_address_0/wl_5 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_11/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2045 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_11/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_11/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2046 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_11/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_11/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2047 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_11/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_11/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2048 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_11/a_72_128# bank_0/port_address_0/wl_5 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_11/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2049 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_12/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_12/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2050 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_12/a_56_112# bank_0/port_address_0/wl_4 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_12/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2051 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_12/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_12/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2052 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_12/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_12/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2053 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_12/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_12/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2054 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_12/a_72_128# bank_0/port_address_0/wl_4 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_12/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2055 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_13/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_13/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2056 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_13/a_56_112# bank_0/port_address_0/wl_3 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_13/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2057 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_13/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_13/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2058 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_13/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_13/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2059 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_13/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_13/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2060 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_13/a_72_128# bank_0/port_address_0/wl_3 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_13/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2061 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_14/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_14/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2062 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_14/a_56_112# bank_0/port_address_0/wl_2 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_14/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2063 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_14/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_14/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2064 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_14/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_14/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2065 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_14/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_14/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2066 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_14/a_72_128# bank_0/port_address_0/wl_2 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_14/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2067 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_15/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_15/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2068 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_15/a_56_112# bank_0/port_address_0/wl_1 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_15/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2069 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_15/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_15/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2070 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_15/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_15/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2071 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_15/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_15/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2072 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_15/a_72_128# bank_0/port_address_0/wl_1 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_15/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2073 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_16/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_16/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2074 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_16/a_56_112# bank_0/port_address_0/wl_0 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_16/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2075 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_16/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_16/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2076 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_16/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_16/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2077 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_16/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_16/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2078 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_16/a_72_128# bank_0/port_address_0/wl_0 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_16/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2079 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_17/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_17/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2080 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_17/a_56_112# bank_0/wl_en0 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_17/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2081 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_17/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_17/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2082 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_17/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_17/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2083 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_17/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_17/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2084 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_17/a_72_128# bank_0/wl_en0 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_17/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2085 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_18/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_18/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2086 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_18/a_56_112# bank_0/replica_bitcell_array_0/dummy_array_1/wl_0 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_18/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2087 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_18/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_18/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2088 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_18/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_18/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2089 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_18/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_18/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2090 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_18/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1/wl_0 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_18/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2091 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_0/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2092 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_0/a_56_112# bank_0/replica_bitcell_array_0/dummy_array_0/wl_0 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_0/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2093 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_0/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2094 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_0/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2095 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_0/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2096 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0/wl_0 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_0/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2097 gnd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_1/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2098 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_1/a_56_112# bank_0/port_address_0/wl_15 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_1/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2099 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_1/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2100 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_1/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2101 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_1/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2102 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_1/a_72_128# bank_0/port_address_0/wl_15 bank_0/replica_bitcell_array_0/dummy_array_1_0/dummy_cell_6t_1/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2103 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_2/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_2/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2104 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_2/a_56_112# bank_0/port_address_0/wl_14 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_2/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2105 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_2/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_2/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2106 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_2/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_2/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2107 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_2/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_2/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2108 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_2/a_72_128# bank_0/port_address_0/wl_14 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_2/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2109 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_3/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_3/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2110 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_3/a_56_112# bank_0/port_address_0/wl_13 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_3/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2111 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_3/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_3/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2112 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_3/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_3/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2113 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_3/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_3/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2114 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_3/a_72_128# bank_0/port_address_0/wl_13 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_3/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2115 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_4/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_4/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2116 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_4/a_56_112# bank_0/port_address_0/wl_12 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_4/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2117 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_4/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_4/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2118 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_4/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_4/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2119 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_4/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_4/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2120 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_4/a_72_128# bank_0/port_address_0/wl_12 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_4/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2121 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_5/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_5/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2122 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_5/a_56_112# bank_0/port_address_0/wl_11 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_5/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2123 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_5/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_5/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2124 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_5/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_5/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2125 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_5/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_5/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2126 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_5/a_72_128# bank_0/port_address_0/wl_11 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_5/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2127 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_6/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_6/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2128 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_6/a_56_112# bank_0/port_address_0/wl_10 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_6/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2129 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_6/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_6/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2130 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_6/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_6/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2131 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_6/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_6/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2132 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_6/a_72_128# bank_0/port_address_0/wl_10 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_6/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2133 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_7/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_7/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2134 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_7/a_56_112# bank_0/port_address_0/wl_9 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_7/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2135 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_7/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_7/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2136 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_7/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_7/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2137 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_7/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_7/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2138 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_7/a_72_128# bank_0/port_address_0/wl_9 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_7/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2139 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_8/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_8/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2140 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_8/a_56_112# bank_0/port_address_0/wl_8 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_8/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2141 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_8/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_8/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2142 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_8/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_8/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2143 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_8/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_8/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2144 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_8/a_72_128# bank_0/port_address_0/wl_8 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_8/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2145 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_9/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_9/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2146 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_9/a_56_112# bank_0/port_address_0/wl_7 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_9/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2147 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_9/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_9/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2148 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_9/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_9/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2149 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_9/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_9/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2150 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_9/a_72_128# bank_0/port_address_0/wl_7 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_9/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2151 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_10/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_10/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2152 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_10/a_56_112# bank_0/port_address_0/wl_6 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_10/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2153 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_10/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_10/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2154 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_10/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_10/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2155 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_10/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_10/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2156 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_10/a_72_128# bank_0/port_address_0/wl_6 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_10/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2157 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_11/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_11/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2158 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_11/a_56_112# bank_0/port_address_0/wl_5 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_11/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2159 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_11/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_11/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2160 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_11/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_11/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2161 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_11/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_11/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2162 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_11/a_72_128# bank_0/port_address_0/wl_5 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_11/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2163 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_12/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_12/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2164 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_12/a_56_112# bank_0/port_address_0/wl_4 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_12/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2165 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_12/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_12/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2166 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_12/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_12/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2167 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_12/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_12/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2168 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_12/a_72_128# bank_0/port_address_0/wl_4 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_12/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2169 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_13/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_13/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2170 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_13/a_56_112# bank_0/port_address_0/wl_3 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_13/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2171 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_13/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_13/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2172 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_13/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_13/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2173 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_13/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_13/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2174 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_13/a_72_128# bank_0/port_address_0/wl_3 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_13/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2175 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_14/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_14/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2176 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_14/a_56_112# bank_0/port_address_0/wl_2 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_14/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2177 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_14/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_14/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2178 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_14/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_14/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2179 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_14/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_14/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2180 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_14/a_72_128# bank_0/port_address_0/wl_2 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_14/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2181 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_15/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_15/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2182 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_15/a_56_112# bank_0/port_address_0/wl_1 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_15/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2183 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_15/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_15/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2184 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_15/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_15/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2185 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_15/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_15/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2186 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_15/a_72_128# bank_0/port_address_0/wl_1 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_15/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2187 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_16/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_16/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2188 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_16/a_56_112# bank_0/port_address_0/wl_0 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_16/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2189 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_16/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_16/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2190 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_16/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_16/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2191 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_16/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_16/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2192 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_16/a_72_128# bank_0/port_address_0/wl_0 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_16/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2193 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_17/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_17/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2194 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_17/a_56_112# bank_0/wl_en0 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_17/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2195 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_17/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_17/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2196 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_17/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_17/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2197 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_17/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_17/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2198 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_17/a_72_128# bank_0/wl_en0 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_17/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2199 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_18/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_18/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2200 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_18/a_56_112# bank_0/replica_bitcell_array_0/dummy_array_1/wl_0 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_18/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2201 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_18/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_18/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2202 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_18/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_18/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2203 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_18/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_18/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2204 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_18/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_1/wl_0 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_18/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2205 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_0/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2206 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_0/a_56_112# bank_0/replica_bitcell_array_0/dummy_array_0/wl_0 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_0/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2207 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_0/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2208 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_0/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2209 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_0/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2210 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_0/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0/wl_0 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_0/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2211 gnd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_1/a_56_112# gnd n w=1.6u l=0.4u
+  ad=0p pd=0u as=2.4p ps=7.2u
M2212 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_1/a_56_112# bank_0/port_address_0/wl_15 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_1/a_192_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
M2213 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_1/a_56_112# gnd gnd n w=1.6u l=0.4u
+  ad=2.4p pd=7.2u as=0p ps=0u
M2214 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_1/a_56_112# vdd vdd p w=0.6u l=0.8u
+  ad=0.76p pd=3.6u as=0p ps=0u
M2215 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_1/a_72_128# bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_1/a_56_112# vdd p w=0.6u l=0.8u
+  ad=0p pd=0u as=0.76p ps=3.6u
M2216 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_1/a_72_128# bank_0/port_address_0/wl_15 bank_0/replica_bitcell_array_0/dummy_array_0_0/dummy_cell_6t_1/a_80_32# gnd n w=0.8u l=0.4u
+  ad=0p pd=0u as=0.8p ps=3.6u
C0 control_logic_rw_0/pand3_0/B control_logic_rw_0/pinv_4_0/A 9.82fF
C1 control_logic_rw_0/pand2_1/Z control_logic_rw_0/pinv_4_0/A 10.44fF
C2 vdd control_logic_rw_0/delay_chain_0/pinv_12_39/A 6.84fF
C3 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/br_0 3.80fF
C4 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_48_48# vdd 2.83fF
C5 vdd control_logic_rw_0/delay_chain_0/pinv_12_4/A 6.39fF
C6 bank_0/port_address_0/hierarchical_decoder_0/predecode_6 bank_0/port_address_0/hierarchical_decoder_0/predecode_5 10.13fF
C7 bank_0/s_en0 bank_0/w_en0 6.93fF
C8 vdd bank_0/addr0_1 10.70fF
C9 control_logic_rw_0/delay_chain_0/pinv_12_9/A vdd 6.84fF
C10 bank_0/port_address_0/hierarchical_decoder_0/predecode_7 bank_0/port_address_0/hierarchical_decoder_0/predecode_6 10.13fF
C11 control_logic_rw_0/pand2_0/B data_dff_0/clk 9.79fF
C12 bank_0/port_address_0/hierarchical_decoder_0/predecode_2 bank_0/port_address_0/hierarchical_decoder_0/predecode_1 10.16fF
C13 vdd bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_1/Z 2.00fF
C14 bank_0/port_address_0/hierarchical_decoder_0/predecode_1 bank_0/port_address_0/hierarchical_decoder_0/predecode_0 10.36fF
C15 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_0/Z bank_0/addr0_2 2.51fF
C16 bank_0/s_en0 vdd 9.67fF
C17 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_1 6.30fF
C18 bank_0/addr0_1 bank_0/addr0_0 14.92fF
C19 bank_0/port_address_0/hierarchical_decoder_0/predecode_5 bank_0/port_address_0/hierarchical_decoder_0/predecode_4 10.13fF
C20 vdd bl0_0 6.40fF
C21 vdd row_addr_dff_0/dff_3/a_48_48# 2.85fF
C22 data_dff_0/dff_0/a_48_48# vdd 2.76fF
C23 vdd control_logic_rw_0/pinv_4_0/A 16.35fF
C24 control_logic_rw_0/delay_chain_0/pinv_12_29/A vdd 7.80fF
C25 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_48_48# vdd 2.91fF
C26 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_304_32# vdd 2.35fF
C27 bank_0/din0_0 bank_0/din0_1 2.62fF
C28 control_logic_rw_0/pand3_0/B vdd 2.56fF
C29 data_dff_0/dff_1/a_48_48# vdd 2.91fF
C30 control_logic_rw_0/pand2_1/Z vdd 6.99fF
C31 control_logic_rw_0/pand3_0_0/C vdd 5.55fF
C32 vdd bank_0/addr0_3 9.15fF
C33 vdd row_addr_dff_0/dff_3/a_304_32# 2.30fF
C34 vdd bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_1/Z 2.00fF
C35 vdd dout0[1] 2.12fF
C36 control_logic_rw_0/delay_chain_0/pinv_12_34/A vdd 7.42fF
C37 vdd row_addr_dff_0/dff_2/a_48_48# 2.74fF
C38 control_logic_rw_0/pand3_0_0/C control_logic_rw_0/pand3_0/A 9.67fF
C39 bank_0/w_en0 vdd 7.71fF
C40 control_logic_rw_0/pand2_1/Z control_logic_rw_0/pand2_0/Z 9.72fF
C41 bank_0/port_address_0/hierarchical_decoder_0/predecode_3 bank_0/port_address_0/hierarchical_decoder_0/predecode_2 10.16fF
C42 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_2 3.59fF
C43 data_dff_0/dff_0/a_304_32# vdd 2.21fF
C44 bl0_1 br0_1 2.37fF
C45 vdd row_addr_dff_0/dff_2/a_304_32# 2.33fF
C46 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_0 3.39fF
C47 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_3 4.19fF
C48 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_304_32# vdd 2.26fF
C49 control_logic_rw_0/delay_chain_0/pinv_12_24/A vdd 6.35fF
C50 vdd bank_0/wl_en0 18.37fF
C51 data_dff_0/dff_1/a_304_32# vdd 2.25fF
C52 vdd rbl_bl0 11.72fF
C53 bank_0/addr0_2 bank_0/addr0_1 11.16fF
C54 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_0/Z bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_1/Z 2.52fF
C55 control_logic_rw_0/pand3_0/A vdd 6.74fF
C56 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_0/Z bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_1/Z 2.52fF
C57 vdd bank_0/addr0_0 7.60fF
C58 br0_0 bl0_0 2.37fF
C59 vdd row_addr_dff_0/dff_1/a_48_48# 2.71fF
C60 control_logic_rw_0/pand2_0/Z vdd 4.36fF
C61 vdd bank_0/port_data_0/rbl_br 14.37fF
C62 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_6 5.63fF
C63 control_logic_rw_0/pand3_0/A control_logic_rw_0/pand2_0/Z 9.67fF
C64 vdd bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_0/Z 3.24fF
C65 vdd row_addr_dff_0/dff_1/a_304_32# 2.36fF
C66 bank_0/addr0_3 bank_0/addr0_2 17.28fF
C67 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/Q vdd 2.82fF
C68 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_0/Z bank_0/addr0_0 2.51fF
C69 control_logic_rw_0/pand3_0_0/C data_dff_0/clk 9.63fF
C70 bank_0/port_address_0/hierarchical_decoder_0/predecode_3 bank_0/port_address_0/hierarchical_decoder_0/predecode_4 10.18fF
C71 vdd control_logic_rw_0/pnand2_1_0/Z 2.29fF
C72 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_4 5.68fF
C73 control_logic_rw_0/pand2_0/B vdd 6.34fF
C74 bank_0/w_en0 bank_0/p_en_bar0 6.95fF
C75 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/bl_0 6.95fF
C76 vdd br0_0 6.15fF
C77 vdd row_addr_dff_0/dff_0/a_48_48# 2.80fF
C78 bank_0/din0_0 vdd 4.01fF
C79 vdd bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_0/Z 3.24fF
C80 vdd bank_0/addr0_2 10.13fF
C81 bank_0/p_en_bar0 bank_0/wl_en0 7.00fF
C82 vdd bank_0/p_en_bar0 11.97fF
C83 vdd bank_0/replica_bitcell_array_0/dummy_array_1_0/bl_0 5.03fF
C84 vdd data_dff_0/clk 35.57fF
C85 vdd bl0_1 9.70fF
C86 control_logic_rw_0/delay_chain_0/pinv_12_19/A vdd 6.76fF
C87 bank_0/din0_1 vdd 4.69fF
C88 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/Q vdd 2.72fF
C89 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_5 8.11fF
C90 vdd bank_0/replica_bitcell_array_0/dummy_array_0_0/br_0 5.11fF
C91 data_dff_0/clk bank_0/addr0_0 6.56fF
C92 vdd br0_1 8.52fF
C93 vdd bank_0/port_address_0/hierarchical_decoder_0/predecode_7 6.74fF
C94 control_logic_rw_0/delay_chain_0/pinv_12_14/A vdd 6.41fF
C95 vdd row_addr_dff_0/dff_0/a_304_32# 2.25fF
C96 bank_0/replica_bitcell_array_0/dummy_array_0_0/br_0 gnd 19.78fF ; **FLOATING
C97 bank_0/replica_bitcell_array_0/dummy_array_0_0/bl_0 gnd 16.03fF ; **FLOATING
C98 bank_0/port_address_0/wl_0 gnd 5.54fF
C99 bank_0/port_address_0/wl_2 gnd 5.87fF
C100 bank_0/port_address_0/wl_4 gnd 5.48fF
C101 bank_0/port_address_0/wl_6 gnd 5.54fF
C102 bank_0/port_address_0/wl_8 gnd 5.87fF
C103 bank_0/port_address_0/wl_9 gnd 3.02fF
C104 bank_0/port_address_0/wl_10 gnd 5.48fF
C105 bank_0/port_address_0/wl_11 gnd 2.70fF
C106 bank_0/port_address_0/wl_12 gnd 5.54fF
C107 bank_0/port_address_0/wl_13 gnd 4.36fF
C108 bank_0/port_address_0/wl_14 gnd 5.87fF
C109 bank_0/replica_bitcell_array_0/dummy_array_1_0/br_0 gnd 15.46fF ; **FLOATING
C110 bank_0/replica_bitcell_array_0/dummy_array_1_0/bl_0 gnd 20.50fF ; **FLOATING
C111 bank_0/replica_bitcell_array_0/dummy_array_1/wl_0 gnd 5.08fF
C112 br0_1 gnd 10.29fF
C113 bl0_1 gnd 18.66fF
C114 br0_0 gnd 18.32fF
C115 bl0_0 gnd 21.69fF
C116 bank_0/port_data_0/rbl_br gnd 17.54fF
C117 rbl_bl0 gnd 23.95fF
C118 bank_0/replica_bitcell_array_0/dummy_array_0/wl_0 gnd 5.08fF
C119 bank_0/port_address_0/wl_15 gnd 4.77fF
C120 bank_0/wl_en0 gnd 17.66fF
C121 bank_0/port_address_0/hierarchical_decoder_0/predecode_0 gnd 10.16fF
C122 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_1/Z gnd 3.93fF
C123 bank_0/addr0_0 gnd 9.63fF
C124 bank_0/port_address_0/hierarchical_decoder_0/predecode_1 gnd 6.92fF
C125 bank_0/addr0_1 gnd 10.11fF
C126 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_1/pinv_0/Z gnd 3.86fF
C127 bank_0/port_address_0/hierarchical_decoder_0/predecode_2 gnd 7.11fF
C128 bank_0/port_address_0/hierarchical_decoder_0/predecode_4 gnd 7.00fF
C129 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_1/Z gnd 3.93fF
C130 bank_0/addr0_2 gnd 5.84fF
C131 bank_0/port_address_0/hierarchical_decoder_0/predecode_5 gnd 6.80fF
C132 bank_0/addr0_3 gnd 10.39fF
C133 bank_0/port_address_0/hierarchical_decoder_0/hierarchical_predecode2x4_0/pinv_0/Z gnd 3.86fF
C134 bank_0/port_address_0/hierarchical_decoder_0/predecode_6 gnd 7.19fF
C135 bank_0/port_address_0/hierarchical_decoder_0/predecode_7 gnd 5.71fF
C136 bank_0/port_address_0/hierarchical_decoder_0/predecode_3 gnd 9.20fF
C137 bank_0/p_en_bar0 gnd 7.00fF
C138 row_addr_dff_0/dff_3/a_48_48# gnd 2.39fF
C139 row_addr_dff_0/dff_2/a_48_48# gnd 2.54fF
C140 row_addr_dff_0/dff_1/a_48_48# gnd 2.56fF
C141 row_addr_dff_0/dff_0/a_48_48# gnd 2.44fF
C142 data_dff_0/clk gnd 35.58fF
C143 control_logic_rw_0/pand2_0/Z gnd 7.12fF
C144 control_logic_rw_0/delay_chain_0/pinv_12_39/A gnd 2.56fF
C145 control_logic_rw_0/delay_chain_0/pinv_12_4/A gnd 4.09fF
C146 control_logic_rw_0/pinv_4_0/A gnd 10.38fF
C147 vdd gnd 8559.44fF
C148 control_logic_rw_0/delay_chain_0/pinv_12_14/A gnd 3.15fF
C149 control_logic_rw_0/delay_chain_0/pinv_12_24/A gnd 2.83fF
C150 control_logic_rw_0/delay_chain_0/pinv_12_34/A gnd 2.95fF
C151 control_logic_rw_0/delay_chain_0/pinv_12_9/A gnd 2.69fF
C152 control_logic_rw_0/delay_chain_0/pinv_12_19/A gnd 2.83fF
C153 control_logic_rw_0/delay_chain_0/pinv_12_29/A gnd 2.52fF
C154 bank_0/w_en0 gnd 14.92fF
C155 control_logic_rw_0/pand2_1/Z gnd 6.54fF
C156 control_logic_rw_0/pand3_0_0/C gnd 4.53fF
C157 control_logic_rw_0/pand3_0/A gnd 4.44fF
C158 control_logic_rw_0/dff_buf_array_0/dff_buf_0_0/dff_0/a_48_48# gnd 2.49fF
C159 control_logic_rw_0/pand2_0/B gnd 6.57fF
C160 control_logic_rw_0/dff_buf_array_0/dff_buf_0_1/dff_0/a_48_48# gnd 2.40fF
C161 bank_0/s_en0 gnd 9.47fF
C162 data_dff_0/dff_1/a_48_48# gnd 2.39fF
C163 data_dff_0/dff_0/a_48_48# gnd 2.54fF
C164 bank_0/din0_0 gnd 3.05fF
.ends
