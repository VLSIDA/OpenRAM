CUR_DIR = $(shell pwd)
TEST_DIR = ${CUR_DIR}/tests

MAKEFLAGS += -j 2

# Library test
LIBRARY_TESTS = \
01_library_drc_test.py \
02_library_lvs_test.py

# Technology and DRC tests (along with ptx)
TECH_TESTS = \
03_contact_test.py \
03_ptx_1finger_pmos_test.py \
03_ptx_4finger_nmos_test.py \
03_path_test.py \
03_ptx_3finger_nmos_test.py \
03_ptx_4finger_pmos_test.py \
03_ptx_1finger_nmos_test.py \
03_ptx_3finger_pmos_test.py \
03_wire_test.py

# Parameterized cells
PCELLS_TESTS = \
04_pinv_1x_test.py \
04_pinv_1x_beta_test.py \
04_pinv_2x_test.py \
04_pinv_10x_test.py \
04_pnand2_test.py \
04_pnor2_test.py \
04_pnand3_test.py\
04_wordline_driver_test.py \
04_precharge_test.py

# Dynamically generated modules and arrays
MODULE_TESTS = \
05_bitcell_array_test.py \
06_hierarchical_decoder_test.py \
06_hierarchical_predecode2x4_test.py \
06_hierarchical_predecode3x8_test.py \
07_single_level_column_mux_array_test.py \
08_precharge_array_test.py \
09_sense_amp_array_test.py \
10_write_driver_array_test.py \
11_ms_flop_array_test.py \
12_tri_gate_array_test.py \
13_delay_chain_test.py \
14_replica_bitline_test.py \
16_control_logic_test.py 

# Top-level SRAM configurations
TOP_TESTS = \
19_multi_bank_test.py \
19_single_bank_test.py \
20_sram_1bank_test.py \
20_sram_2bank_test.py \
20_sram_4bank_test.py

# All simulation tests.
CHAR_TESTS = \
21_hspice_delay_test.py \
21_ngspice_delay_test.py \
21_ngspice_setuphold_test.py \
21_hspice_setuphold_test.py \
22_sram_func_test.py \
22_pex_func_test_with_pinv.py \
23_lib_sram_prune_test.py \
23_lib_sram_test.py

# Keep the model lib test here since it is fast
# and doesn't need simulation.
USAGE_TESTS = \
23_lib_sram_model_test.py \
24_lef_sram_test.py \
25_verilog_sram_test.py 

ALL_FILES = \
${LIBRARY_TESTS} \
${TECH_TESTS} \
${PCELLS_TESTS} \
${MODULES_TESTS} \
${TOP_TESTS} \
${CHAR_TESTS} \
${USAGE_TESTS} 

default all:

$(ALL_FILES):
	python ${TEST_DIR}/$@ -t freepdk45
	python ${TEST_DIR}/$@ -t scn3me_subm

# Library tests
lib:	${LIBRARY_TESTS}

# Transistor and wire tests
tech: ${TECH_TESTS}

# Dynamically generated cells
pcells: ${PCELLS_TESTS}

# Dynamically generated modules
modules: ${MODULES_TESTS}

# Top level SRAM tests
top: ${TOP_TESTS}

# Timing and characterization tests
char: ${CHAR_TESTS}

# Usage and file generation
usage: ${USAGE_TESTS}

clean:
	find . -name \*.pyc -exec rm {} \;
	find . -name \*~ -exec rm {} \;

