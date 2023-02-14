# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
import os
import re
from math import ceil, log
from openram import OPTS
from .template import template


class sram_multibank:

    def __init__(self, sram):
        rw_ports = [i for i in sram.all_ports if i in sram.read_ports and i in sram.write_ports]
        r_ports = [i for i in sram.all_ports if i in sram.read_ports and i not in sram.write_ports]
        w_ports = [i for i in sram.all_ports if i not in sram.read_ports and i in sram.write_ports]
        self.dict = {
            'module_name': sram.name + '_top',
            'bank_module_name': sram.name,
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
            'num_wmask': sram.num_wmasks,
            'write_size': sram.write_size
        }

    def verilog_write(self, name):
        template_filename = os.path.join(os.path.abspath(os.environ["OPENRAM_HOME"]), "modules/sram_multibank_template.v")
        t = template(template_filename, self.dict)
        t.write(name)
        with open(name, 'r') as f:
            text = f.read()
            badComma = re.compile(r',(\s*\n\s*\);)')
            text = badComma.sub(r'\1', text)
        with open(name, 'w') as f:
            f.write(text)
