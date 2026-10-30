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
* Flattened from RM_IHPSG13_64x16_c2_1P_DLY_MUX; unchanged W/L/m.
.subckt ihp_delay_mux a sel z vdd gnd
Xinternal_XI11_MN0 z internal_net4 gnd gnd sg13_lv_nmos w=705.000n l=130.00n m=1
Xinternal_XI11_MP0 z internal_net4 vdd vdd sg13_lv_pmos w=1.62u l=130.00n m=1
Xinternal_XI8_MP4 internal_XI8_SN sel vdd vdd sg13_lv_pmos w=645.000n l=130.00n m=1
Xinternal_XI8_MP3 internal_net4 internal_XI8_SN internal_XI8_net12 vdd sg13_lv_pmos w=985.000n l=130.00n m=1
Xinternal_XI8_MP2 internal_XI8_net12 internal_D<3> vdd vdd sg13_lv_pmos w=985.000n l=130.00n m=1
Xinternal_XI8_MP1 internal_net4 sel internal_XI8_net17 vdd sg13_lv_pmos w=985.000n l=130.00n m=1
Xinternal_XI8_MP0 internal_XI8_net17 a vdd vdd sg13_lv_pmos w=985.000n l=130.00n m=1
Xinternal_XI8_MN5 internal_XI8_SN sel gnd gnd sg13_lv_nmos w=480.00n l=130.00n m=1
Xinternal_XI8_MN3 internal_XI8_net13 internal_D<3> gnd gnd sg13_lv_nmos w=480.00n l=130.00n m=1
Xinternal_XI8_MN2 internal_net4 sel internal_XI8_net13 gnd sg13_lv_nmos w=480.00n l=130.00n m=1
Xinternal_XI8_MN1 internal_XI8_net15 a gnd gnd sg13_lv_nmos w=480.00n l=130.00n m=1
Xinternal_XI8_MN0 internal_net4 internal_XI8_SN internal_XI8_net15 gnd sg13_lv_nmos w=480.00n l=130.00n m=1
Xinternal_XI20<3>_MN1 internal_XI20<3>_net010 internal_XI20<3>_net032 gnd gnd sg13_lv_nmos w=300.0n l=160.00n m=1
Xinternal_XI20<3>_MN2 internal_XI20<3>_net032 internal_D<2> internal_XI20<3>_net014 gnd sg13_lv_nmos w=300.0n l=160.00n m=1
Xinternal_XI20<3>_MN0 internal_D<3> internal_XI20<3>_net032 internal_XI20<3>_net010 gnd sg13_lv_nmos w=300.0n l=160.00n m=1
Xinternal_XI20<3>_MN3 internal_XI20<3>_net014 internal_D<2> gnd gnd sg13_lv_nmos w=300.0n l=160.00n m=1
Xinternal_XI20<3>_MP1 internal_D<3> internal_XI20<3>_net032 internal_XI20<3>_net07 vdd sg13_lv_pmos w=720.00n l=160.00n m=1
Xinternal_XI20<3>_MP3 internal_XI20<3>_net011 internal_D<2> vdd vdd sg13_lv_pmos w=720.00n l=160.00n m=1
Xinternal_XI20<3>_MP0 internal_XI20<3>_net07 internal_XI20<3>_net032 vdd vdd sg13_lv_pmos w=720.00n l=160.00n m=1
Xinternal_XI20<3>_MP2 internal_XI20<3>_net032 internal_D<2> internal_XI20<3>_net011 vdd sg13_lv_pmos w=720.00n l=160.00n m=1
Xinternal_XI20<2>_MN1 internal_XI20<2>_net010 internal_XI20<2>_net032 gnd gnd sg13_lv_nmos w=300.0n l=160.00n m=1
Xinternal_XI20<2>_MN2 internal_XI20<2>_net032 internal_D<1> internal_XI20<2>_net014 gnd sg13_lv_nmos w=300.0n l=160.00n m=1
Xinternal_XI20<2>_MN0 internal_D<2> internal_XI20<2>_net032 internal_XI20<2>_net010 gnd sg13_lv_nmos w=300.0n l=160.00n m=1
Xinternal_XI20<2>_MN3 internal_XI20<2>_net014 internal_D<1> gnd gnd sg13_lv_nmos w=300.0n l=160.00n m=1
Xinternal_XI20<2>_MP1 internal_D<2> internal_XI20<2>_net032 internal_XI20<2>_net07 vdd sg13_lv_pmos w=720.00n l=160.00n m=1
Xinternal_XI20<2>_MP3 internal_XI20<2>_net011 internal_D<1> vdd vdd sg13_lv_pmos w=720.00n l=160.00n m=1
Xinternal_XI20<2>_MP0 internal_XI20<2>_net07 internal_XI20<2>_net032 vdd vdd sg13_lv_pmos w=720.00n l=160.00n m=1
Xinternal_XI20<2>_MP2 internal_XI20<2>_net032 internal_D<1> internal_XI20<2>_net011 vdd sg13_lv_pmos w=720.00n l=160.00n m=1
Xinternal_XI20<1>_MN1 internal_XI20<1>_net010 internal_XI20<1>_net032 gnd gnd sg13_lv_nmos w=300.0n l=160.00n m=1
Xinternal_XI20<1>_MN2 internal_XI20<1>_net032 a internal_XI20<1>_net014 gnd sg13_lv_nmos w=300.0n l=160.00n m=1
Xinternal_XI20<1>_MN0 internal_D<1> internal_XI20<1>_net032 internal_XI20<1>_net010 gnd sg13_lv_nmos w=300.0n l=160.00n m=1
Xinternal_XI20<1>_MN3 internal_XI20<1>_net014 a gnd gnd sg13_lv_nmos w=300.0n l=160.00n m=1
Xinternal_XI20<1>_MP1 internal_D<1> internal_XI20<1>_net032 internal_XI20<1>_net07 vdd sg13_lv_pmos w=720.00n l=160.00n m=1
Xinternal_XI20<1>_MP3 internal_XI20<1>_net011 a vdd vdd sg13_lv_pmos w=720.00n l=160.00n m=1
Xinternal_XI20<1>_MP0 internal_XI20<1>_net07 internal_XI20<1>_net032 vdd vdd sg13_lv_pmos w=720.00n l=160.00n m=1
Xinternal_XI20<1>_MP2 internal_XI20<1>_net032 a internal_XI20<1>_net011 vdd sg13_lv_pmos w=720.00n l=160.00n m=1
.ends ihp_delay_mux
