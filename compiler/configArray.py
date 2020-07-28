import sys
import os
import datetime
import optparse
from globals import OPTS
import subprocess
#OPTS = options.options()
#CHECKPOINT_OPTS = None

#global OPTS

wordsize_count = 32
wordnum_count = 256

while wordsize_count < 128:
    while wordnum_count <= 131072:
        word_size = wordsize_count
        num_words = wordnum_count
        write_size = 8
        if (wordsize_count == 256):
            wordnum_count = 2048
        elif (wordnum_count == 2048):
            wordnum_count = 8192
        else:
            wordnum_count = wordnum_count * 2
        print("config") 
        num_rw_ports = 1
        num_r_ports = 1
        num_w_ports = 0

        tech_name = "sky130"
        nominal_corners_only = True

        route_supplies = True
        check_lvsdrc = True
        perimeter_pins = True
        #netlist_only = True
        #analytical_delay = False
        output_path = "macros/sram_1rw1r_{0}_{1}_{2}_{3}".format(word_size,
	                                                         num_words,
                                                                 write_size,
                                                                 tech_name)
        output_name = "sram_1rw1r_{0}_{1}_{2}_{3}".format(word_size,
                                                          num_words,
                                                          write_size,
                                                          tech_name)

        os.system('python3 $OPENRAM_HOME/openram.py $OPENRAM_HOME/configArray.y')

    wordsize_count = wordsize_count * 2
    wordnum_count = 8192

