.PHONY: build serve all

image = github-page:latest

build:
	docker build -t $(image) .

serve:
	rm -rf _site && \
	docker run \
  		-it --rm \
		-p 4000:4000 \
		-v '$(PWD)':/home/tmp \
		$(image) \
		bundle exec jekyll serve --source /home/tmp \
		--host 0.0.0.0 --future --unpublished --incremental

all: build serve
