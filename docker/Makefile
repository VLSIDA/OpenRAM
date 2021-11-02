
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
