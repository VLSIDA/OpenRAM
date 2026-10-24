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
* Flattened from RSC_IHPSG13_AND2X2; unchanged W/L/m.
.subckt ihp_and2 a b z vdd gnd
Xinternal_MN3 z internal_net6 gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_MN4 internal_net9 b gnd gnd sg13_lv_nmos w=500.0n l=130.00n m=1
Xinternal_MN6 internal_net6 a internal_net9 gnd sg13_lv_nmos w=500.0n l=130.00n m=1
Xinternal_MP2 z internal_net6 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_MP0 internal_net6 b vdd vdd sg13_lv_pmos w=860.00n l=130.00n m=1
Xinternal_MP1 internal_net6 a vdd vdd sg13_lv_pmos w=860.00n l=130.00n m=1
.ends ihp_and2
