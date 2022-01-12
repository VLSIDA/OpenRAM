
module multibank # (
  DATA_WIDTH = 32,
  ADDR_WIDTH= 8
)(
#<RW_PORTS
    clk#$PORT_NUM$#,
    addr#$PORT_NUM$#,
    din#$PORT_NUM$#,
    csb#$PORT_NUM$#,
    web#$PORT_NUM$#,
    dout#$PORT_NUM$#,
#>RW_PORTS
#<R_PORTS
    clk#$PORT_NUM$#,
    addr#$PORT_NUM$#,
    csb#$PORT_NUM$#,
    web#$PORT_NUM$#,
    dout#$PORT_NUM$#,
#>R_PORTS
  );

  parameter RAM_DEPTH = 1 << ADRR_WIDTH;
  
#<BANK_INIT
  bank bank#$BANK_NUM$# #(DATA_WIDTH, ADDR_WIDTH) (
#<BANK_RW_PORTS
    clk#$PORT_NUM$#,
    addr#$PORT_NUM$#,
    din#$PORT_NUM$#,
    csb#$PORT_NUM$#,
    web#$PORT_NUM$#,
    dout#$PORT_NUM$#,
#>BANK_R_PORTS
  )
#>BANK_INIT
