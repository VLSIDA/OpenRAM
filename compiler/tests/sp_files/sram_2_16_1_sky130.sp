**************************************************
* OpenRAM generated memory.
* Words: 16
* Data bits: 2
* Banks: 1
* Column mux: 1:1
* Trimmed: False
* LVS: False
**************************************************
* Copyright 2020 The SkyWater PDK Authors
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     https://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*
* SPDX-License-Identifier: Apache-2.0

* SPICE3 file created from sky130_fd_bd_sram__openram_dff.ext - technology: EFS8A

.subckt sky130_fd_bd_sram__openram_dff D Q CLK VDD GND
X1000 a_511_725# a_n8_115# VDD VDD sky130_fd_pr__pfet_01v8 W=3 L=0.15
X1001 a_353_115# CLK a_11_624# GND sky130_fd_pr__nfet_01v8 W=1 L=0.15
X1002 a_353_725# a_203_89# a_11_624# VDD sky130_fd_pr__pfet_01v8 W=3 L=0.15
X1003 a_11_624# a_203_89# a_161_115# GND sky130_fd_pr__nfet_01v8 W=1 L=0.15
X1004 a_11_624# CLK a_161_725# VDD sky130_fd_pr__pfet_01v8 W=3 L=0.15
X1005 GND Q a_703_115# GND sky130_fd_pr__nfet_01v8 W=1 L=0.15
X1006 VDD Q a_703_725# VDD sky130_fd_pr__pfet_01v8 W=3 L=0.15
X1007 a_203_89# CLK GND GND sky130_fd_pr__nfet_01v8 W=1 L=0.15
X1008 a_203_89# CLK VDD VDD sky130_fd_pr__pfet_01v8 W=3 L=0.15
X1009 a_161_115# D GND GND sky130_fd_pr__nfet_01v8 W=1 L=0.15
X1010 a_161_725# D VDD VDD sky130_fd_pr__pfet_01v8 W=3 L=0.15
X1011 GND a_11_624# a_n8_115# GND sky130_fd_pr__nfet_01v8 W=1 L=0.15
X1012 a_703_115# a_203_89# ON GND sky130_fd_pr__nfet_01v8 W=1 L=0.15
X1013 VDD a_11_624# a_n8_115# VDD sky130_fd_pr__pfet_01v8 W=3 L=0.15
X1014 a_703_725# CLK ON VDD sky130_fd_pr__pfet_01v8 W=3 L=0.15
X1015 Q ON VDD VDD sky130_fd_pr__pfet_01v8 W=3 L=0.15
X1016 Q ON GND GND sky130_fd_pr__nfet_01v8 W=1 L=0.15
X1017 ON a_203_89# a_511_725# VDD sky130_fd_pr__pfet_01v8 W=3 L=0.15
X1018 ON CLK a_511_115# GND sky130_fd_pr__nfet_01v8 W=1 L=0.15
X1019 GND a_n8_115# a_353_115# GND sky130_fd_pr__nfet_01v8 W=1 L=0.15
X1020 VDD a_n8_115# a_353_725# VDD sky130_fd_pr__pfet_01v8 W=3 L=0.15
X1021 a_511_115# a_n8_115# GND GND sky130_fd_pr__nfet_01v8 W=1 L=0.15
.ends

.SUBCKT sram_2_16_1_sky130_row_addr_dff
+ din_0 din_1 din_2 din_3 din_4 dout_0 dout_1 dout_2 dout_3 dout_4 clk
+ vdd gnd
* INPUT : din_0 
* INPUT : din_1 
* INPUT : din_2 
* INPUT : din_3 
* INPUT : din_4 
* OUTPUT: dout_0 
* OUTPUT: dout_1 
* OUTPUT: dout_2 
* OUTPUT: dout_3 
* OUTPUT: dout_4 
* INPUT : clk 
* POWER : vdd 
* GROUND: gnd 
* rows: 5 cols: 1
Xdff_r0_c0
+ din_0 dout_0 CLK VDD GND
+ sky130_fd_bd_sram__openram_dff
Xdff_r1_c0
+ din_1 dout_1 CLK VDD GND
+ sky130_fd_bd_sram__openram_dff
Xdff_r2_c0
+ din_2 dout_2 CLK VDD GND
+ sky130_fd_bd_sram__openram_dff
Xdff_r3_c0
+ din_3 dout_3 CLK VDD GND
+ sky130_fd_bd_sram__openram_dff
Xdff_r4_c0
+ din_4 dout_4 CLK VDD GND
+ sky130_fd_bd_sram__openram_dff
.ENDS sram_2_16_1_sky130_row_addr_dff

.SUBCKT sram_2_16_1_sky130_data_dff
+ din_0 din_1 din_2 dout_0 dout_1 dout_2 clk vdd gnd
* INPUT : din_0 
* INPUT : din_1 
* INPUT : din_2 
* OUTPUT: dout_0 
* OUTPUT: dout_1 
* OUTPUT: dout_2 
* INPUT : clk 
* POWER : vdd 
* GROUND: gnd 
* rows: 1 cols: 3
Xdff_r0_c0
+ din_0 dout_0 CLK VDD GND
+ sky130_fd_bd_sram__openram_dff
Xdff_r0_c1
+ din_1 dout_1 CLK VDD GND
+ sky130_fd_bd_sram__openram_dff
Xdff_r0_c2
+ din_2 dout_2 CLK VDD GND
+ sky130_fd_bd_sram__openram_dff
.ENDS sram_2_16_1_sky130_data_dff

* spice ptx X{0} {1} sky130_fd_pr__nfet_01v8 m=1 w=0.36 l=0.15 pd=1.02 ps=1.02 as=0.14u ad=0.14u

* spice ptx X{0} {1} sky130_fd_pr__pfet_01v8 m=1 w=1.12 l=0.15 pd=2.54 ps=2.54 as=0.42u ad=0.42u

.SUBCKT sram_2_16_1_sky130_pinv_dec
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 1
Xpinv_pmos Z A vdd vdd sky130_fd_pr__pfet_01v8 m=1 w=1.12 l=0.15 pd=2.54 ps=2.54 as=0.42u ad=0.42u
Xpinv_nmos Z A gnd gnd sky130_fd_pr__nfet_01v8 m=1 w=0.36 l=0.15 pd=1.02 ps=1.02 as=0.14u ad=0.14u
.ENDS sram_2_16_1_sky130_pinv_dec
* Copyright 2020 The SkyWater PDK Authors
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     https://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*
* SPDX-License-Identifier: Apache-2.0

* NGSPICE file created from sky130_fd_bd_sram__openram_sp_nand2_dec.ext - technology: EFS8A


* Top level circuit sky130_fd_bd_sram__openram_sp_nand2_dec
.subckt sky130_fd_bd_sram__openram_sp_nand2_dec A B Z VDD GND

X1001 Z B VDD VDD sky130_fd_pr__pfet_01v8 W=1.12 L=0.15
X1002 VDD A Z VDD sky130_fd_pr__pfet_01v8 W=1.12 L=0.15
X1000 Z A a_n722_276# GND sky130_fd_pr__nfet_01v8 W=0.74 L=0.15
X1003 a_n722_276# B GND GND sky130_fd_pr__nfet_01v8 W=0.74 L=0.15
.ends


.SUBCKT sram_2_16_1_sky130_and2_dec
+ A B Z vdd gnd
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 1
Xpand2_dec_nand
+ A B zb_int vdd gnd
+ sky130_fd_bd_sram__openram_sp_nand2_dec
Xpand2_dec_inv
+ zb_int Z vdd gnd
+ sram_2_16_1_sky130_pinv_dec
.ENDS sram_2_16_1_sky130_and2_dec

.SUBCKT sram_2_16_1_sky130_hierarchical_predecode2x4
+ in_0 in_1 out_0 out_1 out_2 out_3 vdd gnd
* INPUT : in_0 
* INPUT : in_1 
* OUTPUT: out_0 
* OUTPUT: out_1 
* OUTPUT: out_2 
* OUTPUT: out_3 
* POWER : vdd 
* GROUND: gnd 
Xpre_inv_0
+ in_0 inbar_0 vdd gnd
+ sram_2_16_1_sky130_pinv_dec
Xpre_inv_1
+ in_1 inbar_1 vdd gnd
+ sram_2_16_1_sky130_pinv_dec
XXpre2x4_and_0
+ inbar_0 inbar_1 out_0 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XXpre2x4_and_1
+ in_0 inbar_1 out_1 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XXpre2x4_and_2
+ inbar_0 in_1 out_2 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XXpre2x4_and_3
+ in_0 in_1 out_3 vdd gnd
+ sram_2_16_1_sky130_and2_dec
.ENDS sram_2_16_1_sky130_hierarchical_predecode2x4
* Copyright 2020 The SkyWater PDK Authors
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     https://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*
* SPDX-License-Identifier: Apache-2.0

* NGSPICE file created from sky130_fd_bd_sram__openram_sp_nand3_dec.ext - technology: EFS8A


* Top level circuit sky130_fd_bd_sram__openram_sp_nand3_dec
.subckt sky130_fd_bd_sram__openram_sp_nand3_dec A B C Z VDD GND

X1001 Z A a_n346_328# GND sky130_fd_pr__nfet_01v8 W=0.74 L=0.15
X1002 a_n346_256# C GND GND sky130_fd_pr__nfet_01v8 W=0.74 L=0.15
X1003 a_n346_328# B a_n346_256# GND sky130_fd_pr__nfet_01v8 W=0.74 L=0.15
X1000 Z B VDD VDD sky130_fd_pr__pfet_01v8 W=1.12 L=0.15
X1004 Z A VDD VDD sky130_fd_pr__pfet_01v8 W=1.12 L=0.15
X1005 Z C VDD VDD sky130_fd_pr__pfet_01v8 W=1.12 L=0.15
.ends


.SUBCKT sram_2_16_1_sky130_and3_dec
+ A B C Z vdd gnd
* INPUT : A 
* INPUT : B 
* INPUT : C 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 1
Xpand3_dec_nand
+ A B C zb_int vdd gnd
+ sky130_fd_bd_sram__openram_sp_nand3_dec
Xpand3_dec_inv
+ zb_int Z vdd gnd
+ sram_2_16_1_sky130_pinv_dec
.ENDS sram_2_16_1_sky130_and3_dec

.SUBCKT sram_2_16_1_sky130_hierarchical_predecode3x8
+ in_0 in_1 in_2 out_0 out_1 out_2 out_3 out_4 out_5 out_6 out_7 vdd gnd
* INPUT : in_0 
* INPUT : in_1 
* INPUT : in_2 
* OUTPUT: out_0 
* OUTPUT: out_1 
* OUTPUT: out_2 
* OUTPUT: out_3 
* OUTPUT: out_4 
* OUTPUT: out_5 
* OUTPUT: out_6 
* OUTPUT: out_7 
* POWER : vdd 
* GROUND: gnd 
Xpre_inv_0
+ in_0 inbar_0 vdd gnd
+ sram_2_16_1_sky130_pinv_dec
Xpre_inv_1
+ in_1 inbar_1 vdd gnd
+ sram_2_16_1_sky130_pinv_dec
Xpre_inv_2
+ in_2 inbar_2 vdd gnd
+ sram_2_16_1_sky130_pinv_dec
XXpre3x8_and_0
+ inbar_0 inbar_1 inbar_2 out_0 vdd gnd
+ sram_2_16_1_sky130_and3_dec
XXpre3x8_and_1
+ in_0 inbar_1 inbar_2 out_1 vdd gnd
+ sram_2_16_1_sky130_and3_dec
XXpre3x8_and_2
+ inbar_0 in_1 inbar_2 out_2 vdd gnd
+ sram_2_16_1_sky130_and3_dec
XXpre3x8_and_3
+ in_0 in_1 inbar_2 out_3 vdd gnd
+ sram_2_16_1_sky130_and3_dec
XXpre3x8_and_4
+ inbar_0 inbar_1 in_2 out_4 vdd gnd
+ sram_2_16_1_sky130_and3_dec
XXpre3x8_and_5
+ in_0 inbar_1 in_2 out_5 vdd gnd
+ sram_2_16_1_sky130_and3_dec
XXpre3x8_and_6
+ inbar_0 in_1 in_2 out_6 vdd gnd
+ sram_2_16_1_sky130_and3_dec
XXpre3x8_and_7
+ in_0 in_1 in_2 out_7 vdd gnd
+ sram_2_16_1_sky130_and3_dec
.ENDS sram_2_16_1_sky130_hierarchical_predecode3x8

