module sram; 
   reg [3:0] addr;
   reg [1:0] data;
   reg 	     clk;
   reg 	     csb;
   reg 	     web;
   reg 	     oeb;

   wire [1:0] data_in = !oeb ? 2'bzz : data;
    
   sram_2_16_1_freepdk45 U0 (.DATA(data_in),
			     .ADDR(addr),
			     .CSb (csb), 
			     .WEb (web), 
			     .OEb (oeb),
			     .clk (clk)
			     ); 

   
   initial 
     begin
	
	$monitor("%g addr=%b data=%b",
		 $time, addr, data_in,);

	
	  

	clk = 0;
	csb = 1;
	web = 1;
	oeb = 1;
	addr = 0;
	data = 0;

	// write 
	#10 data=2'b10;
	addr=4'h1;
	web = 0;
	oeb = 1;
	csb = 0;
	
	// write another
	#10 data=2'b01;
	addr=4'hC;
	web = 0;
	oeb = 1;
	csb = 0;

	// read undefined	
	#10 data=2'b11;
	addr=4'h0;	
	web = 1;
	oeb = 0;
	csb = 0;

	// read defined
	#10 data=2'b11;
	addr=4'hC;	
	web = 1;
	oeb = 0;
	csb = 0;

	// read defined
	#10 data=2'b11;
	addr=4'h1;	
	web = 1;
	oeb = 0;
	csb = 0;
	  
	#30 $finish;
	
  end 
    
  always 
    #5 clk = !clk; 
    
endmodule 
