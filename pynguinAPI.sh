#!/bin/bash
# This script is used to run the pynguin API.

# INPUT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# set INPUT_DIR to second argument passed to shell script
INPUT_DIR=$1
# set INPUT_DIR to third argument passed to shell script
OUTPUT_DIR=$2
# set INPUT_DIR to fourth argument passed to shell script
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

