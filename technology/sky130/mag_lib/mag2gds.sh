magic -dnull -noconsole << EOF
load $1
gds write $1.gds
EOF
mv $1.gds ../gds_lib
