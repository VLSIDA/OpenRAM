# This is a temp file. Remove either this or the fake_sram.py

from modules import sram
import debug
from globals import OPTS
import os


class fake_sram_v2(sram):

    def create_netlist(self):
        # Make sure spice file is here
        debug.check(os.path.exists(self.sp_name), "Spice netlist in {} not found".format(self.sp_name))

    def generate_pins(self):
        self.pins = ['vdd', 'gnd']
        self.pins.extend(['clk{}'.format(port) for port in range(
            OPTS.num_rw_ports + OPTS.num_r_ports + OPTS.num_w_ports)])
        for port in range(OPTS.num_rw_ports):
            self.pins.extend(['din{0}[{1}]'.format(port, bit)
                              for bit in range(self.num_cols)])
            self.pins.extend(['dout{0}[{1}]'.format(port, bit)
                              for bit in range(self.num_cols)])
            self.pins.extend(['addr{0}[{1}]'.format(port, bit)
                              for bit in range(self.addr_size)])
            #if self.num_wmasks != 0:
            #    self.pins.extend(['wmask{0}[{1}]'.format(port, bit)
            #                      for bit in range(self.num_wmasks)])

            self.pins.extend(['csb{}'.format(port), 'web{}'.format(port)])

        start_port = OPTS.num_rw_ports
        for port in range(start_port, start_port + OPTS.num_r_ports):
            self.pins.extend(['dout{0}[{1}]'.format(port, bit)
                              for bit in range(self.num_cols)])
            self.pins.extend(['addr{0}[{1}]'.format(port, bit)
                              for bit in range(self.addr_size)])

            self.pins.extend(['csb{}'.format(port)])

        start_port += OPTS.num_r_ports
        for port in range(start_port, start_port + OPTS.num_w_ports):
            self.pins.extend(['din{0}[{1}]'.format(port, bit)
                              for bit in range(self.num_cols)])
            self.pins.extend(['addr{0}[{1}]'.format(port, bit)
                              for bit in range(self.addr_size)])
            if self.num_wmasks != 0:
                self.pins.extend(['wmask{0}[{1}]'.format(port, bit)
                                  for bit in range(self.num_wmasks)])

            self.pins.extend(['csb{}'.format(port), 'web{}'.format(port)])
