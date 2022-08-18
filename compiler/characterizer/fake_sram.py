from modules import sram_config
from math import ceil
import re


class fake_sram(sram_config):
    """
    This is an SRAM class that doesn't actually create an instance.
    It will read neccessary members from HTML file from a previous run.
    """
    def __init__(self, name, word_size, num_words, write_size=None, num_banks=1,
                 words_per_row=None, num_spare_rows=0, num_spare_cols=0):
        self.name = name
        self.word_size = word_size
        self.num_words = num_words
        # Don't add a write mask if it is the same size as the data word
        if write_size and write_size==word_size:
            self.write_size = None
        else:
            self.write_size = write_size
        self.num_banks = num_banks
        self.num_spare_rows = num_spare_rows
        self.num_spare_cols = num_spare_cols

        try:
            from tech import array_row_multiple
            self.array_row_multiple = array_row_multiple
        except ImportError:
            self.array_row_multiple = 1
        try:
            from tech import array_col_multiple
            self.array_col_multiple = array_col_multiple
        except ImportError:
            self.array_col_multiple = 1

        if self.write_size:
            self.num_wmasks = int(ceil(self.word_size / self.write_size))
        else:
            self.num_wmasks = 0

        if not self.num_spare_cols:
            self.num_spare_cols = 0

        if not self.num_spare_rows:
            self.num_spare_rows = 0

        # This will get over-written when we determine the organization
        self.words_per_row = words_per_row

        self.compute_sizes()
        self.pins = ['vdd', 'gnd', 'clk0'] # TODO: remove clk

    def setup_multiport_constants(self):
        """
        Taken from ../base/design.py
        These are contants and lists that aid multiport design.
        Ports are always in the order RW, W, R.
        Port indices start from 0 and increment.
        A first RW port will have clk0, csb0, web0, addr0, data0
        A first W port (with no RW ports) will be: clk0, csb0, addr0, data0

        """
        total_ports = self.num_rw_ports + self.num_w_ports + self.num_r_ports

        # These are the read/write port indices.
        self.readwrite_ports = []
        # These are the read/write and write-only port indices
        self.write_ports = []
        # These are the write-only port indices.
        self.writeonly_ports = []
        # These are the read/write and read-only port indices
        self.read_ports = []
        # These are the read-only port indices.
        self.readonly_ports = []
        # These are all the ports
        self.all_ports = list(range(total_ports))

        # The order is always fixed as RW, W, R
        port_number = 0
        for port in range(self.num_rw_ports):
            self.readwrite_ports.append(port_number)
            self.write_ports.append(port_number)
            self.read_ports.append(port_number)
            port_number += 1
        for port in range(self.num_w_ports):
            self.write_ports.append(port_number)
            self.writeonly_ports.append(port_number)
            port_number += 1
        for port in range(self.num_r_ports):
            self.read_ports.append(port_number)
            self.readonly_ports.append(port_number)
            port_number += 1

    def str_to_pins(self, s):
        pinsRE = re.compile(r'^(\w+)\[(\d+):(\d+)\]')
        match = pinsRE.match(s)
        port, start, end = match.group(1, 2, 3)
        pins = [port + '[' + str(p) + ']' for p in range(int(start) - int(end) + 1)]
        return pins

    def parse_html(self, filename):
        """
        Parse the HTML file generated from previous SRAM generation
        and populate the members
        """
        with open(filename, 'r') as html:
            for line in html:
                if 'Ports and Configuration' in line:
                    configRE = re.compile(r'<tr><td>(\w*)</td><td>(\w*)</td></tr>')
                    values = configRE.finditer(line)
                    for val in values:
                        if val.group(1) == 'WORD_SIZE':
                            self.word_size = int(val.group(2))
                        elif val.group(1) == 'NUM_WORDS':
                            self.num_words = int(val.group(2))
                        elif val.group(1) == 'NUM_BANKS':
                            self.num_banks = int(val.group(2))
                        elif val.group(1) == 'NUM_RW_PORTS':
                            self.num_rw_ports = int(val.group(2))
                        elif val.group(1) == 'NUM_R_PORTS':
                            self.num_r_ports = int(val.group(2))
                        elif val.group(1) == 'NUM_W_PORTS':
                            self.num_w_ports = int(val.group(2))
                        elif val.group(1) == 'Area (&microm<sup>2</sup>)':
                            self.height = int(val.group(2) ** 0.5)
                            self.width = int(val.group(2) ** 0.5)
                if 'Timing Data' in line:
                    timingRE = re.compile(r'<tr><td>([\w\[\]:]*) \w* \w*</td><td>[\w\.]*</td><td>[\w\.]*</td><td>\w*</td></tr>')
                    values = timingRE.finditer(line)
                    for val in values:
                        if '[' in val.group(1):
                            pins = self.str_to_pins(val.group(1))
                            for pin in pins:
                                if pin not in self.pins:
                                    self.pins.append(pin)
                        else:
                            if val.group(1) not in self.pins:
                                self.pins.append(val.group(1))
