SUBDIRS := $(wildcard */.)
SUBDIRSCLEAN=$(addsuffix clean,$(SUBDIRS))

MAKEFLAGS += -j 2
OPTS = -k

all: $(SUBDIRS)

$(SUBDIRS):
	$(MAKE) $(OPTS) -C $@

clean: 
	for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir $@; \
	done

.PHONY: all $(SUBDIRS) $(SUBDIRSCLEAN)
