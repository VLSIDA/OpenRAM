TOP_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST)))../..)
include $(TOP_DIR)/openram.mk

.DEFAULT_GOAL := all

ARGS ?=
TECHS ?= scn4m_subm freepdk45 sky130

TEST_DIR   = $(TOP_DIR)/compiler/tests
TEST_SRCS  = $(sort $(notdir $(wildcard $(TEST_DIR)/*_test.py)))
TEST_BASES = $(basename $(TEST_SRCS))
TEST_STAMPS= $(addsuffix .ok,$(TEST_BASES))

OPENRAM_DIR = $(OPENRAM_HOME)/tests
RESULTS_DIR = $(OPENRAM_DIR)/results



# Use % for all techs:
# %/test.py
# or a specific tech:
# freepdk45/test.py
BROKEN_STAMPS = \
	%/06_hierarchical_decoder_4096row_test.ok \
	%/19_single_bank_16mux_1rw_1r_test.ok \
	%/19_single_bank_16mux_test.ok \
	%/20_sram_1bank_16mux_1rw_1r_test.ok \
	%/20_sram_1bank_16mux_test.ok \
	%/20_psram_1bank_2mux_1rw_1w_test.ok \
	%/20_psram_1bank_2mux_1rw_1w_wmask_test.ok \
	%/20_psram_1bank_2mux_1w_1r_test.ok \
	%/20_psram_1bank_2mux_test.ok \
	%/21_hspice_delay_test.ok \
	%/21_hspice_setuphold_test.ok \
	%/21_xyce_delay_test.ok \
	%/22_psram_1bank_2mux_func_test.ok \
	%/22_psram_1bank_4mux_func_test.ok \
	%/22_psram_1bank_8mux_func_test.ok \
	%/22_psram_1bank_nomux_func_test.ok \
	%/22_sram_1bank_2mux_func_test.ok \
	%/22_sram_1bank_2mux_global_func_test.ok \
	%/22_sram_1bank_2mux_sparecols_func_test.ok \
	%/22_sram_1bank_4mux_func_test.ok \
	%/22_sram_1bank_8mux_func_test.ok \
	%/22_sram_1bank_nomux_1rw_1r_func_test.ok \
	%/22_sram_1bank_nomux_func_test.ok \
	%/22_sram_1bank_nomux_sparecols_func_test.ok \
	%/22_sram_1bank_wmask_1rw_1r_func_test.ok \
	%/22_sram_wmask_func_test.ok \
	%/26_hspice_pex_pinv_test.ok \
	%/27_verilog_multibank_test.ok \
	%/50_riscv_1k_1rw1r_func_test.ok \
	%/50_riscv_1k_1rw_func_test.ok \
	%/50_riscv_1rw1r_func_test.ok \
	%/50_riscv_1rw1r_phys_test.ok \
	%/50_riscv_1rw_func_test.ok \
	%/50_riscv_1rw_phys_test.ok \
	%/50_riscv_2k_1rw1r_func_test.ok \
	%/50_riscv_2k_1rw_func_test.ok \
	%/50_riscv_4k_1rw1r_func_test.ok \
	%/50_riscv_4k_1rw_func_test.ok \
	%/50_riscv_512b_1rw1r_func_test.ok \
	%/50_riscv_512b_1rw_func_test.ok \
	%/50_riscv_8k_1rw1r_func_test.ok \
	%/50_riscv_8k_1rw_func_test.ok \
	freepdk45/06_rom_decoder_test.ok \
	freepdk45/07_rom_column_mux_array_test.ok \
	freepdk45/08_rom_decoder_buffer_array_test.ok \
	freepdk45/08_rom_precharge_array_test.ok \
	freepdk45/10_rom_wordline_driver_array_test.ok \
	freepdk45/14_rom_array_test.ok \
	freepdk45/16_rom_control_logic_test.ok \
	freepdk45/16_control_logic_delay_multiport_test.ok \
	freepdk45/16_control_logic_delay_rw_test.ok \
	freepdk45/16_control_logic_delay_r_test.ok \
	freepdk45/16_control_logic_delay_w_test.ok \
	freepdk45/19_rom_bank_test.ok \
	scn4m_subm/06_rom_decoder_test.ok \
	scn4m_subm/07_rom_column_mux_array_test.ok \
	scn4m_subm/08_rom_decoder_buffer_array_test.ok \
	scn4m_subm/08_rom_precharge_array_test.ok \
	scn4m_subm/10_rom_wordline_driver_array_test.ok \
	scn4m_subm/14_rom_array_test.ok \
	scn4m_subm/16_rom_control_logic_test.ok \
	scn4m_subm/19_rom_bank_test.ok \
	scn4m_subm/19_single_bank_global_bitline_test.ok \
	sky130/01_library_test.ok \
	sky130/03_wire_test.ok \
	sky130/04_column_mux_pbitcell_test.ok \
	sky130/04_dummy_pbitcell_test.ok \
	sky130/04_pbitcell_test.ok \
	sky130/04_pnand4_test.ok \
	sky130/04_pand4_test.ok \
	sky130/04_precharge_pbitcell_test.ok \
	sky130/04_replica_pbitcell_test.ok \
	sky130/04_dummy_pbitcell_1rw1r1w_test.ok \
	sky130/04_dummy_pbitcell_1rw_test.ok \
	sky130/04_replica_pbitcell_1rw1r1w_test.ok \
	sky130/04_replica_pbitcell_1rw_test.ok \
	sky130/05_pbitcell_array_test.ok \
	sky130/05_bitcell_array_test.ok \
	sky130/05_bitcell_array_1rw_1r_test.ok \
	sky130/05_dummy_array_test.ok \
	sky130/06_hierarchical_decoder_132row_test.ok \
	sky130/06_hierarchical_decoder_512row_test.ok \
	sky130/06_hierarchical_decoder_64row_test.ok \
	sky130/06_hierarchical_decoder_pbitcell_test.ok \
	sky130/07_column_mux_array_pbitcell_test.ok \
	sky130/10_write_driver_array_spare_cols_test.ok \
	sky130/10_write_driver_array_wmask_spare_cols_test.ok \
	sky130/14_capped_replica_bitcell_array_dummies_1rw_test.ok \
	sky130/14_capped_replica_bitcell_array_leftrbl_1rw_test.ok \
	sky130/14_capped_replica_bitcell_array_norbl_1rw_1r_test.ok \
	sky130/14_capped_replica_bitcell_array_norbl_1rw_test.ok \
	sky130/14_replica_bitcell_array_dummies_1rw_test.ok \
	sky130/14_replica_bitcell_array_leftrbl_1rw_test.ok \
	sky130/14_replica_bitcell_array_norbl_1rw_1r_test.ok \
	sky130/14_replica_bitcell_array_norbl_1rw_test.ok \
	sky130/14_replica_column_1rw_1r_test.ok \
	sky130/14_replica_column_1rw_test.ok \
	sky130/14_replica_pbitcell_1rw1r_array_test.ok \
	sky130/14_replica_pbitcell_1rw_array_test.ok \
	sky130/15_global_bitcell_array_norbl_1rw_1r_test.ok \
	sky130/15_global_bitcell_array_norbl_1rw_test.ok \
	sky130/15_global_bitcell_array_rbl_1rw_1r_test.ok \
	sky130/15_global_bitcell_array_rbl_1rw_test.ok \
	sky130/15_local_bitcell_array_dummies_1rw_test.ok \
	sky130/15_local_bitcell_array_leftrbl_1rw_test.ok \
	sky130/15_local_bitcell_array_norbl_1rw_1r_test.ok \
	sky130/15_local_bitcell_array_norbl_1rw_test.ok \
	sky130/16_control_logic_delay_multiport_test.ok \
	sky130/16_control_logic_delay_rw_test.ok \
	sky130/16_control_logic_delay_r_test.ok \
	sky130/16_control_logic_delay_w_test.ok \
	sky130/18_port_address_512rows_test.ok \
	sky130/18_port_data_spare_cols_test.ok \
	sky130/19_single_bank_2mux_test.ok \
	sky130/19_single_bank_4mux_test.ok \
	sky130/19_single_bank_8mux_test.ok \
	sky130/19_single_bank_global_bitline_test.ok \
	sky130/19_single_bank_nomux_test.ok \
	sky130/19_single_bank_nomux_norbl_1rw_1r_test.ok \
	sky130/19_single_bank_nomux_norbl_test.ok \
	sky130/19_single_bank_spare_cols_test.ok \
	sky130/19_single_bank_wmask_test.ok \
	sky130/19_pmulti_bank_test.ok \
	sky130/19_psingle_bank_test.ok \
	sky130/19_bank_select_pbitcell_test.ok \
	sky130/20_psram_1bank_4mux_1rw_1r_test.ok \
	sky130/20_sram_1bank_2mux_1rw_1r_spare_cols_test.ok \
	sky130/20_sram_1bank_2mux_1w_1r_spare_cols_test.ok \
	sky130/20_sram_1bank_2mux_global_test.ok \
	sky130/20_sram_1bank_2mux_test.ok \
	sky130/20_sram_1bank_2mux_wmask_spare_cols_test.ok \
	sky130/20_sram_1bank_2mux_wmask_test.ok \
	sky130/20_sram_1bank_4mux_test.ok \
	sky130/20_sram_1bank_8mux_test.ok \
	sky130/20_sram_1bank_nomux_norbl_1rw_1r_test.ok \
	sky130/20_sram_1bank_nomux_norbl_test.ok \
	sky130/20_sram_1bank_nomux_spare_cols_test.ok \
	sky130/20_sram_1bank_nomux_test.ok \
	sky130/20_sram_1bank_nomux_wmask_test.ok \
	sky130/20_sram_1bank_ring_test.ok \
	sky130/21_model_delay_test.ok \
	sky130/21_ngspice_delay_extra_rows_test.ok \
	sky130/21_ngspice_delay_test.ok \
	sky130/21_regression_delay_test.ok \
	sky130/22_psram_1bank_2mux_func_test.ok \
	sky130/22_psram_1bank_4mux_func_test.ok \
	sky130/22_psram_1bank_8mux_func_test.ok \
	sky130/22_psram_1bank_nomux_func_test.ok \
	sky130/23_lib_sram_linear_regression_test.ok \
	sky130/23_lib_sram_model_corners_test.ok \
	sky130/23_lib_sram_model_test.ok \
	sky130/23_lib_sram_prune_test.ok \
	sky130/23_lib_sram_test.ok \
	sky130/25_verilog_multibank_test.ok \
	sky130/25_verilog_sram_test.ok \
	sky130/30_openram_back_end_library_test.ok \
	sky130/30_openram_back_end_test.ok \
	sky130/30_openram_front_end_library_test.ok \
	sky130/30_openram_front_end_test.ok \
	sky130/30_openram_sram_char_test.ok \
	sky130/30_openram_sram_func_test.ok \

gettech = $(word 1,$(subst /, ,$*))
getfile = $(word 2,$(subst /, ,$*))
TECH_TEST_STAMPS=$(foreach T, $(TECHS), $(addprefix $T/, $(TEST_STAMPS)))

# Filter out the tests after creating the tech stamps
WORKING_TECH_TEST_STAMPS=$(shell shuf -e -- $(filter-out $(BROKEN_STAMPS), $(TECH_TEST_STAMPS)))


# Run all technologies
all: clean $(WORKING_TECH_TEST_STAMPS)
	@ls -1 $(TOP_DIR)/compiler/tests/results/*/*.bad 1> /dev/null 2>&1 && echo "FAILING TESTS" && ls -1 $(TOP_DIR)/compiler/tests/results/*/*.bad | sed -e "s#^.*results\/##" && exit 1 || exit 0
.PHONY: all

# Run a given technology
# e.g. make freepdk45
$(TECHS):
	@$(MAKE) --no-print-directory $(filter-out $(BROKEN_STAMPS), $(addprefix $@/, $(TEST_STAMPS)))
.PHONY: $(TECHS)

# Targets for each individual test in all technologies
# e.g. make 04_pinv_1x_test
$(TEST_BASES):
	@$(MAKE) --no-print-directory $(foreach T, $(TECHS), $(addprefix $T/, $@.ok))
.PHONY: $(TEST_BASES)

# To run a test in a given technology
%.ok:
#	@echo "Running $(gettech) $(getfile) ... "
	@rm -rf results/$*
	@rm -rf results/$*.*
	@mkdir -p results/$*/tmp
	@sh -c "python3 -u $(OPENRAM_DIR)/$(getfile).py -t $(gettech) -k -v $(ARGS) -p $(OPENRAM_DIR)/results/$* > $(OPENRAM_DIR)/results/$*.out 2>&1 && touch $(OPENRAM_DIR)/results/$*.ok || touch $(OPENRAM_DIR)/results/$*.bad"
ifdef KEEP
	@test -f $(TOP_DIR)/compiler/tests/results/$*.ok && echo "$* ... PASS!" || echo "$* ... FAIL!"
else
	@test -f $(TOP_DIR)/compiler/tests/results/$*.ok && echo "$* ... PASS!" && rm -rf $(TOP_DIR)/compiler/tests/results/$* || echo "$* ... FAIL!"
endif
.DELETE_ON_ERROR: $(TEST_STAMPS)

clean:
	@rm -rf $(TOP_DIR)/compiler/tests/results
.PHONY: clean
