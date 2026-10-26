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
* Flattened from RSC_IHPSG13_DFNQX2; unchanged W/L/m.
.subckt ihp_dff clk_n d q vdd gnd
Xinternal_MN0 q internal_QIN_SL gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_MN10 internal_QIN_SL internal_CNN internal_net21 gnd sg13_lv_nmos w=850.00n l=130.00n m=1
Xinternal_MN11 internal_net21 internal_QI_MS gnd gnd sg13_lv_nmos w=850.00n l=130.00n m=1
Xinternal_MN7 internal_net30 internal_QI_MS gnd gnd sg13_lv_nmos w=480.00n l=130.00n m=1
Xinternal_MN6 internal_QIN_MS internal_CNN internal_net30 gnd sg13_lv_nmos w=480.00n l=130.00n m=1
Xinternal_MN3 internal_QI_MS internal_QIN_MS gnd gnd sg13_lv_nmos w=480.00n l=130.00n m=1
Xinternal_MN12 internal_CNN clk_n gnd gnd sg13_lv_nmos w=495.000n l=130.00n m=1
Xinternal_MN9 internal_net37 d gnd gnd sg13_lv_nmos w=870.00n l=130.00n m=1
Xinternal_MN8 internal_QIN_MS clk_n internal_net37 gnd sg13_lv_nmos w=870.00n l=130.00n m=1
Xinternal_MN5 internal_QIN_SL clk_n internal_net25 gnd sg13_lv_nmos w=480.00n l=130.00n m=1
Xinternal_MN4 internal_net25 internal_QI_SL gnd gnd sg13_lv_nmos w=480.00n l=130.00n m=1
Xinternal_MN2 internal_QI_SL internal_QIN_SL gnd gnd sg13_lv_nmos w=480.00n l=130.00n m=1
Xinternal_MP0 q internal_QIN_SL vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_MP6 internal_QI_MS internal_QIN_MS vdd vdd sg13_lv_pmos w=480.00n l=130.00n m=1
Xinternal_MP3 internal_QIN_SL internal_CNN internal_net27 vdd sg13_lv_pmos w=480.00n l=130.00n m=1
Xinternal_MP2 internal_net27 internal_QI_SL vdd vdd sg13_lv_pmos w=480.00n l=130.00n m=1
Xinternal_MP10 internal_net36 d vdd vdd sg13_lv_pmos w=975.000n l=130.00n m=1
Xinternal_MP11 internal_QIN_MS internal_CNN internal_net36 vdd sg13_lv_pmos w=975.000n l=130.00n m=1
Xinternal_MP4 internal_net32 internal_QI_MS vdd vdd sg13_lv_pmos w=480.00n l=130.00n m=1
Xinternal_MP5 internal_QIN_MS clk_n internal_net32 vdd sg13_lv_pmos w=480.00n l=130.00n m=1
Xinternal_MP7 internal_QI_SL internal_QIN_SL vdd vdd sg13_lv_pmos w=480.00n l=130.00n m=1
Xinternal_MP12 internal_CNN clk_n vdd vdd sg13_lv_pmos w=480.00n l=130.00n m=1
Xinternal_MP9 internal_QIN_SL clk_n internal_net19 vdd sg13_lv_pmos w=990.00n l=130.00n m=1
Xinternal_MP8 internal_net19 internal_QI_MS vdd vdd sg13_lv_pmos w=990.00n l=130.00n m=1
.ends ihp_dff
