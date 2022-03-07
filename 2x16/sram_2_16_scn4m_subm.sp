**************************************************
* OpenRAM generated memory.
* Words: 16
* Data bits: 2
* Banks: 1
* Column mux: 1:1
* Trimmed: False
* LVS: False
**************************************************
*********************** "dff" ******************************
* Positive edge-triggered FF
.SUBCKT dff D Q clk vdd gnd

* SPICE3 file created from dff.ext - technology: scmos

M1000 vdd clk a_24_24# vdd p w=8u l=0.4u
M1001 a_84_296# D vdd vdd p w=4u l=0.4u
M1002 a_104_24# clk a_84_296# vdd p w=4u l=0.4u
M1003 a_140_296# a_24_24# a_104_24# vdd p w=4u l=0.4u
M1004 vdd a_152_16# a_140_296# vdd p w=4u l=0.4u
M1005 a_152_16# a_104_24# vdd vdd p w=4u l=0.4u
M1006 a_260_296# a_152_16# vdd vdd p w=4u l=0.4u
M1007 a_280_24# a_24_24# a_260_296# vdd p w=4u l=0.4u
M1008 a_320_336# clk a_280_24# vdd p w=2u l=0.4u
M1009 vdd Q a_320_336# vdd p w=2u l=0.4u
M1010 gnd clk a_24_24# gnd n w=4u l=0.4u
M1011 Q a_280_24# vdd vdd p w=8u l=0.4u
M1012 a_84_24# D gnd gnd n w=2u l=0.4u
M1013 a_104_24# a_24_24# a_84_24# gnd n w=2u l=0.4u
M1014 a_140_24# clk a_104_24# gnd n w=2u l=0.4u
M1015 gnd a_152_16# a_140_24# gnd n w=2u l=0.4u
M1016 a_152_16# a_104_24# gnd gnd n w=2u l=0.4u
M1017 a_260_24# a_152_16# gnd gnd n w=2u l=0.4u
M1018 a_280_24# clk a_260_24# gnd n w=2u l=0.4u
M1019 a_320_24# a_24_24# a_280_24# gnd n w=2u l=0.4u
M1020 gnd Q a_320_24# gnd n w=2u l=0.4u
M1021 Q a_280_24# gnd gnd n w=4u l=0.4u

.ENDS

.SUBCKT row_addr_dff din_0 din_1 din_2 din_3 dout_0 dout_1 dout_2 dout_3 clk vdd gnd
*.PININFO din_0:I din_1:I din_2:I din_3:I dout_0:O dout_1:O dout_2:O dout_3:O clk:I vdd:B gnd:B
* INPUT : din_0 
* INPUT : din_1 
* INPUT : din_2 
* INPUT : din_3 
* OUTPUT: dout_0 
* OUTPUT: dout_1 
* OUTPUT: dout_2 
* OUTPUT: dout_3 
* INPUT : clk 
* POWER : vdd 
* GROUND: gnd 
* rows: 4 cols: 1
Xdff_r0_c0 din_0 dout_0 clk vdd gnd dff
Xdff_r1_c0 din_1 dout_1 clk vdd gnd dff
Xdff_r2_c0 din_2 dout_2 clk vdd gnd dff
Xdff_r3_c0 din_3 dout_3 clk vdd gnd dff
.ENDS row_addr_dff

*********************** "dummy_cell_1rw" ******************************
.SUBCKT dummy_cell_1rw bl br wl vdd gnd

* Inverter 1
M1000 Q Q_bar vdd vdd p w=0.6u l=0.8u
M1002 Q Q_bar gnd gnd n w=1.6u l=0.4u

* Inverter 2
M1001 vdd Q Q_bar vdd p w=0.6u l=0.8u
M1003 gnd Q Q_bar gnd n w=1.6u l=0.4u

* Access transistors
M1004 Q wl bl_noconn gnd n w=0.8u l=0.4u
M1005 Q_bar wl br_noconn gnd n w=0.8u l=0.4u

.ENDS

.SUBCKT dummy_array_3 bl_0_0 br_0_0 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 wl_0_16 wl_0_17 wl_0_18 vdd gnd
*.PININFO bl_0_0:B br_0_0:B wl_0_0:I wl_0_1:I wl_0_2:I wl_0_3:I wl_0_4:I wl_0_5:I wl_0_6:I wl_0_7:I wl_0_8:I wl_0_9:I wl_0_10:I wl_0_11:I wl_0_12:I wl_0_13:I wl_0_14:I wl_0_15:I wl_0_16:I wl_0_17:I wl_0_18:I vdd:B gnd:B
* INOUT : bl_0_0 
* INOUT : br_0_0 
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
* INPUT : wl_0_17 
* INPUT : wl_0_18 
* POWER : vdd 
* GROUND: gnd 
Xbit_r0_c0 bl_0_0 br_0_0 wl_0_0 vdd gnd dummy_cell_1rw
Xbit_r1_c0 bl_0_0 br_0_0 wl_0_1 vdd gnd dummy_cell_1rw
Xbit_r2_c0 bl_0_0 br_0_0 wl_0_2 vdd gnd dummy_cell_1rw
Xbit_r3_c0 bl_0_0 br_0_0 wl_0_3 vdd gnd dummy_cell_1rw
Xbit_r4_c0 bl_0_0 br_0_0 wl_0_4 vdd gnd dummy_cell_1rw
Xbit_r5_c0 bl_0_0 br_0_0 wl_0_5 vdd gnd dummy_cell_1rw
Xbit_r6_c0 bl_0_0 br_0_0 wl_0_6 vdd gnd dummy_cell_1rw
Xbit_r7_c0 bl_0_0 br_0_0 wl_0_7 vdd gnd dummy_cell_1rw
Xbit_r8_c0 bl_0_0 br_0_0 wl_0_8 vdd gnd dummy_cell_1rw
Xbit_r9_c0 bl_0_0 br_0_0 wl_0_9 vdd gnd dummy_cell_1rw
Xbit_r10_c0 bl_0_0 br_0_0 wl_0_10 vdd gnd dummy_cell_1rw
Xbit_r11_c0 bl_0_0 br_0_0 wl_0_11 vdd gnd dummy_cell_1rw
Xbit_r12_c0 bl_0_0 br_0_0 wl_0_12 vdd gnd dummy_cell_1rw
Xbit_r13_c0 bl_0_0 br_0_0 wl_0_13 vdd gnd dummy_cell_1rw
Xbit_r14_c0 bl_0_0 br_0_0 wl_0_14 vdd gnd dummy_cell_1rw
Xbit_r15_c0 bl_0_0 br_0_0 wl_0_15 vdd gnd dummy_cell_1rw
Xbit_r16_c0 bl_0_0 br_0_0 wl_0_16 vdd gnd dummy_cell_1rw
Xbit_r17_c0 bl_0_0 br_0_0 wl_0_17 vdd gnd dummy_cell_1rw
Xbit_r18_c0 bl_0_0 br_0_0 wl_0_18 vdd gnd dummy_cell_1rw
.ENDS dummy_array_3

*********************** "cell_1rw" ******************************
.SUBCKT replica_cell_1rw bl br wl vdd gnd
* SPICE3 file created from cell_1rw.ext - technology: scmos

