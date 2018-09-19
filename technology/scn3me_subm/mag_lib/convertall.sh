magic -dnull -noconsole << EOF
load dff
gds write dff.gds
load cell_6t
gds write cell_6t.gds
load replica_cell_6t
gds write replica_cell_6t.gds
load sense_amp
gds write sense_amp.gds
load tri_gate
gds write tri_gate.gds
load write_driver
gds write write_driver.gds
EOF
