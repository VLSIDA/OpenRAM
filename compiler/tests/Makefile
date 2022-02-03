TOP_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST)))../..)
include $(TOP_DIR)/openram.mk

.DEFAULT_GOAL := regress

ARGS ?= "-k"

TEST_DIR = $(TOP_DIR)/compiler/tests
TEST_SRCS=$(sort $(notdir $(wildcard $(TEST_DIR)/*_test.py)))
TEST_DIRS=$(basename $(TEST_SRCS))
TEST_STAMPS=$(addsuffix .ok,$(TEST_DIRS))

TEST_BROKEN := \
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

$(TEST_DIRS):
	@$(MAKE) --no-print-directory $@.ok

tests:
	@echo "Running the following tests"
	@for S in $(WORKING_TEST_STAMPS); do echo " - $$S"; done
	@sleep 5
	@$(MAKE) $(WORKING_TEST_STAMPS)
.PHONY:

%.ok: %.py
	@echo "Running $*"
	@mkdir -p $(TOP_DIR)/compiler/tests/results/$*
	@docker run \
		-v $(TOP_DIR):/openram \
		-v $(FREEPDK45):/pdk/freepdk45\
		-v $(PDK_ROOT):/pdk \
		--user $(UID):$(GID) \
        vlsida/openram-ubuntu:latest \
		sh -c ". ~/.bashrc && python3 -u /openram/compiler/tests/$*.py $(ARGS) && touch $@"

.DELETE_ON_ERROR: $(TEST_STAMPS)

TECHS := scn4m_subm freepdk45
#sky130

$(TECHS):
	docker run \
		-v $(TOP_DIR):/openram \
		-v $(FREEPDK45):/pdk/freepdk45 \
		-v $(PDK_ROOT):/pdk \
		--user $(UID):$(GID) \
		-e OPENRAM_TMP=/openram/compiler/tests/tmp_$@/$* \
		vlsida/openram-ubuntu:latest \
        sh -c ". ~/.bashrc && python3 -u /openram/compiler/tests/regress.py $(ARGS) -t $@"
.PHONY: $(TECHS)

regress: $(TECHS)
.PHONY: regress

foo:
	docker run \
		-v $(TOP_DIR):/openram \
		-v $(FREEPDK45):/pdk/freepdk45 \
		-v $(PDK_ROOT):/pdk \
		--user $(UID):$(GID) \
        vlsida/openram-ubuntu:latest \
		sh -c ". ~/.bashrc && env"
.PHONY: foo

mount:
	docker run -it \
		-v $(TOP_DIR):/openram \
		-v $(FREEPDK45):/pdk/freepdk45 \
		-v $(PDK_ROOT):/pdk \
		--user $(UID):$(GID) \
        vlsida/openram-ubuntu:latest
.PHONY: mount

clean:
	@rm -rf $(TEST_STAMPS)
	@rm -rf $(TEST_DIRS)
.PHONE: clean
