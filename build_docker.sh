#!/usr/bin/env bash
#
# Title: build_docker.sh
# Description: This script builds docker images with and without references included
# Usage: ./build_docker.sh [with_references|without_references] [testing]
# Date Created: 2023-12-19 16:34
# Last Modified: Tue 19 Dec 2023 05:05:55 PM EST
# Author: Reagan Kelly (ylb9@cdc.gov)
#


if [[ ${1} == "without_references" ]]; then
    if [[ ${2} == "testing" ]]; then
        TAG=testing
    else
        TAG=latest
    fi
    echo "Building docker image without references as $TAG"
    DOCKER_BUILDKIT=1 docker build -t ghcr.io/cdcgov/varpipe_wgs_without_refs:$TAG -f Dockerfile.without_refs .
elif [[ ${1} == "with_references" ]]; then
    if [[ ${2} == "testing" ]]; then
        TAG=testing
    else
        TAG=latest
    fi
    echo "Building docker image with references as $TAG"
    DOCKER_BUILDKIT=1 docker build -t ghcr.io/cdcgov/varpipe_wgs_with_refs:$TAG -f Dockerfile.with_refs .
else
    if [[ ${1} == "testing" ]]; then
        TAG=testing
    else
        TAG=latest
    fi
    echo "Building docker images with & without references as $TAG"
    echo "Building docker image without references as $TAG"
    DOCKER_BUILDKIT=1 docker build -t ghcr.io/cdcgov/varpipe_wgs_without_refs:$TAG -f Dockerfile.without_refs .
    echo "Building docker image with references as $TAG"
    DOCKER_BUILDKIT=1 docker build -t ghcr.io/cdcgov/varpipe_wgs_with_refs:$TAG -f Dockerfile.with_refs .
fi