* Inverter 1
M1000 Q vdd vdd vdd p w=0.6u l=0.8u
M1002 Q vdd gnd gnd n w=1.6u l=0.4u

* Inverter 2
M1001 vdd Q vdd vdd p w=0.6u l=0.8u
M1003 gnd Q vdd gnd n w=1.6u l=0.4u

* Access transistors
M1004 Q wl bl gnd n w=0.8u l=0.4u
M1005 vdd wl br gnd n w=0.8u l=0.4u

.ENDS

.SUBCKT replica_column bl_0_0 br_0_0 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 wl_0_16 wl_0_17 wl_0_18 vdd gnd
*.PININFO bl_0_0:O br_0_0:O wl_0_0:I wl_0_1:I wl_0_2:I wl_0_3:I wl_0_4:I wl_0_5:I wl_0_6:I wl_0_7:I wl_0_8:I wl_0_9:I wl_0_10:I wl_0_11:I wl_0_12:I wl_0_13:I wl_0_14:I wl_0_15:I wl_0_16:I wl_0_17:I wl_0_18:I vdd:B gnd:B
* OUTPUT: bl_0_0 
* OUTPUT: br_0_0 
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
* INPUT : wl_0_17 
* INPUT : wl_0_18 
* POWER : vdd 
* GROUND: gnd 
Xrbc_0 bl_0_0 br_0_0 wl_0_0 vdd gnd dummy_cell_1rw
Xrbc_1 bl_0_0 br_0_0 wl_0_1 vdd gnd replica_cell_1rw
Xrbc_2 bl_0_0 br_0_0 wl_0_2 vdd gnd replica_cell_1rw
Xrbc_3 bl_0_0 br_0_0 wl_0_3 vdd gnd replica_cell_1rw
Xrbc_4 bl_0_0 br_0_0 wl_0_4 vdd gnd replica_cell_1rw
Xrbc_5 bl_0_0 br_0_0 wl_0_5 vdd gnd replica_cell_1rw
Xrbc_6 bl_0_0 br_0_0 wl_0_6 vdd gnd replica_cell_1rw
Xrbc_7 bl_0_0 br_0_0 wl_0_7 vdd gnd replica_cell_1rw
Xrbc_8 bl_0_0 br_0_0 wl_0_8 vdd gnd replica_cell_1rw
Xrbc_9 bl_0_0 br_0_0 wl_0_9 vdd gnd replica_cell_1rw
Xrbc_10 bl_0_0 br_0_0 wl_0_10 vdd gnd replica_cell_1rw
Xrbc_11 bl_0_0 br_0_0 wl_0_11 vdd gnd replica_cell_1rw
Xrbc_12 bl_0_0 br_0_0 wl_0_12 vdd gnd replica_cell_1rw
Xrbc_13 bl_0_0 br_0_0 wl_0_13 vdd gnd replica_cell_1rw
Xrbc_14 bl_0_0 br_0_0 wl_0_14 vdd gnd replica_cell_1rw
Xrbc_15 bl_0_0 br_0_0 wl_0_15 vdd gnd replica_cell_1rw
Xrbc_16 bl_0_0 br_0_0 wl_0_16 vdd gnd replica_cell_1rw
Xrbc_17 bl_0_0 br_0_0 wl_0_17 vdd gnd replica_cell_1rw
Xrbc_18 bl_0_0 br_0_0 wl_0_18 vdd gnd dummy_cell_1rw
.ENDS replica_column

.SUBCKT dummy_array bl_0_0 br_0_0 bl_0_1 br_0_1 wl_0_0 vdd gnd
*.PININFO bl_0_0:B br_0_0:B bl_0_1:B br_0_1:B wl_0_0:I vdd:B gnd:B
* INOUT : bl_0_0 
* INOUT : br_0_0 
* INOUT : bl_0_1 
* INOUT : br_0_1 
* INPUT : wl_0_0 
* POWER : vdd 
* GROUND: gnd 
Xbit_r0_c0 bl_0_0 br_0_0 wl_0_0 vdd gnd dummy_cell_1rw
Xbit_r0_c1 bl_0_1 br_0_1 wl_0_0 vdd gnd dummy_cell_1rw
.ENDS dummy_array

.SUBCKT dummy_array_1 bl_0_0 br_0_0 bl_0_1 br_0_1 wl_0_0 vdd gnd
*.PININFO bl_0_0:B br_0_0:B bl_0_1:B br_0_1:B wl_0_0:I vdd:B gnd:B
* INOUT : bl_0_0 
* INOUT : br_0_0 
* INOUT : bl_0_1 
* INOUT : br_0_1 
* INPUT : wl_0_0 
* POWER : vdd 
* GROUND: gnd 
Xbit_r0_c0 bl_0_0 br_0_0 wl_0_0 vdd gnd dummy_cell_1rw
Xbit_r0_c1 bl_0_1 br_0_1 wl_0_0 vdd gnd dummy_cell_1rw
.ENDS dummy_array_1

.SUBCKT dummy_array_0 bl_0_0 br_0_0 bl_0_1 br_0_1 wl_0_0 vdd gnd
*.PININFO bl_0_0:B br_0_0:B bl_0_1:B br_0_1:B wl_0_0:I vdd:B gnd:B
* INOUT : bl_0_0 
* INOUT : br_0_0 
* INOUT : bl_0_1 
* INOUT : br_0_1 
* INPUT : wl_0_0 
* POWER : vdd 
* GROUND: gnd 
Xbit_r0_c0 bl_0_0 br_0_0 wl_0_0 vdd gnd dummy_cell_1rw
Xbit_r0_c1 bl_0_1 br_0_1 wl_0_0 vdd gnd dummy_cell_1rw
.ENDS dummy_array_0

*********************** "cell_1rw" ******************************
.SUBCKT cell_1rw bl br wl vdd gnd
* SPICE3 file created from cell_1rw.ext - technology: scmos

* Inverter 1
M1000 Q Q_bar vdd vdd p w=0.6u l=0.8u
M1002 Q Q_bar gnd gnd n w=1.6u l=0.4u

* Inverter 2
M1001 vdd Q Q_bar vdd p w=0.6u l=0.8u
M1003 gnd Q Q_bar gnd n w=1.6u l=0.4u

* Access transistors
M1004 Q wl bl gnd n w=0.8u l=0.4u
M1005 Q_bar wl br gnd n w=0.8u l=0.4u

.ENDS

