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
XXCDEC_MP1 BLC_PMOS_DRIVE wr_zero vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXCDEC_MP0 BLC_PMOS_DRIVE sel_p vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXCDEC_MN0 BLC_PMOS_DRIVE wr_zero XCDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXCDEC_MN1 XCDEC_net7 sel_p gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXTDEC_MP1 BLT_PMOS_DRIVE wr_one vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXTDEC_MP0 BLT_PMOS_DRIVE sel_p vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXTDEC_MN0 BLT_PMOS_DRIVE wr_one XTDEC_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXTDEC_MN1 XTDEC_net7 sel_p gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XMTWN bl BLT_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
XMCWN br BLC_NMOS_DRIVE gnd gnd sg13_lv_nmos w=4.82u l=130.00n m=1
XMCWP br BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
XMTWP bl BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.5u l=130.00n m=1
XMTSP bl_sel SEL_N bl vdd sg13_lv_pmos w=1.5u l=130.00n m=1
XMTPR bl pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
XMCSP br_sel SEL_N br vdd sg13_lv_pmos w=1.5u l=130.00n m=1
XMCPR br pre_n vdd vdd sg13_lv_pmos w=3.000u l=130.00n m=1
XXI86_MN0 SEL_N sel_p gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI86_MP0 SEL_N sel_p vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXTINV_MN0 BLT_NMOS_DRIVE BLC_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXTINV_MP0 BLT_NMOS_DRIVE BLC_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXCINV_MN0 BLC_NMOS_DRIVE BLT_PMOS_DRIVE gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXCINV_MP0 BLC_NMOS_DRIVE BLT_PMOS_DRIVE vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
.ends ihp_bldrv