.SUBCKT sram_2_16_1_sky130_hierarchical_decoder
+ addr_0 addr_1 addr_2 addr_3 addr_4 decode_0 decode_1 decode_2 decode_3
+ decode_4 decode_5 decode_6 decode_7 decode_8 decode_9 decode_10
+ decode_11 decode_12 decode_13 decode_14 decode_15 decode_16 vdd gnd
* INPUT : addr_0 
* INPUT : addr_1 
* INPUT : addr_2 
* INPUT : addr_3 
* INPUT : addr_4 
* OUTPUT: decode_0 
* OUTPUT: decode_1 
* OUTPUT: decode_2 
* OUTPUT: decode_3 
* OUTPUT: decode_4 
* OUTPUT: decode_5 
* OUTPUT: decode_6 
* OUTPUT: decode_7 
* OUTPUT: decode_8 
* OUTPUT: decode_9 
* OUTPUT: decode_10 
* OUTPUT: decode_11 
* OUTPUT: decode_12 
* OUTPUT: decode_13 
* OUTPUT: decode_14 
* OUTPUT: decode_15 
* OUTPUT: decode_16 
* POWER : vdd 
* GROUND: gnd 
Xpre_0
+ addr_0 addr_1 out_0 out_1 out_2 out_3 vdd gnd
+ sram_2_16_1_sky130_hierarchical_predecode2x4
Xpre3x8_0
+ addr_2 addr_3 addr_4 out_4 out_5 out_6 out_7 out_8 out_9 out_10 out_11
+ vdd gnd
+ sram_2_16_1_sky130_hierarchical_predecode3x8
XDEC_AND_0
+ out_0 out_4 decode_0 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XDEC_AND_4
+ out_0 out_5 decode_4 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XDEC_AND_8
+ out_0 out_6 decode_8 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XDEC_AND_12
+ out_0 out_7 decode_12 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XDEC_AND_16
+ out_0 out_8 decode_16 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XDEC_AND_1
+ out_1 out_4 decode_1 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XDEC_AND_5
+ out_1 out_5 decode_5 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XDEC_AND_9
+ out_1 out_6 decode_9 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XDEC_AND_13
+ out_1 out_7 decode_13 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XDEC_AND_2
+ out_2 out_4 decode_2 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XDEC_AND_6
+ out_2 out_5 decode_6 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XDEC_AND_10
+ out_2 out_6 decode_10 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XDEC_AND_14
+ out_2 out_7 decode_14 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XDEC_AND_3
+ out_3 out_4 decode_3 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XDEC_AND_7
+ out_3 out_5 decode_7 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XDEC_AND_11
+ out_3 out_6 decode_11 vdd gnd
+ sram_2_16_1_sky130_and2_dec
XDEC_AND_15
+ out_3 out_7 decode_15 vdd gnd
+ sram_2_16_1_sky130_and2_dec
.ENDS sram_2_16_1_sky130_hierarchical_decoder

.SUBCKT sram_2_16_1_sky130_and2_dec_0
+ A B Z vdd gnd
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 1
Xpand2_dec_nand
+ A B zb_int vdd gnd
+ sky130_fd_bd_sram__openram_sp_nand2_dec
Xpand2_dec_inv
+ zb_int Z vdd gnd
+ sram_2_16_1_sky130_pinv_dec
.ENDS sram_2_16_1_sky130_and2_dec_0

.SUBCKT sram_2_16_1_sky130_wordline_driver
+ A B Z vdd gnd
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* cols: 3
Xwld_nand
+ A B zb_int vdd gnd
+ sky130_fd_bd_sram__openram_sp_nand2_dec
Xwl_driver
+ zb_int Z vdd gnd
+ sram_2_16_1_sky130_pinv_dec
.ENDS sram_2_16_1_sky130_wordline_driver

.SUBCKT sram_2_16_1_sky130_wordline_driver_array
+ in_0 in_1 in_2 in_3 in_4 in_5 in_6 in_7 in_8 in_9 in_10 in_11 in_12
+ in_13 in_14 in_15 in_16 wl_0 wl_1 wl_2 wl_3 wl_4 wl_5 wl_6 wl_7 wl_8
+ wl_9 wl_10 wl_11 wl_12 wl_13 wl_14 wl_15 wl_16 en vdd gnd
* INPUT : in_0 
* INPUT : in_1 
* INPUT : in_2 
* INPUT : in_3 
* INPUT : in_4 
* INPUT : in_5 
* INPUT : in_6 
* INPUT : in_7 
* INPUT : in_8 
* INPUT : in_9 
* INPUT : in_10 
* INPUT : in_11 
* INPUT : in_12 
* INPUT : in_13 
* INPUT : in_14 
* INPUT : in_15 
* INPUT : in_16 
* OUTPUT: wl_0 
* OUTPUT: wl_1 
* OUTPUT: wl_2 
* OUTPUT: wl_3 
* OUTPUT: wl_4 
* OUTPUT: wl_5 
* OUTPUT: wl_6 
* OUTPUT: wl_7 
* OUTPUT: wl_8 
* OUTPUT: wl_9 
* OUTPUT: wl_10 
* OUTPUT: wl_11 
* OUTPUT: wl_12 
* OUTPUT: wl_13 
* OUTPUT: wl_14 
* OUTPUT: wl_15 
* OUTPUT: wl_16 
* INPUT : en 
* POWER : vdd 
* GROUND: gnd 
* rows: 17 cols: 3
Xwl_driver_and0
+ in_0 en wl_0 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
Xwl_driver_and1
+ in_1 en wl_1 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
Xwl_driver_and2
+ in_2 en wl_2 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
Xwl_driver_and3
+ in_3 en wl_3 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
Xwl_driver_and4
+ in_4 en wl_4 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
Xwl_driver_and5
+ in_5 en wl_5 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
Xwl_driver_and6
+ in_6 en wl_6 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
Xwl_driver_and7
+ in_7 en wl_7 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
Xwl_driver_and8
+ in_8 en wl_8 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
Xwl_driver_and9
+ in_9 en wl_9 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
Xwl_driver_and10
+ in_10 en wl_10 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
Xwl_driver_and11
+ in_11 en wl_11 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
Xwl_driver_and12
+ in_12 en wl_12 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
Xwl_driver_and13
+ in_13 en wl_13 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
Xwl_driver_and14
+ in_14 en wl_14 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
Xwl_driver_and15
+ in_15 en wl_15 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
Xwl_driver_and16
+ in_16 en wl_16 vdd gnd
+ sram_2_16_1_sky130_wordline_driver
.ENDS sram_2_16_1_sky130_wordline_driver_array

.SUBCKT sram_2_16_1_sky130_port_address
+ addr_0 addr_1 addr_2 addr_3 addr_4 wl_en wl_0 wl_1 wl_2 wl_3 wl_4 wl_5
+ wl_6 wl_7 wl_8 wl_9 wl_10 wl_11 wl_12 wl_13 wl_14 wl_15 wl_16 rbl_wl
+ vdd gnd
* INPUT : addr_0 
* INPUT : addr_1 
* INPUT : addr_2 
* INPUT : addr_3 
* INPUT : addr_4 
* INPUT : wl_en 
* OUTPUT: wl_0 
* OUTPUT: wl_1 
* OUTPUT: wl_2 
* OUTPUT: wl_3 
* OUTPUT: wl_4 
* OUTPUT: wl_5 
* OUTPUT: wl_6 
* OUTPUT: wl_7 
* OUTPUT: wl_8 
* OUTPUT: wl_9 
* OUTPUT: wl_10 
* OUTPUT: wl_11 
* OUTPUT: wl_12 
* OUTPUT: wl_13 
* OUTPUT: wl_14 
* OUTPUT: wl_15 
* OUTPUT: wl_16 
* OUTPUT: rbl_wl 
* POWER : vdd 
* GROUND: gnd 
Xrow_decoder
+ addr_0 addr_1 addr_2 addr_3 addr_4 dec_out_0 dec_out_1 dec_out_2
+ dec_out_3 dec_out_4 dec_out_5 dec_out_6 dec_out_7 dec_out_8 dec_out_9
+ dec_out_10 dec_out_11 dec_out_12 dec_out_13 dec_out_14 dec_out_15
+ dec_out_16 vdd gnd
+ sram_2_16_1_sky130_hierarchical_decoder
Xwordline_driver
+ dec_out_0 dec_out_1 dec_out_2 dec_out_3 dec_out_4 dec_out_5 dec_out_6
+ dec_out_7 dec_out_8 dec_out_9 dec_out_10 dec_out_11 dec_out_12
+ dec_out_13 dec_out_14 dec_out_15 dec_out_16 wl_0 wl_1 wl_2 wl_3 wl_4
+ wl_5 wl_6 wl_7 wl_8 wl_9 wl_10 wl_11 wl_12 wl_13 wl_14 wl_15 wl_16
+ wl_en vdd gnd
+ sram_2_16_1_sky130_wordline_driver_array
Xrbl_driver
+ wl_en vdd rbl_wl vdd gnd
+ sram_2_16_1_sky130_and2_dec_0
.ENDS sram_2_16_1_sky130_port_address
* NGSPICE file created from sky130_fd_bd_sram__sram_sp_colenda_cent.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_colenda_cent VPWR VPB VNB
.ends
* NGSPICE file created from sky130_fd_bd_sram__sram_sp_colenda.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_colenda bl vdd gnd br gate vpb vnb
*X0 br gate br vnb sky130_fd_pr__special_nfet_pass w=0.065u l=0.17u
.ends

* NGSPICE file created from sky130_fd_bd_sram__sram_sp_colenda_p_cent.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_colenda_p_cent VGND VPB VNB
.ends

.SUBCKT sram_2_16_1_sky130_sky130_col_cap_array_0
+ fake_bl_0 fake_br_0 fake_bl_1 fake_br_1 fake_bl_2 fake_br_2 vdd gnd
+ gate
* OUTPUT: fake_bl_0 
* OUTPUT: fake_br_0 
* OUTPUT: fake_bl_1 
* OUTPUT: fake_br_1 
* OUTPUT: fake_bl_2 
* OUTPUT: fake_br_2 
* POWER : vdd 
* GROUND: gnd 
* BIAS  : gate 
Xrca_bottom_0
+ fake_bl_0 vdd gnd fake_br_0 gate vdd gnd
+ sky130_fd_bd_sram__sram_sp_colenda
Xrca_bottom_1
+ vdd vdd gnd
+ sky130_fd_bd_sram__sram_sp_colenda_cent
Xrca_bottom_2
+ fake_bl_1 vdd gnd fake_br_1 gate vdd gnd
+ sky130_fd_bd_sram__sram_sp_colenda
Xrca_bottom_3
+ gnd vdd vnb
+ sky130_fd_bd_sram__sram_sp_colenda_p_cent
Xrca_bottom_4
+ fake_bl_2 vdd gnd fake_br_2 gate vdd gnd
+ sky130_fd_bd_sram__sram_sp_colenda
.ENDS sram_2_16_1_sky130_sky130_col_cap_array_0
* NGSPICE file created from sky130_fd_bd_sram__sram_sp_wlstrap_p.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_wlstrap_p VGND
.ends
* NGSPICE file created from sky130_fd_bd_sram__openram_sp_cell_opt1a_replica.ext - technology: sky130A

