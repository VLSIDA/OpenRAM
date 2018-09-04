from globals import OPTS

class sram_config:
    """ This is a structure that is used to hold the SRAM configuration options. """
    
    def __init__(self, word_size, num_words, num_banks=1, num_rw_ports=OPTS.num_rw_ports, num_w_ports=OPTS.num_w_ports, num_r_ports=OPTS.num_r_ports):
        self.word_size = word_size
        self.num_words = num_words
        self.num_banks = num_banks
        self.num_rw_ports = num_rw_ports
        self.num_w_ports = num_w_ports
        self.num_r_ports = num_r_ports

        # This will get over-written when we determine the organization
        self.num_banks = 1
        self.words_per_row = None
        
        self.total_write = num_rw_ports + num_w_ports
        self.total_read = num_rw_ports + num_r_ports
        self.total_ports = num_rw_ports + num_w_ports + num_r_ports


    def set_local_config(self, module):
        module.word_size = self.word_size
        module.num_words = self.num_words
        module.num_banks = self.num_banks
        module.num_rw_ports = self.num_rw_ports
        module.num_w_ports = self.num_w_ports
        module.num_r_ports = self.num_r_ports
        
        module.words_per_row = self.words_per_row
        
        module.total_write = self.total_write
        module.total_read = self.total_read
        module.total_ports = self.total_ports

