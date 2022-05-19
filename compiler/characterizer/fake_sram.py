import sram_config

class fake_sram(sram_config.sram_config):
    """ This is an SRAM that doesn't actually create itself, just computes
    the sizes. """
    def __init__(self, word_size, num_words, num_banks, name, num_spare_rows):
        self.name = name
        self.word_size = word_size
        self.num_words = num_words
        self.num_banks = num_banks
        self.num_spare_rows = num_spare_rows
        # TODO: Get width and height from gds bbox
        self.width = 0
        self.height = 0
        #c = reload(__import__(OPTS.bitcell))
        #self.mod_bitcell = getattr(c, OPTS.bitcell)
        #self.bitcell = self.mod_bitcell()
        # to get the row, col, etc.
        self.compute_sizes()
        self.setup_multiport_constants()

    def setup_multiport_constants(self):
        """
        Taken from ../base/design.py
        These are contants and lists that aid multiport design.
        Ports are always in the order RW, W, R.
        Port indices start from 0 and increment.
        A first RW port will have clk0, csb0, web0, addr0, data0
        A first W port (with no RW ports) will be: clk0, csb0, addr0, data0

        """
        total_ports = OPTS.num_rw_ports + OPTS.num_w_ports + OPTS.num_r_ports

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
        for port in range(OPTS.num_rw_ports):
            self.readwrite_ports.append(port_number)
            self.write_ports.append(port_number)
            self.read_ports.append(port_number)
            port_number += 1
        for port in range(OPTS.num_w_ports):
            self.write_ports.append(port_number)
            self.writeonly_ports.append(port_number)
            port_number += 1
        for port in range(OPTS.num_r_ports):
            self.read_ports.append(port_number)
            self.readonly_ports.append(port_number)
            port_number += 1
