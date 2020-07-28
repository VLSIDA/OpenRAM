# We must flatten these because the ports are disconnected
flatten class {-circuit1 dummy_cell_6t}
flatten class {-circuit1 dummy_cell_1rw_1r}
flatten class {-circuit1 dummy_cell_1w_1r}
flatten class {-circuit1 bitcell_array_0}
flatten class {-circuit1 pbitcell_0}
flatten class {-circuit1 pbitcell_1}
property {-circuit1 nshort} remove as ad ps pd
property {-circuit1 pshort} remove as ad ps pd
property {-circuit2 nshort} remove as ad ps pd
property {-circuit2 pshort} remove as ad ps pd
permute transistors
