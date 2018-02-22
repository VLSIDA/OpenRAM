SUBDIRS := $(wildcard */.)
SUBDIRSCLEAN=$(addsuffix clean,$(SUBDIRS))

MAKEFLAGS += -j 2

all: $(SUBDIRS)

$(SUBDIRS):
	$(MAKE) -C $@

clean: 
	for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir $@; \
	done

.PHONY: all $(SUBDIRS) $(SUBDIRSCLEAN)
