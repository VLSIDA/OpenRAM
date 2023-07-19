TOP_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
include $(TOP_DIR)/openram.mk

.DEFAULT_GOAL := install

# Set the shell here
SHELL := /bin/bash

# Skywater PDK SRAM library
SRAM_LIB_DIR ?= $(PDK_ROOT)/sky130_fd_bd_sram
# Use this for release
SRAM_LIB_GIT_REPO ?= https://github.com/vlsida/sky130_fd_bd_sram.git
# Use this for development
#SRAM_LIB_GIT_REPO ?= git@github.com:VLSIDA/sky130_fd_bd_sram.git
#SRAM_LIB_GIT_REPO ?= https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram.git
SRAM_LIB_GIT_COMMIT ?= 060f3638be6269dd9aa82cfbbdfd9525943c1582

# Open PDKs
OPEN_PDKS_DIR ?= $(PDK_ROOT)/open_pdks
OPEN_PDKS_GIT_REPO ?= https://github.com/RTimothyEdwards/open_pdks.git
OPEN_PDKS_GIT_COMMIT ?= 1.0.311
#OPEN_PDKS_GIT_COMMIT ?= 7ea416610339d3c29af9d0d748ceadd3fd368608
SKY130_PDK ?= $(PDK_ROOT)/sky130A

# Skywater PDK
SKY130_PDKS_DIR ?= $(PDK_ROOT)/skywater-pdk
SKY130_PDKS_GIT_REPO ?= https://github.com/google/skywater-pdk.git
SKY130_PDKS_GIT_COMMIT ?= f70d8ca46961ff92719d8870a18a076370b85f6c

# Create lists of all the files to copy/link
GDS_FILES := $(sort $(wildcard $(SRAM_LIB_DIR)/cells/*/*.gds))
GDS_FILES := $(GDS_FILES) $(PDK_ROOT)/skywater-pdk/libraries/sky130_fd_sc_hd/latest/cells/dlxtn/sky130_fd_sc_hd__dlxtn_1.gds
MAG_FILES := $(sort $(wildcard $(SRAM_LIB_DIR)/cells/*/*.mag))

SPICE_SUFFIX := spice
SPICE_LVS_SUFFIX := lvs.$(SPICE_SUFFIX)
SPICE_CALIBRE_SUFFIX := lvs.calibre.$(SPICE_SUFFIX)
SPICE_KLAYOUT_SUFFIX := lvs.klayout.$(SPICE_SUFFIX)
SPICE_BASE_SUFFIX := base.$(SPICE_SUFFIX)
ALL_SPICE_FILES := $(sort $(wildcard $(SRAM_LIB_DIR)/cells/*/*.$(SPICE_SUFFIX)))
ALL_SPICE_FILES := $(ALL_SPICE_FILES) $(PDK_ROOT)/skywater-pdk/libraries/sky130_fd_sc_hd/latest/cells/dlxtn/sky130_fd_sc_hd__dlxtn_1.spice

MAGLEF_SUFFIX := maglef
MAGLEF_FILES := $(sort $(wildcard $(SRAM_LIB_DIR)/cells/*/*.$(MAGLEF_SUFFIX)))

MAGICRC_FILE := $(SKY130_PDK)/libs.tech/magic/sky130A.magicrc

ALL_FILES := $(ALL_SPICE_FILES) $(GDS_FILES) $(MAG_FILES) $(MAGLEF_FILES)


INSTALL_BASE_DIRS := gds_lib mag_lib sp_lib lvs_lib calibre_lvs_lib klayout_lvs_lib maglef_lib
INSTALL_BASE := $(OPENRAM_HOME)/../technology/sky130
INSTALL_DIRS := $(addprefix $(INSTALL_BASE)/,$(INSTALL_BASE_DIRS))

# If conda is installed, we will use Magic from there
CONDA_DIR := $(wildcard $(TOP_DIR)/miniconda)

check-pdk-root:
ifndef PDK_ROOT
	$(error PDK_ROOT is undefined, please export it before running make)
endif

$(SKY130_PDKS_DIR): check-pdk-root
	@echo "Cloning skywater PDK..."
	@[ -d $(PDK_ROOT)/skywater-pdk ] || \
		git clone https://github.com/google/skywater-pdk.git $(PDK_ROOT)/skywater-pdk
	@git -C $(SKY130_PDKS_DIR) checkout $(SKY130_PDKS_GIT_COMMIT) && \
		git -C $(SKY130_PDKS_DIR) submodule update --init libraries/sky130_fd_pr/latest libraries/sky130_fd_sc_hd/latest