.SUBCKT bitcell_array bl_0_0 br_0_0 bl_0_1 br_0_1 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 vdd gnd
*.PININFO bl_0_0:B br_0_0:B bl_0_1:B br_0_1:B wl_0_0:I wl_0_1:I wl_0_2:I wl_0_3:I wl_0_4:I wl_0_5:I wl_0_6:I wl_0_7:I wl_0_8:I wl_0_9:I wl_0_10:I wl_0_11:I wl_0_12:I wl_0_13:I wl_0_14:I wl_0_15:I vdd:B gnd:B
* INOUT : bl_0_0 
* INOUT : br_0_0 
* INOUT : bl_0_1 
* INOUT : br_0_1 
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
* POWER : vdd 
* GROUND: gnd 
* rows: 16 cols: 2
Xbit_r0_c0 bl_0_0 br_0_0 wl_0_0 vdd gnd cell_1rw
Xbit_r1_c0 bl_0_0 br_0_0 wl_0_1 vdd gnd cell_1rw
Xbit_r2_c0 bl_0_0 br_0_0 wl_0_2 vdd gnd cell_1rw
Xbit_r3_c0 bl_0_0 br_0_0 wl_0_3 vdd gnd cell_1rw
Xbit_r4_c0 bl_0_0 br_0_0 wl_0_4 vdd gnd cell_1rw
Xbit_r5_c0 bl_0_0 br_0_0 wl_0_5 vdd gnd cell_1rw
Xbit_r6_c0 bl_0_0 br_0_0 wl_0_6 vdd gnd cell_1rw
Xbit_r7_c0 bl_0_0 br_0_0 wl_0_7 vdd gnd cell_1rw
Xbit_r8_c0 bl_0_0 br_0_0 wl_0_8 vdd gnd cell_1rw
Xbit_r9_c0 bl_0_0 br_0_0 wl_0_9 vdd gnd cell_1rw
Xbit_r10_c0 bl_0_0 br_0_0 wl_0_10 vdd gnd cell_1rw
Xbit_r11_c0 bl_0_0 br_0_0 wl_0_11 vdd gnd cell_1rw
Xbit_r12_c0 bl_0_0 br_0_0 wl_0_12 vdd gnd cell_1rw
Xbit_r13_c0 bl_0_0 br_0_0 wl_0_13 vdd gnd cell_1rw
Xbit_r14_c0 bl_0_0 br_0_0 wl_0_14 vdd gnd cell_1rw
Xbit_r15_c0 bl_0_0 br_0_0 wl_0_15 vdd gnd cell_1rw
Xbit_r0_c1 bl_0_1 br_0_1 wl_0_0 vdd gnd cell_1rw
Xbit_r1_c1 bl_0_1 br_0_1 wl_0_1 vdd gnd cell_1rw
Xbit_r2_c1 bl_0_1 br_0_1 wl_0_2 vdd gnd cell_1rw
Xbit_r3_c1 bl_0_1 br_0_1 wl_0_3 vdd gnd cell_1rw
Xbit_r4_c1 bl_0_1 br_0_1 wl_0_4 vdd gnd cell_1rw
Xbit_r5_c1 bl_0_1 br_0_1 wl_0_5 vdd gnd cell_1rw
Xbit_r6_c1 bl_0_1 br_0_1 wl_0_6 vdd gnd cell_1rw
Xbit_r7_c1 bl_0_1 br_0_1 wl_0_7 vdd gnd cell_1rw
Xbit_r8_c1 bl_0_1 br_0_1 wl_0_8 vdd gnd cell_1rw
Xbit_r9_c1 bl_0_1 br_0_1 wl_0_9 vdd gnd cell_1rw
Xbit_r10_c1 bl_0_1 br_0_1 wl_0_10 vdd gnd cell_1rw
Xbit_r11_c1 bl_0_1 br_0_1 wl_0_11 vdd gnd cell_1rw
Xbit_r12_c1 bl_0_1 br_0_1 wl_0_12 vdd gnd cell_1rw
Xbit_r13_c1 bl_0_1 br_0_1 wl_0_13 vdd gnd cell_1rw
Xbit_r14_c1 bl_0_1 br_0_1 wl_0_14 vdd gnd cell_1rw
Xbit_r15_c1 bl_0_1 br_0_1 wl_0_15 vdd gnd cell_1rw
.ENDS bitcell_array

.SUBCKT dummy_array_2 bl_0_0 br_0_0 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 wl_0_16 wl_0_17 wl_0_18 vdd gnd
*.PININFO bl_0_0:B br_0_0:B wl_0_0:I wl_0_1:I wl_0_2:I wl_0_3:I wl_0_4:I wl_0_5:I wl_0_6:I wl_0_7:I wl_0_8:I wl_0_9:I wl_0_10:I wl_0_11:I wl_0_12:I wl_0_13:I wl_0_14:I wl_0_15:I wl_0_16:I wl_0_17:I wl_0_18:I vdd:B gnd:B
* INOUT : bl_0_0 
* INOUT : br_0_0 
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
* INPUT : wl_0_17 
* INPUT : wl_0_18 
* POWER : vdd 
* GROUND: gnd 
Xbit_r0_c0 bl_0_0 br_0_0 wl_0_0 vdd gnd dummy_cell_1rw
Xbit_r1_c0 bl_0_0 br_0_0 wl_0_1 vdd gnd dummy_cell_1rw
Xbit_r2_c0 bl_0_0 br_0_0 wl_0_2 vdd gnd dummy_cell_1rw
Xbit_r3_c0 bl_0_0 br_0_0 wl_0_3 vdd gnd dummy_cell_1rw
Xbit_r4_c0 bl_0_0 br_0_0 wl_0_4 vdd gnd dummy_cell_1rw
Xbit_r5_c0 bl_0_0 br_0_0 wl_0_5 vdd gnd dummy_cell_1rw
Xbit_r6_c0 bl_0_0 br_0_0 wl_0_6 vdd gnd dummy_cell_1rw
Xbit_r7_c0 bl_0_0 br_0_0 wl_0_7 vdd gnd dummy_cell_1rw
Xbit_r8_c0 bl_0_0 br_0_0 wl_0_8 vdd gnd dummy_cell_1rw
Xbit_r9_c0 bl_0_0 br_0_0 wl_0_9 vdd gnd dummy_cell_1rw
Xbit_r10_c0 bl_0_0 br_0_0 wl_0_10 vdd gnd dummy_cell_1rw
Xbit_r11_c0 bl_0_0 br_0_0 wl_0_11 vdd gnd dummy_cell_1rw
Xbit_r12_c0 bl_0_0 br_0_0 wl_0_12 vdd gnd dummy_cell_1rw
Xbit_r13_c0 bl_0_0 br_0_0 wl_0_13 vdd gnd dummy_cell_1rw
Xbit_r14_c0 bl_0_0 br_0_0 wl_0_14 vdd gnd dummy_cell_1rw
Xbit_r15_c0 bl_0_0 br_0_0 wl_0_15 vdd gnd dummy_cell_1rw
Xbit_r16_c0 bl_0_0 br_0_0 wl_0_16 vdd gnd dummy_cell_1rw
Xbit_r17_c0 bl_0_0 br_0_0 wl_0_17 vdd gnd dummy_cell_1rw
Xbit_r18_c0 bl_0_0 br_0_0 wl_0_18 vdd gnd dummy_cell_1rw
.ENDS dummy_array_2

