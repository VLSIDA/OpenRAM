"""
Pseudo-dual port (independent read and write ports), 8bit word, 1 kbyte SRAM.

Useful as a byte FIFO between two devices (the reader and the writer).
"""
word_size = 8 # Bits
num_words = 1024
human_byte_size = "{:.0f}kbytes".format((word_size * num_words)/1024/8)

# Allow byte writes
write_size = 8 # Bits

# Dual port
num_rw_ports = 0
num_r_ports = 1
num_w_ports = 1
ports_human = '1r1w'

import os
exec(open(os.path.join(os.path.dirname(__file__), 'sky130_sram_common.py')).read())