.subckt sky130_fd_bd_sram__openram_sp_cell_opt1a_replica BL BR VGND VPWR VPB VNB WL
X0 VPWR WL BR VNB sky130_fd_pr__special_nfet_pass ad=4.375e+10p pd=920000u as=1.68e+10p ps=520000u w=140000u l=150000u
X1 Q VPWR VGND VNB sky130_fd_pr__special_nfet_latch ad=1.56e+11p pd=2.38e+06u as=8.08e+10p ps=1.28e+06u w=210000u l=150000u
X2 BL WL Q VNB sky130_fd_pr__special_nfet_pass ad=1.68e+10p pd=520000u as=4.25e+10p ps=920000u w=140000u l=150000u
*X3 Q WL Q VPB sky130_fd_pr__special_pfet_pass ad=3.5e+10p pd=780000u as=0p ps=0u w=70000u l=95000u
*X4 VPWR WL VPWR VPB sky130_fd_pr__special_pfet_pass ad=9.72e+10p pd=1.86e+06u as=0p ps=0u w=70000u l=95000u
X5 VPWR Q VPWR VPB sky130_fd_pr__special_pfet_pass ad=0p pd=0u as=0p ps=0u w=140000u l=150000u
X6 Q VPWR VPWR VPB sky130_fd_pr__special_pfet_pass ad=0p pd=0u as=0p ps=0u w=140000u l=150000u
X7 VGND Q VPWR VNB sky130_fd_pr__special_nfet_latch ad=0p pd=0u as=0p ps=0u w=210000u l=150000u
.ends
* NGSPICE file created from sky130_fd_bd_sram__sram_sp_colend_p_cent.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_colend_p_cent VGND VPB VNB
.ends
* NGSPICE file created from sky130_fd_bd_sram__sram_sp_wlstrapa_p.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_wlstrapa_p VGND
.ends
* NGSPICE file created from sky130_fd_bd_sram__openram_sp_cell_opt1_replica.ext - technology: sky130A

.subckt sky130_fd_bd_sram__openram_sp_cell_opt1_replica BL BR VGND VPWR VPB VNB WL
X0 VPWR WL BR VNB sky130_fd_pr__special_nfet_pass ad=4.375e+10p pd=920000u as=1.68e+10p ps=520000u w=140000u l=150000u
X1 Q VPWR VGND VNB sky130_fd_pr__special_nfet_latch ad=1.56e+11p pd=2.38e+06u as=8.08e+10p ps=1.28e+06u w=210000u l=150000u
X2 BL WL Q VNB sky130_fd_pr__special_nfet_pass ad=1.68e+10p pd=520000u as=4.25e+10p ps=920000u w=140000u l=150000u
*X3 Q WL Q VPB sky130_fd_pr__special_pfet_pass ad=3.5e+10p pd=780000u as=0p ps=0u w=70000u l=95000u
*X4 VPWR WL VPWR VPB sky130_fd_pr__special_pfet_pass ad=9.72e+10p pd=1.86e+06u as=0p ps=0u w=70000u l=95000u
X5 VPWR Q VPWR VPB sky130_fd_pr__special_pfet_pass ad=0p pd=0u as=0p ps=0u w=140000u l=150000u
X6 Q VPWR VPWR VPB sky130_fd_pr__special_pfet_pass ad=0p pd=0u as=0p ps=0u w=140000u l=150000u
X7 VGND Q VPWR VNB sky130_fd_pr__special_nfet_latch ad=0p pd=0u as=0p ps=0u w=210000u l=150000u
.ends
* NGSPICE file created from sky130_fd_bd_sram__sram_sp_colend.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_colend bl vdd gnd br gate vpb vnb
*X0 br gate br vnb sky130_fd_pr__special_nfet_pass w=0.07u l=0.21u
.ends


.SUBCKT sram_2_16_1_sky130_sky130_replica_column
+ bl_0_0 br_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8
+ wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 wl_0_16 wl_0_17
+ wl_0_18 vdd gnd top_gate bot_gate
* OUTPUT: bl_0_0 
* OUTPUT: br_0_0 
* INPUT : wl_0_1 
* INPUT : wl_0_2 
* INPUT : wl_0_3 
* INPUT : wl_0_4 
* INPUT : wl_0_5 
* INPUT : wl_0_6 
* INPUT : wl_0_7 
* INPUT : wl_0_8 
* INPUT : wl_0_9 
* INPUT : wl_0_10 
* INPUT : wl_0_11 
* INPUT : wl_0_12 
* INPUT : wl_0_13 
* INPUT : wl_0_14 
* INPUT : wl_0_15 
* INPUT : wl_0_16 
* INPUT : wl_0_17 
* INPUT : wl_0_18 
* POWER : vdd 
* GROUND: gnd 
* INPUT : top_gate 
* INPUT : bot_gate 
Xrbc_0
+ bl_0_0 vdd gnd br_0_0 top_gate vdd gnd
+ sky130_fd_bd_sram__sram_sp_colend
Xrbc_0_cap
+ gnd vdd gnd
+ sky130_fd_bd_sram__sram_sp_colend_p_cent
Xrbc_1
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_1
+ sky130_fd_bd_sram__openram_sp_cell_opt1_replica
Xrbc_1_strap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrbc_2
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_2
+ sky130_fd_bd_sram__openram_sp_cell_opt1a_replica
Xrbc_2_strap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrbc_3
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_3
+ sky130_fd_bd_sram__openram_sp_cell_opt1_replica
Xrbc_3_strap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrbc_4
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_4
+ sky130_fd_bd_sram__openram_sp_cell_opt1a_replica
Xrbc_4_strap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrbc_5
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_5
+ sky130_fd_bd_sram__openram_sp_cell_opt1_replica
Xrbc_5_strap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrbc_6
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_6
+ sky130_fd_bd_sram__openram_sp_cell_opt1a_replica
Xrbc_6_strap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrbc_7
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_7
+ sky130_fd_bd_sram__openram_sp_cell_opt1_replica
Xrbc_7_strap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrbc_8
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_8
+ sky130_fd_bd_sram__openram_sp_cell_opt1a_replica
Xrbc_8_strap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrbc_9
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_9
+ sky130_fd_bd_sram__openram_sp_cell_opt1_replica
Xrbc_9_strap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrbc_10
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_10
+ sky130_fd_bd_sram__openram_sp_cell_opt1a_replica
Xrbc_10_strap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrbc_11
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_11
+ sky130_fd_bd_sram__openram_sp_cell_opt1_replica
Xrbc_11_strap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrbc_12
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_12
+ sky130_fd_bd_sram__openram_sp_cell_opt1a_replica
Xrbc_12_strap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrbc_13
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_13
+ sky130_fd_bd_sram__openram_sp_cell_opt1_replica
Xrbc_13_strap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrbc_14
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_14
+ sky130_fd_bd_sram__openram_sp_cell_opt1a_replica
Xrbc_14_strap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrbc_15
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_15
+ sky130_fd_bd_sram__openram_sp_cell_opt1_replica
Xrbc_15_strap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrbc_16
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_16
+ sky130_fd_bd_sram__openram_sp_cell_opt1a_replica
Xrbc_16_strap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrbc_17
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_17
+ sky130_fd_bd_sram__openram_sp_cell_opt1_replica
Xrbc_17_strap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrbc_18
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_18
+ sky130_fd_bd_sram__openram_sp_cell_opt1a_replica
Xrbc_18_strap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrbc_19
+ bl_0_0 vdd gnd br_0_0 bot_gate vdd gnd
+ sky130_fd_bd_sram__sram_sp_colenda
Xrbc_19_cap
+ gnd vdd gnd
+ sky130_fd_bd_sram__sram_sp_colenda_p_cent
.ENDS sram_2_16_1_sky130_sky130_replica_column
* NGSPICE file created from sky130_fd_bd_sram__sram_sp_colend_cent.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_colend_cent VPWR VPB VNB
.ends

.SUBCKT sram_2_16_1_sky130_sky130_col_cap_array
+ fake_bl_0 fake_br_0 fake_bl_1 fake_br_1 fake_bl_2 fake_br_2 vdd gnd
+ gate
* OUTPUT: fake_bl_0 
* OUTPUT: fake_br_0 
* OUTPUT: fake_bl_1 
* OUTPUT: fake_br_1 
* OUTPUT: fake_bl_2 
* OUTPUT: fake_br_2 
* POWER : vdd 
* GROUND: gnd 
* BIAS  : gate 
Xrca_top_0
+ fake_bl_0 vdd gnd fake_br_0 gate vdd gnd
+ sky130_fd_bd_sram__sram_sp_colend
Xrca_top_1
+ vdd vdd gnd
+ sky130_fd_bd_sram__sram_sp_colend_cent
Xrca_top_2
+ fake_bl_1 vdd gnd fake_br_1 gate vdd gnd
+ sky130_fd_bd_sram__sram_sp_colend
Xrca_top_3
+ gnd vdd vnb
+ sky130_fd_bd_sram__sram_sp_colend_p_cent
Xrca_top_4
+ fake_bl_2 vdd gnd fake_br_2 gate vdd gnd
+ sky130_fd_bd_sram__sram_sp_colend
.ENDS sram_2_16_1_sky130_sky130_col_cap_array
* NGSPICE file created from sky130_fd_bd_sram__sram_sp_wlstrapa.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_wlstrapa VPWR
.ends
* NGSPICE file created from sky130_fd_bd_sram__openram_sp_cell_opt1a_dummy.ext - technology: sky130A

.subckt sky130_fd_bd_sram__openram_sp_cell_opt1a_dummy BL BR VGND VPWR VPB VNB WL
X0 ll WL BR VNB sky130_fd_pr__special_nfet_pass w=0.14 l=0.15
X1 ul Q_bar_float VGND VNB sky130_fd_pr__special_nfet_latch w=0.21 l=0.15
X2 BL WL ul VNB sky130_fd_pr__special_nfet_pass w=0.14 l=0.15
*X3 ur WL ur VPB sky130_fd_pr__special_pfet_pass w=0.07 l=0.095
*X4 lr WL lr VPB sky130_fd_pr__special_pfet_pass w=0.07 l=0.095
X5 VPWR Q_float lr VPB sky130_fd_pr__special_pfet_pass w=0.14 l=0.15
X6 ur Q_bar_float VPWR VPB sky130_fd_pr__special_pfet_pass w=0.14 l=0.15
X7 VGND Q_float ll VNB sky130_fd_pr__special_nfet_latch w=0.21 l=0.15
.ends

