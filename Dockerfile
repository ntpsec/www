FROM alpine

RUN apk update
RUN apk add python3 asciidoc findutils gzip