.SUBCKT replica_bitcell_array rbl_bl_0_0 rbl_br_0_0 bl_0_0 br_0_0 bl_0_1 br_0_1 rbl_wl_0_0 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 vdd gnd
*.PININFO rbl_bl_0_0:B rbl_br_0_0:B bl_0_0:B br_0_0:B bl_0_1:B br_0_1:B rbl_wl_0_0:I wl_0_0:I wl_0_1:I wl_0_2:I wl_0_3:I wl_0_4:I wl_0_5:I wl_0_6:I wl_0_7:I wl_0_8:I wl_0_9:I wl_0_10:I wl_0_11:I wl_0_12:I wl_0_13:I wl_0_14:I wl_0_15:I vdd:B gnd:B
* INOUT : rbl_bl_0_0 
* INOUT : rbl_br_0_0 
* INOUT : bl_0_0 
* INOUT : br_0_0 
* INOUT : bl_0_1 
* INOUT : br_0_1 
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
* POWER : vdd 
* GROUND: gnd 
* rbl: None left_rbl: None right_rbl: None
Xbitcell_array bl_0_0 br_0_0 bl_0_1 br_0_1 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 vdd gnd bitcell_array
Xreplica_col_0 rbl_bl_0_0 rbl_br_0_0 gnd rbl_wl_0_0 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 gnd vdd gnd replica_column
Xdummy_row_0 bl_0_0 br_0_0 bl_0_1 br_0_1 rbl_wl_0_0 vdd gnd dummy_array
Xdummy_row_bot bl_0_0 br_0_0 bl_0_1 br_0_1 gnd vdd gnd dummy_array_1
Xdummy_row_top bl_0_0 br_0_0 bl_0_1 br_0_1 gnd vdd gnd dummy_array_0
Xdummy_col_left dummy_left_bl_0_0 dummy_left_br_0_0 gnd rbl_wl_0_0 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 gnd vdd gnd dummy_array_2
Xdummy_col_right dummy_right_bl_0_0 dummy_right_br_0_0 gnd rbl_wl_0_0 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 gnd vdd gnd dummy_array_3
.ENDS replica_bitcell_array

* spice ptx M{0} {1} p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p

.SUBCKT precharge_0 bl br en_bar vdd
*.PININFO bl:O br:O en_bar:I vdd:B
* OUTPUT: bl 
* OUTPUT: br 
* INPUT : en_bar 
* POWER : vdd 
Mlower_pmos bl en_bar br vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mupper_pmos1 bl en_bar vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mupper_pmos2 br en_bar vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
.ENDS precharge_0

.SUBCKT precharge_array bl_0 br_0 bl_1 br_1 bl_2 br_2 en_bar vdd
*.PININFO bl_0:O br_0:O bl_1:O br_1:O bl_2:O br_2:O en_bar:I vdd:B
* OUTPUT: bl_0 
* OUTPUT: br_0 
* OUTPUT: bl_1 
* OUTPUT: br_1 
* OUTPUT: bl_2 
* OUTPUT: br_2 
* INPUT : en_bar 
* POWER : vdd 
* cols: 3 size: 1 bl: bl br: br
Xpre_column_0 bl_0 br_0 en_bar vdd precharge_0
Xpre_column_1 bl_1 br_1 en_bar vdd precharge_0
Xpre_column_2 bl_2 br_2 en_bar vdd precharge_0
.ENDS precharge_array
*********************** "sense_amp" ******************************

.SUBCKT sense_amp bl br dout en vdd gnd

* SPICE3 file created from sense_amp.ext - technology: scmos

M1000 gnd en a_56_432# gnd n w=1.8u l=0.4u
M1001 a_56_432# a_48_304# dout gnd n w=1.8u l=0.4u
M1002 a_48_304# dout a_56_432# gnd n w=1.8u l=0.4u
M1003 vdd a_48_304# dout vdd p w=3.6u l=0.4u
M1004 a_48_304# dout vdd vdd p w=3.6u l=0.4u
M1005 bl en dout vdd p w=4.8u l=0.4u
M1006 a_48_304# en br vdd p w=4.8u l=0.4u

.ENDS

.SUBCKT sense_amp_array data_0 bl_0 br_0 data_1 bl_1 br_1 en vdd gnd
*.PININFO data_0:O bl_0:I br_0:I data_1:O bl_1:I br_1:I en:I vdd:B gnd:B
* OUTPUT: data_0 
* INPUT : bl_0 
* INPUT : br_0 
* OUTPUT: data_1 
* INPUT : bl_1 
* INPUT : br_1 
* INPUT : en 
* POWER : vdd 
* GROUND: gnd 
* words_per_row: 1
Xsa_d0 bl_0 br_0 data_0 en vdd gnd sense_amp
Xsa_d1 bl_1 br_1 data_1 en vdd gnd sense_amp
.ENDS sense_amp_array
*********************** Write_Driver ******************************
.SUBCKT write_driver din bl br en vdd gnd

**** Inverter to conver Data_in to data_in_bar ******
* din_bar = inv(din)
M_1 din_bar din gnd gnd n W=0.8u L=0.4u
M_2 din_bar din vdd vdd p W=1.4u L=0.4u

**** 2input nand gate follwed by inverter to drive BL ******
* din_bar_gated = nand(en, din)
M_3 din_bar_gated en net_7 gnd n W=1.4u L=0.4u
M_4 net_7 din gnd gnd n W=1.4u L=0.4u
M_5 din_bar_gated en vdd vdd p W=1.4u L=0.4u
M_6 din_bar_gated din vdd vdd p W=1.4u L=0.4u
* din_bar_gated_bar = inv(din_bar_gated)
M_7 din_bar_gated_bar din_bar_gated vdd vdd p W=1.4u L=0.4u
M_8 din_bar_gated_bar din_bar_gated gnd gnd n W=0.8u L=0.4u

**** 2input nand gate follwed by inverter to drive BR******
* din_gated = nand(en, din_bar)
M_9 din_gated en vdd vdd p W=1.4u L=0.4u
M_10 din_gated en net_8 gnd n W=1.4u L=0.4u
M_11 net_8 din_bar gnd gnd n W=1.4u L=0.4u
M_12 din_gated din_bar vdd vdd p W=1.4u L=0.4u
* din_gated_bar = inv(din_gated)
M_13 din_gated_bar din_gated vdd vdd p W=1.4u L=0.4u
M_14 din_gated_bar din_gated gnd gnd n W=0.8u L=0.4u

************************************************
* pull down with en enable
M_15 bl din_gated_bar gnd gnd n W=2.4u L=0.4u
M_16 br din_bar_gated_bar gnd gnd n W=2.4u L=0.4u



.ENDS   $ write_driver

.SUBCKT write_driver_array data_0 data_1 bl_0 br_0 bl_1 br_1 en vdd gnd
*.PININFO data_0:I data_1:I bl_0:O br_0:O bl_1:O br_1:O en:I vdd:B gnd:B
* INPUT : data_0 
* INPUT : data_1 
* OUTPUT: bl_0 
* OUTPUT: br_0 
* OUTPUT: bl_1 
* OUTPUT: br_1 
* INPUT : en 
* POWER : vdd 
* GROUND: gnd 
* word_size 2
Xwrite_driver0 data_0 bl_0 br_0 en vdd gnd write_driver
Xwrite_driver1 data_1 bl_1 br_1 en vdd gnd write_driver
.ENDS write_driver_array