.SUBCKT sram_2_16_1_sky130_sky130_dummy_array
+ bl_0_0 br_0_0 bl_0_1 br_0_1 bl_0_2 br_0_2 wl_0_0 vdd gnd
* INOUT : bl_0_0 
* INOUT : br_0_0 
* INOUT : bl_0_1 
* INOUT : br_0_1 
* INOUT : bl_0_2 
* INOUT : br_0_2 
* INPUT : wl_0_0 
* POWER : vdd 
* GROUND: gnd 
Xrow_0_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_0
+ sky130_fd_bd_sram__openram_sp_cell_opt1a_dummy
Xrow_0_col_0_wlstrapa
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa
Xrow_0_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_0
+ sky130_fd_bd_sram__openram_sp_cell_opt1a_dummy
Xrow_0_col_1_wlstrap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrow_0_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_0
+ sky130_fd_bd_sram__openram_sp_cell_opt1a_dummy
.ENDS sram_2_16_1_sky130_sky130_dummy_array
* NGSPICE file created from sky130_fd_bd_sram__sram_sp_cornera.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_cornera VNB VPWR VPB
.ends
* NGSPICE file created from sky130_fd_bd_sram__sram_sp_cornerb.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_cornerb VPWR VPB VNB
.ends
* NGSPICE file created from sky130_fd_bd_sram__sram_sp_rowenda.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_rowenda VPWR WL
.ends
* NGSPICE file created from sky130_fd_bd_sram__sram_sp_rowend.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_rowend VPWR WL
.ends

.SUBCKT sram_2_16_1_sky130_sky130_row_cap_array_0
+ wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9
+ wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 wl_0_16 wl_0_17
+ wl_0_18 wl_0_19 vdd gnd
* OUTPUT: wl_0_0 
* OUTPUT: wl_0_1 
* OUTPUT: wl_0_2 
* OUTPUT: wl_0_3 
* OUTPUT: wl_0_4 
* OUTPUT: wl_0_5 
* OUTPUT: wl_0_6 
* OUTPUT: wl_0_7 
* OUTPUT: wl_0_8 
* OUTPUT: wl_0_9 
* OUTPUT: wl_0_10 
* OUTPUT: wl_0_11 
* OUTPUT: wl_0_12 
* OUTPUT: wl_0_13 
* OUTPUT: wl_0_14 
* OUTPUT: wl_0_15 
* OUTPUT: wl_0_16 
* OUTPUT: wl_0_17 
* OUTPUT: wl_0_18 
* OUTPUT: wl_0_19 
* POWER : vdd 
* GROUND: gnd 
Xrca_0
+ vdd gnd vdd
+ sky130_fd_bd_sram__sram_sp_cornera
Xrca_1
+ wl_0_0 vdd
+ sky130_fd_bd_sram__sram_sp_rowenda
Xrca_2
+ wl_0_1 vdd
+ sky130_fd_bd_sram__sram_sp_rowend
Xrca_3
+ wl_0_2 vdd
+ sky130_fd_bd_sram__sram_sp_rowenda
Xrca_4
+ wl_0_3 vdd
+ sky130_fd_bd_sram__sram_sp_rowend
Xrca_5
+ wl_0_4 vdd
+ sky130_fd_bd_sram__sram_sp_rowenda
Xrca_6
+ wl_0_5 vdd
+ sky130_fd_bd_sram__sram_sp_rowend
Xrca_7
+ wl_0_6 vdd
+ sky130_fd_bd_sram__sram_sp_rowenda
Xrca_8
+ wl_0_7 vdd
+ sky130_fd_bd_sram__sram_sp_rowend
Xrca_9
+ wl_0_8 vdd
+ sky130_fd_bd_sram__sram_sp_rowenda
Xrca_10
+ wl_0_9 vdd
+ sky130_fd_bd_sram__sram_sp_rowend
Xrca_11
+ wl_0_10 vdd
+ sky130_fd_bd_sram__sram_sp_rowenda
Xrca_12
+ wl_0_11 vdd
+ sky130_fd_bd_sram__sram_sp_rowend
Xrca_13
+ wl_0_12 vdd
+ sky130_fd_bd_sram__sram_sp_rowenda
Xrca_14
+ wl_0_13 vdd
+ sky130_fd_bd_sram__sram_sp_rowend
Xrca_15
+ wl_0_14 vdd
+ sky130_fd_bd_sram__sram_sp_rowenda
Xrca_16
+ wl_0_15 vdd
+ sky130_fd_bd_sram__sram_sp_rowend
Xrca_17
+ wl_0_16 vdd
+ sky130_fd_bd_sram__sram_sp_rowenda
Xrca_18
+ wl_0_17 vdd
+ sky130_fd_bd_sram__sram_sp_rowend
Xrca_19
+ vdd gnd vdd
+ sky130_fd_bd_sram__sram_sp_cornerb
.ENDS sram_2_16_1_sky130_sky130_row_cap_array_0
* NGSPICE file created from sky130_fd_bd_sram__sram_sp_cell_opt1a.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_cell_opt1a BL BR VGND VPWR VPB VNB WL
X0 Q_bar WL BR VNB sky130_fd_pr__special_nfet_pass w=0.14 l=0.15
X1 Q Q_bar VGND VNB sky130_fd_pr__special_nfet_latch w=0.21 l=0.15
X2 BL WL Q VNB sky130_fd_pr__special_nfet_pass w=0.14 l=0.15
*X3 Q WL Q VPB sky130_fd_pr__special_pfet_pass w=0.07 l=0.095
*X4 Q_bar WL Q_bar VPB sky130_fd_pr__special_pfet_pass w=0.07 l=0.095
X5 VPWR Q Q_bar VPB sky130_fd_pr__special_pfet_pass w=0.14 l=0.15
X6 Q Q_bar VPWR VPB sky130_fd_pr__special_pfet_pass w=0.14 l=0.15
X7 VGND Q Q_bar VNB sky130_fd_pr__special_nfet_latch w=0.21 l=0.15
.ends
* NGSPICE file created from sky130_fd_bd_sram__sram_sp_cell_opt1.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_cell_opt1 BL BR VGND VPWR VPB VNB WL
X0 Q_bar WL BR VNB sky130_fd_pr__special_nfet_pass w=0.14 l=0.15
X1 Q Q_bar VGND VNB sky130_fd_pr__special_nfet_latch w=0.21 l=0.15
X2 BL WL Q VNB sky130_fd_pr__special_nfet_pass w=0.14 l=0.15
*X3 Q WL Q VPB sky130_fd_pr__special_pfet_pass w=0.07 l=0.095
*X4 Q_bar WL Q_bar VPB sky130_fd_pr__special_pfet_pass w=0.07 l=0.095
X5 VPWR Q Q_bar VPB sky130_fd_pr__special_pfet_pass w=0.14 l=0.15
X6 Q Q_bar VPWR VPB sky130_fd_pr__special_pfet_pass w=0.14 l=0.15
X7 VGND Q Q_bar VNB sky130_fd_pr__special_nfet_latch w=0.21 l=0.15
.ends
* NGSPICE file created from sky130_fd_bd_sram__sram_sp_wlstrap.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_wlstrap VPWR
.ends

.SUBCKT sram_2_16_1_sky130_sky130_bitcell_array
+ bl_0_0 br_0_0 bl_0_1 br_0_1 bl_0_2 br_0_2 wl_0_0 wl_0_1 wl_0_2 wl_0_3
+ wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12
+ wl_0_13 wl_0_14 wl_0_15 wl_0_16 vdd gnd
* INOUT : bl_0_0 
* INOUT : br_0_0 
* INOUT : bl_0_1 
* INOUT : br_0_1 
* INOUT : bl_0_2 
* INOUT : br_0_2 
* INPUT : wl_0_0 
* INPUT : wl_0_1 
* INPUT : wl_0_2 
* INPUT : wl_0_3 
* INPUT : wl_0_4 
* INPUT : wl_0_5 
* INPUT : wl_0_6 
* INPUT : wl_0_7 
* INPUT : wl_0_8 
* INPUT : wl_0_9 
* INPUT : wl_0_10 
* INPUT : wl_0_11 
* INPUT : wl_0_12 
* INPUT : wl_0_13 
* INPUT : wl_0_14 
* INPUT : wl_0_15 
* INPUT : wl_0_16 
* POWER : vdd 
* GROUND: gnd 
* rows: 17 cols: 3
Xrow_0_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_0
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_0_col_0_wlstrap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrap
Xrow_0_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_0
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_0_col_1_wlstrap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrow_0_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_0
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_1_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_1
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_1_col_0_wlstrapa
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa
Xrow_1_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_1
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_1_col_1_wlstrapa_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrow_1_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_1
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_2_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_2
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_2_col_0_wlstrap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrap
Xrow_2_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_2
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_2_col_1_wlstrap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrow_2_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_2
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_3_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_3
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_3_col_0_wlstrapa
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa
Xrow_3_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_3
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_3_col_1_wlstrapa_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrow_3_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_3
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_4_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_4
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_4_col_0_wlstrap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrap
Xrow_4_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_4
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_4_col_1_wlstrap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrow_4_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_4
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_5_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_5
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_5_col_0_wlstrapa
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa
Xrow_5_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_5
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_5_col_1_wlstrapa_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrow_5_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_5
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_6_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_6
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_6_col_0_wlstrap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrap
Xrow_6_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_6
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_6_col_1_wlstrap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrow_6_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_6
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_7_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_7
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_7_col_0_wlstrapa
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa
Xrow_7_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_7
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_7_col_1_wlstrapa_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrow_7_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_7
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_8_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_8
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_8_col_0_wlstrap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrap
Xrow_8_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_8
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_8_col_1_wlstrap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrow_8_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_8
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_9_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_9
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_9_col_0_wlstrapa
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa
Xrow_9_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_9
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_9_col_1_wlstrapa_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrow_9_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_9
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_10_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_10
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_10_col_0_wlstrap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrap
Xrow_10_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_10
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_10_col_1_wlstrap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrow_10_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_10
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_11_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_11
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_11_col_0_wlstrapa
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa
Xrow_11_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_11
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_11_col_1_wlstrapa_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrow_11_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_11
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_12_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_12
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_12_col_0_wlstrap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrap
Xrow_12_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_12
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_12_col_1_wlstrap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrow_12_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_12
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_13_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_13
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_13_col_0_wlstrapa
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa
Xrow_13_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_13
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_13_col_1_wlstrapa_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrow_13_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_13
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_14_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_14
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_14_col_0_wlstrap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrap
Xrow_14_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_14
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_14_col_1_wlstrap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrow_14_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_14
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_15_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_15
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_15_col_0_wlstrapa
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrapa
Xrow_15_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_15
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_15_col_1_wlstrapa_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrapa_p
Xrow_15_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_15
+ sky130_fd_bd_sram__sram_sp_cell_opt1a
Xrow_16_col_0_bitcell
+ bl_0_0 br_0_0 gnd vdd vdd gnd wl_0_16
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_16_col_0_wlstrap
+ vdd
+ sky130_fd_bd_sram__sram_sp_wlstrap
Xrow_16_col_1_bitcell
+ bl_0_1 br_0_1 gnd vdd vdd gnd wl_0_16
+ sky130_fd_bd_sram__sram_sp_cell_opt1
Xrow_16_col_1_wlstrap_p
+ gnd
+ sky130_fd_bd_sram__sram_sp_wlstrap_p
Xrow_16_col_2_bitcell
+ bl_0_2 br_0_2 gnd vdd vdd gnd wl_0_16
+ sky130_fd_bd_sram__sram_sp_cell_opt1
.ENDS sram_2_16_1_sky130_sky130_bitcell_array
* NGSPICE file created from sky130_fd_bd_sram__sram_sp_corner.ext - technology: sky130A

.subckt sky130_fd_bd_sram__sram_sp_corner VPWR VPB VNB
.ends
* NGSPICE file created from sky130_fd_bd_sram__openram_sp_rowenda_replica.ext - technology: sky130A

.subckt sky130_fd_bd_sram__openram_sp_rowenda_replica VPWR WL
.ends
* NGSPICE file created from sky130_fd_bd_sram__openram_sp_rowend_replica.ext - technology: sky130A

.subckt sky130_fd_bd_sram__openram_sp_rowend_replica VPWR WL
.ends

