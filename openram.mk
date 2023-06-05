OPENRAM_HOME := $(abspath $(TOP_DIR)/compiler)
OPENRAM_TECH := $(abspath $(TOP_DIR)/technology)
SRAM_COMPILER := $(abspath $(TOP_DIR)/sram_compiler.py)
ROM_COMPILER := $(abspath $(TOP_DIR)/rom_compiler.py)

PDK_ROOT ?= $(TOP_DIR)

ifeq (,$(wildcard $(SRAM_COMPILER)))
$(error Did not find '$(SRAM_COMPILER)' in '$(OPENRAM_HOME)' (from $$OPENRAM_HOME))
endif
export OPENRAM_HOME
export OPENRAM_TECH
export PDK_ROOT
#$(info Using OPENRAM_HOME=$(OPENRAM_HOME))
#$(info Using OPENRAM_TECH=$(OPENRAM_TECH))
#$(info Using PDK_ROOT=$(PDK_ROOT))

UID = $(shell id -u)
GID = $(shell id -g)

export OPENRAM_TMP=$(OPENRAM_DIR)/results/$*/tmp
export DOCKER_CMD= docker run \
		-v $(TOP_DIR):/openram \
		-v $(FREEPDK45):/freepdk45 \
		-e FREEPDK45=/freepdk45 \
		-v $(PDK_ROOT):/pdk \
		-e PDK_ROOT=/pdk \
		-e PDKPATH=/pdk/sky130A \
        -e OPENRAM_HOME=/openram/compiler \
        -e OPENRAM_TECH=/openram/technology \
		-e OPENRAM_TMP=$(OPENRAM_TMP)\
        -e PYTHONPATH=/openram/compiler \
		-v /etc/passwd:/etc/passwd:ro -v /etc/group:/etc/group:ro \
		--user $(UID):$(GID) \
        vlsida/openram-ubuntu:latest

mount:
	@docker run -it \
	    -v $(TOP_DIR):/openram \
		-v $(FREEPDK45):/freepdk45 \
		-e FREEPDK45=/freepdk45 \
		-v $(PDK_ROOT):/pdk \
		-e PDK_ROOT=/pdk \
		-e PDKPATH=/pdk/sky130A \
        -e OPENRAM_HOME=/openram/compiler \
        -e OPENRAM_TECH=/openram/technology \
        -e PYTHONPATH=/openram/compiler \
		-v /etc/passwd:/etc/passwd:ro -v /etc/group:/etc/group:ro \
		--user $(UID):$(GID) \
        vlsida/openram-ubuntu:latest
.PHONY: mount

