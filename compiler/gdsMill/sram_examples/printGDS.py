#!/usr/bin/env python
import gdsMill, sys

gds_file = sys.argv[1]  #"layoutB.gds" #"sram_cell_6t.gds" #"gds_sram_tgate2.gds"
#streamer = gdsMill.GdsStreamer()

arrayCellLayout = gdsMill.VlsiLayout()
reader = gdsMill.Gds2reader(arrayCellLayout,debugToTerminal = 1)
reader.loadFromFile(gds_file)

