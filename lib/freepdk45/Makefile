CUR_DIR = $(shell pwd)
TEST_DIR = ${CUR_DIR}/tests

#MAKEFLAGS += -j 2

CONFIG_DIR = configs
OUT_DIRS = sp lib lef gds  verilog
$(shell   mkdir -p $(OUT_DIRS))

SRCS=$(wildcard $(CONFIG_DIR)/*.py)
SPICES=$(SRCS:.py=.sp)
all : $(SPICES) 

# Characterize and perform DRC/LVS
OPTS = -c
# Do not characterize or perform DRC/LVS
#OPTS += -n
# Verbosity
OPTS += -v
%.sp : %.py
	$(eval bname=$(basename $(notdir $<)))
	openram.py $(OPTS) $< 2>&1 > $(bname).log
	mv $(bname).lef lef
	mv $(bname).v verilog
	mv $(bname).sp sp
	mv $(bname).gds gds
	mv $(bname)*.lib lib

clean:
	rm -f *.log configs/*.pyc *~ *.gds *.lib *.sp *.v *.lef
	rm -f gds/* lef/* lib/* sp/* verilog/*

