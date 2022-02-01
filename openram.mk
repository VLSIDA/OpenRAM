OPENRAM_HOME := $(abspath $(TOP_DIR)/compiler)
OPENRAM_TECH := $(abspath $(TOP_DIR)/technology)
OPENRAM_COMPILER := $(OPENRAM_HOME)/openram.py
ifeq (,$(wildcard $(OPENRAM_COMPILER)))
$(error Did not find '$(OPENRAM_COMPILER)' in '$(OPENRAM_HOME)' (from $$OPENRAM_HOME))
endif
export OPENRAM_HOME
export OPENRAM_TECH

UID = $(shell id -u)
GID = $(shell id -g)
