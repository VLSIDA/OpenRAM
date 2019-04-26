# Setup file for netgen
ignore class c
equate class {-circuit1 nfet} {-circuit2 n}
equate class {-circuit1 pfet} {-circuit2 p}
# This circuit has symmetries and needs to be flattened to resolve them
# or the banks won't pass
flatten class {-circuit1 bitcell_array_0}
flatten class {-circuit1 bitcell_array_1}
#flatten class {-circuit1 precharge_array_0}
#flatten class {-circuit1 precharge_array_1}
#flatten class {-circuit1 precharge_array_2}
#flatten class {-circuit1 precharge_array_3}
property {-circuit1 nfet} remove as ad ps pd
property {-circuit1 pfet} remove as ad ps pd
property {-circuit2 n} remove as ad ps pd
property {-circuit2 p} remove as ad ps pd
permute transistors