.SUBCKT sram_2_16_1_sky130_sky130_row_cap_array
+ wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9
+ wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 wl_0_16 wl_0_17
+ wl_0_18 wl_0_19 vdd gnd
* OUTPUT: wl_0_0 
* OUTPUT: wl_0_1 
* OUTPUT: wl_0_2 
* OUTPUT: wl_0_3 
* OUTPUT: wl_0_4 
* OUTPUT: wl_0_5 
* OUTPUT: wl_0_6 
* OUTPUT: wl_0_7 
* OUTPUT: wl_0_8 
* OUTPUT: wl_0_9 
* OUTPUT: wl_0_10 
* OUTPUT: wl_0_11 
* OUTPUT: wl_0_12 
* OUTPUT: wl_0_13 
* OUTPUT: wl_0_14 
* OUTPUT: wl_0_15 
* OUTPUT: wl_0_16 
* OUTPUT: wl_0_17 
* OUTPUT: wl_0_18 
* OUTPUT: wl_0_19 
* POWER : vdd 
* GROUND: gnd 
Xrca_0
+ vdd gnd vdd
+ sky130_fd_bd_sram__sram_sp_cornera
Xrca_1
+ wl_0_0 vdd
+ sky130_fd_bd_sram__openram_sp_rowenda_replica
Xrca_2
+ wl_0_1 vdd
+ sky130_fd_bd_sram__openram_sp_rowend_replica
Xrca_3
+ wl_0_2 vdd
+ sky130_fd_bd_sram__openram_sp_rowenda_replica
Xrca_4
+ wl_0_3 vdd
+ sky130_fd_bd_sram__openram_sp_rowend_replica
Xrca_5
+ wl_0_4 vdd
+ sky130_fd_bd_sram__openram_sp_rowenda_replica
Xrca_6
+ wl_0_5 vdd
+ sky130_fd_bd_sram__openram_sp_rowend_replica
Xrca_7
+ wl_0_6 vdd
+ sky130_fd_bd_sram__openram_sp_rowenda_replica
Xrca_8
+ wl_0_7 vdd
+ sky130_fd_bd_sram__openram_sp_rowend_replica
Xrca_9
+ wl_0_8 vdd
+ sky130_fd_bd_sram__openram_sp_rowenda_replica
Xrca_10
+ wl_0_9 vdd
+ sky130_fd_bd_sram__openram_sp_rowend_replica
Xrca_11
+ wl_0_10 vdd
+ sky130_fd_bd_sram__openram_sp_rowenda_replica
Xrca_12
+ wl_0_11 vdd
+ sky130_fd_bd_sram__openram_sp_rowend_replica
Xrca_13
+ wl_0_12 vdd
+ sky130_fd_bd_sram__openram_sp_rowenda_replica
Xrca_14
+ wl_0_13 vdd
+ sky130_fd_bd_sram__openram_sp_rowend_replica
Xrca_15
+ wl_0_14 vdd
+ sky130_fd_bd_sram__openram_sp_rowenda_replica
Xrca_16
+ wl_0_15 vdd
+ sky130_fd_bd_sram__openram_sp_rowend_replica
Xrca_17
+ wl_0_16 vdd
+ sky130_fd_bd_sram__openram_sp_rowenda_replica
Xrca_18
+ wl_0_17 vdd
+ sky130_fd_bd_sram__openram_sp_rowend_replica
Xrca_19
+ vdd gnd vdd
+ sky130_fd_bd_sram__sram_sp_corner
.ENDS sram_2_16_1_sky130_sky130_row_cap_array

.SUBCKT sram_2_16_1_sky130_sky130_replica_bitcell_array
+ rbl_bl_0_0 rbl_br_0_0 bl_0_0 br_0_0 bl_0_1 br_0_1 bl_0_2 br_0_2
+ rbl_wl_0_0 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7
+ wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 wl_0_16
+ vdd gnd
* INOUT : rbl_bl_0_0 
* INOUT : rbl_br_0_0 
* INOUT : bl_0_0 
* INOUT : br_0_0 
* INOUT : bl_0_1 
* INOUT : br_0_1 
* INOUT : bl_0_2 
* INOUT : br_0_2 
* INPUT : rbl_wl_0_0 
* INPUT : wl_0_0 
* INPUT : wl_0_1 
* INPUT : wl_0_2 
* INPUT : wl_0_3 
* INPUT : wl_0_4 
* INPUT : wl_0_5 
* INPUT : wl_0_6 
* INPUT : wl_0_7 
* INPUT : wl_0_8 
* INPUT : wl_0_9 
* INPUT : wl_0_10 
* INPUT : wl_0_11 
* INPUT : wl_0_12 
* INPUT : wl_0_13 
* INPUT : wl_0_14 
* INPUT : wl_0_15 
* INPUT : wl_0_16 
* POWER : vdd 
* GROUND: gnd 
* rows: 17 cols: 3
* rbl: [1, 0] left_rbl: [0] right_rbl: []
Xbitcell_array
+ bl_0_0 br_0_0 bl_0_1 br_0_1 bl_0_2 br_0_2 wl_0_0 wl_0_1 wl_0_2 wl_0_3
+ wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12
+ wl_0_13 wl_0_14 wl_0_15 wl_0_16 vdd gnd
+ sram_2_16_1_sky130_sky130_bitcell_array
Xreplica_col_0
+ rbl_bl_0_0 rbl_br_0_0 rbl_wl_0_0 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4
+ wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13
+ wl_0_14 wl_0_15 wl_0_16 vdd gnd gnd gnd
+ sram_2_16_1_sky130_sky130_replica_column
Xdummy_row_0
+ bl_0_0 br_0_0 bl_0_1 br_0_1 bl_0_2 br_0_2 rbl_wl_0_0 vdd gnd
+ sram_2_16_1_sky130_sky130_dummy_array
Xdummy_row_bot
+ bl_0_0 br_0_0 bl_0_1 br_0_1 bl_0_2 br_0_2 vdd gnd gnd
+ sram_2_16_1_sky130_sky130_col_cap_array_0
Xdummy_row_top
+ bl_0_0 br_0_0 bl_0_1 br_0_1 bl_0_2 br_0_2 vdd gnd gnd
+ sram_2_16_1_sky130_sky130_col_cap_array
Xdummy_col_left
+ gnd rbl_wl_0_0 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7
+ wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 wl_0_16
+ gnd vdd gnd
+ sram_2_16_1_sky130_sky130_row_cap_array
Xdummy_col_right
+ gnd rbl_wl_0_0 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7
+ wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 wl_0_16
+ gnd vdd gnd
+ sram_2_16_1_sky130_sky130_row_cap_array_0
.ENDS sram_2_16_1_sky130_sky130_replica_bitcell_array

.SUBCKT sram_2_16_1_sky130_sky130_capped_replica_bitcell_array
+ rbl_bl_0_0 rbl_br_0_0 bl_0_0 br_0_0 bl_0_1 br_0_1 bl_0_2 br_0_2
+ rbl_wl_0_0 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7
+ wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 wl_0_16
+ vdd gnd
* INOUT : rbl_bl_0_0 
* INOUT : rbl_br_0_0 
* INOUT : bl_0_0 
* INOUT : br_0_0 
* INOUT : bl_0_1 
* INOUT : br_0_1 
* INOUT : bl_0_2 
* INOUT : br_0_2 
* INPUT : rbl_wl_0_0 
* INPUT : wl_0_0 
* INPUT : wl_0_1 
* INPUT : wl_0_2 
* INPUT : wl_0_3 
* INPUT : wl_0_4 
* INPUT : wl_0_5 
* INPUT : wl_0_6 
* INPUT : wl_0_7 
* INPUT : wl_0_8 
* INPUT : wl_0_9 
* INPUT : wl_0_10 
* INPUT : wl_0_11 
* INPUT : wl_0_12 
* INPUT : wl_0_13 
* INPUT : wl_0_14 
* INPUT : wl_0_15 
* INPUT : wl_0_16 
* POWER : vdd 
* GROUND: gnd 
* rows: 17 cols: 3
* rbl: [1, 0] left_rbl: [0] right_rbl: []
Xreplica_bitcell_array
+ rbl_bl_0_0 rbl_br_0_0 bl_0_0 br_0_0 bl_0_1 br_0_1 bl_0_2 br_0_2
+ rbl_wl_0_0 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7
+ wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 wl_0_16
+ vdd gnd
+ sram_2_16_1_sky130_sky130_replica_bitcell_array
.ENDS sram_2_16_1_sky130_sky130_capped_replica_bitcell_array
* Copyright 2020 The SkyWater PDK Authors
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     https://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*
* SPDX-License-Identifier: Apache-2.0

*********************** "sky130_fd_bd_sram__openram_write_driver" ******************************

.SUBCKT sky130_fd_bd_sram__openram_write_driver DIN BL BR EN VDD GND

**** Inverter to conver Data_in to data_in_bar ******
* din_bar = inv(DIN)
X_1 din_bar DIN GND GND sky130_fd_pr__nfet_01v8 W=0.36 L=0.15
X_2 din_bar DIN VDD VDD sky130_fd_pr__pfet_01v8 W=0.55 L=0.15

**** 2input nand gate follwed by inverter to drive BL ******
* din_bar_gated = nand(EN, DIN)
X_3 din_bar_gated EN net_7 GND sky130_fd_pr__nfet_01v8 W=0.55 L=0.15
X_4 net_7 DIN GND GND sky130_fd_pr__nfet_01v8 W=0.55 L=0.15
X_5 din_bar_gated EN VDD VDD sky130_fd_pr__pfet_01v8 W=0.55 L=0.15
X_6 din_bar_gated DIN VDD VDD sky130_fd_pr__pfet_01v8 W=0.55 L=0.15
* din_bar_gated_bar = inv(din_bar_gated)
X_7 din_bar_gated_bar din_bar_gated VDD VDD sky130_fd_pr__pfet_01v8 W=0.55 L=0.15
X_8 din_bar_gated_bar din_bar_gated GND GND sky130_fd_pr__nfet_01v8 W=0.36 L=0.15

**** 2input nand gate follwed by inverter to drive BR******
* din_gated = nand(EN, din_bar)
X_9 din_gated EN VDD VDD sky130_fd_pr__pfet_01v8 W=0.55 L=0.15
X_10 din_gated EN net_8 GND sky130_fd_pr__nfet_01v8 W=0.55 L=0.15
X_11 net_8 din_bar GND GND sky130_fd_pr__nfet_01v8 W=0.55 L=0.15
X_12 din_gated din_bar VDD VDD sky130_fd_pr__pfet_01v8 W=0.55 L=0.15
* din_gated_bar = inv(din_gated)
X_13 din_gated_bar din_gated VDD VDD sky130_fd_pr__pfet_01v8 W=0.55 L=0.15
X_14 din_gated_bar din_gated GND GND sky130_fd_pr__nfet_01v8 W=0.36 L=0.15

************************************************
* pull down with EN enable
X_15 BL din_gated_bar GND GND sky130_fd_pr__nfet_01v8 W=1 L=0.15
X_16 BR din_bar_gated_bar GND GND sky130_fd_pr__nfet_01v8 W=1 L=0.15

.ENDS sky130_fd_bd_sram__openram_write_driver

.SUBCKT sram_2_16_1_sky130_write_driver_array
+ data_0 data_1 data_2 bl_0 br_0 bl_1 br_1 bl_2 br_2 en_0 en_1 vdd gnd
* INPUT : data_0 
* INPUT : data_1 
* INPUT : data_2 
* OUTPUT: bl_0 
* OUTPUT: br_0 
* OUTPUT: bl_1 
* OUTPUT: br_1 
* OUTPUT: bl_2 
* OUTPUT: br_2 
* INPUT : en_0 
* INPUT : en_1 
* POWER : vdd 
* GROUND: gnd 
* columns: 2
* word_size 2
Xwrite_driver0
+ data_0 bl_0 br_0 en_0 vdd gnd
+ sky130_fd_bd_sram__openram_write_driver
Xwrite_driver1
+ data_1 bl_1 br_1 en_0 vdd gnd
+ sky130_fd_bd_sram__openram_write_driver
Xwrite_driver2
+ data_2 bl_2 br_2 en_1 vdd gnd
+ sky130_fd_bd_sram__openram_write_driver
.ENDS sram_2_16_1_sky130_write_driver_array

