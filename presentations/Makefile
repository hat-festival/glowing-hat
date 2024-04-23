ID=hatlights-presentation
run:
	docker run \
		--name ${ID} \
		--volume $(shell pwd):/opt/presentations \
		--publish 8000:8000 \
		--rm \
		--interactive \
		--tty \
		${ID} bash

build:
	docker build \
		--tag ${ID} .
