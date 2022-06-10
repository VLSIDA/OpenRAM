from template import template
from globals import OPTS
<<<<<<< HEAD
import os
from math import ceil, log
=======
>>>>>>> 3dd65b1a (modified template engine & sram multibank class)


class sram_multibank:

    def __init__(self, sram):
<<<<<<< HEAD
        rw_ports = [i for i in sram.all_ports if i in sram.read_ports and i in sram.write_ports]
        r_ports = [i for i in sram.all_ports if i in sram.read_ports and i not in sram.write_ports]
        w_ports = [i for i in sram.all_ports if i not in sram.read_ports and i in sram.write_ports]
        self.dict = {
            'module_name': OPTS.output_name,
            'bank_module_name': OPTS.output_name + '_1bank',
            'vdd': 'vdd',
            'gnd': 'gnd',
            'ports': sram.all_ports,
            'rw_ports': rw_ports,
            'r_ports': r_ports,
            'w_ports': w_ports,
            'banks': list(range(sram.num_banks)),
            'data_width': sram.word_size,
            'addr_width': sram.bank_addr_size + ceil(log(sram.num_banks, 2)),
            'bank_sel': ceil(log(sram.num_banks, 2)),
            'num_wmask': sram.num_wmasks
            }

    def verilog_write(self, name):
        template_filename = os.path.join(os.path.abspath(os.environ["OPENRAM_HOME"]), "sram/sram_multibank_template.v")
        t = template(template_filename, self.dict)
        t.write(name)
=======
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

>>>>>>> 3dd65b1a (modified template engine & sram multibank class)
