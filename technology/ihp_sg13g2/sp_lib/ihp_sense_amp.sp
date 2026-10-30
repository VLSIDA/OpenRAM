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
* Flattened from RSC_IHPSG13_DFPQD_MSAFFX2; unchanged W/L/m.
.subckt ihp_sense_amp cp dn dp qn qp vdd gnd
Xinternal_MN12 internal_SN internal_RN internal_DIFFP gnd sg13_lv_nmos w=2.4u l=200.0n m=1
Xinternal_MN13 internal_TAIL cp gnd gnd sg13_lv_nmos w=2.4u l=130.00n m=1
Xinternal_MN9 internal_DIFFP dp internal_TAIL gnd sg13_lv_nmos w=2.4u l=200.0n m=1
Xinternal_MN10 internal_DIFFN dn internal_TAIL gnd sg13_lv_nmos w=2.4u l=200.0n m=1
Xinternal_MN11 internal_RN internal_SN internal_DIFFN gnd sg13_lv_nmos w=2.4u l=200.0n m=1
Xinternal_MN19 internal_net33 internal_SN gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_MN20 qn qp internal_net37 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_MN18 internal_net37 internal_RN gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_MN17 qp qn internal_net33 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
Xinternal_MP15 internal_SN internal_RN vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xinternal_MP16 internal_RN cp vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xinternal_MP14 internal_DIFFP cp vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xinternal_MP12 internal_RN internal_SN vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xinternal_MP13 internal_DIFFN cp vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xinternal_MP11 internal_SN cp vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
Xinternal_MP19 qn qp vdd vdd sg13_lv_pmos w=900.0n l=130.00n m=1
Xinternal_MP20 qp internal_SN vdd vdd sg13_lv_pmos w=1.8u l=130.00n m=1
Xinternal_MP18 qn internal_RN vdd vdd sg13_lv_pmos w=1.8u l=130.00n m=1
Xinternal_MP17 qp qn vdd vdd sg13_lv_pmos w=900.0n l=130.00n m=1
.ends ihp_sense_amp
