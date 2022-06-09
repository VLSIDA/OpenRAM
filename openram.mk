OPENRAM_HOME := $(abspath $(TOP_DIR)/compiler)
OPENRAM_TECH := $(abspath $(TOP_DIR)/technology)
OPENRAM_COMPILER := $(OPENRAM_HOME)/openram.py

PDK_ROOT ?= $(TOP_DIR)

ifeq (,$(wildcard $(OPENRAM_COMPILER)))
$(error Did not find '$(OPENRAM_COMPILER)' in '$(OPENRAM_HOME)' (from $$OPENRAM_HOME))
endif
export OPENRAM_HOME
export OPENRAM_TECH
export PDK_ROOT
#$(info Using OPENRAM_HOME=$(OPENRAM_HOME))
#$(info Using OPENRAM_TECH=$(OPENRAM_TECH))
#$(info Using PDK_ROOT=$(PDK_ROOT))

UID = $(shell id -u)
GID = $(shell id -g)
