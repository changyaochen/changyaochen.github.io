# Docker image for Jekyll to build github-pages
FROM alpine:latest

# Install basic packages
RUN apk update
RUN apk upgrade
RUN apk add curl wget bash cmake
RUN apk add ruby ruby-bundler ruby-dev ruby-irb ruby-rdoc \
    libatomic readline readline-dev \
    libxml2 libxml2-dev libxslt libxslt-dev zlib-dev zlib \
    libffi-dev build-base git nodejs

RUN export PATH="/root/.rbenv/bin:$PATH"
RUN rm -rf /var/cache/apk/*

# Install Jekyll and bundler
RUN gem install jekyll bundler

# Copy files over
WORKDIR /home
COPY . .

RUN bundle update
RUN bundle config set force_ruby_platform true
RUN bundle install

EXPOSE 4000 4000
CMD bundle exec jekyll serve --host 0.0.0.0
