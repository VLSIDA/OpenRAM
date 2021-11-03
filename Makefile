TOP_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
include $(TOP_DIR)/openram.mk

.DEFAULT_GOAL := install

# Keep it locally if they didn't specify
PDK_ROOT ?= $(TOP_DIR)

# Skywater PDK SRAM library
SRAM_LIB_DIR ?= $(PDK_ROOT)/sky130_fd_bd_sram
SRAM_LIB_GIT_REPO ?= https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram.git
SRAM_LIB_GIT_COMMIT ?= main

# Open PDKs
OPEN_PDKS_DIR ?= $(PDK_ROOT)/open_pdks
OPEN_PDKS_GIT_REPO ?= https://github.com/RTimothyEdwards/open_pdks.git
OPEN_PDKS_GIT_COMMIT ?= 1.0.156
SKY130_PDK ?= $(PDK_ROOT)/share/pdk/sky130A

# Create lists of all the files to copy/link
GDS_FILES := $(sort $(wildcard $(SRAM_LIB_DIR)/cells/*/*.gds))
MAG_FILES := $(sort $(wildcard $(SRAM_LIB_DIR)/cells/*/*.mag))

SPICE_SUFFIX := spice
SPICE_LVS_SUFFIX := lvs.$(SPICE_SUFFIX)
SPICE_CALIBRE_SUFFIX := lvs.calibre.$(SPICE_SUFFIX)
SPICE_BASE_SUFFIX := base.$(SPICE_SUFFIX)
ALL_SPICE_FILES := $(sort $(wildcard $(SRAM_LIB_DIR)/cells/*/*.$(SPICE_SUFFIX)))

MAGLEF_SUFFIX := maglef
MAGLEF_FILES := $(sort $(wildcard $(SRAM_LIB_DIR)/cells/*/*.$(MAGLEF_SUFFIX)))

MAGICRC_FILE := $(SKY130_PDK)/libs.tech/magic/sky130A.magicrc

ALL_FILES := $(ALL_SPICE_FILES) $(GDS_FILES) $(MAG_FILES) $(MAGLEF_FILES)


INSTALL_BASE_DIRS := gds_lib mag_lib sp_lib lvs_lib calibre_lvs_lib maglef_lib
INSTALL_BASE := $(OPENRAM_HOME)/../technology/sky130
INSTALL_DIRS := $(addprefix $(INSTALL_BASE)/,$(INSTALL_BASE_DIRS))

$(OPEN_PDKS_DIR):
	@echo "Cloning open_pdks..."
	git clone $(OPEN_PDKS_GIT_REPO) $(OPEN_PDKS_DIR)
	cd $(OPEN_PDKS_DIR) && git checkout $(OPEN_PDKS_GIT_COMMIT)

$(SKY130_PDK): $(OPEN_PDKS_DIR)
	@echo "Installing open_pdks..."
	cd $(OPEN_PDKS_DIR) &&\
	./configure --prefix=$(PDK_ROOT) --enable-sky130-pdk  \
	--disable-openlane --disable-irsim --disable-xschem --disable-qflow
	@sleep 5
	make -C $(OPEN_PDKS_DIR) install

install: $(SRAM_LIB_DIR) $(SKY130_PDK) $(INSTALL_DIRS)
	@echo "Installing sky130 SRAM PDK..."
	@echo "PDK_ROOT='$(PDK_ROOT)'"
	@echo "SRAM_LIB_DIR='$(SRAM_LIB_DIR)'"
	@echo "SKY130_PDK='$(SKY130_PDK)'"
	@true
.PHONY: install

$(SRAM_LIB_DIR):
	@echo "Cloning SRAM library..."
	git clone $(SRAM_LIB_GIT_REPO) $(SRAM_LIB_DIR)
	cd $(SRAM_LIB_DIR) && git checkout $(SRAM_LIB_GIT_COMMIT)

.PHONY: $(INSTALL_DIRS)

$(INSTALL_BASE)/gds_lib: $(GDS_FILES)
	@echo
	@echo "Setting up GDS cell library for OpenRAM."
	@echo "=================================================================="
	mkdir -p $@
	cp -va $? $@
	@echo "=================================================================="
	@echo

