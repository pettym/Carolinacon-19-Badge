SHELL := /bin/bash
BUILD := build
CC := avr-gcc
CFLAGS := -Wall -Os -mmcu=attiny85

SOURCEFILE := "main.c"
COM := "ttyUSB0"


build: .make_build_dir
	$(CC) -w -o "$(BUILD)/out.bin" $(SOURCEFILE) $(CFLAGS)

hex: build
	avr-objcopy -j .text -j .data -O ihex "$(BUILD)/out.bin" "$(BUILD)/out.hex"

upload: hex
	avrdude -p t85 -P /dev/$(COM) -c avrisp -b 19200 -U "$(BUILD)/out.hex"

.make_build_dir:
	mkdir -p "$(BUILD)"
