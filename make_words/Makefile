build:
	docker build \
		--tag word-maker .

run:
	docker run \
		--name word-maker \
		--volume $(shell pwd):/opt/${PROJECT} \
		--interactive \
		--tty \
		--rm \
		word-maker \
