TECH = scn4m_subm
CUR_DIR = $(shell pwd)
TEST_DIR = ${CUR_DIR}/tests

#MAKEFLAGS += -j 1

# Library test
LIBRARY_TESTS = $(shell find ${TEST_DIR} -name 0[1-2]*_test.py)

# Technology and DRC tests (along with ptx)
TECH_TESTS = $(shell find ${TEST_DIR} -name 03*_test.py)

# Parameterized cells
CELL_TESTS = $(shell find ${TEST_DIR} -name 04*_test.py)

# Dynamically generated modules and arrays
MODULE_TESTS = $(shell find ${TEST_DIR} -name 0[5-9]*_test.py)\
$(shell find ${TEST_DIR} -name 1*_test.py)

# Top-level SRAM configurations
TOP_TESTS = $(shell find ${TEST_DIR} -name 20*_test.py)

# All simulation tests.
CHAR_TESTS = $(shell find ${TEST_DIR} -name 2[1-2]*_test.py)

# Keep the model lib test here since it is fast
# and doesn't need simulation.
USAGE_TESTS = $(shell find ${TEST_DIR} -name 2[3-9]*_test.py)\
$(shell find ${TEST_DIR} -name 30*_test.py)

ALL_TESTS = \
${LIBRARY_TESTS} \
${TECH_TESTS} \
${CELL_TESTS} \
${MODULE_TESTS} \
${TOP_TESTS} \
${CHAR_TESTS} \
${USAGE_TESTS}

.PHONY: ${ALL_TESTS}

all: ${ALL_TESTS}

# Library tests
lib:	${LIBRARY_TESTS}

# Transistor and wire tests
tech: ${TECH_TESTS}

# Dynamically generated cells
cell: ${CELL_TESTS}

# Dynamically generated modules
module: ${MODULE_TESTS}

# Top level SRAM tests
top: ${TOP_TESTS}

# Timing and characterization tests
char: ${CHAR_TESTS}

# Usage and file generation
usage: ${USAGE_TESTS}

$(ALL_TESTS):
	python3 $@ -t ${TECH}


OPENRAM_TECHS = $(subst :, ,$(OPENRAM_TECH))
TECH_DIR := $(word 1, $(foreach dir,$(OPENRAM_TECHS),$(wildcard $(dir)/$(TECH))))
CONFIG_DIR = $(OPENRAM_HOME)/model_configs
MODEL_CONFIGS = $(wildcard $(CONFIG_DIR)/*.py)
SIM_DIR = $(OPENRAM_HOME)/model_data/$(TECH)
CSV_DIR = $(TECH_DIR)/sim_data
# Creates names of technology specific okay files for the configs
STAMPS=$(addprefix $(SIM_DIR)/, $(addsuffix .ok, $(notdir $(basename $(MODEL_CONFIGS)))))

OPTS =
# Characterize and perform DRC/LVS
OPTS += -c
# Do not characterize or perform DRC/LVS
OPTS += -n
# Verbosity
#OPTS += -v
# Spice
OPTS += -s hspice

.PHONY: model

model: $(STAMPS)
	mkdir -p $(CSV_DIR)
	python3 $(OPENRAM_HOME)/model_data_util.py $(SIM_DIR) $(CSV_DIR)

%.ok:
	$(eval bname=$(basename $(notdir $@)))
	$(eval config_path=$(CONFIG_DIR)/$(addsuffix .py, $(notdir $(basename $@))))
	mkdir -p $(SIM_DIR)/$(bname)
	-python3 $(OPENRAM_HOME)/../sram_compiler.py $(OPTS) -p $(SIM_DIR)/$(bname) -o $(bname) -t $(TECH) $(config_path) 2>&1 > /dev/null
	touch $@

clean_model:
	rm -f -r $(SIM_DIR)/*.ok

clean:
	find . -name \*.pyc -exec rm {} \;
	find . -name \*~ -exec rm {} \;