* spice ptx X{0} {1} sky130_fd_pr__pfet_01v8 m=1 w=0.55 l=0.15 pd=1.40 ps=1.40 as=0.21u ad=0.21u

.SUBCKT sram_2_16_1_sky130_precharge_0
+ bl br en_bar vdd
* OUTPUT: bl 
* OUTPUT: br 
* INPUT : en_bar 
* POWER : vdd 
Xlower_pmos bl en_bar br vdd sky130_fd_pr__pfet_01v8 m=1 w=0.55 l=0.15 pd=1.40 ps=1.40 as=0.21u ad=0.21u
Xupper_pmos1 bl en_bar vdd vdd sky130_fd_pr__pfet_01v8 m=1 w=0.55 l=0.15 pd=1.40 ps=1.40 as=0.21u ad=0.21u
Xupper_pmos2 br en_bar vdd vdd sky130_fd_pr__pfet_01v8 m=1 w=0.55 l=0.15 pd=1.40 ps=1.40 as=0.21u ad=0.21u
.ENDS sram_2_16_1_sky130_precharge_0

.SUBCKT sram_2_16_1_sky130_precharge_array
+ bl_0 br_0 bl_1 br_1 bl_2 br_2 bl_3 br_3 en_bar vdd
* OUTPUT: bl_0 
* OUTPUT: br_0 
* OUTPUT: bl_1 
* OUTPUT: br_1 
* OUTPUT: bl_2 
* OUTPUT: br_2 
* OUTPUT: bl_3 
* OUTPUT: br_3 
* INPUT : en_bar 
* POWER : vdd 
* cols: 4 size: 1 bl: bl br: br
Xpre_column_0
+ bl_0 br_0 en_bar vdd
+ sram_2_16_1_sky130_precharge_0
Xpre_column_1
+ bl_1 br_1 en_bar vdd
+ sram_2_16_1_sky130_precharge_0
Xpre_column_2
+ bl_2 br_2 en_bar vdd
+ sram_2_16_1_sky130_precharge_0
Xpre_column_3
+ bl_3 br_3 en_bar vdd
+ sram_2_16_1_sky130_precharge_0
.ENDS sram_2_16_1_sky130_precharge_array
* Copyright 2020 The SkyWater PDK Authors
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     https://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*
* SPDX-License-Identifier: Apache-2.0

*********************** "sky130_fd_bd_sram__openram_sense_amp" ******************************

.SUBCKT sky130_fd_bd_sram__openram_sense_amp BL BR DOUT EN VDD GND
X1000 GND EN a_56_432# GND sky130_fd_pr__nfet_01v8 W=0.65 L=0.15
X1001 a_56_432# dint_bar dint GND sky130_fd_pr__nfet_01v8 W=0.65 L=0.15
X1002 dint_bar dint a_56_432# GND sky130_fd_pr__nfet_01v8 W=0.65 L=0.15

X1003 VDD dint_bar dint VDD sky130_fd_pr__pfet_01v8 W=1.26 L=0.15
X1004 dint_bar dint VDD VDD sky130_fd_pr__pfet_01v8 W=1.26 L=0.15

X1005 BL EN dint VDD sky130_fd_pr__pfet_01v8 W=2 L=0.15
X1006 dint_bar EN BR VDD sky130_fd_pr__pfet_01v8 W=2 L=0.15

X1007 VDD dint_bar DOUT VDD sky130_fd_pr__pfet_01v8 W=1.26 L=0.15
X1008 DOUT dint_bar GND GND sky130_fd_pr__nfet_01v8 W=0.65 L=0.15

.ENDS sky130_fd_bd_sram__openram_sense_amp

.SUBCKT sram_2_16_1_sky130_sense_amp_array
+ data_0 bl_0 br_0 data_1 bl_1 br_1 data_2 bl_2 br_2 en vdd gnd
* OUTPUT: data_0 
* INPUT : bl_0 
* INPUT : br_0 
* OUTPUT: data_1 
* INPUT : bl_1 
* INPUT : br_1 
* OUTPUT: data_2 
* INPUT : bl_2 
* INPUT : br_2 
* INPUT : en 
* POWER : vdd 
* GROUND: gnd 
* word_size 2
* words_per_row: 1
Xsa_d0
+ bl_0 br_0 data_0 en vdd gnd
+ sky130_fd_bd_sram__openram_sense_amp
Xsa_d1
+ bl_1 br_1 data_1 en vdd gnd
+ sky130_fd_bd_sram__openram_sense_amp
Xsa_d2
+ bl_2 br_2 data_2 en vdd gnd
+ sky130_fd_bd_sram__openram_sense_amp
.ENDS sram_2_16_1_sky130_sense_amp_array

.SUBCKT sram_2_16_1_sky130_port_data
+ rbl_bl rbl_br bl_0 br_0 bl_1 br_1 sparebl_0 sparebr_0 dout_0 dout_1
+ dout_2 din_0 din_1 din_2 s_en p_en_bar w_en bank_spare_wen0 vdd gnd
* INOUT : rbl_bl 
* INOUT : rbl_br 
* INOUT : bl_0 
* INOUT : br_0 
* INOUT : bl_1 
* INOUT : br_1 
* INOUT : sparebl_0 
* INOUT : sparebr_0 
* OUTPUT: dout_0 
* OUTPUT: dout_1 
* OUTPUT: dout_2 
* INPUT : din_0 
* INPUT : din_1 
* INPUT : din_2 
* INPUT : s_en 
* INPUT : p_en_bar 
* INPUT : w_en 
* INPUT : bank_spare_wen0 
* POWER : vdd 
* GROUND: gnd 
Xprecharge_array0
+ rbl_bl rbl_br bl_0 br_0 bl_1 br_1 sparebl_0 sparebr_0 p_en_bar vdd
+ sram_2_16_1_sky130_precharge_array
Xsense_amp_array0
+ dout_0 bl_0 br_0 dout_1 bl_1 br_1 dout_2 sparebl_0 sparebr_0 s_en vdd
+ gnd
+ sram_2_16_1_sky130_sense_amp_array
Xwrite_driver_array0
+ din_0 din_1 din_2 bl_0 br_0 bl_1 br_1 sparebl_0 sparebr_0 w_en
+ bank_spare_wen0 vdd gnd
+ sram_2_16_1_sky130_write_driver_array
.ENDS sram_2_16_1_sky130_port_data

.SUBCKT sram_2_16_1_sky130_bank
+ dout0_0 dout0_1 dout0_2 rbl_bl_0_0 din0_0 din0_1 din0_2 addr0_0
+ addr0_1 addr0_2 addr0_3 addr0_4 s_en0 p_en_bar0 w_en0
+ bank_spare_wen0_0 wl_en0 vdd gnd
* OUTPUT: dout0_0 
* OUTPUT: dout0_1 
* OUTPUT: dout0_2 
* OUTPUT: rbl_bl_0_0 
* INPUT : din0_0 
* INPUT : din0_1 
* INPUT : din0_2 
* INPUT : addr0_0 
* INPUT : addr0_1 
* INPUT : addr0_2 
* INPUT : addr0_3 
* INPUT : addr0_4 
* INPUT : s_en0 
* INPUT : p_en_bar0 
* INPUT : w_en0 
* INPUT : bank_spare_wen0_0 
* INPUT : wl_en0 
* POWER : vdd 
* GROUND: gnd 
Xbitcell_array
+ rbl_bl_0_0 rbl_br_0_0 bl_0_0 br_0_0 bl_0_1 br_0_1 bl_0_2 br_0_2
+ rbl_wl0 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8
+ wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 wl_0_16 vdd gnd
+ sram_2_16_1_sky130_sky130_capped_replica_bitcell_array
Xport_data0
+ rbl_bl_0_0 rbl_br_0_0 bl_0_0 br_0_0 bl_0_1 br_0_1 bl_0_2 br_0_2
+ dout0_0 dout0_1 dout0_2 din0_0 din0_1 din0_2 s_en0 p_en_bar0 w_en0
+ bank_spare_wen0_0 vdd gnd
+ sram_2_16_1_sky130_port_data
Xport_address0
+ addr0_0 addr0_1 addr0_2 addr0_3 addr0_4 wl_en0 wl_0_0 wl_0_1 wl_0_2
+ wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9 wl_0_10 wl_0_11
+ wl_0_12 wl_0_13 wl_0_14 wl_0_15 wl_0_16 rbl_wl0 vdd gnd
+ sram_2_16_1_sky130_port_address
.ENDS sram_2_16_1_sky130_bank

.SUBCKT sram_2_16_1_sky130_pinv_4
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 1
Xpinv_pmos Z A vdd vdd sky130_fd_pr__pfet_01v8 m=1 w=1.12 l=0.15 pd=2.54 ps=2.54 as=0.42u ad=0.42u
Xpinv_nmos Z A gnd gnd sky130_fd_pr__nfet_01v8 m=1 w=0.36 l=0.15 pd=1.02 ps=1.02 as=0.14u ad=0.14u
.ENDS sram_2_16_1_sky130_pinv_4

* spice ptx X{0} {1} sky130_fd_pr__nfet_01v8 m=3 w=2.0 l=0.15 pd=4.30 ps=4.30 as=0.75u ad=0.75u

* spice ptx X{0} {1} sky130_fd_pr__pfet_01v8 m=3 w=2.0 l=0.15 pd=4.30 ps=4.30 as=0.75u ad=0.75u

.SUBCKT sram_2_16_1_sky130_pinv_8
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 5
Xpinv_pmos Z A vdd vdd sky130_fd_pr__pfet_01v8 m=3 w=2.0 l=0.15 pd=4.30 ps=4.30 as=0.75u ad=0.75u
Xpinv_nmos Z A gnd gnd sky130_fd_pr__nfet_01v8 m=3 w=2.0 l=0.15 pd=4.30 ps=4.30 as=0.75u ad=0.75u
.ENDS sram_2_16_1_sky130_pinv_8

.SUBCKT sram_2_16_1_sky130_pdriver_1
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [1, 5]
Xbuf_inv1
+ A Zb1_int vdd gnd
+ sram_2_16_1_sky130_pinv_4
Xbuf_inv2
+ Zb1_int Z vdd gnd
+ sram_2_16_1_sky130_pinv_8
.ENDS sram_2_16_1_sky130_pdriver_1

* spice ptx X{0} {1} sky130_fd_pr__nfet_01v8 m=6 w=2.0 l=0.15 pd=4.30 ps=4.30 as=0.75u ad=0.75u

* spice ptx X{0} {1} sky130_fd_pr__pfet_01v8 m=6 w=2.0 l=0.15 pd=4.30 ps=4.30 as=0.75u ad=0.75u

.SUBCKT sram_2_16_1_sky130_pinv_9
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 10
Xpinv_pmos Z A vdd vdd sky130_fd_pr__pfet_01v8 m=6 w=2.0 l=0.15 pd=4.30 ps=4.30 as=0.75u ad=0.75u
Xpinv_nmos Z A gnd gnd sky130_fd_pr__nfet_01v8 m=6 w=2.0 l=0.15 pd=4.30 ps=4.30 as=0.75u ad=0.75u
.ENDS sram_2_16_1_sky130_pinv_9

