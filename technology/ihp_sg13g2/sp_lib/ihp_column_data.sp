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
Xsense_internal_MN12 sense_internal_SN sense_internal_RN sense_internal_DIFFP gnd sg13_lv_nmos w=2.4u l=200.0n m=1
Xsense_internal_MN13 sense_internal_TAIL sae gnd gnd sg13_lv_nmos w=2.4u l=130.00n m=1
Xsense_internal_MN9 sense_internal_DIFFP bl_sel sense_internal_TAIL gnd sg13_lv_nmos w=2.4u l=200.0n m=1
Xsense_internal_MN10 sense_internal_DIFFN br_sel sense_internal_TAIL gnd sg13_lv_nmos w=2.4u l=200.0n m=1
Xsense_internal_MN11 sense_internal_RN sense_internal_SN sense_internal_DIFFN gnd sg13_lv_nmos w=2.4u l=200.0n m=1
Xsense_internal_MN19 sense_internal_net33 sense_internal_SN gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xsense_internal_MN20 qn qp sense_internal_net37 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xsense_internal_MN18 sense_internal_net37 sense_internal_RN gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xsense_internal_MN17 qp qn sense_internal_net33 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xsense_internal_MP15 sense_internal_SN sense_internal_RN vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xsense_internal_MP16 sense_internal_RN sae vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xsense_internal_MP14 sense_internal_DIFFP sae vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xsense_internal_MP12 sense_internal_RN sense_internal_SN vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xsense_internal_MP13 sense_internal_DIFFN sae vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xsense_internal_MP11 sense_internal_SN sae vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xsense_internal_MP19 qn qp vdd vdd sg13_lv_pmos w=900.0n l=130.00n m=1
Xsense_internal_MP20 qp sense_internal_SN vdd vdd sg13_lv_pmos w=1.8u l=130.00n m=1
Xsense_internal_MP18 qn sense_internal_RN vdd vdd sg13_lv_pmos w=1.8u l=130.00n m=1
Xsense_internal_MP17 qp qn vdd vdd sg13_lv_pmos w=900.0n l=130.00n m=1
Xdriver_3_internal_XCDEC_MP1 driver_3_internal_BLC_PMOS_DRIVE wr_zero vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_3_internal_XCDEC_MP0 driver_3_internal_BLC_PMOS_DRIVE sel_3 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_3_internal_XCDEC_MN0 driver_3_internal_BLC_PMOS_DRIVE wr_zero driver_3_internal_XCDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_3_internal_XCDEC_MN1 driver_3_internal_XCDEC_net7 sel_3 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_3_internal_XTDEC_MP1 driver_3_internal_BLT_PMOS_DRIVE wr_one vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_3_internal_XTDEC_MP0 driver_3_internal_BLT_PMOS_DRIVE sel_3 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_3_internal_XTDEC_MN0 driver_3_internal_BLT_PMOS_DRIVE wr_one driver_3_internal_XTDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_3_internal_XTDEC_MN1 driver_3_internal_XTDEC_net7 sel_3 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_3_internal_MTWN bl_3 driver_3_internal_BLT_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xdriver_3_internal_MCWN br_3 driver_3_internal_BLC_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xdriver_3_internal_MCWP br_3 driver_3_internal_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_3_internal_MTWP bl_3 driver_3_internal_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_3_internal_MTSP bl_sel driver_3_internal_SEL_N bl_3 vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_3_internal_MTPR bl_3 pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xdriver_3_internal_MCSP br_sel driver_3_internal_SEL_N br_3 vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_3_internal_MCPR br_3 pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xdriver_3_internal_XI86_MN0 driver_3_internal_SEL_N sel_3 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_3_internal_XI86_MP0 driver_3_internal_SEL_N sel_3 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_3_internal_XTINV_MN0 driver_3_internal_BLT_NMOS_DRIVE driver_3_internal_BLC_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_3_internal_XTINV_MP0 driver_3_internal_BLT_NMOS_DRIVE driver_3_internal_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_3_internal_XCINV_MN0 driver_3_internal_BLC_NMOS_DRIVE driver_3_internal_BLT_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_3_internal_XCINV_MP0 driver_3_internal_BLC_NMOS_DRIVE driver_3_internal_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_1_internal_XCDEC_MP1 driver_1_internal_BLC_PMOS_DRIVE wr_zero vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_1_internal_XCDEC_MP0 driver_1_internal_BLC_PMOS_DRIVE sel_1 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_1_internal_XCDEC_MN0 driver_1_internal_BLC_PMOS_DRIVE wr_zero driver_1_internal_XCDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_1_internal_XCDEC_MN1 driver_1_internal_XCDEC_net7 sel_1 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_1_internal_XTDEC_MP1 driver_1_internal_BLT_PMOS_DRIVE wr_one vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_1_internal_XTDEC_MP0 driver_1_internal_BLT_PMOS_DRIVE sel_1 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_1_internal_XTDEC_MN0 driver_1_internal_BLT_PMOS_DRIVE wr_one driver_1_internal_XTDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_1_internal_XTDEC_MN1 driver_1_internal_XTDEC_net7 sel_1 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_1_internal_MTWN bl_1 driver_1_internal_BLT_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xdriver_1_internal_MCWN br_1 driver_1_internal_BLC_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xdriver_1_internal_MCWP br_1 driver_1_internal_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_1_internal_MTWP bl_1 driver_1_internal_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_1_internal_MTSP bl_sel driver_1_internal_SEL_N bl_1 vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_1_internal_MTPR bl_1 pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xdriver_1_internal_MCSP br_sel driver_1_internal_SEL_N br_1 vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_1_internal_MCPR br_1 pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xdriver_1_internal_XI86_MN0 driver_1_internal_SEL_N sel_1 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_1_internal_XI86_MP0 driver_1_internal_SEL_N sel_1 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_1_internal_XTINV_MN0 driver_1_internal_BLT_NMOS_DRIVE driver_1_internal_BLC_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_1_internal_XTINV_MP0 driver_1_internal_BLT_NMOS_DRIVE driver_1_internal_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_1_internal_XCINV_MN0 driver_1_internal_BLC_NMOS_DRIVE driver_1_internal_BLT_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_1_internal_XCINV_MP0 driver_1_internal_BLC_NMOS_DRIVE driver_1_internal_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_0_internal_XCDEC_MP1 driver_0_internal_BLC_PMOS_DRIVE wr_zero vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_0_internal_XCDEC_MP0 driver_0_internal_BLC_PMOS_DRIVE sel_0 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_0_internal_XCDEC_MN0 driver_0_internal_BLC_PMOS_DRIVE wr_zero driver_0_internal_XCDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_0_internal_XCDEC_MN1 driver_0_internal_XCDEC_net7 sel_0 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_0_internal_XTDEC_MP1 driver_0_internal_BLT_PMOS_DRIVE wr_one vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_0_internal_XTDEC_MP0 driver_0_internal_BLT_PMOS_DRIVE sel_0 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_0_internal_XTDEC_MN0 driver_0_internal_BLT_PMOS_DRIVE wr_one driver_0_internal_XTDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_0_internal_XTDEC_MN1 driver_0_internal_XTDEC_net7 sel_0 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_0_internal_MTWN bl_0 driver_0_internal_BLT_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xdriver_0_internal_MCWN br_0 driver_0_internal_BLC_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xdriver_0_internal_MCWP br_0 driver_0_internal_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_0_internal_MTWP bl_0 driver_0_internal_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_0_internal_MTSP bl_sel driver_0_internal_SEL_N bl_0 vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_0_internal_MTPR bl_0 pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xdriver_0_internal_MCSP br_sel driver_0_internal_SEL_N br_0 vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_0_internal_MCPR br_0 pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xdriver_0_internal_XI86_MN0 driver_0_internal_SEL_N sel_0 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_0_internal_XI86_MP0 driver_0_internal_SEL_N sel_0 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_0_internal_XTINV_MN0 driver_0_internal_BLT_NMOS_DRIVE driver_0_internal_BLC_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_0_internal_XTINV_MP0 driver_0_internal_BLT_NMOS_DRIVE driver_0_internal_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_0_internal_XCINV_MN0 driver_0_internal_BLC_NMOS_DRIVE driver_0_internal_BLT_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_0_internal_XCINV_MP0 driver_0_internal_BLC_NMOS_DRIVE driver_0_internal_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_2_internal_XCDEC_MP1 driver_2_internal_BLC_PMOS_DRIVE wr_zero vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_2_internal_XCDEC_MP0 driver_2_internal_BLC_PMOS_DRIVE sel_2 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_2_internal_XCDEC_MN0 driver_2_internal_BLC_PMOS_DRIVE wr_zero driver_2_internal_XCDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_2_internal_XCDEC_MN1 driver_2_internal_XCDEC_net7 sel_2 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_2_internal_XTDEC_MP1 driver_2_internal_BLT_PMOS_DRIVE wr_one vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_2_internal_XTDEC_MP0 driver_2_internal_BLT_PMOS_DRIVE sel_2 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_2_internal_XTDEC_MN0 driver_2_internal_BLT_PMOS_DRIVE wr_one driver_2_internal_XTDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_2_internal_XTDEC_MN1 driver_2_internal_XTDEC_net7 sel_2 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_2_internal_MTWN bl_2 driver_2_internal_BLT_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xdriver_2_internal_MCWN br_2 driver_2_internal_BLC_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xdriver_2_internal_MCWP br_2 driver_2_internal_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_2_internal_MTWP bl_2 driver_2_internal_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_2_internal_MTSP bl_sel driver_2_internal_SEL_N bl_2 vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_2_internal_MTPR bl_2 pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xdriver_2_internal_MCSP br_sel driver_2_internal_SEL_N br_2 vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xdriver_2_internal_MCPR br_2 pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xdriver_2_internal_XI86_MN0 driver_2_internal_SEL_N sel_2 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_2_internal_XI86_MP0 driver_2_internal_SEL_N sel_2 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_2_internal_XTINV_MN0 driver_2_internal_BLT_NMOS_DRIVE driver_2_internal_BLC_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_2_internal_XTINV_MP0 driver_2_internal_BLT_NMOS_DRIVE driver_2_internal_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xdriver_2_internal_XCINV_MN0 driver_2_internal_BLC_NMOS_DRIVE driver_2_internal_BLT_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xdriver_2_internal_XCINV_MP0 driver_2_internal_BLC_NMOS_DRIVE driver_2_internal_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
.ends ihp_column_data
