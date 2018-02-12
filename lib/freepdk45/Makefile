CUR_DIR = $(shell pwd)
TEST_DIR = ${CUR_DIR}/tests

MAKEFLAGS += -j 2

CONFIG_DIR = configs
OUT_DIRS = sp lib lef gds 
$(shell   mkdir -p $(OUT_DIRS))

SRCS=$(wildcard $(CONFIG_DIR)/*.py)
SPICES=$(SRCS:.py=.sp)
all : $(SPICES) 

%.sp : %.py
	openram.py -c $<
	mv ($basename $<).lef lef
	mv ($basename $<).sp sp
	mv ($basename $<).gds gds
	mv ($basename $<)\*.lib lib

clean:
	find . -name \*.pyc -exec rm {} \;
	find . -name \*~ -exec rm {} \;
	find . -name \*.lef -exec rm {} \;
	find . -name \*.lib -exec rm {} \;
	find . -name \*.sp -exec rm {} \;
	find . -name \*.gds -exec rm {} \;

