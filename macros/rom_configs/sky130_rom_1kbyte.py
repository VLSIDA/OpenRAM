# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

word_size = 1

check_lvsdrc = True

rom_data = "rom_configs/example_1kbyte.bin"
data_type = "bin"

output_name = "rom_1kbyte"
output_path = "macro/{output_name}".format(**locals())

import os
exec(open(os.path.join(os.path.dirname(__file__), 'sky130_rom_common.py')).read())