.SUBCKT port_data rbl_bl rbl_br bl_0 br_0 bl_1 br_1 dout_0 dout_1 din_0 din_1 s_en p_en_bar w_en vdd gnd
*.PININFO rbl_bl:B rbl_br:B bl_0:B br_0:B bl_1:B br_1:B dout_0:O dout_1:O din_0:I din_1:I s_en:I p_en_bar:I w_en:I vdd:B gnd:B
* INOUT : rbl_bl 
* INOUT : rbl_br 
* INOUT : bl_0 
* INOUT : br_0 
* INOUT : bl_1 
* INOUT : br_1 
* OUTPUT: dout_0 
* OUTPUT: dout_1 
* INPUT : din_0 
* INPUT : din_1 
* INPUT : s_en 
* INPUT : p_en_bar 
* INPUT : w_en 
* POWER : vdd 
* GROUND: gnd 
Xprecharge_array0 rbl_bl rbl_br bl_0 br_0 bl_1 br_1 p_en_bar vdd precharge_array
Xsense_amp_array0 dout_0 bl_0 br_0 dout_1 bl_1 br_1 s_en vdd gnd sense_amp_array
Xwrite_driver_array0 din_0 din_1 bl_0 br_0 bl_1 br_1 w_en vdd gnd write_driver_array
.ENDS port_data

* spice ptx M{0} {1} n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p

* spice ptx M{0} {1} n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p

.SUBCKT pnand2 A B Z vdd gnd
*.PININFO A:I B:I Z:O vdd:B gnd:B
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpnand2_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
.ENDS pnand2

* spice ptx M{0} {1} n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p

* spice ptx M{0} {1} p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p

.SUBCKT pinv A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
.ENDS pinv

.SUBCKT and2_dec A B Z vdd gnd
*.PININFO A:I B:I Z:O vdd:B gnd:B
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 1
Xpand2_dec_nand A B zb_int vdd gnd pnand2
Xpand2_dec_inv zb_int Z vdd gnd pinv
.ENDS and2_dec

.SUBCKT hierarchical_predecode2x4 in_0 in_1 out_0 out_1 out_2 out_3 vdd gnd
*.PININFO in_0:I in_1:I out_0:O out_1:O out_2:O out_3:O vdd:B gnd:B
* INPUT : in_0 
* INPUT : in_1 
* OUTPUT: out_0 
* OUTPUT: out_1 
* OUTPUT: out_2 
* OUTPUT: out_3 
* POWER : vdd 
* GROUND: gnd 
Xpre_inv_0 in_0 inbar_0 vdd gnd pinv
Xpre_inv_1 in_1 inbar_1 vdd gnd pinv
XXpre2x4_and_0 inbar_0 inbar_1 out_0 vdd gnd and2_dec
XXpre2x4_and_1 in_0 inbar_1 out_1 vdd gnd and2_dec
XXpre2x4_and_2 inbar_0 in_1 out_2 vdd gnd and2_dec
XXpre2x4_and_3 in_0 in_1 out_3 vdd gnd and2_dec
.ENDS hierarchical_predecode2x4

.SUBCKT hierarchical_decoder addr_0 addr_1 addr_2 addr_3 decode_0 decode_1 decode_2 decode_3 decode_4 decode_5 decode_6 decode_7 decode_8 decode_9 decode_10 decode_11 decode_12 decode_13 decode_14 decode_15 vdd gnd
*.PININFO addr_0:I addr_1:I addr_2:I addr_3:I decode_0:O decode_1:O decode_2:O decode_3:O decode_4:O decode_5:O decode_6:O decode_7:O decode_8:O decode_9:O decode_10:O decode_11:O decode_12:O decode_13:O decode_14:O decode_15:O vdd:B gnd:B
* INPUT : addr_0 
* INPUT : addr_1 
* INPUT : addr_2 
* INPUT : addr_3 
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
* POWER : vdd 
* GROUND: gnd 
Xpre_0 addr_0 addr_1 out_0 out_1 out_2 out_3 vdd gnd hierarchical_predecode2x4
Xpre_1 addr_2 addr_3 out_4 out_5 out_6 out_7 vdd gnd hierarchical_predecode2x4
XDEC_AND_0 out_0 out_4 decode_0 vdd gnd and2_dec
XDEC_AND_4 out_0 out_5 decode_4 vdd gnd and2_dec
XDEC_AND_8 out_0 out_6 decode_8 vdd gnd and2_dec
XDEC_AND_12 out_0 out_7 decode_12 vdd gnd and2_dec
XDEC_AND_1 out_1 out_4 decode_1 vdd gnd and2_dec
XDEC_AND_5 out_1 out_5 decode_5 vdd gnd and2_dec
XDEC_AND_9 out_1 out_6 decode_9 vdd gnd and2_dec
XDEC_AND_13 out_1 out_7 decode_13 vdd gnd and2_dec
XDEC_AND_2 out_2 out_4 decode_2 vdd gnd and2_dec
XDEC_AND_6 out_2 out_5 decode_6 vdd gnd and2_dec
XDEC_AND_10 out_2 out_6 decode_10 vdd gnd and2_dec
XDEC_AND_14 out_2 out_7 decode_14 vdd gnd and2_dec
XDEC_AND_3 out_3 out_4 decode_3 vdd gnd and2_dec
XDEC_AND_7 out_3 out_5 decode_7 vdd gnd and2_dec
XDEC_AND_11 out_3 out_6 decode_11 vdd gnd and2_dec
XDEC_AND_15 out_3 out_7 decode_15 vdd gnd and2_dec
.ENDS hierarchical_decoder

.SUBCKT and2_dec_0 A B Z vdd gnd
*.PININFO A:I B:I Z:O vdd:B gnd:B
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* size: 1
Xpand2_dec_nand A B zb_int vdd gnd pnand2
Xpand2_dec_inv zb_int Z vdd gnd pinv
.ENDS and2_dec_0

.SUBCKT wordline_driver A B Z vdd gnd
*.PININFO A:I B:I Z:O vdd:B gnd:B
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Xwld_nand A B zb_int vdd gnd pnand2
Xwl_driver zb_int Z vdd gnd pinv
.ENDS wordline_driver

.SUBCKT wordline_driver_array in_0 in_1 in_2 in_3 in_4 in_5 in_6 in_7 in_8 in_9 in_10 in_11 in_12 in_13 in_14 in_15 wl_0 wl_1 wl_2 wl_3 wl_4 wl_5 wl_6 wl_7 wl_8 wl_9 wl_10 wl_11 wl_12 wl_13 wl_14 wl_15 en vdd gnd
*.PININFO in_0:I in_1:I in_2:I in_3:I in_4:I in_5:I in_6:I in_7:I in_8:I in_9:I in_10:I in_11:I in_12:I in_13:I in_14:I in_15:I wl_0:O wl_1:O wl_2:O wl_3:O wl_4:O wl_5:O wl_6:O wl_7:O wl_8:O wl_9:O wl_10:O wl_11:O wl_12:O wl_13:O wl_14:O wl_15:O en:I vdd:B gnd:B
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
* INPUT : en 
* POWER : vdd 
* GROUND: gnd 
* rows: 16 cols: 2
Xwl_driver_and0 in_0 en wl_0 vdd gnd wordline_driver
Xwl_driver_and1 in_1 en wl_1 vdd gnd wordline_driver
Xwl_driver_and2 in_2 en wl_2 vdd gnd wordline_driver
Xwl_driver_and3 in_3 en wl_3 vdd gnd wordline_driver
Xwl_driver_and4 in_4 en wl_4 vdd gnd wordline_driver
Xwl_driver_and5 in_5 en wl_5 vdd gnd wordline_driver
Xwl_driver_and6 in_6 en wl_6 vdd gnd wordline_driver
Xwl_driver_and7 in_7 en wl_7 vdd gnd wordline_driver
Xwl_driver_and8 in_8 en wl_8 vdd gnd wordline_driver
Xwl_driver_and9 in_9 en wl_9 vdd gnd wordline_driver
Xwl_driver_and10 in_10 en wl_10 vdd gnd wordline_driver
Xwl_driver_and11 in_11 en wl_11 vdd gnd wordline_driver
Xwl_driver_and12 in_12 en wl_12 vdd gnd wordline_driver
Xwl_driver_and13 in_13 en wl_13 vdd gnd wordline_driver
Xwl_driver_and14 in_14 en wl_14 vdd gnd wordline_driver
Xwl_driver_and15 in_15 en wl_15 vdd gnd wordline_driver
.ENDS wordline_driver_array

