#!/bin/bash
# This script is used to run the pynguin API.

# INPUT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

INPUT_DIR=$1
OUTPUT_DIR=$2
MODULE_NAME=$3

# set docker Image Tag accirding to your container version
DOCKER_IMAGE_TAG="9ccbdc17"

# ~/pynguin/input:/input:ro
 # ~/pynguin/output/output
docker run \
    -v ~/APC_backend/input:/input:ro \
    -v ~/APC_backend/output:/output \
    -v ~/pynguin/package:/package:ro pynguin:${DOCKER_IMAGE_TAG} \
    --project-path ${INPUT_DIR} \
    --output-path ${OUTPUT_DIR} \
    --module-name ${MODULE_NAME} -v

