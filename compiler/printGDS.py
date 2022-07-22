#!/usr/bin/env python3

import sys
from gdsMill import gdsMill

if len(sys.argv) < 2:
    print("Usage: {0} file.gds".format(sys.argv[0]))
    sys.exit(1)

gds_file = sys.argv[1]  
arrayCellLayout = gdsMill.VlsiLayout()
reader = gdsMill.Gds2reader(arrayCellLayout,debugToTerminal = 1)
reader.loadFromFile(gds_file)