.SUBCKT port_address addr_0 addr_1 addr_2 addr_3 wl_en wl_0 wl_1 wl_2 wl_3 wl_4 wl_5 wl_6 wl_7 wl_8 wl_9 wl_10 wl_11 wl_12 wl_13 wl_14 wl_15 rbl_wl vdd gnd
*.PININFO addr_0:I addr_1:I addr_2:I addr_3:I wl_en:I wl_0:O wl_1:O wl_2:O wl_3:O wl_4:O wl_5:O wl_6:O wl_7:O wl_8:O wl_9:O wl_10:O wl_11:O wl_12:O wl_13:O wl_14:O wl_15:O rbl_wl:O vdd:B gnd:B
* INPUT : addr_0 
* INPUT : addr_1 
* INPUT : addr_2 
* INPUT : addr_3 
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
* OUTPUT: rbl_wl 
* POWER : vdd 
* GROUND: gnd 
Xrow_decoder addr_0 addr_1 addr_2 addr_3 dec_out_0 dec_out_1 dec_out_2 dec_out_3 dec_out_4 dec_out_5 dec_out_6 dec_out_7 dec_out_8 dec_out_9 dec_out_10 dec_out_11 dec_out_12 dec_out_13 dec_out_14 dec_out_15 vdd gnd hierarchical_decoder
Xwordline_driver dec_out_0 dec_out_1 dec_out_2 dec_out_3 dec_out_4 dec_out_5 dec_out_6 dec_out_7 dec_out_8 dec_out_9 dec_out_10 dec_out_11 dec_out_12 dec_out_13 dec_out_14 dec_out_15 wl_0 wl_1 wl_2 wl_3 wl_4 wl_5 wl_6 wl_7 wl_8 wl_9 wl_10 wl_11 wl_12 wl_13 wl_14 wl_15 wl_en vdd gnd wordline_driver_array
Xrbl_driver wl_en vdd rbl_wl vdd gnd and2_dec_0
.ENDS port_address

.SUBCKT bank dout0_0 dout0_1 rbl_bl_0_0 din0_0 din0_1 addr0_0 addr0_1 addr0_2 addr0_3 s_en0 p_en_bar0 w_en0 wl_en0 vdd gnd
*.PININFO dout0_0:O dout0_1:O rbl_bl_0_0:O din0_0:I din0_1:I addr0_0:I addr0_1:I addr0_2:I addr0_3:I s_en0:I p_en_bar0:I w_en0:I wl_en0:I vdd:B gnd:B
* OUTPUT: dout0_0 
* OUTPUT: dout0_1 
* OUTPUT: rbl_bl_0_0 
* INPUT : din0_0 
* INPUT : din0_1 
* INPUT : addr0_0 
* INPUT : addr0_1 
* INPUT : addr0_2 
* INPUT : addr0_3 
* INPUT : s_en0 
* INPUT : p_en_bar0 
* INPUT : w_en0 
* INPUT : wl_en0 
* POWER : vdd 
* GROUND: gnd 
Xbitcell_array rbl_bl_0_0 rbl_br_0_0 bl_0_0 br_0_0 bl_0_1 br_0_1 rbl_wl0 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 vdd gnd replica_bitcell_array
Xport_data0 rbl_bl_0_0 rbl_br_0_0 bl_0_0 br_0_0 bl_0_1 br_0_1 dout0_0 dout0_1 din0_0 din0_1 s_en0 p_en_bar0 w_en0 vdd gnd port_data
Xport_address0 addr0_0 addr0_1 addr0_2 addr0_3 wl_en0 wl_0_0 wl_0_1 wl_0_2 wl_0_3 wl_0_4 wl_0_5 wl_0_6 wl_0_7 wl_0_8 wl_0_9 wl_0_10 wl_0_11 wl_0_12 wl_0_13 wl_0_14 wl_0_15 rbl_wl0 vdd gnd port_address
.ENDS bank

* spice ptx M{0} {1} n m=1 w=4.0u l=0.4u pd=8.80u ps=8.80u as=4.00p ad=4.00p

* spice ptx M{0} {1} p m=1 w=8.0u l=0.4u pd=16.80u ps=16.80u as=8.00p ad=8.00p

.SUBCKT pinv_7 A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd p m=1 w=8.0u l=0.4u pd=16.80u ps=16.80u as=8.00p ad=8.00p
Mpinv_nmos Z A gnd gnd n m=1 w=4.0u l=0.4u pd=8.80u ps=8.80u as=4.00p ad=4.00p
.ENDS pinv_7

.SUBCKT pinv_5 A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
.ENDS pinv_5

.SUBCKT pdriver_1 A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [1, 5]
Xbuf_inv1 A Zb1_int vdd gnd pinv_5
Xbuf_inv2 Zb1_int Z vdd gnd pinv_7
.ENDS pdriver_1

.SUBCKT pnand2_1 A B Z vdd gnd
*.PININFO A:I B:I Z:O vdd:B gnd:B
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpnand2_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
.ENDS pnand2_1

* spice ptx M{0} {1} p m=1 w=19.200000000000003u l=0.4u pd=39.20u ps=39.20u as=19.20p ad=19.20p

* spice ptx M{0} {1} n m=1 w=9.600000000000001u l=0.4u pd=20.00u ps=20.00u as=9.60p ad=9.60p

.SUBCKT pinv_2 A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd p m=1 w=19.200000000000003u l=0.4u pd=39.20u ps=39.20u as=19.20p ad=19.20p
Mpinv_nmos Z A gnd gnd n m=1 w=9.600000000000001u l=0.4u pd=20.00u ps=20.00u as=9.60p ad=9.60p
.ENDS pinv_2

.SUBCKT pdriver A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [12]
Xbuf_inv1 A Z vdd gnd pinv_2
.ENDS pdriver

.SUBCKT pnand2_0 A B Z vdd gnd
*.PININFO A:I B:I Z:O vdd:B gnd:B
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpnand2_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_nmos1 Z B net1 gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand2_nmos2 net1 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
.ENDS pnand2_0

.SUBCKT pand2 A B Z vdd gnd
*.PININFO A:I B:I Z:O vdd:B gnd:B
* INPUT : A 
* INPUT : B 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Xpand2_nand A B zb_int vdd gnd pnand2_0
Xpand2_inv zb_int Z vdd gnd pdriver
.ENDS pand2

