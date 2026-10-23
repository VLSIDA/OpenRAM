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
XMN12 SN RN DIFFP gnd sg13_lv_nmos w=2.4u l=200.0n m=1
XMN13 TAIL cp gnd gnd sg13_lv_nmos w=2.4u l=130.00n m=1
XMN9 DIFFP dp TAIL gnd sg13_lv_nmos w=2.4u l=200.0n m=1
XMN10 DIFFN dn TAIL gnd sg13_lv_nmos w=2.4u l=200.0n m=1
XMN11 RN SN DIFFN gnd sg13_lv_nmos w=2.4u l=200.0n m=1
XMN19 net33 SN gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XMN20 qn qp net37 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XMN18 net37 RN gnd gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XMN17 qp qn net33 gnd sg13_lv_nmos w=980.00n l=130.00n m=1
XMP15 SN RN vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
XMP16 RN cp vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
XMP14 DIFFP cp vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
XMP12 RN SN vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
XMP13 DIFFN cp vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
XMP11 SN cp vdd vdd sg13_lv_pmos w=800.0n l=130.00n m=1
XMP19 qn qp vdd vdd sg13_lv_pmos w=900.0n l=130.00n m=1
XMP20 qp SN vdd vdd sg13_lv_pmos w=1.8u l=130.00n m=1
XMP18 qn RN vdd vdd sg13_lv_pmos w=1.8u l=130.00n m=1
XMP17 qp qn vdd vdd sg13_lv_pmos w=900.0n l=130.00n m=1
.ends ihp_sense_amp
