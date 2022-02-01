DOCKER_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
TOP_DIR := $(realpath $(DOCKER_DIR)/..)
include $(TOP_DIR)/openram.mk

TAG_DATE := $(shell date +%F)
all: build push

.PHONY: build
build:
	docker build -t vlsida/openram-ubuntu:${TAG_DATE} -f Dockerfile . | tee -i openram-ubuntu.log
	docker tag  vlsida/openram-ubuntu:${TAG_DATE} vlsida/openram-ubuntu:latest

.PHONY: push
push:
	docker login
	docker push vlsida/openram-ubuntu:latest

.PHONY: pull
pull:
	docker pull vlsida/openram-ubuntu:latest

mount:
	docker run -it -v $(TOP_DIR):/openram \
		-v $(SKY130_PDK):$(SKY130_PDK) \
		-e PDK_ROOT=$(PDK_ROOT) \
                -e OPENRAM_HOME=/openram/compiler \
                -e OPENRAM_TECH=/openram/technology \
		--user $(UID):$(GID) \
                vlsida/openram-ubuntu:latest
.PHONY: mount
