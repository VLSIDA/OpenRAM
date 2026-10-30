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
* Flattened from RM_IHPSG13_64x16_c2_1P_DLY_pcell_2; unchanged W/L/m.
.subckt ihp_delay_high a z vdd gnd
Xinternal_XIDL_MN1 internal_XIDL_net010 internal_XIDL_net032 gnd gnd sg13_lv_nmos w=300.0n l=160.00n m=1
Xinternal_XIDL_MN2 internal_XIDL_net032 a internal_XIDL_net014 gnd sg13_lv_nmos w=300.0n l=160.00n m=1
Xinternal_XIDL_MN0 z internal_XIDL_net032 internal_XIDL_net010 gnd sg13_lv_nmos w=300.0n l=160.00n m=1
Xinternal_XIDL_MN3 internal_XIDL_net014 a gnd gnd sg13_lv_nmos w=300.0n l=160.00n m=1
Xinternal_XIDL_MP1 z internal_XIDL_net032 internal_XIDL_net07 vdd sg13_lv_pmos w=720.00n l=160.00n m=1
Xinternal_XIDL_MP3 internal_XIDL_net011 a vdd vdd sg13_lv_pmos w=720.00n l=160.00n m=1
Xinternal_XIDL_MP0 internal_XIDL_net07 internal_XIDL_net032 vdd vdd sg13_lv_pmos w=720.00n l=160.00n m=1
Xinternal_XIDL_MP2 internal_XIDL_net032 a internal_XIDL_net011 vdd sg13_lv_pmos w=720.00n l=160.00n m=1
Xinternal_XIDM<7>_MN0 internal_XIDM<7>_vss_r internal_XIDM<7>_vdd_r gnd gnd sg13_lv_nmos w=2.49u l=300.0n m=1
Xinternal_XIDM<7>_MP0 internal_XIDM<7>_vdd_r internal_XIDM<7>_vss_r vdd vdd sg13_lv_pmos w=3.24u l=640.00n m=1
Xinternal_XIDM<6>_MN0 internal_XIDM<6>_vss_r internal_XIDM<6>_vdd_r gnd gnd sg13_lv_nmos w=2.49u l=300.0n m=1
Xinternal_XIDM<6>_MP0 internal_XIDM<6>_vdd_r internal_XIDM<6>_vss_r vdd vdd sg13_lv_pmos w=3.24u l=640.00n m=1
Xinternal_XIDM<5>_MN0 internal_XIDM<5>_vss_r internal_XIDM<5>_vdd_r gnd gnd sg13_lv_nmos w=2.49u l=300.0n m=1
Xinternal_XIDM<5>_MP0 internal_XIDM<5>_vdd_r internal_XIDM<5>_vss_r vdd vdd sg13_lv_pmos w=3.24u l=640.00n m=1
Xinternal_XIDM<4>_MN0 internal_XIDM<4>_vss_r internal_XIDM<4>_vdd_r gnd gnd sg13_lv_nmos w=2.49u l=300.0n m=1
Xinternal_XIDM<4>_MP0 internal_XIDM<4>_vdd_r internal_XIDM<4>_vss_r vdd vdd sg13_lv_pmos w=3.24u l=640.00n m=1
Xinternal_XIDM<3>_MN0 internal_XIDM<3>_vss_r internal_XIDM<3>_vdd_r gnd gnd sg13_lv_nmos w=2.49u l=300.0n m=1
Xinternal_XIDM<3>_MP0 internal_XIDM<3>_vdd_r internal_XIDM<3>_vss_r vdd vdd sg13_lv_pmos w=3.24u l=640.00n m=1
Xinternal_XIDM<2>_MN0 internal_XIDM<2>_vss_r internal_XIDM<2>_vdd_r gnd gnd sg13_lv_nmos w=2.49u l=300.0n m=1
Xinternal_XIDM<2>_MP0 internal_XIDM<2>_vdd_r internal_XIDM<2>_vss_r vdd vdd sg13_lv_pmos w=3.24u l=640.00n m=1
Xinternal_XIDM<1>_MN0 internal_XIDM<1>_vss_r internal_XIDM<1>_vdd_r gnd gnd sg13_lv_nmos w=2.49u l=300.0n m=1
Xinternal_XIDM<1>_MP0 internal_XIDM<1>_vdd_r internal_XIDM<1>_vss_r vdd vdd sg13_lv_pmos w=3.24u l=640.00n m=1
.ends ihp_delay_high
