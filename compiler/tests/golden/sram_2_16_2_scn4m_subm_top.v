
module sram_2_16_2_scn4m_subm_top  (
`ifdef USE_POWER_PINS
    vdd,
    gnd,
`endif
    clk0,
    addr0,
    din0,
    csb0,
    web0,
    dout0
  );

  parameter DATA_WIDTH = 2;
  parameter ADDR_WIDTH= 4;

  parameter BANK_SEL = 1;
  parameter NUM_WMASK = 0;

`ifdef USE_POWER_PINS
  inout vdd;
  inout gnd;
`endif
  input clk0;
  input [ADDR_WIDTH - 1 : 0] addr0;
  input [DATA_WIDTH - 1: 0] din0;
  input csb0;
  input web0;
  output reg [DATA_WIDTH - 1 : 0] dout0;

  reg [BANK_SEL - 1 : 0] addr0_reg;

  wire [DATA_WIDTH - 1 : 0] dout0_bank0;

  reg web0_bank0;

  reg csb0_bank0;

  wire [DATA_WIDTH - 1 : 0] dout0_bank1;

  reg web0_bank1;

  reg csb0_bank1;


  sram_2_16_2_scn4m_subm bank0 (
`ifdef USE_POWER_PINS
    .vdd(vdd),
    .gnd(gnd),
`endif
    .clk0(clk0),
    .addr0(addr0[ADDR_WIDTH - BANK_SEL - 1 : 0]),
    .din0(din0),
    .csb0(csb0_bank0),
    .web0(web0_bank0),
    .dout0(dout0_bank0)
  );
  sram_2_16_2_scn4m_subm bank1 (
`ifdef USE_POWER_PINS
    .vdd(vdd),
    .gnd(gnd),
`endif
    .clk0(clk0),
    .addr0(addr0[ADDR_WIDTH - BANK_SEL - 1 : 0]),
    .din0(din0),
    .csb0(csb0_bank1),
    .web0(web0_bank1),
    .dout0(dout0_bank1)
  );

  always @(posedge clk0) begin
    addr0_reg <= addr0[ADDR_WIDTH - 1 : ADDR_WIDTH - BANK_SEL];
  end

  always @(*) begin
    case (addr0_reg)
      0: begin
        dout0 = dout0_bank0;
      end
      1: begin
        dout0 = dout0_bank1;
      end
    endcase
  end

  always @(*) begin
    csb0_bank0 = 1'b1;
    web0_bank0 = 1'b1;
    csb0_bank1 = 1'b1;
    web0_bank1 = 1'b1;
    case (addr0[ADDR_WIDTH - 1 : ADDR_WIDTH - BANK_SEL])
      0: begin
        web0_bank0 = web0;
        csb0_bank0 = csb0;
      end
      1: begin
        web0_bank1 = web0;
        csb0_bank1 = csb0;
      end
    endcase
  end


endmodule
