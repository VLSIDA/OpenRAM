MACRO_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
TOP_DIR := $(realpath $(MACRO_DIR)/..)
include $(TOP_DIR)/openram.mk

UID = $(shell id -u)
GID = $(shell id -g)

.DEFAULT_GOAL := all

SKY130_PDK ?= $(PDK_ROOT)/share/pdk/sky130A

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

CONFIG_DIR = configs
SRCS=$(filter-out disabled-% %_common.py,$(sort $(notdir $(wildcard $(CONFIG_DIR)/*.py))))
DIRS=$(basename $(SRCS))
STAMPS=$(addsuffix .ok,$(DIRS))

configs:
	@echo
	@echo "Using OpenRAM at $(OPENRAM_HOME)"
	@echo " (which is version $$(cd $(OPENRAM_HOME); git describe --tags))"
	@echo
	@echo "Configurations:"
	@for D in $(DIRS); do echo " - $$D"; done
	@echo

.PHONY: configs

BROKEN := \
	sky130_sram_1kbyte_1r1w_8x1024_8 \
	sky130_sram_1kbyte_1rw_32x256_8 \
	sky130_sram_2kbyte_1rw_32x512_8 \
	sky130_sram_4kbyte_1rw_32x1024_8 \

WORKING_STAMPS=$(filter-out $(addsuffix .ok, (BROKEN)), $(STAMPS))

all: | configs
	@echo
	@echo "Building following working configs"
	@for S in $(WORKING_STAMPS); do echo " - $$S"; done
	@sleep 5
	$(MAKE) $(WORKING_STAMPS)
	@echo "Built all macros."

%.ok: configs/%.py
	@echo "Building $*"
	@mkdir -p $*
	docker run -v $(TOP_DIR):/openram \
		-v $(SKY130_PDK):$(SKY130_PDK) \
		-e PDK_ROOT=$(PDK_ROOT) \
                -e OPENRAM_HOME=/openram/compiler \
                -e OPENRAM_TECH=/openram/technology \
		-e OPENRAM_TMP=/openram/macros/$*/tmp \
		--user $(UID):$(GID) \
                vlsida/openram-ubuntu:latest \
		python3 -u /openram/compiler/openram.py $(OPENRAM_OPTS) -o $* -p /openram/macros/$* /openram/macros/$< && touch $@

mount:
	docker run -it -v $(TOP_DIR):/openram \
		-v $(SKY130_PDK):$(SKY130_PDK) \
		-e PDK_ROOT=$(PDK_ROOT) \
                -e OPENRAM_HOME=/openram/compiler \
                -e OPENRAM_TECH=/openram/technology \
		--user $(UID):$(GID) \
                vlsida/openram-ubuntu:latest
.PHONY: macros


.DELETE_ON_ERROR: $(STAMPS)

$(DIRS):
	@$(MAKE) --no-print-directory $@.ok

.PHONY: $(DIRS)

clean:
	rm -rf $(STAMPS)
	rm -rf $(DIRS)
.PHONY: clean