.SUBCKT pinv_11 A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
.ENDS pinv_11

.SUBCKT delay_chain in out vdd gnd
*.PININFO in:I out:O vdd:B gnd:B
* INPUT : in 
* OUTPUT: out 
* POWER : vdd 
* GROUND: gnd 
* fanouts: [4, 4, 4, 4, 4, 4, 4, 4, 4]
Xdinv0 in dout_1 vdd gnd pinv_11
Xdload_0_0 dout_1 n_0_0 vdd gnd pinv_11
Xdload_0_1 dout_1 n_0_1 vdd gnd pinv_11
Xdload_0_2 dout_1 n_0_2 vdd gnd pinv_11
Xdload_0_3 dout_1 n_0_3 vdd gnd pinv_11
Xdinv1 dout_1 dout_2 vdd gnd pinv_11
Xdload_1_0 dout_2 n_1_0 vdd gnd pinv_11
Xdload_1_1 dout_2 n_1_1 vdd gnd pinv_11
Xdload_1_2 dout_2 n_1_2 vdd gnd pinv_11
Xdload_1_3 dout_2 n_1_3 vdd gnd pinv_11
Xdinv2 dout_2 dout_3 vdd gnd pinv_11
Xdload_2_0 dout_3 n_2_0 vdd gnd pinv_11
Xdload_2_1 dout_3 n_2_1 vdd gnd pinv_11
Xdload_2_2 dout_3 n_2_2 vdd gnd pinv_11
Xdload_2_3 dout_3 n_2_3 vdd gnd pinv_11
Xdinv3 dout_3 dout_4 vdd gnd pinv_11
Xdload_3_0 dout_4 n_3_0 vdd gnd pinv_11
Xdload_3_1 dout_4 n_3_1 vdd gnd pinv_11
Xdload_3_2 dout_4 n_3_2 vdd gnd pinv_11
Xdload_3_3 dout_4 n_3_3 vdd gnd pinv_11
Xdinv4 dout_4 dout_5 vdd gnd pinv_11
Xdload_4_0 dout_5 n_4_0 vdd gnd pinv_11
Xdload_4_1 dout_5 n_4_1 vdd gnd pinv_11
Xdload_4_2 dout_5 n_4_2 vdd gnd pinv_11
Xdload_4_3 dout_5 n_4_3 vdd gnd pinv_11
Xdinv5 dout_5 dout_6 vdd gnd pinv_11
Xdload_5_0 dout_6 n_5_0 vdd gnd pinv_11
Xdload_5_1 dout_6 n_5_1 vdd gnd pinv_11
Xdload_5_2 dout_6 n_5_2 vdd gnd pinv_11
Xdload_5_3 dout_6 n_5_3 vdd gnd pinv_11
Xdinv6 dout_6 dout_7 vdd gnd pinv_11
Xdload_6_0 dout_7 n_6_0 vdd gnd pinv_11
Xdload_6_1 dout_7 n_6_1 vdd gnd pinv_11
Xdload_6_2 dout_7 n_6_2 vdd gnd pinv_11
Xdload_6_3 dout_7 n_6_3 vdd gnd pinv_11
Xdinv7 dout_7 dout_8 vdd gnd pinv_11
Xdload_7_0 dout_8 n_7_0 vdd gnd pinv_11
Xdload_7_1 dout_8 n_7_1 vdd gnd pinv_11
Xdload_7_2 dout_8 n_7_2 vdd gnd pinv_11
Xdload_7_3 dout_8 n_7_3 vdd gnd pinv_11
Xdinv8 dout_8 out vdd gnd pinv_11
Xdload_8_0 out n_8_0 vdd gnd pinv_11
Xdload_8_1 out n_8_1 vdd gnd pinv_11
Xdload_8_2 out n_8_2 vdd gnd pinv_11
Xdload_8_3 out n_8_3 vdd gnd pinv_11
.ENDS delay_chain

* spice ptx M{0} {1} n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p

* spice ptx M{0} {1} p m=1 w=3.2u l=0.4u pd=7.20u ps=7.20u as=3.20p ad=3.20p

.SUBCKT pinv_6 A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd p m=1 w=3.2u l=0.4u pd=7.20u ps=7.20u as=3.20p ad=3.20p
Mpinv_nmos Z A gnd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
.ENDS pinv_6

.SUBCKT pdriver_3 A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [2]
Xbuf_inv1 A Z vdd gnd pinv_6
.ENDS pdriver_3

* spice ptx M{0} {1} n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p

.SUBCKT pnand3_0 A B C Z vdd gnd
*.PININFO A:I B:I C:I Z:O vdd:B gnd:B
* INPUT : A 
* INPUT : B 
* INPUT : C 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpnand3_pmos1 vdd A Z vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand3_pmos2 Z B vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand3_pmos3 Z C vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand3_nmos1 Z C net1 gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand3_nmos2 net1 B net2 gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpnand3_nmos3 net2 A gnd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
.ENDS pnand3_0

.SUBCKT pand3_0 A B C Z vdd gnd
*.PININFO A:I B:I C:I Z:O vdd:B gnd:B
* INPUT : A 
* INPUT : B 
* INPUT : C 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Xpand3_nand A B C zb_int vdd gnd pnand3_0
Xpand3_inv zb_int Z vdd gnd pdriver_3
.ENDS pand3_0

* spice ptx M{0} {1} p m=1 w=24.0u l=0.4u pd=48.80u ps=48.80u as=24.00p ad=24.00p

* spice ptx M{0} {1} n m=1 w=12.0u l=0.4u pd=24.80u ps=24.80u as=12.00p ad=12.00p

.SUBCKT pinv_8 A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd p m=1 w=24.0u l=0.4u pd=48.80u ps=48.80u as=24.00p ad=24.00p
Mpinv_nmos Z A gnd gnd n m=1 w=12.0u l=0.4u pd=24.80u ps=24.80u as=12.00p ad=12.00p
.ENDS pinv_8

.SUBCKT pdriver_0 A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [1, 2, 5, 15]
Xbuf_inv1 A Zb1_int vdd gnd pinv_5
Xbuf_inv2 Zb1_int Zb2_int vdd gnd pinv_6
Xbuf_inv3 Zb2_int Zb3_int vdd gnd pinv_7
Xbuf_inv4 Zb3_int Z vdd gnd pinv_8
.ENDS pdriver_0

* spice ptx M{0} {1} n m=1 w=3.2u l=0.4u pd=7.20u ps=7.20u as=3.20p ad=3.20p

* spice ptx M{0} {1} p m=1 w=6.4u l=0.4u pd=13.60u ps=13.60u as=6.40p ad=6.40p

.SUBCKT pinv_1 A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd p m=1 w=6.4u l=0.4u pd=13.60u ps=13.60u as=6.40p ad=6.40p
Mpinv_nmos Z A gnd gnd n m=1 w=3.2u l=0.4u pd=7.20u ps=7.20u as=3.20p ad=3.20p
.ENDS pinv_1

.SUBCKT pinv_0 A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd p m=1 w=3.2u l=0.4u pd=7.20u ps=7.20u as=3.20p ad=3.20p
Mpinv_nmos Z A gnd gnd n m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
.ENDS pinv_0