$(OPEN_PDKS_DIR): $(SKY130_PDKS_DIR)
	@echo "Cloning open_pdks..."
	@[ -d $(OPEN_PDKS_DIR) ] || \
		git clone $(OPEN_PDKS_GIT_REPO) $(OPEN_PDKS_DIR)
	@git -C $(OPEN_PDKS_DIR) checkout $(OPEN_PDKS_GIT_COMMIT)

$(SKY130_PDK): $(OPEN_PDKS_DIR) $(SKY130_PDKS_DIR)
	@echo "Installing open_pdks..."
ifeq ($(CONDA_DIR),"")
	@cd $(PDK_ROOT)/open_pdks && \
		./configure --enable-sky130-pdk=$(PDK_ROOT)/skywater-pdk/libraries --with-sky130-local-path=$(PDK_ROOT) && \
		cd sky130 && \
		make veryclean && \
		make && \
		make SHARED_PDKS_PATH=$(PDK_ROOT) install
else
	@source $(TOP_DIR)/miniconda/bin/activate && \
		cd $(PDK_ROOT)/open_pdks && \
		./configure --enable-sky130-pdk=$(PDK_ROOT)/skywater-pdk/libraries --with-sky130-local-path=$(PDK_ROOT) && \
		cd sky130 && \
		make veryclean && \
		make && \
		make SHARED_PDKS_PATH=$(PDK_ROOT) install && \
		conda deactivate
endif

$(SRAM_LIB_DIR): check-pdk-root
	@echo "Cloning SRAM library..."
	@[ -d $(SRAM_LIB_DIR) ] || \
		git clone $(SRAM_LIB_GIT_REPO) $(SRAM_LIB_DIR)
	@git -C $(SRAM_LIB_DIR) fetch
	@git -C $(SRAM_LIB_DIR) checkout $(SRAM_LIB_GIT_COMMIT)

install: $(SRAM_LIB_DIR)
	@[ -d $(PDK_ROOT)/sky130A ] || \
		(echo "Warning: $(PDK_ROOT)/sky130A not found!! Run make pdk first." &&  false)
	@[ -d $(PDK_ROOT)/skywater-pdk ] || \
		(echo "Warning: $(PDK_ROOT)/skywater-pdk not found!! Run make pdk first." && false)
	@echo "Installing sky130 SRAM PDK..."
	@echo "PDK_ROOT='$(PDK_ROOT)'"
	@echo "SRAM_LIB_DIR='$(SRAM_LIB_DIR)'"
	@echo "SKY130_PDK='$(SKY130_PDK)'"
	@make $(INSTALL_DIRS)
.PHONY: install

pdk: $(SKY130_PDK)
	@true
.PHONY: pdk

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

$(INSTALL_BASE)/klayout_lvs_lib: $(filter %.$(SPICE_KLAYOUT_SUFFIX),$(ALL_SPICE_FILES))
	@echo
	@echo "Setting up klayout LVS library for OpenRAM."
	@echo "=================================================================="
	mkdir -p $@
	@for SP in $?; do \
		cp -va $$SP $@/$$(basename $$SP .$(SPICE_KLAYOUT_SUFFIX)).sp; \
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
	@echo $(SKY130_PDK)
	@echo $(SRAM_LIB_DIR)
	@echo $(OPEN_PDKS_DIR)
	@echo  $(SKY130_PDKS_DIR)
	@echo "Wiping above PDK repos in 5 sec... (ctrl-c to quit)"
	@sleep 5
	@rm -rf $(SKY130_PDK)
	@rm -rf $(SRAM_LIB_DIR)
	@rm -rf $(OPEN_PDKS_DIR)
	@rm -rf $(SKY130_PDKS_DIR)
.PHONY: wipe

# Build the openram library
build_library:
	@rm -rf dist
	@rm -rf openram.egg-info
	@python3 -m pip install --upgrade build
	@python3 -m build
.PHONY: build_library

# Build and install the openram library
library: build_library
	@python3 -m pip install --force dist/openram*.whl
.PHONY: library
