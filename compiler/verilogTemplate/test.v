
module multibank # (
  DATA_WIDTH = 32,
  ADDR_WIDTH= 8,
  NUM_BANKS=2
)(
    clk,
    addr,
    din,
    csb,
    web,
    dout
  );

  parameter RAM_DEPTH = 1 << ADDR_WIDTH;
  parameter BANK_SEL = (NUM_BANKS <= 2)? 1 :
                       (NUM_BANKS <= 4)? 2 :
                       (NUM_BANKS <= 8)? 3 :
                       (NUM_BANKS <= 16)? 4 : 5;

  input clk;
  input [ADDR_WIDTH -1 : 0] addr;
  input [DATA_WIDTH - 1: 0] din;
  input csb;
  input web;
  output reg [DATA_WIDTH - 1 : 0] dout;

  reg csb0;
  reg web0;
  reg [DATA_WIDTH - 1 : 0] dout0;
  reg csb1;
  reg web1;
  reg [DATA_WIDTH - 1 : 0] dout1;

  bank #(DATA_WIDTH, ADDR_WIDTH) bank0 (
    .clk(clk),
    .addr(addr[ADDR_WIDTH - BANK_SEL - 1 : 0]),
    .din(din),
    .csb(csb0),
    .web(web0),
    .dout(dout0)
  );
  bank #(DATA_WIDTH, ADDR_WIDTH) bank1 (
    .clk(clk),
    .addr(addr[ADDR_WIDTH - BANK_SEL - 1 : 0]),
    .din(din),
    .csb(csb1),
    .web(web1),
    .dout(dout1)
  );

always @(posedge clk) begin
    case (addr[ADDR_WIDTH - 1 : ADDR_WIDTH - BANK_SEL])
        0: begin
            dout <= dout0;
            web0 <= web;
        end
        1: begin
            dout <= dout1;
            web1 <= web;
        end
    endcase
end

endmodule
