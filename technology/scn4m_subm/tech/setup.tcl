# Setup file for netgen
ignore class c
equate class {-circuit1 nfet} {-circuit2 n}
equate class {-circuit1 pfet} {-circuit2 p}
# We must flatten these because the ports are disconnected
flatten class {-circuit1 dummy_cell_6t}
flatten class {-circuit1 dummy_cell_1rw_1r}
flatten class {-circuit1 dummy_cell_1w_1r}
flatten class {-circuit1 dummy_pbitcell}
flatten class {-circuit1 dummy_pbitcell_0}
flatten class {-circuit1 dummy_pbitcell_1}
flatten class {-circuit1 dummy_pbitcell_2}
flatten class {-circuit1 dummy_pbitcell_3}
flatten class {-circuit1 pbitcell}
flatten class {-circuit1 pbitcell_0}
flatten class {-circuit1 pbitcell_1}
flatten class {-circuit1 pbitcell_2}
flatten class {-circuit1 pbitcell_3}
property {-circuit1 nfet} remove as ad ps pd
property {-circuit1 pfet} remove as ad ps pd
property {-circuit2 n} remove as ad ps pd
property {-circuit2 p} remove as ad ps pd
permute transistors