$(INSTALL_BASE)/mag_lib: $(MAG_FILES)
	@echo
	@echo "Setting up MAG files for OpenRAM."
	@echo "=================================================================="
	mkdir -p $@
	@cp -va $? $@
	@echo
	cp -f $(MAGICRC_FILE) $(INSTALL_BASE)/tech/.magicrc
	cp -f $(MAGICRC_FILE) $(INSTALL_BASE)/mag_lib/.magicrc
	@echo "=================================================================="
	@echo

$(INSTALL_BASE)/maglef_lib: $(MAGLEF_FILES)
	@echo
	@echo "Setting up MAGLEF cell library for OpenRAM."
	@echo "=================================================================="
	mkdir -p $@
	@for SP in $?; do \
		cp -va $$SP $@/$$(basename $$SP .$(MAGLEF_SUFFIX)).mag; \
	done
	@echo
	cp -f $(MAGICRC_FILE) $(INSTALL_BASE)/maglef_lib/.magicrc
	@echo "=================================================================="
	@echo


$(INSTALL_BASE)/lvs_lib: $(filter %.$(SPICE_LVS_SUFFIX),$(ALL_SPICE_FILES))
	@echo
	@echo "Setting up LVS cell library for OpenRAM."
	@echo "=================================================================="
	mkdir -p $@
	@for SP in $?; do \
		cp -va $$SP $@/$$(basename $$SP .$(SPICE_LVS_SUFFIX)).sp; \
	done
	@echo "=================================================================="
	@echo

$(INSTALL_BASE)/calibre_lvs_lib: $(filter %.$(SPICE_CALIBRE_SUFFIX),$(ALL_SPICE_FILES))
	@echo
	@echo "Setting up Calibre LVS library for OpenRAM."
	@echo "=================================================================="
	mkdir -p $@
	@for SP in $?; do \
		cp -va $$SP $@/$$(basename $$SP .$(SPICE_CALIBRE_SUFFIX)).sp; \
	done
	@echo "=================================================================="
	@echo

$(INSTALL_BASE)/sp_lib: $(filter-out %.$(SPICE_LVS_SUFFIX) %.$(SPICE_CALIBRE_SUFFIX),$(ALL_SPICE_FILES))
	@echo
	@echo "Setting up spice simulation library for OpenRAM."
	@echo "=================================================================="
	mkdir -p $@
	@for SP in $(filter-out %.$(SPICE_BASE_SUFFIX),$?); do \
		cp -va $$SP $@/$$(basename $$SP .$(SPICE_SUFFIX)).sp; \
	done
	@echo
	@echo "Overwriting some cells with base version."
	@for SP in $(filter %.$(SPICE_BASE_SUFFIX),$?); do \
		cp -va $$SP $@/$$(basename $$SP .$(SPICE_BASE_SUFFIX)).sp; \
	done
	@echo "=================================================================="
	@echo

macros:
	cd macros && make

.PHONY: macros

mount:
	@docker run -it -v $(TOP_DIR):/openram \
		-v $(SKY130_PDK):$(SKY130_PDK) \
		-e PDK_ROOT=$(PDK_ROOT) \
                -e OPENRAM_HOME=/openram/compiler \
                -e OPENRAM_TECH=/openram/technology \
		--user $(UID):$(GID) \
                vlsida/openram-ubuntu:latest
.PHONY: mount

clean:
	@rm -f *.zip
.PHONE: clean

uninstall: clean
	@rm -f $(INSTALL_BASE)/tech/.magicrc
	@rm -f $(INSTALL_BASE)/mag_lib/.magicrc
	@rm -f $(INSTALL_BASE)/lef_lib/.magicrc
	@rm -f $(INSTALL_BASE)/maglef_lib/.magicrc
	@rm -rf $(INSTALL_DIRS)
.PHONY: uninstall

# wipe the entire repos
wipe: uninstall
	@echo "Wiping PDK repos in 5 sec... (ctrl-c to quit)"
	@sleep 5
	@rm -rf $(SKY130_PDK)
	@rm -rf $(SRAM_LIB_DIR)
	@rm -rf $(OPEN_PDKS_DIR)
.PHONY: wipe
