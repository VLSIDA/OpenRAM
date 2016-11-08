
for i in addr_ff clock_nor dinv inv_clk inv_nor nor_1 out_inv_16 output_latch sense_amp addr_latch  cell_10t dinv_mx inv_col mux_a nor_1_mx out_inv_2 precharge tgate cell_6t inv inv_dec mux_abar out_inv_4  write_driver
do
	echo $i
  	strmout -layerMap ../sram_lib/layers.map -library sram -topCell $i -view layout -strmFile ../sram_lib/$i.gds
done


