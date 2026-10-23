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
XXI1<3>_MP1 addr_n<3> PADR<0> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXI1<3>_MP0 addr_n<3> PADR<1> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXI1<3>_MN0 addr_n<3> PADR<0> XI1<3>_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI1<3>_MN1 XI1<3>_net7 PADR<1> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI1<2>_MP1 addr_n<2> NADR<0> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXI1<2>_MP0 addr_n<2> PADR<1> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXI1<2>_MN0 addr_n<2> NADR<0> XI1<2>_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI1<2>_MN1 XI1<2>_net7 PADR<1> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI1<1>_MP1 addr_n<1> PADR<0> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXI1<1>_MP0 addr_n<1> NADR<1> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXI1<1>_MN0 addr_n<1> PADR<0> XI1<1>_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI1<1>_MN1 XI1<1>_net7 NADR<1> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI1<0>_MP1 addr_n<0> NADR<0> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXI1<0>_MP0 addr_n<0> NADR<1> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXI1<0>_MN0 addr_n<0> NADR<0> XI1<0>_net7 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI1<0>_MN1 XI1<0>_net7 NADR<1> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI3<1>_MN0 NADR<1> addr_1 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI3<1>_MP0 NADR<1> addr_1 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXI3<0>_MN0 NADR<0> addr_0 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI3<0>_MP0 NADR<0> addr_0 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXI13<1>_MN0 PADR<1> NADR<1> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI13<1>_MP0 PADR<1> NADR<1> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXI13<0>_MN0 PADR<0> NADR<0> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI13<0>_MP0 PADR<0> NADR<0> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXI2<3>_MN0 sel_3 addr_n<3> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI2<3>_MP0 sel_3 addr_n<3> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXI2<2>_MN0 sel_2 addr_n<2> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI2<2>_MP0 sel_2 addr_n<2> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXI2<1>_MN0 sel_1 addr_n<1> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI2<1>_MP0 sel_1 addr_n<1> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
XXI2<0>_MN0 sel_0 addr_n<0> gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XXI2<0>_MP0 sel_0 addr_n<0> vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
.ends ihp_column_decoder
