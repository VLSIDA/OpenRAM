import sram_config
import OPTS


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

    def parse_characterizer_csv(f, pages):
        """
        Parses output data of the Liberty file generator in order to construct the timing and
        current table
        """
        #TODO: Func taken from datasheet_gen.py. Read datasheet.info and extract sram members
        with open(f) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
    
                found = 0
                col = 0
    
                # defines layout of csv file
                NAME = row[col]
                col += 1
    
                NUM_WORDS = row[col]
                col += 1
    
                NUM_BANKS = row[col]
                col += 1
    
                NUM_RW_PORTS = row[col]
                col += 1
    
                NUM_W_PORTS = row[col]
                col += 1
    
                NUM_R_PORTS = row[col]
                col += 1
    
                TECH_NAME = row[col]
                col += 1
    
                TEMP = row[col]
                col += 1
    
                VOLT = row[col]
                col += 1
    
                PROC = row[col]
                col += 1
    
                MIN_PERIOD = row[col]
                col += 1
    
                OUT_DIR = row[col]
                col += 1
    
                LIB_NAME = row[col]
                col += 1
    
                WORD_SIZE = row[col]
                col += 1
    
                ORIGIN_ID = row[col]
                col += 1
    
                DATETIME = row[col]
                col += 1
    
                ANALYTICAL_MODEL = row[col]
                col += 1
    
                DRC = row[col]
                col += 1
    
                LVS = row[col]
                col += 1
    
                AREA = row[col]
                col += 1

