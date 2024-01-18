MACRO_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
TOP_DIR := $(realpath $(MACRO_DIR)/..)
include $(TOP_DIR)/openram.mk

.DEFAULT_GOAL := all

SKY130_PDK ?= $(PDK_ROOT)/sky130A

OPENRAM_DIR = $(MACRO_DIR)
OPENRAM_OPTS := $(OPENRAM_OPTS)
# Define `OPENRAM_FULL` in your environment to run a full characterize
ifeq ($(OPENRAM_FULL),)
# Do not characterize (default)
else
# Characterize
OPTS += -c
endif
# Verbosity
OPENRAM_OPTS += -v --keeptemp

SRAM_CONFIG_DIR = sram_configs
SRAM_SRCS=$(filter-out disabled-% %_common.py,$(sort $(notdir $(wildcard $(SRAM_CONFIG_DIR)/*.py))))
SRAM_DIRS=$(basename $(SRAM_SRCS))
SRAM_STAMPS=$(addsuffix .ok,$(SRAM_DIRS))

ROM_CONFIG_DIR = rom_configs
ROM_SRCS=$(filter-out disabled-% %_common.py,$(sort $(notdir $(wildcard $(ROM_CONFIG_DIR)/*.py))))
ROM_DIRS=$(basename $(ROM_SRCS))
ROM_STAMPS=$(addsuffix .ok,$(ROM_DIRS))

DIRS=$(SRAM_DIRS) $(ROM_DIRS)

configs:
	@echo
	@echo "Using OpenRAM at $(OPENRAM_HOME)"
	@echo " (which is version $$(cd $(OPENRAM_HOME); git describe --tags))"
	@echo
	@echo "SRAM Configurations:"
	@for D in $(SRAM_DIRS); do echo " - $$D"; done
	@echo "ROM Configurations:"
	@for D in $(ROM_DIRS); do echo " - $$D"; done
	@echo

.PHONY: configs

BROKEN :=

WORKING_SRAM_STAMPS=$(filter-out $(addsuffix .ok, $(BROKEN)), $(SRAM_STAMPS))
WORKING_ROM_STAMPS=$(filter-out $(addsuffix .ok, $(BROKEN)), $(ROM_STAMPS))

EXAMPLE_STAMPS=$(filter example%, $(WORKING_SRAM_STAMPS)) $(filter example%, $(WORKING_ROM_STAMPS))
SKY130_STAMPS=$(filter sky130%, $(WORKING_SRAM_STAMPS)) $(filter sky130%, $(WORKING_ROM_STAMPS))
GF180MCU_STAMPS=$(filter gf180mcu%, $(WORKING_SRAM_STAMPS)) $(filter gf180mcu%, $(WORKING_ROM_STAMPS))
FREEPDK45_STAMPS=$(filter freepdk45%, $(WORKING_STAMPS)) $(filter freepdk45%, $(WORKING_ROM_STAMPS))
SCN4M_SUBM_STAMPS=$(filter scn4m_subm%, $(WORKING_STAMPS)) $(filter scn4m_subm%, $(WORKING_ROM_STAMPS))

all: | configs
	@echo
	@echo "Building following working configs"
	@for S in $(WORKING_STAMPS); do echo " - $$S"; done
	@sleep 5
	$(MAKE) $(WORKING_STAMPS)
	@echo "Built all macros."

example: $(EXAMPLE_STAMPS)
.PHONY: example

sky130: $(SKY130_STAMPS)
.PHONY: sky130

freepdk45: $(FREEPDK45_STAMPS)
.PHONY: freepdk45

scn4m_subm: $(SCN4M_SUBM_STAMPS)
.PHONY: scn4m_subm

rom: $(WORKING_ROM_STAMPS)
.PHONY: rom

sram: $(WORKING_SRAM_STAMPS)
.PHONY: sram

%.ok: sram_configs/%.py
	@echo "Building $*"
	@mkdir -p $*
	@OPENRAM_TMP=$*/tmp python3 -u $(SRAM_COMPILER) $(OPENRAM_OPTS) -o $* -p $(MACRO_DIR)/$* $(MACRO_DIR)/$< && touch $@

%.ok: rom_configs/%.py
	@echo "Building $*"
	@mkdir -p $*
	@OPENRAM_TMP=$*/tmp python3 -u $(ROM_COMPILER) $(OPENRAM_OPTS) -o $* -p $(MACRO_DIR)/$* $(MACRO_DIR)/$< && touch $@

.DELETE_ON_ERROR: $(WORKING_SRAM_STAMPS) $(WORKING_ROM_STAMPS)

$(DIRS):
	@$(MAKE) --no-print-directory $@.ok

.PHONY: $(DIRS)

clean:
	rm -rf $(WORKING_SRAM_STAMPS)
	rm -rf $(WORKING_ROM_STAMPS)
	rm -rf $(SRAM_DIRS)
	rm -rf $(ROM_DIRS)
.PHONY: clean
