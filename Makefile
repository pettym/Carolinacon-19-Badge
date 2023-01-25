

BUILD := "$(PWD)/output"


build:
	docker run --rm  -v "$(PWD)":/mnt/kibot:ro -w "/tmp/kibot" \
	-v "$(PWD)/output":/mnt/output \
	--user $(id -u):$(id -g) \
	-e dir=output \
	-e out_dir=output \
	ghcr.io/inti-cmnb/kicad6_auto_full:latest /bin/bash -c \
	"cp -r /mnt/kibot/* . && kibot -d /mnt/output"

