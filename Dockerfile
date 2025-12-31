# Docker image for Jekyll to build github-pages
FROM alpine:latest

# Install Ruby and build dependencies in a single layer
RUN apk add --no-cache \
    ruby \
    ruby-bundler \
    ruby-dev \
    libxml2 \
    libxml2-dev \
    libxslt \
    libxslt-dev \
    zlib \
    zlib-dev \
    libffi \
    libffi-dev \
    build-base \
    git

# Install Jekyll and bundler
RUN gem install --no-document jekyll bundler

# Set working directory
WORKDIR /home

# Copy Gemfile first for better layer caching
COPY Gemfile Gemfile.lock* ./

# Install gems
RUN bundle config set force_ruby_platform true && \
    bundle install --jobs 4 --retry 3

# Copy rest of the site
COPY . .

EXPOSE 4000
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]