.SUBCKT sram_2_16_1_sky130_pdriver_2
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [10]
Xbuf_inv1
+ A Z vdd gnd
+ sram_2_16_1_sky130_pinv_9
.ENDS sram_2_16_1_sky130_pdriver_2

* spice ptx X{0} {1} sky130_fd_pr__nfet_01v8 m=1 w=0.74 l=0.15 pd=1.78 ps=1.78 as=0.28u ad=0.28u

* spice ptx X{0} {1} sky130_fd_pr__pfet_01v8 m=1 w=1.12 l=0.15 pd=2.54 ps=2.54 as=0.42u ad=0.42u

* spice ptx X{0} {1} sky130_fd_pr__nfet_01v8 m=1 w=0.74 l=0.15 pd=1.78 ps=1.78 as=0.28u ad=0.28u

* spice ptx X{0} {1} sky130_fd_pr__nfet_01v8 m=1 w=0.74 l=0.15 pd=1.78 ps=1.78 as=0.28u ad=0.28u

.SUBCKT sram_2_16_1_sky130_pnand3
+ A B C Z vdd gnd
* INPUT : A 
* INPUT : B 
* INPUT : C 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 1
Xpnand3_pmos1 vdd A Z vdd sky130_fd_pr__pfet_01v8 m=1 w=1.12 l=0.15 pd=2.54 ps=2.54 as=0.42u ad=0.42u
Xpnand3_pmos2 Z B vdd vdd sky130_fd_pr__pfet_01v8 m=1 w=1.12 l=0.15 pd=2.54 ps=2.54 as=0.42u ad=0.42u
Xpnand3_pmos3 Z C vdd vdd sky130_fd_pr__pfet_01v8 m=1 w=1.12 l=0.15 pd=2.54 ps=2.54 as=0.42u ad=0.42u
Xpnand3_nmos1 Z C net1 gnd sky130_fd_pr__nfet_01v8 m=1 w=0.74 l=0.15 pd=1.78 ps=1.78 as=0.28u ad=0.28u
Xpnand3_nmos2 net1 B net2 gnd sky130_fd_pr__nfet_01v8 m=1 w=0.74 l=0.15 pd=1.78 ps=1.78 as=0.28u ad=0.28u
Xpnand3_nmos3 net2 A gnd gnd sky130_fd_pr__nfet_01v8 m=1 w=0.74 l=0.15 pd=1.78 ps=1.78 as=0.28u ad=0.28u
.ENDS sram_2_16_1_sky130_pnand3

.SUBCKT sram_2_16_1_sky130_pand3
+ A B C Z vdd gnd
* INPUT : A 
* INPUT : B 
* INPUT : C 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 10
Xpand3_nand
+ A B C zb_int vdd gnd
+ sram_2_16_1_sky130_pnand3
Xpand3_inv
+ zb_int Z vdd gnd
+ sram_2_16_1_sky130_pdriver_2
.ENDS sram_2_16_1_sky130_pand3

.SUBCKT sram_2_16_1_sky130_pdriver_4
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [1, 1]
Xbuf_inv1
+ A Zb1_int vdd gnd
+ sram_2_16_1_sky130_pinv_4
Xbuf_inv2
+ Zb1_int Z vdd gnd
+ sram_2_16_1_sky130_pinv_4
.ENDS sram_2_16_1_sky130_pdriver_4

.SUBCKT sram_2_16_1_sky130_pnand2_0
+ A B Z vdd gnd
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 1
Xpnand2_pmos1 vdd A Z vdd sky130_fd_pr__pfet_01v8 m=1 w=1.12 l=0.15 pd=2.54 ps=2.54 as=0.42u ad=0.42u
Xpnand2_pmos2 Z B vdd vdd sky130_fd_pr__pfet_01v8 m=1 w=1.12 l=0.15 pd=2.54 ps=2.54 as=0.42u ad=0.42u
Xpnand2_nmos1 Z B net1 gnd sky130_fd_pr__nfet_01v8 m=1 w=0.74 l=0.15 pd=1.78 ps=1.78 as=0.28u ad=0.28u
Xpnand2_nmos2 net1 A gnd gnd sky130_fd_pr__nfet_01v8 m=1 w=0.74 l=0.15 pd=1.78 ps=1.78 as=0.28u ad=0.28u
.ENDS sram_2_16_1_sky130_pnand2_0

* spice ptx X{0} {1} sky130_fd_pr__pfet_01v8 m=7 w=2.0 l=0.15 pd=4.30 ps=4.30 as=0.75u ad=0.75u

* spice ptx X{0} {1} sky130_fd_pr__nfet_01v8 m=7 w=1.68 l=0.15 pd=3.66 ps=3.66 as=0.63u ad=0.63u

.SUBCKT sram_2_16_1_sky130_pinv_1
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 12
Xpinv_pmos Z A vdd vdd sky130_fd_pr__pfet_01v8 m=7 w=2.0 l=0.15 pd=4.30 ps=4.30 as=0.75u ad=0.75u
Xpinv_nmos Z A gnd gnd sky130_fd_pr__nfet_01v8 m=7 w=1.68 l=0.15 pd=3.66 ps=3.66 as=0.63u ad=0.63u
.ENDS sram_2_16_1_sky130_pinv_1

.SUBCKT sram_2_16_1_sky130_pdriver
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [12]
Xbuf_inv1
+ A Z vdd gnd
+ sram_2_16_1_sky130_pinv_1
.ENDS sram_2_16_1_sky130_pdriver

.SUBCKT sram_2_16_1_sky130_pnand2
+ A B Z vdd gnd
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 1
Xpnand2_pmos1 vdd A Z vdd sky130_fd_pr__pfet_01v8 m=1 w=1.12 l=0.15 pd=2.54 ps=2.54 as=0.42u ad=0.42u
Xpnand2_pmos2 Z B vdd vdd sky130_fd_pr__pfet_01v8 m=1 w=1.12 l=0.15 pd=2.54 ps=2.54 as=0.42u ad=0.42u
Xpnand2_nmos1 Z B net1 gnd sky130_fd_pr__nfet_01v8 m=1 w=0.74 l=0.15 pd=1.78 ps=1.78 as=0.28u ad=0.28u
Xpnand2_nmos2 net1 A gnd gnd sky130_fd_pr__nfet_01v8 m=1 w=0.74 l=0.15 pd=1.78 ps=1.78 as=0.28u ad=0.28u
.ENDS sram_2_16_1_sky130_pnand2

.SUBCKT sram_2_16_1_sky130_pand2
+ A B Z vdd gnd
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 12
Xpand2_nand
+ A B zb_int vdd gnd
+ sram_2_16_1_sky130_pnand2
Xpand2_inv
+ zb_int Z vdd gnd
+ sram_2_16_1_sky130_pdriver
.ENDS sram_2_16_1_sky130_pand2

* spice ptx X{0} {1} sky130_fd_pr__nfet_01v8 m=10 w=1.68 l=0.15 pd=3.66 ps=3.66 as=0.63u ad=0.63u

* spice ptx X{0} {1} sky130_fd_pr__pfet_01v8 m=10 w=2.0 l=0.15 pd=4.30 ps=4.30 as=0.75u ad=0.75u

.SUBCKT sram_2_16_1_sky130_pinv_7
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 17
Xpinv_pmos Z A vdd vdd sky130_fd_pr__pfet_01v8 m=10 w=2.0 l=0.15 pd=4.30 ps=4.30 as=0.75u ad=0.75u
Xpinv_nmos Z A gnd gnd sky130_fd_pr__nfet_01v8 m=10 w=1.68 l=0.15 pd=3.66 ps=3.66 as=0.63u ad=0.63u
.ENDS sram_2_16_1_sky130_pinv_7

* spice ptx X{0} {1} sky130_fd_pr__pfet_01v8 m=4 w=2.0 l=0.15 pd=4.30 ps=4.30 as=0.75u ad=0.75u

* spice ptx X{0} {1} sky130_fd_pr__nfet_01v8 m=4 w=1.26 l=0.15 pd=2.82 ps=2.82 as=0.47u ad=0.47u

.SUBCKT sram_2_16_1_sky130_pinv_6
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 6
Xpinv_pmos Z A vdd vdd sky130_fd_pr__pfet_01v8 m=4 w=2.0 l=0.15 pd=4.30 ps=4.30 as=0.75u ad=0.75u
Xpinv_nmos Z A gnd gnd sky130_fd_pr__nfet_01v8 m=4 w=1.26 l=0.15 pd=2.82 ps=2.82 as=0.47u ad=0.47u
.ENDS sram_2_16_1_sky130_pinv_6

* spice ptx X{0} {1} sky130_fd_pr__pfet_01v8 m=2 w=1.26 l=0.15 pd=2.82 ps=2.82 as=0.47u ad=0.47u

* spice ptx X{0} {1} sky130_fd_pr__nfet_01v8 m=2 w=0.74 l=0.15 pd=1.78 ps=1.78 as=0.28u ad=0.28u

.SUBCKT sram_2_16_1_sky130_pinv_5
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 2
Xpinv_pmos Z A vdd vdd sky130_fd_pr__pfet_01v8 m=2 w=1.26 l=0.15 pd=2.82 ps=2.82 as=0.47u ad=0.47u
Xpinv_nmos Z A gnd gnd sky130_fd_pr__nfet_01v8 m=2 w=0.74 l=0.15 pd=1.78 ps=1.78 as=0.28u ad=0.28u
.ENDS sram_2_16_1_sky130_pinv_5

.SUBCKT sram_2_16_1_sky130_pdriver_0
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [1, 2, 6, 17]
Xbuf_inv1
+ A Zb1_int vdd gnd
+ sram_2_16_1_sky130_pinv_4
Xbuf_inv2
+ Zb1_int Zb2_int vdd gnd
+ sram_2_16_1_sky130_pinv_5
Xbuf_inv3
+ Zb2_int Zb3_int vdd gnd
+ sram_2_16_1_sky130_pinv_6
Xbuf_inv4
+ Zb3_int Z vdd gnd
+ sram_2_16_1_sky130_pinv_7
.ENDS sram_2_16_1_sky130_pdriver_0

.SUBCKT sram_2_16_1_sky130_pinv_11
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 1
Xpinv_pmos Z A vdd vdd sky130_fd_pr__pfet_01v8 m=1 w=1.12 l=0.15 pd=2.54 ps=2.54 as=0.42u ad=0.42u
Xpinv_nmos Z A gnd gnd sky130_fd_pr__nfet_01v8 m=1 w=0.36 l=0.15 pd=1.02 ps=1.02 as=0.14u ad=0.14u
.ENDS sram_2_16_1_sky130_pinv_11

