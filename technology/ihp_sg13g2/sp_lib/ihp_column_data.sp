* ------------------------------------------------------
*
*		Copyright 2025 IHP PDK Authors
*
*		Licensed under the Apache License, Version 2.0 (the "License");
*		you may not use this file except in compliance with the License.
*		You may obtain a copy of the License at
*		
*		   https://www.apache.org/licenses/LICENSE-2.0
*		
*		Unless required by applicable law or agreed to in writing, software
*		distributed under the License is distributed on an "AS IS" BASIS,
*		WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*		See the License for the specific language governing permissions and
*		limitations under the License.
*		
*		Generated on Thu Jul 30 11:38:32 2026		
*
* ------------------------------------------------------
* Flattened from RM_IHPSG13_64x16_c2_1P_BLDRV; unchanged W/L/m.
.subckt ihp_column_data bl_0 br_0 bl_1 br_1 bl_2 br_2 bl_3 br_3 sel_0 sel_1 sel_2 sel_3 pre_n wr_one wr_zero sae qp qn vdd gnd
Xsense_MN12 sense_SN sense_RN sense_DIFFP gnd sg13_lv_nmos w=2.4u l=200.0n m=1
Xsense_MN13 sense_TAIL sae gnd gnd sg13_lv_nmos w=2.4u l=130.00n m=1
Xsense_MN9 sense_DIFFP bl_sel sense_TAIL gnd sg13_lv_nmos w=2.4u l=200.0n m=1
Xsense_MN10 sense_DIFFN br_sel sense_TAIL gnd sg13_lv_nmos w=2.4u l=200.0n m=1
Xsense_MN11 sense_RN sense_SN sense_DIFFN gnd sg13_lv_nmos w=2.4u l=200.0n m=1
Xsense_MN19 sense_net33 sense_SN gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xsense_MN20 qn qp sense_net37 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xsense_MN18 sense_net37 sense_RN gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xsense_MN17 qp qn sense_net33 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xsense_MP15 sense_SN sense_RN vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xsense_MP16 sense_RN sae vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xsense_MP14 sense_DIFFP sae vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xsense_MP12 sense_RN sense_SN vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xsense_MP13 sense_DIFFN sae vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xsense_MP11 sense_SN sae vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xsense_MP19 qn qp vdd vdd sg13_lv_pmos w=900.0n l=130.00n m=1
Xsense_MP20 qp sense_SN vdd vdd sg13_lv_pmos w=1.8u l=130.00n m=1
Xsense_MP18 qn sense_RN vdd vdd sg13_lv_pmos w=1.8u l=130.00n m=1
Xsense_MP17 qp qn vdd vdd sg13_lv_pmos w=900.0n l=130.00n m=1
Xdriver_3_XCDEC_MP1 driver_3_BLC_PMOS_DRIVE wr_zero vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_3_XCDEC_MP0 driver_3_BLC_PMOS_DRIVE sel_3 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_3_XCDEC_MN0 driver_3_BLC_PMOS_DRIVE wr_zero driver_3_XCDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_3_XCDEC_MN1 driver_3_XCDEC_net7 sel_3 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_3_XTDEC_MP1 driver_3_BLT_PMOS_DRIVE wr_one vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_3_XTDEC_MP0 driver_3_BLT_PMOS_DRIVE sel_3 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_3_XTDEC_MN0 driver_3_BLT_PMOS_DRIVE wr_one driver_3_XTDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_3_XTDEC_MN1 driver_3_XTDEC_net7 sel_3 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_3_MTWN bl_3 driver_3_BLT_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xdriver_3_MCWN br_3 driver_3_BLC_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xdriver_3_MCWP br_3 driver_3_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_3_MTWP bl_3 driver_3_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_3_MTSP bl_sel driver_3_SEL_N bl_3 vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_3_MTPR bl_3 pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xdriver_3_MCSP br_sel driver_3_SEL_N br_3 vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_3_MCPR br_3 pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xdriver_3_XI86_MN0 driver_3_SEL_N sel_3 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_3_XI86_MP0 driver_3_SEL_N sel_3 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_3_XTINV_MN0 driver_3_BLT_NMOS_DRIVE driver_3_BLC_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_3_XTINV_MP0 driver_3_BLT_NMOS_DRIVE driver_3_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_3_XCINV_MN0 driver_3_BLC_NMOS_DRIVE driver_3_BLT_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_3_XCINV_MP0 driver_3_BLC_NMOS_DRIVE driver_3_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_1_XCDEC_MP1 driver_1_BLC_PMOS_DRIVE wr_zero vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_1_XCDEC_MP0 driver_1_BLC_PMOS_DRIVE sel_1 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_1_XCDEC_MN0 driver_1_BLC_PMOS_DRIVE wr_zero driver_1_XCDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_1_XCDEC_MN1 driver_1_XCDEC_net7 sel_1 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_1_XTDEC_MP1 driver_1_BLT_PMOS_DRIVE wr_one vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_1_XTDEC_MP0 driver_1_BLT_PMOS_DRIVE sel_1 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_1_XTDEC_MN0 driver_1_BLT_PMOS_DRIVE wr_one driver_1_XTDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_1_XTDEC_MN1 driver_1_XTDEC_net7 sel_1 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_1_MTWN bl_1 driver_1_BLT_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xdriver_1_MCWN br_1 driver_1_BLC_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xdriver_1_MCWP br_1 driver_1_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_1_MTWP bl_1 driver_1_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_1_MTSP bl_sel driver_1_SEL_N bl_1 vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_1_MTPR bl_1 pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xdriver_1_MCSP br_sel driver_1_SEL_N br_1 vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_1_MCPR br_1 pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xdriver_1_XI86_MN0 driver_1_SEL_N sel_1 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_1_XI86_MP0 driver_1_SEL_N sel_1 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_1_XTINV_MN0 driver_1_BLT_NMOS_DRIVE driver_1_BLC_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_1_XTINV_MP0 driver_1_BLT_NMOS_DRIVE driver_1_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_1_XCINV_MN0 driver_1_BLC_NMOS_DRIVE driver_1_BLT_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_1_XCINV_MP0 driver_1_BLC_NMOS_DRIVE driver_1_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_0_XCDEC_MP1 driver_0_BLC_PMOS_DRIVE wr_zero vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_0_XCDEC_MP0 driver_0_BLC_PMOS_DRIVE sel_0 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_0_XCDEC_MN0 driver_0_BLC_PMOS_DRIVE wr_zero driver_0_XCDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_0_XCDEC_MN1 driver_0_XCDEC_net7 sel_0 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_0_XTDEC_MP1 driver_0_BLT_PMOS_DRIVE wr_one vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_0_XTDEC_MP0 driver_0_BLT_PMOS_DRIVE sel_0 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_0_XTDEC_MN0 driver_0_BLT_PMOS_DRIVE wr_one driver_0_XTDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_0_XTDEC_MN1 driver_0_XTDEC_net7 sel_0 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_0_MTWN bl_0 driver_0_BLT_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xdriver_0_MCWN br_0 driver_0_BLC_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xdriver_0_MCWP br_0 driver_0_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_0_MTWP bl_0 driver_0_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_0_MTSP bl_sel driver_0_SEL_N bl_0 vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_0_MTPR bl_0 pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xdriver_0_MCSP br_sel driver_0_SEL_N br_0 vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_0_MCPR br_0 pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xdriver_0_XI86_MN0 driver_0_SEL_N sel_0 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_0_XI86_MP0 driver_0_SEL_N sel_0 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_0_XTINV_MN0 driver_0_BLT_NMOS_DRIVE driver_0_BLC_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_0_XTINV_MP0 driver_0_BLT_NMOS_DRIVE driver_0_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_0_XCINV_MN0 driver_0_BLC_NMOS_DRIVE driver_0_BLT_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_0_XCINV_MP0 driver_0_BLC_NMOS_DRIVE driver_0_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_2_XCDEC_MP1 driver_2_BLC_PMOS_DRIVE wr_zero vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_2_XCDEC_MP0 driver_2_BLC_PMOS_DRIVE sel_2 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_2_XCDEC_MN0 driver_2_BLC_PMOS_DRIVE wr_zero driver_2_XCDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_2_XCDEC_MN1 driver_2_XCDEC_net7 sel_2 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_2_XTDEC_MP1 driver_2_BLT_PMOS_DRIVE wr_one vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_2_XTDEC_MP0 driver_2_BLT_PMOS_DRIVE sel_2 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_2_XTDEC_MN0 driver_2_BLT_PMOS_DRIVE wr_one driver_2_XTDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_2_XTDEC_MN1 driver_2_XTDEC_net7 sel_2 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_2_MTWN bl_2 driver_2_BLT_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xdriver_2_MCWN br_2 driver_2_BLC_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xdriver_2_MCWP br_2 driver_2_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_2_MTWP bl_2 driver_2_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_2_MTSP bl_sel driver_2_SEL_N bl_2 vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_2_MTPR bl_2 pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xdriver_2_MCSP br_sel driver_2_SEL_N br_2 vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_2_MCPR br_2 pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xdriver_2_XI86_MN0 driver_2_SEL_N sel_2 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_2_XI86_MP0 driver_2_SEL_N sel_2 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_2_XTINV_MN0 driver_2_BLT_NMOS_DRIVE driver_2_BLC_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_2_XTINV_MP0 driver_2_BLT_NMOS_DRIVE driver_2_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_2_XCINV_MN0 driver_2_BLC_NMOS_DRIVE driver_2_BLT_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_2_XCINV_MP0 driver_2_BLC_NMOS_DRIVE driver_2_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
.ends ihp_column_data
