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
.subckt ihp_bldrv br br_sel bl bl_sel pre_n sel_p wr_one wr_zero vdd gnd
Xinternal_XCDEC_MP1 internal_BLC_PMOS_DRIVE wr_zero vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XCDEC_MP0 internal_BLC_PMOS_DRIVE sel_p vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XCDEC_MN0 internal_BLC_PMOS_DRIVE wr_zero internal_XCDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XCDEC_MN1 internal_XCDEC_net7 sel_p gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XTDEC_MP1 internal_BLT_PMOS_DRIVE wr_one vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XTDEC_MP0 internal_BLT_PMOS_DRIVE sel_p vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XTDEC_MN0 internal_BLT_PMOS_DRIVE wr_one internal_XTDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XTDEC_MN1 internal_XTDEC_net7 sel_p gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_MTWN bl internal_BLT_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xinternal_MCWN br internal_BLC_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
Xinternal_MCWP br internal_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xinternal_MTWP bl internal_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xinternal_MTSP bl_sel internal_SEL_N bl vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xinternal_MTPR bl pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xinternal_MCSP br_sel internal_SEL_N br vdd sg13_lv_pmos w=1.5u l=130.00n m=1
Xinternal_MCPR br pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
Xinternal_XI86_MN0 internal_SEL_N sel_p gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI86_MP0 internal_SEL_N sel_p vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XTINV_MN0 internal_BLT_NMOS_DRIVE internal_BLC_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XTINV_MP0 internal_BLT_NMOS_DRIVE internal_BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XCINV_MN0 internal_BLC_NMOS_DRIVE internal_BLT_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XCINV_MP0 internal_BLC_NMOS_DRIVE internal_BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
.ends ihp_bldrv
