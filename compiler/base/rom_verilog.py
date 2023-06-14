# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import math
from openram.tech import spice


class rom_verilog:
    """
    Create a behavioral Verilog file for simulation.
    This is inherited by the rom_base class.
    """
    def __init__(self):
        pass

    def verilog_write(self, verilog_name):
        """ Write a behavioral Verilog model. """
        self.vf = open(verilog_name, "w")

        self.vf.write("// OpenROM ROM model\n")

        #basic info
        self.vf.write("// Words: {0}\n".format(self.num_words))
        self.vf.write("// Word size: {0}\n".format(self.word_size))
        self.vf.write("// Word per Row: {0}\n".format(self.words_per_row))
        self.vf.write("// Data Type: {0}\n".format(self.data_type))
        self.vf.write("// Data File: {0}\n".format(self.rom_data))

        self.vf.write("\n")

        try:
            self.vdd_name = spice["power"]
        except KeyError:
            self.vdd_name = "vdd"
        try:
            self.gnd_name = spice["ground"]
        except KeyError:
            self.gnd_name = "gnd"

        #add multiple banks later
        self.vf.write("module {0}(\n".format(self.name))
        self.vf.write("`ifdef USE_POWER_PINS\n")
        self.vf.write("    {},\n".format(self.vdd_name))
        self.vf.write("    {},\n".format(self.gnd_name))
        self.vf.write("`endif\n")

        for port in self.all_ports:
            if port in self.read_ports:
                self.vf.write("// Port {0}: R\n".format(port))
                self.vf.write("    clk{0},csb{0},addr{0},dout{0}".format(port))
            # Continue for every port on a new line
            if port != self.all_ports[-1]:
                self.vf.write(",\n")
        self.vf.write("\n  );\n\n")

        self.vf.write("  parameter DATA_WIDTH = {0} ;\n".format(self.word_size))
        self.vf.write("  parameter ADDR_WIDTH = {0} ;\n".format(math.ceil(math.log(self.num_words,2))))
        self.vf.write("  parameter ROM_DEPTH = 1 << ADDR_WIDTH;\n")
        self.vf.write("  // FIXME: This delay is arbitrary.\n")
        self.vf.write("  parameter DELAY = 3 ;\n")
        self.vf.write("  parameter VERBOSE = 1 ; //Set to 0 to only display warnings\n")
        self.vf.write("  parameter T_HOLD = 1 ; //Delay to hold dout value after posedge. Value is arbitrary\n")
        self.vf.write("\n")

        self.vf.write("`ifdef USE_POWER_PINS\n")
        self.vf.write("    inout {};\n".format(self.vdd_name))
        self.vf.write("    inout {};\n".format(self.gnd_name))
        self.vf.write("`endif\n")

        for port in self.all_ports:
            self.add_inputs_outputs(port)

        self.vf.write("\n")

        # This is the memory array itself
        self.vf.write("  reg [DATA_WIDTH-1:0]    mem [0:ROM_DEPTH-1];\n\n")

        #write memory init here
        self.vf.write(f"  initial begin\n")
        if self.data_type == "bin":
            self.vf.write(f"    $readmemb(\"{self.rom_data}\",mem,0,ROM_DEPTH-1);\n")
        elif self.data_type == "hex":
            self.vf.write(f"    $readmemh(\"{self.rom_data}\",mem,0, ROM_DEPTH-1);\n")
        else:
            raise ValueError(f"Data type: {self.data_type} is not supported!")
        self.vf.write(f"  end\n\n")

        for port in self.all_ports:
            self.register_inputs(port)

        for port in self.all_ports:
            if port in self.read_ports:
                self.add_read_block(port)

        self.vf.write("\n")
        self.vf.write("endmodule\n")
        self.vf.close()

    def register_inputs(self, port):
        """
        Register the control signal, address and data inputs.
        """
        self.add_regs(port)
        self.add_flops(port)

    def add_regs(self, port):
        """
        Create the input regs for the given port.
        """
        self.vf.write("  reg  csb{0}_reg;\n".format(port))
        self.vf.write("  reg [ADDR_WIDTH-1:0]  addr{0}_reg;\n".format(port))
        if port in self.read_ports:
            self.vf.write("  reg [DATA_WIDTH-1:0]  dout{0};\n".format(port))


    def add_flops(self, port):
        """
        Add the flop behavior logic for a port.
        """
        self.vf.write("\n")
        self.vf.write("  // All inputs are registers\n")
        self.vf.write("  always @(posedge clk{0})\n".format(port))
        self.vf.write("  begin\n")
        self.vf.write("    csb{0}_reg = csb{0};\n".format(port))
        self.vf.write("    addr{0}_reg = addr{0};\n".format(port))
        if port in self.read_ports:
            self.add_write_read_checks(port)

        if port in self.read_ports:
            self.vf.write("    #(T_HOLD) dout{0} = {1}'bx;\n".format(port, self.word_size))
            self.vf.write("    if ( !csb{0}_reg && VERBOSE ) \n".format(port))
            self.vf.write("      $display($time,\" Reading %m addr{0}=%b dout{0}=%b\",addr{0}_reg,mem[addr{0}_reg]);\n".format(port))

        self.vf.write("  end\n\n")

    def add_inputs_outputs(self, port):
        """
        Add the module input and output declaration for a port.
        """
        self.vf.write("  input  clk{0}; // clock\n".format(port))
        self.vf.write("  input   csb{0}; // active low chip select\n".format(port))

        self.vf.write("  input [ADDR_WIDTH-1:0]  addr{0};\n".format(port))
        if port in self.read_ports:
            self.vf.write("  output [DATA_WIDTH-1:0] dout{0};\n".format(port))

    def add_write_block(self, port):
        """
        ROM does not take writes thus this function does nothing
        """
        self.vf.write("\n")
    def add_read_block(self, port):
        """
        Add a read port block.
        """
        self.vf.write("\n")
        self.vf.write("  // Memory Read Block Port {0}\n".format(port))
        self.vf.write("  // Read Operation : When web{0} = 1, csb{0} = 0\n".format(port))
        self.vf.write("  always @ (negedge clk{0})\n".format(port))
        self.vf.write("  begin : MEM_READ{0}\n".format(port))
        self.vf.write("    if (!csb{0}_reg)\n".format(port))
        self.vf.write("       dout{0} <= #(DELAY) mem[addr{0}_reg];\n".format(port))
        self.vf.write("  end\n")

    def add_write_read_checks(self, rport):
        """
        Since ROMs dont have write ports this does nothing
        """
        pass
