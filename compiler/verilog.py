import debug

class verilog:
    """ Create a behavioral Verilog file for simulation."""

    def verilog_write(self,verilog_name):
        """ Write a behavioral Verilog model. """
        
        self.vf = open(verilog_name, "w")

        self.vf.write("// OpenRAM SRAM model\n")
        self.vf.write("// Words: {0}\n".format(self.num_words))
        self.vf.write("// Word size: {0}\n\n".format(self.word_size))
    
        self.vf.write("module {0}(DATA,ADDR,CSb,WEb,OEb,clk);\n".format(self.name))
        self.vf.write("\n")
        self.vf.write("  parameter DATA_WIDTH = {0} ;\n".format(self.word_size))
        self.vf.write("  parameter ADDR_WIDTH = {0} ;\n".format(self.addr_size))
        self.vf.write("  parameter RAM_DEPTH = 1 << ADDR_WIDTH;\n")
        self.vf.write("  parameter DELAY = 3 ;\n")
        self.vf.write("\n")    
        self.vf.write("  inout [DATA_WIDTH-1:0] DATA;\n")
        self.vf.write("  input [ADDR_WIDTH-1:0] ADDR;\n")
        self.vf.write("  input CSb;             // active low chip select\n")
        self.vf.write("  input WEb;             // active low write control\n")
        self.vf.write("  input OEb;             // active output enable\n")
        self.vf.write("  input clk;             // clock\n")
        self.vf.write("\n")
        self.vf.write("  reg [DATA_WIDTH-1:0] data_out ;\n")
        self.vf.write("  reg [DATA_WIDTH-1:0] mem [0:RAM_DEPTH-1];\n")
        self.vf.write("\n")
        self.vf.write("  // Tri-State Buffer control\n")
        self.vf.write("  // output : When WEb = 1, oeb = 0, csb = 0\n")
        self.vf.write("  assign DATA = (!CSb && !OEb && WEb) ? data_out : {0}'bz;\n".format(self.word_size))
        self.vf.write("\n")    
        self.vf.write("  // Memory Write Block\n")
        self.vf.write("  // Write Operation : When WEb = 0, CSb = 0\n")
        self.vf.write("  always @ (posedge clk)\n")
        self.vf.write("  begin : MEM_WRITE\n")
        self.vf.write("  if ( !CSb && !WEb ) begin\n")
        self.vf.write("    mem[ADDR] = DATA;\n")
        self.vf.write("    $display($time,\" Writing %m ABUS=%b DATA=%b\",ADDR,DATA);\n")
        self.vf.write("    end\n")
        self.vf.write("  end\n\n")
        self.vf.write("\n")    
        self.vf.write("  // Memory Read Block\n")
        self.vf.write("  // Read Operation : When WEb = 1, CSb = 0\n")
        self.vf.write("  always @ (posedge clk)\n")
        self.vf.write("  begin : MEM_READ\n")
        self.vf.write("  if (!CSb && WEb) begin\n")
        self.vf.write("    data_out <= #(DELAY) mem[ADDR];\n")
        self.vf.write("    $display($time,\" Reading %m ABUS=%b DATA=%b\",ADDR,mem[ADDR]);\n")
        self.vf.write("    end\n")
        self.vf.write("  end\n")
        self.vf.write("\n")    
        self.vf.write("endmodule\n")


        self.vf.close()

