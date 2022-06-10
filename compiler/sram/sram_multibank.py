from template import template
from globals import OPTS


class sram_multibank:

    def __init__(self, sram):
        dict = {
                'module_name': OPTS.output_name, 
                'bank_module_name': OPTS.output_name + '_1bank', 
                'vdd': 'vdd', 
                'gnd': 'gnd', 
                'ports': sram.all_ports, 
                'rw_ports': sram.readwrite_ports, 
                'r_ports': sram.read_ports, 
                'w_ports': sram.write_ports,
                'banks': sram.banks,
                'data_width': sram.word_size, 
                'addr_width': sram.addr_size,
                'bank_sel': list(range(sram.num_banks)),
                'num_wmask': sram.num_wmasks
                }

    def verilog_write():
        t = template('../sram/sram_multibank_template.v', dict)
        t.write(OPTS.output_name + '.v')

