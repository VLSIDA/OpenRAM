TOP_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST)))../..)
include $(TOP_DIR)/openram.mk

.DEFAULT_GOAL := all

ARGS ?=
TEST_TECHS ?= scn4m_subm freepdk45
TECHS ?= scn4m_subm freepdk45 sky130

TEST_DIR   = $(TOP_DIR)/compiler/tests
TEST_SRCS  = $(sort $(notdir $(wildcard $(TEST_DIR)/*_test.py)))
TEST_BASES = $(basename $(TEST_SRCS))
TEST_STAMPS= $(addsuffix .ok,$(TEST_BASES))

OPENRAM_DIR = /openram/compiler/tests
RESULTS_DIR = $(OPENRAM_DIR)/results

# Use % for all techs: 
# %/test.py
# or a specific tech:
# freepdk45/test.py
BROKEN_STAMPS = \
	sky130/01_library_test.ok \
	sky130/04_column_mux_pbitcell_test.ok \
	sky130/04_dummy_pbitcell_test.ok \
	sky130/04_pbitcell_test.ok \
	sky130/04_pnand4_test.ok \
	sky130/04_pand4_test.ok \
	sky130/04_precharge_pbitcell_test.ok \
	sky130/04_replica_pbitcell_test.ok \
	sky130/05_pbitcell_array_test.ok \
	sky130/05_bitcell_array_test.ok \
	sky130/05_bitcell_array_1rw_1r_test.ok \
	sky130/05_dummy_array_test.ok \
	sky130/07_column_mux_array_pbitcell_test.ok \
	sky130/19_pmulti_bank_test.ok \
	sky130/19_psingle_bank_test.ok \
	sky130/19_bank_select_pbitcell_test.ok \
	sky130/20_psram_1bank_2mux_1rw_1w_test.ok \
	sky130/20_psram_1bank_2mux_1rw_1w_wmask_test.ok \
	sky130/20_psram_1bank_2mux_1w_1r_test.ok \
	sky130/20_psram_1bank_2mux_test.ok \
	sky130/20_psram_1bank_4mux_1rw_1r_test.ok \
	sky130/22_psram_1bank_2mux_func_test.ok \
	sky130/22_psram_1bank_4mux_func_test.ok \
	sky130/22_psram_1bank_8mux_func_test.ok \
	sky130/22_psram_1bank_nomux_func_test.ok \
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
	%/50_riscv_8k_1rw_func_test.ok

gettech = $(word 1,$(subst /, ,$*))
getfile = $(word 2,$(subst /, ,$*))
TECH_TEST_STAMPS=$(foreach T, $(TEST_TECHS), $(addprefix $T/, $(TEST_STAMPS)))

# Filter out the tests after creating the tech stamps
WORKING_TECH_TEST_STAMPS=$(filter-out $(BROKEN_STAMPS), $(TECH_TEST_STAMPS))


# Run all technologies
all: $(WORKING_TECH_TEST_STAMPS)
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
	@docker run \
		-v $(TOP_DIR):/openram \
		-v $(FREEPDK45):/pdk/freepdk45\
		-e FREEPDK45=/pdk/freepdk45\
		-v $(PDK_ROOT):/pdk \
		-e PDK_ROOT=/pdk \
		-e PDKPATH=/pdk/sky130A \
		-v /etc/passwd:/etc/passwd:ro -v /etc/group:/etc/group:ro \
		--user $(UID):$(GID) \
		-e OPENRAM_TMP=$(OPENRAM_DIR)/results/$*/tmp \
        vlsida/openram-ubuntu:latest \
		sh -c ". /home/cad-user/.bashrc && python3 -u $(OPENRAM_DIR)/$(getfile).py \
		-t $(gettech) -k $(ARGS) -p $(OPENRAM_DIR)/results/$* > $(OPENRAM_DIR)/results/$*.out 2>&1 && touch $(OPENRAM_DIR)/results/$*.ok || touch $(OPENRAM_DIR)/results/$*.bad"
	@test -f $(TOP_DIR)/compiler/tests/results/$*.ok && echo "$* ... PASS!" && \
	rm -rf $(TOP_DIR)/compiler/tests/results/$* || echo "$* ... FAIL!"
.DELETE_ON_ERROR: $(TEST_STAMPS)

# Mount environment for debug
#
mount:
	docker run -it \
		-v $(TOP_DIR):/openram \
		-v $(FREEPDK45):/pdk/freepdk45 \
		-v $(PDK_ROOT):/pdk \
		-e PDK_ROOT=/pdk \
		-e PDKPATH=/pdk/sky130A \
		-v /etc/passwd:/etc/passwd:ro -v /etc/group:/etc/group:ro \
		--user $(UID):$(GID) \
        vlsida/openram-ubuntu:latest
.PHONY: mount

clean:
	@rm -rf $(TOP_DIR)/compiler/tests/results
.PHONE: clean
