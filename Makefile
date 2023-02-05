SHELL	:= /bin/bash

BUILD	:= "$(PWD)/output"


build: .make-build-dir
	docker run --rm -w "/tmp/kibot" \
	-v "$(PWD)":/mnt/kibot:ro \
	-v "$(PWD)/output":/mnt/output \
	--user $(id -u):$(id -g) \
	-e dir=output \
	-e out_dir=output \
	ghcr.io/inti-cmnb/kicad6_auto_full:latest /bin/bash -c \
	"cp -r /mnt/kibot/* . && kibot -d /mnt/output ; chown -R $$(id -u):$$(id -g) /mnt/output"


.make-build-dir:
	mkdir -p "$(BUILD)"
