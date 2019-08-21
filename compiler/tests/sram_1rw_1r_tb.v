`define assert(signal, value) \
if (!(signal === value)) begin \
   $display("ASSERTION FAILED in %m: signal != value"); \
   $finish;\
end

module sram_1rw_1r_tb;
   reg 	     clk;
   
   // 1rw port
   reg [3:0] addr0;
   reg [1:0] din0;
   reg 	     csb0;
   reg 	     web0;
   wire [1:0] dout0;

   // 1r port
   reg [3:0] addr1;
   reg 	     csb1;
   wire [1:0] dout1;
   
   sram_1rw_1r_2_16_scn4m_subm U0 (.din0(din0),
				   .dout0(dout0),
				   .addr0(addr0),
				   .csb0(csb0), 
				   .web0(web0), 
				   .clk0(clk),
				   .dout1(dout1),
				   .addr1(addr1),
				   .csb1(csb1),
				   .clk1(clk)
				   ); 

   
   initial 
     begin
	
	//$monitor("%g addr0=%b din0=%b dout0=%b addr1=%b dout1=%b",
	//	 $time, addr0, din0, dout0, addr1, dout1);

	clk = 1;
	csb0 = 1;
	web0 = 1;
	addr0 = 0;
	din0 = 0;

	csb1 = 1;
	addr1 = 0;

	// write 
	#10 din0=2'b10;
	addr0=4'h1;
	web0 = 0;
	csb0 = 0;
	// nop
	csb1 = 1;
	addr1 = 0;
	
	// write another
	#10 din0=2'b01;
	addr0=4'hC;
	web0 = 0;
	csb0 = 0;
	// read last
	csb1 = 0;
	addr1 = 4'h1;

	#10 `assert(dout1, 2'b10)
	
	// read undefined	
	din0=2'b11;
	addr0=4'h0;	
	web0 = 1;
	csb0 = 0;
	// read another
	csb1 = 0;
	addr1 = 4'hC;
	
	#10 `assert(dout0, 2'bxx)
	`assert(dout1, 2'b01)	

	// read defined
	din0=2'b11;
	addr0=4'hC;	
	web0 = 1;
	csb0 = 0;
	// read undefined
	csb1 = 0;
	addr1 = 4'hD;

	#10 `assert(dout0, 2'b01)
	`assert(dout1, 2'bxx)	
	
	// write another
	din0=2'b11;
	addr0=4'hA;
	web0 = 0;
	csb0 = 0;
	// read the feedthrough value
	csb1 = 0;
	addr1 = 4'hA;

	#10 `assert(dout1, 2'b11)
	
	// read defined
	din0=2'b11;
	addr0=4'h1;	
	web0 = 1;
	csb0 = 0;
	// read old value
	csb1 = 0;
	addr1 = 4'h1;

	#10 `assert(dout0, 2'b10)
	`assert(dout1, 2'b10)
	
	// read defined
	din0=2'b11;
	addr0=4'hA;	
	web0 = 1;
	csb0 = 0;
	// dual read
	csb1 = 0;
	addr1 = 4'hA;
	#10 `assert(dout0, 2'b11)
	`assert(dout1, 2'b11)	
	
	// read undefined	
	din0=2'b11;
	addr0=4'h0;	
	web0 = 1;
	csb0 = 0;

	#10 `assert(dout0, 2'bxx)
	
	#10 $finish;
	
  end 
    
  always 
    #5 clk = !clk; 
    
endmodule 
