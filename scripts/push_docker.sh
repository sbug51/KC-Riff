#!/bin/sh

set -eu

export VERSION=${VERSION:-0.0.0}
export GOFLAGS="'-ldflags=-w -s \"-X=github.com/sbug51/kcriff/version.Version=$VERSION\" \"-X=github.com/sbug51/kcriff/server.mode=release\"'"

docker build \
    --push \
    --platform=linux/arm64,linux/amd64 \
    --build-arg=VERSION \
    --build-arg=GOFLAGS \
    -f Dockerfile \
    -t sbug51/kcriff -t sbug51/kcriff:$VERSION \
    .
