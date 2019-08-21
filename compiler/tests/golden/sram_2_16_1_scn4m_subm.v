// OpenRAM SRAM model
// Words: 16
// Word size: 2

module sram_2_16_1_scn4m_subm(
// Port 0: RW
    clk0,csb0,web0,addr0,din0,dout0
  );

  parameter data_WIDTH = 2 ;
  parameter addr_WIDTH = 4 ;
  parameter RAM_DEPTH = 1 << addr_WIDTH;
  // FIXME: This delay is arbitrary.
  parameter DELAY = 3 ;

  input  clk0; // clock
  input   csb0; // active low chip select
  input  web0; // active low write control
  input [addr_WIDTH-1:0]  addr0;
  input [data_WIDTH-1:0]  din0;
  output [data_WIDTH-1:0] dout0;

  reg  csb0_reg;
  reg  web0_reg;
  reg [addr_WIDTH-1:0]  addr0_reg;
  reg [data_WIDTH-1:0]  din0_reg;
  reg [data_WIDTH-1:0]  dout0;

  // All inputs are registers
  always @(posedge clk0)
  begin
    csb0_reg = csb0;
    web0_reg = web0;
    addr0_reg = addr0;
    din0_reg = din0;
    dout0 = 2'bx;
    if ( !csb0_reg && web0_reg ) 
      $display($time," Reading %m addr0=%b dout0=%b",addr0_reg,mem[addr0_reg]);
    if ( !csb0_reg && !web0_reg )
      $display($time," Writing %m addr0=%b din0=%b",addr0_reg,din0_reg);
  end

reg [data_WIDTH-1:0]    mem [0:RAM_DEPTH-1];

  // Memory Write Block Port 0
  // Write Operation : When web0 = 0, csb0 = 0
  always @ (negedge clk0)
  begin : MEM_WRITE0
    if ( !csb0_reg && !web0_reg )
        mem[addr0_reg] = din0_reg;
  end

  // Memory Read Block Port 0
  // Read Operation : When web0 = 1, csb0 = 0
  always @ (negedge clk0)
  begin : MEM_READ0
    if (!csb0_reg && web0_reg)
       dout0 <= #(DELAY) mem[addr0_reg];
  end

endmodule
