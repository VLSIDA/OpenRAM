from verilog_template import verilog_template

t = verilog_template('../sram/multibank_template.v')
t.readTemplate()
t.setSectionRepeat('RW_PORTS', 1)
t.setSectionRepeat('R_PORTS', 0)
t.setSectionRepeat('BANK_DEFS', 2)
t.setSectionRepeat('BANK_INIT', 2)
t.setSectionRepeat('BANK_CASE', 2)
t.setTextDict('PORT_NUM', 0)


t.generate('test.v')