.SUBCKT dff_buf_0 D Q Qb clk vdd gnd
*.PININFO D:I Q:O Qb:O clk:I vdd:B gnd:B
* INPUT : D 
* OUTPUT: Q 
* OUTPUT: Qb 
* INPUT : clk 
* POWER : vdd 
* GROUND: gnd 
* inv1: 2 inv2: 4
Xdff_buf_dff D qint clk vdd gnd dff
Xdff_buf_inv1 qint Qb vdd gnd pinv_0
Xdff_buf_inv2 Qb Q vdd gnd pinv_1
.ENDS dff_buf_0

.SUBCKT dff_buf_array din_0 din_1 dout_0 dout_bar_0 dout_1 dout_bar_1 clk vdd gnd
*.PININFO din_0:I din_1:I dout_0:O dout_bar_0:O dout_1:O dout_bar_1:O clk:I vdd:B gnd:B
* INPUT : din_0 
* INPUT : din_1 
* OUTPUT: dout_0 
* OUTPUT: dout_bar_0 
* OUTPUT: dout_1 
* OUTPUT: dout_bar_1 
* INPUT : clk 
* POWER : vdd 
* GROUND: gnd 
* inv1: 2 inv2: 4
Xdff_r0_c0 din_0 dout_0 dout_bar_0 clk vdd gnd dff_buf_0
Xdff_r1_c0 din_1 dout_1 dout_bar_1 clk vdd gnd dff_buf_0
.ENDS dff_buf_array

.SUBCKT pinv_10 A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd p m=1 w=1.6u l=0.4u pd=4.00u ps=4.00u as=1.60p ad=1.60p
Mpinv_nmos Z A gnd gnd n m=1 w=0.8u l=0.4u pd=2.40u ps=2.40u as=0.80p ad=0.80p
.ENDS pinv_10

.SUBCKT pdriver_4 A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [1, 1]
Xbuf_inv1 A Zb1_int vdd gnd pinv_5
Xbuf_inv2 Zb1_int Z vdd gnd pinv_5
.ENDS pdriver_4

* spice ptx M{0} {1} p m=1 w=16.0u l=0.4u pd=32.80u ps=32.80u as=16.00p ad=16.00p

* spice ptx M{0} {1} n m=1 w=8.0u l=0.4u pd=16.80u ps=16.80u as=8.00p ad=8.00p

.SUBCKT pinv_9 A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Mpinv_pmos Z A vdd vdd p m=1 w=16.0u l=0.4u pd=32.80u ps=32.80u as=16.00p ad=16.00p
Mpinv_nmos Z A gnd gnd n m=1 w=8.0u l=0.4u pd=16.80u ps=16.80u as=8.00p ad=8.00p
.ENDS pinv_9

.SUBCKT pdriver_2 A Z vdd gnd
*.PININFO A:I Z:O vdd:B gnd:B
* INPUT : A 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
* sizes: [10]
Xbuf_inv1 A Z vdd gnd pinv_9
.ENDS pdriver_2

.SUBCKT pand3 A B C Z vdd gnd
*.PININFO A:I B:I C:I Z:O vdd:B gnd:B
* INPUT : A 
* INPUT : B 
* INPUT : C 
* OUTPUT: Z 
* POWER : vdd 
* GROUND: gnd 
Xpand3_nand A B C zb_int vdd gnd pnand3_0
Xpand3_inv zb_int Z vdd gnd pdriver_2
.ENDS pand3

.SUBCKT control_logic_rw csb web clk rbl_bl s_en w_en p_en_bar wl_en clk_buf vdd gnd
*.PININFO csb:I web:I clk:I rbl_bl:I s_en:O w_en:O p_en_bar:O wl_en:O clk_buf:O vdd:B gnd:B
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
* word_size 2
Xctrl_dffs csb web cs_bar cs we_bar we clk_buf vdd gnd dff_buf_array
Xclkbuf clk clk_buf vdd gnd pdriver_0
Xinv_clk_bar clk_buf clk_bar vdd gnd pinv_10
Xand2_gated_clk_bar clk_bar cs gated_clk_bar vdd gnd pand2
Xand2_gated_clk_buf clk_buf cs gated_clk_buf vdd gnd pand2
Xbuf_wl_en gated_clk_bar wl_en vdd gnd pdriver_1
Xrbl_bl_delay_inv rbl_bl_delay rbl_bl_delay_bar vdd gnd pinv_10
Xw_en_and we rbl_bl_delay_bar gated_clk_bar w_en vdd gnd pand3
Xbuf_s_en_and rbl_bl_delay gated_clk_bar we_bar s_en vdd gnd pand3_0
Xdelay_chain rbl_bl rbl_bl_delay vdd gnd delay_chain
Xnand_p_en_bar gated_clk_buf rbl_bl_delay p_en_bar_unbuf vdd gnd pnand2_1
Xbuf_p_en_bar p_en_bar_unbuf p_en_bar vdd gnd pdriver_4
.ENDS control_logic_rw

.SUBCKT data_dff din_0 din_1 dout_0 dout_1 clk vdd gnd
*.PININFO din_0:I din_1:I dout_0:O dout_1:O clk:I vdd:B gnd:B
* INPUT : din_0 
* INPUT : din_1 
* OUTPUT: dout_0 
* OUTPUT: dout_1 
* INPUT : clk 
* POWER : vdd 
* GROUND: gnd 
* rows: 1 cols: 2
Xdff_r0_c0 din_0 dout_0 clk vdd gnd dff
Xdff_r0_c1 din_1 dout_1 clk vdd gnd dff
.ENDS data_dff

.SUBCKT sram_2_16_scn4m_subm din0[0] din0[1] addr0[0] addr0[1] addr0[2] addr0[3] csb0 web0 clk0 dout0[0] dout0[1] vdd gnd
*.PININFO din0[0]:I din0[1]:I addr0[0]:I addr0[1]:I addr0[2]:I addr0[3]:I csb0:I web0:I clk0:I dout0[0]:O dout0[1]:O vdd:B gnd:B
* INPUT : din0[0] 
* INPUT : din0[1] 
* INPUT : addr0[0] 
* INPUT : addr0[1] 
* INPUT : addr0[2] 
* INPUT : addr0[3] 
* INPUT : csb0 
* INPUT : web0 
* INPUT : clk0 
* OUTPUT: dout0[0] 
* OUTPUT: dout0[1] 
* POWER : vdd 
* GROUND: gnd 
Xbank0 dout0[0] dout0[1] rbl_bl0 bank_din0_0 bank_din0_1 a0_0 a0_1 a0_2 a0_3 s_en0 p_en_bar0 w_en0 wl_en0 vdd gnd bank
Xcontrol0 csb0 web0 clk0 rbl_bl0 s_en0 w_en0 p_en_bar0 wl_en0 clk_buf0 vdd gnd control_logic_rw
Xrow_address0 addr0[0] addr0[1] addr0[2] addr0[3] a0_0 a0_1 a0_2 a0_3 clk_buf0 vdd gnd row_addr_dff
Xdata_dff0 din0[0] din0[1] bank_din0_0 bank_din0_1 clk_buf0 vdd gnd data_dff
.ENDS sram_2_16_scn4m_subm
