FROM alpine

RUN apk update
RUN apk add asciidoc findutils gzip
