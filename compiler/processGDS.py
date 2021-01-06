#!/usr/bin/env python3

import sys
from gdsMill import gdsMill

if len(sys.argv) < 2:
    print("Usage: {0} in.gds out.gds".format(sys.argv[0]))
    sys.exit(1)

in_gds_file = sys.argv[1]
out_gds_file = sys.argv[2]
layout = gdsMill.VlsiLayout()
reader = gdsMill.Gds2reader(layout)
reader.loadFromFile(in_gds_file)


struct = layout.structures[layout.rootStructureName]
# Do something to the structure
for text in struct.texts:
    print(text.textString)
    text.magFactor=""
 
writer = gdsMill.Gds2writer(layout)
writer.writeToFile(out_gds_file)

