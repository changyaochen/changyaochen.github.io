.PHONY: build serve all

image=github-page:latest

build:
	docker build -t $(image) .

serve:
	rm -rf _site && \
	docker run \
		-it --rm \
		-p 4000:4000 \
		-v ${PWD}/_posts:/home/_posts \
		${image} \
		bundle exec jekyll serve \
		--future --unpublished --verbose --incremental --host 0.0.0.0

all: build serve
