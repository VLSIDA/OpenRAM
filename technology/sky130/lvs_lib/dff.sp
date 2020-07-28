* SPICE3 file created from dff.ext - technology: EFS8A

.subckt dff D Q clk vdd gnd
M1000 a_511_725# a_n8_115# vdd vdd pshort W=3u L=0.15u m=1
M1001 a_353_115# clk a_11_624# gnd nshort W=1u L=0.15u m=1
M1002 a_353_725# a_203_89# a_11_624# vdd pshort W=3u L=0.15u m=1
M1003 a_11_624# a_203_89# a_161_115# gnd nshort W=1u L=0.15u m=1
M1004 a_11_624# clk a_161_725# vdd pshort W=3u L=0.15u m=1
M1005 gnd Q a_703_115# gnd nshort W=1u L=0.15u m=1
M1006 vdd Q a_703_725# vdd pshort W=3u L=0.15u m=1
M1007 a_203_89# clk gnd gnd nshort W=1u L=0.15u m=1
M1008 a_203_89# clk vdd vdd pshort W=3u L=0.15u m=1
M1009 a_161_115# D gnd gnd nshort W=1u L=0.15u m=1
M1010 a_161_725# D vdd vdd pshort W=3u L=0.15u m=1
M1011 gnd a_11_624# a_n8_115# gnd nshort W=1u L=0.15u m=1
M1012 a_703_115# a_203_89# ON gnd nshort W=1u L=0.15u m=1
M1013 vdd a_11_624# a_n8_115# vdd pshort W=3u L=0.15u m=1
M1014 a_703_725# clk ON vdd pshort W=3u L=0.15u m=1
M1015 Q ON vdd vdd pshort W=3u L=0.15u m=1
M1016 Q ON gnd gnd nshort W=1u L=0.15u m=1
M1017 ON a_203_89# a_511_725# vdd pshort W=3u L=0.15u m=1
M1018 ON clk a_511_115# gnd nshort W=1u L=0.15u m=1
M1019 gnd a_n8_115# a_353_115# gnd nshort W=1u L=0.15u m=1
M1020 vdd a_n8_115# a_353_725# vdd pshort W=3u L=0.15u m=1
M1021 a_511_115# a_n8_115# gnd gnd nshort W=1u L=0.15u m=1
.ends
