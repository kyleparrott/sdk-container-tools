#!/bin/bash
#This script takes 1 parameter as the tag for the sdk-container to be built

default_tag="latest"
container_repo="kubostech/kubos-sdk"

echo "Building kubostech/sdk-base container..."
docker build -t kubostech/sdk-base -f dist/Dockerfile.sdkbase dist/

echo "Building $container_repo:$default_tag..."
docker build -t kubostech/kubos-sdk:$default_tag -f dist/Dockerfile dist/

if [ ! -z $1 ]
then
    version_tag="$1"
    echo "Tagging $container_repo:$version_tag"
    docker tag $container_repo:$default_tag $container_repo:$version_tag
fi

