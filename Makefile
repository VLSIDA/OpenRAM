TOP_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
include $(TOP_DIR)/openram.mk

.DEFAULT_GOAL := install

# Skywater PDK SRAM library
SRAM_GIT_REPO ?= https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram.git
SRAM_GIT_COMMIT ?= 9fa642baaf01110b59ac2783beba9a4fda03aeaf
SRAM_LIBRARY ?= $(TOP_DIR)/sky130_fd_bd_sram

# Open PDKs
PDK_ROOT ?= $(TOP_DIR)/open_pdks
OPEN_PDKS_REPO ?= https://github.com/RTimothyEdwards/open_pdks.git
OPEN_PDKS ?= $(PDK_ROOT)/sky130/sky130A


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


$(OPEN_PDKS):
	git clone $(OPEN_PDKS_REPO) $(PDK_ROOT)
	cd $(PDK_ROOT) &&\
	$(PDK_ROOT)/configure --enable-sky130-pdk
	make -C $(PDK_ROOT)

.PHONY: $(SRAM_LIBRARY) $(OPEN_PDKS) $(INSTALL_DIRS) install

install: $(SRAM_LIBRARY) $(INSTALL_DIRS) $(OPEN_PDKS)
	@echo "Installing sky130 SRAM PDK..."
	@echo "PDK_ROOT='$(PDK_ROOT)'"
	@echo "SRAM_LIBRARY='$(SRAM_LIBRARY)'"
	@echo "OPEN_PDKS='$(OPEN_PDKS)'"
	make install
	@true

$(SRAM_LIBRARY):
	git clone $(SRAM_GIT_REPO) $(SRAM_LIBRARY)

.PHONY: $(SRAM_LIBRARY) $(INSTALL_DIRS) install


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

macros:
	cd macros && make

.PHONY: macros

tests:
	docker run -v $(TOP_DIR):/openram \
                -e OPENRAM_HOME=/openram/compiler \
                -e OPENRAM_TECH=/openram/technology \
                vlsida/openram-ubuntu:latest \
                sh -c "cd /openram/compiler/tests && ./regress.py -v -k"
.PHONY: tests


mount:
	docker run -it -v $(TOP_DIR):/openram \
                -e OPENRAM_HOME=/openram/compiler \
                -e OPENRAM_TECH=/openram/technology \
                vlsida/openram-ubuntu:latest
.PHONY: macros


uninstall:
	rm -rf $(SRAM_LIBRARY)
	rm -rf $(PDK_ROOT)
	rm -f $(INSTALL_BASE)/tech/.magicrc
	rm -f $(INSTALL_BASE)/mag_lib/.magicrc
	rm -f $(INSTALL_BASE)/lef_lib/.magicrc
	rm -f $(INSTALL_BASE)/maglef_lib/.magicrc
	rm -rf $(INSTALL_DIRS)
.PHONY: uninstall
