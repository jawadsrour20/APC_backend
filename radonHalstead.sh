#!/bin/bash
# This script is used to run the radon halstead metrics on a given Python module


FILE_PATH=$1
FILE_NAME=$2

difficulty=$(radon hal ${FILE_PATH}/${FILE_NAME} | grep difficulty)

echo ${difficulty}