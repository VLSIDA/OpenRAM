# -*- coding: utf-8 -*-
#
# Copyright 2020 Regents of the University of California
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

# The top directory where environment will be created.
TOP_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))

.DEFAULT_GOAL := all

# Skywater PDK SRAM library
#SRAM_LIBRARY ?= $(PDK_ROOT)/skywater-pdk/libraries/sky130_fd_bd_sram
SRAM_GIT_REPO ?= git@github.com:google/skywater-pdk-libs-sky130_fd_bd_sram.git
SRAM_LIBRARY ?= $(TOP_DIR)/sky130_fd_bd_sram
# Open PDKs
OPEN_PDKS ?= $(PDK_ROOT)/sky130A


# Create lists of all the files to copy/link
GDS_FILES := $(sort $(wildcard $(SRAM_LIBRARY)/cells/*/*.gds))
MAG_FILES := $(sort $(wildcard $(SRAM_LIBRARY)/cells/*/*.mag))

SPICE_SUFFIX := spice
SPICE_LVS_SUFFIX := lvs.$(SPICE_SUFFIX)
SPICE_CALIBRE_SUFFIX := lvs.calibre.$(SPICE_SUFFIX)
SPICE_BASE_SUFFIX := base.$(SPICE_SUFFIX)
ALL_SPICE_FILES := $(sort $(wildcard $(SRAM_LIBRARY)/cells/*/*.$(SPICE_SUFFIX)))

MAGLEF_SUFFIX := maglef
MAGLEF_FILES := $(sort $(wildcard $(SRAM_LIBRARY)/cells/*/*.$(MAGLEF_SUFFIX)))

MAGICRC_FILE := $(OPEN_PDKS)/libs.tech/magic/sky130A.magicrc

ALL_FILES := $(ALL_SPICE_FILES) $(GDS_FILES) $(MAG_FILES) $(MAGLEF_FILES)


INSTALL_BASE_DIRS := gds_lib mag_lib sp_lib lvs_lib calibre_lvs_lib lef_lib maglef_lib
INSTALL_BASE := $(OPENRAM_HOME)/../technology/sky130
INSTALL_DIRS := $(addprefix $(INSTALL_BASE)/,$(INSTALL_BASE_DIRS))


install: $(INSTALL_DIRS)

$(SRAM_LIBRARY):
	git clone $(SRAM_GIT_REPO) $(SRAM_LIBRARY)

.PHONY: $(SRAM_LIBRARY) $(INSTALL_DIRS) install

all:	$(SRAM_LIBRARY)
	@echo "Installing sky130 SRAM PDK..."
	@echo "PDK_ROOT='$(PDK_ROOT)'"
	@echo "SRAM_LIBRARY='$(SRAM_LIBRARY)'"
	@echo "OPEN_PDKS='$(OPEN_PDKS)'"
	make install
	@true

$(INSTALL_BASE)/gds_lib: $(GDS_FILES)
	@echo
	@echo "Setting up GDS cell library for OpenRAM."
	@echo "=================================================================="
	mkdir -p $@
	@cp -va $? $@
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

clean:
	rm -f $(SRAM_LIBRARY)
	rm -f $(INSTALL_BASE)/tech/.magicrc
	rm -f $(INSTALL_BASE)/mag_lib/.magicrc
	rm -f $(INSTALL_BASE)/lef_lib/.magicrc
	rm -f $(INSTALL_BASE)/maglef_lib/.magicrc
	rm -rf $(INSTALL_DIRS)
