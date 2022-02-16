// OpenRAM SRAM model
// Words: #$WORDS$#
// Word size: #$WORD_SIZE$#
#<WRITE_SIZE_CMT
// Write size: #$WRITE_SIZE$#
#>WRITE_SIZE_CMT

module #$MODULE_NAME$# (
`ifdef USE_POWER_PINS
    #$VDD$#,
    #$GND$#,
`endif
#<WRITE_MASK
    wmask#$PORT_NUM$#,
#>WRITE_MASK
#<SPARE_WEN
    spare_wen#$PORT_NUM$#,
#<SPARE_WEN
#<RW_PORT
// Port #$PORT_NUM$#: RW
    clk#$PORT_NUM#$,csb#$PORT_NUM$#,web$#PORT_NUM$#,addr#$PORT_NUM$#,din#$PORT_NUM$#,dout#$PORT_NUM$#
#>RW_PORT
#<R_PORT
// Port #$PORT_NUM$#: R
    clk#$PORT_NUM#$,csb#$PORT_NUM$#,addr#PORT_NUM$#,dout#PORT_NUM$#
#>RW_PORT
#<W_PORT
// Port #$PORT_NUM$#: W
    clk#$PORT_NUM#$,csb#$PORT_NUM$#,web$#PORT_NUM$#,addr#PORT_NUM$#,din#PORT_NUM$#
#>W_PORT
  );
#<WMASK_PAR
  parameter NUM_WMASK = #$NUM_WMASK#$ ;
#>WMASK_PAR
  parameter DATA_WIDTH = #$DATA_WIDTH$# ;
  parameter ADDR_WIDTH = #$ADD_WIDTH$# ;
  parameter RAM_DEPTH = 1 << ADDR_WIDTH;
  // FIXME: This delay is arbitrary.
  parameter DELAY = 3 ;
  parameter VERBOSE = 1 ; //Set to 0 to only display warnings
  parameter T_HOLD = 1 ; //Delay to hold dout value after posedge. Value is arbitrary

`ifdef USE_POWER_PINS
    inout #$VDD$#;
    inout #$GND$#;
`endif

#<WRITE_MASK
    input [NUM_WMASK-1:0] wmask#$PORT_NUM$#;
#>WRITE_MASK
#<SPARE_WEN_SINGLE
    input spare_wen#$PORT_NUM$#;
#<SPARE_WEN_SINGLE
#<SPARE_WEN_MULT
    input [#$NUM_SPARE_COL$#-1:0] spare_wen;
#<SPARE_WEN_MULT
#<RW_PORT
    input clk#$PORT_NUM#$;
    input csb#$PORT_NUM$#;
    input web#$PORT_NUM$#;
    input [ADDR_WIDTH-1:0] addr#$PORT_NUM$#;
    input [DATA_WIDTH-1:0] din#$PORT_NUM$#;
    output [DATA_WIDTH-1:0] dout#$PORT_NUM$#;
#>RW_PORT
#<R_PORT
    input clk#$PORT_NUM#$;
    input csb#$PORT_NUM$#;
    input [ADDR_WIDTH-1:0] addr#$PORT_NUM$#;
    output [DATA_WIDTH-1:0] dout#$PORT_NUM$#;
#>RW_PORT
#<W_PORT
// Port 0: RW
    input clk#$PORT_NUM#$;
    input csb#$PORT_NUM$#;
    input web#$PORT_NUM$#;
    input [ADDR_WIDTH-1:0] addr#$PORT_NUM$#;
    input [DATA_WIDTH-1:0] din#$PORT_NUM$#;
    output [DATA_WIDTH-1:0] dout#$PORT_NUM$#;
    clk#$PORT_NUM#$,csb#$PORT_NUM$#,web$#PORT_NUM$#,addr#PORT_NUM$#,din#PORT_NUM$#,dout#PORT_NUM$#
#>W_PORT

  reg [DATA_WIDTH-1:0]    mem [0:RAM_DEPTH-1];

#<REGS
  reg  csb#$PORT_NUM$#_reg;
  reg  web#$PORT_NUM$#_reg;
  reg [NUM_WMASK-1:0]  wmask#$PORT_NUM$#_reg;
  reg spare_wen#$PORT_NUM$#_reg;
  reg [#$SPARE_COLS$#-1:0]  spare_wen#$PORT_NUM$#_reg;
  reg [ADDR_WIDTH-1:0]  addr#$PORT_NUM$#_reg;
  reg [DATA_WIDTH-1:0]  din#$PORT_NUM$#_reg;
  reg [DATA_WIDTH-1:0]  dout#$PORT_NUM$#;
#<REGS
#<FLOPS
  // All inputs are registers
  always @(posedge clk#$PORT_NUM$#)
  begin
    csb#$PORT_NUM$#_reg = csb#$PORT_NUM$#;
#<WEB_FLOP
    web#$PORT_NUM$#_reg = web#$PORT_NUM$#;
#>WEB_FLOP
#<W_MASK_FLOP
    w_mask#$PORT_NUM$#_reg = w_mask#$PORT_NUM$#;
#>W_MASK_FLOP
#<SPARE_WEN_FLOP
    spare_wen#$PORT_NUM$#_reg = spare_wen#$PORT_NUM$#;
#>SPARE_WEN_FLOP
    addr#$PORT_NUM$#_reg = addr#$PORT_NUM$#;
#<RW_CHECKS
    if (#$WPORT_CONTROL$# && #$RPORT_CONTROL$# && (addr#$WPORT$# == addr#$RPORT$#))
      $display($time," WARNING: Writing and reading addr{0}=%b and addr{1}=%b simultaneously!",addr#$WPORT$#,addr#$RPORT$#);
#>RW_CHECKS
    if ( !csb0_reg && web0_reg && VERBOSE )
      $display($time," Reading %m addr0=%b dout0=%b",addr0_reg,mem[addr0_reg]);
    if ( !csb0_reg && !web0_reg && VERBOSE )
      $display($time," Writing %m addr0=%b din0=%b",addr0_reg,din0_reg);
#>FLOPS
#<DIN_FLOP
    din#$PORT_NUM$#_reg = din#$PORT_NUM$#;
#>DIN_FLOP
#<DOUT_FLOP
    #(T_HOLD) dout#$PORT_NUM$# = #$WORD_SIZE$#'bx;
#>DOUT_FLOP
#<RW_VERBOSE
    if ( !csb#$PORT_NUM$#_reg && web#$PORT_NUM$#_reg && VERBOSE )
      $display($time," Reading %m addr#$PORT_NUM$#=%b dout#$PORT_NUM$#=%b",addr#$PORT_NUM$#_reg,mem[addr#$PORT_NUM$#_reg]);
#>RW_VERBOSE
#<R_VERBOSE
if ( !csb{0}_reg && VERBOSE )
  $display($time," Reading %m addr{0}=%b dout{0}=%b",addr{0}_reg,mem[addr{0}_reg]);
#>R_VERBOSE
#<W_VERBOSE

#>W_VERBOSE
  end
  // Memory Write Block Port 0
  // Write Operation : When web0 = 0, csb0 = 0
  always @ (negedge clk0)
  begin : MEM_WRITE0
    if ( !csb0_reg && !web0_reg ) begin
        mem[addr0_reg][1:0] = din0_reg[1:0];
    end
  end

  // Memory Read Block Port 0
  // Read Operation : When web0 = 1, csb0 = 0
  always @ (negedge clk0)
  begin : MEM_READ0
    if (!csb0_reg && web0_reg)
       dout0 <= #(DELAY) mem[addr0_reg];
  end

e
