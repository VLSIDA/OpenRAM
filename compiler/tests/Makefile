TOP_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST)))../..)
include $(TOP_DIR)/openram.mk

.DEFAULT_GOAL := all

ARGS ?=
TECH ?= scn4m_subm
TECHS = scn4m_subm freepdk45
# sky130

TEST_DIR   = $(TOP_DIR)/compiler/tests
TEST_SRCS  = $(sort $(notdir $(wildcard $(TEST_DIR)/*_test.py)))
TEST_BASES = $(basename $(TEST_SRCS))
TEST_STAMPS= $(addsuffix .ok,$(TEST_BASES))

OPENRAM_DIR = /openram/compiler/tests
RESULTS_DIR = $(OPENRAM_DIR)/results

TEST_BROKEN = \
	50_riscv_1k_1rw1r_func_test.py \
	50_riscv_1k_1rw_func_test.py \
	50_riscv_1rw1r_func_test.py \
	50_riscv_1rw1r_phys_test.py \
	50_riscv_1rw_func_test.py \
	50_riscv_1rw_phys_test.py \
	50_riscv_2k_1rw1r_func_test.py \
	50_riscv_2k_1rw_func_test.py \
	50_riscv_4k_1rw1r_func_test.py \
	50_riscv_4k_1rw_func_test.py \
	50_riscv_512b_1rw1r_func_test.py \
	50_riscv_512b_1rw_func_test.py \
	50_riscv_8k_1rw1r_func_test.py \
	50_riscv_8k_1rw_func_test.py


WORKING_TEST_STAMPS=$(filter-out $(addsuffix .ok, (TEST_BROKEN)), $(TEST_STAMPS))


gettech = $(word 1,$(subst /, ,$*))
getfile = $(word 2,$(subst /, ,$*))
WORKING_TECH_TEST_STAMPS=$(foreach T, $(TECHS),$(addprefix $T/,$(WORKING_TEST_STAMPS)))

all: $(WORKING_TECH_TEST_STAMPS)
.PHONY: all

# Targets for each individual test
# e.g. make 04_pinv_1x_test
$(TEST_BASES):
#	@echo "Running $(TECH) $@ ... "
	@$(MAKE) --no-print-directory $(TECH)/$@.ok
.PHONY: $(TEST_BASES)

# To run a test in a given technology
%.ok:
#	@echo "Running $(gettech) $(getfile) ... "
	@mkdir -p results/$*/tmp
	@docker run \
		-v $(TOP_DIR):/openram \
		-v $(FREEPDK45):/pdk/freepdk45\
		-v $(PDK_ROOT):/pdk \
		-v /etc/passwd:/etc/passwd:ro -v /etc/group:/etc/group:ro \
		--user $(UID):$(GID) \
		-e OPENRAM_TMP=$(OPENRAM_DIR)/results/$*/tmp \
        vlsida/openram-ubuntu:latest \
		sh -c ". /home/cad-user/.bashrc && python3 -u $(OPENRAM_DIR)/$(getfile).py \
		-t $(gettech) -k $(ARGS) -p $(OPENRAM_DIR)/results/$* > $(OPENRAM_DIR)/results/$*.out 2>&1 && touch $(OPENRAM_DIR)/results/$*.ok || touch $(OPENRAM_DIR)/results/$*.bad"
	@test -f $(TOP_DIR)/compiler/tests/results/$*.ok && echo "$* ... PASS!" && rm -rf $(OPENRAM_DIR)/results/$* || echo "$* ... FAIL!"
.DELETE_ON_ERROR: $(TEST_STAMPS)

# This would use the regress.py script to run in parallel instead of
# the Makefile.
#$(TECHS):
#	@echo "Running $*"
#	docker run \
#		-v $(TOP_DIR):/openram \
#		-v $(FREEPDK45):/pdk/freepdk45 \
#		-v $(PDK_ROOT):/pdk \
#		--user $(UID):$(GID) \
#		-e OPENRAM_TMP=$(OPENRAM_DIR)/results/$@ \
#		vlsida/openram-ubuntu:latest \
#        sh -c ". /home/cad-user/.bashrc && python3 -u $(OPENRAM_DIR)/regress.py -t $@ $(ARGS)"
#.PHONY: $(TECHS)
#regress: $(TECHS)
#.PHONY: regress

# Mount environment for debug
mount:
	docker run -it \
		-v $(TOP_DIR):/openram \
		-v $(FREEPDK45):/pdk/freepdk45 \
		-v $(PDK_ROOT):/pdk \
		-v /etc/passwd:/etc/passwd:ro -v /etc/group:/etc/group:ro \
		--user $(UID):$(GID) \
        vlsida/openram-ubuntu:latest
.PHONY: mount

clean:
	@rm -rf $(TOP_DIR)/compiler/tests/results
.PHONE: clean
