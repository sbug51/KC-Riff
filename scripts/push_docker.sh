#!/bin/sh

set -eu

export VERSION=${VERSION:-0.0.0}
export GOFLAGS="'-ldflags=-w -s \"-X=github.com/sbug51/kc-riff/version.Version=$VERSION\" \"-X=github.com/sbug51/kc-riff/server.mode=release\"'"

docker build \
    --push \
    --platform=linux/arm64,linux/amd64 \
    --build-arg=VERSION \
    --build-arg=GOFLAGS \
    -f Dockerfile \
    -t sbug51/kc-riff -t sbug51/kc-riff:$VERSION \
    .
