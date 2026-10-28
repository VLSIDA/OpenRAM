SHELL := /bin/bash
TOP_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST)))../..)
include $(TOP_DIR)/openram.mk

.DEFAULT_GOAL := all

ARGS ?=
TECHS ?= scn4m_subm freepdk45 sky130 ihp_sg13g2

TEST_DIR   = $(TOP_DIR)/compiler/tests
TEST_SRCS  = $(sort $(notdir $(wildcard $(TEST_DIR)/*_test.py)))
TEST_BASES = $(basename $(TEST_SRCS))
TEST_STAMPS= $(addsuffix .ok,$(TEST_BASES))

OPENRAM_DIR = $(OPENRAM_HOME)/tests
RESULTS_DIR = $(OPENRAM_DIR)/results

# Technology-local checks use the common result handling below.
TEST_COMMAND = python3 -u $(OPENRAM_DIR)/$(getfile).py -t $(gettech) -k $(if $(TECH_FILE),-f $(TECH_FILE)) -v $(ARGS) -p $(RESULTS_DIR)/$*
ihp_sg13g2/foundry.ok: TEST_COMMAND = python3 -u $(OPENRAM_TECH)/ihp_sg13g2/tests/test_bitcell.py -v
ihp_sg13g2/sram_physical.ok: TEST_COMMAND = python3 -u $(OPENRAM_TECH)/ihp_sg13g2/tests/verify_array.py --sram --cols 8 --output $(RESULTS_DIR)/$*

# Reuse a selected IHP environment locally; otherwise provide its PSP models
# and installed decks here, not in CI YAML. Mount the checkout at the same
# absolute path so the common commands and result paths need no translation.
IHP_DOCKER_IMAGE ?= hpretl/iic-osic-tools:2026.10
ifneq ($(PDK),ihp-sg13g2)
ihp_sg13g2/%.ok: TEST_ENV = docker run --rm --entrypoint /bin/bash \
	-v "$(TOP_DIR):$(TOP_DIR)" -w "$(CURDIR)" \
	-e OPENRAM_HOME -e OPENRAM_TECH $(IHP_DOCKER_IMAGE) \
	-ic 'set -e; iic-pdk ihp-sg13g2; python3 -m pip install --no-deps "$(TOP_DIR)"/dist/openram*.whl; exec "$$@"' --
endif

# Use % for all techs:
# %/test.py
# or a specific tech:
# freepdk45/test.py
BROKEN_STAMPS = \
	%/19_single_bank_16mux_1rw_1r_test.ok \
	%/19_single_bank_16mux_test.ok \
	%/20_sram_1bank_16mux_1rw_1r_test.ok \
	%/21_xyce_delay_test.ok \
	%/27_verilog_multibank_test.ok \
	freepdk45/04_rom_address_control_buf_test.ok \
	freepdk45/05_rom_array_test.ok \
	freepdk45/06_rom_decoder_test.ok \
	freepdk45/06_hierarchical_decoder_4096row_test.ok \
	freepdk45/07_rom_column_mux_array_test.ok \
	freepdk45/08_rom_decoder_buffer_array_test.ok \
	freepdk45/08_rom_precharge_array_test.ok \
	freepdk45/16_rom_control_logic_test.ok \
	freepdk45/19_rom_bank_test.ok \
	scn4m_subm/04_rom_address_control_buf_test.ok \
	scn4m_subm/06_rom_decoder_test.ok \
	scn4m_subm/06_hierarchical_decoder_4096row_test.ok \
	scn4m_subm/08_rom_decoder_buffer_array_test.ok \
	scn4m_subm/14_rom_array_test.ok \
	scn4m_subm/19_rom_bank_test.ok \
	scn4m_subm/19_single_bank_global_bitline_test.ok \
	scn4m_subm/50_riscv_1rw_phys_test.ok \
	scn4m_subm/50_riscv_1rw1r_phys_test.ok \
	sky130/01_library_test.ok \
	sky130/03_wire_test.ok \
	sky130/04_column_mux_pbitcell_test.ok \
	sky130/04_dummy_pbitcell_test.ok \
	sky130/04_pbitcell_test.ok \
	sky130/04_precharge_pbitcell_test.ok \
	sky130/04_replica_pbitcell_test.ok \
	sky130/04_dummy_pbitcell_1rw1r1w_test.ok \
	sky130/04_dummy_pbitcell_1rw_test.ok \
	sky130/04_replica_pbitcell_1rw1r1w_test.ok \
	sky130/04_replica_pbitcell_1rw_test.ok \
	sky130/05_pbitcell_array_test.ok \
	sky130/05_bitcell_array_1rw_1r_test.ok \
	sky130/05_dummy_array_test.ok \
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
	sky130/19_psingle_bank_test.ok \
	sky130/19_bank_select_pbitcell_test.ok \
	sky130/20_psram_1bank_2mux_1rw_1w_test.ok \
	sky130/20_psram_1bank_2mux_1rw_1w_wmask_test.ok \
	sky130/20_psram_1bank_2mux_1w_1r_test.ok \
	sky130/20_psram_1bank_2mux_test.ok \
	sky130/20_sram_1bank_16mux_test.ok \
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
	sky130/22_sram_1bank_2mux_global_func_test.ok \
	sky130/22_sram_1bank_wmask_1rw_1r_func_test.ok \
	sky130/22_sram_wmask_func_test.ok \
	sky130/23_lib_sram_linear_regression_test.ok \
	sky130/23_lib_sram_model_corners_test.ok \
	sky130/23_lib_sram_model_test.ok \
	sky130/23_lib_sram_test.ok \
	sky130/25_verilog_multibank_test.ok \
	sky130/25_verilog_sram_test.ok \
	sky130/30_openram_back_end_library_test.ok \
	sky130/30_openram_back_end_test.ok \
	sky130/30_openram_front_end_library_test.ok \
	sky130/30_openram_front_end_test.ok \
	sky130/30_openram_sram_char_test.ok \
	sky130/50_riscv_1rw_phys_test.ok \
	sky130/50_riscv_1rw1r_phys_test.ok \

# These generic cells/banks remain unqualified for IHP geometry, connectivity,
# or module contracts. Shared local_check/local_drc_check reuse the installed-PDK checker
# for IHP; passing basic gates and routing tests are enabled normally.
# Keep explicit filenames so newly added shared tests are included by default.
BROKEN_STAMPS += \
	ihp_sg13g2/01_library_test.ok \
	ihp_sg13g2/03_contact_test.ok \
	ihp_sg13g2/03_ptx_1finger_nmos_test.ok \
	ihp_sg13g2/03_ptx_1finger_pmos_test.ok \
	ihp_sg13g2/03_ptx_3finger_nmos_test.ok \
	ihp_sg13g2/03_ptx_3finger_pmos_test.ok \
	ihp_sg13g2/03_ptx_4finger_nmos_test.ok \
	ihp_sg13g2/03_ptx_4finger_pmos_test.ok \
	ihp_sg13g2/03_ptx_no_contacts_test.ok \
	ihp_sg13g2/04_and2_dec_test.ok \
	ihp_sg13g2/04_column_mux_1rw_1r_test.ok \
	ihp_sg13g2/04_column_mux_pbitcell_test.ok \
	ihp_sg13g2/04_column_mux_test.ok \
	ihp_sg13g2/04_dff_buf_test.ok \
	ihp_sg13g2/04_dummy_pbitcell_1rw1r1w_test.ok \
	ihp_sg13g2/04_dummy_pbitcell_1rw_test.ok \
	ihp_sg13g2/04_pbitcell_test.ok \
	ihp_sg13g2/04_pbuf_dec_8x_test.ok \
	ihp_sg13g2/04_pinv_dec_1x_test.ok \
	ihp_sg13g2/04_pinvbuf_test.ok \
	ihp_sg13g2/04_pnand2_test.ok \
	ihp_sg13g2/04_precharge_1rw_1r_test.ok \
	ihp_sg13g2/04_precharge_pbitcell_test.ok \
	ihp_sg13g2/04_precharge_test.ok \
	ihp_sg13g2/04_replica_pbitcell_1rw1r1w_test.ok \
	ihp_sg13g2/04_replica_pbitcell_1rw_test.ok \
	ihp_sg13g2/04_rom_address_control_buf_test.ok \
	ihp_sg13g2/04_rom_precharge_test.ok \
	ihp_sg13g2/04_wordline_driver_test.ok \
	ihp_sg13g2/05_bitcell_array_1rw_1r_test.ok \
	ihp_sg13g2/05_bitcell_array_test.ok \
	ihp_sg13g2/05_dummy_array_test.ok \
	ihp_sg13g2/05_pbitcell_array_test.ok \
	ihp_sg13g2/05_rom_array_test.ok \
	ihp_sg13g2/06_column_decoder_16row_test.ok \
	ihp_sg13g2/06_hierarchical_decoder_132row_1rw_1r_test.ok \
	ihp_sg13g2/06_hierarchical_decoder_132row_test.ok \
	ihp_sg13g2/06_hierarchical_decoder_16row_1rw_1r_test.ok \
	ihp_sg13g2/06_hierarchical_decoder_16row_test.ok \
	ihp_sg13g2/06_hierarchical_decoder_17row_1rw_1r_test.ok \
	ihp_sg13g2/06_hierarchical_decoder_17row_test.ok \
	ihp_sg13g2/06_hierarchical_decoder_32row_1rw_1r_test.ok \
	ihp_sg13g2/06_hierarchical_decoder_32row_test.ok \
	ihp_sg13g2/06_hierarchical_decoder_4096row_1rw_1r_test.ok \
	ihp_sg13g2/06_hierarchical_decoder_4096row_test.ok \
	ihp_sg13g2/06_hierarchical_decoder_512row_1rw_1r_test.ok \
	ihp_sg13g2/06_hierarchical_decoder_512row_test.ok \
	ihp_sg13g2/06_hierarchical_decoder_64row_1rw_1r_test.ok \
	ihp_sg13g2/06_hierarchical_decoder_64row_test.ok \
	ihp_sg13g2/06_hierarchical_decoder_pbitcell_test.ok \
	ihp_sg13g2/06_hierarchical_predecode2x4_1rw_1r_test.ok \
	ihp_sg13g2/06_hierarchical_predecode2x4_pbitcell_test.ok \
	ihp_sg13g2/06_hierarchical_predecode2x4_test.ok \
	ihp_sg13g2/06_hierarchical_predecode3x8_1rw_1r_test.ok \
	ihp_sg13g2/06_hierarchical_predecode3x8_pbitcell_test.ok \
	ihp_sg13g2/06_hierarchical_predecode3x8_test.ok \
	ihp_sg13g2/06_hierarchical_predecode4x16_test.ok \
	ihp_sg13g2/06_rom_decoder_test.ok \
	ihp_sg13g2/07_column_mux_array_16mux_1rw_1r_test.ok \
	ihp_sg13g2/07_column_mux_array_16mux_test.ok \
	ihp_sg13g2/07_column_mux_array_2mux_1rw_1r_test.ok \
	ihp_sg13g2/07_column_mux_array_2mux_test.ok \
	ihp_sg13g2/07_column_mux_array_4mux_1rw_1r_test.ok \
	ihp_sg13g2/07_column_mux_array_4mux_test.ok \
	ihp_sg13g2/07_column_mux_array_8mux_1rw_1r_test.ok \
	ihp_sg13g2/07_column_mux_array_8mux_test.ok \
	ihp_sg13g2/07_column_mux_array_pbitcell_test.ok \
	ihp_sg13g2/07_rom_column_mux_array_test.ok \
	ihp_sg13g2/08_precharge_array_1rw_1r_test.ok \
	ihp_sg13g2/08_precharge_array_test.ok \
	ihp_sg13g2/08_rom_decoder_buffer_array_test.ok \
	ihp_sg13g2/08_rom_precharge_array_test.ok \
	ihp_sg13g2/08_wordline_buffer_array_test.ok \
	ihp_sg13g2/08_wordline_driver_array_1rw_1r_test.ok \
	ihp_sg13g2/08_wordline_driver_array_pbitcell_test.ok \
	ihp_sg13g2/08_wordline_driver_array_test.ok \
	ihp_sg13g2/09_sense_amp_array_1rw_1r_test.ok \
	ihp_sg13g2/09_sense_amp_array_pbitcell_test.ok \
	ihp_sg13g2/09_sense_amp_array_spare_cols_test.ok \
	ihp_sg13g2/09_sense_amp_array_test.ok \
	ihp_sg13g2/10_rom_wordline_driver_array_test.ok \
	ihp_sg13g2/10_write_driver_array_1rw_1r_test.ok \
	ihp_sg13g2/10_write_driver_array_pbitcell_test.ok \
	ihp_sg13g2/10_write_driver_array_spare_cols_test.ok \
	ihp_sg13g2/10_write_driver_array_test.ok \
	ihp_sg13g2/10_write_driver_array_wmask_pbitcell_test.ok \
	ihp_sg13g2/10_write_driver_array_wmask_spare_cols_test.ok \
	ihp_sg13g2/10_write_driver_array_wmask_test.ok \
	ihp_sg13g2/10_write_mask_and_array_1rw_1r_test.ok \
	ihp_sg13g2/10_write_mask_and_array_pbitcell_test.ok \
	ihp_sg13g2/10_write_mask_and_array_test.ok \
	ihp_sg13g2/11_dff_array_test.ok \
	ihp_sg13g2/11_dff_buf_array_test.ok \
	ihp_sg13g2/13_delay_chain_test.ok \
	ihp_sg13g2/14_capped_replica_bitcell_array_bothrbl_1rw_1r_test.ok \
	ihp_sg13g2/14_capped_replica_bitcell_array_dummies_1rw_1r_test.ok \
	ihp_sg13g2/14_capped_replica_bitcell_array_dummies_1rw_test.ok \
	ihp_sg13g2/14_capped_replica_bitcell_array_leftrbl_1rw_1r_test.ok \
	ihp_sg13g2/14_capped_replica_bitcell_array_leftrbl_1rw_test.ok \
	ihp_sg13g2/14_capped_replica_bitcell_array_norbl_1rw_1r_test.ok \
	ihp_sg13g2/14_capped_replica_bitcell_array_norbl_1rw_test.ok \
	ihp_sg13g2/14_capped_replica_bitcell_array_rightrbl_1rw_1r_test.ok \
	ihp_sg13g2/14_replica_bitcell_array_bothrbl_1rw_1r_test.ok \
	ihp_sg13g2/14_replica_bitcell_array_dummies_1rw_1r_test.ok \
	ihp_sg13g2/14_replica_bitcell_array_dummies_1rw_test.ok \
	ihp_sg13g2/14_replica_bitcell_array_leftrbl_1rw_1r_test.ok \
	ihp_sg13g2/14_replica_bitcell_array_leftrbl_1rw_test.ok \
	ihp_sg13g2/14_replica_bitcell_array_norbl_1rw_1r_test.ok \
	ihp_sg13g2/14_replica_bitcell_array_norbl_1rw_test.ok \
	ihp_sg13g2/14_replica_bitcell_array_rightrbl_1rw_1r_test.ok \
	ihp_sg13g2/14_replica_column_1rw_1r_test.ok \
	ihp_sg13g2/14_replica_column_1rw_test.ok \
	ihp_sg13g2/14_replica_pbitcell_1rw1r_array_test.ok \
	ihp_sg13g2/14_replica_pbitcell_1rw_array_test.ok \
	ihp_sg13g2/15_global_bitcell_array_norbl_1rw_1r_test.ok \
	ihp_sg13g2/15_global_bitcell_array_norbl_1rw_test.ok \
	ihp_sg13g2/15_global_bitcell_array_rbl_1rw_1r_test.ok \
	ihp_sg13g2/15_global_bitcell_array_rbl_1rw_test.ok \
	ihp_sg13g2/15_local_bitcell_array_bothrbl_1rw_1r_test.ok \
	ihp_sg13g2/15_local_bitcell_array_dummies_1rw_1r_test.ok \
	ihp_sg13g2/15_local_bitcell_array_dummies_1rw_test.ok \
	ihp_sg13g2/15_local_bitcell_array_leftrbl_1rw_1r_test.ok \
	ihp_sg13g2/15_local_bitcell_array_leftrbl_1rw_test.ok \
	ihp_sg13g2/15_local_bitcell_array_norbl_1rw_1r_test.ok \
	ihp_sg13g2/15_local_bitcell_array_norbl_1rw_test.ok \
	ihp_sg13g2/15_local_bitcell_array_rightrbl_1rw_1r_test.ok \
	ihp_sg13g2/16_control_logic_delay_multiport_test.ok \
	ihp_sg13g2/16_control_logic_delay_r_test.ok \
	ihp_sg13g2/16_control_logic_delay_rw_test.ok \
	ihp_sg13g2/16_control_logic_delay_w_test.ok \
	ihp_sg13g2/16_control_logic_multiport_test.ok \
	ihp_sg13g2/16_control_logic_r_test.ok \
	ihp_sg13g2/16_control_logic_rw_test.ok \
	ihp_sg13g2/16_control_logic_w_test.ok \
	ihp_sg13g2/16_rom_control_logic_test.ok \
	ihp_sg13g2/18_port_address_16rows_1rw_1r_test.ok \
	ihp_sg13g2/18_port_address_16rows_test.ok \
	ihp_sg13g2/18_port_address_256rows_1rw_1r_test.ok \
	ihp_sg13g2/18_port_address_512rows_test.ok \
	ihp_sg13g2/18_port_data_16mux_1rw_1r_test.ok \
	ihp_sg13g2/18_port_data_16mux_test.ok \
	ihp_sg13g2/18_port_data_2mux_1rw_1r_test.ok \
	ihp_sg13g2/18_port_data_2mux_test.ok \
	ihp_sg13g2/18_port_data_4mux_1rw_1r_test.ok \
	ihp_sg13g2/18_port_data_4mux_test.ok \
	ihp_sg13g2/18_port_data_8mux_1rw_1r_test.ok \
	ihp_sg13g2/18_port_data_8mux_test.ok \
	ihp_sg13g2/18_port_data_nomux_1rw_1r_test.ok \
	ihp_sg13g2/18_port_data_nomux_test.ok \
	ihp_sg13g2/18_port_data_spare_cols_test.ok \
	ihp_sg13g2/18_port_data_wmask_1rw_1r_test.ok \
	ihp_sg13g2/18_port_data_wmask_test.ok \
	ihp_sg13g2/19_psingle_bank_test.ok \
	ihp_sg13g2/19_rom_bank_test.ok \
	ihp_sg13g2/19_single_bank_1w_1r_test.ok \
	ihp_sg13g2/19_single_bank_2mux_1rw_1r_test.ok \
	ihp_sg13g2/19_single_bank_2mux_test.ok \
	ihp_sg13g2/19_single_bank_4mux_1rw_1r_test.ok \
	ihp_sg13g2/19_single_bank_4mux_test.ok \
	ihp_sg13g2/19_single_bank_8mux_1rw_1r_test.ok \
	ihp_sg13g2/19_single_bank_8mux_test.ok \
	ihp_sg13g2/19_single_bank_global_bitline_test.ok \
	ihp_sg13g2/19_single_bank_nomux_1rw_1r_test.ok \
	ihp_sg13g2/19_single_bank_nomux_norbl_1rw_1r_test.ok \
	ihp_sg13g2/19_single_bank_nomux_norbl_test.ok \
	ihp_sg13g2/19_single_bank_nomux_test.ok \
	ihp_sg13g2/19_single_bank_spare_cols_test.ok \
	ihp_sg13g2/19_single_bank_wmask_1rw_1r_test.ok \
	ihp_sg13g2/19_single_bank_wmask_test.ok \
	ihp_sg13g2/20_psram_1bank_2mux_1rw_1w_test.ok \
	ihp_sg13g2/20_psram_1bank_2mux_1rw_1w_wmask_test.ok \
	ihp_sg13g2/20_psram_1bank_2mux_1w_1r_test.ok \
	ihp_sg13g2/20_psram_1bank_2mux_test.ok \
	ihp_sg13g2/20_psram_1bank_4mux_1rw_1r_test.ok \
	ihp_sg13g2/20_sram_1bank_16mux_test.ok \
	ihp_sg13g2/20_sram_1bank_2mux_1rw_1r_spare_cols_test.ok \
	ihp_sg13g2/20_sram_1bank_2mux_1rw_1r_test.ok \
	ihp_sg13g2/20_sram_1bank_2mux_1w_1r_spare_cols_test.ok \
	ihp_sg13g2/20_sram_1bank_2mux_1w_1r_test.ok \
	ihp_sg13g2/20_sram_1bank_2mux_global_test.ok \
	ihp_sg13g2/20_sram_1bank_2mux_test.ok \
	ihp_sg13g2/20_sram_1bank_2mux_wmask_spare_cols_test.ok \
	ihp_sg13g2/20_sram_1bank_2mux_wmask_test.ok \
	ihp_sg13g2/20_sram_1bank_4mux_1rw_1r_test.ok \
	ihp_sg13g2/20_sram_1bank_4mux_test.ok \
	ihp_sg13g2/20_sram_1bank_8mux_1rw_1r_test.ok \
	ihp_sg13g2/20_sram_1bank_8mux_test.ok \
	ihp_sg13g2/20_sram_1bank_nomux_1rw_1r_spare_cols_test.ok \
	ihp_sg13g2/20_sram_1bank_nomux_1rw_1r_test.ok \
	ihp_sg13g2/20_sram_1bank_nomux_norbl_1rw_1r_test.ok \
	ihp_sg13g2/20_sram_1bank_nomux_norbl_test.ok \
	ihp_sg13g2/20_sram_1bank_nomux_spare_cols_test.ok \
	ihp_sg13g2/20_sram_1bank_nomux_test.ok \
	ihp_sg13g2/20_sram_1bank_nomux_wmask_test.ok \
	ihp_sg13g2/20_sram_1bank_ring_test.ok \
	ihp_sg13g2/50_riscv_1rw1r_phys_test.ok \
	ihp_sg13g2/50_riscv_1rw_phys_test.ok

# These tests hard-code unsupported organizations (16/32/128+ words, mux1/2/8,
# multiport or spares), analytical models, or 16-word frontend/SPICE fixtures.
BROKEN_STAMPS += \
	ihp_sg13g2/21_model_delay_test.ok \
	ihp_sg13g2/21_ngspice_delay_extra_rows_test.ok \
	ihp_sg13g2/21_ngspice_delay_test.ok \
	ihp_sg13g2/21_regression_delay_test.ok \
	ihp_sg13g2/22_psram_1bank_2mux_func_test.ok \
	ihp_sg13g2/22_psram_1bank_4mux_func_test.ok \
	ihp_sg13g2/22_psram_1bank_8mux_func_test.ok \
	ihp_sg13g2/22_psram_1bank_nomux_func_test.ok \
	ihp_sg13g2/22_sram_1bank_2mux_func_test.ok \
	ihp_sg13g2/22_sram_1bank_2mux_global_func_test.ok \
	ihp_sg13g2/22_sram_1bank_8mux_func_test.ok \
	ihp_sg13g2/22_sram_1bank_nomux_1rw_1r_func_test.ok \
	ihp_sg13g2/22_sram_1bank_nomux_func_test.ok \
	ihp_sg13g2/22_sram_1bank_wmask_1rw_1r_func_test.ok \
	ihp_sg13g2/23_lib_sram_linear_regression_test.ok \
	ihp_sg13g2/23_lib_sram_model_corners_test.ok \
	ihp_sg13g2/23_lib_sram_model_test.ok \
	ihp_sg13g2/23_lib_sram_nonpow2_test.ok \
	ihp_sg13g2/23_lib_sram_test.ok \
	ihp_sg13g2/25_verilog_multibank_test.ok \
	ihp_sg13g2/25_verilog_sram_test.ok \
	ihp_sg13g2/30_openram_back_end_library_test.ok \
	ihp_sg13g2/30_openram_back_end_test.ok \
	ihp_sg13g2/30_openram_front_end_library_test.ok \
	ihp_sg13g2/30_openram_front_end_test.ok \
	ihp_sg13g2/30_openram_sram_char_test.ok \
	ihp_sg13g2/30_openram_sram_func_test.ok

# Setup/hold tests explicitly fail unknown technologies: no IHP golden data.
BROKEN_STAMPS += \
	ihp_sg13g2/21_ngspice_setuphold_test.ok \
	ihp_sg13g2/21_xyce_setuphold_test.ok

gettech = $(word 1,$(subst /, ,$*))
getfile = $(word 2,$(subst /, ,$*))
TECH_TEST_STAMPS=$(foreach T, $(TECHS), $(addprefix $T/, $(TEST_STAMPS)))
ifneq ($(filter ihp_sg13g2,$(TECHS)),)
TECH_TEST_STAMPS += ihp_sg13g2/foundry.ok ihp_sg13g2/sram_physical.ok
endif

# Filter out the broken tests after creating the tech stamps
WORKING_TECH_TEST_STAMPS=$(shell shuf -e -- $(filter-out $(BROKEN_STAMPS), $(TECH_TEST_STAMPS)))
# Filter out the working tests after creating the tech stamps
BROKEN_TECH_TEST_STAMPS=$(shell shuf -e -- $(filter $(BROKEN_STAMPS), $(TECH_TEST_STAMPS)))

# Run all technologies
all: clean $(WORKING_TECH_TEST_STAMPS)
	@ls -1 $(TOP_DIR)/compiler/tests/results/*/*.bad 1> /dev/null 2>&1 && echo "FAILING TESTS" && ls -1 $(TOP_DIR)/compiler/tests/results/*/*.bad | sed -e "s#^.*results\/##" && exit 1 || exit 0
.PHONY: all

# Run broken stamps only
broken: clean $(BROKEN_TECH_TEST_STAMPS)
	@ls -1 $(TOP_DIR)/compiler/tests/results/*/*.bad 1> /dev/null 2>&1 && echo "FAILING TESTS" && ls -1 $(TOP_DIR)/compiler/tests/results/*/*.bad | sed -e "s#^.*results\/##" && exit 1 || exit 0
.PHONY: broken

# Run a given technology
# e.g. make freepdk45
$(TECHS):
	@$(MAKE) --no-print-directory $(filter $@/%,$(WORKING_TECH_TEST_STAMPS))
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
	@$(TEST_ENV) $(TEST_COMMAND) > $(RESULTS_DIR)/$*.out 2>&1 && touch $(RESULTS_DIR)/$*.ok || touch $(RESULTS_DIR)/$*.bad
ifdef KEEP
	@test -f $(TOP_DIR)/compiler/tests/results/$*.ok && echo "$* ... PASS!" || (echo "$* ... FAIL!"; exit 1)
else
	@test -f $(TOP_DIR)/compiler/tests/results/$*.ok && echo "$* ... PASS!" && rm -rf $(TOP_DIR)/compiler/tests/results/$* || (echo "$* ... FAIL!"; exit 1)
endif
.DELETE_ON_ERROR: $(TEST_STAMPS)

clean:
	@rm -rf $(TOP_DIR)/compiler/tests/results
.PHONY: clean
