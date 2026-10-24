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
* Flattened from column_decode_subset; unchanged W/L/m.
.subckt ihp_column_decoder addr_1 addr_0 sel_0 sel_1 sel_2 sel_3 vdd gnd
Xinternal_XI1<3>_MP1 internal_addr_n<3> internal_PADR<0> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XI1<3>_MP0 internal_addr_n<3> internal_PADR<1> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XI1<3>_MN0 internal_addr_n<3> internal_PADR<0> internal_XI1<3>_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI1<3>_MN1 internal_XI1<3>_net7 internal_PADR<1> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI1<2>_MP1 internal_addr_n<2> internal_NADR<0> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XI1<2>_MP0 internal_addr_n<2> internal_PADR<1> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XI1<2>_MN0 internal_addr_n<2> internal_NADR<0> internal_XI1<2>_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI1<2>_MN1 internal_XI1<2>_net7 internal_PADR<1> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI1<1>_MP1 internal_addr_n<1> internal_PADR<0> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XI1<1>_MP0 internal_addr_n<1> internal_NADR<1> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XI1<1>_MN0 internal_addr_n<1> internal_PADR<0> internal_XI1<1>_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI1<1>_MN1 internal_XI1<1>_net7 internal_NADR<1> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI1<0>_MP1 internal_addr_n<0> internal_NADR<0> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XI1<0>_MP0 internal_addr_n<0> internal_NADR<1> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XI1<0>_MN0 internal_addr_n<0> internal_NADR<0> internal_XI1<0>_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI1<0>_MN1 internal_XI1<0>_net7 internal_NADR<1> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI3<1>_MN0 internal_NADR<1> addr_1 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI3<1>_MP0 internal_NADR<1> addr_1 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XI3<0>_MN0 internal_NADR<0> addr_0 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI3<0>_MP0 internal_NADR<0> addr_0 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XI13<1>_MN0 internal_PADR<1> internal_NADR<1> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI13<1>_MP0 internal_PADR<1> internal_NADR<1> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XI13<0>_MN0 internal_PADR<0> internal_NADR<0> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI13<0>_MP0 internal_PADR<0> internal_NADR<0> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XI2<3>_MN0 sel_3 internal_addr_n<3> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI2<3>_MP0 sel_3 internal_addr_n<3> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XI2<2>_MN0 sel_2 internal_addr_n<2> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI2<2>_MP0 sel_2 internal_addr_n<2> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XI2<1>_MN0 sel_1 internal_addr_n<1> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI2<1>_MP0 sel_1 internal_addr_n<1> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XI2<0>_MN0 sel_0 internal_addr_n<0> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_XI2<0>_MP0 sel_0 internal_addr_n<0> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
.ends ihp_column_decoder