.SUBCKT sram_2_16_1_sky130_delay_chain
+ in out vdd gnd
* INPUT : in 
* OUTPUT: out 
* POWER : vdd 
* GROUND: gnd 
* fanouts: [4, 4, 4, 4, 4, 4, 4, 4, 4]
Xdinv0
+ in dout_1 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_0_0
+ dout_1 n_0_0 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_0_1
+ dout_1 n_0_1 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_0_2
+ dout_1 n_0_2 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_0_3
+ dout_1 n_0_3 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdinv1
+ dout_1 dout_2 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_1_0
+ dout_2 n_1_0 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_1_1
+ dout_2 n_1_1 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_1_2
+ dout_2 n_1_2 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_1_3
+ dout_2 n_1_3 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdinv2
+ dout_2 dout_3 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_2_0
+ dout_3 n_2_0 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_2_1
+ dout_3 n_2_1 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_2_2
+ dout_3 n_2_2 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_2_3
+ dout_3 n_2_3 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdinv3
+ dout_3 dout_4 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_3_0
+ dout_4 n_3_0 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_3_1
+ dout_4 n_3_1 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_3_2
+ dout_4 n_3_2 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_3_3
+ dout_4 n_3_3 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdinv4
+ dout_4 dout_5 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_4_0
+ dout_5 n_4_0 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_4_1
+ dout_5 n_4_1 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_4_2
+ dout_5 n_4_2 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_4_3
+ dout_5 n_4_3 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdinv5
+ dout_5 dout_6 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_5_0
+ dout_6 n_5_0 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_5_1
+ dout_6 n_5_1 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_5_2
+ dout_6 n_5_2 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_5_3
+ dout_6 n_5_3 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdinv6
+ dout_6 dout_7 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_6_0
+ dout_7 n_6_0 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_6_1
+ dout_7 n_6_1 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_6_2
+ dout_7 n_6_2 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_6_3
+ dout_7 n_6_3 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdinv7
+ dout_7 dout_8 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_7_0
+ dout_8 n_7_0 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_7_1
+ dout_8 n_7_1 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_7_2
+ dout_8 n_7_2 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_7_3
+ dout_8 n_7_3 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdinv8
+ dout_8 out vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_8_0
+ out n_8_0 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_8_1
+ out n_8_1 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_8_2
+ out n_8_2 vdd gnd
+ sram_2_16_1_sky130_pinv_11
Xdload_8_3
+ out n_8_3 vdd gnd
+ sram_2_16_1_sky130_pinv_11
.ENDS sram_2_16_1_sky130_delay_chain

* spice ptx X{0} {1} sky130_fd_pr__pfet_01v8 m=2 w=2.0 l=0.15 pd=4.30 ps=4.30 as=0.75u ad=0.75u

* spice ptx X{0} {1} sky130_fd_pr__nfet_01v8 m=2 w=1.26 l=0.15 pd=2.82 ps=2.82 as=0.47u ad=0.47u

.SUBCKT sram_2_16_1_sky130_pinv_10
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 3
Xpinv_pmos Z A vdd vdd sky130_fd_pr__pfet_01v8 m=2 w=2.0 l=0.15 pd=4.30 ps=4.30 as=0.75u ad=0.75u
Xpinv_nmos Z A gnd gnd sky130_fd_pr__nfet_01v8 m=2 w=1.26 l=0.15 pd=2.82 ps=2.82 as=0.47u ad=0.47u
.ENDS sram_2_16_1_sky130_pinv_10

.SUBCKT sram_2_16_1_sky130_pdriver_3
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [3]
Xbuf_inv1
+ A Z vdd gnd
+ sram_2_16_1_sky130_pinv_10
.ENDS sram_2_16_1_sky130_pdriver_3

.SUBCKT sram_2_16_1_sky130_pand3_0
+ A B C Z vdd gnd
* INPUT : A 
* INPUT : B 
* INPUT : C 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 3
Xpand3_nand
+ A B C zb_int vdd gnd
+ sram_2_16_1_sky130_pnand3
Xpand3_inv
+ zb_int Z vdd gnd
+ sram_2_16_1_sky130_pdriver_3
.ENDS sram_2_16_1_sky130_pand3_0

.SUBCKT sram_2_16_1_sky130_pinv
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 2
Xpinv_pmos Z A vdd vdd sky130_fd_pr__pfet_01v8 m=2 w=1.26 l=0.15 pd=2.82 ps=2.82 as=0.47u ad=0.47u
Xpinv_nmos Z A gnd gnd sky130_fd_pr__nfet_01v8 m=2 w=0.74 l=0.15 pd=1.78 ps=1.78 as=0.28u ad=0.28u
.ENDS sram_2_16_1_sky130_pinv

* spice ptx X{0} {1} sky130_fd_pr__nfet_01v8 m=3 w=1.68 l=0.15 pd=3.66 ps=3.66 as=0.63u ad=0.63u

* spice ptx X{0} {1} sky130_fd_pr__pfet_01v8 m=3 w=1.68 l=0.15 pd=3.66 ps=3.66 as=0.63u ad=0.63u

.SUBCKT sram_2_16_1_sky130_pinv_0
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 4
Xpinv_pmos Z A vdd vdd sky130_fd_pr__pfet_01v8 m=3 w=1.68 l=0.15 pd=3.66 ps=3.66 as=0.63u ad=0.63u
Xpinv_nmos Z A gnd gnd sky130_fd_pr__nfet_01v8 m=3 w=1.68 l=0.15 pd=3.66 ps=3.66 as=0.63u ad=0.63u
.ENDS sram_2_16_1_sky130_pinv_0

.SUBCKT sram_2_16_1_sky130_dff_buf_0
+ D Q Qb clk vdd gnd
* INPUT : D 
* OUTPUT: Q 
* OUTPUT: Qb 
* INPUT : clk 
* POWER : vdd 
* GROUND: gnd 
* inv1: 2 inv2: 4
Xdff_buf_dff
+ D qint clk vdd gnd
+ sky130_fd_bd_sram__openram_dff
Xdff_buf_inv1
+ qint Qb vdd gnd
+ sram_2_16_1_sky130_pinv
Xdff_buf_inv2
+ Qb Q vdd gnd
+ sram_2_16_1_sky130_pinv_0
.ENDS sram_2_16_1_sky130_dff_buf_0

.SUBCKT sram_2_16_1_sky130_dff_buf_array
+ din_0 din_1 dout_0 dout_bar_0 dout_1 dout_bar_1 clk vdd gnd
* INPUT : din_0 
* INPUT : din_1 
* OUTPUT: dout_0 
* OUTPUT: dout_bar_0 
* OUTPUT: dout_1 
* OUTPUT: dout_bar_1 
* INPUT : clk 
* POWER : vdd 
* GROUND: gnd 
* rows: 2 cols: 1
* inv1: 2 inv2: 4
Xdff_r0_c0
+ din_0 dout_0 dout_bar_0 clk vdd gnd
+ sram_2_16_1_sky130_dff_buf_0
Xdff_r1_c0
+ din_1 dout_1 dout_bar_1 clk vdd gnd
+ sram_2_16_1_sky130_dff_buf_0
.ENDS sram_2_16_1_sky130_dff_buf_array

.SUBCKT sram_2_16_1_sky130_pinv_2
+ A Z vdd gnd
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 1
Xpinv_pmos Z A vdd vdd sky130_fd_pr__pfet_01v8 m=1 w=1.12 l=0.15 pd=2.54 ps=2.54 as=0.42u ad=0.42u
Xpinv_nmos Z A gnd gnd sky130_fd_pr__nfet_01v8 m=1 w=0.36 l=0.15 pd=1.02 ps=1.02 as=0.14u ad=0.14u
.ENDS sram_2_16_1_sky130_pinv_2

.SUBCKT sram_2_16_1_sky130_control_logic_rw
+ csb web clk rbl_bl s_en w_en p_en_bar wl_en clk_buf vdd gnd
* INPUT : csb 
* INPUT : web 
* INPUT : clk 
* INPUT : rbl_bl 
* OUTPUT: s_en 
* OUTPUT: w_en 
* OUTPUT: p_en_bar 
* OUTPUT: wl_en 
* OUTPUT: clk_buf 
* POWER : vdd 
* GROUND: gnd 
* num_rows: 17
* words_per_row: 1
* word_size 2
Xctrl_dffs
+ csb web cs_bar cs we_bar we clk_buf vdd gnd
+ sram_2_16_1_sky130_dff_buf_array
Xclkbuf
+ clk clk_buf vdd gnd
+ sram_2_16_1_sky130_pdriver_0
Xinv_clk_bar
+ clk_buf clk_bar vdd gnd
+ sram_2_16_1_sky130_pinv_2
Xand2_gated_clk_bar
+ clk_bar cs gated_clk_bar vdd gnd
+ sram_2_16_1_sky130_pand2
Xand2_gated_clk_buf
+ clk_buf cs gated_clk_buf vdd gnd
+ sram_2_16_1_sky130_pand2
Xbuf_wl_en
+ gated_clk_bar wl_en vdd gnd
+ sram_2_16_1_sky130_pdriver_1
Xrbl_bl_delay_inv
+ rbl_bl_delay rbl_bl_delay_bar vdd gnd
+ sram_2_16_1_sky130_pinv_2
Xw_en_and
+ we rbl_bl_delay_bar gated_clk_bar w_en vdd gnd
+ sram_2_16_1_sky130_pand3
Xbuf_s_en_and
+ rbl_bl_delay gated_clk_bar we_bar s_en vdd gnd
+ sram_2_16_1_sky130_pand3_0
Xdelay_chain
+ rbl_bl rbl_bl_delay vdd gnd
+ sram_2_16_1_sky130_delay_chain
Xnand_p_en_bar
+ gated_clk_buf rbl_bl_delay p_en_bar_unbuf vdd gnd
+ sram_2_16_1_sky130_pnand2_0
Xbuf_p_en_bar
+ p_en_bar_unbuf p_en_bar vdd gnd
+ sram_2_16_1_sky130_pdriver_4
.ENDS sram_2_16_1_sky130_control_logic_rw

.SUBCKT sram_2_16_1_sky130_spare_wen_dff
+ din_0 dout_0 clk vdd gnd
* INPUT : din_0 
* OUTPUT: dout_0 
* INPUT : clk 
* POWER : vdd 
* GROUND: gnd 
* rows: 1 cols: 1
Xdff_r0_c0
+ din_0 dout_0 CLK VDD GND
+ sky130_fd_bd_sram__openram_dff
.ENDS sram_2_16_1_sky130_spare_wen_dff

.SUBCKT sram_2_16_1_sky130
+ din0[0] din0[1] din0[2] addr0[0] addr0[1] addr0[2] addr0[3] addr0[4]
+ csb0 web0 clk0 spare_wen0 dout0[0] dout0[1] dout0[2] vccd1 vssd1
* INPUT : din0[0] 
* INPUT : din0[1] 
* INPUT : din0[2] 
* INPUT : addr0[0] 
* INPUT : addr0[1] 
* INPUT : addr0[2] 
* INPUT : addr0[3] 
* INPUT : addr0[4] 
* INPUT : csb0 
* INPUT : web0 
* INPUT : clk0 
* INPUT : spare_wen0 
* OUTPUT: dout0[0] 
* OUTPUT: dout0[1] 
* OUTPUT: dout0[2] 
* POWER : vccd1 
* GROUND: vssd1 
Xbank0
+ dout0[0] dout0[1] dout0[2] rbl_bl0 bank_din0_0 bank_din0_1 bank_din0_2
+ a0_0 a0_1 a0_2 a0_3 a0_4 s_en0 p_en_bar0 w_en0 bank_spare_wen0_0
+ wl_en0 vccd1 vssd1
+ sram_2_16_1_sky130_bank
Xcontrol0
+ csb0 web0 clk0 rbl_bl0 s_en0 w_en0 p_en_bar0 wl_en0 clk_buf0 vccd1
+ vssd1
+ sram_2_16_1_sky130_control_logic_rw
Xrow_address0
+ addr0[0] addr0[1] addr0[2] addr0[3] addr0[4] a0_0 a0_1 a0_2 a0_3 a0_4
+ clk_buf0 vccd1 vssd1
+ sram_2_16_1_sky130_row_addr_dff
Xdata_dff0
+ din0[0] din0[1] din0[2] bank_din0_0 bank_din0_1 bank_din0_2 clk_buf0
+ vccd1 vssd1
+ sram_2_16_1_sky130_data_dff
Xspare_wen_dff0
+ spare_wen0[0] bank_spare_wen0_0 clk_buf0 vccd1 vssd1
+ sram_2_16_1_sky130_spare_wen_dff
.ENDS sram_2_16_1_sky130
