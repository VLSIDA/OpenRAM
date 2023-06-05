# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import math
from openram.tech import spice


class verilog:
    """
    Create a behavioral Verilog file for simulation.
    This is inherited by the sram_base class.
    """
    def __init__(self):
        pass

    def verilog_write(self, verilog_name):
        """ Write a behavioral Verilog model. """
        self.vf = open(verilog_name, "w")

        self.vf.write("// OpenRAM SRAM model\n")
        self.vf.write("// Words: {0}\n".format(self.num_words))
        self.vf.write("// Word size: {0}\n".format(self.word_size))
        if self.write_size != self.word_size:
            self.vf.write("// Write size: {0}\n\n".format(self.write_size))
        else:
            self.vf.write("\n")

        try:
            self.vdd_name = spice["power"]
        except KeyError:
            self.vdd_name = "vdd"
        try:
            self.gnd_name = spice["ground"]
        except KeyError:
            self.gnd_name = "gnd"

        if self.num_banks > 1:
            self.vf.write("module {0}(\n".format(self.name))
        else:
            self.vf.write("module {0}(\n".format(self.name))
        self.vf.write("`ifdef USE_POWER_PINS\n")
        self.vf.write("    {},\n".format(self.vdd_name))
        self.vf.write("    {},\n".format(self.gnd_name))
        self.vf.write("`endif\n")

        for port in self.all_ports:
            if port in self.readwrite_ports:
                self.vf.write("// Port {0}: RW\n".format(port))
            elif port in self.read_ports:
                self.vf.write("// Port {0}: R\n".format(port))
            elif port in self.write_ports:
                self.vf.write("// Port {0}: W\n".format(port))
            if port in self.readwrite_ports:
                self.vf.write("    clk{0},csb{0},web{0},".format(port))
                if self.write_size != self.word_size:
                    self.vf.write("wmask{},".format(port))
                if self.num_spare_cols > 0:
                    self.vf.write("spare_wen{0},".format(port))
                self.vf.write("addr{0},din{0},dout{0}".format(port))
            elif port in self.write_ports:
                self.vf.write("    clk{0},csb{0},".format(port))
                if self.write_size != self.word_size:
                    self.vf.write("wmask{},".format(port))
                if self.num_spare_cols > 0:
                    self.vf.write("spare_wen{0},".format(port))
                self.vf.write("addr{0},din{0}".format(port))
            elif port in self.read_ports:
                self.vf.write("    clk{0},csb{0},addr{0},dout{0}".format(port))
            # Continue for every port on a new line
            if port != self.all_ports[-1]:
                self.vf.write(",\n")
        self.vf.write("\n  );\n\n")

        if self.write_size != self.word_size:
            self.num_wmasks = int(math.ceil(self.word_size / self.write_size))
            self.vf.write("  parameter NUM_WMASKS = {0} ;\n".format(self.num_wmasks))
        self.vf.write("  parameter DATA_WIDTH = {0} ;\n".format(self.word_size + self.num_spare_cols))
        self.vf.write("  parameter ADDR_WIDTH = {0} ;\n".format(self.bank_addr_size))
        self.vf.write("  parameter RAM_DEPTH = 1 << ADDR_WIDTH;\n")
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
        self.vf.write("  reg [DATA_WIDTH-1:0]    mem [0:RAM_DEPTH-1];\n\n")

        for port in self.all_ports:
            self.register_inputs(port)

        for port in self.all_ports:
            if port in self.write_ports:
                self.add_write_block(port)
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
        if port in self.readwrite_ports:
            self.vf.write("  reg  web{0}_reg;\n".format(port))
        if port in self.write_ports:
            if self.write_size != self.word_size:
                self.vf.write("  reg [NUM_WMASKS-1:0]   wmask{0}_reg;\n".format(port))
            if self.num_spare_cols > 1:
                self.vf.write("  reg [{1}:0] spare_wen{0}_reg;".format(port, self.num_spare_cols - 1))
            elif self.num_spare_cols == 1:
                self.vf.write("  reg spare_wen{0}_reg;\n".format(port))
        self.vf.write("  reg [ADDR_WIDTH-1:0]  addr{0}_reg;\n".format(port))
        if port in self.write_ports:
            self.vf.write("  reg [DATA_WIDTH-1:0]  din{0}_reg;\n".format(port))
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
        if port in self.readwrite_ports:
            self.vf.write("    web{0}_reg = web{0};\n".format(port))
        if port in self.write_ports:
            if self.write_size != self.word_size:
                self.vf.write("    wmask{0}_reg = wmask{0};\n".format(port))
            if self.num_spare_cols:
                self.vf.write("    spare_wen{0}_reg = spare_wen{0};\n".format(port))
        self.vf.write("    addr{0}_reg = addr{0};\n".format(port))
        if port in self.read_ports:
            self.add_write_read_checks(port)

        if port in self.write_ports:
            self.vf.write("    din{0}_reg = din{0};\n".format(port))
        if port in self.read_ports:
            self.vf.write("    #(T_HOLD) dout{0} = {1}'bx;\n".format(port, self.word_size))
        if port in self.readwrite_ports:
            self.vf.write("    if ( !csb{0}_reg && web{0}_reg && VERBOSE )\n".format(port))
            self.vf.write("      $display($time,\" Reading %m addr{0}=%b dout{0}=%b\",addr{0}_reg,mem[addr{0}_reg]);\n".format(port))
        elif port in self.read_ports:
            self.vf.write("    if ( !csb{0}_reg && VERBOSE ) \n".format(port))
            self.vf.write("      $display($time,\" Reading %m addr{0}=%b dout{0}=%b\",addr{0}_reg,mem[addr{0}_reg]);\n".format(port))
        if port in self.readwrite_ports:
            self.vf.write("    if ( !csb{0}_reg && !web{0}_reg && VERBOSE )\n".format(port))
            if self.write_size != self.word_size:
                self.vf.write("      $display($time,\" Writing %m addr{0}=%b din{0}=%b wmask{0}=%b\",addr{0}_reg,din{0}_reg,wmask{0}_reg);\n".format(port))
            else:
                self.vf.write("      $display($time,\" Writing %m addr{0}=%b din{0}=%b\",addr{0}_reg,din{0}_reg);\n".format(port))
        elif port in self.write_ports:
            self.vf.write("    if ( !csb{0}_reg && VERBOSE )\n".format(port))
            if self.write_size != self.word_size:
                self.vf.write("      $display($time,\" Writing %m addr{0}=%b din{0}=%b wmask{0}=%b\",addr{0}_reg,din{0}_reg,wmask{0}_reg);\n".format(port))
            else:
                self.vf.write("      $display($time,\" Writing %m addr{0}=%b din{0}=%b\",addr{0}_reg,din{0}_reg);\n".format(port))

        self.vf.write("  end\n\n")

    def add_inputs_outputs(self, port):
        """
        Add the module input and output declaration for a port.
        """
        self.vf.write("  input  clk{0}; // clock\n".format(port))
        self.vf.write("  input   csb{0}; // active low chip select\n".format(port))
        if port in self.readwrite_ports:
            self.vf.write("  input  web{0}; // active low write control\n".format(port))

        self.vf.write("  input [ADDR_WIDTH-1:0]  addr{0};\n".format(port))
        if port in self.write_ports:
            if self.write_size != self.word_size:
                self.vf.write("  input [NUM_WMASKS-1:0]   wmask{0}; // write mask\n".format(port))
            if self.num_spare_cols == 1:
                self.vf.write("  input           spare_wen{0}; // spare mask\n".format(port))
            elif self.num_spare_cols > 1:
                self.vf.write("  input [{1}:0]   spare_wen{0}; // spare mask\n".format(port, self.num_spare_cols-1))
            self.vf.write("  input [DATA_WIDTH-1:0]  din{0};\n".format(port))
        if port in self.read_ports:
            self.vf.write("  output [DATA_WIDTH-1:0] dout{0};\n".format(port))

    def add_write_block(self, port):
        """
        Add a write port block. Multiple simultaneous writes to the same address
        have arbitrary priority and are not allowed.
        """
        self.vf.write("\n")
        self.vf.write("  // Memory Write Block Port {0}\n".format(port))
        self.vf.write("  // Write Operation : When web{0} = 0, csb{0} = 0\n".format(port))
        self.vf.write("  always @ (negedge clk{0})\n".format(port))
        self.vf.write("  begin : MEM_WRITE{0}\n".format(port))
        if port in self.readwrite_ports:
            self.vf.write("    if ( !csb{0}_reg && !web{0}_reg ) begin\n".format(port))
        else:
            self.vf.write("    if (!csb{0}_reg) begin\n".format(port))

        if self.write_size != self.word_size:
            for mask in range(0, self.num_wmasks):
                lower = mask * self.write_size
                upper = lower + self.write_size - 1
                self.vf.write("        if (wmask{0}_reg[{1}])\n".format(port, mask))
                self.vf.write("                mem[addr{0}_reg][{1}:{2}] = din{0}_reg[{1}:{2}];\n".format(port, upper, lower))
        else:
            upper = self.word_size - self.num_spare_cols - 1
            self.vf.write("        mem[addr{0}_reg][{1}:0] = din{0}_reg[{1}:0];\n".format(port, upper))

        if self.num_spare_cols == 1:
            self.vf.write("        if (spare_wen{0}_reg)\n".format(port))
            self.vf.write("                mem[addr{0}_reg][{1}] = din{0}_reg[{1}];\n".format(port, self.word_size))
        else:
            for num in range(self.num_spare_cols):
                self.vf.write("        if (spare_wen{0}_reg[{1}])\n".format(port, num))
                self.vf.write("                mem[addr{0}_reg][{1}] = din{0}_reg[{1}];\n".format(port, self.word_size + num))

        self.vf.write("    end\n")
        self.vf.write("  end\n")

    def add_read_block(self, port):
        """
        Add a read port block.
        """
        self.vf.write("\n")
        self.vf.write("  // Memory Read Block Port {0}\n".format(port))
        self.vf.write("  // Read Operation : When web{0} = 1, csb{0} = 0\n".format(port))
        self.vf.write("  always @ (negedge clk{0})\n".format(port))
        self.vf.write("  begin : MEM_READ{0}\n".format(port))
        if port in self.readwrite_ports:
            self.vf.write("    if (!csb{0}_reg && web{0}_reg)\n".format(port))
        else:
            self.vf.write("    if (!csb{0}_reg)\n".format(port))
        self.vf.write("       dout{0} <= #(DELAY) mem[addr{0}_reg];\n".format(port))
        self.vf.write("  end\n")

    def add_address_check(self, wport, rport):
        """ Output a warning if the two addresses match """
        # If the rport is actually reading... and addresses match.
        if rport in self.readwrite_ports:
            rport_control = "!csb{0} && web{0}".format(rport)
        else:
            rport_control = "!csb{0}".format(rport)
        if wport in self.readwrite_ports:
            wport_control = "!csb{0} && !web{0}".format(wport)
        else:
            wport_control = "!csb{0}".format(wport)

        self.vf.write("    if ({1} && {3} && (addr{0} == addr{2}))\n".format(wport, wport_control, rport, rport_control))
        self.vf.write("         $display($time,\" WARNING: Writing and reading addr{0}=%b and addr{1}=%b simultaneously!\",addr{0},addr{1});\n".format(wport, rport))

    def add_write_read_checks(self, rport):
        """
        Add a warning if we read from an address that we are currently writing.
        Can be fixed if we appropriately size the write drivers to do this .
        """
        for wport in self.write_ports:
            if wport == rport:
                continue
            else:
                self.add_address_check(wport, rport)
