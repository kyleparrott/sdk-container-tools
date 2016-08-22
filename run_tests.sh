#!/bin/bash
echo "docker run -it -v $(pwd):/kubos-sdk -w /kubos-sdk kubostech/ci-test python -m unittest discover"
docker run -it -v $(pwd):/kubos-sdk -w /kubos-sdk kubostech/ci-test python -m unittest discover
