from template import template

dict = {
        'module_name': 'sram_1kbyte_32b_2bank', 
        'bank_module_name': 'sram_1kbyte_32b_2bank_1bank', 
        'vdd': 'vdd', 
        'gnd': 'gnd', 
        'ports': [0, 1], 
        'rw_ports': [0], 
        'r_ports': [1], 
        'w_ports': [],
        'banks': [0, 1],
        'data_width': 32, 
        'addr_width': 8,
        'bank_sel': 1,
        'num_wmask': 4
        }
t = template('../sram/sram_multibank_template.v', dict)
t.write(dict['module_name'] + '.v')

