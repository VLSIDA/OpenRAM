// OpenRAM SRAM model
// Words: 16
// Word size: 2

module sram_2_16_1_freepdk45(
// Port 0: RW
    clk0,csb0,web0,ADDR0,DIN0,DOUT0
  );

  parameter DATA_WIDTH = 2 ;
  parameter ADDR_WIDTH = 4 ;
  parameter RAM_DEPTH = 1 << ADDR_WIDTH;
  // FIXME: This delay is arbitrary.
  parameter DELAY = 3 ;

  input  clk0; // clock
  input   csb0; // active low chip select
  input  web0; // active low write control
  input [ADDR_WIDTH-1:0]  ADDR0;
  input [DATA_WIDTH-1:0]  DIN0;
  output [DATA_WIDTH-1:0] DOUT0;

  reg  csb0_reg;
  reg  web0_reg;
  reg [ADDR_WIDTH-1:0]  ADDR0_reg;
  reg [DATA_WIDTH-1:0]  DIN0_reg;
  reg [DATA_WIDTH-1:0]  DOUT0;

  // All inputs are registers
  always @(posedge clk0)
  begin
    csb0_reg = csb0;
    web0_reg = web0;
    ADDR0_reg = ADDR0;
    DIN0_reg = DIN0;
    DOUT0 = 2'bx;
    if ( !csb0_reg && web0_reg ) 
      $display($time," Reading %m ADDR0=%b DOUT0=%b",ADDR0_reg,mem[ADDR0_reg]);
    if ( !csb0_reg && !web0_reg )
      $display($time," Writing %m ADDR0=%b DIN0=%b",ADDR0_reg,DIN0_reg);
  end

reg [DATA_WIDTH-1:0]    mem [0:RAM_DEPTH-1];

  // Memory Write Block Port 0
  // Write Operation : When web0 = 0, csb0 = 0
  always @ (negedge clk0)
  begin : MEM_WRITE0
    if ( !csb0_reg && !web0_reg )
        mem[ADDR0_reg] = DIN0_reg;
  end

  // Memory Read Block Port 0
  // Read Operation : When web0 = 1, csb0 = 0
  always @ (negedge clk0)
  begin : MEM_READ0
    if (!csb0_reg && web0_reg)
       DOUT0 <= #(DELAY) mem[ADDR0_reg];
  end

endmodule
