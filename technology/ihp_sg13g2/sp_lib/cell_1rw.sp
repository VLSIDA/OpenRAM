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

* Imported from RM_IHPSG13_1P_64x16_c2.cdl: RM_IHPSG13_64x16_c2_1P_BITKIT_CELL
* NW/PW require array taps. lvsres through-pins are joined.
.subckt cell_1rw bl br wl vdd gnd
XN0 NC NT gnd gnd sg13_lv_nmos w=300.0n l=130.00n m=1
XN1 NT NC gnd gnd sg13_lv_nmos w=300.0n l=130.00n m=1
XN3 NC wl br gnd sg13_lv_nmos w=300.0n l=130.00n m=1
XN2 bl wl NT gnd sg13_lv_nmos w=300.0n l=130.00n m=1
XP1 NT NC vdd vdd sg13_lv_pmos w=150.00n l=130.00n m=1
XP0 NC NT vdd vdd sg13_lv_pmos w=150.00n l=130.00n m=1
.ends cell_1rw
