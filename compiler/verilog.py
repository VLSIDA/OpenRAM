import debug

class verilog:
    """ Create a behavioral Verilog file for simulation."""

    def __init__(self,verilog_name,sram):
        self.sram_name = sram.name
        self.num_words = sram.num_words
        self.word_size = sram.word_size
        self.addr_size = sram.addr_size
    
        debug.info(1,"Writing to {0}".format(verilog_name))
        self.vf = open(verilog_name, "w")
    
        self.create()

        self.vf.close()


    def create(self):
        self.vf.write("// OpenRAM SRAM model\n")
        self.vf.write("// Words: {0}\n".format(self.num_words))
        self.vf.write("// Word size: {0}\n\n".format(self.word_size))
    
        self.vf.write("module {0}(DATA,ADDR,CSb,WEb,OEb,clk);\n".format(self.sram_name))
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


    
# //SRAM Model
# module sram(CSB,WRB,ABUS,DATABUS);
#   input CSB;             // active low chip select
#   input WRB;             // active low write control
#   input [11:0] ABUS;     // 12-bit address bus
#   inout [7:0] DATABUS;   // 8-bit data bus
#                  //** internal signals
#   reg  [7:0] DATABUS_driver;
#   wire [7:0] DATABUS = DATABUS_driver;
#   reg [7:0] ram[0:4095];            // memory cells
#   integer i;

#   initial     //initialize all RAM cells to 0 at startup
#     begin
#     DATABUS_driver = 8'bzzzzzzzz;
#     for (i=0; i < 4095; i = i + 1)
#        ram[i] = 0;
#     end

#   always @(CSB or WRB or ABUS)
#     begin
#       if (CSB == 1'b0)
#         begin
#         if (WRB == 1'b0) //Start: latch Data on rising edge of CSB or WRB
#           begin
#           DATABUS_driver <= #10 8'bzzzzzzzz;
#           @(posedge CSB or posedge WRB);
#           $display($time," Writing %m ABUS=%b DATA=%b",ABUS,DATABUS);
#           ram[ABUS] = DATABUS;
#           end
#         if (WRB == 1'b1) //Reading from sram (data becomes valid after 10ns)
#           begin
#           #10 DATABUS_driver =  ram[ABUS];
#           $display($time," Reading %m ABUS=%b DATA=%b",ABUS,DATABUS_driver);
#           end
#         end
#       else //sram unselected, stop driving bus after 10ns
#         begin
#         DATABUS_driver <=  #10 8'bzzzzzzzz;
#         end
#     end
# endmodule

